const themeToggle = document.getElementById("themeToggle");
const heroStage = document.getElementById("heroStage");
const revealItems = document.querySelectorAll(".reveal");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const compactHero = window.matchMedia("(max-width: 1320px)");
const coarsePointer = window.matchMedia("(pointer: coarse)");
const menuToggle = document.getElementById("menuToggle");
const mobileMenu = document.getElementById("mobileMenu");
const userMenus = document.querySelectorAll(".user-menu");

function syncThemeButton() {
  if (!themeToggle) {
    return;
  }

  themeToggle.setAttribute(
    "aria-label",
    document.body.classList.contains("light-theme") ? "Switch to dark theme" : "Switch to light theme"
  );
}

function applySavedTheme() {
  const savedTheme = localStorage.getItem("devhub-theme");

  if (savedTheme === "light") {
    document.body.classList.add("light-theme");
  }

  syncThemeButton();
}

function toggleTheme() {
  document.body.classList.toggle("light-theme");
  localStorage.setItem(
    "devhub-theme",
    document.body.classList.contains("light-theme") ? "light" : "dark"
  );
  syncThemeButton();
}

function syncMenuButton() {
  if (!menuToggle || !mobileMenu) {
    return;
  }

  const isOpen = mobileMenu.classList.contains("is-open");
  menuToggle.setAttribute("aria-expanded", String(isOpen));
  menuToggle.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
}

function toggleMenu() {
  if (!mobileMenu) {
    return;
  }

  mobileMenu.classList.toggle("is-open");
  syncMenuButton();
}

function closeMenu() {
  if (!mobileMenu) {
    return;
  }

  mobileMenu.classList.remove("is-open");
  syncMenuButton();
}

function closeAllUserMenus(exceptMenu = null) {
  if (!userMenus.length) {
    return;
  }

  userMenus.forEach((menu) => {
    if (menu !== exceptMenu) {
      menu.removeAttribute("open");
    }
  });
}

function setupUserMenus() {
  if (!userMenus.length) {
    return;
  }

  userMenus.forEach((menu) => {
    const summary = menu.querySelector("summary");
    const links = menu.querySelectorAll("a");

    if (summary) {
      summary.addEventListener("click", () => {
        const willOpen = !menu.hasAttribute("open");
        if (willOpen) {
          closeAllUserMenus(menu);
        }
      });
    }

    links.forEach((link) => {
      link.addEventListener("click", () => {
        menu.removeAttribute("open");
      });
    });
  });

  document.addEventListener("click", (event) => {
    userMenus.forEach((menu) => {
      if (!menu.contains(event.target)) {
        menu.removeAttribute("open");
      }
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeAllUserMenus();
    }
  });
}

function setupHeroTilt() {
  if (!heroStage || reducedMotion.matches || compactHero.matches || coarsePointer.matches) {
    document.documentElement.style.setProperty("--hero-rotate-x", "0deg");
    document.documentElement.style.setProperty("--hero-rotate-y", "0deg");
    return;
  }

  let frameId = 0;
  let pointerX = 0;
  let pointerY = 0;

  function renderTilt() {
    frameId = 0;
    const rotateY = pointerX * 8;
    const rotateX = pointerY * -6;

    document.documentElement.style.setProperty("--hero-rotate-x", `${rotateX.toFixed(2)}deg`);
    document.documentElement.style.setProperty("--hero-rotate-y", `${rotateY.toFixed(2)}deg`);
  }

  function queueTilt() {
    if (!frameId) {
      frameId = window.requestAnimationFrame(renderTilt);
    }
  }

  heroStage.addEventListener("pointermove", (event) => {
    const rect = heroStage.getBoundingClientRect();
    const offsetX = (event.clientX - rect.left) / rect.width;
    const offsetY = (event.clientY - rect.top) / rect.height;

    pointerX = (offsetX - 0.5) * 2;
    pointerY = (offsetY - 0.5) * 2;
    queueTilt();
  });

  heroStage.addEventListener("pointerleave", () => {
    pointerX = 0;
    pointerY = 0;
    queueTilt();
  });
}

function setupReveals() {
  if (!revealItems.length) {
    return;
  }

  document.documentElement.classList.add("reveal-ready");

  if (reducedMotion.matches || !("IntersectionObserver" in window)) {
    revealItems.forEach((item) => item.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.05,
      rootMargin: "0px 0px -4% 0px"
    }
  );

  revealItems.forEach((item, index) => {
    item.style.transitionDelay = `${Math.min(index * 35, 260)}ms`;
    observer.observe(item);
  });
}

applySavedTheme();
setupHeroTilt();
setupReveals();
syncMenuButton();
setupUserMenus();

if (themeToggle) {
  themeToggle.addEventListener("click", toggleTheme);
}

if (menuToggle) {
  menuToggle.addEventListener("click", toggleMenu);
}

if (mobileMenu) {
  mobileMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });
}
