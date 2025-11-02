# Quick Start - Deploy to Render

## Files Created ✅

All deployment files are ready:
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Render start command
- ✅ `runtime.txt` - Python version
- ✅ `.gitignore` - Git ignore rules
- ✅ `DEPLOYMENT.md` - Full deployment guide
- ✅ `settings.py` - Updated for production

## Next Steps

### 1. Push to GitHub

```bash
cd mysite
git init
git add .
git commit -m "Ready for deployment"
git branch -M main

# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Deploy on Render

1. **Sign up**: https://render.com
2. **New Web Service**: Connect your GitHub repo
3. **Settings**:
   - Root Directory: `mysite`
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn mysite.wsgi`
4. **Add Environment Variables** (see DEPLOYMENT.md)
5. **Create PostgreSQL Database** on Render
6. **Run Migrations** in Render Shell

### 3. Generate SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Use this as your `SECRET_KEY` environment variable.

## Important Notes

- Root Directory must be `mysite` (not root of repo)
- All environment variables must be set
- Database migrations must run after first deploy
- Free tier: Service sleeps after 15 min inactivity (wakes on next request)

See `DEPLOYMENT.md` for detailed instructions.

