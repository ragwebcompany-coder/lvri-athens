/* LVRI Athens — interface behaviour. No dependencies. */
(function () {
  "use strict";

  var $  = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var BASE = document.documentElement.getAttribute("data-base") || "/";

  function store(key, val) {
    try {
      if (val === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, val);
    } catch (e) { return null; }
  }

  /* ── Header, drawer, mega menu ─────────────────────────────────────── */
  function header() {
    var el = $(".header");
    if (!el) return;
    var onScroll = function () { el.classList.toggle("is-stuck", window.scrollY > 8); };
    onScroll();
    addEventListener("scroll", onScroll, { passive: true });

    var burger = $(".burger");
    if (burger) {
      burger.addEventListener("click", function () {
        var open = document.body.classList.toggle("nav-open");
        burger.setAttribute("aria-expanded", open);
      });
    }

    $$(".drawer__group").forEach(function (g) {
      var top = $(".drawer__top", g);
      if (!top || top.tagName === "A") return;
      top.addEventListener("click", function () {
        var open = g.classList.toggle("is-open");
        top.setAttribute("aria-expanded", open);
      });
    });

    var closeAll = function (except) {
      $$(".nav__item.is-open").forEach(function (i) {
        if (i === except) return;
        i.classList.remove("is-open");
        var b = $(".nav__link", i);
        if (b) b.setAttribute("aria-expanded", "false");
      });
    };
    $$(".nav__item[data-mega]").forEach(function (item) {
      var trigger = $(".nav__link", item);
      var shut;
      trigger.addEventListener("click", function (e) {
        e.preventDefault();
        var open = !item.classList.contains("is-open");
        closeAll(item);
        item.classList.toggle("is-open", open);
        trigger.setAttribute("aria-expanded", open);
      });
      item.addEventListener("mouseenter", function () {
        clearTimeout(shut); closeAll(item);
        item.classList.add("is-open"); trigger.setAttribute("aria-expanded", "true");
      });
      item.addEventListener("mouseleave", function () {
        shut = setTimeout(function () {
          item.classList.remove("is-open"); trigger.setAttribute("aria-expanded", "false");
        }, 160);
      });
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".nav__item")) closeAll();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      closeAll();
      if (document.body.classList.contains("nav-open")) {
        document.body.classList.remove("nav-open");
        if (burger) burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ── Reveal on scroll ──────────────────────────────────────────────── */
  function reveal() {
    var items = $$("[data-reveal]");
    if (!items.length) return;
    if (reduced || !("IntersectionObserver" in window)) {
      items.forEach(function (i) { i.classList.add("is-in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var delay = +(en.target.getAttribute("data-reveal") || 0);
        setTimeout(function () { en.target.classList.add("is-in"); }, delay);
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });
    items.forEach(function (i) { io.observe(i); });
    // Safety net: nothing stays hidden if the observer never fires for it.
    setTimeout(function () {
      items.forEach(function (i) {
        var r = i.getBoundingClientRect();
        if (r.top < innerHeight * 1.2) i.classList.add("is-in");
      });
    }, 1500);
  }

  /* ── Site search ───────────────────────────────────────────────────── */
  function search() {
    var box = $(".search");
    if (!box) return;
    var input = $("#search-input"), out = $("#search-results");
    var index = null, active = -1, hits = [];

    function load() {
      if (index) return Promise.resolve(index);
      return fetch(BASE + "search-index.json")
        .then(function (r) { return r.json(); })
        .then(function (j) { index = j; return j; })
        .catch(function () { index = []; return index; });
    }
    function open() {
      box.classList.add("is-open");
      box.setAttribute("aria-hidden", "false");
      load().then(function () { input.focus(); input.select(); });
    }
    function close() {
      box.classList.remove("is-open");
      box.setAttribute("aria-hidden", "true");
    }
    function norm(s) {
      return s.toLowerCase()
        .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        .replace(/ς/g, "σ");
    }
    function mark(text, q) {
      var i = norm(text).indexOf(q);
      if (i < 0) return text.slice(0, 110);
      var from = Math.max(0, i - 38);
      var slice = (from ? "…" : "") + text.slice(from, i) + "<em>" + text.slice(i, i + q.length) + "</em>" + text.slice(i + q.length, i + q.length + 60) + "…";
      return slice;
    }
    function render(q) {
      var nq = norm(q.trim());
      if (nq.length < 2) {
        out.innerHTML = '<p class="search__empty">Γράψτε τουλάχιστον 2 χαρακτήρες.</p>';
        hits = []; return;
      }
      hits = (index || []).map(function (p) {
        var t = norm(p.t), b = norm(p.b || "");
        var score = 0;
        if (t.indexOf(nq) === 0) score += 60;
        else if (t.indexOf(nq) > -1) score += 40;
        if ((p.k || "") && norm(p.k).indexOf(nq) > -1) score += 15;
        if (b.indexOf(nq) > -1) score += 10;
        return { p: p, score: score };
      }).filter(function (r) { return r.score > 0; })
        .sort(function (a, b) { return b.score - a.score; })
        .slice(0, 8).map(function (r) { return r.p; });

      if (!hits.length) {
        out.innerHTML = '<p class="search__empty">Δεν βρέθηκε κάτι για «' + q.replace(/[<>&]/g, "") + '».</p>';
        return;
      }
      active = 0;
      out.innerHTML = hits.map(function (p, i) {
        return '<a class="search__hit' + (i === 0 ? " is-active" : "") + '" href="' + BASE + p.u + '">' +
               "<b>" + p.t + "</b><span>" + mark(p.b || "", nq) + "</span></a>";
      }).join("");
    }
    function move(step) {
      var links = $$(".search__hit", out);
      if (!links.length) return;
      links[active] && links[active].classList.remove("is-active");
      active = (active + step + links.length) % links.length;
      links[active].classList.add("is-active");
      links[active].scrollIntoView({ block: "nearest" });
    }

    $$("[data-search-open]").forEach(function (b) { b.addEventListener("click", open); });
    $("[data-search-close]") && $("[data-search-close]").addEventListener("click", close);
    box.addEventListener("click", function (e) { if (e.target === box) close(); });
    input.addEventListener("input", function () { render(input.value); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter") {
        var link = $$(".search__hit", out)[active];
        if (link) { e.preventDefault(); location.href = link.href; }
      }
    });
    document.addEventListener("keydown", function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); open(); }
      if (e.key === "Escape" && box.classList.contains("is-open")) close();
    });
  }

  /* ── Symptom guide ─────────────────────────────────────────────────── */
  function guide() {
    var root = $("#guide");
    if (!root || !window.LVRI_GUIDE) return;
    var data = window.LVRI_GUIDE;
    var step = 0;
    var answers = {};

    var dots = $(".guide__dots", root);
    var body = $(".guide__body", root);

    function check() {
      return '<svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8.5l3.2 3.2L13 5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    }
    function dotsHtml() {
      return data.steps.map(function (_, i) {
        return '<span class="guide__dot' + (i < step ? " is-done" : i === step ? " is-now" : "") + '"></span>';
      }).join("") + '<span class="guide__dot' + (step >= data.steps.length ? " is-now" : "") + '"></span>';
    }
    function renderStep() {
      var s = data.steps[step];
      var picked = answers[s.id] || [];
      body.innerHTML =
        '<div class="guide__q"><p class="eyebrow eyebrow--plain">Βήμα ' + (step + 1) + " από " + data.steps.length + '</p>' +
        "<h3 style=\"font-size:clamp(1.25rem,1.1rem+.8vw,1.6rem)\">" + s.q + "</h3>" +
        (s.help ? '<p class="small muted">' + s.help + "</p>" : "") + "</div>" +
        '<div class="guide__opts' + (s.options.length > 6 ? " guide__opts--2col" : "") + '" role="group">' +
        s.options.map(function (o) {
          return '<button type="button" class="opt' + (s.type === "single" ? " opt--radio" : "") + '" ' +
            'data-val="' + o[0] + '" aria-pressed="' + (picked.indexOf(o[0]) > -1) + '">' +
            '<span class="opt__box">' + check() + "</span><span>" + o[1] + "</span></button>";
        }).join("") + "</div>" +
        '<div class="guide__foot">' +
          '<p class="guide__privacy">' + lockIcon() + " Οι απαντήσεις μένουν στη συσκευή σας.</p>" +
          '<span style="display:flex;gap:.6rem">' +
          (step > 0 ? '<button type="button" class="btn btn--ghost btn--sm" data-back>Πίσω</button>' : "") +
          '<button type="button" class="btn btn--sm" data-next' + (picked.length ? "" : " disabled style=\"opacity:.45;pointer-events:none\"") + ">" +
          (step === data.steps.length - 1 ? "Δείτε το αποτέλεσμα" : "Συνέχεια") + "</button></span></div>";
      dots.innerHTML = dotsHtml();
      bindStep(s);
      body.querySelector(".guide__q h3").setAttribute("tabindex", "-1");
      if (step > 0) body.querySelector(".guide__q h3").focus({ preventScroll: true });
    }
    function lockIcon() {
      return '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2.5" stroke="currentColor" stroke-width="1.8"/><path d="M8 10V7a4 4 0 018 0v3" stroke="currentColor" stroke-width="1.8"/></svg>';
    }
    function bindStep(s) {
      $$(".opt", body).forEach(function (btn) {
        btn.addEventListener("click", function () {
          var v = btn.getAttribute("data-val");
          var list = answers[s.id] || [];
          if (s.type === "single") {
            list = [v];
            $$(".opt", body).forEach(function (b) { b.setAttribute("aria-pressed", b === btn); });
          } else {
            var i = list.indexOf(v);
            if (i > -1) list.splice(i, 1); else list.push(v);
            btn.setAttribute("aria-pressed", list.indexOf(v) > -1);
          }
          answers[s.id] = list;
          var next = $("[data-next]", body);
          next.disabled = !list.length;
          next.style.opacity = list.length ? "" : ".45";
          next.style.pointerEvents = list.length ? "" : "none";
        });
      });
      var next = $("[data-next]", body);
      next && next.addEventListener("click", function () {
        step++;
        if (step >= data.steps.length) renderResult(); else renderStep();
        root.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
      });
      var back = $("[data-back]", body);
      back && back.addEventListener("click", function () { step--; renderStep(); });
    }
    function score() {
      var totals = {};
      data.steps.forEach(function (s) {
        (answers[s.id] || []).forEach(function (v) {
          var opt = s.options.filter(function (o) { return o[0] === v; })[0];
          if (!opt) return;
          Object.keys(opt[2] || {}).forEach(function (k) {
            totals[k] = (totals[k] || 0) + opt[2][k];
          });
        });
      });
      var max = Math.max.apply(null, [1].concat(Object.keys(totals).map(function (k) { return totals[k]; })));
      return Object.keys(totals)
        .map(function (k) { return { id: k, n: totals[k], pct: Math.round(totals[k] / max * 100) }; })
        .sort(function (a, b) { return b.n - a.n; })
        .filter(function (r) { return r.pct >= 34; })
        .slice(0, 3);
    }
    function renderResult() {
      var ranked = score();
      dots.innerHTML = dotsHtml();
      var urgent = (answers.impact || [])[0] === "high";
      var html = '<div class="result">' +
        '<div class="guide__q"><p class="eyebrow eyebrow--plain">Το αποτέλεσμά σας</p>' +
        "<h3 style=\"font-size:clamp(1.3rem,1.1rem+.9vw,1.75rem)\">" +
        (ranked.length ? "Αυτά συζητάμε συνήθως με γυναίκες που περιγράφουν τα ίδια"
                       : "Χρειάζεται να μιλήσουμε πρώτα") + "</h3></div>";

      if (ranked.length) {
        html += ranked.map(function (r) {
          var c = data.conditions[r.id];
          if (!c) return "";
          return '<div class="result__match">' +
            '<div class="result__rank"><h4 style="font-size:1.06rem">' + c.title + "</h4>" +
            '<span class="tiny muted">' + (r.pct >= 80 ? "Ισχυρή αντιστοιχία" : r.pct >= 55 ? "Πιθανή αντιστοιχία" : "Αξίζει να ελεγχθεί") + "</span></div>" +
            '<div class="meter"><i style="width:0%" data-w="' + r.pct + '"></i></div>' +
            '<p class="small muted">' + c.lead + "</p>" +
            '<div class="result__links"><a class="chip" href="' + BASE + c.url + '">Διαβάστε για ' + c.title.toLowerCase() + "</a>" +
            (c.treatments || []).map(function (t) {
              return '<a class="chip" href="' + BASE + t.url + '">' + t.title + "</a>";
            }).join("") + "</div></div>";
        }).join("");
      } else {
        html += '<p class="muted">Οι απαντήσεις σας δεν δείχνουν καθαρά προς κάποια συγκεκριμένη πάθηση. Αυτό είναι συνηθισμένο — και είναι ακριβώς ο λόγος που η εξέταση γίνεται από γιατρό.</p>';
      }

      html += '<div class="note"><b>Αυτό δεν είναι διάγνωση.</b>' +
        "<span>Ο οδηγός σας δίνει λέξεις για να ξεκινήσετε τη συζήτηση. Η διάγνωση γίνεται μόνο με κλινική εξέταση" +
        (ranked.some(function (r) { return r.id === "akrateia-ouron"; }) ? " και, για την ακράτεια, με ουροδυναμικό έλεγχο" : "") + ".</span></div>";

      if (urgent) {
        html += '<div class="note"><b>Το αναφέρατε ως έντονο.</b><span>Μη το αφήσετε. Καλέστε μας στο ' +
          data.phone + " και θα βρούμε ραντεβού σύντομα.</span></div>";
      }

      html += '<div class="guide__foot"><button type="button" class="btn btn--ghost btn--sm" data-restart>Ξεκινήστε ξανά</button>' +
        '<span style="display:flex;gap:.6rem;flex-wrap:wrap">' +
        '<a class="btn btn--ghost btn--sm" href="tel:' + data.phoneHref + '">' + data.phone + "</a>" +
        '<button type="button" class="btn btn--sm" data-book>Κλείστε ραντεβού</button></span></div></div>';

      body.innerHTML = html;
      requestAnimationFrame(function () {
        $$(".meter i", body).forEach(function (m) { m.style.width = m.getAttribute("data-w") + "%"; });
      });
      $("[data-restart]", body).addEventListener("click", function () {
        step = 0; answers = {}; renderStep();
      });
      var bookBtn = $("[data-book]", body);
      bookBtn && bookBtn.addEventListener("click", function () {
        var dlg = $("#book");
        if (dlg) {
          var sel = $("#book-topic", dlg);
          if (sel && ranked.length) {
            var want = data.conditions[ranked[0].id].title;
            $$("option", sel).forEach(function (o) { if (o.textContent === want) sel.value = o.value; });
          }
          dlg.showModal();
        }
      });
    }
    renderStep();
  }

  /* ── Pelvic-floor diagram ──────────────────────────────────────────── */
  function anatomy() {
    var root = $("#anatomy");
    if (!root) return;
    var panel = $(".anatomy__panel", root);
    var hots = $$(".hot", root);
    var svg = $(".anatomy__svg", root);
    var info = window.LVRI_ANATOMY || {};

    function show(id) {
      hots.forEach(function (h) { h.classList.toggle("is-active", h.getAttribute("data-organ") === id); });
      var d = info[id];
      if (!d) return;
      panel.innerHTML =
        '<p class="eyebrow">' + d.organ + "</p>" +
        (d.conditions || []).map(function (c) {
          return '<div class="anatomy__cond"><h3>' + c.title + "</h3>" +
            '<p class="voice">' + c.plain + "</p>" +
            '<p class="muted small">' + c.lead + "</p>" +
            '<div class="result__links"><a class="chip" href="' + BASE + c.url + '">Αναλυτικά</a>' +
            (c.treatments || []).map(function (t) {
              return '<a class="chip" href="' + BASE + t.url + '">' + t.title + "</a>";
            }).join("") + "</div></div>";
        }).join("");
    }
    hots.forEach(function (h) {
      var id = h.getAttribute("data-organ");
      h.addEventListener("click", function () { show(id); });
      h.addEventListener("mouseenter", function () { show(id); });
      h.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); show(id); }
      });
      h.addEventListener("focus", function () { show(id); });
    });
    $$(".anatomy__toggle button", root).forEach(function (b) {
      b.addEventListener("click", function () {
        $$(".anatomy__toggle button", root).forEach(function (o) { o.setAttribute("aria-pressed", o === b); });
        svg.classList.toggle("is-prolapsed", b.getAttribute("data-state") === "prolapse");
      });
    });
    show(root.getAttribute("data-default") || "bladder");
  }

  /* ── Treatment comparison ──────────────────────────────────────────── */
  function compare() {
    var root = $("#compare");
    if (!root) return;
    $$(".filter", root).forEach(function (f) {
      f.addEventListener("click", function () {
        var val = f.getAttribute("data-filter");
        $$(".filter", root).forEach(function (o) { o.setAttribute("aria-pressed", o === f); });
        var shown = 0;
        $$("tbody tr", root).forEach(function (tr) {
          var ok = val === "all" || tr.getAttribute("data-invasive") === val;
          tr.hidden = !ok;
          if (ok) shown++;
        });
        var live = $("[data-compare-count]", root);
        if (live) live.textContent = shown + (shown === 1 ? " θεραπεία" : " θεραπείες");
      });
    });
  }

  /* ── Kegel trainer ─────────────────────────────────────────────────── */
  function kegel() {
    var root = $("#kegel");
    if (!root || !window.LVRI_KEGEL) return;
    var progs = window.LVRI_KEGEL;
    var current = progs[0];
    var timer = null, phase = "idle", left = 0, rep = 0, running = false;

    var orb = $(".kegel__orb", root);
    var phaseEl = $(".kegel__phase", root);
    var countEl = $(".kegel__count", root);
    var repEl = $("[data-kegel-rep]", root);
    var totalEl = $("[data-kegel-total]", root);
    var startBtn = $("[data-kegel-start]", root);
    var ring = $(".kegel__prog", root);
    var C = 2 * Math.PI * 46;
    ring.style.strokeDasharray = C;
    ring.style.strokeDashoffset = C;

    var done = +(store("lvri-kegel") || 0);
    if (totalEl) totalEl.textContent = done;

    var LABEL = { contract: "Σφίξτε", hold: "Κρατήστε", release: "Χαλαρώστε", idle: "Έτοιμη;", done: "Τελειώσατε" };

    function paint(pct, colour) {
      ring.style.strokeDashoffset = C * (1 - pct);
      ring.style.stroke = colour;
    }
    function setPhase(p) {
      phase = p;
      phaseEl.textContent = LABEL[p];
      orb.classList.toggle("is-hold", p === "contract" || p === "hold");
      orb.classList.toggle("is-rest", p === "release" || p === "idle");
    }
    function tick() {
      left--;
      countEl.textContent = Math.max(0, left);
      var span = current[phase] || 1;
      paint(1 - left / span, phase === "release" ? "var(--iris-300)" : "var(--iris)");
      if (left > 0) return;
      if (phase === "contract") { left = current.hold; setPhase("hold"); }
      else if (phase === "hold") { left = current.release; setPhase("release"); }
      else {
        rep++;
        repEl.textContent = rep;
        if (rep >= current.reps) return finish();
        left = current.contract; setPhase("contract");
      }
      countEl.textContent = left;
    }
    function finish() {
      stop();
      setPhase("done");
      countEl.textContent = "✓";
      paint(1, "var(--iris)");
      done++; store("lvri-kegel", done);
      if (totalEl) totalEl.textContent = done;
      startBtn.textContent = "Ξανά";
    }
    function stop() {
      clearInterval(timer); timer = null; running = false;
      startBtn.setAttribute("data-state", "idle");
    }
    function start() {
      rep = 0; repEl.textContent = 0;
      left = current.contract; setPhase("contract");
      countEl.textContent = left;
      running = true;
      startBtn.textContent = "Παύση";
      startBtn.setAttribute("data-state", "running");
      timer = setInterval(tick, 1000);
    }
    startBtn.addEventListener("click", function () {
      if (running) { stop(); startBtn.textContent = "Συνέχεια"; }
      else if (timer === null && phase !== "idle" && phase !== "done" && rep < current.reps) {
        running = true; startBtn.textContent = "Παύση";
        timer = setInterval(tick, 1000);
      } else start();
    });
    $$(".prog-btn", root).forEach(function (b) {
      b.addEventListener("click", function () {
        stop();
        current = progs.filter(function (p) { return p.id === b.getAttribute("data-prog"); })[0];
        $$(".prog-btn", root).forEach(function (o) { o.setAttribute("aria-pressed", o === b); });
        setPhase("idle"); countEl.textContent = current.contract;
        rep = 0; repEl.textContent = 0; paint(0, "var(--iris)");
        startBtn.textContent = "Ξεκινήστε";
      });
    });
    setPhase("idle");
    countEl.textContent = current.contract;
  }

  /* ── FAQ ───────────────────────────────────────────────────────────── */
  function faq() {
    $$(".faq__item").forEach(function (item) {
      var btn = $(".faq__q", item);
      var panel = $(".faq__a", item);
      btn.addEventListener("click", function () {
        var open = item.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", open);
        panel.setAttribute("aria-hidden", !open);
        if (open && item.id) history.replaceState(null, "", "#" + item.id);
      });
    });
    if (location.hash) {
      var target = document.getElementById(location.hash.slice(1));
      if (target && target.classList.contains("faq__item")) {
        target.classList.add("is-open");
        $(".faq__q", target).setAttribute("aria-expanded", "true");
      }
    }
  }

  /* ── Article: TOC, scroll spy, reading progress ────────────────────── */
  function doc() {
    var bar = $(".progress");
    if (bar) {
      var onScroll = function () {
        var h = document.documentElement.scrollHeight - innerHeight;
        bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, scrollY / h) : 0) + ")";
      };
      onScroll();
      addEventListener("scroll", onScroll, { passive: true });
    }
    var toc = $(".toc");
    var prose = $(".prose");
    if (!toc || !prose) return;
    var heads = $$("h2, h3", prose).filter(function (h) { return h.textContent.trim().length > 2; });
    if (heads.length < 3) { var w = toc.closest("[data-toc-wrap]"); if (w) w.hidden = true; return; }
    heads.forEach(function (h, i) {
      if (!h.id) h.id = "s-" + (i + 1);
      var a = document.createElement("a");
      a.href = "#" + h.id;
      a.textContent = h.textContent;
      a.setAttribute("data-depth", h.tagName === "H3" ? "3" : "2");
      toc.appendChild(a);
    });
    if (!("IntersectionObserver" in window)) return;
    var links = $$("a", toc);
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (l) {
          l.classList.toggle("is-active", l.getAttribute("href") === "#" + en.target.id);
        });
      });
    }, { rootMargin: "-15% 0px -70% 0px" });
    heads.forEach(function (h) { spy.observe(h); });
  }

  /* ── Gallery + lightbox ────────────────────────────────────────────── */
  function gallery() {
    var lb = $(".lightbox");
    if (!lb) return;
    var stage = $(".lightbox__stage", lb);
    var caption = $("[data-lb-caption]", lb);
    var items = [], idx = 0, opener = null;

    function render() {
      var it = items[idx];
      if (!it) return;
      stage.innerHTML = it.video
        ? '<div class="ratio"><iframe src="https://www.youtube-nocookie.com/embed/' + it.video +
          '?autoplay=1&rel=0" title="' + it.alt + '" allow="accelerometer;autoplay;encrypted-media;picture-in-picture" allowfullscreen></iframe></div>'
        : '<img src="' + it.src + '" alt="' + it.alt + '">';
      caption.textContent = (idx + 1) + " / " + items.length;
    }
    function open(list, i, from) {
      items = list; idx = i; opener = from;
      lb.classList.add("is-open");
      lb.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
      render();
      $(".lightbox__close", lb).focus();
    }
    function close() {
      lb.classList.remove("is-open");
      lb.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
      stage.innerHTML = "";
      if (opener) opener.focus();
    }
    function step(d) { idx = (idx + d + items.length) % items.length; render(); }

    // Clinical photographs stay blurred until the visitor opts in.
    var grid0 = $("[data-gallery]");
    var gate = $("[data-reveal-gate]");
    var sensitiveOK = store("lvri-gallery") === "shown";
    function applyGate() {
      if (!grid0) return;
      grid0.classList.toggle("is-revealed", sensitiveOK);
      if (gate) gate.hidden = sensitiveOK;
      $$("[data-sensitive]", grid0).forEach(function (b) {
        b.setAttribute("aria-disabled", String(!sensitiveOK));
      });
    }
    applyGate();
    var revealBtn = $("[data-reveal-photos]");
    if (revealBtn) {
      revealBtn.addEventListener("click", function () {
        sensitiveOK = true; store("lvri-gallery", "shown"); applyGate();
      });
    }

    $$("[data-gallery]").forEach(function (grid) {
      var buttons = $$("[data-item]", grid);
      var list = buttons.map(function (b) {
        return { src: b.getAttribute("data-full") || "", alt: b.getAttribute("data-alt") || "", video: b.getAttribute("data-video") || "" };
      });
      buttons.forEach(function (b, i) {
        b.addEventListener("click", function () {
          if (b.hasAttribute("data-sensitive") && !sensitiveOK) {
            if (revealBtn) revealBtn.focus();
            return;
          }
          var visible = buttons.filter(function (x) { return !x.hidden; });
          var vlist = visible.map(function (x) { return list[buttons.indexOf(x)]; });
          open(vlist, visible.indexOf(b), b);
        });
      });
      $$("[data-gal-filter]", grid.parentNode).forEach(function (f) {
        f.addEventListener("click", function () {
          var v = f.getAttribute("data-gal-filter");
          $$("[data-gal-filter]", grid.parentNode).forEach(function (o) { o.setAttribute("aria-pressed", o === f); });
          buttons.forEach(function (b) { b.hidden = v !== "all" && b.getAttribute("data-kind") !== v; });
        });
      });
    });
    $(".lightbox__close", lb).addEventListener("click", close);
    $("[data-lb-prev]", lb).addEventListener("click", function () { step(-1); });
    $("[data-lb-next]", lb).addEventListener("click", function () { step(1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") step(-1);
      if (e.key === "ArrowRight") step(1);
    });
  }

  /* ── Article list filter ───────────────────────────────────────────── */
  function articleFilter() {
    var root = $("#articles");
    if (!root) return;
    var input = $("[data-article-search]", root);
    var rows = $$(".article-row", root);
    var empty = $("[data-article-empty]", root);
    var tag = "all";

    function apply() {
      var q = (input ? input.value : "").trim().toLowerCase();
      var n = 0;
      rows.forEach(function (r) {
        var okTag = tag === "all" || r.getAttribute("data-tag") === tag;
        var okQ = !q || r.getAttribute("data-search").indexOf(q) > -1;
        r.hidden = !(okTag && okQ);
        if (!r.hidden) n++;
      });
      if (empty) empty.hidden = n > 0;
    }
    input && input.addEventListener("input", apply);
    $$("[data-tag-filter]", root).forEach(function (b) {
      b.addEventListener("click", function () {
        tag = b.getAttribute("data-tag-filter");
        $$("[data-tag-filter]", root).forEach(function (o) { o.setAttribute("aria-pressed", o === b); });
        apply();
      });
    });
  }

  /* ── Booking dialog ────────────────────────────────────────────────── */
  function booking() {
    var dlg = $("#book");
    if (!dlg) return;
    $$("[data-book-open]").forEach(function (b) {
      b.addEventListener("click", function (e) { e.preventDefault(); dlg.showModal(); });
    });
    $$("[data-book-close]", dlg).forEach(function (b) {
      b.addEventListener("click", function () { dlg.close(); });
    });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });

    var dateEl = $("#book-date", dlg);
    if (dateEl) {
      var t = new Date(); t.setDate(t.getDate() + 1);
      dateEl.min = t.toISOString().slice(0, 10);
      var max = new Date(); max.setMonth(max.getMonth() + 4);
      dateEl.max = max.toISOString().slice(0, 10);
    }
    var slotWrap = $("[data-slots]", dlg);
    var slotInput = $("#book-slot", dlg);
    $$(".slot", slotWrap).forEach(function (s) {
      s.addEventListener("click", function () {
        $$(".slot", slotWrap).forEach(function (o) { o.setAttribute("aria-pressed", o === s); });
        slotInput.value = s.textContent.trim();
      });
    });
    // Saturday closes at 15:00; Sunday is closed.
    dateEl && dateEl.addEventListener("change", function () {
      var d = new Date(dateEl.value + "T12:00:00").getDay();
      var warn = $("[data-day-warn]", dlg);
      warn.hidden = d !== 0;
      $$(".slot", slotWrap).forEach(function (s) {
        var hour = parseInt(s.textContent, 10);
        var closed = d === 0 || (d === 6 && hour >= 15);
        s.disabled = closed;
        s.style.opacity = closed ? ".35" : "";
        if (closed && s.getAttribute("aria-pressed") === "true") {
          s.setAttribute("aria-pressed", "false"); slotInput.value = "";
        }
      });
    });

    var form = $("form", dlg);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      $$(".field", form).forEach(function (f) {
        var input = $("input, select, textarea", f);
        if (!input || !input.required) return;
        var valid = input.checkValidity();
        f.classList.toggle("is-invalid", !valid);
        if (!valid && ok) { input.focus(); ok = false; }
      });
      if (!ok) return;

      var d = new FormData(form);
      var lines = [
        "Αίτημα ραντεβού από το lvriathens.com", "",
        "Ονοματεπώνυμο: " + (d.get("name") || "—"),
        "Τηλέφωνο: " + (d.get("phone") || "—"),
        "Email: " + (d.get("email") || "—"),
        "Θέμα: " + (d.get("topic") || "—"),
        "Προτιμώμενη ημερομηνία: " + (d.get("date") || "—"),
        "Προτιμώμενη ώρα: " + (d.get("slot") || "—"), "",
        "Σημείωση:", (d.get("note") || "—")
      ].join("\n");

      var mail = "mailto:" + dlg.getAttribute("data-email") +
        "?subject=" + encodeURIComponent("Αίτημα ραντεβού — " + (d.get("name") || "")) +
        "&body=" + encodeURIComponent(lines);

      $(".book__body", dlg).innerHTML =
        '<div class="stack" style="justify-items:stretch">' +
        '<h3>Το αίτημά σας είναι έτοιμο</h3>' +
        '<p class="muted small">Το πρόγραμμα email σας θα ανοίξει με τα στοιχεία συμπληρωμένα. Αν δεν ανοίξει, αντιγράψτε το κείμενο ή καλέστε μας.</p>' +
        '<pre style="white-space:pre-wrap;background:var(--mist-2);padding:1rem;border-radius:var(--r-sm);font:inherit;font-size:.86rem;margin:0">' +
        lines.replace(/[<>&]/g, "") + "</pre></div>";
      $(".book__foot", dlg).innerHTML =
        '<button type="button" class="btn btn--ghost btn--sm" data-copy>Αντιγραφή κειμένου</button>' +
        '<span style="display:flex;gap:.6rem"><a class="btn btn--ghost btn--sm" href="tel:' + dlg.getAttribute("data-phone") + '">Καλέστε</a>' +
        '<a class="btn btn--sm" href="' + mail + '">Άνοιγμα email</a></span>';
      $("[data-copy]", dlg).addEventListener("click", function (e) {
        navigator.clipboard && navigator.clipboard.writeText(lines).then(function () {
          e.target.textContent = "Αντιγράφηκε ✓";
        });
      });
      location.href = mail;
    });
  }

  /* ── Chrome: to-top, action bar ────────────────────────────────────── */
  function chrome() {
    var top = $(".totop"), bar = $(".actionbar");
    var onScroll = function () {
      var show = scrollY > 600;
      top && top.classList.toggle("is-shown", show);
      bar && bar.classList.toggle("is-shown", scrollY > 320);
    };
    onScroll();
    addEventListener("scroll", onScroll, { passive: true });
    top && top.addEventListener("click", function () {
      scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
    });
  }

  /* ── Cookie notice ─────────────────────────────────────────────────── */
  function cookies() {
    var box = $(".cookies");
    if (!box) return;
    if (store("lvri-consent")) return;
    setTimeout(function () { box.classList.add("is-shown"); }, 900);
    function save(value) {
      store("lvri-consent", value);
      box.classList.remove("is-shown");
    }
    $("[data-cookie-accept]", box).addEventListener("click", function () {
      save($("#cookie-analytics", box).checked ? "all" : "necessary");
    });
    $("[data-cookie-reject]", box).addEventListener("click", function () { save("necessary"); });
  }

  function init() {
    header(); reveal(); search(); guide(); anatomy(); compare();
    kegel(); faq(); doc(); gallery(); articleFilter(); booking(); chrome(); cookies();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
