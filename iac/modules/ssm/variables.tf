variable "name" {
  description = "SSM parameter name"
  type        = string
}

variable "value" {
  description = "SSM parameter value"
  type        = string
  sensitive   = true
}

variable "type" {
  description = "SSM parameter type"
  type        = string
  default     = "SecureString"
}