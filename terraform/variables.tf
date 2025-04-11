variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
  sensitive   = true
}

variable "administrator_login_password" {
  description = "Administrator password for database"
  type        = string
  sensitive   = true
}
