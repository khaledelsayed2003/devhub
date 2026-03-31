const projectStatCounts = document.querySelectorAll(".project-stat-count");

projectStatCounts.forEach((counter) => {
  const target = Number(counter.dataset.count || 0);
  const duration = 900;
  const start = performance.now();

  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    counter.textContent = String(Math.round(target * eased));

    if (progress < 1) {
      window.requestAnimationFrame(tick);
    } else {
      counter.textContent = String(target);
    }
  }

  window.requestAnimationFrame(tick);
});
