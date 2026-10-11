/**
 * Maldives Statistical Yearbook 2021 — Minimalist Dashboard Logic
 * Linear / Vercel monochrome aesthetic with single restrained accent.
 */

// Global Chart Store
const charts = {};

// Helper: Format Numbers with Commas
function formatNum(num) {
  if (num === null || num === undefined) return 'N/A';
  return Number(num).toLocaleString();
}

// Helper: Get Theme Chart Colors (Vercel / Linear Minimalist)
function getChartTheme() {
  const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
  return {
    textColor: isDark ? '#71717a' : '#71717a',
    headingColor: isDark ? '#f4f4f5' : '#09090b',
    gridColor: isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)',
    accent: isDark ? '#38bdf8' : '#0284c7',
    accentMuted: isDark ? 'rgba(56, 189, 248, 0.08)' : 'rgba(2, 132, 199, 0.08)',
    barBase: isDark ? '#27272a' : '#e4e4e7',
    barHover: isDark ? '#3f3f46' : '#d4d4d8',
    statusNeg: isDark ? '#f43f5e' : '#e11d48',
    statusPos: isDark ? '#10b981' : '#059669',
    tooltipBg: isDark ? '#18181b' : '#ffffff',
    tooltipBorder: isDark ? '#27272a' : '#e4e4e7',
    tooltipText: isDark ? '#f4f4f5' : '#09090b',
  };
}

// Destroy Chart Instance safely
function destroyChart(id) {
  if (charts[id]) {
    charts[id].destroy();
    delete charts[id];
  }
}

// ==========================================================================
// Initialization & Data Loading
// ==========================================================================
document.addEventListener('DOMContentLoaded', async () => {
  initTheme();
  initTabs();
  
  let data = window.MALDIVES_DATA;
  if (!data) {
    try {
      const res = await fetch('dashboard_data.json');
      data = await res.json();
      window.MALDIVES_DATA = data;
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
      return;
    }
  }

  // Render initial dashboard view
  renderInterestingFacts(data.interesting_facts);
  renderCatalogExplorer(data.catalog);
  renderGeographySection(data.geography);
  renderTourismSection(data.tourism);
  renderGdpSection(data.gdp);
  renderFisheriesSection(data.fisheries);
  renderPublicFinanceSection(data.public_finance);
  renderWaterSection(data.water);
  renderExecutiveSection(data);
});

// ==========================================================================
// Theme Management (Light / Dark)
// ==========================================================================
function initTheme() {
  const toggleBtn = document.getElementById('theme-toggle-btn');
  const stored = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', stored);
  updateThemeIcon(stored);

  toggleBtn?.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateThemeIcon(next);
    refreshAllCharts();
  });
}

function updateThemeIcon(theme) {
  const svg = document.getElementById('theme-icon-svg');
  if (svg) {
    if (theme === 'light') {
      // Moon icon
      svg.innerHTML = `
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
      `;
    } else {
      // Sun icon
      svg.innerHTML = `
        <circle cx="12" cy="12" r="5"></circle>
        <line x1="12" y1="1" x2="12" y2="3"></line>
        <line x1="12" y1="21" x2="12" y2="23"></line>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
        <line x1="1" y1="12" x2="3" y2="12"></line>
        <line x1="21" y1="12" x2="23" y2="12"></line>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
      `;
    }
  }
}

function refreshAllCharts() {
  const data = window.MALDIVES_DATA;
  if (!data) return;
  renderGeographySection(data.geography);
  renderTourismSection(data.tourism);
  renderGdpSection(data.gdp);
  renderFisheriesSection(data.fisheries);
  renderPublicFinanceSection(data.public_finance);
  renderWaterSection(data.water);
  renderExecutiveSection(data);
}

// ==========================================================================
// Tab Switching
// ==========================================================================
function initTabs() {
  const triggers = document.querySelectorAll('.tab-trigger');
  triggers.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-tab');
      
      triggers.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      document.querySelectorAll('.tab-pane').forEach(c => {
        c.classList.remove('active');
      });
      
      const targetContent = document.getElementById(targetId);
      if (targetContent) {
        targetContent.classList.add('active');
        window.dispatchEvent(new Event('resize'));
      }
    });
  });
}

