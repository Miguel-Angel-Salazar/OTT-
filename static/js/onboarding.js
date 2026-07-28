(function () {
  const root = document.getElementById("onboarding-root");
  if (!root) return;

  const buttons = root.querySelectorAll(".genre-btn");
  const counter = document.getElementById("genre-counter");
  const submit = document.getElementById("onboarding-submit");
  const selected = new Set();

  function updateFooter() {
    const count = selected.size;

    if (count === 0) {
      counter.textContent = "Selecciona al menos un género";
      counter.classList.remove("has-selection");
    } else {
      counter.textContent = `${count} ${count === 1 ? "género seleccionado" : "géneros seleccionados"}`;
      counter.classList.add("has-selection");
    }

    submit.disabled = count === 0;
    submit.classList.toggle("is-enabled", count > 0);
  }

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const genre = btn.dataset.genre;

      if (selected.has(genre)) {
        selected.delete(genre);
        btn.classList.remove("is-selected");
      } else {
        selected.add(genre);
        btn.classList.add("is-selected");
      }

      updateFooter();
    });
  });

  submit.addEventListener("click", () => {
    if (selected.size === 0) return;

    // TODO: enviar los géneros elegidos (Array.from(selected)) al backend
    // cuando exista profile_service.py, para guardarlos como preferencias
    // del usuario en la tabla `profiles`.
    window.location.href = root.dataset.homeUrl;
  });
})();
