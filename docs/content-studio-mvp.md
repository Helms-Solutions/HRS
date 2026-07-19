# HRS Content Studio MVP

Working branch: `codex/content-studio-mvp`
Tracking issue: #1

## Purpose
Create a secure internal content engine inside the HRS website. The first version generates, edits, and stores marketing drafts. Direct Meta publishing and scheduling are intentionally deferred until the daily workflow is proven.

## MVP content outputs
- Facebook post
- Reel script
- Carousel copy
- Blog article
- Email newsletter
- SMS message

## Recommended implementation order
1. Audit current hosting/runtime, routing, forms, and environment-variable handling.
2. Add secure server-side admin authentication.
3. Add the `/admin/content` shell and mobile navigation.
4. Implement the AI provider abstraction and generation endpoint.
5. Add editable structured results for all six formats.
6. Add persistent draft storage and draft management screens.
7. Add first-pass Medicare compliance flags.
8. Add tests, setup documentation, and regression checks for public pages.

## Data model
Each draft should support:
- id
- brand
- contentType
- title
- topic
- audience
- market
- tone
- callToAction
- body
- structuredContent
- status
- complianceFlags
- createdAt
- updatedAt
- scheduledAt (reserved)
- publishedAt (reserved)
- externalPostId (reserved)

## Security rules
- AI API keys remain server-side.
- Admin protection must be enforced server-side.
- No client-side-only password gate.
- Validate and limit generation inputs.
- Do not log secrets or full sensitive client information.

## Phase 2 extension points
- Meta Graph API connection
- Facebook and Instagram publishing
- Scheduling and content calendar
- Image generation
- Analytics
- Multiple brands, including VitaLink