// ==========================================================================
// Curated Insights (Minimal Card Deck)
// ==========================================================================
function renderInterestingFacts(facts) {
  const container = document.getElementById('facts-cards-row');
  const filterBtns = document.querySelectorAll('.fact-filter-btn');
  if (!container || !facts) return;

  function display(category = 'All') {
    container.innerHTML = '';
    const filtered = category === 'All' ? facts : facts.filter(f => f.category === category);
    
    filtered.forEach(fact => {
      const card = document.createElement('div');
      card.className = 'fact-item';
      card.innerHTML = `
        <div>
          <div class="fact-tag">${fact.category}</div>
          <h4 class="fact-heading">${fact.headline}</h4>
          <p class="fact-body">${fact.detail}</p>
        </div>
      `;
      container.appendChild(card);
    });
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      display(btn.getAttribute('data-category'));
    });
  });

  display('All');
}

// ==========================================================================
// 1. Executive Summary & Overview
// ==========================================================================
function renderExecutiveSection(data) {
  const theme = getChartTheme();
  
  destroyChart('execRadarChart');
  const ctx = document.getElementById('execRadarChart')?.getContext('2d');
  if (!ctx) return;

  charts['execRadarChart'] = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Urban Density', 'Tourism Dominance', 'Fish Consumption', 'GDP Volatility', 'Climate Sensitivity', 'Debt Pressure'],
      datasets: [
        {
          label: 'Maldives',
          data: [98, 92, 95, 96, 94, 88],
          borderColor: theme.accent,
          backgroundColor: theme.accentMuted,
          pointBackgroundColor: theme.accent,
          pointRadius: 3,
          borderWidth: 2
        },
        {
          label: 'Global Average Baseline',
          data: [40, 35, 25, 30, 45, 50],
          borderColor: '#52525b',
          backgroundColor: 'transparent',
          pointBackgroundColor: '#52525b',
          pointRadius: 2,
          borderWidth: 1.5,
          borderDash: [3, 3]
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          grid: { color: theme.gridColor },
          angleLines: { color: theme.gridColor },
          pointLabels: { color: theme.textColor, font: { size: 11, family: 'Inter' } },
          ticks: { display: false, max: 100 }
        }
      },
      plugins: {
        legend: { labels: { color: theme.textColor, font: { family: 'Inter', size: 11 } } }
      }
    }
  });
}

