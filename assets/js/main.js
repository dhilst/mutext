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

  // --- case file -----------------------------------------------------------
  // Which incidents the operator has closed. Slugs, not pathnames, so a local
  // build and the deployed site agree.
  const solvedKey = "mutext-solved";

  function loadSolved() {
    try { return JSON.parse(localStorage.getItem(solvedKey)) || []; }
    catch { return []; }
  }

  function slugOf(path) {
    return path.split("/").pop().replace(/\.html$/, "");
  }

  function markSolved(slug) {
    if (!slug) return;
    const solved = loadSolved();
    if (solved.includes(slug)) return;
    solved.push(slug);
    try { localStorage.setItem(solvedKey, JSON.stringify(solved)); } catch { /* ignore */ }
    renderProgress();
  }

  // --- incident queue ------------------------------------------------------
  // Incidents are routed one at a time: an incident is in your queue only once
  // the one before it is closed.
  function queue() {
    const tag = document.getElementById("incident-queue");
    if (!tag) return [];
    try { return JSON.parse(tag.textContent) || []; } catch { return []; }
  }

  function isOpen(slug) {
    const list = queue();
    const i = list.findIndex((c) => c.slug === slug);
    if (i < 0) return true;                       // not an incident page
    if (i === 0) return true;                     // the first one is always open
    return loadSolved().includes(list[i - 1].slug);
  }

  function currentIncident() {
    const solved = loadSolved();
    return queue().find((c) => !solved.includes(c.slug)) || null;
  }

  function sealNotice() {
    const next = currentIncident();
    document.title = "\u03bc-text";          // don't leak the title in the tab
    const main = document.getElementById("content");
    if (!main) return;
    const back = next
      ? `<a class="button-primary" href="${next.url}">OPEN ${next.title.split(" ")[0]}</a>`
      : "";
    main.innerHTML = `
      <section class="shell-panel">
        <div class="panel-header">
          <span>incident queue</span>
          <span class="text-amber-warn">not routed</span>
        </div>
        <div class="space-y-4 p-6 text-sm leading-7 text-slate-300">
          <p class="font-mono text-xs uppercase text-amber-warn">access withheld</p>
          <p>This record is not in your queue. Incidents are routed one at a time,
             in the order they were filed, and this one is behind at least one that
             is still open.</p>
          <p class="text-slate-mutext">Close the incident ahead of it and this page
             will route to you.</p>
          <div class="flex flex-wrap gap-3 pt-2">
            ${back}
            <a class="button-quiet" href="${document.querySelector('a[href$="archive.html"]')?.getAttribute("href") || "../archive.html"}">Archive</a>
          </div>
        </div>
      </section>`;
  }

  function enforceQueue() {
    const required = document.body.dataset.requires;
    const locked = required
      ? !loadSolved().includes(required)
      : !isOpen(slugOf(location.pathname));
    if (locked) sealNotice();
    return locked;
  }

  function renderProgress() {
    const solved = loadSolved();

    document.querySelectorAll("[data-chapter]").forEach((row) => {
      row.hidden = !isOpen(row.dataset.chapter);
      const done = solved.includes(row.dataset.chapter);
      row.classList.toggle("is-closed", done);
      const badge = row.querySelector("[data-solved-badge]");
      if (badge) badge.textContent = done ? "closed" : "";
    });

    const counter = document.querySelector("[data-progress-count]");
    if (counter) {
      const total = Number(counter.dataset.progressTotal) || 0;
      const closed = solved.length > total ? total : solved.length;
      counter.textContent = closed + "/" + total;
      const bar = document.querySelector("[data-progress-bar]");
      if (bar && total) bar.style.width = Math.round((closed / total) * 100) + "%";
    }

    const reset = document.querySelector("[data-clear-progress]");
    if (reset) reset.hidden = solved.length === 0;

    const active = document.querySelector("[data-active-incident]");
    if (active) {
      const next = currentIncident();
      if (next) {
        active.hidden = false;
        active.setAttribute("href", next.url);
        const id = next.title.split(" ")[0];
        active.querySelector("[data-active-id]").textContent = id;
        active.querySelector("[data-active-title]").textContent =
          next.title.slice(id.length).trim();
      } else {
        active.hidden = true;
      }
    }
  }

  enforceQueue();

  const resetBtn = document.querySelector("[data-clear-progress]");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      if (!confirm("Reopen every incident? This clears your case file.")) return;
      localStorage.removeItem(solvedKey);
      renderProgress();
    });
  }

  renderProgress();

  const submitButtons = new Set();
  const answerBlocks = Array.from(document.querySelectorAll("[data-puzzle-answer]"));

  document.querySelectorAll("[data-puzzle-answer]").forEach((answerEl) => {
    const answer = answerEl.getAttribute("data-puzzle-answer").split(",").map(s => s.trim().toLowerCase());
    const revealSel = answerEl.getAttribute("data-reveal") || "#lore-reveal";
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
        // A two-stage chapter is only closed once its final block is solved.
        if (answerBlocks.indexOf(answerEl) === answerBlocks.length - 1) {
          markSolved(slugOf(location.pathname));
        }
        const reveal = document.querySelector(revealSel);
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
