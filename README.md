# Azure Containerized Web Architecture

A production-oriented web stack hosted in **Azure UK South**. Terraform provisions the network and Ubuntu VM; Docker Compose runs Nginx and a FastAPI architecture dashboard.

> Live site: [cloudProject.coderaxa.com](https://cloudProject.coderaxa.com)

## Architecture

```text
User
  │ HTTPS / HTTP (80, 443)
  ▼
Azure Public IP → NSG → Ubuntu 22.04 VM
                         │
                         ▼
                    Nginx reverse proxy
                         │ http://api:8000
                         ▼
                    FastAPI dashboard
                         │
                    Docker Compose
```

## Stack

- Microsoft Azure: resource group, VNet, subnet, static public IP, NSG, and VM
- Terraform: reproducible Azure infrastructure
- Docker Compose: application orchestration
- Nginx: reverse proxy
- FastAPI / Python 3.11: dashboard and API
- Let's Encrypt: TLS certificate provisioning (see below)

## Local application run

```bash
docker compose up --build
```

Open `http://localhost`, `http://localhost/health`, or `http://localhost/api/v1/status`.

## Infrastructure quickstart

Prerequisites: Terraform >= 1.3, Azure CLI authenticated with `az login`, an SSH public key at `~/.ssh/id_rsa.pub` (or an alternative passed with `ssh_public_key_path`), and a public GitHub repository URL.

```bash
cd terraform
terraform init
terraform apply \
  -var="my_ip=$(curl -s https://ifconfig.me)/32" \
  -var="github_repo_url=https://github.com/YOUR_GITHUB_USERNAME/azure-container-architecture.git"
```

Confirm the plan when Terraform prompts. The deployment output includes the static public IP and SSH command. Point the domain's DNS A record at that IP, then allow cloud-init a few minutes to clone the repository and start the containers.

## HTTPS / Let's Encrypt

The checked-in Nginx configuration intentionally starts on HTTP only, allowing the initial DNS validation and ACME HTTP-01 challenge to succeed. Port 443 is exposed by Docker Compose and allowed by the NSG for the TLS configuration you install after certificate issuance.

After the A record resolves to the VM, issue a certificate on the host (replace the email):

```bash
sudo apt-get update && sudo apt-get install -y certbot
sudo systemctl stop docker
sudo certbot certonly --standalone -d cloudProject.coderaxa.com -m you@example.com --agree-tos --no-eff-email
sudo systemctl start docker
```

Then mount `/etc/letsencrypt` read-only into `nginx_proxy` and use an Nginx TLS server block for port 443 that proxies to `http://api:8000`; redirect port 80 to HTTPS. Do not commit certificate material: local `certbot/`, `letsencrypt/`, keys, and `.env` files are ignored.

## Security notes

- SSH is restricted to `my_ip`; HTTP and HTTPS are public.
- Terraform state and provider files are ignored. Use an encrypted remote Terraform backend before team or production use.
- The Git URL must be public because cloud-init clones it without credentials.
- Treat the VM's initial cloud-init configuration as immutable. Updating the repository later requires SSHing to the VM and running `git pull && docker compose up -d --build`, or implementing a deployment pipeline.
