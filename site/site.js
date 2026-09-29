const heroStats = document.getElementById('hero-stats');
const sectionSummary = document.getElementById('section-summary');
const coreSystems = document.getElementById('core-systems');
const catalog = document.getElementById('catalog');
const catalogCount = document.getElementById('catalog-count');
const searchInput = document.getElementById('search');
const sectionSelect = document.getElementById('section');
const statusSelect = document.getElementById('status');
const resetButton = document.getElementById('reset-filters');

async function getJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

function renderHero(summary) {
  const stats = [
    ['Systems', summary.summary.system_count],
    ['Core Systems', summary.core_systems.length],
    ['Sections', summary.sections.length],
    ['Statuses', Object.keys(summary.summary.by_status).length],
  ];

  heroStats.innerHTML = stats
    .map(
      ([label, value]) => `
        <article class="stat">
          <h2>${value}</h2>
          <p>${label}</p>
        </article>
      `,
    )
    .join('');
}

function renderSections(sections) {
  sectionSummary.innerHTML = sections
    .map(
      (section) => `
        <article class="system-card">
          <h3>${section.section_name}</h3>
          <p class="section-note">${section.section}</p>
          <div class="pill-row">
            <span class="pill">${section.count} systems</span>
          </div>
        </article>
      `,
    )
    .join('');
}

function renderCore(systems) {
  coreSystems.innerHTML = systems
    .map(
      (system) => `
        <article class="system-card">
          <h3>${system.id}. ${system.name}</h3>
          <p>${system.purpose}</p>
          <div class="pill-row">
            <span class="pill">${system.priority}</span>
            <span class="pill">${system.operational_status}</span>
          </div>
        </article>
      `,
    )
    .join('');
}

function renderCatalog(result) {
  catalogCount.textContent = `${result.count} systems shown`;
  catalog.innerHTML = result.systems
    .map(
      (system) => `
        <article class="system-card">
          <h3>${system.id}. ${system.name}</h3>
          <p>${system.purpose}</p>
          <p class="system-meta">${system.section_name}</p>
          <div class="pill-row">
            <span class="pill">${system.asset_class}</span>
            <span class="pill">${system.operational_status}</span>
            <span class="pill">${system.security_class}</span>
          </div>
        </article>
      `,
    )
    .join('');
}

function buildCatalogUrl() {
  const params = new URLSearchParams();
  if (searchInput.value.trim()) params.set('search', searchInput.value.trim());
  if (sectionSelect.value) params.set('section', sectionSelect.value);
  if (statusSelect.value) params.set('status', statusSelect.value);
  return `/v1/public/catalog?${params.toString()}`;
}

async function refreshCatalog() {
  renderCatalog(await getJson(buildCatalogUrl()));
}

function populateFilters(summary) {
  const sectionOptions = [
    '<option value="">All sections</option>',
    ...summary.sections.map(
      (section) =>
        `<option value="${section.section}">${section.section_name}</option>`,
    ),
  ];
  sectionSelect.innerHTML = sectionOptions.join('');

  const statusOptions = [
    '<option value="">All statuses</option>',
    ...Object.keys(summary.summary.by_status).map(
      (status) => `<option value="${status}">${status}</option>`,
    ),
  ];
  statusSelect.innerHTML = statusOptions.join('');
}

async function boot() {
  const summary = await getJson('/v1/public/summary');
  renderHero(summary);
  renderSections(summary.sections);
  renderCore(summary.core_systems);
  populateFilters(summary);
  await refreshCatalog();
}

searchInput.addEventListener('input', refreshCatalog);
sectionSelect.addEventListener('change', refreshCatalog);
statusSelect.addEventListener('change', refreshCatalog);
resetButton.addEventListener('click', async () => {
  searchInput.value = '';
  sectionSelect.value = '';
  statusSelect.value = '';
  await refreshCatalog();
});

boot().catch((error) => {
  catalog.innerHTML = `<article class="system-card"><h3>Unable to load catalog</h3><p>${error.message}</p></article>`;
});
