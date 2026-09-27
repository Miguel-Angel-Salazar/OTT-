// logica del reproductor de video (movie_detail.html)
(function () {
  const root = document.getElementById("movie-player");
  if (!root) return;

  const video = document.getElementById("player-video");
  if (!video) return;

  // al cargar el video, saltamos al minuto donde el usuario se habia quedado
  video.addEventListener("loadedmetadata", () => {
    const minuto = parseInt(video.dataset.minuto, 10);
    // aca minuto guarda segundos, para que el resume sea mas preciso
    if (!isNaN(minuto) && minuto > 0 && minuto < (video.duration || Infinity) - 1) {
      video.currentTime = minuto;
    }
  });

  const toggleBtns = [
    document.getElementById("player-toggle"),
    document.getElementById("player-play-btn"),
  ].filter(Boolean);

  const progress = document.getElementById("player-progress");
  const progressFill = document.getElementById("player-progress-fill");
  const progressHandle = document.getElementById("player-progress-handle");
  const backBtn = document.getElementById("player-back-10");
  const fwdBtn = document.getElementById("player-fwd-10");
  const volumeTrack = document.getElementById("player-volume-track");
  const volumeFill = document.getElementById("player-volume-fill");
  const timeLabel = document.getElementById("player-time");
  const fullscreenBtn = document.getElementById("player-fullscreen");
  const favBtn = document.getElementById("movie-fav-btn");
  const favLabel = document.getElementById("movie-fav-label");

  // pasa segundos a formato m:ss
  function formatTime(seconds) {
    if (!isFinite(seconds) || seconds < 0) return "0:00";
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${String(s).padStart(2, "0")}`;
  }

  // cambia entre el icono de play y el de pausa en todos los botones
  function setPlayingIcons(isPlaying) {
    root.querySelectorAll(".player__icon-play").forEach((el) => {
      el.style.display = isPlaying ? "none" : "";
    });
    root.querySelectorAll(".player__icon-pause").forEach((el) => {
      el.style.display = isPlaying ? "" : "none";
    });
  }

  function togglePlay() {
    if (video.paused) {
      // si el navegador dejo el video muteado por el autoplay, lo desmuteamos
      // al darle play manual, para que si suene
      try {
        if (video.muted) video.muted = false;
        if (video.volume === 0) video.volume = 1;
      } catch (e) {
        // ignorar
      }
      video.play();
    } else {
      video.pause();
    }
  }

  // varios botones (y el video mismo) hacen play/pausa
  toggleBtns.forEach((btn) => btn.addEventListener("click", togglePlay));
  video.addEventListener("click", togglePlay);
  video.addEventListener("play", () => setPlayingIcons(true));
  video.addEventListener("pause", () => setPlayingIcons(false));

  // va actualizando la barra de progreso y el tiempo mientras se reproduce
  video.addEventListener("timeupdate", () => {
    const pct = video.duration ? (video.currentTime / video.duration) * 100 : 0;
    if (progressFill) progressFill.style.width = `${pct}%`;
    if (progressHandle) progressHandle.style.left = `${pct}%`;
    if (timeLabel) {
      timeLabel.textContent = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
    }
  });

  // convierte una barra (progreso o volumen) en algo arrastrable con el mouse
  function makeScrubber(trackEl, onScrub) {
    if (!trackEl) return;

    function pctFromEvent(event) {
      const rect = trackEl.getBoundingClientRect();
      return Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width));
    }

    function onMouseMove(event) {
      onScrub(pctFromEvent(event));
    }

    function onMouseUp() {
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
    }

    trackEl.addEventListener("mousedown", (event) => {
      event.preventDefault();
      onScrub(pctFromEvent(event));
      document.addEventListener("mousemove", onMouseMove);
      document.addEventListener("mouseup", onMouseUp);
    });
  }

  // arrastrar la barra de progreso mueve el video a esa posicion
  makeScrubber(progress, (pct) => {
    if (video.duration) video.currentTime = pct * video.duration;
  });

  // arrastrar la barra de volumen cambia el volumen
  makeScrubber(volumeTrack, (pct) => {
    video.volume = pct;
    if (volumeFill) volumeFill.style.width = `${pct * 100}%`;
  });

  // recupera el volumen guardado de una sesion anterior
  try {
    const savedVolume = localStorage.getItem("player_volume");
    if (savedVolume !== null) {
      const v = parseFloat(savedVolume);
      video.volume = isFinite(v) ? v : video.volume;
      if (volumeFill) volumeFill.style.width = `${video.volume * 100}%`;
    }
  } catch (e) {}

  backBtn?.addEventListener("click", () => {
    video.currentTime = Math.max(0, video.currentTime - 10);
  });

  fwdBtn?.addEventListener("click", () => {
    video.currentTime = Math.min(video.duration || 0, video.currentTime + 10);
  });

  if (volumeFill) volumeFill.style.width = `${video.volume * 100}%`;

  // boton de pantalla completa, entra y sale
  fullscreenBtn?.addEventListener("click", () => {
    if (document.fullscreenElement) {
      document.exitFullscreen();
    } else {
      root.requestFullscreen?.();
    }
  });

  // boton de favorito (mi lista), solo cambia el estilo aca
  favBtn?.addEventListener("click", () => {
    const isActive = favBtn.classList.toggle("is-active");
    if (favLabel) favLabel.textContent = isActive ? "En mi lista" : "Mi Lista";
  });

  // guarda el volumen cada vez que cambia, para la proxima sesion
  const saveVolume = () => {
    try {
      localStorage.setItem("player_volume", String(video.volume));
    } catch (e) {}
  };

  video.addEventListener("volumechange", saveVolume);

  // cada 15 segundos manda el progreso al backend para guardar el historial
  setInterval(() => {
    if (video.paused || !video.duration) return;
    if (!root.dataset.movieId) return;

    // mandamos segundos para que el resume sea mas preciso
    fetch(`/movie/${root.dataset.movieId}/progreso`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ minuto: Math.floor(video.currentTime) }),
    }).catch(() => {});
  }, 15000);

  // manda el progreso de una vez cuando se pausa o se cierra la pagina
  function sendProgressNow() {
    if (!root.dataset.movieId || !video.duration) return;
    try {
      const payload = JSON.stringify({ minuto: Math.floor(video.currentTime) });
      const url = `/movie/${root.dataset.movieId}/progreso`;
      if (navigator.sendBeacon) {
        const blob = new Blob([payload], { type: "application/json" });
        navigator.sendBeacon(url, blob);
      } else {
        fetch(url, {
          method: "POST",
          credentials: "same-origin",
          headers: { "Content-Type": "application/json" },
          body: payload,
          keepalive: true,
        }).catch(() => {});
      }
    } catch (e) {
      // ignorar
    }
  }

  video.addEventListener("pause", sendProgressNow);
  window.addEventListener("pagehide", sendProgressNow);
  window.addEventListener("beforeunload", sendProgressNow);
})();
