(function () {
  const root = document.getElementById("movie-player");
  if (!root) return;

  const video = document.getElementById("player-video");
  if (!video) return;

  video.addEventListener("loadedmetadata", () => {
    const minuto = parseInt(video.dataset.minuto, 10);
    // `minuto` here stores seconds for finer-grained resume support
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
      // Unmute on user-initiated play to allow audio in browsers that
      // block autoplay with sound. Respect existing volume if set.
      try {
        if (video.muted) video.muted = false;
        if (video.volume === 0) video.volume = 1;
      } catch (e) {
        // ignore
      }
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
    if (progressFill) progressFill.style.width = `${pct}%`;
    if (progressHandle) progressHandle.style.left = `${pct}%`;
    if (timeLabel) {
      timeLabel.textContent = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
    }
  });

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

  makeScrubber(progress, (pct) => {
    if (video.duration) video.currentTime = pct * video.duration;
  });

  makeScrubber(volumeTrack, (pct) => {
    video.volume = pct;
    if (volumeFill) volumeFill.style.width = `${pct * 100}%`;
  });

  // persist volume between sessions
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

  fullscreenBtn?.addEventListener("click", () => {
    if (document.fullscreenElement) {
      document.exitFullscreen();
    } else {
      root.requestFullscreen?.();
    }
  });

  favBtn?.addEventListener("click", () => {
    const isActive = favBtn.classList.toggle("is-active");
    if (favLabel) favLabel.textContent = isActive ? "En mi lista" : "Mi Lista";
  });

  // save volume when changed by scrubber
  const saveVolume = () => {
    try {
      localStorage.setItem("player_volume", String(video.volume));
    } catch (e) {}
  };

  video.addEventListener("volumechange", saveVolume);

  setInterval(() => {
    if (video.paused || !video.duration) return;
    if (!root.dataset.movieId) return;

    // send seconds for finer resume granularity
    fetch(`/movie/${root.dataset.movieId}/progreso`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ minuto: Math.floor(video.currentTime) }),
    }).catch(() => {});
  }, 15000);

  // send progress immediately (in minutes) — used on pause/unload
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
      // ignore
    }
  }

  video.addEventListener("pause", sendProgressNow);
  window.addEventListener("pagehide", sendProgressNow);
  window.addEventListener("beforeunload", sendProgressNow);
})();