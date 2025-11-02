# Email Queue Setup - Automatic Email Sending

## How It Works

1. **During Signup**: Emails are queued in the database (instant, no 502 errors)
2. **Automatic Sending**: A scheduled job processes the queue every few minutes
3. **Result**: Emails sent automatically 2-3 minutes after signup

## Setup Automatic Email Sending on Render

### Option 1: Render Cron Job (Recommended)

1. Go to your Render dashboard: https://dashboard.render.com
2. Click **"New +"** → **"Cron Job"**
3. Configure:
   - **Name**: `send-pending-emails`
   - **Schedule**: `*/3 * * * *` (runs every 3 minutes)
   - **Command**: `cd mysite && python manage.py send_welcome_emails`
   - **Root Directory**: `.` (root of repo)
   - **Environment**: `Python 3`
   - **Branch**: `main`

4. **Add Environment Variables** (same as your web service):
   - Copy all environment variables from your Web Service
   - Especially important:
     - `DATABASE_URL` (to access Neon database)
     - `EMAIL_HOST_USER`
     - `EMAIL_HOST_PASSWORD`
     - `ADMIN_EMAIL`

### Option 2: Manual Testing

Test the email queue manually:

```bash
# In Render Shell (when available) or locally:
python manage.py send_welcome_emails
```

This will:
- Process emails queued 2+ minutes ago
- Send up to 20 emails per run
- Mark emails as sent when successful

## How It Works

1. **User signs up** → Email data saved to `PendingEmail` table (instant)
2. **Cron job runs** (every 3 minutes) → Processes queued emails
3. **Emails sent** → 2-3 minutes after signup automatically

## Commands

```bash
# Process queued emails (default: emails older than 2 minutes)
python manage.py send_welcome_emails

# Process with custom settings
python manage.py send_welcome_emails --limit 50 --delay-minutes 1
```

## Database Migration

After deployment, run the migration:

```bash
python manage.py migrate
```

This creates the `PendingEmail` table for queuing.

## Monitoring

Check email queue status:
- Render Logs → Cron Job logs
- Look for: `✓ Processed X emails: Y sent, Z failed`

