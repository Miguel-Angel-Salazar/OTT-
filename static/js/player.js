(function () {
  const root = document.getElementById("movie-player");
  if (!root) return;

  const video = document.getElementById("player-video");
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

  function formatTime(seconds) {
    if (!isFinite(seconds) || seconds < 0) return "0:00";
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${String(s).padStart(2, "0")}`;
  }

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
      video.play();
    } else {
      video.pause();
    }
  }

  toggleBtns.forEach((btn) => btn.addEventListener("click", togglePlay));
  video.addEventListener("click", togglePlay);
  video.addEventListener("play", () => setPlayingIcons(true));
  video.addEventListener("pause", () => setPlayingIcons(false));

  video.addEventListener("timeupdate", () => {
    const pct = video.duration ? (video.currentTime / video.duration) * 100 : 0;
    progressFill.style.width = `${pct}%`;
    progressHandle.style.left = `${pct}%`;
    timeLabel.textContent = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
  });

  function seekFromEvent(event) {
    const rect = progress.getBoundingClientRect();
    const pct = Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width));
    if (video.duration) video.currentTime = pct * video.duration;
  }

  progress.addEventListener("click", seekFromEvent);

  backBtn?.addEventListener("click", () => {
    video.currentTime = Math.max(0, video.currentTime - 10);
  });

  fwdBtn?.addEventListener("click", () => {
    video.currentTime = Math.min(video.duration || 0, video.currentTime + 10);
  });

  function setVolumeFromEvent(event) {
    const rect = volumeTrack.getBoundingClientRect();
    const pct = Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width));
    video.volume = pct;
    volumeFill.style.width = `${pct * 100}%`;
  }

  volumeTrack?.addEventListener("click", setVolumeFromEvent);
  if (volumeFill) volumeFill.style.width = `${video.volume * 100}%`;

  fullscreenBtn?.addEventListener("click", () => {
    if (document.fullscreenElement) {
      document.exitFullscreen();
    } else {
      root.requestFullscreen?.();
    }
  });

  // Favorito (Mi Lista): solo visual por ahora — favorite_service.py no existe.
  // TODO: reemplazar por un fetch a /movie/<id>/favorito cuando exista la
  // tabla `favorites` conectada.
  favBtn?.addEventListener("click", () => {
    const isActive = favBtn.classList.toggle("is-active");
    favLabel.textContent = isActive ? "En mi lista" : "Mi Lista";
  });

  // Tracking de tiempo (RF-10, tabla `watch_history.minuto`): por ahora solo
  // deja el hook listo. TODO: cuando exista el endpoint, enviar aquí
  // Math.floor(video.currentTime / 60) periódicamente para persistirlo.
  setInterval(() => {
    if (video.paused || !video.duration) return;
    // fetch(`/movie/${root.dataset.movieId}/progreso`, { method: "POST", ... })
  }, 15000);
})();