// ==========================================================================
// 2. Geography & Urban Density Section
// ==========================================================================
function renderGeographySection(geo) {
  if (!geo) return;
  const theme = getChartTheme();
  
  // Chart 1: Global Density Benchmark (Log Scale)
  destroyChart('densityBenchmarkChart');
  const ctxBench = document.getElementById('densityBenchmarkChart')?.getContext('2d');
  if (ctxBench) {
    const bench = geo.global_benchmarks;
    charts['densityBenchmarkChart'] = new Chart(ctxBench, {
      type: 'bar',
      data: {
        labels: bench.map(b => b.entity),
        datasets: [{
          label: 'Population Density (/km²)',
          data: bench.map(b => b.density),
          backgroundColor: bench.map(b => b.highlight ? (b.density > 20000 ? theme.statusNeg : theme.statusPos) : theme.barBase),
          borderRadius: 3
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'logarithmic',
            grid: { color: theme.gridColor },
            ticks: {
              color: theme.textColor,
              callback: val => val >= 1000 ? (val / 1000) + 'k' : val,
              font: { family: 'JetBrains Mono', size: 10 }
            }
          },
          y: {
            grid: { display: false },
            ticks: { color: theme.textColor, font: { size: 11 } }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText,
            callbacks: {
              label: c => `Density: ${formatNum(c.raw)} / km²`
            }
          }
        }
      }
    });
  }

  // Chart 2: Top 10 Inhabited Islands Population
  destroyChart('topIslandsPopChart');
  const ctxTop = document.getElementById('topIslandsPopChart')?.getContext('2d');
  if (ctxTop) {
    const top10 = geo.localities.slice(0, 10);
    charts['topIslandsPopChart'] = new Chart(ctxTop, {
      type: 'bar',
      data: {
        labels: top10.map(i => i.display_name || i.name),
        datasets: [{
          label: 'Resident Population (Census 2014)',
          data: top10.map(i => i.population),
          backgroundColor: top10.map(i => i.is_capital ? theme.statusNeg : theme.barBase),
          borderRadius: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: theme.textColor, font: { size: 10 } }
          },
          y: {
            grid: { color: theme.gridColor },
            ticks: {
              color: theme.textColor,
              callback: val => val >= 1000 ? (val / 1000) + 'k' : val,
              font: { family: 'JetBrains Mono', size: 10 }
            }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText,
            callbacks: {
              title: items => {
                const item = top10[items[0].dataIndex];
                return `${item.display_name || item.name} • ${item.atoll_name || item.atoll_code}`;
              },
              label: c => `Population: ${formatNum(c.raw)} residents`
            }
          }
        }
      }
    });
  }

  // Inhabited Islands Table
  const tableBody = document.getElementById('islands-table-body');
  const searchInput = document.getElementById('island-search-input');
  const atollSelect = document.getElementById('island-atoll-select');
  const sortSelect = document.getElementById('island-sort-select');
  const countBadge = document.getElementById('islands-count-badge');

  // Populate Atoll filter dropdown
  if (atollSelect && geo.atolls && atollSelect.options.length <= 1) {
    geo.atolls.forEach(att => {
      const opt = document.createElement('option');
      opt.value = att.code;
      opt.textContent = att.code === 'Male'
        ? `Malé City (${att.island_count})`
        : `${att.code} - ${att.name} (${att.island_count})`;
      atollSelect.appendChild(opt);
    });
  }

  function renderTable(list) {
    if (!tableBody) return;
    tableBody.innerHTML = '';
    if (countBadge) {
      countBadge.textContent = `Showing ${list.length} of ${geo.localities.length}`;
    }
    if (list.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 2.5rem; color: var(--text-muted);">No matching localities found. Try clearing filters.</td></tr>`;
      return;
    }
    list.forEach((loc, idx) => {
      const tr = document.createElement('tr');
      const atollPrefix = loc.atoll_code && loc.atoll_code !== 'Male'
        ? `<span class="badge-atoll-tag" title="Administrative Atoll Code">${loc.atoll_code}</span>`
        : '';
      const capitalBadge = loc.is_capital ? '<span class="badge-capital" title="National Capital Area">Capital</span>' : '';
      const atollCapBadge = loc.is_atoll_capital ? '<span class="badge-atoll-cap" title="Atoll Administrative Capital">Atoll Capital</span>' : '';

      tr.innerHTML = `
        <td class="num">${idx + 1}</td>
        <td>
          ${atollPrefix}<strong>${loc.name}</strong>
          ${capitalBadge}${atollCapBadge}
        </td>
        <td>
          <span style="font-weight: 500;">${loc.atoll_name || 'Malé City'}</span>
          ${loc.atoll_code !== 'Male' && loc.atoll_geo ? `<span class="atoll-meta-text">${loc.atoll_geo}</span>` : ''}
        </td>
        <td class="num font-mono">${formatNum(loc.population)}</td>
        <td class="num font-mono">${loc.land_area_ha ? formatNum(loc.land_area_ha) : '—'}</td>
        <td class="num font-mono">${loc.density_km2 ? formatNum(loc.density_km2) : '—'}</td>
        <td class="num font-mono">${loc.distance_km ? formatNum(loc.distance_km) + ' km' : '0 km'}</td>
      `;
      tableBody.appendChild(tr);
    });
  }

  function filterAndSort() {
    let list = [...geo.localities];
    const q = searchInput?.value.toLowerCase().trim() || '';
    const atollVal = atollSelect?.value || 'all';

    if (atollVal !== 'all') {
      list = list.filter(l => l.atoll_code === atollVal);
    }

    if (q) {
      list = list.filter(l =>
        l.name.toLowerCase().includes(q) ||
        (l.display_name && l.display_name.toLowerCase().includes(q)) ||
        (l.atoll_code && l.atoll_code.toLowerCase().includes(q)) ||
        (l.atoll_name && l.atoll_name.toLowerCase().includes(q)) ||
        (l.atoll_geo && l.atoll_geo.toLowerCase().includes(q))
      );
    }

    const sortVal = sortSelect?.value || 'pop-desc';
    if (sortVal === 'pop-desc') list.sort((a, b) => b.population - a.population);
    if (sortVal === 'pop-asc') list.sort((a, b) => a.population - b.population);
    if (sortVal === 'name-asc') list.sort((a, b) => a.name.localeCompare(b.name));
    if (sortVal === 'atoll-asc') {
      const atollOrder = ['Male', 'HA', 'HDh', 'Sh', 'N', 'R', 'B', 'Lh', 'K', 'AA', 'ADh', 'V', 'M', 'F', 'Dh', 'Th', 'L', 'GA', 'GDh', 'Gn', 'S'];
      list.sort((a, b) => {
        const idxA = atollOrder.indexOf(a.atoll_code);
        const idxB = atollOrder.indexOf(b.atoll_code);
        if (idxA !== idxB) return idxA - idxB;
        return a.name.localeCompare(b.name);
      });
    }
    if (sortVal === 'dens-desc') list.sort((a, b) => (b.density_km2 || 0) - (a.density_km2 || 0));
    if (sortVal === 'dist-desc') list.sort((a, b) => (b.distance_km || 0) - (a.distance_km || 0));

    renderTable(list);
  }

  searchInput?.addEventListener('input', filterAndSort);
  atollSelect?.addEventListener('change', filterAndSort);
  sortSelect?.addEventListener('change', filterAndSort);
  renderTable(geo.localities);
}

