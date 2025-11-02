# Deployment Guide for Render

This guide will help you deploy your Aigis Django application to Render using GitHub.

## Prerequisites

1. GitHub account
2. Render account (sign up at https://render.com - free tier available)
3. Git installed on your computer

## Step 1: Push to GitHub

1. **Initialize Git repository** (if not already done):
   ```bash
   cd mysite
   git init
   git add .
   git commit -m "Initial commit - Aigis landing page"
   ```

2. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Name it (e.g., "aigis-landing")
   - Don't initialize with README
   - Click "Create repository"

3. **Push your code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy on Render

### A. Create Web Service

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `aigis-landing` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn mysite.wsgi`
   - **Root Directory**: `mysite` (important!)

### B. Add Environment Variables

Click "Environment" tab and add:

```
SECRET_KEY=your-super-secret-key-here-generate-random-string
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost
DATABASE_URL=(Render will provide this automatically when you create PostgreSQL)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=pvarad2022@gmail.com
EMAIL_HOST_PASSWORD=zklrtkprlbrjrpvv
DEFAULT_FROM_EMAIL=Aigis <pvarad2022@gmail.com>
ADMIN_EMAIL=pvarad2022@gmail.com
```

**To generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### C. Create PostgreSQL Database

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Name it (e.g., `aigis-db`)
3. Select "Free" plan
4. Copy the **Internal Database URL**
5. Go back to your Web Service → Environment
6. Add environment variable: `DATABASE_URL` = (paste the URL)

### D. Run Migrations

1. In Render dashboard, go to your Web Service
2. Click "Shell" tab
3. Run:
   ```bash
   python manage.py migrate
   ```

### E. Create Superuser (Optional)

In the Shell:
```bash
python manage.py createsuperuser
```

## Step 3: Configure Static Files

Static files are handled by WhiteNoise automatically. The `collectstatic` command in the build step will collect all static files.

## Step 4: Test Your Deployment

1. Visit your Render URL: `https://your-app-name.onrender.com`
2. Test the signup form
3. Check that emails are being sent

## Troubleshooting

### Build Fails
- Check that `Root Directory` is set to `mysite`
- Verify `requirements.txt` has all dependencies
- Check build logs in Render dashboard

### Static Files Not Loading
- Ensure `STATIC_ROOT` is set in settings.py
- Verify `collectstatic` runs in build command
- Check WhiteNoise middleware is added

### Database Errors
- Ensure PostgreSQL database is created
- Verify `DATABASE_URL` environment variable is set
- Run migrations in Shell: `python manage.py migrate`

### Email Not Sending
- Verify Gmail App Password is correct
- Check environment variables are set
- Try console backend first: `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend`

## Free Tier Limits (Render)

- **Web Service**: Free tier available (spins down after 15 min inactivity)
- **PostgreSQL**: Free tier (90MB storage)
- **Bandwidth**: 100GB/month free

## Security Notes

- Never commit `SECRET_KEY` or passwords to GitHub
- Use environment variables for all sensitive data
- `DEBUG=False` in production
- Add your Render domain to `ALLOWED_HOSTS`

