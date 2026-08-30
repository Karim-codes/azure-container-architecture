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

The Nginx container starts in HTTP mode until a Let's Encrypt certificate exists. After certificate issuance, it automatically switches to the TLS configuration on the next container restart.

After the DNS A record resolves to the VM, SSH into the server and issue the certificate:

```bash
ssh azureuser@40.120.63.116
cd ~/app
git pull
./scripts/issue-cert.sh cloudproject.coderaxa.com you@example.com
```

Replace `you@example.com` with the email address for Let's Encrypt expiry notices. Do not commit certificate material: local `certbot/`, `letsencrypt/`, keys, and `.env` files are ignored.

To renew later:

```bash
cd ~/app
docker compose run --rm certbot renew --webroot -w /var/www/certbot
docker compose up -d nginx_proxy
```

## Security notes

- SSH is restricted to `my_ip`; HTTP and HTTPS are public.
- Terraform state and provider files are ignored. Use an encrypted remote Terraform backend before team or production use.
- The Git URL must be public because cloud-init clones it without credentials.
- Treat the VM's initial cloud-init configuration as immutable. Updating the repository later requires SSHing to the VM and running `git pull && docker compose up -d --build`, or implementing a deployment pipeline.
