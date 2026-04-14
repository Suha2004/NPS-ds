const COORDS = [
  { lat: 12.9716, lng: 77.6079 }, { lat: 12.9352, lng: 77.6245 },
  { lat: 13.0827, lng: 80.2707 }, { lat: 19.0760, lng: 72.8777 },
  { lat: 28.6139, lng: 77.2090 }, { lat: 17.3850, lng: 78.4867 },
  { lat: 22.5726, lng: 88.3639 }, { lat: 12.2958, lng: 76.6394 },
  { lat: 15.3173, lng: 75.7139 }, { lat: 26.9124, lng: 75.7873 },
];

const SIGNALS = [
  { dbm: -58,  type: '5G', label: 'Excellent Signal', tier: 'good', bars: 5, upi: 'High – 96%',   badge: 'Low Risk'    },
  { dbm: -65,  type: '5G', label: 'Excellent Signal', tier: 'good', bars: 5, upi: 'High – 91%',   badge: 'Low Risk'    },
  { dbm: -72,  type: '4G', label: 'Good Signal',      tier: 'good', bars: 4, upi: 'High – 84%',   badge: 'Low Risk'    },
  { dbm: -80,  type: '4G', label: 'Good Signal',      tier: 'good', bars: 3, upi: 'Medium – 72%', badge: 'Low Risk'    },
  { dbm: -88,  type: '4G', label: 'Moderate Signal',  tier: 'mid',  bars: 3, upi: 'Medium – 61%', badge: 'Medium Risk' },
  { dbm: -95,  type: '3G', label: 'Moderate Signal',  tier: 'mid',  bars: 2, upi: 'Medium – 48%', badge: 'Medium Risk' },
  { dbm: -102, type: '4G', label: 'Poor Signal',      tier: 'poor', bars: 1, upi: 'Low – 32%',    badge: 'High Risk'   },
  { dbm: -110, type: '4G', label: 'Poor Signal',      tier: 'poor', bars: 1, upi: 'Low – 28%',    badge: 'High Risk'   },
  { dbm: -115, type: '2G', label: 'Very Poor Signal', tier: 'poor', bars: 1, upi: 'Low – 14%',    badge: 'High Risk'   },
];

const RECS = {
  good: [
    { icon: '📱', text: '<strong>Use Airtel / Jio</strong> — network is stable and fast' },
    { icon: '✅', text: '<strong>Safe to proceed</strong> with UPI payments now' },
    { icon: '⚡', text: '<strong>Fast transactions</strong> expected under 5 seconds' },
    { icon: '🔒', text: '<strong>Low risk</strong> of payment failure or timeout' },
  ],
  mid: [
    { icon: '🔄', text: '<strong>Switch to Jio</strong> for better network stability' },
    { icon: '⏱️', text: '<strong>Wait 10–15 minutes</strong> and retry the payment' },
    { icon: '💵', text: '<strong>Carry Cash as Backup</strong> in case payment fails' },
  ],
  poor: [
    { icon: '🔄', text: '<strong>Switch to Vi / BSNL</strong> for better coverage here' },
    { icon: '⏱️', text: '<strong>Wait 10–15 minutes</strong> and retry the payment' },
    { icon: '💵', text: '<strong>Carry Cash as Backup</strong> — payments likely to fail' },
  ],
};

let currentSig = null;
let recents = JSON.parse(localStorage.getItem('nps_recents') || '[]');

function hash(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) >>> 0;
  return h;
}

function runCheck() {
  const raw = document.getElementById('loc-input').value.trim();
  if (!raw) { shake(document.getElementById('loc-input')); return; }

  const btn = document.getElementById('check-btn');
  btn.textContent = 'Checking…';
  btn.disabled = true;

  // Go to analyzing screen
  goStep(2);
  runAnalyzing(raw, btn);
}

async function runAnalyzing(raw, btn) {
  const steps = ['a1','a2', 'a3', 'a4'];
  const delays = [600, 1200, 1900, 2600];

  steps.forEach((id, i) => {
    setTimeout(() => {
      document.getElementById(id).classList.add('done');
    }, delays[i]);
  });

  try {
    // 1. Fetch real coordinates from Geocoder (Photon by Komoot - more fuzzy/forgiving)
    let coords = { lat: 12.9716, lng: 77.6079 }; // Default: MG Road, Bangalore
    let found = false;

    async function tryGeocode(query) {
      try {
        const res = await fetch(`https://photon.komoot.io/api?q=${encodeURIComponent(query)}&limit=1`);
        const data = await res.json();
        if (data.features && data.features.length > 0) {
          const f = data.features[0].geometry.coordinates;
          return { lat: f[1], lng: f[0] };
        }
      } catch (e) { console.error("Geocode error:", e); }
      return null;
    }

    // Attempt 1: Full Query (biased to Karnataka)
    let res = await tryGeocode(`${raw}, Karnataka`);
    
    // Attempt 2: Fallback - Remove descriptive words like "Lake", "Park" if first fail
    if (!res) {
        const cleanRaw = raw.replace(/\b(lake|park|garden|road|street|st|rd)\b/gi, '').trim();
        if (cleanRaw !== raw) {
            res = await tryGeocode(cleanRaw + ", Karnataka");
        }
    }

    if (res) {
      coords = res;
      found = true;
      console.log("Geocoded:", raw, "to", coords);
    } else {
      console.warn("Could not geocode", raw, "- using default Bangalore coordinates.");
    }

    // 2. Fetch real prediction from backend
    const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            lat: coords.lat, 
            lon: coords.lng,
            rsrp: -90, 
            rsrq: -12
        })
    });

    if (!response.ok) throw new Error("Backend Error");
    const data = await response.json();

    // 3. Wrap result
    currentSig = {
      tier: data.tier,
      bars: data.bars,
      dbm: data.dbm,
      label: data.label,
      upi: data.upi,
      badge: data.badge,
      type: data.type
    };

    const resultCoords = { lat: data.lat, lng: data.lon };

    // 4. Populate UI
    setTimeout(() => {
        document.getElementById('loc-name').textContent = found ? raw : raw + " (Estimated)";
        document.getElementById('loc-coords').textContent = `${resultCoords.lat}, ${resultCoords.lng}`;
        populateSignal(currentSig);
        populateRecs(currentSig.tier);

        saveRecent(raw, resultCoords, currentSig);

        btn.textContent = 'Check';
        btn.disabled = false;
        goStep(3);
    }, 3200);

  } catch (err) {
    console.error(err);
    alert("ML Server Error. Please ensure the backend is running.");
    goStep(1);
    btn.textContent = 'Check';
    btn.disabled = false;
  }
}

