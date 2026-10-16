// encuesta de generos del onboarding: guarda la seleccion en memoria y
// habilita el boton de continuar cuando hay al menos un genero marcado
(function () {
  const root = document.getElementById("onboarding-root");
  if (!root) return;

  const buttons = root.querySelectorAll(".genre-btn");
  const counter = document.getElementById("genre-counter");
  const submit = document.getElementById("onboarding-submit");
  const selected = new Set();

  // actualiza el texto del contador y si el boton de submit esta habilitado
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

  // toggle de cada boton de genero (agregar/quitar del set)
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

  // boton final: por ahora solo redirige al home, todavia no guarda nada
  submit.addEventListener("click", () => {
    if (selected.size === 0) return;

    // pendiente: mandar los generos elegidos (Array.from(selected)) al
    // backend para guardarlos como preferencia del usuario en profiles
    window.location.href = root.dataset.homeUrl;
  });
})();
