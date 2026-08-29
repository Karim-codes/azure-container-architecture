from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Azure Container Architecture", version="1.0.0")


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Azure Container Architecture</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,sans-serif;background:#07111f;color:#e6edf7}.wrap{max-width:1050px;margin:auto;padding:64px 24px}h1{font-size:clamp(2.2rem,6vw,4.4rem);margin:.2em 0}.eyebrow{color:#67e8f9;text-transform:uppercase;letter-spacing:.14em;font-weight:700}.lead{max-width:680px;color:#afbdd0;font-size:1.15rem;line-height:1.7}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px;margin-top:44px}.card{background:#0e1b2d;border:1px solid #1d3554;border-radius:16px;padding:22px}.card h2{margin:0 0 8px;font-size:1.15rem}.card p{margin:0;color:#aebcd0;line-height:1.55}.status{display:inline-flex;gap:9px;align-items:center;background:#0e2b26;color:#92f5d5;border-radius:999px;padding:8px 14px}.dot{height:9px;width:9px;border-radius:50%;background:#4ade80;box-shadow:0 0 12px #4ade80}code{color:#8be9fd}</style></head>
<body><main class="wrap"><p class="eyebrow">UK South · Production</p><h1>Containerized web architecture</h1><p class="lead">A FastAPI dashboard delivered through Nginx, Docker Compose, and Azure infrastructure managed with Terraform.</p><p class="status"><span class="dot"></span> Application online</p><section class="grid"><article class="card"><h2>Azure VM</h2><p>Ubuntu 22.04 LTS on a private subnet with a static public IP.</p></article><article class="card"><h2>Nginx proxy</h2><p>Public traffic is forwarded to <code>api:8000</code>.</p></article><article class="card"><h2>FastAPI</h2><p>Health and JSON status endpoints support monitoring.</p></article><article class="card"><h2>Security</h2><p>SSH is limited to the configured administrator CIDR.</p></article></section></main></body></html>"""


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/api/v1/status")
def status() -> dict[str, str]:
    return {"service": "azure-container-architecture", "status": "online", "region": "UK South"}
