// interacciones globales del dom (navbar, utilidades compartidas)

// navbar overlay del home: cuando el scroll pasa el umbral, se pone solido
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

// carruseles horizontales (home.html, movie_detail.html): flechas prev/next
// que mueven el track un "slide" (ancho de una card mas el gap)
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

// dropdown de perfil (navbar): abre/cierra con el avatar, se cierra al
// hacer click afuera o al apretar escape
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

    // click fuera del menu lo cierra
    document.addEventListener("click", (event) => {
      if (!menu.contains(event.target)) close();
    });

    // escape tambien lo cierra
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") close();
    });
  });
})();
