(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Reveal sections as they scroll into view; start the demo board when visible.
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      e.target.classList.add("in");
      e.target.querySelector(".board")?.classList.add("play");
      io.unobserve(e.target);
    }
  }, { threshold: 0.15 });
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  if (reduce) return;

  // Hero phones follow the pointer a little.
  const stage = document.getElementById("stage");
  if (stage && matchMedia("(pointer: fine)").matches) {
    addEventListener("pointermove", (e) => {
      stage.style.setProperty("--mx", (e.clientX / innerWidth - 0.5).toFixed(3));
      stage.style.setProperty("--my", (e.clientY / innerHeight - 0.5).toFixed(3));
    }, { passive: true });
  }

  // Feature phones straighten as they reach the middle of the screen.
  const phones = [...document.querySelectorAll(".feature .phone, .feature .poster")];
  let ticking = false;
  const update = () => {
    ticking = false;
    const mid = innerHeight / 2;
    for (const p of phones) {
      const r = p.getBoundingClientRect();
      const d = Math.min(1, Math.abs(r.top + r.height / 2 - mid) / innerHeight);
      p.style.setProperty("--t", (d * 1.6).toFixed(3));
    }
  };
  addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  update();
})();
