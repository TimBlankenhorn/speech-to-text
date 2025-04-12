# Add this to your Terraform config
resource "local_file" "ansible_inventory" {
  content = templatefile("templates/inventory.tftpl", {
    vm_ip = azurerm_public_ip.public_ip.ip_address
    ssh_user = "azureuser" 
    ssh_key_path = "/home/vboxuser/.ssh/id_ed25519"
  })
  filename = "../ansible/inventory.ini"
}