// ==========================================================================
// 3. Tourism & COVID-19 Disruption Section
// ==========================================================================
function renderTourismSection(tour) {
  if (!tour) return;
  const theme = getChartTheme();

  // Chart 1: Annual Arrivals 2012-2020
  destroyChart('tourAnnualChart');
  const ctxAnn = document.getElementById('tourAnnualChart')?.getContext('2d');
  if (ctxAnn) {
    charts['tourAnnualChart'] = new Chart(ctxAnn, {
      type: 'line',
      data: {
        labels: tour.annual_arrivals.map(a => a.year),
        datasets: [{
          label: 'Annual Arrivals',
          data: tour.annual_arrivals.map(a => a.arrivals),
          borderColor: theme.accent,
          backgroundColor: theme.accentMuted,
          fill: true,
          tension: 0.2,
          borderWidth: 2,
          pointBackgroundColor: theme.accent,
          pointRadius: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { color: theme.gridColor }, ticks: { color: theme.textColor, font: { size: 10 } } },
          y: {
            grid: { color: theme.gridColor },
            ticks: { color: theme.textColor, callback: val => (val / 1000) + 'k', font: { family: 'JetBrains Mono', size: 10 } }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText,
            callbacks: { label: c => `Arrivals: ${formatNum(c.raw)}` }
          }
        }
      }
    });
  }

  // Chart 2: 2020 Monthly Arrivals
  destroyChart('tourMonthlyChart');
  const ctxMon = document.getElementById('tourMonthlyChart')?.getContext('2d');
  if (ctxMon) {
    charts['tourMonthlyChart'] = new Chart(ctxMon, {
      type: 'bar',
      data: {
        labels: tour.monthly_2020.map(m => m.month),
        datasets: [{
          label: '2020 Monthly Arrivals',
          data: tour.monthly_2020.map(m => m.arrivals),
          backgroundColor: tour.monthly_2020.map(m => m.arrivals < 5000 ? theme.statusNeg : theme.barBase),
          borderRadius: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { display: false }, ticks: { color: theme.textColor, font: { size: 10 } } },
          y: {
            grid: { color: theme.gridColor },
            ticks: { color: theme.textColor, callback: val => (val / 1000) + 'k', font: { family: 'JetBrains Mono', size: 10 } }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText,
            callbacks: { label: c => `Arrivals: ${formatNum(c.raw)}` }
          }
        }
      }
    });
  }

  // Chart 3: Source Market Shift (2019 vs 2020)
  destroyChart('tourMarketShiftChart');
  const ctxShift = document.getElementById('tourMarketShiftChart')?.getContext('2d');
  if (ctxShift) {
    const markets = tour.market_shifts.slice(0, 8);
    charts['tourMarketShiftChart'] = new Chart(ctxShift, {
      type: 'bar',
      data: {
        labels: markets.map(m => m.country),
        datasets: [
          {
            label: '2019 Arrivals',
            data: markets.map(m => m['2019']),
            backgroundColor: theme.barBase,
            borderRadius: 3
          },
          {
            label: '2020 Arrivals',
            data: markets.map(m => m['2020']),
            backgroundColor: theme.accent,
            borderRadius: 3
          }
        ]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: { color: theme.gridColor },
            ticks: { color: theme.textColor, callback: val => (val / 1000) + 'k', font: { family: 'JetBrains Mono', size: 10 } }
          },
          y: { grid: { display: false }, ticks: { color: theme.textColor, font: { size: 11 } } }
        },
        plugins: {
          legend: { labels: { color: theme.textColor, font: { family: 'Inter', size: 11 } } },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText
          }
        }
      }
    });
  }
}

