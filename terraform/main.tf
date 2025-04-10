# Terraform configuration
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

# Azure provider configuration
provider "azurerm" {
  features {}
  resource_provider_registrations = "none"

  subscription_id = var.subscription_id
}
}