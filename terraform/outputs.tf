output "public_ip_address" {
  description = "Static public IP address assigned to the web VM."
  value       = azurerm_public_ip.web.ip_address
}

output "ssh_connection_command" {
  description = "Command for connecting to the VM."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.web.ip_address}"
}
