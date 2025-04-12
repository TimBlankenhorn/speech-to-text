resource "local_file" "ansible_inventory" {
  content = templatefile("templates/inventory.tftpl", {
    vm_ip = azurerm_public_ip.public_ip.ip_address
    ssh_user = "azureuser" 
    ssh_key_path = "/home/vboxuser/.ssh/id_ed25519"
  })
  filename = "../ansible/inventory.ini"

}

resource "local_sensitive_file" "backend_env" {
  content = <<-EOT
region=${azurerm_cognitive_account.speech_service.location}
api_key=${azurerm_cognitive_account.speech_service.primary_access_key}
sql_domain_name=${azurerm_mssql_server.example.fully_qualified_domain_name}
db_connection_string=mssql+pymssql://${azurerm_mssql_server.example.administrator_login}:${var.administrator_login_password}@${azurerm_mssql_server.example.fully_qualified_domain_name}:1433/${azurerm_mssql_database.example.name}
EOT
  filename = "../vm/backend/.env"
}

resource "local_file" "frontend_env" {
  content = <<-EOT
VITE_API_URL=http://${azurerm_public_ip.public_ip.ip_address}:8001/transcribe/
EOT
  filename = "../vm/frontend/.env"
}