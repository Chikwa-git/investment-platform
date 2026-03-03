const API_BASE = "http://127.0.0.1:8000";

function formatMDYtoBR(mdy) {
  // "03-02-2026" -> "02/03/2026"
  const [mm, dd, yyyy] = String(mdy).split("-");
  if (!mm || !dd || !yyyy) return mdy;
  return `${dd}/${mm}/${yyyy}`;
}

function setVisible(id, isVisible) {
  const el = document.getElementById(id);
  el.classList.toggle("d-none", !isVisible);
}

function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function buildFxCard({ label, rate, extras, stale, days_back, as_of, source }) {
  const isStale = !!stale;
  const daysBack = days_back ?? 0;

  // seu as_of vem "MM-DD-YYYY", então NÃO usa new Date aqui por enquanto
  const asOf = as_of ? formatMDYtoBR(as_of) : "-";
  const src = source ?? "BCB PTAX";

  const badge = isStale
    ? `<span class="badge badge-stale ms-2">stale (${daysBack}d)</span>`
    : `<span class="badge text-bg-success ms-2">atual</span>`;

  return `
    <div class="col-12 col-md-6">
      <div class="card p-3">
        <div class="d-flex align-items-center justify-content-between">
          <div>
            <div class="muted-small">${escapeHtml(label)} ${badge}</div>
            <div class="rate-big">R$ ${Number(rate).toFixed(4)}</div>
          </div>
          <div class="text-end">
            <div class="muted-small">As of</div>
            <div class="fw-semibold">${escapeHtml(asOf)}</div>
          </div>
        </div>

        <hr class="my-3"/>

        <div class="d-flex justify-content-between muted-small">
          <span>Fonte: ${escapeHtml(src)}</span>
          <span>Fallback: ${daysBack} dia(s)</span>
        </div>
      </div>
    </div>
  `;
}

async function loadMarketSummary() {
  setVisible("market-error", false);
  setVisible("market-cards", false);
  setVisible("market-loading", true);

  const statusEl = document.getElementById("market-status");
  statusEl.textContent = "";

  try {
    const res = await fetch(`${API_BASE}/api/market/summary`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();

    const items = [data.usd, data.eur].filter(Boolean);
        if (items.length === 0) {
        throw new Error("Resposta vazia (usd/eur).");
        }

    const cardsHtml = items.map(buildFxCard).join("");
    document.getElementById("market-cards").innerHTML = cardsHtml;
    const order = { "USD/BRL": 1, "EUR/BRL": 2 };
    items.sort((a, b) => (order[a.label] ?? 99) - (order[b.label] ?? 99));

    // status geral (ex: se qualquer item stale, mostra aviso)
const anyStale = items.some((it) => it?.stale);
    statusEl.innerHTML = anyStale
      ? `<span class="badge badge-stale">Alguns dados estão stale</span>`
      : `<span class="badge text-bg-success">Dados atualizados</span>`;

    setVisible("market-loading", false);
    setVisible("market-cards", true);
  } catch (err) {
    setVisible("market-loading", false);
    setVisible("market-cards", false);

    const msg = `Erro ao carregar /api/market/summary: ${err.message}`;
    const errEl = document.getElementById("market-error");
    errEl.textContent = msg;
    setVisible("market-error", true);
  }
}

function setupStockSearch() {
  const input = document.getElementById("stock-input");
  const button = document.getElementById("stock-search-btn");
  const error = document.getElementById("stock-search-error");

  if (!input || !button) return;

  function handleSearch() {
    const ticker = input.value.trim().toUpperCase();

    if (!ticker || ticker.length < 4) {
      error.classList.remove("d-none");
      return;
    }

    error.classList.add("d-none");

    // navegação simulada (fluxo real)
    window.location.href = `./stock.html?ticker=${encodeURIComponent(ticker)}`;
  }

  button.addEventListener("click", handleSearch);

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") handleSearch();
  });
}

function debounce(fn, delay = 300) {
  let timer = null;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

function renderStockResults(items) {
  const box = document.getElementById("stock-results");
  if (!box) return;

  if (!items || items.length === 0) {
    box.classList.add("d-none");
    box.innerHTML = "";
    return;
  }

  box.innerHTML = items
    .map(
      (it) => `
        <button type="button" class="list-group-item list-group-item-action"
          data-ticker="${escapeHtml(it.ticker)}">
          <div class="d-flex justify-content-between">
            <span class="fw-semibold">${escapeHtml(it.ticker)}</span>
            <span class="text-secondary">${escapeHtml(it.name)}</span>
          </div>
        </button>
      `
    )
    .join("");

  box.classList.remove("d-none");

  // click handler (event delegation)
  box.onclick = (e) => {
    const btn = e.target.closest("[data-ticker]");
    if (!btn) return;
    const ticker = btn.getAttribute("data-ticker");
    window.location.href = `./stock.html?ticker=${encodeURIComponent(ticker)}`;
  };
}

function setupStockSearch() {
  const input = document.getElementById("stock-input");
  const button = document.getElementById("stock-search-btn");
  const error = document.getElementById("stock-search-error");
  const resultsBox = document.getElementById("stock-results");

  if (!input || !button) return;

  const doSearch = debounce(async () => {
    const q = input.value.trim();
    if (q.length < 2) {
      error?.classList.add("d-none");
      renderStockResults([]);
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/api/stocks/search?q=${encodeURIComponent(q)}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      renderStockResults(data.items || []);
    } catch (err) {
      console.error("Autocomplete error:", err);
      renderStockResults([]);
    }
  }, 300);

  input.addEventListener("input", () => {
    error?.classList.add("d-none");
    doSearch();
  });

  input.addEventListener("focus", () => {
    if (input.value.trim().length >= 2) doSearch();
  });

  // fechar dropdown ao clicar fora
  document.addEventListener("click", (e) => {
    if (!resultsBox) return;
    const clickedInside = e.target.closest("#stock-results") || e.target.closest("#stock-input");
    if (!clickedInside) renderStockResults([]);
  });

  function goWithFirstResult() {
    // se tiver resultados, entra no primeiro
    if (!resultsBox || resultsBox.classList.contains("d-none")) return false;
    const first = resultsBox.querySelector("[data-ticker]");
    if (!first) return false;
    const ticker = first.getAttribute("data-ticker");
    window.location.href = `./stock.html?ticker=${encodeURIComponent(ticker)}`;
    return true;
  }

  button.addEventListener("click", () => {
    const q = input.value.trim();
    if (q.length < 2) {
      error?.classList.remove("d-none");
      return;
    }
    // tenta usar o primeiro resultado; senão, tenta como ticker direto
    if (!goWithFirstResult()) {
      window.location.href = `./stock.html?ticker=${encodeURIComponent(q.toUpperCase())}`;
    }
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      button.click();
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadMarketSummary();
  setupStockSearch();
});