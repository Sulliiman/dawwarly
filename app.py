from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

DATA_URL = "https://mazad.absher.sa/portal/auction-dashboard/data/MVPData.json"
AUCTION_URL = "https://mazad.absher.sa/portal/auction-dashboard/"

PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">
<title>دور لي — بحث لوحات مزاد أبشر</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root{
    --asphalt: #23211E;
    --steel: #34312B;
    --plate: #EDEAE1;
    --amber: #E8A33D;
    --rust: #B4532A;
    --ink: #201F1C;
    --paper: #F3F0E8;
    --line: rgba(237,234,225,0.14);
    --font-ar: 'IBM Plex Sans Arabic', sans-serif;
    --font-num: 'IBM Plex Sans Arabic', sans-serif;
  }

  *{ box-sizing: border-box; }
  html{ scroll-behavior: smooth; }
  body{
    margin:0;
    background: var(--asphalt);
    background-image:
      radial-gradient(ellipse at 15% -10%, rgba(232,163,61,0.08), transparent 45%),
      repeating-linear-gradient(0deg, rgba(255,255,255,0.015) 0px, rgba(255,255,255,0.015) 1px, transparent 1px, transparent 3px);
    color: var(--paper);
    font-family: var(--font-ar);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    min-height: 100vh;
  }

  a{ color: inherit; }
  button{ font-family: inherit; cursor: pointer; }
  :focus-visible{ outline: 2px solid var(--amber); outline-offset: 3px; }

  .wrap{ max-width: 900px; margin: 0 auto; padding-left: 24px; padding-right: 24px; }

  /* ---------- Header ---------- */
  header{ padding: 26px 0 20px; border-bottom: 1px solid var(--line); }
  header .wrap{ display:flex; align-items:center; justify-content:space-between; gap: 24px; }
  .logo{
    font-family: var(--font-ar); font-weight: 700; font-size: 21px;
    letter-spacing: 0.3px; display:flex; align-items:center; gap:9px;
    text-decoration: none;
  }
  .logo .dot{ width:8px; height:8px; border-radius:50%; background: var(--amber); display:inline-block; }
  nav a{
    font-size: 15px; color: rgba(243,240,232,0.72); text-decoration:none;
    transition: color .15s ease;
  }
  nav a:hover{ color: var(--paper); }

  /* ---------- Hero ---------- */
  .hero{ padding-top: 64px; padding-bottom: 12px; text-align:center; }
  .hero h1{
    font-size: clamp(28px, 4.4vw, 42px);
    font-weight: 700; line-height: 1.3; margin: 0 0 14px;
  }
  .hero p.lede{
    font-size: 16px; color: rgba(243,240,232,0.7);
    max-width: 46ch; margin: 0 auto 36px;
  }

  .search-rig{
    background: var(--steel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 20px;
    max-width: 560px;
    margin: 0 auto;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04), 0 20px 40px -24px rgba(0,0,0,0.6);
  }
  .search-fields{
    display:flex;
    gap: 12px;
    margin-bottom: 14px;
  }
  .field{ flex:1; text-align: right; }
  .field label{
    display:block; font-size: 12.5px; color: rgba(243,240,232,0.5);
    margin-bottom: 6px; font-weight: 500;
  }
  .input-wrap{ position:relative; display:flex; align-items:center; }
  .input-wrap input{
    width:100%;
    background: var(--asphalt);
    border: 1px solid transparent;
    border-radius: 8px;
    color: var(--paper);
    font-family: var(--font-ar);
    font-size: 15px;
    padding: 13px 34px 13px 14px;
  }
  .input-wrap input::placeholder{ color: rgba(243,240,232,0.35); }
  .input-wrap input:focus{ outline:none; border-color: rgba(232,163,61,0.5); }
  .clear-btn{
    position:absolute; right: 8px; border:none;
    background: rgba(255,255,255,0.08);
    color: rgba(243,240,232,0.75); font-size: 15px; line-height:1;
    width: 22px; height: 22px;
    display:none; align-items:center; justify-content:center;
    cursor:pointer; padding: 0; border-radius: 50%; z-index: 2;
  }
  .clear-btn:hover{ color: var(--paper); background: rgba(255,255,255,0.16); }
  .input-wrap.has-value .clear-btn{ display:flex; }

  .search-rig button[type="submit"]{
    width:100%;
    background: var(--amber);
    color: var(--ink);
    border: none;
    border-radius: 8px;
    padding: 13px;
    font-weight: 600;
    font-size: 15px;
    transition: filter .15s ease;
  }
  .search-rig button[type="submit"]:hover{ filter: brightness(1.08); }
  .search-rig button[disabled]{ opacity:.6; cursor:default; }

  @media (max-width: 520px){ .search-fields{ flex-direction: column; } }

  @media (max-width: 480px){
    .hero{ padding-top: 40px; padding-bottom: 8px; }
    .wrap{ padding-left: 20px; padding-right: 20px; }
    .search-rig{ padding: 18px 14px; border-radius: 10px; }
    .search-fields{ gap: 14px; margin-bottom: 14px; }
    .field label{ font-size: 12px; margin-bottom: 6px; }
    .input-wrap input{ padding: 10px 30px 10px 12px; font-size: 14px; }
    .search-rig button[type="submit"]{ padding: 11px; font-size: 14px; }
  }

  /* ---------- Stats ---------- */
  .stat-row{
    display:flex; justify-content:center; gap: 48px;
    margin: 34px 0 60px;
  }
  .stat-row .stat b{
    display:block; font-family: var(--font-num); font-size: 28px;
    font-weight: 600; color: var(--amber);
  }
  .stat-row .stat span{ font-size: 13px; color: rgba(243,240,232,0.6); }

  /* ---------- Results ---------- */
  #status{ text-align:center; color: rgba(243,240,232,0.55); min-height: 24px; margin-bottom: 10px; }

  .grid{
    display:grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 22px;
    padding-bottom: 60px;
  }
  @media (max-width: 760px){ .grid{ grid-template-columns: repeat(2,1fr); } }
  @media (max-width: 520px){ .grid{ grid-template-columns: 1fr; } }

  .card{
    background: var(--steel);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 20px;
    opacity: 0;
    transform: translateY(8px);
    animation: rise .35s ease forwards;
    animation-delay: calc(var(--i, 0) * 0.04s);
    cursor: pointer;
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
  }
  @keyframes rise{ to{ opacity:1; transform: translateY(0); } }
  .card:hover{
    transform: translateY(-4px);
    border-color: rgba(232,163,61,0.35);
    box-shadow: 0 18px 30px -18px rgba(0,0,0,0.6);
  }

  .plate-mini{
    background: var(--plate);
    border-radius: 6px;
    padding: 14px 10px;
    display:flex; align-items:center; justify-content:center; gap:10px;
    margin-bottom: 16px;
    box-shadow: inset 0 2px 0 rgba(255,255,255,0.5), inset 0 -2px 4px rgba(0,0,0,0.1);
    transform: rotate(var(--tilt, 0deg));
    position: relative;
  }
  .plate-mini .bolt{ position:absolute; width:6px; height:6px; border-radius:50%; background: radial-gradient(circle at 35% 35%, #8a867a, #55524a); }
  .plate-mini .bolt.tl{ top:6px; left:6px; } .plate-mini .bolt.tr{ top:6px; right:6px; }
  .plate-mini .bolt.bl{ bottom:6px; left:6px; } .plate-mini .bolt.br{ bottom:6px; right:6px; }
  .plate-mini .let{ font-family: var(--font-ar); font-weight:700; color: var(--ink); font-size:19px; }
  .plate-mini .num{ font-family: var(--font-num); font-weight:600; color: var(--ink); font-size:23px; letter-spacing:1px; }

  .card .price{ font-family: var(--font-num); font-size: 21px; font-weight:600; color: var(--amber); }
  .card .ends{ margin-top: 8px; font-size: 13px; color: rgba(243,240,232,0.55); }

  @media (prefers-reduced-motion: reduce){
    .card{ animation:none; opacity:1; transform:none; }
  }

  /* ---------- How it works ---------- */
  .section{ padding: 20px 0 70px; border-top: 1px solid var(--line); margin-top: 20px; }
  .section h2{ font-size: 24px; font-weight:700; margin: 0 0 30px; text-align:center; }
  .steps{ display:grid; grid-template-columns: repeat(3,1fr); gap: 28px; }
  @media (max-width: 700px){ .steps{ grid-template-columns:1fr; } }
  .step{ padding-top: 16px; border-top: 1px solid var(--line); }
  .step .n{ font-family: var(--font-num); font-size: 14px; color: var(--amber); margin-bottom: 8px; }
  .step h3{ margin: 0 0 6px; font-size: 17px; }
  .step p{ margin:0; font-size: 14px; color: rgba(243,240,232,0.65); }

  footer{ border-top: 1px solid var(--line); padding: 26px 0; }
  footer .wrap{ display:flex; justify-content:space-between; flex-wrap:wrap; gap:10px; }
  footer p{ margin:0; font-size: 13px; color: rgba(243,240,232,0.45); }
  footer .disclaimer{ font-size: 12px; color: rgba(243,240,232,0.35); }
</style>
</head>
<body>

<header>
  <div class="wrap">
    <a href="/" class="logo"><span class="dot"></span>دور لي</a>
    <nav><a href="#how">كيف يعمل</a></nav>
  </div>
</header>

<section class="hero wrap">
  <h1>دوّر على لوحتك في مزاد أبشر</h1>
  <p class="lede">بحث مباشر في بيانات مزاد أبشر بالحروف أو الرقم.</p>

  <form id="searchForm">
    <div class="search-rig">
      <div class="search-fields">
        <div class="field">
          <label for="letters">الحروف</label>
          <div class="input-wrap" data-wrap="letters">
            <input id="letters" type="text" placeholder="ب ح ر">
            <button type="button" class="clear-btn" data-target="letters" aria-label="مسح الحروف">×</button>
          </div>
        </div>
        <div class="field">
          <label for="number">الرقم</label>
          <div class="input-wrap" data-wrap="number">
            <input id="number" type="text" placeholder="XXXX" inputmode="numeric" maxlength="4">
            <button type="button" class="clear-btn" data-target="number" aria-label="مسح الرقم">×</button>
          </div>
        </div>
      </div>
      <button type="submit" id="submitBtn">بحث</button>
    </div>
  </form>

  <div class="stat-row">
    <div class="stat"><b id="statCount">—</b><span>لوحة في المزاد الآن</span></div>
    <div class="stat"><b id="statTop">—</b><span>أعلى صفقة (ريال)</span></div>
  </div>
</section>

<div class="wrap">
  <div id="status"></div>
  <div class="grid" id="results"></div>
</div>

<section class="section" id="how">
  <div class="wrap">
    <h2>كيف يعمل</h2>
    <div class="steps">
      <div class="step">
        <div class="n">01</div>
        <h3>دوّر</h3>
        <p>اكتب الحروف أو الرقم اللي يهمك، أو الاثنين مع بعض.</p>
      </div>
      <div class="step">
        <div class="n">02</div>
        <h3>ابحث</h3>
        <p>نجيب لك النتائج مباشرة من بيانات مزاد أبشر لحظة الطلب.</p>
      </div>
      <div class="step">
        <div class="n">03</div>
        <h3>افتح المزاد</h3>
        <p>اضغط على أي لوحة تفتح لك صفحة المزاد الرسمية لمتابعتها.</p>
      </div>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <p>© 2026 دور لي</p>
    <p class="disclaimer">أداة بحث مستقلة، غير تابعة لأي جهة حكومية.</p>
  </div>
</footer>

<script>
  const form = document.getElementById('searchForm');
  const status = document.getElementById('status');
  const results = document.getElementById('results');
  const btn = document.getElementById('submitBtn');

  document.querySelectorAll('.input-wrap').forEach((wrap) => {
    const input = wrap.querySelector('input');
    const clearBtn = wrap.querySelector('.clear-btn');
    const toggle = () => wrap.classList.toggle('has-value', input.value.length > 0);
    toggle();
    input.addEventListener('input', toggle);
    clearBtn.addEventListener('click', () => { input.value = ''; toggle(); input.focus(); });
  });

  function formatLetters(letters) {
    return (letters || '')
      .split(' ')
      .map(ch => ch === 'ه' ? 'هـ' : ch)
      .join(' ');
  }

  function formatEndDate(dateStr) {
    const [datePart, timePart] = (dateStr || '').split(' ');
    let [h, m] = (timePart || '').split(':').map(Number);
    if (isNaN(h) || isNaN(m)) return dateStr;
    const ampm = h >= 12 ? 'PM' : 'AM';
    h = h % 12;
    if (h === 0) h = 12;
    const mm = String(m).padStart(2, '0');
    return `${datePart} - ${h}:${mm} ${ampm}`;
  }

  async function loadStats() {
    try {
      const res = await fetch('/api/stats');
      const data = await res.json();
      document.getElementById('statCount').textContent = data.count.toLocaleString('ar');
      document.getElementById('statTop').textContent = data.topAmount.toLocaleString('ar');
    } catch (err) {
      document.getElementById('statCount').textContent = '—';
      document.getElementById('statTop').textContent = '—';
    }
  }
  loadStats();

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const letters = document.getElementById('letters').value.trim();
    const number = document.getElementById('number').value.trim();

    btn.disabled = true;
    btn.textContent = 'يبحث...';
    status.textContent = '';
    results.innerHTML = '';

    try {
      const res = await fetch(`/api/search?letters=${encodeURIComponent(letters)}&number=${encodeURIComponent(number)}`);
      const data = await res.json();

      if (!data.length) {
        status.textContent = 'ما فيه لوحة مطابقة حالياً';
      } else {
        data.forEach((p, i) => {
          const card = document.createElement('div');
          card.className = 'card';
          card.style.setProperty('--i', i);
          card.style.setProperty('--tilt', ((Math.random() * 6) - 3).toFixed(1) + 'deg');
          card.innerHTML = `
            <div class="plate-mini" style="--tilt: ${((Math.random()*4)-2).toFixed(1)}deg">
              <span class="bolt tl"></span><span class="bolt tr"></span><span class="bolt bl"></span><span class="bolt br"></span>
              <span class="let">${formatLetters(p.letters)}</span><span class="num">${p.plateNumber}</span>
            </div>
            <div class="price">${p.topBiddingAmount.toLocaleString('ar')} ريال</div>
            <div class="ends">ينتهي: ${formatEndDate(p.auctionEndDate)}</div>
          `;
          card.addEventListener('click', () => window.open('{{ auction_url }}#' + p.anchor, '_blank'));
          results.appendChild(card);
        });
      }
    } catch (err) {
      status.textContent = 'تعذر جلب البيانات، حاول مرة ثانية';
    } finally {
      btn.disabled = false;
      btn.textContent = 'بحث';
    }
  });
