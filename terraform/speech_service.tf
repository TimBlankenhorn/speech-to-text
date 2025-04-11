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