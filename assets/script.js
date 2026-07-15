const META_PIXEL_ID = "2084492505493969";

(function initializeMetaPixel(windowObject, documentObject, scriptTag, pixelUrl, fbq, firstScript) {
  if (windowObject.fbq) return;

  fbq = windowObject.fbq = function () {
    fbq.callMethod ? fbq.callMethod.apply(fbq, arguments) : fbq.queue.push(arguments);
  };

  if (!windowObject._fbq) windowObject._fbq = fbq;
  fbq.push = fbq;
  fbq.loaded = true;
  fbq.version = "2.0";
  fbq.queue = [];

  firstScript = documentObject.createElement(scriptTag);
  firstScript.async = true;
  firstScript.src = pixelUrl;

  const existingScript = documentObject.getElementsByTagName(scriptTag)[0];
  existingScript.parentNode.insertBefore(firstScript, existingScript);
})(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");

window.fbq("init", META_PIXEL_ID);
window.fbq("track", "PageView");

const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector(".site-nav");

if (navToggle && siteNav) {
  navToggle.addEventListener("click", () => {
    const isOpen = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!isOpen));
    navToggle.classList.toggle("is-open", !isOpen);
    siteNav.classList.toggle("is-open", !isOpen);
  });

  siteNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.classList.remove("is-open");
      siteNav.classList.remove("is-open");
    });
  });
}

const revealItems = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.14 }
  );

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

const blueprintForm = document.querySelector("[data-blueprint-form]");

if (blueprintForm) {
  const status = blueprintForm.querySelector("[data-blueprint-status]");
  const submitButton = blueprintForm.querySelector("button[type='submit']");
  const guideSelect = blueprintForm.querySelector("select[name='interest']");
  const guideLabels = {
    "medicare": "Medicare Timeline Guide",
    "social-security": "Social Security & Income Guide",
    "tax": "Retirement Tax Guide",
    "family-protection": "Family Protection Guide",
  };
  const guideAliases = {
    medicare: "medicare",
    socialsecurity: "social-security",
    social: "social-security",
    income: "social-security",
    tax: "tax",
    taxes: "tax",
    family: "family-protection",
    protection: "family-protection",
    life: "family-protection",
  };

  if (guideSelect) {
    const params = new URLSearchParams(window.location.search);
    const requestedGuide = (params.get("guide") || params.get("interest") || "").toLowerCase().replace(/[^a-z]/g, "");
    const guideValue = guideAliases[requestedGuide] || params.get("guide") || params.get("interest");

    if (guideValue && guideLabels[guideValue]) {
      guideSelect.value = guideValue;
    }
  }

  blueprintForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const endpoint = blueprintForm.getAttribute("data-endpoint");
    if (!endpoint) {
      return;
    }

    const formData = new FormData(blueprintForm);
    const payload = {
      firstName: formData.get("firstName"),
      lastName: formData.get("lastName"),
      email: formData.get("email"),
      phone: formData.get("phone"),
      state: formData.get("state"),
      interest: formData.get("interest"),
      guideTitle: guideLabels[formData.get("interest")] || "Selected retirement guide",
      emailConsent: formData.get("emailConsent") === "on",
      smsConsent: formData.get("smsConsent") === "on",
      company: formData.get("company"),
      sourcePage: window.location.href,
    };

    if (status) {
      status.classList.remove("is-error");
      status.textContent = "Sending your verification email...";
    }

    if (submitButton) {
      submitButton.disabled = true;
    }

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Please try again.");
      }

      if (window.fbq) {
        window.fbq("track", "Lead", {
          content_name: payload.guideTitle,
          content_category: "Retirement Guide",
        });
      }

      blueprintForm.reset();

      if (status) {
        status.textContent = result.message || "Please check your email to confirm and download the guide.";
      }
    } catch (error) {
      if (status) {
        status.classList.add("is-error");
        status.textContent = error.message || "Something went wrong. Please call (402) 237-6592.";
      }
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
      }
    }
  });
}
