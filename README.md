# Real User Survey

Simple Django application that captures qualitative survey responses for the getsva research initiative.

## Local setup

```bash
cd /Users/anuragsingh/Documents/GitHub/survey
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit http://127.0.0.1:8000 to fill out the form.

## Running tests

```bash
source .venv/bin/activate
python manage.py test
```

## Production deployment on Cloudflare Workers (survey.getsva.com)

Cloudflare’s Python Workers runtime can host this Django app as long as the database lives in a remotely reachable service (Neon, Supabase, RDS, etc.). The checklist below covers everything you need to do locally **before** the deploy, followed by the exact steps to run inside Cloudflare.

### Local preparation (one-time)

1. **Create env files**
   ```bash
   cd /Users/anuragsingh/Documents/GitHub/survey
   cp env.example env.local
   cp env.example env.production
   ```
   Fill in:
   - `ENVIRONMENT=local` (or `production` inside `env.production`)
   - `SECRET_KEY=` new random string
   - `DEBUG=false` in prod
   - `ALLOWED_HOSTS=survey.getsva.com,*.workers.dev`
   - `CSRF_TRUSTED_ORIGINS=https://survey.getsva.com,https://<your-worker>.workers.dev`
   - `DATABASE_URL=` connection string for your managed cloud DB (e.g., `postgres://user:pass@host:5432/dbname`)
   - Any email/S3 keys you need later.

2. **Update Django settings**
   - In `survey_site/settings.py`, load env vars (e.g., using `os.environ` or `django-environ`) and configure:
     - `SECRET_KEY = os.environ["SECRET_KEY"]`
     - `DEBUG = os.environ.get("DEBUG", "false").lower() == "true"`
     - `ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")`
     - `CSRF_TRUSTED_ORIGINS = os.environ["CSRF_TRUSTED_ORIGINS"].split(",")`
     - `DATABASES["default"]` from `DATABASE_URL` when present (fall back to SQLite for local dev).
   - Set `STATIC_ROOT = BASE_DIR / "staticfiles"` so `collectstatic` has a deterministic output.

3. **Expose Django as ASGI**
   - Ensure `survey_site/__init__.py` sets `DJANGO_SETTINGS_MODULE`.
   - Add `worker.py` at the repo root:
     ```python
     import os
     import django
     from asgiref.wsgi import WsgiToAsgi
     from django.core.wsgi import get_wsgi_application

     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "survey_site.settings")
     django.setup()
     asgi_app = WsgiToAsgi(get_wsgi_application())
     ```

4. **Create the Worker project**
   ```bash
   npm install -g wrangler
   wrangler init survey-worker --python --no-config
   mv worker.py functions
   ```
   Structure after this step (key files only):
   ```
   .
   ├─ functions/
   │  └─ _worker.py
   ├─ survey_site/
   ├─ surveys/
   ├─ worker.py
   ├─ wrangler.toml
   ```

5. **Wire the Worker entry point**
   - Replace `functions/_worker.py` with:
     ```python
     from worker import asgi_app

     async def on_fetch(request, env, ctx):
         return await asgi_app(request, env, ctx)
     ```
   - Set up `wrangler.toml`:
     ```toml
     name = "survey-getSVA"
     main = "functions/_worker.py"
     compatibility_date = "2025-11-17"
     compatibility_flags = ["python_workers"]

     [vars]
     DJANGO_SETTINGS_MODULE = "survey_site.settings"
     SECRET_KEY = "copy-from-.env.production"
     ALLOWED_HOSTS = "survey.getsva.com,*.workers.dev"
     CSRF_TRUSTED_ORIGINS = "https://survey.getsva.com,https://survey-getSVA.workers.dev"
     DATABASE_URL = "postgres://..."
     ```

6. **Install dependencies & freeze**
   ```bash
   python -m pip install -r requirements.txt
   pip freeze > requirements.txt  # ensures Worker build sees exact versions
   ```

7. **Static assets**
   ```bash
   python manage.py collectstatic --settings=survey_site.settings --noinput
   ```
   Upload the resulting `staticfiles/` directory to Cloudflare R2 (recommended) or keep it alongside the Worker and serve via WhiteNoise if the footprint is small.

8. **Local validation**
   ```bash
   python manage.py migrate --settings=survey_site.settings
   python manage.py test
   ```
   Run against your managed DB (temporarily allow your IP if needed) to confirm migrations succeed before the Worker touches production data.

Commit all necessary files (`worker.py`, `functions/_worker.py`, `wrangler.toml`, updated settings) and push so Wrangler can deploy from the clean state.

### Actions inside Cloudflare

1. **Authenticate Wrangler**
   ```bash
   cd /Users/anuragsingh/Documents/GitHub/survey
   wrangler login
   ```

2. **Deploy the Worker**
   ```bash
   wrangler deploy
   wrangler tail  # stream logs for sanity check
   ```
   Ensure your external database allows connections from Cloudflare’s egress IPs (most managed Postgres/Supabase instances permit this by default).

3. **Run migrations in the Worker environment**
   ```bash
   wrangler invoke survey-getSVA --command "python manage.py migrate --settings=survey_site.settings"
   ```

4. **Bind secrets (optional)**
   For values you do not want inside `wrangler.toml`, use:
   ```bash
   wrangler secret put SECRET_KEY
   wrangler secret put DATABASE_URL
   ```
   and remove them from the `[vars]` block.

5. **Attach the custom domain**
   - Cloudflare Dashboard → Workers & Pages → `survey-getSVA` → **Triggers** → Add Custom Domain → `survey.getsva.com`.
   - Accept the suggested CNAME DNS record; keep the proxy enabled (orange cloud).
   - Enable “Always use HTTPS” under SSL/TLS → Edge Certificates.

6. **Cache controls**
   - Create a Cache Rule: `if path starts_with "/admin"` or Request Method is `POST` → Cache level: Bypass.
   - Optional rule to cache static assets aggressively if served via Worker/R2.

7. **Smoke test**
   - Visit the workers.dev preview URL to ensure forms work and data lands in the DB.
   - After DNS propagates, verify `https://survey.getsva.com` for both survey form and `/admin`.
   - Monitor logs via `wrangler tail` during initial traffic.

Once these steps are complete, the Django app runs entirely inside Cloudflare’s Python Workers runtime while persisting data to your managed cloud database.

