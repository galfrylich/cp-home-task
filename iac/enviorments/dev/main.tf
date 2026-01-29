module "vpc" {
  source = "../../modules/vpc"

  name = "dev-eks"

  azs = ["ca-central-1a", "ca-central-1b"]

  public_subnet_cidrs = [
    "10.0.1.0/24",
    "10.0.2.0/24"
  ]

  private_subnet_cidrs = [
    "10.0.101.0/24",
    "10.0.102.0/24"
  ]
}

module "eks" {
  source = "../../modules/eks"

  cluster_name = "dev-eks"
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnets

  instance_type = "t3.medium"
  desired_size  = 2
}

module "sqs" {
  source = "../../modules/sqs"
  name   = "dev-email-queue"
}

module "s3" {
  source      = "../../modules/s3"
  bucket_name = "dev-email-payloads-${data.aws_caller_identity.current.account_id}"
}

data "aws_caller_identity" "current" {}


variable "jwt_secret" {
  description = "JWT secret for API service"
  type        = string
  sensitive   = true
}


module "ssm_jwt" {
  source = "../../modules/ssm"

  name  = "/dev/email-service/jwt-secret"
  value = var.jwt_secret
}

module "alb" {
  source = "../../modules/alb"


  name = "service-1"
  vpc_id = module.vpc.vpc_id
  public_subnets = module.vpc.public_subnets


  cluster_name = module.eks.cluster_name
  node_sg_id = module.eks.node_security_group_id
  node_port = 30080
}

