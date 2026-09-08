/* =============================================================
   LVRI ATHENS — version 2 runtime
   Vanilla JS, no dependencies. Everything runs on the device.
   ============================================================= */
(function () {
"use strict";

var D = document, W = window, root = D.documentElement;
var $ = function (s, c) { return (c || D).querySelector(s); };
var $$ = function (s, c) { return Array.prototype.slice.call((c || D).querySelectorAll(s)); };
var depth = +(D.body.dataset.depth || 0);
var base = depth ? new Array(depth + 1).join("../") : "";
var reduced = W.matchMedia("(prefers-reduced-motion: reduce)").matches;
var LANG = D.body.dataset.lang === "en" ? "en" : "el";
var TXT = {
  el: { on: "Ενεργοποιήθηκε", off: "Απενεργοποιήθηκε", wiped: "Τα τοπικά δεδομένα διαγράφηκαν",
        added: "Προστέθηκε στη λίστα σας", removed: "Αφαιρέθηκε από τη λίστα",
        addTo: "Προσθήκη στη λίστα μου: ", removeFrom: "Αφαίρεση από τη λίστα μου: ",
        checkFields: "Ελέγξτε τα σημειωμένα πεδία", mailOpening: "Ανοίγει το πρόγραμμα email σας",
        unlockFirst: "Ξεκλειδώστε πρώτα τις φωτογραφίες", sessionDone: "Συνεδρία ολοκληρώθηκε",
        reset: "Μηδενίστηκε", start: "Έναρξη", pause: "Παύση", ready: "Έτοιμη;",
        done: "Τέλος", phases: ["Σφίξτε", "Κρατήστε", "Χαλαρώστε"],
        commands: "Εντολές", typeMore: "Γράψτε τουλάχιστον 2 χαρακτήρες ή διαλέξτε μια εντολή.",
        noMatch: "Καμία αντιστοιχία.",
        emptyList: "Η λίστα σας είναι άδεια", removeBtn: "Αφαίρεση",
        kinds: { treatment: "Θεραπεία", condition: "Πάθηση", article: "Άρθρο", page: "Σελίδα" },
        groups: { treatment: "Θεραπείες", condition: "Παθήσεις", article: "Άρθρα", page: "Σελίδες" } },
  en: { on: "On", off: "Off", wiped: "Local data deleted",
        added: "Added to your list", removed: "Removed from your list",
        addTo: "Add to my list: ", removeFrom: "Remove from my list: ",
        checkFields: "Please check the marked fields", mailOpening: "Opening your email app",
        unlockFirst: "Unlock the photographs first", sessionDone: "Session complete",
        reset: "Reset", start: "Start", pause: "Pause", ready: "Ready?",
        done: "Done", phases: ["Squeeze", "Hold", "Release"],
        commands: "Commands", typeMore: "Type at least 2 characters, or pick a command.",
        noMatch: "No match.",
        emptyList: "Your list is empty", removeBtn: "Remove",
        kinds: { treatment: "Treatment", condition: "Condition", article: "Article", page: "Page" },
        groups: { treatment: "Treatments", condition: "Conditions", article: "Articles", page: "Pages" } }
}[LANG];

/* ── storage ─────────────────────────────────────────────── */
var K = { list: "lvri2:list", kegel: "lvri2:kegel", ck: "lvri2:ck",
          gal: "lvri2:gal", motion: "lvri2:motion", contrast: "lvri2:contrast",
          autoplay: "lvri2:autoplay", intro: "lvri2:intro" };
function get(k, fb) { try { var v = localStorage.getItem(k); return v == null ? fb : JSON.parse(v); }
  catch (e) { return fb; } }
function set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
function del(k) { try { localStorage.removeItem(k); } catch (e) {} }

/* ── toast ───────────────────────────────────────────────── */
var toastBox = $("#toast");
function toast(msg) {
  if (!toastBox) return;
  var el = D.createElement("div");
  el.className = "toast__i"; el.textContent = msg;
  toastBox.appendChild(el);
  setTimeout(function () {
    el.style.transition = "opacity .35s, transform .35s";
    el.style.opacity = "0"; el.style.transform = "translateY(10px)";
    setTimeout(function () { el.remove(); }, 380);
  }, 2400);
}

/* ── greek-aware text normalisation ──────────────────────── */
function norm(s) {
  return (s || "").toString().toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/ς/g, "σ").replace(/[^\p{L}\p{N} ]/gu, " ").replace(/\s+/g, " ").trim();
}

/* ── prefs ───────────────────────────────────────────────── */
var prefs = {
  motion: get(K.motion, "on") !== "off",
  contrast: get(K.contrast, "normal") === "high",
  autoplay: true
};
function applyPrefs() {
  root.dataset.motion = prefs.motion ? "on" : "off";
  if (prefs.contrast) root.dataset.contrast = "high"; else delete root.dataset.contrast;
  set(K.motion, prefs.motion ? "on" : "off");
  set(K.contrast, prefs.contrast ? "high" : "normal");
}
applyPrefs();
$$("[data-pref]").forEach(function (inp) {
  inp.checked = !!prefs[inp.dataset.pref];
  inp.addEventListener("change", function () {
    prefs[inp.dataset.pref] = inp.checked; applyPrefs();
    toast(inp.checked ? TXT.on : TXT.off);
  });
});
var wipe = $("[data-wipe]");
if (wipe) wipe.addEventListener("click", function () {
  Object.keys(K).forEach(function (k) { del(K[k]); });
  toast(TXT.wiped); setTimeout(function () { location.reload(); }, 700);
});

/* ── overlay manager ─────────────────────────────────────── */
var openStack = [], lastFocus = null;
function openOv(id, ctx) {
  var ov = D.getElementById(id === "scanner" ? "scanner-ov" : id);
  if (!ov) return;
  lastFocus = D.activeElement;
  ov.hidden = false;
  D.body.style.overflow = "hidden";
  openStack.push(ov);
  if (id === "palette") palOpen();
  if (id === "scanner") scOpen();
  if (id === "book" && ctx && ctx.dataset.topic) {
    var sel = $("#bk-topic"); if (sel) sel.value = ctx.dataset.topic;
  }
  var f = ov.querySelector("input,select,textarea,button:not([data-close]),a[href]");
  if (f) setTimeout(function () { f.focus(); }, 60);
}
function closeOv(ov) {
  ov = ov || openStack[openStack.length - 1];
  if (!ov) return;
  ov.hidden = true;
  openStack = openStack.filter(function (x) { return x !== ov; });
  if (!openStack.length) D.body.style.overflow = "";
  if (ov.id === "player") { var fr = $(".pl__frame", ov); if (fr) fr.innerHTML = ""; }
  if (lastFocus && lastFocus.focus) lastFocus.focus();
}
D.addEventListener("click", function (e) {
  var op = e.target.closest("[data-open]");
  if (op) { e.preventDefault(); openOv(op.dataset.open, op); return; }
  if (e.target.closest("[data-close]") || e.target.classList.contains("ov__scrim")) {
    e.preventDefault(); closeOv();
  }
});
D.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && openStack.length) { e.preventDefault(); closeOv(); }
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
    e.preventDefault();
    var pal = D.getElementById("palette");
    if (pal && !pal.hidden) closeOv(pal); else openOv("palette");
  }
  if (openStack.length && e.key === "Tab") {
    var ov = openStack[openStack.length - 1];
    var f = $$('a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])', ov)
      .filter(function (el) { return el.offsetParent !== null; });
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && D.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && D.activeElement === last) { e.preventDefault(); first.focus(); }
  }
});
/* drawer */
var drawer = $("#drawer");
if (drawer) {
  $$("[data-open='drawer']").forEach(function (b) {
    b.addEventListener("click", function () { drawer.hidden = false; D.body.style.overflow = "hidden"; });
  });
  drawer.addEventListener("click", function (e) {
    if (e.target === drawer || e.target.closest("[data-close]") || e.target.closest("a")) {
      drawer.hidden = true; if (!openStack.length) D.body.style.overflow = "";
    }
  });
}

