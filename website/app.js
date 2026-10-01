const heroStats = document.getElementById('hero-stats');
const sectionSummary = document.getElementById('section-summary');
const coreSystems = document.getElementById('core-systems');
const algoTrajSystems = document.getElementById('algo-traj-systems');
const catalog = document.getElementById('catalog');
const catalogCount = document.getElementById('catalog-count');
const searchInput = document.getElementById('search');
const sectionSelect = document.getElementById('section');
const statusSelect = document.getElementById('status');
const resetButton = document.getElementById('reset-filters');

let allSystems = [];

async function getJson(path) {
  const response = await fetch(path);
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

function renderAlgoTrajSystems(systems) {
  algoTrajSystems.innerHTML = systems
    .map(
      (system) => `
        <article class="system-card trajectory-card">
          <h3>${system.id}. ${system.name}</h3>
          <p>${system.purpose}</p>
          <div class="pill-row">
            <span class="pill">${system.priority}</span>
            <span class="pill">${system.operational_status}</span>
            <span class="pill">${system.security_class}</span>
          </div>
        </article>
      `,
    )
    .join('');
}

function renderCatalog(systems) {
  catalogCount.textContent = `${systems.length} systems shown`;
  catalog.innerHTML = systems
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

function populateFilters(summary, catalogData) {
  const sectionOptions = [
    '<option value="">All sections</option>',
    ...summary.sections.map(
      (section) =>
        `<option value="${section.section}">${section.section_name}</option>`,
    ),
  ];
  sectionSelect.innerHTML = sectionOptions.join('');

  const statuses = [...new Set(catalogData.systems.map((system) => system.operational_status))];
  statusSelect.innerHTML = [
    '<option value="">All statuses</option>',
    ...statuses.map((status) => `<option value="${status}">${status}</option>`),
  ].join('');
}

function applyFilters() {
  const search = searchInput.value.trim().toLowerCase();
  const section = sectionSelect.value;
  const status = statusSelect.value;

  const filtered = allSystems.filter((system) => {
    if (section && system.section !== section) return false;
    if (status && system.operational_status !== status) return false;
    if (!search) return true;
    return (
      system.id.toLowerCase().includes(search) ||
      system.name.toLowerCase().includes(search) ||
      system.purpose.toLowerCase().includes(search) ||
      system.section_name.toLowerCase().includes(search)
    );
  });

  renderCatalog(filtered);
}

async function boot() {
  const [summary, catalogData, core] = await Promise.all([
    getJson('./data/summary.json'),
    getJson('./data/catalog.json'),
    getJson('./data/core.json'),
  ]);

  allSystems = catalogData.systems;
  renderHero(summary);
  renderSections(summary.sections);
  renderCore(core.systems);
  renderAlgoTrajSystems(
    allSystems.filter((system) =>
      ['003', '023', '041', '051', '105'].includes(system.id),
    ),
  );
  populateFilters(summary, catalogData);
  applyFilters();
}

searchInput.addEventListener('input', applyFilters);
sectionSelect.addEventListener('change', applyFilters);
statusSelect.addEventListener('change', applyFilters);
resetButton.addEventListener('click', () => {
  searchInput.value = '';
  sectionSelect.value = '';
  statusSelect.value = '';
  applyFilters();
});

boot().catch((error) => {
  catalog.innerHTML = `<article class="system-card"><h3>Unable to load website data</h3><p>${error.message}</p></article>`;
});
