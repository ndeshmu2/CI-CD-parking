provider "aws" {
  region  = "us-east-1"  # Adjust to your desired AWS region
  # It's recommended to use environment variables for AWS credentials for better security.
  # Jenkins will set these during the pipeline run.
}
