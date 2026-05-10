# Free Deployment Guide (Production Demo Path)

This guide shows practical no-cost deployment paths for the AgentDesk AI capstone.

## Deployment Goals

- Run Flask app publicly
- Connect app to a remote MCP server endpoint
- Store case lifecycle state (`tickets.json`)
- Keep secrets outside source code

## Option A (Most Practical): Oracle Cloud Always Free VM

Why:
- Always Free compute resources are officially documented by Oracle.

Official references:
- Always Free resources: https://docs.oracle.com/iaas/Content/FreeTier/resourceref.htm
- Oracle Free Tier FAQ: https://www.oracle.com/cloud/free/faq/

### Steps

1. Create Oracle Cloud Free Tier account.
2. Provision an Always Free Ubuntu VM.
3. SSH into VM and install:
   - `python3`, `pip`, `venv`, `git`, `nginx`
4. Clone repo and create virtual environment.
5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Add `.env` with:
   - `OPENAI_API_KEY`
   - `MODEL`
   - `EMBEDDING_MODEL`
   - `REMOTE_MCP_URL`
7. Run app with Gunicorn:

```bash
gunicorn -w 2 -b 0.0.0.0:5050 app:app
```

8. Put Nginx in front (reverse proxy `80 -> 5050`).
9. Use `systemd` service for auto-restart.

Result:
- Public URL for the capstone UI
- Stable hosting for recording/demo

## Option B (Free Demo Hosting): Hugging Face Spaces

Why:
- Free CPU hosting is available with documented baseline limits.

Official reference:
- Spaces overview and default resources: https://huggingface.co/docs/hub/main/spaces-overview

### Notes

- Good for demos and portfolio exposure.
- Free hardware limits can pause or throttle under heavy use.
- For production reliability, use VM-based deployment.

## Production Checklist (Even on Free Infra)

1. Secrets in env vars only.
2. Disable Flask debug in deployed runtime.
3. Add request logging and error logging.
4. Add backup of `data/tickets.json`.
5. Put rate limiting in front of POST endpoints.
6. Keep dependency versions pinned for repeatability.

## Suggested Runtime Commands

From chapter folder:

```bash
python app.py
```

For production process manager:

```bash
gunicorn -w 2 -b 0.0.0.0:5050 app:app
```

## Final Recommendation

For a free but reliable "enterprise-style" demo stack:
- Host on Oracle Cloud Always Free VM
- Use Nginx + Gunicorn
- Keep OpenAI key in env
- Connect capstone UI to a stable remote MCP server URL