/* ── topbar, progress, spotlight, totop ──────────────────── */
var tb = $("#topbar"), prog = $(".progress"), totop = $(".totop");
var ticking = false;
function onScroll() {
  var y = W.scrollY || 0;
  if (tb) tb.dataset.atTop = y > 12 ? "0" : "1";
  var h = D.documentElement.scrollHeight - W.innerHeight;
  var p = h > 0 ? Math.min(1, y / h) : 0;
  if (prog) prog.style.setProperty("--p", p.toFixed(4));
  if (tb) tb.style.setProperty("--scan", p.toFixed(4));
  if (totop) totop.hidden = y < 700;
  ticking = false;
}
W.addEventListener("scroll", function () {
  if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
}, { passive: true });
onScroll();
if (totop) totop.addEventListener("click", function () {
  W.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
});
/* ── reveal ──────────────────────────────────────────────── */
var revealTargets = $$(".rv");
if ("IntersectionObserver" in W && revealTargets.length) {
  var io = new IntersectionObserver(function (en) {
    en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("is-in"); io.unobserve(x.target); } });
  }, { rootMargin: "0px 0px -8% 0px", threshold: .06 });
  revealTargets.forEach(function (t) { io.observe(t); });
} else { revealTargets.forEach(function (t) { t.classList.add("is-in"); }); }

