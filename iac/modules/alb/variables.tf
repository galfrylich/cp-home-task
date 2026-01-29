variable "name" {
description = "Base name for ALB resources"
type = string
}


variable "vpc_id" {
description = "VPC ID where ALB will be created"
type = string
}


variable "public_subnets" {
description = "Public subnet IDs for the ALB"
type = list(string)
}


variable "cluster_name" {
description = "EKS cluster name (used to find worker nodes)"
type = string
}


variable "node_port" {
description = "Kubernetes NodePort exposed by the service"
type = number
}


variable "health_check_path" {
description = "HTTP health check path"
type = string
default = "/health"
}


variable "listener_port" {
description = "ALB listener port"
type = number
default = 80
}

variable "node_sg_id" {
description = "Security group ID of EKS worker nodes"
type = string
}