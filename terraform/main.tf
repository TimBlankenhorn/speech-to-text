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


# Create resource group
resource "azurerm_resource_group" "rg" {
  name     = "speech-to-text-rg"
  location = "westeurope"
}

# Create virtual network
resource "azurerm_virtual_network" "vnet" {
  name                = "myVNet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

# Create subnet
resource "azurerm_subnet" "subnet" {
  name                 = "mySubnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Create public IP
resource "azurerm_public_ip" "public_ip" {
  name                = "myPublicIP"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Dynamic"
  sku                 = "Basic"
}

# Create network interface
resource "azurerm_network_interface" "nic" {
  name                = "myNIC"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "myNicConfiguration"
    subnet_id                     = azurerm_subnet.subnet.id
    public_ip_address_id          = azurerm_public_ip.public_ip.id
    private_ip_address_allocation = "Dynamic"
  }
}

# Create Linux virtual machine
resource "azurerm_linux_virtual_machine" "vm" {
  name                = "example-vm"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = "Standard_DS1_v2"
  admin_username      = "azureuser"
  network_interface_ids = [azurerm_network_interface.nic.id]

  admin_ssh_key {
    username   = "azureuser"
    public_key = file("/home/vboxuser/.ssh/id_ed25519.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-focal"
    sku       = "20_04-lts"
    version   = "latest"
  }
}

# Create Azure Cognitive Services Speech resource
resource "azurerm_cognitive_account" "speech_service" {
  name                = "speech-to-text-service"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "SpeechServices"
  
  # Available SKUs: F0 (free), S0 (standard)
  sku_name            = "F0"
  
  tags = {
    environment = "production"
    purpose     = "speech-to-text"
  }
}

# Output the Speech Service endpoint
output "speech_service_endpoint" {
  value       = azurerm_cognitive_account.speech_service.endpoint
  description = "The endpoint of the Speech Service"
}

# Output the Speech Service primary key
output "speech_service_key" {
  value       = azurerm_cognitive_account.speech_service.primary_access_key
  description = "The primary access key for the Speech Service"
  sensitive   = true
}
# Output the public IP of the VM
output "public_ip" {
  value       = azurerm_public_ip.public_ip.ip_address
  description = "Die öffentliche IP-Adresse der VM"
}