// ==========================================================================
// 4. Macroeconomics & Real GDP Section
// ==========================================================================
function renderGdpSection(gdp) {
  if (!gdp) return;
  const theme = getChartTheme();

  // Chart 1: Real GDP Trend
  destroyChart('gdpTrendChart');
  const ctxGdp = document.getElementById('gdpTrendChart')?.getContext('2d');
  if (ctxGdp) {
    charts['gdpTrendChart'] = new Chart(ctxGdp, {
      type: 'line',
      data: {
        labels: gdp.series.map(s => s.year),
        datasets: [{
          label: 'Real GDP (Billion MVR)',
          data: gdp.series.map(s => s.real_gdp_mvr_m / 1000),
          borderColor: theme.accent,
          backgroundColor: theme.accentMuted,
          fill: true,
          tension: 0.15,
          borderWidth: 2,
          pointBackgroundColor: theme.accent,
          pointRadius: 2.5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { color: theme.gridColor }, ticks: { color: theme.textColor, font: { size: 10 } } },
          y: { grid: { color: theme.gridColor }, ticks: { color: theme.textColor, callback: v => v + 'B', font: { family: 'JetBrains Mono', size: 10 } } }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText,
            callbacks: { label: c => `Real GDP: ${c.raw.toFixed(1)}B MVR` }
          }
        }
      }
    });
  }

  // Chart 2: Sectoral Growth / Contraction in 2020
  destroyChart('gdpSectorChart');
  const ctxSec = document.getElementById('gdpSectorChart')?.getContext('2d');
  if (ctxSec) {
    const sec = gdp.sectoral_growth;
    charts['gdpSectorChart'] = new Chart(ctxSec, {
      type: 'bar',
      data: {
        labels: sec.map(s => s.sector),
        datasets: [{
          label: '2020 YoY Growth (%)',
          data: sec.map(s => s.growth_pct),
          backgroundColor: sec.map(s => s.growth_pct > 0 ? theme.statusPos : theme.statusNeg),
          borderRadius: 3
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { color: theme.gridColor }, ticks: { color: theme.textColor, callback: v => v + '%', font: { family: 'JetBrains Mono', size: 10 } } },
          y: { grid: { display: false }, ticks: { color: theme.textColor, font: { size: 11 } } }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText,
            callbacks: { label: c => `Growth: ${c.raw > 0 ? '+' : ''}${c.raw}%` }
          }
        }
      }
    });
  }

  // Chart 3: Global GDP Benchmark Comparison (2020)
  destroyChart('gdpBenchmarkChart');
  const ctxBench = document.getElementById('gdpBenchmarkChart')?.getContext('2d');
  if (ctxBench) {
    const bench = gdp.global_gdp_benchmarks;
    charts['gdpBenchmarkChart'] = new Chart(ctxBench, {
      type: 'bar',
      data: {
        labels: bench.map(b => b.country),
        datasets: [{
          label: '2020 Real GDP Growth (%)',
          data: bench.map(b => b.growth_2020),
          backgroundColor: bench.map(b => b.highlight ? theme.statusNeg : theme.barBase),
          borderRadius: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { display: false }, ticks: { color: theme.textColor, font: { size: 10 } } },
          y: { grid: { color: theme.gridColor }, ticks: { color: theme.textColor, callback: v => v + '%', font: { family: 'JetBrains Mono', size: 10 } } }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText,
            callbacks: { label: c => `Growth: ${c.raw}%` }
          }
        }
      }
    });
  }
}