/* ── rows ────────────────────────────────────────────────── */
$$("[data-row]").forEach(function (row) {
  var track = $(".row__track", row), L = $(".row__nav--l", row), R = $(".row__nav--r", row);
  var rail = $(".row__rail i", row);
  if (!track) return;
  function page() { return Math.max(240, track.clientWidth * .82); }
  function sync() {
    var max = track.scrollWidth - track.clientWidth;
    if (L) L.disabled = track.scrollLeft < 8;
    if (R) R.disabled = track.scrollLeft > max - 8;
    if (rail && max > 0) {
      var vis = track.clientWidth / track.scrollWidth;
      rail.style.setProperty("--w", (vis * 100).toFixed(2) + "%");
      rail.style.setProperty("--x", ((track.scrollLeft / max) * ((1 / vis) - 1) * 100).toFixed(2) + "%");
    } else if (rail) { rail.parentElement.style.opacity = "0"; }
  }
  if (L) L.addEventListener("click", function () { track.scrollBy({ left: -page(), behavior: "smooth" }); });
  if (R) R.addEventListener("click", function () { track.scrollBy({ left: page(), behavior: "smooth" }); });
  track.addEventListener("scroll", function () { requestAnimationFrame(sync); }, { passive: true });
  track.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { e.preventDefault(); track.scrollBy({ left: page(), behavior: "smooth" }); }
    if (e.key === "ArrowLeft") { e.preventDefault(); track.scrollBy({ left: -page(), behavior: "smooth" }); }
  });
  /* pointer drag on non-touch */
  var down = false, sx = 0, sl = 0, moved = 0;
  track.addEventListener("pointerdown", function (e) {
    if (e.pointerType === "touch" || e.target.closest(".nf-save,.nf-card__panel")) return;
    down = true; moved = 0; sx = e.clientX; sl = track.scrollLeft;
  });
  W.addEventListener("pointermove", function (e) {
    if (!down) return;
    var dx = e.clientX - sx; moved = Math.abs(dx);
    if (moved > 4) { track.style.scrollBehavior = "auto"; track.scrollLeft = sl - dx; }
  });
  W.addEventListener("pointerup", function () {
    if (down && moved > 6) track.addEventListener("click", function k(ev) {
      ev.preventDefault(); ev.stopPropagation(); track.removeEventListener("click", k, true);
    }, true);
    down = false; track.style.scrollBehavior = "";
  });
  new ResizeObserver(sync).observe(track);
  sync();
});

/* ── my list ─────────────────────────────────────────────── */
function listGet() { var l = get(K.list, []); return Array.isArray(l) ? l : []; }
function listHas(id) { return listGet().some(function (x) { return x.id === id; }); }
function listCount() {
  var n = listGet().length;
  $$("[data-mylist-count]").forEach(function (b) { b.textContent = n; b.hidden = !n; });
}
function listToggle(item) {
  var l = listGet(), i = l.findIndex(function (x) { return x.id === item.id; });
  if (i > -1) { l.splice(i, 1); set(K.list, l); toast(TXT.removed); }
  else { l.unshift(Object.assign({ ts: Date.now() }, item)); set(K.list, l); toast(TXT.added); }
  syncSaves(); listCount();
}
function syncSaves() {
  $$("[data-save]").forEach(function (b) {
    var it; try { it = JSON.parse(b.dataset.save); } catch (e) { return; }
    b.setAttribute("aria-pressed", listHas(it.id) ? "true" : "false");
    b.setAttribute("aria-label", (listHas(it.id) ? TXT.removeFrom : TXT.addTo) + it.t);
  });
}
D.addEventListener("click", function (e) {
  var b = e.target.closest("[data-save]");
  if (!b) return;
  e.preventDefault(); e.stopPropagation();
  try { listToggle(JSON.parse(b.dataset.save)); } catch (err) {}
});
syncSaves(); listCount();

function esc(s) { var d = D.createElement("div"); d.textContent = s == null ? "" : s; return d.innerHTML; }

/* render the saved list page */
(function myListPage() {
  var mount = $("[data-mylist]");
  if (!mount) return;
  function draw() {
    var l = listGet();
    if (!l.length) {
      mount.innerHTML = '<div class="tile"><h3>' + TXT.emptyList + '</h3>' +
        '<p>Πατήστε το <b>+</b> σε οποιαδήποτε κάρτα θεραπείας, πάθησης ή άρθρου και θα βρίσκεται εδώ. ' +
        'Αποθηκεύεται μόνο σε αυτή τη συσκευή.</p></div>';
      return;
    }
    var KIND = TXT.kinds;
    mount.innerHTML = '<div class="grid-3">' + l.map(function (x) {
      return '<article class="tile"><span class="tile__n">' + (KIND[x.k] || "Σελίδα") + '</span>' +
        '<h3><a href="' + base + x.u + '">' + esc(x.t) + '</a></h3>' +
        '<p><button class="linky" type="button" data-drop="' + esc(x.id) + '">' + TXT.removeBtn + '</button></p></article>';
    }).join("") + "</div>";
  }
  mount.addEventListener("click", function (e) {
    var d = e.target.closest("[data-drop]"); if (!d) return;
    var l = listGet().filter(function (x) { return x.id !== d.dataset.drop; });
    set(K.list, l); listCount(); syncSaves(); draw(); toast(TXT.removed);
  });
  draw();
})();

