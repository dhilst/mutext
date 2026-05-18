(() => {
  const audioHooks = {
    key: null,
    notify: null,
    ambience: null
  };

  window.mutextAudioHooks = audioHooks;

  const states = ["", "is-x", "is-check"];
  const labels = ["", "✕", "✓"];
  const storageKey = "mutext-grid-" + location.pathname;

  function saveGrid(cells) {
    const data = Array.from(cells).map((c) => Number(c.dataset.state));
    localStorage.setItem(storageKey, JSON.stringify(data));
  }

  function loadGrid() {
    try { return JSON.parse(localStorage.getItem(storageKey)); }
    catch { return null; }
  }

  const cells = document.querySelectorAll("[data-grid-cell]");
  const saved = loadGrid();

  cells.forEach((cell, i) => {
    const initial = saved && saved[i] != null ? saved[i] : 0;
    cell.dataset.state = String(initial);
    if (states[initial]) cell.classList.add(states[initial]);
    if (labels[initial]) cell.textContent = labels[initial];
    if (initial) cell.setAttribute("aria-pressed", "true");

    cell.addEventListener("click", () => {
      const next = (Number(cell.dataset.state) + 1) % states.length;
      cell.dataset.state = String(next);
      cell.classList.remove("is-x", "is-check");

      if (states[next]) {
        cell.classList.add(states[next]);
      }

      cell.textContent = labels[next];
      cell.setAttribute("aria-pressed", next === 0 ? "false" : "true");
      saveGrid(cells);
    });
  });

  const clearBtn = document.querySelector("[data-clear-grid]");
  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      if (!confirm("Are you sure you want to clear the board?")) return;
      cells.forEach((cell) => {
        cell.dataset.state = "0";
        cell.classList.remove("is-x", "is-check");
        cell.textContent = "";
        cell.setAttribute("aria-pressed", "false");
      });
      localStorage.removeItem(storageKey);
    });
  }

  const submitButtons = new Set();

  document.querySelectorAll("[data-puzzle-answer]").forEach((answerEl) => {
    const answer = answerEl.getAttribute("data-puzzle-answer").split(",").map(s => s.trim().toLowerCase());
    const submitBtn = answerEl.querySelector('[data-fake-action="SUBMIT"]');
    const selects = answerEl.querySelectorAll("select[data-answer-dim]");

    if (!submitBtn || selects.length === 0) return;
    submitButtons.add(submitBtn);

    function getSelected() {
      return Array.from(selects).map(s => s.value.trim().toLowerCase());
    }

    function checkAnswer(tokens) {
      return answer.length === tokens.length && answer.every((val, i) => val === tokens[i]);
    }

    submitBtn.addEventListener("click", (e) => {
      e.stopImmediatePropagation();
      const tokens = getSelected();
      const correct = checkAnswer(tokens);

      if (correct) {
        submitBtn.textContent = "CORRECT";
        submitBtn.classList.remove("button-primary");
        submitBtn.classList.add("button-correct");
        spawnConfetti();
        const reveal = document.getElementById("lore-reveal");
        if (reveal) {
          reveal.classList.remove("hidden");
          reveal.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      } else {
        submitBtn.textContent = "INCORRECT";
        submitBtn.classList.remove("button-primary");
        submitBtn.classList.add("button-incorrect");
        setTimeout(() => {
          submitBtn.textContent = "SUBMIT";
          submitBtn.classList.remove("button-incorrect");
          submitBtn.classList.add("button-primary");
        }, 3000);
      }
    });
  });

  function spawnConfetti() {
    const colors = ["#67e8f9", "#8fffc1", "#fbbf24", "#f87171", "#d946ef"];
    const wrapper = document.createElement("div");
    wrapper.className = "confetti-wrapper";
    document.body.appendChild(wrapper);

    for (let i = 0; i < 80; i++) {
      const piece = document.createElement("span");
      piece.className = "confetti-piece";
      piece.style.setProperty("--x", (Math.random() * 200 - 100) + "px");
      piece.style.setProperty("--r", (Math.random() * 720 - 360) + "deg");
      piece.style.setProperty("--d", (Math.random() * 0.8).toFixed(2) + "s");
      piece.style.left = Math.random() * 100 + "%";
      piece.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
      wrapper.appendChild(piece);
    }

    setTimeout(() => wrapper.remove(), 4000);
  }

  document.querySelectorAll("[data-fake-action]").forEach((button) => {
    if (submitButtons.has(button)) return;
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
