# Retirement Blueprint Edge Function

This function powers the public website lead form without requiring the local agent portal.

Deploy function:

```bash
supabase functions deploy retirement-blueprint
```

Required secrets:

```bash
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=...
supabase secrets set RESEND_API_KEY=...
supabase secrets set RESEND_FROM_EMAIL="Helms Retirement Solutions <onboarding@resend.dev>"
supabase secrets set LEAD_NOTIFICATION_EMAIL=helmsretirement@gmail.com
supabase secrets set BLUEPRINT_DOWNLOAD_URL=https://uqkchegglsznnxbynhjp.supabase.co/storage/v1/object/public/lead-magnets/the-retirement-blueprint-helms-retirement-solutions.pdf
supabase secrets set PUBLIC_SITE_ORIGIN=https://helmsretirement.com
```

The homepage posts to:

```text
https://uqkchegglsznnxbynhjp.supabase.co/functions/v1/retirement-blueprint
```
