# HRS Content Studio setup

The Content Studio is available at `/admin/content.html`.

## Features
- Facebook post templates and editable copy
- First-pass Medicare marketing checks
- Local draft storage
- One-click Facebook copy
- Matching 1024 x 1024 AI image generation
- Image download

## Vercel environment variable
Add this environment variable to the HRS Vercel project and redeploy:

- `OPENAI_API_KEY`: OpenAI API project key with image-generation access

The key is read only by `/api/generate-image.js` and must never be placed in frontend JavaScript.

## Current security note
The page is marked `noindex`, but this static MVP is not yet authenticated. Do not place private client information in it. Authentication should be the next release before adding CRM data, shared cloud drafts, scheduling, or direct Meta publishing.

## Posting workflow
1. Open `/admin/content.html`.
2. Choose a template and topic.
3. Generate and edit the Facebook copy.
4. Select **Create image**.
5. Download the image.
6. Select **Copy for Facebook** and paste the copy into the HRS Facebook Page post composer.