/* ── command palette ─────────────────────────────────────── */
var IDX = null, palSel = 0, palRows = [];
var ACTIONS = [
  { t: "Ζητήστε ραντεβού", s: "Άνοιγμα φόρμας", act: function () { closeOv(); openOv("book"); }, ic: "RA" },
  { t: "Σαρωτής συμπτωμάτων", s: "Ξεκινήστε τη σάρωση", act: function () { closeOv(); openOv("scanner"); }, ic: "ΣΑ" },
  { t: "Κλήση στο ιατρείο", s: "210 7609109", act: function () { location.href = "tel:+302107609109"; }, ic: "ΤΗ" },
  { t: "Η λίστα μου", s: "Αποθηκευμένα", act: function () { location.href = base + "i-lista-mou/"; }, ic: "ΛΙ" },
  { t: "Προπονητής Kegel", s: "Ασκήσεις", act: function () { location.href = base + "askiseis-kegel/"; }, ic: "KG" },
  { t: "Εναλλαγή κίνησης", s: "Ενεργοποίηση/απενεργοποίηση εφέ", ic: "ΚΙ",
    act: function () { prefs.motion = !prefs.motion; applyPrefs(); toast(prefs.motion ? "Κίνηση: ναι" : "Κίνηση: όχι"); closeOv(); } }
];
function palOpen() {
  var inp = $(".pal__in");
  if (inp) { inp.value = ""; setTimeout(function () { inp.focus(); }, 40); }
  palRender("");
  if (IDX === null) {
    IDX = [];
    fetch(base + "search-index.json").then(function (r) { return r.json(); })
      .then(function (j) { IDX = j; palRender($(".pal__in") ? $(".pal__in").value : ""); })
      .catch(function () { IDX = []; });
  }
}
function score(q, item) {
  var t = item._t || (item._t = norm(item.t)), k = item._k || (item._k = norm((item.kw || "") + " " + (item.d || "")));
  if (t === q) return 100;
  if (t.indexOf(q) === 0) return 80;
  if (t.indexOf(q) > -1) return 60;
  if (k.indexOf(q) > -1) return 30;
  var parts = q.split(" ").filter(Boolean);
  if (parts.length > 1 && parts.every(function (p) { return (t + " " + k).indexOf(p) > -1; })) return 24;
  return 0;
}
function hi(text, q) {
  if (!q) return esc(text);
  var n = norm(text), i = n.indexOf(q);
  if (i < 0) return esc(text);
  return esc(text.slice(0, i)) + "<mark>" + esc(text.slice(i, i + q.length)) + "</mark>" + esc(text.slice(i + q.length));
}
var LABEL = TXT.groups;
function palRender(raw) {
  var box = $("#pal-res"); if (!box) return;
  var q = norm(raw), html = "", n = 0;
  palRows = [];
  var acts = ACTIONS.filter(function (a) { return !q || norm(a.t).indexOf(q) > -1 || norm(a.s).indexOf(q) > -1; });
  if (acts.length) {
    html += '<p class="pal__group">' + TXT.commands + '</p>';
    acts.slice(0, q ? 4 : 3).forEach(function (a) {
      html += '<button class="pal__item" data-act="' + ACTIONS.indexOf(a) + '"><span class="pal__ic">' + a.ic +
        '</span><span class="pal__txt"><b>' + hi(a.t, q) + '</b><span>' + esc(a.s) + '</span></span></button>';
      palRows.push({ act: a }); n++;
    });
  }
  if (q && q.length > 1 && IDX && IDX.length) {
    var hits = IDX.map(function (it) { return { it: it, s: score(q, it) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s || a.it.t.length - b.it.t.length; }).slice(0, 24);
    var groups = {}, best = {};
    hits.forEach(function (x) {
      (groups[x.it.k] = groups[x.it.k] || []).push(x.it);
      best[x.it.k] = Math.max(best[x.it.k] || 0, x.s);
    });
    /* strongest group first, so an exact title match never sits below a keyword hit */
    Object.keys(groups).sort(function (a, b) { return best[b] - best[a]; }).forEach(function (k) {
      html += '<p class="pal__group">' + (LABEL[k] || k) + "</p>";
      groups[k].forEach(function (it) {
        html += '<a class="pal__item" href="' + base + it.u + '">' +
          '<span class="pal__ic">' + esc((it.t || "?").slice(0, 2).toUpperCase()) + '</span>' +
          '<span class="pal__txt"><b>' + hi(it.t, q) + '</b><span>' + esc(it.d || "") + "</span></span></a>";
        palRows.push({ href: base + it.u }); n++;
      });
    });
  }
  if (!n) html += '<p class="pal__empty">' + (q.length > 1 ? TXT.noMatch : TXT.typeMore) + "</p>";
  box.innerHTML = html;
  palSel = 0; palMark();
}
function palMark() {
  var items = $$(".pal__item", $("#pal-res"));
  items.forEach(function (el, i) { el.classList.toggle("is-sel", i === palSel); });
  if (items[palSel]) items[palSel].scrollIntoView({ block: "nearest" });
}
var palIn = $(".pal__in");
if (palIn) {
  palIn.addEventListener("input", function () { palRender(palIn.value); });
  palIn.addEventListener("keydown", function (e) {
    var items = $$(".pal__item", $("#pal-res"));
    if (e.key === "ArrowDown") { e.preventDefault(); palSel = Math.min(items.length - 1, palSel + 1); palMark(); }
    if (e.key === "ArrowUp") { e.preventDefault(); palSel = Math.max(0, palSel - 1); palMark(); }
    if (e.key === "Enter") {
      e.preventDefault();
      var r = palRows[palSel]; if (!r) return;
      if (r.act) r.act.act(); else location.href = r.href;
    }
  });
}
var palResBox = $("#pal-res");
if (palResBox) palResBox.addEventListener("click", function (e) {
  var b = e.target.closest("[data-act]");
  if (b) { e.preventDefault(); ACTIONS[+b.dataset.act].act(); }
});

/* ── symptom scanner ─────────────────────────────────────── */
var SC = null, scStep = 0, scAns = {};
try { SC = JSON.parse($("#scanner-data") ? $("#scanner-data").textContent : "null"); } catch (e) { SC = null; }
function scOpen() { scStep = 0; scAns = {}; scDraw(); }
function scDraw() {
  if (!SC) return;
  var body = $(".sc__body"), q = $(".sc__q"), bar = $(".sc__bar i"), stepEl = $(".sc__step b");
  var back = $("[data-sc=back]"), next = $("[data-sc=next]");
  if (scStep >= SC.steps.length) return scResult();
  var s = SC.steps[scStep];
  q.textContent = s.q;
  bar.style.width = ((scStep) / SC.steps.length * 100) + "%";
  if (stepEl) stepEl.textContent = scStep + 1;
  back.disabled = scStep === 0;
  next.textContent = scStep === SC.steps.length - 1 ? "Δείτε το αποτέλεσμα" : "Συνέχεια";
  next.hidden = false; back.hidden = false;
  var picked = scAns[s.id] || [];
  body.innerHTML = (s.help ? '<p class="sc__help">' + esc(s.help) + "</p>" : "") +
    '<ul class="sc__opts">' + s.options.map(function (o) {
      return '<li><label class="sc__opt"><input type="' + (s.type === "multi" ? "checkbox" : "radio") +
        '" name="' + s.id + '" value="' + o.id + '"' + (picked.indexOf(o.id) > -1 ? " checked" : "") +
        '><span class="sc__box"></span><span>' + esc(o.label) + "</span></label></li>";
    }).join("") + "</ul>";
  body.querySelectorAll("input").forEach(function (inp) {
    inp.addEventListener("change", function () {
      var vals = Array.prototype.slice.call(body.querySelectorAll("input:checked")).map(function (x) { return x.value; });
      scAns[s.id] = vals;
    });
  });
  body.scrollTop = 0;
}
function scResult() {
  var body = $(".sc__body"), q = $(".sc__q"), bar = $(".sc__bar i"), stepEl = $(".sc__step");
  var scores = {};
  SC.steps.forEach(function (s) {
    (scAns[s.id] || []).forEach(function (id) {
      var o = s.options.filter(function (x) { return x.id === id; })[0];
      if (!o) return;
      Object.keys(o.w || {}).forEach(function (c) { scores[c] = (scores[c] || 0) + o.w[c]; });
    });
  });
  var ranked = Object.keys(scores).map(function (k) { return { k: k, v: scores[k] }; })
    .sort(function (a, b) { return b.v - a.v; }).filter(function (x) { return x.v > 0; }).slice(0, 3);
  var max = ranked.length ? ranked[0].v : 1;
  q.textContent = ranked.length ? "Τι ταιριάζει με όσα περιγράψατε" : "Δεν επιλέξατε κάποιο σύμπτωμα";
  bar.style.width = "100%";
  if (stepEl) stepEl.textContent = "Αποτέλεσμα";
  $("[data-sc=next]").hidden = true;
  $("[data-sc=back]").hidden = false;
  if (!ranked.length) {
    body.innerHTML = '<p class="sc__help">Γυρίστε πίσω και διαλέξτε ό,τι σας ταιριάζει, ή ζητήστε ' +
      "απευθείας μια εκτίμηση.</p>" + '<button class="btn btn--cta" type="button" data-open="book">Ζητήστε ραντεβού</button>';
    return;
  }
  var seen = {}, treats = [];
  ranked.forEach(function (r) {
    (SC.conditions[r.k].treatments || []).forEach(function (t) { if (!seen[t]) { seen[t] = 1; treats.push(t); } });
  });
  body.innerHTML = '<div class="sc__res">' + ranked.map(function (r) {
    var c = SC.conditions[r.k], pct = Math.round(r.v / max * 100);
    return '<article class="sc__match"><span class="sc__pct">' + pct + "%</span>" +
      "<h3>" + esc(c.title) + "</h3><p>" + esc(c.lead) + "</p>" +
      '<div class="sc__meter"><i data-w="' + pct + '"></i></div>' +
      '<a class="btn btn--sm btn--ghost" href="' + base + c.url + '">Διαβάστε περισσότερα</a></article>';
  }).join("") + "</div>" +
    '<p class="sc__help" style="margin-top:1.4rem">Θεραπείες που συζητούνται συνήθως σε αυτές τις περιπτώσεις:</p>' +
    '<div class="chips">' + treats.map(function (t) {
      var tr = SC.treatments[t];
      return '<a class="chip" href="' + base + tr.url + '">' + esc(tr.title) + " · " + esc(tr.level) + "</a>";
    }).join("") + "</div>" +
    '<div class="sc__flags"><h3>Ζητήστε εκτίμηση σύντομα αν έχετε</h3><ul>' +
      SC.flags.map(function (f) { return "<li>" + esc(f) + "</li>"; }).join("") + "</ul></div>" +
    '<p class="sc__note">Αυτό δεν είναι διάγνωση. Είναι ένας τρόπος να βάλετε λέξεις σε αυτό που ' +
      "νιώθετε πριν το συζητήσετε με γιατρό. Ο υπολογισμός έγινε στη συσκευή σας.</p>" +
    '<div class="bk__acts" style="justify-content:flex-start;margin-top:1.2rem">' +
      '<button class="btn btn--cta" type="button" data-open="book">Ζητήστε ραντεβού</button>' +
      '<button class="btn btn--ghost" type="button" data-sc="restart">Νέα σάρωση</button></div>';
  requestAnimationFrame(function () {
    $$(".sc__meter i", body).forEach(function (i) { i.style.width = i.dataset.w + "%"; });
  });
}
D.addEventListener("click", function (e) {
  var b = e.target.closest("[data-sc]"); if (!b) return;
  if (b.dataset.sc === "next") { if (scStep < SC.steps.length) { scStep++; scDraw(); } }
  if (b.dataset.sc === "back") { if (scStep > 0) { scStep--; scDraw(); } }
  if (b.dataset.sc === "restart") { scOpen(); }
});

/* ── anatomy explorer ────────────────────────────────────── */
(function anatomy() {
  var stage = $(".an__stage"); if (!stage) return;
  var panel = $(".an__panel"), picks = $$(".an__pick");
  var COPY = window.__ORGANS || {};
  function select(k) {
    picks.forEach(function (p) { p.classList.toggle("is-on", p.dataset.organ === k); });
    $$("[data-organ-hit]", stage).forEach(function (h) { h.classList.toggle("is-active", h.dataset.organHit === k); });
    var c = COPY[k];
    if (panel && c) panel.innerHTML = "<h3>" + esc(c.title) + "</h3><p>" + esc(c.text) + "</p>" +
      (c.links && c.links.length ? "<ul>" + c.links.map(function (l) {
        return '<li><a href="' + base + l.u + '">' + esc(l.t) + "</a></li>"; }).join("") + "</ul>" : "");
  }
  picks.forEach(function (p) { p.addEventListener("click", function () { select(p.dataset.organ); }); });
  $$("[data-organ-hit]", stage).forEach(function (h) {
    h.setAttribute("tabindex", "0"); h.setAttribute("role", "button");
    h.addEventListener("click", function () { select(h.dataset.organHit); });
    h.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select(h.dataset.organHit); }
    });
  });
  var toggle = $(".an__toggle", stage), thumb = $(".an__thumb", stage);
  if (toggle) {
    var btns = $$("button", toggle);
    function place(b) {
      if (!thumb) return;
      thumb.style.setProperty("--tw", b.offsetWidth + "px");
      thumb.style.setProperty("--tx", (b.offsetLeft - 4) + "px");
    }
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        stage.dataset.state = b.dataset.state; place(b);
      });
    });
    requestAnimationFrame(function () { place(btns[0]); stage.dataset.state = "normal"; });
    W.addEventListener("resize", function () {
      var on = btns.filter(function (b) { return b.getAttribute("aria-pressed") === "true"; })[0];
      if (on) place(on);
    });
  }
  select(stage.dataset.default || "bladder");
})();