// ==========================================================================
// 5. Fisheries & Blue Economy Section
// ==========================================================================
function renderFisheriesSection(fish) {
  if (!fish) return;
  const theme = getChartTheme();

  // Chart 1: Catch by Species
  destroyChart('fishCatchChart');
  const ctxCatch = document.getElementById('fishCatchChart')?.getContext('2d');
  if (ctxCatch) {
    charts['fishCatchChart'] = new Chart(ctxCatch, {
      type: 'bar',
      data: {
        labels: fish.catch.map(c => c.year),
        datasets: [
          {
            label: 'Skipjack Tuna (MT)',
            data: fish.catch.map(c => c.skipjack_mt),
            backgroundColor: theme.accent,
            borderRadius: 2
          },
          {
            label: 'Yellowfin Tuna (MT)',
            data: fish.catch.map(c => c.yellowfin_mt),
            backgroundColor: theme.barHover,
            borderRadius: 2
          },
          {
            label: 'Other Species (MT)',
            data: fish.catch.map(c => c.other_mt),
            backgroundColor: theme.barBase,
            borderRadius: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { stacked: true, grid: { display: false }, ticks: { color: theme.textColor, font: { size: 10 } } },
          y: {
            stacked: true,
            grid: { color: theme.gridColor },
            ticks: { color: theme.textColor, callback: v => (v / 1000) + 'k MT', font: { family: 'JetBrains Mono', size: 10 } }
          }
        },
        plugins: {
          legend: { labels: { color: theme.textColor, font: { family: 'Inter', size: 11 } } },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText
          }
        }
      }
    });
  }

  // Chart 2: Global Fish Consumption per Capita
  destroyChart('fishBenchmarkChart');
  const ctxBench = document.getElementById('fishBenchmarkChart')?.getContext('2d');
  if (ctxBench) {
    const bench = fish.global_consumption_benchmarks;
    charts['fishBenchmarkChart'] = new Chart(ctxBench, {
      type: 'bar',
      data: {
        labels: bench.map(b => b.country),
        datasets: [{
          label: 'Consumption (kg/yr)',
          data: bench.map(b => b.consumption_kg_per_capita),
          backgroundColor: bench.map(b => b.highlight ? theme.statusPos : theme.barBase),
          borderRadius: 3
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { color: theme.gridColor }, ticks: { color: theme.textColor, font: { family: 'JetBrains Mono', size: 10 } } },
          y: { grid: { display: false }, ticks: { color: theme.textColor, font: { size: 11 } } }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText,
            callbacks: { label: c => `${c.raw} kg / person / yr` }
          }
        }
      }
    });
  }
}

// ==========================================================================
// 6. Public Finance Section
// ==========================================================================
function renderPublicFinanceSection(pf) {
  if (!pf) return;
  const theme = getChartTheme();

  destroyChart('pfBalanceChart');
  const ctxPf = document.getElementById('pfBalanceChart')?.getContext('2d');
  if (ctxPf) {
    charts['pfBalanceChart'] = new Chart(ctxPf, {
      type: 'bar',
      data: {
        labels: pf.series.map(s => s.year),
        datasets: [
          {
            type: 'line',
            label: 'Revenue & Grants',
            data: pf.series.map(s => s.revenue_mvr_m / 1000),
            borderColor: theme.accent,
            borderWidth: 2,
            pointBackgroundColor: theme.accent,
            pointRadius: 2.5
          },
          {
            type: 'line',
            label: 'Total Expenditure',
            data: pf.series.map(s => s.expenditure_mvr_m / 1000),
            borderColor: theme.statusNeg,
            borderWidth: 2,
            pointBackgroundColor: theme.statusNeg,
            pointRadius: 2.5
          },
          {
            type: 'bar',
            label: 'Overall Deficit (Billion MVR)',
            data: pf.series.map(s => s.deficit_mvr_m / 1000),
            backgroundColor: theme.barBase,
            borderRadius: 3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { color: theme.gridColor }, ticks: { color: theme.textColor, font: { size: 10 } } },
          y: { grid: { color: theme.gridColor }, ticks: { color: theme.textColor, callback: v => v + 'B', font: { family: 'JetBrains Mono', size: 10 } } }
        },
        plugins: {
          legend: { labels: { color: theme.textColor, font: { family: 'Inter', size: 11 } } },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText
          }
        }
      }
    });
  }

  // Tourism Budget Share
  destroyChart('pfTourismShareChart');
  const ctxTourShare = document.getElementById('pfTourismShareChart')?.getContext('2d');
  if (ctxTourShare) {
    charts['pfTourismShareChart'] = new Chart(ctxTourShare, {
      type: 'line',
      data: {
        labels: pf.tourism_share.map(t => t.year),
        datasets: [{
          label: '% Share in Revenue',
          data: pf.tourism_share.map(t => t.share_pct),
          borderColor: theme.accent,
          backgroundColor: theme.accentMuted,
          fill: true,
          tension: 0.2,
          borderWidth: 2,
          pointBackgroundColor: theme.accent,
          pointRadius: 2.5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { color: theme.gridColor }, ticks: { color: theme.textColor, font: { size: 10 } } },
          y: { grid: { color: theme.gridColor }, ticks: { color: theme.textColor, callback: v => v + '%', font: { family: 'JetBrains Mono', size: 10 } }, min: 15, max: 40 }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText,
            callbacks: { label: c => `Share: ${c.raw}%` }
          }
        }
      }
    });
  }
}

