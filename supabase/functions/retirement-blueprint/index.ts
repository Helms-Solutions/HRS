const consentText =
  "I request the Retirement Blueprint and agree that Helms Retirement Solutions may contact me by email or phone about retirement, Medicare, and insurance-related options. I understand I can opt out at any time.";

const smsConsentText =
  "I agree that Helms Retirement Solutions may contact me by text message at the phone number provided. Message and data rates may apply. Consent is not required to receive the Retirement Blueprint.";

const formVersion = "retirement-blueprint-2026-07-06";
const publicFunctionUrl =
  "https://uqkchegglsznnxbynhjp.supabase.co/functions/v1/retirement-blueprint";
const defaultBlueprintDownloadUrl =
  "https://uqkchegglsznnxbynhjp.supabase.co/storage/v1/object/public/lead-magnets/the-retirement-blueprint-helms-retirement-solutions.pdf";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
};

type BlueprintRequest = {
  firstName?: string;
  lastName?: string;
  email?: string;
  phone?: string;
  state?: string;
  interest?: string;
  emailConsent?: boolean;
  smsConsent?: boolean;
  sourcePage?: string;
  company?: string;
};

function json(body: Record<string, unknown>, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...corsHeaders,
      "Content-Type": "application/json",
    },
  });
}

function escapeHtml(value: string | null | undefined) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function sha256(value: string) {
  const data = new TextEncoder().encode(value);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(hashBuffer))
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
}

function createToken() {
  const bytes = new Uint8Array(32);
  crypto.getRandomValues(bytes);
  return btoa(String.fromCharCode(...bytes))
    .replaceAll("+", "-")
    .replaceAll("/", "_")
    .replaceAll("=", "");
}

async function sendEmail(input: {
  to: string | string[];
  subject: string;
  html: string;
  replyTo?: string;
}) {
  const apiKey = Deno.env.get("RESEND_API_KEY");
  const from = Deno.env.get("RESEND_FROM_EMAIL");

  if (!apiKey || !from) {
    throw new Error("Resend is not configured.");
  }

  const response = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from,
      to: input.to,
      subject: input.subject,
      html: input.html,
      reply_to: input.replyTo,
    }),
  });

  if (!response.ok) {
    throw new Error(`Resend failed: ${response.status} ${await response.text()}`);
  }
}

async function supabase(path: string, init: RequestInit = {}) {
  const supabaseUrl = Deno.env.get("SUPABASE_URL");
  const serviceRoleKey =
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ??
    Deno.env.get("SUPABASE_SECRET_KEY") ??
    Deno.env.get("SERVICE_ROLE_KEY");

  if (!supabaseUrl || !serviceRoleKey) {
    throw new Error("Supabase service role is not configured.");
  }

  return fetch(`${supabaseUrl}/rest/v1/${path}`, {
    ...init,
    headers: {
      apikey: serviceRoleKey,
      Authorization: `Bearer ${serviceRoleKey}`,
      "Content-Type": "application/json",
      ...(init.headers ?? {}),
    },
  });
}