/* ── kegel trainer ───────────────────────────────────────── */
(function kegel() {
  var ring = $(".kg__ring"); if (!ring) return;
  var bar = $(".kg__bar", ring), phaseEl = $(".kg__phase", ring), countEl = $(".kg__count", ring);
  var repEl = $(".kg__rep", ring), toggle = $("[data-kegel=toggle]"), reset = $("[data-kegel=reset]");
  var clear = $("[data-kegel=clear]"), sessEl = $("[data-kegel-sessions]");
  var progs = $$(".kg__prog"), C = 2 * Math.PI * 104;
  var cfg = null, running = false, t0 = 0, phase = 0, rep = 0, raf = null;
  var PH = [["contract", TXT.phases[0], "c"], ["hold", TXT.phases[1], "h"], ["release", TXT.phases[2], "r"]];
  bar.style.strokeDasharray = C;
  function setProg(b) {
    progs.forEach(function (p) { p.classList.toggle("is-on", p === b); });
    cfg = { c: +b.dataset.c, h: +b.dataset.h, r: +b.dataset.r, reps: +b.dataset.reps };
    stop(); draw(0, "idle", TXT.ready, "0");
    repEl.textContent = "0 / " + cfg.reps;
  }
  progs.forEach(function (b) { b.addEventListener("click", function () { setProg(b); }); });
  if (progs.length) setProg(progs[0]);
  function draw(p, ph, label, count) {
    bar.style.strokeDashoffset = C * (1 - p);
    ring.dataset.phase = ph;
    phaseEl.textContent = label;
    countEl.textContent = count;
  }
  function tick() {
    var dur = cfg[PH[phase][2]] * 1000;
    var el = performance.now() - t0;
    var p = Math.min(1, el / dur);
    draw(p, PH[phase][0], PH[phase][1], Math.max(1, Math.ceil((dur - el) / 1000)));
    if (p >= 1) {
      phase++;
      if (phase >= PH.length) {
        phase = 0; rep++;
        repEl.textContent = rep + " / " + cfg.reps;
        if (rep >= cfg.reps) return finish();
      }
      t0 = performance.now();
    }
    raf = requestAnimationFrame(tick);
  }
  function start() {
    running = true; toggle.textContent = TXT.pause; phase = 0; t0 = performance.now();
    raf = requestAnimationFrame(tick);
  }
  function stop() {
    running = false; if (raf) cancelAnimationFrame(raf); raf = null;
    if (toggle) toggle.textContent = TXT.start;
  }
  function finish() {
    stop(); draw(1, "done", TXT.done, "✓");
    var n = (get(K.kegel, 0) || 0) + 1; set(K.kegel, n); showSess();
    toast(TXT.sessionDone);
    rep = 0;
  }
  function showSess() { if (sessEl) sessEl.textContent = get(K.kegel, 0) || 0; }
  if (toggle) toggle.addEventListener("click", function () { running ? stop() : start(); });
  if (reset) reset.addEventListener("click", function () {
    stop(); rep = 0; phase = 0; draw(0, "idle", TXT.ready, "0"); repEl.textContent = "0 / " + cfg.reps;
  });
  if (clear) clear.addEventListener("click", function () { del(K.kegel); showSess(); toast(TXT.reset); });
  showSess();
})();

