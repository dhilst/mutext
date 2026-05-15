(() => {
  const audioHooks = {
    key: null,
    notify: null,
    ambience: null
  };

  window.mutextAudioHooks = audioHooks;

  const states = ["", "is-x", "is-check"];
  const labels = ["", "×", "✓"];

  document.querySelectorAll("[data-grid-cell]").forEach((cell) => {
    cell.dataset.state = "0";

    cell.addEventListener("click", () => {
      const next = (Number(cell.dataset.state) + 1) % states.length;
      cell.dataset.state = String(next);
      cell.classList.remove("is-x", "is-check");

      if (states[next]) {
        cell.classList.add(states[next]);
      }

      cell.textContent = labels[next];
      cell.setAttribute("aria-pressed", next === 0 ? "false" : "true");
    });
  });

  document.querySelectorAll("[data-fake-action]").forEach((button) => {
    button.addEventListener("click", () => {
      button.setAttribute("data-state", "queued");
      button.textContent = "QUEUED";
      window.setTimeout(() => {
        button.removeAttribute("data-state");
        button.textContent = button.dataset.fakeAction || "RUN";
      }, 1200);
    });
  });
})();
