import json
import boto3
import botocore.exceptions
import logging
import csv

log = logging.getLogger(__name__)

ses = boto3.Session()

log-events = {
  "awslogs": {
    "data": "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"
  }
}

class Scrapper:

    def __init__(self, session, region="us-east-1"):
        self.report_name = "/tmp/service-usage-report.csv"
        self.fildnames = ["account_id", "resource", "count"]
        self.session = session
        self.region = region
        self.account_id = self.session.client("sts").get_caller_identity()["Account"]

    def write_csv_file(self, rows):
        with open(self.report_name, 'a+') as csvfile:
            fieldnames = self.fildnames
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                del row["details"]
                writer.writerow(row)

    def check_kms_usage(self):
        keys = []
        try:
            client = self.session.client("kms", region_name=self.region)
            paginator = client.get_paginator("list_aliases")
            page_iter = paginator.paginate()
            for page in page_iter:
                keys.extend([item["AliasName"] for item in page["Aliases"] if item["AliasName"].split("/")[1] != "aws"])

            return {
                "account_id": self.account_id,
                "resource": "kms",
                "count": len(keys),
                "details": keys
            }
        except botocore.exceptions.ClientError as e:
            log.info(e)
            return {
                "account_id": self.account_id,
                "resource": "kms",
                "count": 0,
                "details": []
            }

    def check_kinesis_usage(self):
        streams = []
        client = self.session.client("kinesis", region_name=self.region)
        paginator = client.get_paginator("list_streams")
        page_iter = paginator.paginate()
        for page in page_iter:
            streams.extend(page["StreamNames"])
        return {
            "account_id": self.account_id,
            "resource": "kinesis",
            "count": len(streams),
            "details": streams
        }

    def check_step_functions_usage(self):
        state_machines = []
        client = self.session.client("stepfunctions", region_name=self.region)
        paginator = client.get_paginator("list_state_machines")
        page_iter = paginator.paginate()
        for page in page_iter:
            state_machines.extend([item["name"] for item in page["stateMachines"]])
        return {
            "account_id": self.account_id,
            "resource": "stepfunctions",
            "count": len(state_machines),
            "details": state_machines
        }

    def check_swf_usage(self):
        domains = []
        client = self.session.client("swf", region_name=self.region)
        paginator = client.get_paginator("list_domains")
        page_iter = paginator.paginate(registrationStatus="REGISTERED")
        for page in page_iter:
            domains.extend([item["name"] for item in page["domainInfos"]])
        return {
            "account_id": self.account_id,
            "resource": "swf",
            "count": len(domains),
            "details": domains
        }

    def check_ssm_usage(self):
        documents = []
        client = self.session.client("ssm", region_name=self.region)
        paginator = client.get_paginator("list_documents")
        page_iter = paginator.paginate(Filters=[{"Key": "Owner", "Values": ["Self"]}])
        for page in page_iter:
            documents.extend([item["Name"] for item in page["DocumentIdentifiers"]])
        return {
            "account_id": self.account_id,
            "resource": "ssm",
            "count": len(documents),
            "details": documents
        }

    def check_sage_maker_usage(self):
        notebook_instances = []
        client = self.session.client("sagemaker", region_name=self.region)
        paginator = client.get_paginator("list_notebook_instances")
        page_iter = paginator.paginate()
        for page in page_iter:
            notebook_instances.extend([item["NotebookInstanceName"] for item in page["NotebookInstances"]])
        return {
            "account_id": self.account_id,
            "resource": "sagemaker",
            "count": len(notebook_instances),
            "details": notebook_instances
        }

    def check_service_catalog_usage(self):
        portfolios = []
        client = self.session.client("servicecatalog", region_name=self.region)
        paginator = client.get_paginator("list_portfolios")
        page_iter = paginator.paginate()
        for page in page_iter:
            portfolios.extend([item["DisplayName"] for item in page["PortfolioDetails"]])
        return {
            "account_id": self.account_id,
            "resource": "service-catalog",
            "count": len(portfolios),
            "details": portfolios
        }

    def check_migration_hub_usage(self):
        tasks = []
        client = self.session.client("mgh", region_name=self.region)
        paginator = client.get_paginator("list_migration_tasks")
        page_iter = paginator.paginate()
        for page in page_iter:
            tasks.extend([item["MigrationTaskName"] for item in page["MigrationTaskSummaryList"]])
        return {
            "account_id": self.account_id,
            "resource": "migration-hub",
            "count": len(tasks),
            "details": tasks
        }

    def check_security_hub_usage(self):
        products = []
        try:
            client = self.session.client("securityhub", region_name=self.region)
            paginator = client.get_paginator("describe_products")
            page_iter = paginator.paginate()
            for page in page_iter:
                products.extend([item["ProductName"] for item in page["Products"]])
            return {
                "account_id": self.account_id,
                "resource": "security-hub",
                "count": len(products),
                "details": products
            }
        except botocore.exceptions.ClientError as e:
            log.info(e)
            return {
                "account_id": self.account_id,
                "resource": "security-hub",
                "count": 0,
                "details": []
            }

    def check_rekognition_usage(self):
        collections = []
        try:
            client = self.session.client("rekognition", region_name=self.region)
            paginator = client.get_paginator("list_collections")
            page_iter = paginator.paginate()
            for page in page_iter:
                collections.extend(page["CollectionIds"])
            return {
                "account_id": self.account_id,
                "resource": "rekognition",
                "count": len(collections),
                "details": collections
            }
        except botocore.exceptions.ClientError as e:
            log.info(e)
            return {
                "account_id": self.account_id,
                "resource": "security-hub",
                "count": 0,
                "details": []
            }

    def check_shield_usage(self):
        protections = []
        try:
            client = self.session.client("shield", region_name=self.region)
            paginator = client.get_paginator("list_protections")
            page_iter = paginator.paginate()
            for page in page_iter:
                protections.extend([item["Name"] for item in page["Protections"]])
            return {
                "account_id": self.account_id,
                "resource": "shield",
                "count": len(protections),
                "details": protections
            }
        except botocore.exceptions.ClientError as e:
            log.info(e)
            return {
                "account_id": self.account_id,
                "resource": "shield",
                "count": 0,
                "details": []
            }

    def check_mwaa_usage(self):
        environments = []
        try:
            client = self.session.client("mwaa", region_name=self.region)
            paginator = client.get_paginator("list_environments")
            page_iter = paginator.paginate()
            for page in page_iter:
                environments.extend(page["Environments"])
            return {
                "account_id": self.account_id,
                "resource": "mwaa",
                "count": len(environments),
                "details": environments
            }
        except botocore.exceptions.ClientError as e:
            log.info(e)
            return {
                "account_id": self.account_id,
                "resource": "mwaa",
                "count": 0,
                "details": []
            }

    def check_quick_sight_usage(self):
        templates = []
        try:
            client = self.session.client("quicksight", region_name=self.region)
            paginator = client.get_paginator("list_templates")
            page_iter = paginator.paginate(AwsAccountId=self.account_id)
            for page in page_iter:
                templates.extend([item["Name"] for item in page["TemplateSummaryList"]])
            return {
                "account_id": self.account_id,
                "resource": "quicksight",
                "count": len(templates),
                "details": templates
            }
        except botocore.exceptions.ClientError as e:
            log.info(e)
            return {
                "account_id": self.account_id,
                "resource": "quicksight",
                "count": 0,
                "details": []
            }

    def check_firehose_usage(self):
        client = self.session.client("firehose", region_name=self.region)
        resp = client.list_delivery_streams()
        return {
            "account_id": self.account_id,
            "resource": "firehose",
            "count": len(resp["DeliveryStreamNames"]),
            "details": resp["DeliveryStreamNames"]
        }

    def check_openseach_usage(self):
        client = self.session.client("opensearch", region_name=self.region)
        resp = client.list_domain_names()
        return {
            "account_id": self.account_id,
            "resource": "opensearch",
            "count": len(resp["DomainNames"]),
            "details": resp["DomainNames"]
        }

    def check_license_manager_usage(self):
        licenses = []
        try:

            client = self.session.client("license-manager", region_name=self.region)
            resp = client.list_licenses()
            licenses.extend([item["LicenseName"] for item in resp["Licenses"]])
            next_token = resp["NextToken"]
            while next_token:
                resp = client.list_licenses(NextToken=next_token)
                licenses.extend([item["LicenseName"] for item in resp["Licenses"]])
                try:
                    next_token = resp["NextToken"]
                except KeyError:
                    next_token = None

            return {
                "account_id": self.account_id,
                "resource": "license-manager",
                "count": len(licenses),
                "details": licenses
            }
        except botocore.exceptions.ClientError as e:
            log.info(e)
            return {
                "account_id": self.account_id,
                "resource": "license-manager",
                "count": 0,
                "details": []
            }

    def check_kafka_usage(self):
        clusters = []
        try:
            client = self.session.client("kafka", region_name=self.region)
            paginator = client.get_paginator("list_clusters")
            page_iter = paginator.paginate()
            for page in page_iter:
                clusters.extend([item["ClusterName"] for item in page["ClusterInfoList"]])
            return {
                "account_id": self.account_id,
                "resource": "kafka",
                "count": len(clusters),
                "details": clusters
            }
        except botocore.exceptions.ClientError as e:
            log.info(e)
            return {
                "account_id": self.account_id,
                "resource": "kafka",
                "count": 0,
                "details": []
            }

    def check_polly_usage(self):
        lexicons = []
        try:
            client = self.session.client("polly", region_name=self.region)
            paginator = client.get_paginator("list_lexicons")
            page_iter = paginator.paginate()
            for page in page_iter:
                lexicons.extend([item["Name"] for item in page["Lexicons"]])
            return {
                "account_id": self.account_id,
                "resource": "polly",
                "count": len(lexicons),
                "details": lexicons
            }
        except botocore.exceptions.ClientError as e:
            log.info(e)
            return {
                "account_id": self.account_id,
                "resource": "polly",
                "count": 0,
                "details": []
            }

    def check_serverless_repo_usage(self):
        applications = []
        try:
            client = self.session.client("serverlessrepo", region_name=self.region)
            paginator = client.get_paginator("list_applications")
            page_iter = paginator.paginate()
            for page in page_iter:
                applications.extend([item["Name"] for item in page["Applications"]])
            return {
                "account_id": self.account_id,
                "resource": "serverless-repo",
                "count": len(applications),
                "details": applications
            }
        except botocore.exceptions.ClientError as e:
            log.info(e)
            return {
                "account_id": self.account_id,
                "resource": "serverless-repo",
                "count": 0,
                "details": []
            }

    def check_macie_usage(self):
        findings = []
        try:
            client = self.session.client("macie2", region_name=self.region)
            paginator = client.get_paginator("list_findings")
            page_iter = paginator.paginate()
            for page in page_iter:
                findings.extend(page["Findings"])
            return {
                "account_id": self.account_id,
                "resource": "macie",
                "count": len(findings),
                "details": findings
            }
        except botocore.exceptions.ClientError as e:
            log.info(e)
            return {
                "account_id": self.account_id,
                "resource": "macie",
                "count": 0,
                "details": []
            }

    def generate_usage_report(self):
        usage_report = [
            self.check_kms_usage(),
            self.check_kinesis_usage(),
            self.check_step_functions_usage(),
            self.check_swf_usage(),
            self.check_ssm_usage(),
            self.check_sage_maker_usage(),
            self.check_service_catalog_usage(),
            self.check_migration_hub_usage(),
            self.check_security_hub_usage(),
            self.check_rekognition_usage(),
            self.check_shield_usage(),
            self.check_mwaa_usage(),
            self.check_quick_sight_usage(),
            self.check_firehose_usage(),
            self.check_openseach_usage(),
            self.check_license_manager_usage(),
            self.check_kafka_usage(),
            self.check_polly_usage(),
            self.check_serverless_repo_usage(),
            self.check_macie_usage()
        ]
        return usage_report


scrapper = Scrapper(ses)
reports = scrapper.generate_usage_report()
scrapper.write_csv_file(reports)
