// Interacciones globales del DOM (navbar, utilidades compartidas).

(function () {
  const overlayNavbar = document.querySelector(".navbar--overlay");
  if (!overlayNavbar) return;

  const SCROLL_THRESHOLD = 55;

  function updateNavbarState() {
    overlayNavbar.classList.toggle("is-scrolled", window.scrollY > SCROLL_THRESHOLD);
  }

  window.addEventListener("scroll", updateNavbarState, { passive: true });
  updateNavbarState();
})();

// Carruseles horizontales (home.html, movie_detail.html): flechas prev/next
// que desplazan el track un "slide" (ancho de una card + gap).
(function () {
  document.querySelectorAll("[data-carousel]").forEach((carousel) => {
    const track = carousel.querySelector("[data-carousel-track]");
    const prevBtn = carousel.querySelector("[data-carousel-prev]");
    const nextBtn = carousel.querySelector("[data-carousel-next]");
    if (!track) return;

    function scrollByStep(direction) {
      const step = track.clientWidth * 0.8;
      track.scrollBy({ left: direction * step, behavior: "smooth" });
    }

    prevBtn?.addEventListener("click", () => scrollByStep(-1));
    nextBtn?.addEventListener("click", () => scrollByStep(1));
  });
})();

// Dropdown de perfil (navbar): abre/cierra al click en el avatar, se cierra
// al hacer click afuera o al presionar Escape.
(function () {
  document.querySelectorAll("[data-profile-menu]").forEach((menu) => {
    const trigger = menu.querySelector("[data-profile-trigger]");
    const dropdown = menu.querySelector("[data-profile-dropdown]");
    if (!trigger || !dropdown) return;

    function close() {
      dropdown.classList.remove("is-open");
      trigger.setAttribute("aria-expanded", "false");
    }

    function toggle(event) {
      event.stopPropagation();
      const isOpen = dropdown.classList.toggle("is-open");
      trigger.setAttribute("aria-expanded", String(isOpen));
    }

    trigger.addEventListener("click", toggle);

    document.addEventListener("click", (event) => {
      if (!menu.contains(event.target)) close();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") close();
    });
  });
})();
