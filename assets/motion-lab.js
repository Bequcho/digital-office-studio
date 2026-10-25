(() => {
  "use strict";

  const preview = document.querySelector("[data-ml-preview]");
  const steps = [...document.querySelectorAll("[data-ml-step]")];
  const pills = [...document.querySelectorAll("[data-ml-target]")];
  const scenes = [...document.querySelectorAll("[data-ml-scene]")];
  const address = document.querySelector("[data-ml-address]");

  if (!preview || !steps.length) return;

  const sceneNames = new Set(["wireframe", "design", "store", "ai"]);
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function activate(name) {
    if (!sceneNames.has(name) || preview.dataset.stage === name) return;
    preview.dataset.stage = name;
    for (const step of steps) {
      step.classList.toggle("is-active", step.dataset.mlStep === name);
    }
    for (const pill of pills) {
      if (pill.dataset.mlTarget === name) {
        pill.setAttribute("aria-current", "step");
      } else {
        pill.removeAttribute("aria-current");
      }
    }
    for (const scene of scenes) {
      const active = scene.dataset.mlScene === name;
      scene.setAttribute("aria-hidden", String(!active));
      scene.inert = !active;
    }
    const activeStep = steps.find(step => step.dataset.mlStep === name);
    if (address && activeStep?.dataset.url) address.textContent = activeStep.dataset.url;
  }

  // Keep the first story scene usable if a visitor does not scroll or uses a keyboard.
  preview.dataset.stage = "initial";
  activate("wireframe");

  for (const pill of pills) {
    pill.addEventListener("click", () => {
      const step = steps.find(item => item.dataset.mlStep === pill.dataset.mlTarget);
      if (!step) return;
      activate(pill.dataset.mlTarget);
      step.scrollIntoView({behavior: reducedMotion ? "auto" : "smooth", block: "center"});
    });
  }

  if ("IntersectionObserver" in window) {
    const visible = new Map();
    const stageObserver = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (entry.isIntersecting) visible.set(entry.target.dataset.mlStep, entry.intersectionRatio);
        else visible.delete(entry.target.dataset.mlStep);
      }
      if (visible.size) {
        const next = [...visible.entries()].sort((a, b) => b[1] - a[1])[0][0];
        activate(next);
      }
    }, {rootMargin: "-28% 0px -28% 0px", threshold: [0, .1, .35, .6, .85]});
    steps.forEach(step => stageObserver.observe(step));

    if (!reducedMotion) {
      document.documentElement.classList.add("ml-js");
      const revealObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        });
      }, {threshold: .09, rootMargin: "0px 0px -25px 0px"});
      document.querySelectorAll("[data-reveal]").forEach(el => revealObserver.observe(el));
    }
  }

  // A small, real local interaction in the illustrated store (no checkout or purchase).
  const addButton = document.querySelector("[data-ml-add]");
  const count = document.querySelector("[data-ml-cart]");
  let cartItems = 0;
  addButton?.addEventListener("click", () => {
    cartItems += 1;
    if (count) {
      count.textContent = String(cartItems);
      count.setAttribute("aria-label", `${count.dataset.label || "Items in cart"}: ${cartItems}`);
    }
    addButton.classList.add("is-added");
    window.setTimeout(() => addButton.classList.remove("is-added"), 350);
  });

  // This is explicitly a scripted UI sample, not a call to a live AI endpoint.
  const response = document.querySelector("[data-ml-ai-response]");
  document.querySelectorAll("[data-ml-question]").forEach(button => {
    button.addEventListener("click", () => {
      if (!response) return;
      response.textContent = button.dataset.answer || "";
    });
  });
})();
