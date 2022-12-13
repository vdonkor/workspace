terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}
provider "aws" {
  region = var.region
}



provider "aws" {
  alias   = "dest"
  region  = var.region
  assume_role {
    role_arn = "myrole"
    session_name = "mysession"
  }
  default_tags {
    tags = {
      ManagedBy = "mymanager"
      Id = "myid"
    }
  }
}
