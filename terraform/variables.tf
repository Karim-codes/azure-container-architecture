variable "location" {
  description = "Azure region for all resources."
  type        = string
  default     = "uksouth"
}

variable "admin_username" {
  description = "Administrator account created on the VM."
  type        = string
  default     = "azureuser"
}

variable "my_ip" {
  description = "CIDR allowed to SSH to the VM, for example 203.0.113.10/32."
  type        = string

  validation {
    condition     = can(cidrhost(var.my_ip, 0))
    error_message = "my_ip must be a valid CIDR block, such as 203.0.113.10/32."
  }
}

variable "ssh_public_key_path" {
  description = "Path to the SSH public key used for the VM administrator."
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "github_repo_url" {
  description = "Public HTTPS Git URL cloned by cloud-init."
  type        = string

  validation {
    condition     = startswith(var.github_repo_url, "https://github.com/")
    error_message = "github_repo_url must be a public GitHub HTTPS URL."
  }
}