async function handleRequest(request: Request) {
  const body = (await request.json()) as BlueprintRequest;

  if (body.company) {
    return json({ ok: true });
  }

  const firstName = body.firstName?.trim();
  const lastName = body.lastName?.trim() ?? "";
  const email = body.email?.trim().toLowerCase();
  const phone = body.phone?.trim() ?? "";
  const state = body.state?.trim() ?? "";
  const interest = body.interest?.trim() ?? "";
  const sourcePage = body.sourcePage?.trim() ?? "";

  if (!firstName || !email || !body.emailConsent) {
    return json(
      { error: "Please provide your first name, email, and consent before requesting the blueprint." },
      400,
    );
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ error: "Please enter a valid email address." }, 400);
  }

  const token = createToken();
  const tokenHash = await sha256(token);
  const now = new Date().toISOString();

  const insertResponse = await supabase("retirement_blueprint_leads", {
    method: "POST",
    headers: { Prefer: "return=minimal" },
    body: JSON.stringify({
      first_name: firstName,
      last_name: lastName || null,
      email,
      phone: phone || null,
      state: state || null,
      interest: interest || null,
      email_consent: true,
      sms_consent: Boolean(body.smsConsent),
      consent_text: consentText,
      sms_consent_text: body.smsConsent ? smsConsentText : null,
      form_version: formVersion,
      source_page: sourcePage || null,
      user_agent: request.headers.get("user-agent"),
      ip_address: request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ?? null,
      verification_token_hash: tokenHash,
      verification_sent_at: now,
    }),
  });

  if (!insertResponse.ok) {
    console.error(await insertResponse.text());
    return json({ error: "We could not save your request. Please try again or call (402) 237-6592." }, 500);
  }

  const downloadUrl = `${publicFunctionUrl}?token=${encodeURIComponent(token)}`;

  await sendEmail({
    to: email,
    subject: "Confirm your Retirement Blueprint download",
    html: `
      <p>Hi ${escapeHtml(firstName)},</p>
      <p>Thanks for requesting the Retirement Blueprint from Helms Retirement Solutions.</p>
      <p><a href="${downloadUrl}">Confirm your email and download the blueprint</a>.</p>
      <p>If you did not request this, you can ignore this email.</p>
      <p>Helms Retirement Solutions<br />
      <a href="tel:+14022376592">(402) 237-6592</a></p>
      <p style="font-size:12px;color:#667085;">Helms Retirement Solutions is not affiliated with or endorsed by the U.S. government or the federal Medicare program.</p>
    `,
  });

  return json({ ok: true, message: "Please check your email to confirm and download the blueprint." });
}

async function handleDownload(request: Request) {
  const token = new URL(request.url).searchParams.get("token");
  const blueprintUrl = defaultBlueprintDownloadUrl;
  const notificationEmail = Deno.env.get("LEAD_NOTIFICATION_EMAIL");

  if (!token || !blueprintUrl) {
    return new Response("This download link is not available.", { status: 400, headers: corsHeaders });
  }

  const tokenHash = await sha256(token);
  const leadResponse = await supabase(
    `retirement_blueprint_leads?verification_token_hash=eq.${encodeURIComponent(tokenHash)}&select=*`,
    { method: "GET" },
  );

  if (!leadResponse.ok) {
    return new Response("This download link is invalid or expired.", { status: 404, headers: corsHeaders });
  }

  const leads = await leadResponse.json();
  const lead = leads[0];

  if (!lead) {
    return new Response("This download link is invalid or expired.", { status: 404, headers: corsHeaders });
  }

  const now = new Date().toISOString();
  const firstDownload = !lead.downloaded_at;

  await supabase(`retirement_blueprint_leads?id=eq.${lead.id}`, {
    method: "PATCH",
    body: JSON.stringify({
      email_verified_at: lead.email_verified_at ?? now,
      downloaded_at: lead.downloaded_at ?? now,
      last_downloaded_at: now,
      download_count: (lead.download_count ?? 0) + 1,
    }),
  });

  if (notificationEmail) {
    await sendEmail({
      to: notificationEmail,
      subject: firstDownload
        ? "Retirement Blueprint downloaded"
        : "Retirement Blueprint downloaded again",
      replyTo: lead.email,
      html: `
        <h2>Retirement Blueprint download</h2>
        <p><strong>Name:</strong> ${escapeHtml(`${lead.first_name ?? ""} ${lead.last_name ?? ""}`.trim())}</p>
        <p><strong>Email:</strong> ${escapeHtml(lead.email)}</p>
        <p><strong>Phone:</strong> ${escapeHtml(lead.phone)}</p>
        <p><strong>State:</strong> ${escapeHtml(lead.state)}</p>
        <p><strong>Interest:</strong> ${escapeHtml(lead.interest)}</p>
        <p><strong>Email consent:</strong> ${lead.email_consent ? "Yes" : "No"}</p>
        <p><strong>Text consent:</strong> ${lead.sms_consent ? "Yes" : "No"}</p>
        <p><strong>Downloaded at:</strong> ${escapeHtml(now)}</p>
      `,
    });
  }

  return Response.redirect(blueprintUrl, 302);
}

Deno.serve(async (request) => {
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  try {
    if (request.method === "POST") {
      return await handleRequest(request);
    }

    if (request.method === "GET") {
      return await handleDownload(request);
    }

    return json({ error: "Method not allowed." }, 405);
  } catch (error) {
    console.error(error);
    return json({ error: "Something went wrong. Please try again or call (402) 237-6592." }, 500);
  }
});