function populateSignal(sig) {
  const qEl = document.getElementById('sig-quality');
  qEl.textContent = sig.label;
  qEl.className = `signal-quality ${sig.tier}`;
  document.getElementById('sig-dbm').textContent = `${sig.dbm} dBm (${sig.type})`;

  const upiVal = document.getElementById('upi-value');
  upiVal.textContent = sig.upi;
  upiVal.className = `upi-value ${sig.tier}`;

  const upiWrap = document.getElementById('upi-icon-wrap');
  upiWrap.className = `upi-icon-wrap ${sig.tier}`;
  document.getElementById('upi-icon').textContent = sig.tier === 'good' ? '✅' : sig.tier === 'mid' ? '⚠️' : '🚨';

  const badge = document.getElementById('upi-badge');
  badge.textContent = sig.badge;
  badge.className = `upi-badge ${sig.tier}`;
}

function populateRecs(tier) {
  const list = document.getElementById('rec-list');
  list.innerHTML = '';
  RECS[tier].forEach(r => {
    const li = document.createElement('li');
    li.innerHTML = `<div class="rec-icon-box">${r.icon}</div><span>${r.text}</span>`;
    list.appendChild(li);
  });
}

function saveRecent(name, coords, sig) {
  // Remove duplicate
  recents = recents.filter(r => r.name.toLowerCase() !== name.toLowerCase());
  recents.unshift({ name, lat: coords.lat, lng: coords.lng, tier: sig.tier, badge: sig.badge });
  if (recents.length > 5) recents = recents.slice(0, 5);
  localStorage.setItem('nps_recents', JSON.stringify(recents));
  renderRecents();
}

function renderRecents() {
  const section = document.getElementById('recents-section');
  const list = document.getElementById('recents-list');
  if (recents.length === 0) { section.classList.add('hidden'); return; }
  section.classList.remove('hidden');
  list.innerHTML = '';
  recents.forEach(r => {
    const div = document.createElement('div');
    div.className = 'recent-item fade-in';
    div.innerHTML = `
      <div class="recent-left">
        <span class="recent-icon">📍</span>
        <div>
          <p class="recent-name">${r.name}</p>
          <p class="recent-coords">${r.lat}, ${r.lng}</p>
        </div>
      </div>
      <span class="recent-badge ${r.tier}">${r.badge}</span>`;
    div.onclick = () => {
      document.getElementById('loc-input').value = r.name;
      runCheck();
    };
    list.appendChild(div);
  });
}

function goStep(step) {
  document.querySelectorAll('.step-panel').forEach(p => p.classList.add('hidden'));
  const panel = document.getElementById(`panel-${step}`);
  panel.classList.remove('hidden');
  panel.classList.add('fade-in');

  if (step === 2) resetAnalyzingSteps();
  if (step === 3 && currentSig) animateBars(currentSig.bars, currentSig.tier);

  document.querySelector('.main').scrollTop = 0;
}

function resetAnalyzingSteps() {
  ['a1','a2','a3','a4'].forEach(id => document.getElementById(id).classList.remove('done'));
}

function animateBars(count, tier) {
  const cols = document.querySelectorAll('.bar-col');
  cols.forEach(col => { col.className = 'bar-col'; });
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      cols.forEach((col, i) => {
        if (i < count) setTimeout(() => col.classList.add('lit', tier), i * 100);
      });
    });
  });
}

function submitFeedback(choice) {
  document.getElementById('feedback-btns').classList.add('hidden');
  document.getElementById('back-from-5').classList.add('hidden');
  const thanks = document.getElementById('feedback-thanks');
  thanks.classList.remove('hidden');
  document.getElementById('thanks-text').textContent = choice === 'yes'
    ? '🎉 Great! Glad the payment went through successfully.'
    : '🙏 Sorry to hear that. Try switching your SIM or moving to a better signal area.';
}

function resetApp() {
  document.getElementById('loc-input').value = '';
  document.getElementById('feedback-btns').classList.remove('hidden');
  document.getElementById('feedback-thanks').classList.add('hidden');
  document.getElementById('back-from-5').classList.remove('hidden');
  currentSig = null;
  goStep(1);
}

function reveal(id) {
  const el = document.getElementById(id);
  el.classList.remove('hidden');
  void el.offsetWidth;
  el.classList.add('fade-in');
}

function shake(el) {
  el.style.animation = 'none';
  void el.offsetWidth;
  el.style.animation = 'shake 0.35s ease';
  el.addEventListener('animationend', () => el.style.animation = '', { once: true });
}

document.getElementById('loc-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') runCheck();
});

// Load recents on start
renderRecents();
