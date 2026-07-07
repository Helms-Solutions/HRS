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

      blueprintForm.reset();

      if (status) {
        status.textContent = result.message || "Please check your email to confirm and download the blueprint.";
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
