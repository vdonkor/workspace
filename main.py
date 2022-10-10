import json
import boto3
import botocore.exceptions
import logging
import csv

log = logging.getLogger(__name__)

ses = boto3.Session()


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