/* ── compare filters ─────────────────────────────────────── */
(function compare() {
  var box = $("#compare"); if (!box) return;
  $$(".chip", box).forEach(function (c) {
    c.addEventListener("click", function () {
      $$(".chip", box).forEach(function (x) { x.classList.toggle("is-on", x === c); });
      var f = c.dataset.inv;
      $$("[data-inv]", box).forEach(function (cell) {
        cell.classList.toggle("is-off", f !== "all" && cell.dataset.inv !== f);
      });
    });
  });
})();

/* ── booking ─────────────────────────────────────────────── */
(function booking() {
  var form = $(".bk__form"); if (!form) return;
  var dateI = $("#bk-date"), timeI = $("#bk-time"), sunday = $("[data-sunday]");
  var today = new Date(); today.setHours(0, 0, 0, 0);
  if (dateI) dateI.min = today.toISOString().slice(0, 10);
  function slots() {
    if (!dateI || !timeI) return;
    var v = dateI.value; timeI.innerHTML = '<option value="">—</option>';
    if (!v) return;
    var d = new Date(v + "T00:00:00"), day = d.getDay();
    if (sunday) sunday.classList.toggle("is-on", day === 0);
    if (day === 0) { timeI.disabled = true; return; }
    timeI.disabled = false;
    var last = day === 6 ? 14.5 : 16.5;
    for (var t = 9; t <= last; t += .5) {
      var hh = Math.floor(t), mm = t % 1 ? "30" : "00";
      var o = D.createElement("option");
      o.value = o.textContent = (hh < 10 ? "0" : "") + hh + ":" + mm;
      timeI.appendChild(o);
    }
  }
  if (dateI) dateI.addEventListener("change", slots);
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var ok = true;
    ["name", "phone"].forEach(function (n) {
      var el = form.elements[n], fld = el.parentElement;
      var bad = !el.value.trim();
      fld.classList.toggle("is-bad", bad);
      if (bad) ok = false;
    });
    var consent = form.elements.consent;
    $(".err--consent").classList.toggle("is-on", !consent.checked);
    if (!consent.checked) ok = false;
    if (!ok) { toast(TXT.checkFields); return; }
    var f = form.elements;
    var lines = [
      "Ονοματεπώνυμο: " + f.name.value.trim(),
      "Τηλέφωνο: " + f.phone.value.trim(),
      f.email.value.trim() ? "Email: " + f.email.value.trim() : "",
      f.topic.value ? "Θέμα: " + f.topic.value : "Θέμα: δεν είμαι σίγουρη",
      f.date.value ? "Προτίμηση ημερομηνίας: " + f.date.value + (f.time.value ? " " + f.time.value : "") : "",
      "", f.note.value.trim()
    ].filter(Boolean).join("\n");
    var href = "mailto:" + "info@lvriathens.com" +
      "?subject=" + encodeURIComponent("Αίτημα ραντεβού — " + f.name.value.trim()) +
      "&body=" + encodeURIComponent(lines);
    location.href = href;
    toast(TXT.mailOpening);
  });
})();

