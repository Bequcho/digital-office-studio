const studioConfig = {
  phoneDisplay: "+995 551 73 93 33",
  phoneLink: "995551739333",
  whatsappNumber: "995551739333",
  whatsappDisplay: "+995 551 73 93 33",
  telegramDisplay: "@digital_studio_beqson",
  telegramLink: "https://t.me/digital_studio_beqson",
  email: "digitalstudiobeqson@gmail.com"
};

const navToggle = document.getElementById("navToggle");
const mainNav = document.getElementById("mainNav");
if (navToggle) {
  navToggle.addEventListener("click", () => mainNav.classList.toggle("open"));
}

document.querySelectorAll("[data-phone-display]").forEach(el => el.textContent = studioConfig.phoneDisplay);
document.querySelectorAll("[data-whatsapp-display]").forEach(el => el.textContent = studioConfig.whatsappDisplay);
document.querySelectorAll("[data-telegram-display]").forEach(el => el.textContent = studioConfig.telegramDisplay);
document.querySelectorAll("[data-email-display]").forEach(el => el.textContent = studioConfig.email);

const phoneHref = `tel:+${studioConfig.phoneLink}`;
const whatsappHref = `https://wa.me/${studioConfig.whatsappNumber}?text=${encodeURIComponent("Здравствуйте! Хочу обсудить сайт и привлечение клиентов.")}`;

document.getElementById("phoneCard").href = phoneHref;
document.getElementById("emailCard").href = `mailto:${studioConfig.email}`;
document.getElementById("whatsappCard").href = whatsappHref;
document.getElementById("telegramCard").href = studioConfig.telegramLink;
document.getElementById("whatsappLeadBtn").href = whatsappHref;
