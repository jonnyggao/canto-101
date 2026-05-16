(function () {
  const pages = [
    { id: "home", href: "index.html", label: "Overview" },
    { id: "unit1", href: "unit1.html", label: "Unit 1 — Introduction" },
    { id: "unit2", href: "unit2.html", label: "Unit 2 — Greetings" },
    { id: "unit3", href: "unit3.html", label: "Unit 3 — Oneself" },
    { id: "unit4", href: "unit4.html", label: "Unit 4 — Manners" },
    { id: "unit5", href: "unit5.html", label: "Unit 5 — Numbers" },
    { id: "unit6", href: "unit6.html", label: "Unit 6 — Time" },
    { id: "unit7", href: "unit7.html", label: "Unit 7 — Getting around" },
    { id: "unit8", href: "unit8.html", label: "Unit 8 — Shopping" },
    { id: "unit9", href: "unit9.html", label: "Unit 9 — Transport" },
    { id: "unit10", href: "unit10.html", label: "Unit 10 — School" },
    { id: "unit11", href: "unit11.html", label: "Unit 11 — Emergency" },
    { id: "unit12", href: "unit12.html", label: "Unit 12 — Classroom" },
    { id: "unit13", href: "unit13.html", label: "Unit 13 — Social" },
    { id: "unit14", href: "unit14.html", label: "Unit 14 — HK places" },
    { id: "unit15", href: "unit15.html", label: "Unit 15 — Reflection" },
    { id: "appendix", href: "appendix-i.html", label: "Appendix I" },
  ];

  const current = document.body.dataset.current || "home";
  const navRoot = document.querySelector(".side-nav");
  const drawer = document.getElementById("drawer-nav");
  const toggle = document.getElementById("nav-toggle");
  const backdrop = document.getElementById("nav-backdrop");

  if (navRoot) {
    const ul = document.createElement("ul");
    for (const p of pages) {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = p.href;
      a.textContent = p.label;
      if (p.id === current) a.setAttribute("aria-current", "page");
      li.appendChild(a);
      ul.appendChild(li);
    }
    navRoot.appendChild(ul);
  }

  function setOpen(open) {
    if (!drawer || !toggle) return;
    drawer.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", String(open));
    if (backdrop) backdrop.hidden = !open;
  }

  toggle?.addEventListener("click", () => {
    const open = !drawer?.classList.contains("open");
    setOpen(open);
  });

  backdrop?.addEventListener("click", () => setOpen(false));

  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") setOpen(false);
  });

  /* Desktop: ensure drawer visible */
  window.addEventListener(
    "resize",
    () => {
      if (window.matchMedia("(min-width: 900px)").matches) {
        drawer?.classList.remove("open");
        if (backdrop) backdrop.hidden = true;
        toggle?.setAttribute("aria-expanded", "false");
      }
    },
    { passive: true },
  );
})();