/* ── video player ────────────────────────────────────────── */
D.addEventListener("click", function (e) {
  var b = e.target.closest("[data-video]"); if (!b) return;
  e.preventDefault();
  var frame = $(".pl__frame"); if (!frame) return;
  frame.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + b.dataset.video +
    '?autoplay=1&rel=0" title="Βίντεο" allow="accelerometer;autoplay;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe>';
  openOv("player");
});

/* ── gallery ─────────────────────────────────────────────── */
(function gallery() {
  var gal = $(".gal"); if (!gal) return;
  var unlock = $("[data-unlock]");
  if (get(K.gal, false) === true) gal.classList.remove("is-locked");
  if (unlock) unlock.addEventListener("click", function () {
    gal.classList.remove("is-locked"); set(K.gal, true);
    var c = unlock.closest(".consent"); if (c) c.hidden = true;
  });
  var imgs = $$(".gal__i", gal), cur = 0;
  var lb = $("#lightbox"), lbImg = lb && $("img", lb), cap = lb && $("figcaption", lb);
  function open(i) {
    if (gal.classList.contains("is-locked")) { toast(TXT.unlockFirst); return; }
    cur = (i + imgs.length) % imgs.length;
    var src = imgs[cur].dataset.full || $("img", imgs[cur]).src;
    lbImg.src = src; lbImg.alt = imgs[cur].dataset.alt || "";
    cap.textContent = (cur + 1) + " / " + imgs.length + (imgs[cur].dataset.cap ? " · " + imgs[cur].dataset.cap : "");
    openOv("lightbox");
  }
  imgs.forEach(function (b, i) { b.addEventListener("click", function () { open(i); }); });
  if (lb) {
    $(".lb__nav--l", lb).addEventListener("click", function () { open(cur - 1); });
    $(".lb__nav--r", lb).addEventListener("click", function () { open(cur + 1); });
    D.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "ArrowLeft") open(cur - 1);
      if (e.key === "ArrowRight") open(cur + 1);
    });
  }
  var filters = $$("[data-gal-filter]");
  filters.forEach(function (f) {
    f.addEventListener("click", function () {
      filters.forEach(function (x) { x.classList.toggle("is-on", x === f); });
      imgs.forEach(function (im) {
        im.hidden = f.dataset.galFilter !== "all" && im.dataset.cat !== f.dataset.galFilter;
      });
    });
  });
})();

