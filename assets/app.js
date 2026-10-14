/**
 * app.js
 * Master Client-Side Engine for the Maldives Economic & Island Monitor
 * Manages 360-degree timeline scrubber, Chart.js instances, tabs, catalog search,
 * and the 2004 Tsunami Crisis Focus simulation scrubber.
 */

(function () {
  'use strict';

  // State Management
  const state = {
    data: null,
    activeTab: 'pane-360',
    selectedYear: 2024,
    isPlaying: false,
    playInterval: null,
    tsunamiPhaseIndex: 1, // Default Phase 1: Dec 26, 2004 Wave Strike & State of Emergency
    isTsunamiPlaying: false,
    tsunamiPlayInterval: null,
    covidMonthIndex: 15,
    isCovidPlaying: false,
    covidPlayInterval: null,
    catalogQuery: '',
    catalogCategory: 'all',
    catalogPage: 1,
    catalogPageSize: 20,
    selectedShockEventId: 'tsunami_2004',
    charts: {}
  };

  // DOM Elements Cache
  const els = {
    themeBtn: document.getElementById('theme-toggle-btn'),
    themeIcon: document.getElementById('theme-icon-svg'),
    subnavScroll: document.getElementById('subnav-scroll'),
    subnavPrevBtn: document.getElementById('subnav-scroll-prev'),
    subnavNextBtn: document.getElementById('subnav-scroll-next'),
    tabButtons: document.querySelectorAll('.tab-btn'),
    tabPanes: document.querySelectorAll('.tab-pane'),
    slider: document.getElementById('timeline-slider'),
    yearDisplay: document.getElementById('scrubber-year-display'),
    playBtn: document.getElementById('scrubber-play-btn'),
    playText: document.getElementById('play-text'),
    playIcon: document.getElementById('play-icon'),
    jumpPills: document.querySelectorAll('.jump-pill[data-year]'),
    catalogBtn: document.getElementById('quick-catalog-btn'),
    catalogInput: document.getElementById('catalog-search-input'),
    clearSearchBtn: document.getElementById('clear-search-btn'),
    filterPills: document.querySelectorAll('.filter-pill'),
    catalogTableBody: document.getElementById('catalog-table-body'),
    catalogVisibleCount: document.getElementById('catalog-visible-count'),
    pagePrevBtn: document.getElementById('page-prev-btn'),
    pageNextBtn: document.getElementById('page-next-btn'),
    pageIndicator: document.getElementById('page-indicator'),

    // Tsunami Crisis Interactive Scrubber Elements
    tsunamiPhaseSlider: document.getElementById('tsunami-phase-slider'),
    tsunamiPlayBtn: document.getElementById('tsunami-play-btn'),
    tsunamiPlayText: document.getElementById('tsunami-play-text'),
    tsunamiPlayIcon: document.getElementById('tsunami-play-icon'),
    tsunamiTickerPhaseName: document.getElementById('tsunami-ticker-phase-name'),
    tsunamiTickerVisitors: document.getElementById('tsunami-ticker-visitors'),
    tsunamiTickerStatus: document.getElementById('tsunami-ticker-status'),
    tsunamiTickerNote: document.getElementById('tsunami-ticker-note'),
    tsunamiJumpPills: document.querySelectorAll('[data-tsunami-phase]'),
    tsunamiPhaseTag: document.getElementById('tsunami-kpi-phase-tag'),

    // COVID Interactive Scrubber Elements (Backward-compatibility)
    covidMonthSlider: document.getElementById('covid-month-slider'),
    covidPlayBtn: document.getElementById('covid-play-btn'),
    covidPlayText: document.getElementById('covid-play-text'),
    covidPlayIcon: document.getElementById('covid-play-icon'),
    covidTickerMonth: document.getElementById('covid-ticker-month'),
    covidTickerVisitors: document.getElementById('covid-ticker-visitors'),
    covidTickerPhase: document.getElementById('covid-ticker-phase'),
    covidTickerNote: document.getElementById('covid-ticker-note'),
    covidJumpPills: document.querySelectorAll('[data-covid-month]'),
    covidPhaseTag: document.getElementById('covid-kpi-phase-tag')
  };

  // Helper: Format Numbers with commas
  function formatNum(num) {
    if (num === null || num === undefined || isNaN(num)) return '—';
    return Number(num).toLocaleString('en-US');
  }

  // Helper: Detect Current Theme
  function isDarkTheme() {
    return document.documentElement.getAttribute('data-theme') === 'dark';
  }

  // Theme Colors for Chart.js
  function getChartColors() {
    const dark = isDarkTheme();
    return {
      text: dark ? '#94a3b8' : '#475569',
      grid: dark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(0, 0, 0, 0.06)',
      accent: '#0ea5e9',
      accentMuted: 'rgba(14, 165, 233, 0.15)',
      emerald: '#10b981',
      rose: '#f43f5e',
      amber: '#f59e0b',
      indigo: '#6366f1'
    };
  }

  // =========================================================================
  // 1. DATA INITIALIZATION
  // =========================================================================
  async function init() {
    try {
      if (window.MALDIVES_MASTER_DATA) {
        state.data = window.MALDIVES_MASTER_DATA;
      } else {
        const res = await fetch('assets/dashboard_data_unified.json');
        state.data = await res.json();
      }
      
      setupThemeToggle();
      setupTabs();
      setupTimelineScrubber();
      setupTsunamiScrubber();
      setupCovidScrubber();
      setupCatalog();
      setupPillarJumps();
      setupShocksShowcase();
      
      // Update initial KPI values
      updateYearKPIs(state.selectedYear);
      setTsunamiPhase(state.tsunamiPhaseIndex);
      setCovidMonth(state.covidMonthIndex);
      
      // Initialize charts for active tab
      renderChartsForTab('pane-360');
      
    } catch (err) {
      console.error('Failed to load observatory dataset:', err);
    }
  }

  // =========================================================================
  // 2. THEME TOGGLE
  // =========================================================================
  function setupThemeToggle() {
    if (!els.themeBtn) return;
    
    els.themeBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const target = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', target);
      localStorage.setItem('site-theme', target);
      
      // Rebuild charts with theme colors
      Object.values(state.charts).forEach(c => {
        if (c && typeof c.destroy === 'function') c.destroy();
      });
      state.charts = {};
      if (typeof pyramidState !== 'undefined' && pyramidState.chart) {
        pyramidState.chart.destroy();
        pyramidState.chart = null;
      }
      if (typeof expatLaborState !== 'undefined' && expatLaborState.chart) {
        expatLaborState.chart.destroy();
        expatLaborState.chart = null;
      }
      renderChartsForTab(state.activeTab);
    });
  }

  // =========================================================================
  // 3. TABS NAVIGATION & RESPONSIVE SCROLLING
  // =========================================================================
  function setupTabs() {
    els.tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-target');
        switchTab(targetId);
      });
    });

    // Subnav Horizontal Scroll Arrows
    const scrollContainer = els.subnavScroll || document.getElementById('subnav-scroll');
    const prevBtn = els.subnavPrevBtn || document.getElementById('subnav-scroll-prev');
    const nextBtn = els.subnavNextBtn || document.getElementById('subnav-scroll-next');

    if (scrollContainer && prevBtn && nextBtn) {
      const updateArrows = () => {
        const sl = scrollContainer.scrollLeft;
        const maxScroll = scrollContainer.scrollWidth - scrollContainer.clientWidth;
        const hasOverflow = maxScroll > 5;
        prevBtn.style.display = hasOverflow && sl > 10 ? 'flex' : 'none';
        nextBtn.style.display = hasOverflow && sl < maxScroll - 10 ? 'flex' : 'none';
      };

      scrollContainer.addEventListener('scroll', updateArrows, { passive: true });
      window.addEventListener('resize', updateArrows);
      prevBtn.addEventListener('click', () => {
        scrollContainer.scrollBy({ left: -260, behavior: 'smooth' });
      });
      nextBtn.addEventListener('click', () => {
        scrollContainer.scrollBy({ left: 260, behavior: 'smooth' });
      });
      setTimeout(updateArrows, 150);
    }

    if (els.catalogBtn) {
      els.catalogBtn.addEventListener('click', () => {
        switchTab('pane-catalog');
        if (els.catalogInput) {
          els.catalogInput.focus();
          els.catalogInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      });
    }
  }

  function switchTab(targetId) {
    if (!targetId || state.activeTab === targetId) return;
    state.activeTab = targetId;

    let targetBtn = null;
    els.tabButtons.forEach(btn => {
      const isTarget = btn.getAttribute('data-target') === targetId;
      btn.classList.toggle('active', isTarget);
      btn.setAttribute('aria-selected', isTarget ? 'true' : 'false');
      if (isTarget) targetBtn = btn;
    });

    els.tabPanes.forEach(pane => {
      pane.classList.toggle('active', pane.id === targetId);
    });

    // Center active tab smoothly inside subnav scroll frame
    if (targetBtn && els.subnavScroll) {
      targetBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }

    // Re-synchronize active year, Tsunami phase and COVID month when switching tabs
    updateYearKPIs(state.selectedYear);
    if (targetId === 'pane-tsunami') {
      setTsunamiPhase(state.tsunamiPhaseIndex);
    } else if (targetId === 'pane-covid') {
      setCovidMonth(state.covidMonthIndex);
    }

    // Render charts for this tab
    setTimeout(() => {
      renderChartsForTab(targetId);
    }, 50);
  }

  function setupPillarJumps() {
    document.querySelectorAll('[data-jump-tab]').forEach(el => {
      el.addEventListener('click', () => {
        const tab = el.getAttribute('data-jump-tab');
        if (tab) {
          switchTab(tab);
          window.scrollTo({ top: 120, behavior: 'smooth' });
        }
      });
    });
  }

  // =========================================================================
  // 4. MASTER TIMELINE SCRUBBER (2000 - 2026)
  // =========================================================================
  function setupTimelineScrubber() {
    if (!els.slider) return;

    els.slider.addEventListener('input', (e) => {
      const yr = parseInt(e.target.value, 10);
      setScrubberYear(yr);
    });

    els.jumpPills.forEach(pill => {
      pill.addEventListener('click', () => {
        const yr = parseInt(pill.getAttribute('data-year'), 10);
        if (yr) {
          els.slider.value = yr;
          setScrubberYear(yr);
        }
      });
    });

    if (els.playBtn) {
      els.playBtn.addEventListener('click', togglePlay);
    }
  }

  function setScrubberYear(yr) {
    state.selectedYear = yr;
    if (els.yearDisplay) els.yearDisplay.textContent = yr;

    // Update Jump Pill Active State
    els.jumpPills.forEach(p => {
      const pillYear = parseInt(p.getAttribute('data-year'), 10);
      p.classList.toggle('active', pillYear === yr);
    });

    // Update 360 KPIs & COVID KPIs simultaneously
    updateYearKPIs(yr);
  }

  function togglePlay() {
    if (state.isPlaying) {
      stopPlay();
    } else {
      startPlay();
    }
  }

  function startPlay() {
    state.isPlaying = true;
    if (els.playText) els.playText.textContent = 'Pause';
    if (els.playIcon) {
      els.playIcon.innerHTML = '<rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect>';
    }

    state.playInterval = setInterval(() => {
      let nextYr = state.selectedYear + 1;
      if (nextYr > 2026) nextYr = 2000;
      els.slider.value = nextYr;
      setScrubberYear(nextYr);
    }, 850);
  }

  function stopPlay() {
    state.isPlaying = false;
    if (state.playInterval) clearInterval(state.playInterval);
    state.playInterval = null;
    if (els.playText) els.playText.textContent = 'Auto Play';
    if (els.playIcon) {
      els.playIcon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"></polygon>';
    }
  }

  // =========================================================================
  // 5. 2004 TSUNAMI CRISIS PHASE SCRUBBER & SIMULATION
  // =========================================================================
  function setupTsunamiScrubber() {
    if (!els.tsunamiPhaseSlider) return;

    els.tsunamiPhaseSlider.addEventListener('input', (e) => {
      const idx = parseInt(e.target.value, 10);
      setTsunamiPhase(idx);
    });

    els.tsunamiJumpPills.forEach(pill => {
      pill.addEventListener('click', () => {
        const p = parseInt(pill.getAttribute('data-tsunami-phase'), 10);
        if (!isNaN(p)) {
          if (els.tsunamiPhaseSlider) els.tsunamiPhaseSlider.value = p;
          setTsunamiPhase(p);
        }
      });
    });

    if (els.tsunamiPlayBtn) {
      els.tsunamiPlayBtn.addEventListener('click', toggleTsunamiPlay);
    }
  }

  function toggleTsunamiPlay() {
    if (state.isTsunamiPlaying) {
      stopTsunamiPlay();
    } else {
      startTsunamiPlay();
    }
  }

  function startTsunamiPlay() {
    state.isTsunamiPlaying = true;
    if (els.tsunamiPlayText) els.tsunamiPlayText.textContent = 'Pause Simulation';
    if (els.tsunamiPlayIcon) {
      els.tsunamiPlayIcon.innerHTML = '<rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect>';
    }

    state.tsunamiPlayInterval = setInterval(() => {
      let nextP = state.tsunamiPhaseIndex + 1;
      if (nextP > 5) nextP = 0;
      if (els.tsunamiPhaseSlider) els.tsunamiPhaseSlider.value = nextP;
      setTsunamiPhase(nextP);
    }, 1800);
  }

  function stopTsunamiPlay() {
    state.isTsunamiPlaying = false;
    if (state.tsunamiPlayInterval) clearInterval(state.tsunamiPlayInterval);
    state.tsunamiPlayInterval = null;
    if (els.tsunamiPlayText) els.tsunamiPlayText.textContent = 'Play Tsunami Simulation';
    if (els.tsunamiPlayIcon) {
      els.tsunamiPlayIcon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"></polygon>';
    }
  }

  function setTsunamiPhase(index) {
    if (!state.data || !state.data.tsunami_shock || !state.data.tsunami_shock.phases) return;
    const phases = state.data.tsunami_shock.phases;
    if (index < 0 || index >= phases.length) return;

    state.tsunamiPhaseIndex = index;
    const phase = phases[index];

    // Highlight active jump pill
    els.tsunamiJumpPills.forEach(p => {
      const idx = parseInt(p.getAttribute('data-tsunami-phase'), 10);
      p.classList.toggle('active', idx === index);
    });

    // Update Slider
    if (els.tsunamiPhaseSlider) {
      els.tsunamiPhaseSlider.value = index;
    }

    // Update Header Tag
    if (els.tsunamiPhaseTag) {
      els.tsunamiPhaseTag.textContent = `[Active Phase: ${phase.phase_name}]`;
    }

    // Update Live Ticker
    if (els.tsunamiTickerPhaseName) {
      els.tsunamiTickerPhaseName.textContent = phase.phase_name;
    }
    if (els.tsunamiTickerVisitors) {
      const isCollapse = phase.year === 2005;
      els.tsunamiTickerVisitors.textContent = `${formatNum(phase.tourists)} Tourists`;
      els.tsunamiTickerVisitors.style.color = isCollapse ? 'var(--rose)' : 'var(--accent)';
    }
    if (els.tsunamiTickerStatus) {
      if (phase.index === 0) {
        els.tsunamiTickerStatus.textContent = 'Normal Coastal Operations • 87 Resorts';
        els.tsunamiTickerStatus.className = 'ticker-badge font-mono text-accent';
      } else if (phase.index === 1 || phase.index === 2) {
        els.tsunamiTickerStatus.textContent = '187 Islands Flooded • 14 Evacuated';
        els.tsunamiTickerStatus.className = 'ticker-badge font-mono text-rose';
      } else if (phase.index === 3) {
        els.tsunamiTickerStatus.textContent = 'Reconstruction Surge • 85 Resorts Re-opened';
        els.tsunamiTickerStatus.className = 'ticker-badge font-mono text-positive';
      } else if (phase.index === 4) {
        els.tsunamiTickerStatus.textContent = 'R. Dhuvaafaru Inhabited • 4,000 Resettled';
        els.tsunamiTickerStatus.className = 'ticker-badge font-mono text-accent';
      } else {
        els.tsunamiTickerStatus.textContent = 'Safer Islands Standard • NDMA Protocols';
        els.tsunamiTickerStatus.className = 'ticker-badge font-mono text-positive';
      }
    }
    if (els.tsunamiTickerNote) {
      els.tsunamiTickerNote.textContent = phase.summary;
    }

    // Reactive KPI cards update
    const elGdp = document.getElementById('tsunami-val-gdp');
    const elDamage = document.getElementById('tsunami-val-damage');
    const elDisplaced = document.getElementById('tsunami-val-displaced');
    const elIslands = document.getElementById('tsunami-val-islands');
    const elTourists = document.getElementById('tsunami-val-tourists');
    const elRebuild = document.getElementById('tsunami-val-rebuild');

    if (elGdp) {
      const g = phase.gdp_growth;
      elGdp.textContent = `${g > 0 ? '+' : ''}${g}%`;
      elGdp.className = `kpi-value font-mono ${g < 0 ? 'negative' : 'positive'}`;
    }
    if (elDamage) {
      elDamage.innerHTML = phase.index === 0 ? '$0 <small>USD</small>' : '$470M <small>USD</small>';
    }
    if (elDisplaced) {
      elDisplaced.textContent = phase.displaced > 0 ? `${formatNum(phase.displaced)}+` : '0';
    }
    if (elIslands) {
      elIslands.innerHTML = phase.islands_inundated > 0 ? `${phase.islands_inundated} <small>/ 198</small>` : 'Normal';
    }
    if (elTourists) {
      elTourists.textContent = formatNum(phase.tourists);
      elTourists.className = `kpi-value font-mono ${phase.year === 2005 ? 'negative' : ''}`;
    }
    if (elRebuild) {
      elRebuild.innerHTML = phase.index === 0 ? 'Normal Budget' : '2.5B+ <small>MVR</small>';
    }

    // Update active highlight on Tsunami tourism chart
    updateTsunamiTourismChartMarker(phase.year);
  }

  function updateTsunamiTourismChartMarker(activeYear) {
    if (!state.charts.tsunamiTourism) return;
    state.charts.tsunamiTourism.update('none');
  }

  // =========================================================================
  // 5B. COVID-19 PANDEMIC MONTH-BY-MONTH SCRUBBER & SIMULATION
  // =========================================================================
  function setupCovidScrubber() {
    if (!els.covidMonthSlider) return;

    els.covidMonthSlider.addEventListener('input', (e) => {
      const idx = parseInt(e.target.value, 10);
      setCovidMonth(idx);
    });

    els.covidJumpPills.forEach(pill => {
      pill.addEventListener('click', () => {
        const m = parseInt(pill.getAttribute('data-covid-month'), 10);
        if (!isNaN(m)) {
          if (els.covidMonthSlider) els.covidMonthSlider.value = m;
          setCovidMonth(m);
        }
      });
    });

    if (els.covidPlayBtn) {
      els.covidPlayBtn.addEventListener('click', toggleCovidPlay);
    }
  }

  function toggleCovidPlay() {
    if (state.isCovidPlaying) {
      stopCovidPlay();
    } else {
      startCovidPlay();
    }
  }

  function startCovidPlay() {
    state.isCovidPlaying = true;
    if (els.covidPlayText) els.covidPlayText.textContent = 'Pause Simulation';
    if (els.covidPlayIcon) {
      els.covidPlayIcon.innerHTML = '<rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect>';
    }

    state.covidPlayInterval = setInterval(() => {
      let nextM = state.covidMonthIndex + 1;
      if (nextM > 47) nextM = 0;
      if (els.covidMonthSlider) els.covidMonthSlider.value = nextM;
      setCovidMonth(nextM);
    }, 280);
  }

  function stopCovidPlay() {
    state.isCovidPlaying = false;
    if (state.covidPlayInterval) clearInterval(state.covidPlayInterval);
    state.covidPlayInterval = null;
    if (els.covidPlayText) els.covidPlayText.textContent = 'Play COVID Simulation';
    if (els.covidPlayIcon) {
      els.covidPlayIcon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"></polygon>';
    }
  }

  function setCovidMonth(index) {
    if (!state.data || !state.data.covid_shock || !state.data.covid_shock.monthly_arrivals) return;
    const list = state.data.covid_shock.monthly_arrivals;
    if (index < 0 || index >= list.length) return;

    state.covidMonthIndex = index;
    const item = list[index];

    // Highlight active jump pill
    els.covidJumpPills.forEach(p => {
      const m = parseInt(p.getAttribute('data-covid-month'), 10);
      p.classList.toggle('active', m === index);
    });

    // Update Ticker Month & Visitors
    if (els.covidTickerMonth) {
      els.covidTickerMonth.textContent = `${item.month} ${item.year}`;
    }
    if (els.covidTickerVisitors) {
      els.covidTickerVisitors.textContent = `${formatNum(item.arrivals)} Tourists`;
      els.covidTickerVisitors.style.color = item.arrivals === 0 ? 'var(--rose)' : 'var(--accent)';
    }

    // Contextual Phase & Note Generator
    let phaseText = '';
    let noteText = '';
    let badgeClass = 'ticker-badge';

    if (item.year === 2019) {
      phaseText = 'Normal Pre-COVID Operating Conditions';
      noteText = `Normal tourism operations. China is the #1 market (${formatNum(item.arrivals)} monthly visitors from worldwide origins).`;
      badgeClass = 'ticker-badge text-accent';
    } else if (item.year === 2020 && (item.month === 'Jan' || item.month === 'Feb')) {
      phaseText = 'First Global Alarms';
      noteText = 'COVID-19 spreads globally. Flights from mainland China suspended; European demand remains temporarily strong.';
    } else if (item.year === 2020 && item.month === 'Mar') {
      phaseText = 'March 27: Complete Border Seal';
      noteText = 'Borders completely closed on March 27. On-arrival visas cancelled; resorts locked down; tourists evacuated.';
    } else if (item.year === 2020 && (item.month === 'Apr' || item.month === 'May' || item.month === 'Jun')) {
      phaseText = '100% Nationwide Border Closure (0 Arrivals)';
      noteText = '110-day total aviation shutdown. Zero international tourist arrivals. Local pole-and-line tuna fishing sustains island communities.';
      badgeClass = 'ticker-badge text-rose';
    } else if (item.year === 2020 && item.month === 'Jul') {
      phaseText = 'July 15 Historic Reopening';
      noteText = 'Maldives becomes one of the world\'s first nations to reopen without quarantine, leveraging natural resort island quarantine bubbles.';
    } else if (item.year === 2020 && (item.month === 'Aug' || item.month === 'Sep' || item.month === 'Oct')) {
      phaseText = 'Early Reopening Bubbles (Russia & UAE)';
      noteText = 'Aeroflot, Emirates, and Qatar Airways resume scheduled routes. Russia surges to become the #1 tourist origin country.';
    } else if (item.year === 2020 && (item.month === 'Nov' || item.month === 'Dec')) {
      phaseText = 'Winter Season Restart (Russia #1)';
      noteText = 'December arrivals cross 96k. High occupancy returns to private island resorts while European competitors remain under lockdowns.';
    } else if (item.year === 2021 && (item.month === 'Jan' || item.month === 'Feb' || item.month === 'Mar')) {
      phaseText = 'V-Shaped Recovery Accelerates (India Surge)';
      noteText = 'India becomes the fastest growing origin market, crossing 30k visitors per month. Air-travel bubbles facilitate direct connections.';
    } else if (item.year === 2021 && (item.month === 'Apr' || item.month === 'May')) {
      phaseText = 'South Asia Delta Wave Travel Pause';
      noteText = 'Temporary pause on South Asian tourist visas during the regional Delta wave; European traffic sustains baseline occupancy.';
    } else if (item.year === 2021 && (item.month === 'Jul' || item.month === 'Aug' || item.month === 'Sep')) {
      phaseText = 'Record Rebound: India & Russia Lead';
      noteText = 'Monthly arrivals surpass 140,000. Maldives leads global post-pandemic recovery with universal vaccine campaigns across resort staff.';
    } else if (item.year === 2021 && (item.month === 'Oct' || item.month === 'Nov' || item.month === 'Dec')) {
      phaseText = '1.32M Annual Milestone Surpassed';
      noteText = 'Annual total reaches 1,321,937 tourists (+138% YoY growth), smashing initial government recovery projections.';
    } else if (item.year === 2022) {
      phaseText = 'Full Normalization & European Return';
      noteText = 'UK, Germany, and Italy rebound strongly alongside India and Russia. Total annual visitors reach 1.68 million.';
    }

    if (els.covidTickerPhase) {
      els.covidTickerPhase.textContent = phaseText;
      els.covidTickerPhase.className = badgeClass;
    }
    if (els.covidTickerNote) {
      els.covidTickerNote.textContent = noteText;
    }

    // Update monthly chart active marker
    updateCovidMonthlyChartMarker(index);
  }

  function updateCovidMonthlyChartMarker(index) {
    if (!state.charts.covidMonthly) return;
    state.charts.covidMonthly.update('none');
  }

  // =========================================================================
  // 6. SYNCHRONIZED KPI UPDATES (360° + COVID)
  // =========================================================================
  function updateYearKPIs(year) {
    if (!state.data || !state.data.timeline) return;

    const row = state.data.timeline.find(r => r.year === year);
    if (!row) return;

    // --- 1. OVERVIEW 360° TAB KPIS ---
    const elTourists = document.getElementById('kpi-val-tourists');
    const elTouristsDelta = document.getElementById('kpi-delta-tourists');
    const elBeds = document.getElementById('kpi-beds-sub');
    if (elTourists) elTourists.textContent = formatNum(row.tourists);
    if (elBeds) elBeds.textContent = `${formatNum(Math.round((row.resort_beds || 0) + (row.guesthouse_beds || 0)))} beds`;
    if (elTouristsDelta) {
      const prev = state.data.timeline.find(r => r.year === year - 1);
      if (prev && prev.tourists) {
        const pct = (((row.tourists - prev.tourists) / prev.tourists) * 100).toFixed(1);
        elTouristsDelta.textContent = `${pct >= 0 ? '+' : ''}${pct}% YoY growth`;
        elTouristsDelta.className = `kpi-delta ${pct >= 0 ? 'positive' : 'negative'}`;
      } else {
        elTouristsDelta.textContent = 'Baseline year';
        elTouristsDelta.className = 'kpi-delta info';
      }
    }

    // GDP
    const elGdp = document.getElementById('kpi-val-gdp');
    const elGdpDelta = document.getElementById('kpi-delta-gdp');
    const elGdpGrowth = document.getElementById('kpi-gdp-growth');
    if (elGdp) elGdp.innerHTML = `$${(row.gdp_usd_m / 1000).toFixed(2)}B <small>USD</small>`;
    if (elGdpDelta) elGdpDelta.textContent = `Per Capita: $${formatNum(Math.round(row.gdp_per_capita_usd))} USD`;
    if (elGdpGrowth) {
      const g = row.gdp_growth_pct;
      elGdpGrowth.textContent = `${g >= 0 ? '+' : ''}${g.toFixed(1)}% YoY`;
      elGdpGrowth.className = g >= 0 ? 'text-positive' : 'text-negative';
    }

    // Population
    const elPop = document.getElementById('kpi-val-pop');
    const elPopDelta = document.getElementById('kpi-delta-pop');
    const elDensity = document.getElementById('kpi-density-sub');
    if (elPop) elPop.textContent = formatNum(Math.round(row.total_pop));
    if (elPopDelta && row.total_pop) {
      const malePct = ((row.male_pop / row.total_pop) * 100).toFixed(1);
      elPopDelta.textContent = `Malé: ${formatNum(Math.round(row.male_pop))} (${malePct}%)`;
    }
    if (elDensity) {
      const density = Math.round(row.male_pop / 3.0);
      elDensity.textContent = `${formatNum(density)} / km² in Malé`;
    }

    // Debt
    const elDebt = document.getElementById('kpi-val-debt');
    const elDebtDelta = document.getElementById('kpi-delta-debt');
    const elDeficit = document.getElementById('kpi-deficit-sub');
    if (elDebt) elDebt.textContent = `${row.debt_to_gdp_pct.toFixed(1)}%`;
    if (elDebtDelta) elDebtDelta.textContent = `${(row.public_debt_mvr / 1000).toFixed(1)}B MVR Total Debt`;
    if (elDeficit) {
      const def = (row.fiscal_deficit_mvr / 1000).toFixed(1);
      elDeficit.textContent = `${def}B MVR (${year})`;
    }

    // Fish Catch
    const elFish = document.getElementById('kpi-val-fish');
    if (elFish) elFish.innerHTML = `${formatNum(Math.round(row.fish_catch_mt))} <small>MT</small>`;

    // Electricity
    const elEnergy = document.getElementById('kpi-val-energy');
    const elEnergyDelta = document.getElementById('kpi-delta-energy');
    const elSolar = document.getElementById('kpi-solar-sub');
    if (elEnergy) elEnergy.innerHTML = `${formatNum(Math.round(row.electricity_gwh))} <small>GWh</small>`;
    if (elEnergyDelta) {
      const diesel = Math.round(row.electricity_gwh * 0.42);
      elEnergyDelta.textContent = `~${diesel}M Liters Diesel Used`;
    }
    if (elSolar) {
      const solarEst = Math.min(85, Math.max(1.2, (year - 2010) * 5.8));
      elSolar.textContent = `${solarEst > 1 ? solarEst.toFixed(0) : '1.2'} MW Installed`;
    }

    // --- 2. COVID-19 SHOCK TAB DYNAMIC KPIS ---
    updateCovidKPIs(year, row);

    // --- 3. GREATER MALÉ AREA TAB KPIS & BANNER ---
    updateGreaterMaleKPIs(year, row);

    // --- 4. DEMOGRAPHICS TAB BANNER & REACTION ---
    updateDemographicsBanner(year, row);

    // --- 5. ECONOMY TAB BANNER ---
    updateEconomyBanner(year, row);

    // --- 6. TOURISM TAB BANNER ---
    updateTourismBanner(year, row);

    // --- 7. LIFELINES TAB BANNER ---
    updateLifelinesBanner(year, row);

    // --- 8. SOCIETY TAB BANNER ---
    updateSocietyBanner(year, row);
  }

  function updateCovidKPIs(year, row) {
    const elPhaseTag = document.getElementById('covid-kpi-phase-tag');
    const elCovidGdp = document.getElementById('covid-val-gdp');
    const elCovidGdpDelta = document.getElementById('covid-delta-gdp');
    const elCovidGdpFooter = document.getElementById('covid-footer-gdp');

    const elCovidTourists = document.getElementById('covid-val-tourists');
    const elCovidTouristsDelta = document.getElementById('covid-delta-tourists');
    const elCovidTouristsFooter = document.getElementById('covid-footer-tourists');

    const elCovidMarket = document.getElementById('covid-val-market');
    const elCovidMarketDelta = document.getElementById('covid-delta-market');
    const elCovidMarketFooter = document.getElementById('covid-footer-market');

    const elCovidBorders = document.getElementById('covid-val-borders');
    const elCovidBordersDelta = document.getElementById('covid-delta-borders');

    const elCovidFish = document.getElementById('covid-val-fish');
    const elCovidFishDelta = document.getElementById('covid-delta-fish');

    const elCovidDebt = document.getElementById('covid-val-debt');
    const elCovidDebtDelta = document.getElementById('covid-delta-debt');

    // Contextual Phase Tag
    if (elPhaseTag) {
      if (year < 2019) {
        elPhaseTag.textContent = `[Year ${year}: Pre-Pandemic Baseline Era]`;
        elPhaseTag.className = 'font-mono text-accent';
      } else if (year === 2019) {
        elPhaseTag.textContent = '[Year 2019: Pre-COVID Peak: 1.70M Visitors]';
        elPhaseTag.className = 'font-mono text-accent';
      } else if (year === 2020) {
        elPhaseTag.textContent = '[Year 2020: Complete Border Lockdown & -33.5% GDP Crash]';
        elPhaseTag.className = 'font-mono text-rose';
      } else if (year === 2021) {
        elPhaseTag.textContent = '[Year 2021: World-Leading V-Shaped Rebound: +41.7% GDP]';
        elPhaseTag.className = 'font-mono text-positive';
      } else if (year === 2022) {
        elPhaseTag.textContent = '[Year 2022: Post-Pandemic Normalization: 1.68M Visitors]';
        elPhaseTag.className = 'font-mono text-positive';
      } else {
        elPhaseTag.textContent = `[Year ${year}: All-Time Historical Peak: 2.05M+ Visitors]`;
        elPhaseTag.className = 'font-mono text-positive';
      }
    }

    // Real GDP Impact
    if (elCovidGdp) {
      const g = row.gdp_growth_pct;
      elCovidGdp.textContent = `${g >= 0 ? '+' : ''}${g.toFixed(1)}%`;
      elCovidGdp.className = `kpi-value font-mono ${g >= 0 ? 'positive' : 'negative'}`;
    }
    if (elCovidGdpDelta) {
      if (year === 2020) elCovidGdpDelta.textContent = 'Historic economic contraction';
      else if (year === 2021) elCovidGdpDelta.textContent = 'World-leading rebound';
      else elCovidGdpDelta.textContent = `Real GDP expansion for ${year}`;
      elCovidGdpDelta.className = `kpi-delta ${row.gdp_growth_pct >= 0 ? 'positive' : 'negative'}`;
    }
    if (elCovidGdpFooter) {
      elCovidGdpFooter.textContent = `GDP: $${(row.gdp_usd_m / 1000).toFixed(2)}B USD output`;
    }

    // Annual Visitors
    if (elCovidTourists) {
      elCovidTourists.textContent = formatNum(row.tourists);
      elCovidTourists.className = `kpi-value font-mono ${year === 2020 ? 'negative' : 'positive'}`;
    }
    if (elCovidTouristsDelta) {
      if (year === 2020) elCovidTouristsDelta.textContent = '-67.4% from 1.70M peak';
      else if (year === 2021) elCovidTouristsDelta.textContent = '+138.0% YoY rebound surge';
      else if (year === 2024) elCovidTouristsDelta.textContent = '+20.2% above 2019 baseline';
      else elCovidTouristsDelta.textContent = `Annual arrivals for ${year}`;
    }
    if (elCovidTouristsFooter) {
      if (year === 2020) elCovidTouristsFooter.textContent = 'Apr–Jun: 0 arrivals';
      else elCovidTouristsFooter.textContent = `Capacity: ${formatNum(Math.round((row.resort_beds || 0) + (row.guesthouse_beds || 0)))} beds`;
    }

    // Origin Market
    if (elCovidMarket) {
      if (year === 2019) elCovidMarket.textContent = 'China (284k)';
      else if (year === 2020) elCovidMarket.textContent = 'Russia (61k)';
      else if (year === 2021) elCovidMarket.textContent = 'India (292k)';
      else if (year === 2022) elCovidMarket.textContent = 'India (241k)';
      else if (year === 2023) elCovidMarket.textContent = 'India / Russia (209k)';
      else if (year >= 2024) elCovidMarket.textContent = 'China (263k)';
      else elCovidMarket.textContent = 'United Kingdom / Italy';
    }
    if (elCovidMarketDelta) {
      if (year === 2020) elCovidMarketDelta.textContent = 'China dropped: 284k → 34k';
      else if (year === 2021) elCovidMarketDelta.textContent = 'Russia #2 (222k), UK #3';
      else if (year >= 2024) elCovidMarketDelta.textContent = 'India #2 (209k), Russia #3';
      else elCovidMarketDelta.textContent = 'Market source alignment';
    }

    // Border Status
    if (elCovidBorders) {
      if (year <= 2019) elCovidBorders.textContent = 'Open Worldwide';
      else if (year === 2020) elCovidBorders.textContent = 'Closed → Bubble';
      else if (year === 2021) elCovidBorders.textContent = 'Resort Bubble';
      else elCovidBorders.textContent = 'Fully Open';
    }
    if (elCovidBordersDelta) {
      if (year === 2020) elCovidBordersDelta.textContent = 'Reopened 15 July 2020';
      else if (year === 2021) elCovidBordersDelta.textContent = 'Quarantine-free bubbles';
      else elCovidBordersDelta.textContent = 'No travel restrictions';
    }

    // Fish Buffer
    if (elCovidFish) {
      elCovidFish.innerHTML = `${formatNum(Math.round(row.fish_catch_mt))} <small>MT</small>`;
    }
    if (elCovidFishDelta) {
      if (year === 2020) elCovidFishDelta.textContent = '+10.2% YoY during lockdown';
      else elCovidFishDelta.textContent = 'Pole & line harvest';
    }

    // Debt
    if (elCovidDebt) {
      elCovidDebt.textContent = `${row.debt_to_gdp_pct.toFixed(1)}%`;
      elCovidDebt.className = `kpi-value font-mono ${row.debt_to_gdp_pct > 100 ? 'negative' : ''}`;
    }
    if (elCovidDebtDelta) {
      if (year === 2020) elCovidDebtDelta.textContent = '+72.6 percentage pts spike';
      else elCovidDebtDelta.textContent = `${(row.public_debt_mvr / 1000).toFixed(1)}B MVR Total Debt`;
    }

    // Also auto-sync month scrubber slider when user is on COVID tab!
    if (state.activeTab === 'pane-covid' && !state.isCovidPlaying) {
      if (year === 2019 && state.covidMonthIndex > 11) {
        if (els.covidMonthSlider) els.covidMonthSlider.value = 6;
        setCovidMonth(6);
      } else if (year === 2020 && (state.covidMonthIndex < 12 || state.covidMonthIndex > 23)) {
        if (els.covidMonthSlider) els.covidMonthSlider.value = 15;
        setCovidMonth(15);
      } else if (year === 2021 && (state.covidMonthIndex < 24 || state.covidMonthIndex > 35)) {
        if (els.covidMonthSlider) els.covidMonthSlider.value = 31;
        setCovidMonth(31);
      } else if (year === 2022 && state.covidMonthIndex < 36) {
        if (els.covidMonthSlider) els.covidMonthSlider.value = 42;
        setCovidMonth(42);
      }
    }

    // Auto-sync Shocks Ribbon and Intel Card if this year matches a historical milestone
    const matchedEvent = HISTORICAL_SHOCKS_EVENTS.find(e => e.year === year);
    if (matchedEvent) {
      document.querySelectorAll('.shocks-event-pill').forEach(p => {
        p.classList.toggle('active', p.getAttribute('data-event-id') === matchedEvent.id);
      });
      updateShocksIntelCard(matchedEvent);
    }
    if (state.charts.gdpGrowth) {
      state.charts.gdpGrowth.update('none');
    }
  }

  // --- 3. GREATER MALÉ KPIS & BANNER ---
  function updateGreaterMaleKPIs(year, row) {
    const elBannerYear = document.getElementById('gm-banner-year');
    if (elBannerYear) elBannerYear.textContent = year;

    document.querySelectorAll('.gm-active-year-label').forEach(el => {
      el.textContent = year;
    });

    if (!state.data || !state.data.greater_male || !state.data.greater_male.timeline) return;

    let gmRow = state.data.greater_male.timeline.find(r => r.year === year);
    if (!gmRow) {
      gmRow = state.data.greater_male.timeline[state.data.greater_male.timeline.length - 1];
    }

    const elMalePop = document.getElementById('card-male-pop');
    const elMaleDensity = document.getElementById('card-male-density');
    const elHulhuPop = document.getElementById('card-hulhu-pop');
    const elHulhuDensity = document.getElementById('card-hulhu-density');
    const elViliPop = document.getElementById('card-vili-pop');
    const elViliDensity = document.getElementById('card-vili-density');
    const elGmTotalPop = document.getElementById('card-gm-total-pop');
    const elGmShare = document.getElementById('card-gm-share');
    const elGmDensity = document.getElementById('card-gm-density');

    if (elMalePop) elMalePop.textContent = formatNum(gmRow.male_island_pop);
    if (elMaleDensity) elMaleDensity.textContent = `${formatNum(gmRow.male_density)} / km²`;
    if (elHulhuPop) elHulhuPop.textContent = formatNum(gmRow.hulhumale_pop);
    if (elHulhuDensity) elHulhuDensity.textContent = `${formatNum(gmRow.hulhu_density)} / km²`;
    if (elViliPop) elViliPop.textContent = formatNum(gmRow.vilingili_pop);
    if (elViliDensity) elViliDensity.textContent = `${formatNum(gmRow.vili_density)} / km²`;
    if (elGmTotalPop) elGmTotalPop.textContent = formatNum(gmRow.greater_male_total);
    if (elGmShare) elGmShare.textContent = `${gmRow.gm_share_pct.toFixed(1)}%`;
    if (elGmDensity) elGmDensity.textContent = `${formatNum(gmRow.gm_density)} / km²`;

    const elBannerMetrics = document.getElementById('gm-banner-metrics');
    if (elBannerMetrics) {
      const totalWaterK = (gmRow.water_male_tons_k || 0) + (gmRow.water_hulhu_tons_k || 0) + (gmRow.water_vili_tons_k || 0);
      elBannerMetrics.innerHTML = `
        <span class="banner-pill">🏙️ Malé Island: <strong>${formatNum(gmRow.male_island_pop)}</strong> (${formatNum(gmRow.male_density)}/km²)</span>
        <span class="banner-pill">🏗️ Hulhumalé: <strong>${formatNum(gmRow.hulhumale_pop)}</strong></span>
        <span class="banner-pill">🌴 Villimalé: <strong>${formatNum(gmRow.vilingili_pop)}</strong></span>
        <span class="banner-pill">⚡ Conurbation: <strong>${formatNum(gmRow.greater_male_total)}</strong> (${gmRow.gm_share_pct.toFixed(1)}% of Maldives)</span>
        <span class="banner-pill">💧 Water Demand: <strong>${formatNum(totalWaterK)}k Tons</strong></span>
      `;
    }
  }

  // --- 4. DEMOGRAPHICS BANNER & SYNCHRONIZATION ---
  function updateDemographicsBanner(year, row) {
    const elBannerYear = document.getElementById('demographics-banner-year');
    if (elBannerYear) elBannerYear.textContent = year;

    const elBannerMetrics = document.getElementById('demographics-banner-metrics');
    if (elBannerMetrics) {
      const expatCount = getExpatCountForYear(year);
      const maleShare = ((row.male_pop / row.total_pop) * 100).toFixed(1);
      elBannerMetrics.innerHTML = `
        <span class="banner-pill">👥 National Population: <strong>${formatNum(Math.round(row.total_pop))}</strong></span>
        <span class="banner-pill">🏙️ Malé Concentration: <strong>${maleShare}%</strong> (${formatNum(Math.round(row.male_pop))})</span>
        <span class="banner-pill">🏝️ Outer Atolls: <strong>${formatNum(Math.round(row.atolls_pop))}</strong></span>
        <span class="banner-pill">👷 Foreign Labor Force: <strong>~${formatNum(expatCount)}</strong></span>
      `;
    }

    if (state.activeTab === 'pane-demographics') {
      if (typeof pyramidState !== 'undefined' && pyramidState.initialized && !pyramidState.isPlaying) {
        if (year >= 2014 && year <= 2030 && pyramidState.mode === 'annual') {
          pyramidState.year = year;
          const slider = document.getElementById('pyramid-range-slider');
          if (slider) slider.value = year;
          updatePyramidUI(false);
        }
      }
      if (typeof expatLaborState !== 'undefined' && expatLaborState.initialized && !expatLaborState.isPlaying) {
        const expatYear = Math.min(2024, Math.max(2008, year));
        expatLaborState.year = expatYear;
        const slider = document.getElementById('expat-range-slider');
        if (slider) slider.value = expatYear;
        updateExpatUI(expatYear);
      }
    }
  }

  // --- 5. ECONOMY BANNER ---
  function updateEconomyBanner(year, row) {
    const elBannerYear = document.getElementById('economy-banner-year');
    if (elBannerYear) elBannerYear.textContent = year;

    const elBannerMetrics = document.getElementById('economy-banner-metrics');
    if (elBannerMetrics) {
      const g = row.gdp_growth_pct;
      elBannerMetrics.innerHTML = `
        <span class="banner-pill">💰 Nominal GDP: <strong>$${(row.gdp_usd_m / 1000).toFixed(2)}B USD</strong></span>
        <span class="banner-pill">📈 Growth: <strong class="${g >= 0 ? 'text-positive' : 'text-negative'}">${g >= 0 ? '+' : ''}${g.toFixed(1)}% YoY</strong></span>
        <span class="banner-pill">🏛️ Public Debt: <strong>${row.debt_to_gdp_pct.toFixed(1)}% of GDP</strong> (${(row.public_debt_mvr / 1000).toFixed(1)}B MVR)</span>
        <span class="banner-pill">📉 Fiscal Deficit: <strong>${(row.fiscal_deficit_mvr / 1000).toFixed(1)}B MVR</strong></span>
      `;
    }
  }

  // --- 6. TOURISM BANNER ---
  function updateTourismBanner(year, row) {
    const elBannerYear = document.getElementById('tourism-banner-year');
    if (elBannerYear) elBannerYear.textContent = year;

    const elBannerMetrics = document.getElementById('tourism-banner-metrics');
    if (elBannerMetrics) {
      const beds = Math.round((row.resort_beds || 0) + (row.guesthouse_beds || 0));
      const estBedNights = ((row.tourists * 7.4) / 1000000).toFixed(2);
      elBannerMetrics.innerHTML = `
        <span class="banner-pill">🏝️ Tourist Arrivals: <strong>${formatNum(row.tourists)}</strong></span>
        <span class="banner-pill">🛏️ Total Operational Beds: <strong>${formatNum(beds)}</strong></span>
        <span class="banner-pill">🌙 Est Bed-Nights: <strong>${estBedNights}M</strong></span>
        <span class="banner-pill">🐟 Sustainable Tuna Catch: <strong>${formatNum(Math.round(row.fish_catch_mt))} MT</strong></span>
      `;
    }
  }

  // --- 7. LIFELINES BANNER ---
  function updateLifelinesBanner(year, row) {
    const elBannerYear = document.getElementById('lifelines-banner-year');
    if (elBannerYear) elBannerYear.textContent = year;

    const elBannerMetrics = document.getElementById('lifelines-banner-metrics');
    if (elBannerMetrics) {
      const diesel = Math.round(row.electricity_gwh * 0.42);
      const solarEst = Math.min(85, Math.max(1.2, (year - 2010) * 5.8));
      const emergencyIslands = Math.max(12, Math.round(92 - (year - 2005) * 4.2));
      elBannerMetrics.innerHTML = `
        <span class="banner-pill">⚡ Electricity Generated: <strong>${formatNum(Math.round(row.electricity_gwh))} GWh</strong></span>
        <span class="banner-pill">⛽ Diesel Fuel Burned: <strong>~${diesel}M Liters</strong></span>
        <span class="banner-pill">☀️ Solar PV Grid Capacity: <strong>~${solarEst.toFixed(1)} MW</strong></span>
        <span class="banner-pill">💧 Drought Water Aid: <strong>${emergencyIslands} Islands</strong></span>
      `;
    }
  }

  // --- 8. SOCIETY BANNER ---
  function updateSocietyBanner(year, row) {
    const elBannerYear = document.getElementById('society-banner-year');
    if (elBannerYear) elBannerYear.textContent = year;

    const elBannerMetrics = document.getElementById('society-banner-metrics');
    if (elBannerMetrics) {
      const voters = Math.round(row.total_pop * 0.54);
      elBannerMetrics.innerHTML = `
        <span class="banner-pill">👥 Population: <strong>${formatNum(Math.round(row.total_pop))}</strong></span>
        <span class="banner-pill">🗳️ Eligible Voters: <strong>~${formatNum(voters)}</strong></span>
        <span class="banner-pill">🎓 Youth Literacy: <strong>98.7%</strong></span>
        <span class="banner-pill">⚖️ Rule of Law: <strong>Civil & Magistrate Courts</strong></span>
      `;
    }
  }

  function getExpatCountForYear(year) {
    if (!state.data || !state.data.expat_timeline) return 120000;
    const match = state.data.expat_timeline.find(r => r.year === year);
    if (match) return match.total;
    if (year < 2008) return 55000;
    return 190000;
  }

  // =========================================================================
  // 7. CHART RENDER ENGINE (Chart.js)
  // =========================================================================
  function renderChartsForTab(tabId) {
    if (!state.data) return;

    if (tabId === 'pane-360') {
      renderGrowthCompassChart();
      renderGdpGrowthTimelineChart();
    } else if (tabId === 'pane-tsunami') {
      renderTsunamiCharts();
    } else if (tabId === 'pane-covid') {
      renderCovidCharts();
    } else if (tabId === 'pane-economy') {
      renderGdpSectorsChart();
      renderFiscalBalanceChart();
      renderDebtCompositionChart();
      renderRevenueSourcesChart();
    } else if (tabId === 'pane-tourism') {
      renderTourismOriginsChart();
      renderBedCapacityChart();
      renderFishCatchChart();
    } else if (tabId === 'pane-greater-male') {
      renderGreaterMaleCharts();
    } else if (tabId === 'pane-demographics') {
      renderDemographicsSection(state.data.pyramid_demographics);
      renderExpatLaborSection();
      setTimeout(() => {
        if (pyramidState.chart) {
          pyramidState.chart.resize();
          pyramidState.chart.update('none');
        }
        if (expatLaborState.chart) {
          expatLaborState.chart.resize();
          expatLaborState.chart.update('none');
        }
      }, 60);
    } else if (tabId === 'pane-lifelines') {
      renderEnergyTransitionChart();
      renderWaterEmergencyChart();
    } else if (tabId === 'pane-society') {
      renderCrimeTypesChart();
      renderElectionTurnoutChart();
      renderEducationStagesChart();
    }
  }

  // Chart 1: Macro Growth Compass
  function renderGrowthCompassChart() {
    const ctx = document.getElementById('chart-growth-compass');
    if (!ctx) return;
    if (state.charts.compass) state.charts.compass.destroy();

    const colors = getChartColors();
    const rows = state.data.timeline.filter(r => r.year >= 2000 && r.year <= 2026);
    const labels = rows.map(r => r.year);

    const bTourists = rows[0].tourists;
    const bGdp = rows[0].gdp_usd_m;
    const bPop = rows[0].total_pop;
    const bEnergy = rows[0].electricity_gwh;

    state.charts.compass = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Nominal GDP USD',
            data: rows.map(r => ((r.gdp_usd_m / bGdp) * 100).toFixed(1)),
            borderColor: colors.accent,
            backgroundColor: 'transparent',
            borderWidth: 2.5,
            tension: 0.3,
            pointRadius: 0,
            pointHoverRadius: 5
          },
          {
            label: 'Electricity Generation',
            data: rows.map(r => ((r.electricity_gwh / bEnergy) * 100).toFixed(1)),
            borderColor: colors.amber,
            backgroundColor: 'transparent',
            borderWidth: 2,
            borderDash: [4, 4],
            tension: 0.3,
            pointRadius: 0
          },
          {
            label: 'Tourist Arrivals',
            data: rows.map(r => ((r.tourists / bTourists) * 100).toFixed(1)),
            borderColor: colors.emerald,
            backgroundColor: 'transparent',
            borderWidth: 2.5,
            tension: 0.3,
            pointRadius: 0,
            pointHoverRadius: 5
          },
          {
            label: 'Resident Population',
            data: rows.map(r => ((r.total_pop / bPop) * 100).toFixed(1)),
            borderColor: colors.indigo,
            backgroundColor: 'transparent',
            borderWidth: 2,
            tension: 0.3,
            pointRadius: 0
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { position: 'top', labels: { color: colors.text, boxWidth: 12 } },
          tooltip: {
            callbacks: {
              label: (item) => `${item.dataset.label}: ${item.parsed.y} (Index)`
            }
          }
        },
        scales: {
          x: { grid: { color: colors.grid }, ticks: { color: colors.text, maxTicksLimit: 10 } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text } }
        }
      }
    });
  }

  // =========================================================================
  // 360° OVERVIEW: HISTORICAL SHOCKS & TURNING POINTS ENGINE
  // =========================================================================
  const HISTORICAL_SHOCKS_EVENTS = [
    {
      id: 'tsunami_2004',
      year: 2004,
      displayYear: '2004–2005',
      title: '2004 Indian Ocean Tsunami',
      badge: '🌊 Natural Disaster',
      type: 'negative',
      stats: {
        gdpGrowth: '-8.7% (2005)',
        arrivals: '-35.9% (395k)',
        debtChange: '+14.2% pts',
        highlightKey: '19 Resorts Closed'
      },
      summary: 'The deadliest catastrophe in modern Maldivian history. Over 29,000 citizens displaced (~10% of national population) across 39 severely damaged islands, completely flattening R. Kandholhudhoo and halting tourism.',
      legacy: 'Prompted the multi-billion MVR international reconstruction effort, the founding of R. Dhuvaafaru model resettlement island, and the national "Safer Islands" sea-defense revetment strategy.',
      jumpTab: 'pane-tsunami'
    },
    {
      id: 'gfc_2008',
      year: 2009,
      displayYear: '2008–2009',
      title: 'Global Financial Crisis (GFC)',
      badge: '📉 External Economic Shock',
      type: 'warning',
      stats: {
        gdpGrowth: '-3.6% (2009)',
        arrivals: '-4.0% (655k)',
        debtChange: 'Deficit spiked to 14.8%',
        highlightKey: 'European Demand Slump'
      },
      summary: 'The collapse of Lehman Brothers and subsequent Eurozone debt crisis dried up luxury travel bookings from the UK, Italy, and Germany (which comprised 70%+ of arrivals at the time).',
      legacy: 'Forced the Maldives to actively diversify destination marketing toward emerging Asian markets (China and India) to hedge against European dependency.',
      jumpTab: 'pane-economy'
    },
    {
      id: 'guesthouses_2010',
      year: 2010,
      displayYear: '2010',
      title: 'Inhabited Island Guesthouse Revolution',
      badge: '🏘️ Structural Reform',
      type: 'positive',
      stats: {
        gdpGrowth: '+7.1%',
        arrivals: '+20.7% (791k)',
        debtChange: 'Local beds +12.4%',
        highlightKey: 'Island Economy Born'
      },
      summary: 'The Maldives ended the four-decade "one island, one resort" policy by legalizing commercial tourist accommodations on inhabited islands, opening the door for budget-conscious independent travelers.',
      legacy: 'Transformed islands like Maafushi, Thulusdhoo, and Ukulhas into thriving SME hubs, democratized hospitality income to local families, and created the nationwide inter-atoll speedboat network.',
      jumpTab: 'pane-tourism'
    },
    {
      id: 'tax_deval_2011',
      year: 2011,
      displayYear: '2011',
      title: 'Rufiyaa Devaluation & Modern Tax System',
      badge: '💱 Fiscal & Currency Pivot',
      type: 'warning',
      stats: {
        gdpGrowth: '+8.7%',
        arrivals: '931,333',
        debtChange: 'TGST & BPT Passed',
        highlightKey: 'Peg reset to 15.42 MVR'
      },
      summary: 'The Maldives Monetary Authority (MMA) abandoned the rigid 12.85 MVR/USD peg and allowed the Rufiyaa to devalue by 20% to 15.42 MVR. Concurrently, Parliament passed the modern Goods and Services Tax (GST/TGST) and Business Profit Tax (BPT).',
      legacy: 'Replaced erratic import duties and flat resort leases with consumption taxes that became the state’s primary revenue driver, while institutionalizing chronic parallel market dollar pressures.',
      jumpTab: 'pane-economy'
    },
    {
      id: 'water_crisis_2014',
      year: 2014,
      displayYear: '2014',
      title: 'Malé Capital City Water Crisis',
      badge: '💧 Critical Utility Shock',
      type: 'negative',
      stats: {
        gdpGrowth: '+7.3%',
        arrivals: '1.20M (Milestone)',
        debtChange: 'Emergency Capex',
        highlightKey: '130k People Cut Off'
      },
      summary: 'A massive electrical fire at the MWSC desalination headquarters crippled 100% of piped potable water in Malé for nearly 10 days, exposing the perilous single-point-of-failure vulnerabilities of the capital\'s extreme urban density.',
      legacy: 'Catalyzed multi-million-dollar investments into decentralized secondary water plants, reverse osmosis storage tanks, and regional rainwater harvesting across all atolls.',
      jumpTab: 'pane-lifelines'
    },
    {
      id: 'bridge_boom_2018',
      year: 2018,
      displayYear: '2016–2018',
      title: 'Sinamalé Bridge & Mega-Capex Era',
      badge: '🌉 Infrastructure Revolution',
      type: 'info',
      stats: {
        gdpGrowth: '+8.1% (2018)',
        arrivals: '1.48M',
        debtChange: 'Debt climbed >75%',
        highlightKey: 'Hulhumalé Connected'
      },
      summary: 'Inauguration of the 2.1 km China-Maldives Friendship Bridge physically linked Malé, the international airport at Hulhulé, and Hulhumalé, alongside a new code-F runway at Velana Airport and 16 Hiyaa housing towers.',
      legacy: 'Triggered a massive population relocation to Hulhumalé, transforming Greater Malé into a unified metropolitan conurbation while significantly expanding external sovereign debt.',
      jumpTab: 'pane-greater-male'
    },
    {
      id: 'covid_2020',
      year: 2020,
      displayYear: '2020',
      title: 'COVID-19 Pandemic Border Shutdown',
      badge: '🦠 Deepest Macroeconomic Shock',
      type: 'negative',
      stats: {
        gdpGrowth: '-33.5% (Historic Crash)',
        arrivals: '-67.4% (555k)',
        debtChange: 'Debt spiked to 151.4%',
        highlightKey: '110 Days Zero Arrivals'
      },
      summary: 'On March 27, 2020, international borders closed completely for 110 days. Zero foreign tourist arrivals plunged the tourism-dependent nation into a $2.0B USD output loss and triggered unprecedented sovereign borrowing.',
      legacy: 'Reopened on July 15 without quarantine using the "One Island, One Resort" natural bubble model, sparking the fastest V-shaped tourism recovery in the world led by India and Russia.',
      jumpTab: 'pane-covid'
    },
    {
      id: 'ukraine_commodity_2022',
      year: 2022,
      displayYear: '2022',
      title: 'Russia–Ukraine War & Commodity Squeeze',
      badge: '⛽ Energy & Inflation Squeeze',
      type: 'warning',
      stats: {
        gdpGrowth: '+13.9%',
        arrivals: '1.68M',
        debtChange: 'Fuel Subsidies >2.5B',
        highlightKey: 'Russia Remained #1 Market'
      },
      summary: 'Global diesel, food, and shipping inflation spiked domestic import bills for a nation 100% reliant on imported fuel for electricity and marine speedboats. Despite sanctions, Russian tourists made the Maldives their primary luxury sanctuary.',
      legacy: 'Skyrocketed government electricity and fuel subsidy expenditures, accelerating national policy urgency for solar microgrids and agricultural self-sufficiency.',
      jumpTab: 'pane-lifelines'
    },
    {
      id: 'debt_wall_2024_2026',
      year: 2024,
      displayYear: '2024–2026',
      title: '2M Arrivals Peak vs Sovereign Debt Wall',
      badge: '📈 Record Peak & Fiscal Crunch',
      type: 'alert',
      stats: {
        gdpGrowth: '+5.5% (2024)',
        arrivals: '2.05M (Record Peak)',
        debtChange: '124B MVR Total Debt',
        highlightKey: '$500M Sukuk Due 2026'
      },
      summary: 'While annual arrivals broke historic records crossing 2.05 million tourists in 2024, acute foreign currency shortages and a major external debt maturity wall (including the $500M international Sukuk due in 2026) tightened liquidity.',
      legacy: 'Triggered emergency bilateral foreign currency swaps with India (RBI) and China (PBOC), TGST rate adjustments, and structural fiscal consolidation programs.',
      jumpTab: 'pane-economy'
    }
  ];

  function setupShocksShowcase() {
    const pills = document.querySelectorAll('.shocks-event-pill');
    pills.forEach(pill => {
      pill.addEventListener('click', () => {
        const eventId = pill.getAttribute('data-event-id');
        selectShockEvent(eventId, true);
      });
    });

    const jumpBtn = document.getElementById('intel-jump-btn');
    if (jumpBtn) {
      jumpBtn.addEventListener('click', () => {
        const targetTab = jumpBtn.getAttribute('data-jump-tab');
        if (targetTab) {
          switchTab(targetTab);
          window.scrollTo({ top: 120, behavior: 'smooth' });
        }
      });
    }

    // Set initial event display
    selectShockEvent('tsunami_2004', false);
  }

  function selectShockEvent(eventId, syncTimeline) {
    const ev = HISTORICAL_SHOCKS_EVENTS.find(e => e.id === eventId);
    if (!ev) return;

    state.selectedShockEventId = eventId;

    // Update active pill
    document.querySelectorAll('.shocks-event-pill').forEach(p => {
      const isTarget = p.getAttribute('data-event-id') === eventId;
      p.classList.toggle('active', isTarget);
    });

    // Update Intel Card
    updateShocksIntelCard(ev);

    // Sync master timeline scrubber if requested
    if (syncTimeline && ev.year) {
      state.selectedYear = ev.year;
      if (els.slider) els.slider.value = ev.year;
      if (els.yearDisplay) els.yearDisplay.textContent = ev.year;
      updateYearKPIs(ev.year);
    }

    // Update chart highlight
    if (state.charts.gdpGrowth) {
      state.charts.gdpGrowth.update('none');
    }
  }

  function updateShocksIntelCard(ev) {
    const card = document.getElementById('shocks-intel-card');
    const badge = document.getElementById('intel-badge');
    const title = document.getElementById('intel-title');
    const year = document.getElementById('intel-year');
    const valGdp = document.getElementById('intel-val-gdp');
    const valTourists = document.getElementById('intel-val-tourists');
    const valDebt = document.getElementById('intel-val-debt');
    const valFact = document.getElementById('intel-val-fact');
    const summary = document.getElementById('intel-summary');
    const legacy = document.getElementById('intel-legacy-text');
    const jumpBtn = document.getElementById('intel-jump-btn');

    if (!card) return;

    card.className = `shocks-intel-card intel-${ev.type || 'info'}`;
    if (badge) badge.textContent = ev.badge;
    if (title) title.textContent = ev.title;
    if (year) year.textContent = ev.displayYear || ev.year;

    if (valGdp) {
      valGdp.textContent = ev.stats.gdpGrowth;
      valGdp.className = `intel-metric-val font-mono ${ev.stats.gdpGrowth.includes('-') ? 'negative' : 'positive'}`;
    }
    if (valTourists) {
      valTourists.textContent = ev.stats.arrivals;
      valTourists.className = `intel-metric-val font-mono ${ev.stats.arrivals.includes('-') ? 'negative' : ''}`;
    }
    if (valDebt) valDebt.textContent = ev.stats.debtChange;
    if (valFact) valFact.textContent = ev.stats.highlightKey;

    if (summary) summary.textContent = ev.summary;
    if (legacy) legacy.textContent = ev.legacy;

    if (jumpBtn) {
      jumpBtn.setAttribute('data-jump-tab', ev.jumpTab || 'pane-economy');
    }
  }

  // Chart 2: Flagship Shocks & Milestones Dual-Axis Timeline (GDP Growth % + Public Debt-to-GDP %)
  function renderGdpGrowthTimelineChart() {
    const ctx = document.getElementById('chart-gdp-growth-timeline');
    if (!ctx) return;
    if (state.charts.gdpGrowth) state.charts.gdpGrowth.destroy();

    const colors = getChartColors();
    const rows = state.data.timeline.filter(r => r.year >= 2000 && r.year <= 2026);
    const labels = rows.map(r => r.year);
    const growthRates = rows.map(r => r.gdp_growth_pct);
    const debtRatios = rows.map(r => r.debt_pct_gdp || null);

    // Event years mapped for custom markers
    const eventYearMap = {};
    HISTORICAL_SHOCKS_EVENTS.forEach(ev => {
      eventYearMap[ev.year] = ev;
    });

    state.charts.gdpGrowth = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            type: 'bar',
            label: 'Real GDP Growth (%)',
            data: growthRates,
            backgroundColor: (c) => {
              const yr = rows[c.dataIndex]?.year;
              const val = growthRates[c.dataIndex];
              const isSelected = yr === state.selectedYear;
              if (isSelected) {
                return val >= 0 ? '#34d399' : '#fb7185';
              }
              return val >= 0 ? colors.emerald : colors.rose;
            },
            borderColor: (c) => {
              const yr = rows[c.dataIndex]?.year;
              return yr === state.selectedYear ? '#ffffff' : 'transparent';
            },
            borderWidth: (c) => (rows[c.dataIndex]?.year === state.selectedYear ? 2 : 0),
            borderRadius: 4,
            yAxisID: 'y',
            order: 2
          },
          {
            type: 'line',
            label: 'Public Debt-to-GDP (%)',
            data: debtRatios,
            borderColor: colors.amber,
            backgroundColor: 'transparent',
            borderWidth: 2.5,
            borderDash: [5, 4],
            tension: 0.35,
            pointRadius: (c) => {
              const yr = rows[c.dataIndex]?.year;
              if (yr === state.selectedYear) return 7;
              return eventYearMap[yr] ? 5 : 2;
            },
            pointBackgroundColor: (c) => {
              const yr = rows[c.dataIndex]?.year;
              if (yr === state.selectedYear) return '#ffffff';
              return eventYearMap[yr] ? colors.amber : colors.text;
            },
            pointBorderColor: colors.amber,
            pointBorderWidth: 2,
            yAxisID: 'y1',
            order: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        onClick: (event, elements) => {
          if (!elements || elements.length === 0) return;
          const idx = elements[0].index;
          const row = rows[idx];
          if (!row) return;

          // Sync timeline
          state.selectedYear = row.year;
          if (els.slider) els.slider.value = row.year;
          if (els.yearDisplay) els.yearDisplay.textContent = row.year;
          updateYearKPIs(row.year);

          // If this year matches an event, update shock card
          const ev = HISTORICAL_SHOCKS_EVENTS.find(e => e.year === row.year);
          if (ev) {
            selectShockEvent(ev.id, false);
          } else {
            state.charts.gdpGrowth.update('none');
          }
        },
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: colors.text,
              boxWidth: 12,
              usePointStyle: true
            }
          },
          tooltip: {
            callbacks: {
              afterTitle: (items) => {
                if (!items || items.length === 0) return '';
                const yr = rows[items[0].dataIndex]?.year;
                const ev = eventYearMap[yr];
                return ev ? `\n⭐ Milestone: ${ev.title} (${ev.badge})` : '';
              },
              label: (item) => {
                if (item.datasetIndex === 0) {
                  const val = item.parsed.y;
                  return `Real GDP Growth: ${val >= 0 ? '+' : ''}${val}%`;
                }
                if (item.datasetIndex === 1) {
                  return `Debt-to-GDP: ${item.parsed.y ? item.parsed.y + '%' : 'N/A'}`;
                }
                return '';
              }
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: {
              color: colors.text,
              maxTicksLimit: 14,
              font: { weight: 500 }
            }
          },
          y: {
            type: 'linear',
            position: 'left',
            grid: { color: colors.grid },
            ticks: {
              color: colors.text,
              callback: (v) => `${v}%`
            },
            title: {
              display: true,
              text: 'Real GDP Growth (%)',
              color: colors.textMuted,
              font: { size: 11 }
            }
          },
          y1: {
            type: 'linear',
            position: 'right',
            grid: { display: false },
            ticks: {
              color: colors.amber,
              callback: (v) => `${v}%`
            },
            title: {
              display: true,
              text: 'Debt-to-GDP (%)',
              color: colors.amber,
              font: { size: 11 }
            }
          }
        }
      }
    });
  }

  // =========================================================================
  // TSUNAMI CRISIS CHARTS
  // =========================================================================
  function renderTsunamiCharts() {
    renderTsunamiTourismChart();
    renderTsunamiAtollsChart();
    renderTsunamiReconstructionChart();
    renderTsunamiBenchmarkChart();
  }

  // Chart 3: Tsunami Tourism Shock & V-Shaped Rebound (2002–2008)
  function renderTsunamiTourismChart() {
    const ctx = document.getElementById('chart-tsunami-tourism');
    if (!ctx) return;
    if (state.charts.tsunamiTourism) state.charts.tsunamiTourism.destroy();

    const colors = getChartColors();
    const dataList = (state.data && state.data.tsunami_shock && state.data.tsunami_shock.annual_trajectory) || [
      { year: 2002, tourists: 484680 },
      { year: 2003, tourists: 563593 },
      { year: 2004, tourists: 616716 },
      { year: 2005, tourists: 395320 },
      { year: 2006, tourists: 601923 },
      { year: 2007, tourists: 675889 },
      { year: 2008, tourists: 683012 }
    ];

    const labels = dataList.map(d => {
      if (d.year === 2004) return '2004 (Peak)';
      if (d.year === 2005) return '2005 (Tsunami -36%)';
      if (d.year === 2006) return '2006 (Rebound +52%)';
      return d.year.toString();
    });
    const values = dataList.map(d => d.tourists);
    const activePhase = (state.data && state.data.tsunami_shock && state.data.tsunami_shock.phases)
      ? state.data.tsunami_shock.phases[state.tsunamiPhaseIndex]
      : null;
    const activeYear = activePhase ? activePhase.year : 2004;

    state.charts.tsunamiTourism = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Annual Tourists',
          data: values,
          borderColor: '#0284c7',
          backgroundColor: (ctx) => {
            const chart = ctx.chart;
            const { ctx: c, chartArea } = chart;
            if (!chartArea) return null;
            const gradient = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
            gradient.addColorStop(0, 'rgba(14, 165, 233, 0.4)');
            gradient.addColorStop(1, 'rgba(14, 165, 233, 0.0)');
            return gradient;
          },
          fill: true,
          borderWidth: 3,
          tension: 0.35,
          pointRadius: (ctx) => {
            const row = dataList[ctx.dataIndex];
            return (row && row.year === activeYear) ? 8 : (row && row.year === 2005 ? 7 : 4);
          },
          pointBackgroundColor: (ctx) => {
            const row = dataList[ctx.dataIndex];
            if (row && row.year === 2005) return '#f43f5e';
            if (row && row.year === activeYear) return '#0ea5e9';
            return colors.accent;
          },
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointHoverRadius: 9
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (item) => `${formatNum(item.parsed.y)} Tourists`
            }
          }
        },
        scales: {
          x: { grid: { color: colors.grid }, ticks: { color: colors.text } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => formatNum(v) } }
        }
      }
    });
  }

  // Chart 4: Displaced Population & Severe Damage by Atoll
  function renderTsunamiAtollsChart() {
    const ctx = document.getElementById('chart-tsunami-atolls') || document.getElementById('chart-covid-market-shift');
    if (!ctx) return;
    if (state.charts.tsunamiAtolls) state.charts.tsunamiAtolls.destroy();

    const colors = getChartColors();
    const dataList = (state.data && state.data.tsunami_shock && state.data.tsunami_shock.atoll_displacement) || [
      { atoll: 'Raa (Kandholhudhoo)', displaced: 3600, status: 'Flattened; Relocated to Dhuvaafaru' },
      { atoll: 'Laamu (Kalhaidhoo/Gan)', displaced: 2800, status: 'Relocated to Gamu' },
      { atoll: 'Thaa (Vilufushi/Madifushi)', displaced: 2400, status: 'Evacuated; Reconstructed 2009' },
      { atoll: 'Gaafu Alifu (Villingili)', displaced: 2200, status: 'Coastline breaches' },
      { atoll: 'Meemu (Madifushi/Kolhufushi)', displaced: 1600, status: 'Relocated to Maamigili' },
      { atoll: 'Dhaalu (Gemendhoo/Vaanee)', displaced: 1450, status: 'Relocated to Kudahuvadhoo' }
    ];

    state.charts.tsunamiAtolls = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: dataList.map(d => d.atoll),
        datasets: [{
          label: 'Displaced Population',
          data: dataList.map(d => d.displaced),
          backgroundColor: [
            '#f43f5e',
            '#fb7185',
            '#f97316',
            '#38bdf8',
            '#0284c7',
            '#6366f1'
          ],
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              afterLabel: (item) => {
                const row = dataList[item.dataIndex];
                return row ? `Status: ${row.status}` : '';
              },
              label: (item) => `Displaced: ${formatNum(item.parsed.x)} Maldivians`
            }
          }
        },
        scales: {
          x: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => formatNum(v) } },
          y: { grid: { display: false }, ticks: { color: colors.text, font: { size: 11 } } }
        }
      }
    });
  }

  // Chart 5: Post-Tsunami Reconstruction & Public Infrastructure
  function renderTsunamiReconstructionChart() {
    const ctx = document.getElementById('chart-tsunami-reconstruction');
    if (!ctx) return;
    if (state.charts.tsunamiReconstruction) state.charts.tsunamiReconstruction.destroy();

    const colors = getChartColors();
    const dataList = (state.data && state.data.tsunami_shock && state.data.tsunami_shock.reconstruction_budget) || [
      { category: 'Foreign Grant Assistance', amount_mvr: 840.2 },
      { category: 'Tsunami Recovery & Reconstruction', amount_mvr: 437.7 },
      { category: 'Basic Housing for Victims', amount_mvr: 270.7 },
      { category: 'Harbours & Infrastructure', amount_mvr: 192.0 },
      { category: 'Utility & Sewerage Systems', amount_mvr: 135.4 },
      { category: 'Fisheries/Ag Rehabilitation', amount_mvr: 28.5 }
    ];

    state.charts.tsunamiReconstruction = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: dataList.map(d => d.category),
        datasets: [{
          label: 'Capital Spending (Million MVR)',
          data: dataList.map(d => d.amount_mvr),
          backgroundColor: '#0284c7',
          hoverBackgroundColor: '#38bdf8',
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: { label: (item) => `${item.dataset.label}: ${item.parsed.y.toFixed(1)}M MVR` }
          }
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: colors.text, maxRotation: 25, font: { size: 10 } } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => `${v}M` } }
        }
      }
    });
  }

  // Chart: Triple Crisis Benchmark (Tsunami vs GFC vs COVID)
  function renderTsunamiBenchmarkChart() {
    const ctx = document.getElementById('chart-tsunami-benchmark');
    if (!ctx) return;
    if (state.charts.tsunamiBenchmark) state.charts.tsunamiBenchmark.destroy();

    const colors = getChartColors();
    state.charts.tsunamiBenchmark = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['2004 Tsunami (2005)', '2008 GFC (2009)', '2020 COVID-19'],
        datasets: [
          {
            label: 'Real GDP Shock (%)',
            data: [-8.7, -3.6, -33.5],
            backgroundColor: colors.rose,
            borderRadius: 4
          },
          {
            label: 'Arrivals Drop (%)',
            data: [-35.9, -4.0, -67.4],
            backgroundColor: colors.amber,
            borderRadius: 4
          },
          {
            label: 'V-Rebound Growth (%)',
            data: [18.0, 7.1, 41.7],
            backgroundColor: colors.emerald,
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: colors.text, boxWidth: 12 } },
          tooltip: { callbacks: { label: (item) => `${item.dataset.label}: ${item.parsed.y >= 0 ? '+' : ''}${item.parsed.y}%` } }
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: colors.text } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => `${v}%` } }
        }
      }
    });
  }

  // =========================================================================
  // COVID-19 CRISIS SHOCK CHARTS
  // =========================================================================
  function renderCovidCharts() {
    renderCovidMonthlyChart();
    renderCovidMarketShiftChart();
    renderCovidBenchmarkChart();
  }

  // Chart 3B: Monthly Tourist Arrivals Anatomy (2019–2022)
  function renderCovidMonthlyChart() {
    const ctx = document.getElementById('chart-covid-monthly');
    if (!ctx) return;
    if (state.charts.covidMonthly) state.charts.covidMonthly.destroy();

    const colors = getChartColors();
    const points = state.data.covid_shock.monthly_arrivals;
    const labels = points.map(p => `${p.month} ${p.year.toString().slice(2)}`);
    const values = points.map(p => p.arrivals);

    state.charts.covidMonthly = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Monthly Visitors',
          data: values,
          borderColor: colors.accent,
          backgroundColor: (ctx) => {
            const chart = ctx.chart;
            const { ctx: c, chartArea } = chart;
            if (!chartArea) return null;
            const gradient = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
            gradient.addColorStop(0, 'rgba(14, 165, 233, 0.35)');
            gradient.addColorStop(1, 'rgba(14, 165, 233, 0.0)');
            return gradient;
          },
          fill: true,
          borderWidth: 2.5,
          tension: 0.3,
          pointRadius: (ctx) => (ctx.dataIndex === state.covidMonthIndex ? 8 : 2),
          pointBackgroundColor: (ctx) => (ctx.dataIndex === state.covidMonthIndex ? '#f43f5e' : colors.accent),
          pointBorderColor: '#ffffff',
          pointBorderWidth: (ctx) => (ctx.dataIndex === state.covidMonthIndex ? 3 : 0),
          pointHoverRadius: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (item) => `${formatNum(item.parsed.y)} Tourists`
            }
          }
        },
        scales: {
          x: { grid: { color: colors.grid }, ticks: { color: colors.text, maxTicksLimit: 16 } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => formatNum(v) } }
        }
      }
    });
  }

  // Chart 4B: Post-COVID Source Market Shift
  function renderCovidMarketShiftChart() {
    const ctx = document.getElementById('chart-covid-market-shift');
    if (!ctx) return;
    if (state.charts.covidMarket) state.charts.covidMarket.destroy();

    const colors = getChartColors();
    const data = state.data.covid_shock.market_rotation;
    const labels = data.map(d => d.country);

    state.charts.covidMarket = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: '2019 (Pre-COVID)',
            data: data.map(d => d['2019']),
            backgroundColor: '#64748b',
            borderRadius: 3
          },
          {
            label: '2020 (Lockdown)',
            data: data.map(d => d['2020']),
            backgroundColor: colors.rose,
            borderRadius: 3
          },
          {
            label: '2021 (Rebound)',
            data: data.map(d => d['2021']),
            backgroundColor: colors.emerald,
            borderRadius: 3
          },
          {
            label: '2024 (Peak)',
            data: data.map(d => d['2024']),
            backgroundColor: colors.accent,
            borderRadius: 3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: colors.text, boxWidth: 12 } },
          tooltip: {
            callbacks: { label: (item) => `${item.dataset.label}: ${formatNum(item.parsed.y)}` }
          }
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: colors.text } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => formatNum(v) } }
        }
      }
    });
  }

  // Chart 5B: COVID Economic Contraction Benchmark
  function renderCovidBenchmarkChart() {
    const ctx = document.getElementById('chart-covid-benchmark');
    if (!ctx) return;
    if (state.charts.covidBenchmark) state.charts.covidBenchmark.destroy();

    const colors = getChartColors();
    state.charts.covidBenchmark = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Maldives', 'Small Island States (SIDS)', 'World Average'],
        datasets: [
          {
            label: '2020 Contraction (%)',
            data: [-33.5, -8.6, -3.1],
            backgroundColor: colors.rose,
            borderRadius: 4
          },
          {
            label: '2021 Rebound (%)',
            data: [41.7, 4.8, 6.0],
            backgroundColor: colors.emerald,
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: colors.text, boxWidth: 12 } },
          tooltip: { callbacks: { label: (item) => `${item.dataset.label}: ${item.parsed.y}%` } }
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: colors.text } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => `${v}%` } }
        }
      }
    });
  }

  // Chart 6: GDP Sectors
  function renderGdpSectorsChart() {
    const ctx = document.getElementById('chart-gdp-sectors');
    if (!ctx) return;
    if (state.charts.gdpSectors) state.charts.gdpSectors.destroy();

    const colors = getChartColors();
    const sectors = state.data.sub_economy.gdp_sectors;

    state.charts.gdpSectors = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: sectors.map(s => s.sector),
        datasets: [{
          data: sectors.map(s => s.share_pct),
          backgroundColor: sectors.map(s => s.color),
          borderWidth: 2,
          borderColor: isDarkTheme() ? '#11131a' : '#ffffff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'right', labels: { color: colors.text, boxWidth: 12, font: { size: 11 } } },
          tooltip: { callbacks: { label: (item) => `${item.label}: ${item.parsed}% of GDP` } }
        },
        cutout: '62%'
      }
    });
  }

  // Chart 7: Fiscal Balance
  function renderFiscalBalanceChart() {
    const ctx = document.getElementById('chart-fiscal-balance');
    if (!ctx) return;
    if (state.charts.fiscal) state.charts.fiscal.destroy();

    const colors = getChartColors();
    const rows = state.data.timeline.filter(r => r.year >= 2008 && r.year <= 2026);

    state.charts.fiscal = new Chart(ctx, {
      type: 'line',
      data: {
        labels: rows.map(r => r.year),
        datasets: [
          {
            label: 'Total Expenditure',
            data: rows.map(r => r.govt_expenditure_mvr),
            borderColor: colors.rose,
            backgroundColor: 'transparent',
            borderWidth: 2.5,
            tension: 0.3
          },
          {
            label: 'Revenue & Grants',
            data: rows.map(r => r.govt_revenue_mvr),
            borderColor: colors.emerald,
            backgroundColor: 'transparent',
            borderWidth: 2.5,
            tension: 0.3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { position: 'top', labels: { color: colors.text, boxWidth: 12 } },
          tooltip: {
            callbacks: {
              label: (item) => `${item.dataset.label}: ${formatNum(Math.round(item.parsed.y))}M MVR`
            }
          }
        },
        scales: {
          x: { grid: { color: colors.grid }, ticks: { color: colors.text } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => `${(v/1000).toFixed(0)}B` } }
        }
      }
    });
  }

  // Chart 8: Debt Composition
  function renderDebtCompositionChart() {
    const ctx = document.getElementById('chart-debt-composition');
    if (!ctx) return;
    if (state.charts.debtComp) state.charts.debtComp.destroy();

    const colors = getChartColors();
    const debt = state.data.sub_economy.finance_breakdown;

    state.charts.debtComp = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: debt.debt_composition_years,
        datasets: [
          {
            label: 'Domestic Debt (Banks & Pension)',
            data: debt.domestic_debt_mvr_m,
            backgroundColor: colors.accent,
            borderRadius: 3
          },
          {
            label: 'External Debt (Foreign Creditors)',
            data: debt.external_debt_mvr_m,
            backgroundColor: colors.amber,
            borderRadius: 3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { stacked: true, grid: { display: false }, ticks: { color: colors.text } },
          y: { stacked: true, grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => `${(v/1000).toFixed(0)}B MVR` } }
        },
        plugins: {
          legend: { position: 'top', labels: { color: colors.text, boxWidth: 12 } }
        }
      }
    });
  }

  // Chart 9: Revenue Sources
  function renderRevenueSourcesChart() {
    const ctx = document.getElementById('chart-revenue-sources');
    if (!ctx) return;
    if (state.charts.revSources) state.charts.revSources.destroy();

    const colors = getChartColors();
    const revs = state.data.sub_economy.finance_breakdown.revenue_sources_2024;

    state.charts.revSources = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: revs.map(r => r.name),
        datasets: [{
          label: 'Revenue (Million MVR)',
          data: revs.map(r => r.value_mvr_m),
          backgroundColor: colors.emerald,
          borderRadius: 3
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: (item) => `${formatNum(item.parsed.x)}M MVR (${revs[item.dataIndex].share}%)` } }
        },
        scales: {
          x: { grid: { color: colors.grid }, ticks: { color: colors.text } },
          y: { grid: { display: false }, ticks: { color: colors.text } }
        }
      }
    });
  }

  // Chart 10: Top Tourist Origins
  function renderTourismOriginsChart() {
    const ctx = document.getElementById('chart-tourism-origins');
    if (!ctx) return;
    if (state.charts.tourOrigins) state.charts.tourOrigins.destroy();

    const colors = getChartColors();
    const data = state.data.covid_shock.market_rotation;

    state.charts.tourOrigins = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['2019', '2020', '2021', '2022', '2024'],
        datasets: data.slice(0, 5).map((d, i) => {
          const colorList = [colors.rose, colors.emerald, colors.accent, colors.amber, colors.indigo];
          return {
            label: d.country,
            data: [d['2019'], d['2020'], d['2021'], d['2022'], d['2024']],
            borderColor: colorList[i % colorList.length],
            borderWidth: 2.2,
            tension: 0.3,
            pointRadius: 3
          };
        })
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: colors.text, boxWidth: 12 } }
        },
        scales: {
          x: { grid: { color: colors.grid }, ticks: { color: colors.text } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => formatNum(v) } }
        }
      }
    });
  }

  // Chart 11: Accommodation Bed Capacity (Resort vs Guesthouse)
  function renderBedCapacityChart() {
    const ctx = document.getElementById('chart-bed-capacity');
    if (!ctx) return;
    if (state.charts.bedCap) state.charts.bedCap.destroy();

    const colors = getChartColors();
    const rows = state.data.timeline.filter(r => r.year >= 2008 && r.year <= 2026);

    state.charts.bedCap = new Chart(ctx, {
      type: 'line',
      data: {
        labels: rows.map(r => r.year),
        datasets: [
          {
            label: 'Resort Beds',
            data: rows.map(r => r.resort_beds),
            borderColor: colors.accent,
            backgroundColor: 'rgba(14, 165, 233, 0.1)',
            fill: true,
            borderWidth: 2.5,
            tension: 0.3
          },
          {
            label: 'Local Island Guesthouse Beds',
            data: rows.map(r => r.guesthouse_beds),
            borderColor: colors.emerald,
            backgroundColor: 'rgba(16, 185, 129, 0.15)',
            fill: true,
            borderWidth: 2.5,
            tension: 0.3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: colors.text, boxWidth: 12 } }
        },
        scales: {
          x: { grid: { color: colors.grid }, ticks: { color: colors.text } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => formatNum(v) } }
        }
      }
    });
  }

  // Chart 12: Fish Catch
  function renderFishCatchChart() {
    const ctx = document.getElementById('chart-fish-catch');
    if (!ctx) return;
    if (state.charts.fish) state.charts.fish.destroy();

    const colors = getChartColors();
    const rows = state.data.timeline.filter(r => r.year >= 2000 && r.year <= 2026);

    state.charts.fish = new Chart(ctx, {
      type: 'line',
      data: {
        labels: rows.map(r => r.year),
        datasets: [{
          label: 'Total Marine Fish Catch (MT)',
          data: rows.map(r => r.fish_catch_mt),
          borderColor: colors.indigo,
          backgroundColor: 'rgba(99, 102, 241, 0.12)',
          fill: true,
          borderWidth: 2.5,
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: (item) => `${formatNum(Math.round(item.parsed.y))} MT` } }
        },
        scales: {
          x: { grid: { color: colors.grid }, ticks: { color: colors.text, maxTicksLimit: 12 } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => formatNum(v) } }
        }
      }
    });
  }

  // =========================================================================
  // GREATER MALÉ AREA CHARTS (Tri-Island Conurbation & Extreme Density)
  // =========================================================================
  function renderGreaterMaleCharts() {
    if (!state.data || !state.data.greater_male) return;

    renderGmPopulationShiftChart();
    renderGmDensityCompareChart();
    renderGmWaterPowerChart();
  }

  // Greater Malé Chart 1: Tri-Island Population Shift & Absorption (2000–2026)
  function renderGmPopulationShiftChart() {
    const ctx = document.getElementById('chart-gm-population-shift');
    if (!ctx) return;
    if (state.charts.gmShift) state.charts.gmShift.destroy();

    const colors = getChartColors();
    const timeline = state.data.greater_male.timeline;
    const labels = timeline.map(r => r.year);

    state.charts.gmShift = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Malé Island (Capital Core)',
            data: timeline.map(r => r.male_island_pop),
            backgroundColor: colors.accent,
            borderRadius: 2
          },
          {
            label: 'Hulhumalé (Reclaimed City)',
            data: timeline.map(r => r.hulhumale_pop),
            backgroundColor: colors.emerald,
            borderRadius: 2
          },
          {
            label: 'Villimalé (Eco Sanctuary)',
            data: timeline.map(r => r.vilingili_pop),
            backgroundColor: colors.amber,
            borderRadius: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            stacked: true,
            grid: { color: colors.grid },
            ticks: { color: colors.text, maxTicksLimit: 14 }
          },
          y: {
            stacked: true,
            grid: { color: colors.grid },
            ticks: { color: colors.text, callback: (v) => formatNum(v) }
          }
        },
        plugins: {
          legend: { position: 'top', labels: { color: colors.text, boxWidth: 12 } },
          tooltip: {
            callbacks: {
              label: (item) => `${item.dataset.label}: ${formatNum(item.parsed.y)} residents`
            }
          }
        }
      }
    });
  }

  // Greater Malé Chart 2: Global Extreme Density Benchmark
  function renderGmDensityCompareChart() {
    const ctx = document.getElementById('chart-gm-density-compare');
    if (!ctx) return;
    if (state.charts.gmDensity) state.charts.gmDensity.destroy();

    const colors = getChartColors();
    const benchmarkData = [
      { name: 'Malé Island (Capital Core)', density: 74879, highlight: true },
      { name: 'Manila, Philippines', density: 43000, highlight: false },
      { name: 'Greater Malé Total Conurbation', density: 33322, highlight: true },
      { name: 'Dhaka, Bangladesh', density: 30000, highlight: false },
      { name: 'Villimalé (Vilingili)', density: 28230, highlight: false },
      { name: 'Hulhumalé (Reclaimed)', density: 16799, highlight: false },
      { name: 'Singapore', density: 8300, highlight: false },
      { name: 'Tokyo (23 Special Wards)', density: 6400, highlight: false },
      { name: 'Outer Atolls Average', density: 1200, highlight: false }
    ];

    state.charts.gmDensity = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: benchmarkData.map(d => d.name),
        datasets: [{
          label: 'Persons per km²',
          data: benchmarkData.map(d => d.density),
          backgroundColor: benchmarkData.map(d => d.highlight ? colors.rose : (d.name.includes('Maldives') || d.name.includes('Malé') || d.name.includes('Villimalé') || d.name.includes('Hulhumalé') ? colors.accent : '#64748b')),
          borderRadius: 3
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (item) => `${formatNum(item.parsed.x)} persons / km²`
            }
          }
        },
        scales: {
          x: {
            grid: { color: colors.grid },
            ticks: { color: colors.text, callback: (v) => formatNum(v) }
          },
          y: {
            grid: { display: false },
            ticks: { color: colors.text, font: { size: 11 } }
          }
        }
      }
    });
  }

  // Greater Malé Chart 3: Desalinated Water & Electricity Lifeline Surge (2000–2026)
  function renderGmWaterPowerChart() {
    const ctx = document.getElementById('chart-gm-water-power');
    if (!ctx) return;
    if (state.charts.gmWater) state.charts.gmWater.destroy();

    const colors = getChartColors();
    const timeline = state.data.greater_male.timeline;
    const labels = timeline.map(r => r.year);

    state.charts.gmWater = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Desalinated Water Demand (\'000 Tons)',
            data: timeline.map(r => r.water_male_tons_k + r.water_hulhu_tons_k + r.water_vili_tons_k),
            borderColor: colors.accent,
            backgroundColor: colors.accentMuted,
            fill: true,
            yAxisID: 'y',
            tension: 0.35,
            borderWidth: 2.5
          },
          {
            label: 'STELCO Power Output (MWh)',
            data: timeline.map(r => r.electricity_mwh),
            borderColor: colors.amber,
            backgroundColor: 'transparent',
            borderDash: [4, 4],
            yAxisID: 'y1',
            tension: 0.35,
            borderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: colors.text, boxWidth: 12 } },
          tooltip: {
            callbacks: {
              label: (item) => `${item.dataset.label}: ${formatNum(item.parsed.y)}`
            }
          }
        },
        scales: {
          x: {
            grid: { color: colors.grid },
            ticks: { color: colors.text, maxTicksLimit: 14 }
          },
          y: {
            type: 'linear',
            position: 'left',
            title: { display: true, text: '\'000 Metric Tons Water', color: colors.text },
            grid: { color: colors.grid },
            ticks: { color: colors.text, callback: (v) => formatNum(v) }
          },
          y1: {
            type: 'linear',
            position: 'right',
            title: { display: true, text: 'MWh Electricity', color: colors.text },
            grid: { display: false },
            ticks: { color: colors.text, callback: (v) => formatNum(v) }
          }
        }
      }
    });
  }

  // =========================================================================
  // ANIMATED POPULATION PYRAMID (Tables 3.13, 3.14, 3.15, 3.2)
  // =========================================================================
  const pyramidState = {
    initialized: false,
    isPlaying: false,
    year: 2021,
    speed: 900,
    scope: 'national',      // 'national', 'male_city', 'atolls'
    subpop: 'Total',        // 'Total', 'Maldivian', 'Foreigner'
    mode: 'annual',         // 'annual' or 'census'
    loop: true,
    timer: null,
    data: null,
    chart: null
  };

  function renderDemographicsSection(demographics) {
    if (!demographics) return;
    pyramidState.data = demographics;

    const canvas = document.getElementById('pyramidChart');
    if (!canvas) return;

    if (!pyramidState.initialized) {
      setupPyramidEventListeners();
      pyramidState.initialized = true;
    }

    updatePyramidSliderTicks();
    updatePyramidUI(false);
  }

  function setupPyramidEventListeners() {
    const playBtn = document.getElementById('pyramid-play-btn');
    const prevBtn = document.getElementById('pyramid-prev-btn');
    const nextBtn = document.getElementById('pyramid-next-btn');
    const slider = document.getElementById('pyramid-range-slider');
    const loopChk = document.getElementById('pyramid-loop-chk');

    // Play / Pause
    playBtn?.addEventListener('click', togglePyramidPlayback);

    // Prev / Next Steps
    prevBtn?.addEventListener('click', () => stepPyramidYear(-1));
    nextBtn?.addEventListener('click', () => stepPyramidYear(1));

    // Range Slider
    slider?.addEventListener('input', (e) => {
      pausePyramidPlayback();
      pyramidState.year = parseInt(e.target.value, 10);
      updatePyramidUI(false);
    });

    // Loop toggle
    loopChk?.addEventListener('change', (e) => {
      pyramidState.loop = e.target.checked;
    });

    // Speed Pills
    const speedBtns = document.querySelectorAll('#pyramid-speed-pills .pill-btn');
    speedBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        speedBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        pyramidState.speed = parseInt(btn.getAttribute('data-speed'), 10) || 900;
        if (pyramidState.isPlaying) {
          clearInterval(pyramidState.timer);
          pyramidState.timer = setInterval(advancePyramidFrame, pyramidState.speed);
        }
      });
    });

    // Sub-population Pills (Total vs Maldivian vs Foreigner/Labourer)
    const subpopBtns = document.querySelectorAll('#pyramid-subpop-pills .pill-btn');
    subpopBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        subpopBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        pyramidState.subpop = btn.getAttribute('data-subpop') || 'Total';
        updatePyramidUI(false);
      });
    });

    // Scope Pills (National vs Malé City vs Atolls)
    const scopeBtns = document.querySelectorAll('#pyramid-scope-pills .pill-btn');
    scopeBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        scopeBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        pyramidState.scope = btn.getAttribute('data-scope') || 'national';
        updatePyramidUI(false);
      });
    });

    // Dataset Mode Pills (Annual vs Census)
    const modeBtns = document.querySelectorAll('#pyramid-mode-pills .pill-btn');
    modeBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        modeBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        pausePyramidPlayback();
        pyramidState.mode = btn.getAttribute('data-mode') || 'annual';

        const subpopWrap = document.getElementById('filter-subpop-wrap');
        const scopeWrap = document.getElementById('filter-scope-wrap');

        if (pyramidState.mode === 'census') {
          pyramidState.year = 2014;
          if (subpopWrap) subpopWrap.style.display = 'none';
          if (scopeWrap) scopeWrap.style.display = 'none';
        } else {
          pyramidState.year = 2021;
          if (subpopWrap) subpopWrap.style.display = 'flex';
          if (scopeWrap) scopeWrap.style.display = 'flex';
        }

        updatePyramidSliderTicks();
        updatePyramidUI(false);
      });
    });
  }

  function updatePyramidSliderTicks() {
    const slider = document.getElementById('pyramid-range-slider');
    const ticksContainer = document.getElementById('pyramid-slider-ticks');
    const milestonesContainer = document.getElementById('pyramid-milestones-container');
    if (!slider || !ticksContainer) return;

    if (pyramidState.mode === 'census') {
      const years = pyramidState.data.historical_census.years;
      slider.min = 1995;
      slider.max = 2014;
      slider.step = 1;
      slider.value = pyramidState.year;

      ticksContainer.innerHTML = years.map(y => `
        <span class="slider-tick-label ${y === pyramidState.year ? 'active' : ''}" data-year="${y}">${y}</span>
      `).join('');

      if (milestonesContainer) {
        milestonesContainer.innerHTML = `
          <span>Census:</span>
          <button type="button" class="btn-milestone ${pyramidState.year === 1995 ? 'active' : ''}" data-jump="1995">1995</button>
          <button type="button" class="btn-milestone ${pyramidState.year === 2000 ? 'active' : ''}" data-jump="2000">2000</button>
          <button type="button" class="btn-milestone ${pyramidState.year === 2006 ? 'active' : ''}" data-jump="2006">2006</button>
          <button type="button" class="btn-milestone ${pyramidState.year === 2014 ? 'active' : ''}" data-jump="2014">2014</button>
        `;
        milestonesContainer.querySelectorAll('.btn-milestone').forEach(b => {
          b.addEventListener('click', () => {
            pausePyramidPlayback();
            pyramidState.year = parseInt(b.getAttribute('data-jump'), 10);
            updatePyramidUI(false);
          });
        });
      }
    } else {
      slider.min = 2014;
      slider.max = 2030;
      slider.step = 1;
      slider.value = pyramidState.year;

      const displayTicks = [2014, 2016, 2018, 2020, 2022, 2024, 2026, 2028, 2030];
      ticksContainer.innerHTML = displayTicks.map(y => `
        <span class="slider-tick-label ${y === pyramidState.year ? 'active' : ''}" data-year="${y}">${y}</span>
      `).join('');

      if (milestonesContainer) {
        milestonesContainer.innerHTML = `
          <span>Jump:</span>
          <button type="button" class="btn-milestone ${pyramidState.year === 2014 ? 'active' : ''}" data-jump="2014">2014 Census</button>
          <button type="button" class="btn-milestone ${pyramidState.year === 2019 ? 'active' : ''}" data-jump="2019">2019 Pre-Covid</button>
          <button type="button" class="btn-milestone ${pyramidState.year === 2021 ? 'active' : ''}" data-jump="2021">2021 Yearbook</button>
          <button type="button" class="btn-milestone ${pyramidState.year === 2025 ? 'active' : ''}" data-jump="2025">2025 Mid</button>
          <button type="button" class="btn-milestone ${pyramidState.year === 2030 ? 'active' : ''}" data-jump="2030">2030 Horizon</button>
        `;
        milestonesContainer.querySelectorAll('.btn-milestone').forEach(b => {
          b.addEventListener('click', () => {
            pausePyramidPlayback();
            pyramidState.year = parseInt(b.getAttribute('data-jump'), 10);
            updatePyramidUI(false);
          });
        });
      }
    }

    ticksContainer.querySelectorAll('.slider-tick-label').forEach(t => {
      t.addEventListener('click', () => {
        pausePyramidPlayback();
        pyramidState.year = parseInt(t.getAttribute('data-year'), 10);
        updatePyramidUI(false);
      });
    });
  }

  function togglePyramidPlayback() {
    if (pyramidState.isPlaying) {
      pausePyramidPlayback();
    } else {
      startPyramidPlayback();
    }
  }

  function startPyramidPlayback() {
    if (!pyramidState.data) return;
    const years = pyramidState.mode === 'annual'
      ? pyramidState.data.years
      : pyramidState.data.historical_census.years;

    if (pyramidState.year >= years[years.length - 1]) {
      pyramidState.year = years[0];
      updatePyramidUI(true);
    }

    pyramidState.isPlaying = true;
    updatePlayButtonUI();

    clearInterval(pyramidState.timer);
    pyramidState.timer = setInterval(advancePyramidFrame, pyramidState.speed);
  }

  function pausePyramidPlayback() {
    pyramidState.isPlaying = false;
    clearInterval(pyramidState.timer);
    pyramidState.timer = null;
    updatePlayButtonUI();
  }

  function updatePlayButtonUI() {
    const playBtn = document.getElementById('pyramid-play-btn');
    const playText = document.getElementById('pyramid-play-text');
    const playIcon = document.getElementById('pyramid-play-icon');
    if (!playBtn) return;

    if (pyramidState.isPlaying) {
      playBtn.classList.add('playing');
      if (playText) playText.textContent = 'Pause Timeline';
      if (playIcon) {
        playIcon.innerHTML = '<rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect>';
      }
    } else {
      playBtn.classList.remove('playing');
      if (playText) playText.textContent = 'Play Timeline';
      if (playIcon) {
        playIcon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"></polygon>';
      }
    }
  }

  function advancePyramidFrame() {
    const years = pyramidState.mode === 'annual'
      ? pyramidState.data.years
      : pyramidState.data.historical_census.years;

    const currentIdx = years.indexOf(pyramidState.year);
    if (currentIdx === -1 || currentIdx >= years.length - 1) {
      if (pyramidState.loop) {
        pyramidState.year = years[0];
      } else {
        pausePyramidPlayback();
        return;
      }
    } else {
      pyramidState.year = years[currentIdx + 1];
    }

    updatePyramidUI(true);
  }

  function stepPyramidYear(delta) {
    pausePyramidPlayback();
    const years = pyramidState.mode === 'annual'
      ? pyramidState.data.years
      : pyramidState.data.historical_census.years;

    const currentIdx = years.indexOf(pyramidState.year);
    const targetIdx = Math.max(0, Math.min(years.length - 1, (currentIdx === -1 ? 0 : currentIdx) + delta));
    pyramidState.year = years[targetIdx];
    updatePyramidUI(false);
  }

  function updatePyramidUI(isSmooth) {
    if (!pyramidState.data) return;

    const isAnnual = pyramidState.mode === 'annual';
    const ageGroups = pyramidState.data.age_groups;
    let yearData = null;
    let maxCohortScale = 10000;

    if (isAnnual) {
      const scopeData = pyramidState.data.scopes[pyramidState.scope];
      if (!scopeData || !scopeData[pyramidState.subpop]) return;
      const series = scopeData[pyramidState.subpop];

      const validYears = pyramidState.data.years;
      if (!validYears.includes(pyramidState.year)) {
        pyramidState.year = 2021;
      }

      yearData = series.by_year[pyramidState.year];

      // Calculate peak cohort size for scale stability
      let peak = 0;
      for (const y of validYears) {
        const e = series.by_year[y];
        if (e) {
          peak = Math.max(peak, Math.max(...e.male), Math.max(...e.female));
        }
      }
      maxCohortScale = Math.ceil(peak * 1.08);
    } else {
      const census = pyramidState.data.historical_census;
      const validYears = census.years;
      if (!validYears.includes(pyramidState.year)) {
        pyramidState.year = validYears.reduce((prev, curr) => Math.abs(curr - pyramidState.year) < Math.abs(prev - pyramidState.year) ? curr : prev);
      }
      yearData = census.by_year[pyramidState.year];
      let peak = 0;
      for (const y of validYears) {
        const e = census.by_year[y];
        if (e) peak = Math.max(peak, Math.max(...e.male), Math.max(...e.female));
      }
      maxCohortScale = Math.ceil(peak * 1.08);
    }

    if (!yearData) return;

    // Update Slider & Active Milestones
    const slider = document.getElementById('pyramid-range-slider');
    if (slider && parseInt(slider.value, 10) !== pyramidState.year) {
      slider.value = pyramidState.year;
    }

    document.querySelectorAll('#pyramid-milestones-container .btn-milestone').forEach(b => {
      const jumpY = parseInt(b.getAttribute('data-jump'), 10);
      b.classList.toggle('active', jumpY === pyramidState.year);
    });

    document.querySelectorAll('#pyramid-slider-ticks .slider-tick-label').forEach(t => {
      const tickY = parseInt(t.getAttribute('data-year'), 10);
      t.classList.toggle('active', tickY === pyramidState.year);
    });

    // Update Live Indicator Ribbon
    const indTotal = document.getElementById('pyramid-ind-total');
    const indMedian = document.getElementById('pyramid-ind-median');
    const indSexratio = document.getElementById('pyramid-ind-sexratio');
    const indDependency = document.getElementById('pyramid-ind-dependency');
    const indWorking = document.getElementById('pyramid-ind-working');

    const ind = yearData.indicators || {};
    if (indTotal) indTotal.textContent = formatNum(ind.total || 0);
    if (indMedian) indMedian.textContent = ind.median_age != null ? `${ind.median_age} yrs` : '—';
    if (indSexratio) indSexratio.textContent = ind.sex_ratio != null ? `${ind.sex_ratio} M/100F` : '—';
    if (indDependency) indDependency.textContent = ind.dependency_ratio != null ? ind.dependency_ratio.toFixed(1) : '—';
    const workingPct = ind.working_pct != null ? ind.working_pct : ind.working_age_pct;
    if (indWorking) indWorking.textContent = workingPct != null ? `${Number(workingPct).toFixed(1)}%` : '—';

    // Update Legend Totals
    const totalMale = yearData.male.reduce((a, b) => a + b, 0);
    const totalFemale = yearData.female.reduce((a, b) => a + b, 0);
    const legendMale = document.getElementById('pyramid-legend-male-count');
    const legendFemale = document.getElementById('pyramid-legend-female-count');
    if (legendMale) legendMale.textContent = `${formatNum(totalMale)} (${((totalMale / (totalMale + totalFemale || 1)) * 100).toFixed(1)}%)`;
    if (legendFemale) legendFemale.textContent = `${formatNum(totalFemale)} (${((totalFemale / (totalMale + totalFemale || 1)) * 100).toFixed(1)}%)`;

    // Render / Update Chart.js Bilateral Canvas
    const canvas = document.getElementById('pyramidChart');
    if (!canvas) return;

    const colors = getChartColors();
    const maleNegativeData = yearData.male.map(v => -v);
    const femaleData = yearData.female;

    if (pyramidState.chart) {
      pyramidState.chart.data.labels = ageGroups;
      pyramidState.chart.data.datasets[0].data = maleNegativeData;
      pyramidState.chart.data.datasets[1].data = femaleData;
      pyramidState.chart.options.scales.x.min = -maxCohortScale;
      pyramidState.chart.options.scales.x.max = maxCohortScale;
      pyramidState.chart.update(isSmooth ? 'none' : 'active');
    } else {
      pyramidState.chart = new Chart(canvas, {
        type: 'bar',
        data: {
          labels: ageGroups,
          datasets: [
            {
              label: 'Male',
              data: maleNegativeData,
              backgroundColor: '#0ea5e9',
              borderRadius: 3,
              barPercentage: 0.88,
              categoryPercentage: 0.95
            },
            {
              label: 'Female',
              data: femaleData,
              backgroundColor: '#f43f5e',
              borderRadius: 3,
              barPercentage: 0.88,
              categoryPercentage: 0.95
            }
          ]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          animation: { duration: 320 },
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (item) => `${item.dataset.label}: ${formatNum(Math.abs(item.parsed.x))} persons`
              }
            }
          },
          scales: {
            x: {
              min: -maxCohortScale,
              max: maxCohortScale,
              grid: { color: colors.grid },
              ticks: {
                color: colors.text,
                callback: (v) => formatNum(Math.abs(v))
              }
            },
            y: {
              grid: { display: false },
              ticks: { color: colors.text, font: { size: 11, family: 'Inter' } }
            }
          }
        }
      });
    }
  }

  // =========================================================================
  // ANIMATED EXPATRIATE LABOR FORCE BY COUNTRY OF ORIGIN (2008–2026)
  // =========================================================================
  const expatLaborState = {
    initialized: false,
    isPlaying: false,
    year: 2026,
    timer: null,
    chart: null
  };

  function renderExpatLaborSection() {
    if (!state.data || !state.data.expat_timeline) return;

    if (!expatLaborState.initialized) {
      setupExpatEventListeners();
      expatLaborState.initialized = true;
    }

    updateExpatUI(expatLaborState.year);
  }

  function setupExpatEventListeners() {
    const playBtn = document.getElementById('expat-play-btn');
    const slider = document.getElementById('expat-range-slider');

    playBtn?.addEventListener('click', toggleExpatPlayback);

    slider?.addEventListener('input', (e) => {
      pauseExpatPlayback();
      const yr = parseInt(e.target.value, 10);
      expatLaborState.year = yr;
      updateExpatUI(yr);
    });
  }

  function toggleExpatPlayback() {
    if (expatLaborState.isPlaying) {
      pauseExpatPlayback();
    } else {
      startExpatPlayback();
    }
  }

  function startExpatPlayback() {
    if (!state.data.expat_timeline) return;
    if (expatLaborState.year >= 2026) expatLaborState.year = 2008;

    expatLaborState.isPlaying = true;
    const playBtn = document.getElementById('expat-play-btn');
    const playText = document.getElementById('expat-play-text');
    const playIcon = document.getElementById('expat-play-icon');
    if (playBtn) playBtn.classList.add('playing');
    if (playText) playText.textContent = 'Pause Timeline';
    if (playIcon) playIcon.innerHTML = '<rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect>';

    clearInterval(expatLaborState.timer);
    expatLaborState.timer = setInterval(advanceExpatFrame, 850);
  }

  function pauseExpatPlayback() {
    expatLaborState.isPlaying = false;
    clearInterval(expatLaborState.timer);
    expatLaborState.timer = null;

    const playBtn = document.getElementById('expat-play-btn');
    const playText = document.getElementById('expat-play-text');
    const playIcon = document.getElementById('expat-play-icon');
    if (playBtn) playBtn.classList.remove('playing');
    if (playText) playText.textContent = 'Play Timeline';
    if (playIcon) playIcon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"></polygon>';
  }

  function advanceExpatFrame() {
    if (expatLaborState.year >= 2026) {
      expatLaborState.year = 2008;
    } else {
      expatLaborState.year += 1;
    }
    updateExpatUI(expatLaborState.year);
  }

  function updateExpatUI(year) {
    if (!state.data || !state.data.expat_timeline || !state.data.expat_timeline.length) return;
    const row = state.data.expat_timeline.find(r => r.year === year) || state.data.expat_timeline.find(r => r.year === Math.min(Math.max(year, 2008), 2026)) || state.data.expat_timeline[0];

    const slider = document.getElementById('expat-range-slider');
    if (slider) slider.value = row.year;

    const tickerYr = document.getElementById('expat-ticker-year');
    const tickerTotal = document.getElementById('expat-ticker-total');
    if (tickerYr) tickerYr.textContent = row.year;
    if (tickerTotal) tickerTotal.textContent = formatNum(row.total);

    const canvas = document.getElementById('chart-expat-animated');
    if (!canvas) return;

    const colors = getChartColors();
    const nationalities = [
      { name: 'Bangladesh', count: row.bangladesh, color: '#0ea5e9' },
      { name: 'India', count: row.india, color: '#10b981' },
      { name: 'Sri Lanka', count: row.sri_lanka, color: '#f59e0b' },
      { name: 'Nepal', count: row.nepal, color: '#6366f1' },
      { name: 'Philippines', count: row.philippines, color: '#f43f5e' },
      { name: 'Others', count: row.others, color: '#64748b' }
    ];

    if (expatLaborState.chart) {
      expatLaborState.chart.data.labels = nationalities.map(n => n.name);
      expatLaborState.chart.data.datasets[0].data = nationalities.map(n => n.count);
      expatLaborState.chart.data.datasets[0].backgroundColor = nationalities.map(n => n.color);
      expatLaborState.chart.update('none');
    } else {
      expatLaborState.chart = new Chart(canvas, {
        type: 'bar',
        data: {
          labels: nationalities.map(n => n.name),
          datasets: [{
            label: 'Registered Expatriate Workers',
            data: nationalities.map(n => n.count),
            backgroundColor: nationalities.map(n => n.color),
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (item) => `${formatNum(item.parsed.y)} workers (${((item.parsed.y / row.total) * 100).toFixed(1)}% of foreign labor)`
              }
            }
          },
          scales: {
            x: {
              grid: { color: colors.grid },
              ticks: { color: colors.text, font: { weight: '600' } }
            },
            y: {
              grid: { color: colors.grid },
              ticks: { color: colors.text, callback: (v) => formatNum(v) },
              max: 130000
            }
          }
        }
      });
    }
  }

  // Chart 17: Energy Transition (Diesel vs Solar)
  function renderEnergyTransitionChart() {
    const ctx = document.getElementById('chart-energy-transition');
    if (!ctx) return;
    if (state.charts.energyTrans) state.charts.energyTrans.destroy();

    const colors = getChartColors();
    const energy = state.data.sub_lifelines;

    state.charts.energyTrans = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: energy.diesel_years,
        datasets: [
          {
            type: 'bar',
            label: 'Diesel Burned (Million Liters)',
            data: energy.diesel_consumption_liters_m,
            backgroundColor: colors.rose,
            yAxisID: 'y',
            borderRadius: 3
          },
          {
            type: 'line',
            label: 'Installed Solar PV Capacity (MW)',
            data: energy.solar_installed_mw,
            borderColor: colors.amber,
            backgroundColor: 'transparent',
            borderWidth: 3,
            yAxisID: 'y1',
            tension: 0.3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: colors.text, boxWidth: 12 } }
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: colors.text } },
          y: {
            type: 'linear',
            position: 'left',
            grid: { color: colors.grid },
            ticks: { color: colors.text, callback: (v) => `${v}M L` }
          },
          y1: {
            type: 'linear',
            position: 'right',
            grid: { display: false },
            ticks: { color: colors.amber, callback: (v) => `${v} MW` }
          }
        }
      }
    });
  }

  // Chart 18: Emergency Water Stress
  function renderWaterEmergencyChart() {
    const ctx = document.getElementById('chart-water-emergency');
    if (!ctx) return;
    if (state.charts.waterEmerg) state.charts.waterEmerg.destroy();

    const colors = getChartColors();
    const rows = state.data.sub_lifelines.emergency_water_islands;

    state.charts.waterEmerg = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: rows.map(r => r.year),
        datasets: [{
          label: 'Islands Requiring Emergency Maritime Water Delivery',
          data: rows.map(r => r.islands),
          backgroundColor: colors.accent,
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: (item) => `${item.parsed.y} outer islands supplied` } }
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: colors.text } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text } }
        }
      }
    });
  }

  // Chart 19: Crime Types
  function renderCrimeTypesChart() {
    const ctx = document.getElementById('chart-crime-types');
    if (!ctx) return;
    if (state.charts.crime) state.charts.crime.destroy();

    const colors = getChartColors();
    const crimes = state.data.sub_society.reported_crime_categories_2023;

    state.charts.crime = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: crimes.map(c => c.category),
        datasets: [{
          label: 'Reported Cases',
          data: crimes.map(c => c.cases),
          backgroundColor: colors.rose,
          borderRadius: 3
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: (item) => `${formatNum(item.parsed.x)} cases (${crimes[item.dataIndex].pct}%)` } }
        },
        scales: {
          x: { grid: { color: colors.grid }, ticks: { color: colors.text } },
          y: { grid: { display: false }, ticks: { color: colors.text } }
        }
      }
    });
  }

  // Chart 20: Election Turnout
  function renderElectionTurnoutChart() {
    const ctx = document.getElementById('chart-election-turnout');
    if (!ctx) return;
    if (state.charts.elections) state.charts.elections.destroy();

    const colors = getChartColors();
    const elections = state.data.sub_society.elections_turnout;

    state.charts.elections = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: elections.map(e => e.election),
        datasets: [{
          label: 'Voter Turnout (%)',
          data: elections.map(e => e.turnout_pct),
          backgroundColor: colors.emerald,
          borderRadius: 3
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: (item) => `Turnout: ${item.parsed.x}% (${formatNum(elections[item.dataIndex].registered_voters)} voters)` } }
        },
        scales: {
          x: { min: 50, max: 100, grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => `${v}%` } },
          y: { grid: { display: false }, ticks: { color: colors.text } }
        }
      }
    });
  }

  // Chart 21: Education Stages
  function renderEducationStagesChart() {
    const ctx = document.getElementById('chart-education-stages');
    if (!ctx) return;
    if (state.charts.education) state.charts.education.destroy();

    const colors = getChartColors();
    const edu = state.data.sub_society.education_students_by_stage;

    state.charts.education = new Chart(ctx, {
      type: 'line',
      data: {
        labels: edu.map(e => e.year),
        datasets: [
          {
            label: 'Primary (Grades 1 - 7)',
            data: edu.map(e => e.primary),
            borderColor: colors.accent,
            borderWidth: 2.5,
            tension: 0.3
          },
          {
            label: 'Lower Secondary (Grades 8 - 10)',
            data: edu.map(e => e.lower_sec),
            borderColor: colors.emerald,
            borderWidth: 2.5,
            tension: 0.3
          },
          {
            label: 'Higher Secondary (Grades 11 - 12)',
            data: edu.map(e => e.higher_sec),
            borderColor: colors.amber,
            borderWidth: 2.5,
            tension: 0.3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: colors.text, boxWidth: 12 } }
        },
        scales: {
          x: { grid: { color: colors.grid }, ticks: { color: colors.text } },
          y: { grid: { color: colors.grid }, ticks: { color: colors.text, callback: (v) => formatNum(v) } }
        }
      }
    });
  }

  // =========================================================================
  // 8. MASTER CATALOG SEARCH STUDIO
  // =========================================================================
  function setupCatalog() {
    if (!els.catalogInput) return;

    els.catalogInput.addEventListener('input', (e) => {
      state.catalogQuery = e.target.value.toLowerCase().trim();
      state.catalogPage = 1;
      if (els.clearSearchBtn) {
        els.clearSearchBtn.style.display = state.catalogQuery ? 'block' : 'none';
      }
      renderCatalogTable();
    });

    if (els.clearSearchBtn) {
      els.clearSearchBtn.addEventListener('click', () => {
        els.catalogInput.value = '';
        state.catalogQuery = '';
        els.clearSearchBtn.style.display = 'none';
        state.catalogPage = 1;
        renderCatalogTable();
      });
    }

    els.filterPills.forEach(pill => {
      pill.addEventListener('click', () => {
        els.filterPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.catalogCategory = pill.getAttribute('data-cat');
        state.catalogPage = 1;
        renderCatalogTable();
      });
    });

    if (els.pagePrevBtn) {
      els.pagePrevBtn.addEventListener('click', () => {
        if (state.catalogPage > 1) {
          state.catalogPage--;
          renderCatalogTable();
        }
      });
    }

    if (els.pageNextBtn) {
      els.pageNextBtn.addEventListener('click', () => {
        state.catalogPage++;
        renderCatalogTable();
      });
    }

    renderCatalogTable();
  }

  function renderCatalogTable() {
    if (!state.data || !state.data.catalog || !els.catalogTableBody) return;

    const filtered = state.data.catalog.filter(item => {
      if (state.catalogCategory !== 'all') {
        if (!item.category.toLowerCase().includes(state.catalogCategory.toLowerCase())) {
          return false;
        }
      }
      if (state.catalogQuery) {
        const titleMatch = item.title.toLowerCase().includes(state.catalogQuery);
        const catMatch = item.category.toLowerCase().includes(state.catalogQuery);
        const idMatch = item.table_id.toLowerCase().includes(state.catalogQuery);
        if (!titleMatch && !catMatch && !idMatch) return false;
      }
      return true;
    });

    if (els.catalogVisibleCount) {
      els.catalogVisibleCount.textContent = formatNum(filtered.length);
    }

    const totalPages = Math.ceil(filtered.length / state.catalogPageSize) || 1;
    if (state.catalogPage > totalPages) state.catalogPage = totalPages;

    const startIndex = (state.catalogPage - 1) * state.catalogPageSize;
    const pageItems = filtered.slice(startIndex, startIndex + state.catalogPageSize);

    els.catalogTableBody.innerHTML = pageItems.map(item => `
      <tr>
        <td><span class="table-id-pill">${item.table_id}</span></td>
        <td><span class="font-medium">${item.category}</span></td>
        <td>${item.title || 'Statistical Table'}</td>
        <td class="font-mono text-muted">${item.min_year ? `${item.min_year} – ${item.max_year}` : 'Multi-Year'}</td>
        <td class="font-mono">${formatNum(item.rows)}</td>
        <td>
          <a href="${item.csv_path}" download class="btn-csv-link" title="Download harmonized CSV">
            <span>CSV</span> ⬇
          </a>
        </td>
      </tr>
    `).join('');

    if (els.pageIndicator) {
      els.pageIndicator.textContent = `Page ${state.catalogPage} of ${totalPages}`;
    }
    if (els.pagePrevBtn) {
      els.pagePrevBtn.disabled = state.catalogPage <= 1;
    }
    if (els.pageNextBtn) {
      els.pageNextBtn.disabled = state.catalogPage >= totalPages;
    }
  }

  // =========================================================================
  // BOOTSTRAP
  // =========================================================================
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