// ==========================================================================
// 7. Climate & Freshwater Infrastructure Section
// ==========================================================================
function renderWaterSection(water) {
  if (!water) return;
  const theme = getChartTheme();

  destroyChart('waterEmergencyChart');
  const ctxW = document.getElementById('waterEmergencyChart')?.getContext('2d');
  if (ctxW) {
    charts['waterEmergencyChart'] = new Chart(ctxW, {
      type: 'bar',
      data: {
        labels: water.emergency_series.map(w => w.year),
        datasets: [
          {
            type: 'bar',
            label: 'Islands Supplied',
            data: water.emergency_series.map(w => w.islands_supplied),
            backgroundColor: theme.barBase,
            borderRadius: 3,
            yAxisID: 'y'
          },
          {
            type: 'line',
            label: 'Cost per Ton (MVR)',
            data: water.emergency_series.map(w => w.cost_per_ton_mvr),
            borderColor: theme.accent,
            backgroundColor: 'transparent',
            borderWidth: 2,
            pointBackgroundColor: theme.accent,
            pointRadius: 2.5,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { color: theme.gridColor }, ticks: { color: theme.textColor, font: { size: 10 } } },
          y: {
            type: 'linear',
            position: 'left',
            grid: { color: theme.gridColor },
            ticks: { color: theme.textColor, font: { family: 'JetBrains Mono', size: 10 } }
          },
          y1: {
            type: 'linear',
            position: 'right',
            grid: { display: false },
            ticks: { color: theme.textColor, callback: v => v + ' MVR', font: { family: 'JetBrains Mono', size: 10 } }
          }
        },
        plugins: {
          legend: { labels: { color: theme.textColor, font: { family: 'Inter', size: 11 } } },
          tooltip: {
            backgroundColor: theme.tooltipBg,
            borderColor: theme.tooltipBorder,
            borderWidth: 1,
            titleColor: theme.tooltipText,
            bodyColor: theme.tooltipText
          }
        }
      }
    });
  }
}

// ==========================================================================
// 8. Master Catalog Explorer (309 Tables)
// ==========================================================================
function renderCatalogExplorer(catalog) {
  if (!catalog) return;
  
  const searchInput = document.getElementById('catalog-search-input');
  const chapterSelect = document.getElementById('catalog-chapter-select');
  const tableBody = document.getElementById('catalog-table-body');
  const countBadge = document.getElementById('catalog-count-badge');

  const chapters = Array.from(new Set(catalog.map(c => c.chapter))).sort((a, b) => {
    return parseFloat(a.split(' ')[0]) - parseFloat(b.split(' ')[0]);
  });
  
  if (chapterSelect) {
    chapterSelect.innerHTML = '<option value="">All 20 Chapters</option>';
    chapters.forEach(ch => {
      const opt = document.createElement('option');
      opt.value = ch;
      opt.textContent = ch;
      chapterSelect.appendChild(opt);
    });
  }

  function filterCatalog() {
    const q = searchInput?.value.toLowerCase().trim() || '';
    const selectedCh = chapterSelect?.value || '';

    const filtered = catalog.filter(item => {
      const matchQ = !q || item.title.toLowerCase().includes(q) || item.id.toLowerCase().includes(q) || item.chapter.toLowerCase().includes(q);
      const matchCh = !selectedCh || item.chapter === selectedCh;
      return matchQ && matchCh;
    });

    if (countBadge) countBadge.textContent = `${filtered.length} tables`;

    if (tableBody) {
      tableBody.innerHTML = '';
      filtered.slice(0, 100).forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><code class="font-mono">${item.id}</code></td>
          <td><span class="badge-pill">${item.chapter}</span></td>
          <td><strong>${item.title}</strong></td>
          <td class="num font-mono">${formatNum(item.rows)}</td>
          <td class="num font-mono">${formatNum(item.cols)}</td>
          <td><a href="datasets/${item.file}" target="_blank" class="btn-ghost" style="height: 26px; padding-inline: 0.5rem; font-size: 0.75rem;">View CSV</a></td>
        `;
        tableBody.appendChild(tr);
      });
    }
  }

  searchInput?.addEventListener('input', filterCatalog);
  chapterSelect?.addEventListener('change', filterCatalog);
  filterCatalog();
}