/* ── FAQ ─────────────────────────────────────────────────── */
$$(".faq__q").forEach(function (q) {
  q.addEventListener("click", function () {
    var on = q.getAttribute("aria-expanded") === "true";
    q.setAttribute("aria-expanded", String(!on));
    var a = D.getElementById(q.getAttribute("aria-controls"));
    if (a) a.hidden = on;
  });
});
if (location.hash && location.hash.indexOf("#faq-") === 0) {
  var target = $(location.hash);
  if (target) { var qb = $(".faq__q", target); if (qb) qb.click(); }
}

/* ── table of contents scroll-spy ────────────────────────── */
(function toc() {
  var nav = $(".toc"); if (!nav) return;
  var links = $$("a", nav);
  var heads = links.map(function (a) { return D.getElementById(a.hash.slice(1)); }).filter(Boolean);
  if (!heads.length) { nav.remove(); return; }
  var spy = new IntersectionObserver(function (en) {
    en.forEach(function (x) {
      if (!x.isIntersecting) return;
      links.forEach(function (a) { a.classList.toggle("is-on", a.hash === "#" + x.target.id); });
    });
  }, { rootMargin: "-15% 0px -70% 0px" });
  heads.forEach(function (h) { spy.observe(h); });
})();

/* ── cookie bar ──────────────────────────────────────────── */
(function cookie() {
  var bar = $("#cookie"); if (!bar) return;
  if (get(K.ck, null)) return;
  setTimeout(function () { bar.hidden = false; }, 1400);
  $$("[data-ck]", bar).forEach(function (b) {
    b.addEventListener("click", function () { set(K.ck, b.dataset.ck); bar.hidden = true; });
  });
})();

/* ── view transitions between pages ──────────────────────── */
if (D.startViewTransition && !reduced && prefs.motion) {
  D.addEventListener("click", function (e) {
    var a = e.target.closest("a[href]");
    if (!a || a.target || a.hasAttribute("download") || e.metaKey || e.ctrlKey || e.shiftKey) return;
    var u = new URL(a.href, location.href);
    if (u.origin !== location.origin || u.pathname === location.pathname) return;
    e.preventDefault();
    D.startViewTransition(function () { location.href = a.href; });
  });
}
})();
