terraform {
  backend "s3" {
    bucket         = "my-terraform-states-ca-central-1"
    key            = "eks/dev/terraform.tfstate"
    region         = "ca-central-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}