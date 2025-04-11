resource "azurerm_mssql_server" "example" {
  name                         = "sql-${random_string.suffix.result}"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "dbadmin"
  administrator_login_password = var.administrator_login_password
}
resource "random_string" "suffix" {
  length  = 10
  special = false
  upper   = false
}

resource "azurerm_mssql_database" "example" {
  name         = "example-db"
  server_id    = azurerm_mssql_server.example.id
  collation    = "SQL_Latin1_General_CP1_CI_AS"
  license_type = "LicenseIncluded"
  max_size_gb  = 2
  sku_name     = "S0"
  enclave_type = "VBS"

  tags = {
    foo = "bar"
  }
}
resource "azurerm_mssql_firewall_rule" "allow_all" {
  name             = "AllowAllIPs"
  server_id        = azurerm_mssql_server.example.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}

output "sql_server_name" {
  description = "The name of the SQL server"
  value       = azurerm_mssql_server.example.name
}

output "sql_server_fqdn" {
  description = "The fully qualified domain name of the SQL server"
  value       = azurerm_mssql_server.example.fully_qualified_domain_name
}

output "database_connection_string" {
  description = "Connection string for the Azure SQL Database in SQLAlchemy format"
  value       = "mssql+pyodbc://${azurerm_mssql_server.example.administrator_login}:${var.administrator_login_password}@${azurerm_mssql_server.example.fully_qualified_domain_name}:1433/${azurerm_mssql_database.example.name}?driver=ODBC+Driver+18+for+SQL+Server&encrypt=yes&TrustServerCertificate=no&connection_timeout=30"
  sensitive   = true
}