</script>

</body>
</html>
"""


def fix_encoding(text):
    try:
        return text.encode("cp1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


# جدول تحويل الحرف العربي لمكافئه الإنجليزي المطبوع فعليًا على لوحات السعودية
AR_TO_EN_LETTER = {
    "أ": "A", "ا": "A", "ب": "B", "ح": "J", "د": "D", "ر": "R",
    "س": "S", "ص": "X", "ط": "T", "ع": "E", "ق": "G", "ك": "K",
    "ل": "L", "م": "Z", "ن": "N", "هـ": "H", "ه": "H", "و": "U", "ي": "V",
}


def build_plate_anchor(letters_ar, plate_number):
    # يبني الـ id اللي تستخدمه صفحة مزاد أبشر للسكرول التلقائي لنفس اللوحة
    # ترتيب الحروف الإنجليزية معكوس عن العربي (العربي يمين-لشمال، الإنجليزي شمال-ليمين)
    # مثال: حروف "س ه ل" ورقم "974" -> "LHS974"
    ar_letters = letters_ar.replace(" ", "")[::-1]
    en_letters = "".join(AR_TO_EN_LETTER.get(ch, "") for ch in ar_letters)
    return f"{en_letters}{plate_number}"


def normalize(letters):
    # يطابق نفس ترتيب الحروف بالضبط، بس يتجاهل المسافات الزايدة
    # ويعامل الألف بدون همزة "ا" كأنها "أ"
    letters = letters.replace("ا", "أ")
    return " ".join(letters.split())


def add_spaces_between_letters(letters):
    # لو المستخدم كتب الحروف بدون مسافات (مثال: "بحر") نحولها إلى "ب ح ر"
    if " " in letters:
        return letters
    return " ".join(letters)


ARABIC_INDIC = "٠١٢٣٤٥٦٧٨٩"
EXTENDED_ARABIC_INDIC = "۰۱۲۳۴۵۶۷۸۹"
WESTERN_DIGITS = "0123456789"

DIGIT_MAP = {}
for _i, _d in enumerate(ARABIC_INDIC):
    DIGIT_MAP[_d] = WESTERN_DIGITS[_i]
for _i, _d in enumerate(EXTENDED_ARABIC_INDIC):
    DIGIT_MAP[_d] = WESTERN_DIGITS[_i]


def normalize_number(number):
    # يحول الأرقام العربية/الهندية (٠١٢..) إلى أرقام إنجليزية، ويحد الطول لـ 4 أرقام
    converted = "".join(DIGIT_MAP.get(ch, ch) for ch in number)
    return converted[:4]


def fetch_plates():
    resp = requests.get(DATA_URL, timeout=15)
    resp.raise_for_status()
    # سيرفر أبشر أحيانًا يرجّع بيانات JSON زايدة بعد نهاية الرد الصحيح.
    # ناخذ بس أول JSON صحيح ونتجاهل أي شي زايد بعده بدل ما نفشل كامل.
    decoder = json.JSONDecoder()
    data, _ = decoder.raw_decode(resp.text)
    return data


@app.route("/")
def index():
    return render_template_string(PAGE, auction_url=AUCTION_URL)


@app.route("/api/search")
def api_search():
    letters = add_spaces_between_letters(request.args.get("letters", "").strip())
    number = normalize_number(request.args.get("number", "").strip())

    try:
        plates = fetch_plates()
    except (requests.RequestException, ValueError) as e:
        print(f"[fetch_plates error - /api/search] {type(e).__name__}: {e}")
        return jsonify({"error": "تعذر جلب البيانات من مزاد أبشر، حاول مرة ثانية"}), 502

    results = []
    for plate in plates:
        letters_ar = fix_encoding(plate["plateLetterAr"])

        if letters and normalize(letters) != normalize(letters_ar):
            continue
        if number and number != plate["plateNumber"]:
            continue

        results.append({
            "plateNumber": plate["plateNumber"],
            "letters": letters_ar,
            "topBiddingAmount": plate["topBiddingAmount"],
            "auctionEndDate": plate["auctionEndDate"],
            "anchor": build_plate_anchor(letters_ar, plate["plateNumber"]),
        })

    return jsonify(results)


@app.route("/api/stats")
def api_stats():
    try:
        plates = fetch_plates()
    except (requests.RequestException, ValueError) as e:
        print(f"[fetch_plates error - /api/stats] {type(e).__name__}: {e}")
        return jsonify({"error": "تعذر جلب البيانات من مزاد أبشر"}), 502
    count = len(plates)
    top_amount = max((p["topBiddingAmount"] for p in plates), default=0)
    return jsonify({"count": count, "topAmount": top_amount})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)