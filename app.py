from flask import Flask, request, jsonify, render_template_string
import requests
import json
import time

app = Flask(__name__)

DATA_URL = "https://mazad.absher.sa/portal/auction-dashboard/data/MVPData.json"
AUCTION_URL = "https://mazad.absher.sa/portal/auction-dashboard/"
GIST_ID = "dc25303cebe9a0ca1b286a4db79de8c6"

PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">
<title>دور لي — بحث لوحات مزاد أبشر</title>
<link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABmJLR0QA/wD/AP+gvaeTAAAFOUlEQVR4nO2bW2xURRjHfzN7lmLb7SVyawttQQRKLbQsKBGitnIJJKQVCQGNqKghUTFRXmxMiA9CIhJCQqJRTIh4CfqAtg8E00h8E6TbLUSoGKDtSrtAqdsbBGT3jA+lWG49C8yecxb4vZ0533zff/85l5kzO4I4CLc2TBWISlDlQB6QC2TF09dGuoB2oA3YZypVk1vob7LqJIY6GW5pWCQEG4FSPRrtRaGCUlA9Ot//861ibmpAR6ghN6bYCTybMHX2UudR5ssjC2eGrz9xgwFnm4OlpkfVoMi3R5tttCshqnLyyw4ObrzGgHAoOEso9SuQaqcyG7lgop7KLfAHBhquGtDRUp9jCvm7grHOaLONsCHlrBHjStsA5EBrTMhv7oMfD5ATNc0dAwcSINwSXAxUOCbJfuafCQUWwhUDhFAbnNXjAEpsBBDh1sZigfmH03qcwDTNIimEqnRaiFMIKSslSj3jtBAHKTeAcToybdq6nYbGo7fVR0hBRno6Pl8avvQ0CgvyKCmeTPGUiaSkDNMha+j6MNYAcnQkC50Kc/TP4zpS4TU8+MtKqFoyjwUVczEMj5a8NyFPApmJyn6nXI7G2H+wkffXb2bpC2+x/2BjokplSesYZ2kJtbHmnfVs+/xrlFLa87veAAClFNt3/MCmrV9qz50UBgzw7fe11O7ZpzVnUhkAsGnLF3R392rLZ2jLFAfpaam8t3b11WOlFOc6IzQebuJA/SFM07TM0dN3np27fmLtmpe0aLLVgJSUFJZVLbzpuRMnQ6z74GNONocs8+yuqePN11/E47n7C9g1t8AjE/LZvu0jsrOt38qd/0T463izlrquMQBg5IhsVq2siis2EDyipaarDACYV/5kXHHBQ/eoAfljcxg+PMUy7kxHp5Z6rjNACEFmhs8yrqfnvJZ6rjMAwOu1nvx09+oZC7jSgHiIXY5qyeNKA2Ix60mPL47bJB5caUBfX59lTFZmupZarjMgEummt++CZVxW5j16BRyoPxRXXHHRJC31XGVANBrjq+9+jCt2RulULTVdY0A0GmPDJ59xpMn6u6JhGJSWFGmpa+ts0FQmPb3/P+Ci0SjnOrsINh5h1+49nDhpPRMEWFAxh9TUh7RostWASKSbufNX3lUOKSWrVy3TpMhFt0C8LF+6iEkTC7XlSyoDiosmsm7QFyUdJI0BxVMf5dMtH2pfMbL1GXAnSClZ8fxi3n371YQsl7nWAK/XS8XTs3njleVa7/nrcYUBhuHB50uncFwe0x6bzLSSKTzhLyFD04RnKMTp1gYt603nOru4ePHSbfXxej340tO0vdPvBG1XwIiH3fbP2fhImrdAonhggNMCnOaBAU4LcJr73gCD/p0Wlu+w2MUIKvZv4hVpQHiG4RmebR0HEYP+bSaWBnT8toFLZw9rkJd4UkZNY0z5Zss4hWqT9O+xuS9RiDYJ6P3TTTKhxC/SVKrGaR1OYZqy1sgt9DeFWwNBgSgbKjh1zEyMtDF2absrhvms930ICORNmH7MAJCCaqXYO1SHjKIVmuS5BVENV8YBV/bV1Tmqx0aUYu/ogrI6GDQQkmZ0FfC3Y6rso92QvDZwcNWAUeMfP22ingOsVyaTl/OmMpeMzJ/RPtBwzVA4t8AfkKaYgyC+JZrkok0JUZ5bOLNhcOMNc4FR48saPaY5m3vomaAUe0XM679+1yhYbJ4+EwosRImNCmYkTl7iEBAAUT3wwLtFjDXtzfVThJSVAlUBIo/+LfRu+wjYBbQpOAVqnxkzavImTD9m1ek/RhFwX3qBWOMAAAAASUVORK5CYII=">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Archivo+Black&family=Oswald:wght@500&display=swap" rel="stylesheet">
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

  .wrap{ max-width: 1080px; margin: 0 auto; padding-left: 24px; padding-right: 24px; }

  /* ---------- Header ---------- */
  header{ padding: 26px 0 20px; border-bottom: 1px solid var(--line); }
  header .wrap{ display:flex; align-items:center; justify-content:space-between; gap: 24px; }
  .logo{
    display:flex; align-items:center; gap: 10px;
    text-decoration: none;
  }
  .logo svg{ width: 34px; height: 34px; display:block; }
  .logo-text{ font-family: var(--font-ar); font-weight: 700; font-size: 20px; color: var(--paper); }
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

  .search-actions{ display:flex; gap: 10px; }
  .search-rig button[type="submit"]{
    flex: 1 1 0;
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
  #showAllBtn{
    display: none;
    flex: 1 1 0;
    align-items: center;
    justify-content: center;
    background: transparent;
    color: rgba(243,240,232,0.75);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 13px;
    font-weight: 500;
    font-size: 15px;
    font-family: var(--font-ar);
    transition: border-color .15s ease, color .15s ease;
  }
  #showAllBtn:hover{ border-color: rgba(232,163,61,0.4); color: var(--paper); }
  .search-rig button[disabled]{ opacity:.6; cursor:default; }

  @media (max-width: 520px){ .search-fields{ flex-direction: column; } }

  @media (max-width: 480px){
    .hero{ padding-top: 40px; padding-bottom: 8px; }
    .wrap{ padding-left: 20px; padding-right: 20px; }
    .search-rig{ padding: 18px 14px; border-radius: 10px; }
    .search-fields{ gap: 14px; margin-bottom: 14px; }
    .field label{ font-size: 12px; margin-bottom: 6px; }
    .input-wrap input{ padding: 10px 30px 10px 12px; font-size: 14px; }
    .search-actions{ flex-direction: column; }
    .search-rig button[type="submit"], #showAllBtn{ padding: 11px; font-size: 14px; }
    footer .wrap{ justify-content: center; text-align: center; }
    footer .made-by{ width: 100%; justify-content: center; }
  }

  /* ---------- Stats ---------- */
  .stat-row{
    display:flex; justify-content:center; gap: 48px;
    margin: 34px 0 6px;
  }
  .stat-row .stat b{
    display:block; font-family: var(--font-num); font-size: 28px;
    font-weight: 600; color: var(--amber);
  }
  .stat-row .stat span{ font-size: 13px; color: rgba(243,240,232,0.6); }

  .last-updated{
    text-align:center; font-size: 12.5px; color: rgba(243,240,232,0.4);
    margin-bottom: 44px;
  }

  /* ---------- Filter bar ---------- */
  .filter-bar{
    display:flex; flex-direction:column; gap: 18px;
    background: var(--steel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 22px;
  }
  .filter-row{
    display:flex; flex-wrap:wrap; align-items:flex-end; gap: 20px;
  }
  .filter-group{ display:flex; flex-direction:column; gap: 8px; }
  .filter-group label{
    font-size: 12.5px; color: rgba(243,240,232,0.5); font-weight: 500;
  }
  .sort-group{ flex: 0 0 170px; }
  .digits-group{ flex: 0 0 auto; }
  .pattern-group{ flex: 0 0 auto; }
  .letter-pattern-group{ flex: 0 0 auto; }
  .clear-group{ flex: 0 0 auto; }
  .filter-bar select{
    background: var(--asphalt);
    border: 1px solid transparent;
    border-radius: 8px;
    color: var(--paper);
    font-family: var(--font-ar);
    font-size: 15px;
    padding: 12px;
    min-height: 46px;
  }
  .filter-bar select:focus{ outline:none; border-color: rgba(232,163,61,0.5); }
  .price-group{ flex: 1 1 300px; }
  .price-inputs{ display:flex; flex-wrap:wrap; align-items:center; gap: 10px; }
  .price-inputs input{
    flex: 1 1 90px;
    min-width: 80px;
    width: auto;
    background: var(--asphalt);
    border: 1px solid transparent;
    border-radius: 8px;
    color: var(--paper);
    font-family: var(--font-num);
    font-size: 16px;
    padding: 13px 12px;
    min-height: 46px;
  }
  .price-inputs input:focus{ outline:none; border-color: rgba(232,163,61,0.5); }
  .price-inputs span{ color: rgba(243,240,232,0.35); flex: 0 0 auto; }
  /* إخفاء أزرار الزيادة/النقصان على حقول الأرقام */
  .price-inputs input[type="number"]::-webkit-outer-spin-button,
  .price-inputs input[type="number"]::-webkit-inner-spin-button{
    -webkit-appearance: none;
    margin: 0;
  }
  .price-inputs input[type="number"]{ -moz-appearance: textfield; appearance: textfield; }
  .apply-price-btn{
    flex: 0 0 auto;
    background: var(--amber);
    color: var(--ink);
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 14px;
    padding: 12px 20px;
    min-height: 46px;
    white-space: nowrap;
    transition: filter .15s ease;
  }
  .apply-price-btn:hover{ filter: brightness(1.08); }
  .clear-filters-btn{
    width: auto;
    background: transparent;
    border: 1px solid var(--line);
    border-radius: 8px;
    color: rgba(243,240,232,0.6);
    font-family: var(--font-ar);
    font-size: 14px;
    padding: 12px 20px;
    min-height: 46px;
    white-space: nowrap;
    transition: border-color .15s ease, color .15s ease;
  }
  .clear-filters-btn:hover{ border-color: rgba(232,163,61,0.4); color: var(--paper); }
  .digit-chips{ display:flex; flex-wrap:nowrap; gap: 8px; }
  .chip{
    flex: 0 0 auto;
    text-align:center;
    white-space: nowrap;
    background: var(--asphalt);
    border: 1px solid transparent;
    border-radius: 999px;
    color: rgba(243,240,232,0.7);
    font-family: var(--font-ar);
    font-size: 13.5px;
    padding: 10px 16px;
    min-height: 46px;
    transition: background .15s ease, color .15s ease, border-color .15s ease;
  }
  .chip:hover{ color: var(--paper); }
  .chip.active{
    background: var(--amber);
    color: var(--ink);
    font-weight: 600;
  }

  @media (max-width: 560px){
    .filter-row{ flex-direction: column; align-items: stretch; }
    .sort-group, .price-group, .digits-group, .pattern-group, .letter-pattern-group, .clear-group{ flex-basis: auto; }
    .apply-price-btn{ flex: 1 1 100%; }
    .clear-filters-btn{ width: 100%; }
    .digit-chips{ flex-wrap: wrap; }
    .chip{ flex: 1 1 calc(33.333% - 6px); min-width: 72px; white-space: normal; }
  }

  /* ---------- Results ---------- */
  #status{ text-align:center; color: rgba(243,240,232,0.55); min-height: 24px; margin-bottom: 10px; }

  .load-more-wrap{ display:none; justify-content:center; padding-bottom: 50px; }
  .load-more-btn{
    background: var(--steel);
    border: 1px solid var(--line);
    border-radius: 8px;
    color: var(--paper);
    font-family: var(--font-ar);
    font-size: 14px;
    padding: 12px 28px;
    transition: border-color .15s ease;
  }
  .load-more-btn:hover{ border-color: rgba(232,163,61,0.4); }

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
  footer .made-by{
    display:flex; align-items:center; gap:6px;
    font-size: 13px; color: rgba(243,240,232,0.55);
    text-decoration:none; transition: color .15s ease;
  }
  footer .made-by:hover{ color: var(--amber); }
</style>
</head>
<body>

<header>
  <div class="wrap">
    <a href="/" class="logo" aria-label="دور لي">
      <svg width="160" height="160" viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="160" height="160" rx="35" fill="#E8E1CE"/>
        <rect x="26" y="127" width="109" height="12" fill="#C98A14"/>
        <text x="80" y="105" text-anchor="middle" style="font-family:'Archivo Black',sans-serif" font-size="109" fill="#16191B">D</text>
      </svg>
      <span class="logo-text">دور لي</span>
    </a>
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
      <div class="search-actions">
        <button type="submit" id="submitBtn">بحث</button>
        <button type="button" id="showAllBtn">عرض كل اللوحات</button>
      </div>
    </div>
  </form>

  <div class="stat-row">
    <div class="stat"><b id="statCount">—</b><span>لوحة في المزاد الآن</span></div>
    <div class="stat"><b id="statTop">—</b><span>أعلى صفقة (ريال)</span></div>
  </div>
  <div class="last-updated">آخر تحديث: <span id="lastUpdated">—</span></div>
</section>

<div class="wrap">
  <div class="filter-bar">
    <div class="filter-row">
      <div class="filter-group sort-group">
        <label for="sortSelect">الترتيب</label>
        <select id="sortSelect">
          <option value="desc">الأعلى للأقل</option>
          <option value="asc">الأقل للأعلى</option>
        </select>
      </div>
      <div class="filter-group price-group">
        <label>السعر (ريال)</label>
        <div class="price-inputs">
          <input id="minPrice" type="number" min="0" placeholder="من">
          <span>—</span>
          <input id="maxPrice" type="number" min="0" placeholder="إلى">
          <button type="button" class="apply-price-btn" id="applyPriceBtn">تطبيق</button>
        </div>
      </div>
    </div>
    <div class="filter-row">
      <div class="filter-group digits-group">
        <label>عدد خانات الرقم</label>
        <div class="digit-chips" id="digitChips">
          <button type="button" class="chip active" data-digits="">الكل</button>
          <button type="button" class="chip" data-digits="1">فردي</button>
          <button type="button" class="chip" data-digits="2">ثنائي</button>
          <button type="button" class="chip" data-digits="3">ثلاثي</button>
          <button type="button" class="chip" data-digits="4">رباعي</button>
        </div>
      </div>
      <div class="filter-group pattern-group">
        <label>تصنيف الأرقام</label>
        <div class="digit-chips" id="patternChips">
          <button type="button" class="chip active" data-pattern="">الكل</button>
          <button type="button" class="chip" data-pattern="repeated">مكرر</button>
          <button type="button" class="chip" data-pattern="lock">قفل</button>
        </div>
      </div>
      <div class="filter-group letter-pattern-group">
        <label>تصنيف الحروف</label>
        <div class="digit-chips" id="letterPatternChips">
          <button type="button" class="chip active" data-letter-pattern="">الكل</button>
          <button type="button" class="chip" data-letter-pattern="repeated">مكرر</button>
          <button type="button" class="chip" data-letter-pattern="lock">قفل</button>
        </div>
      </div>
      <div class="filter-group clear-group">
        <label>&nbsp;</label>
        <button type="button" class="clear-filters-btn" id="clearFiltersBtn">مسح الفلاتر</button>
      </div>
    </div>
  </div>

  <div id="status"></div>
  <div class="grid" id="results"></div>
  <div class="load-more-wrap" id="loadMoreWrap">
    <button type="button" class="load-more-btn" id="loadMoreBtn">عرض المزيد</button>
  </div>
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
        <p>نجيب لك النتائج من بيانات مزاد أبشر، تتحدث كل ساعة.</p>
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
    <a href="https://linkedin.com/in/sulimanalhasan" target="_blank" rel="noopener" class="made-by">
      <svg width="16" height="16" viewBox="0 0 24 24" style="position:relative; top:-2px;"><rect width="24" height="24" rx="4" fill="#0A66C2"/><path fill="#fff" d="M20.45 20.45h-3.55v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.36-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45z"/></svg>
      Made by Suliman
    </a>
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

  // زر "عرض كل اللوحات" يظهر بس بعد ما المستخدم يضغط "بحث" فعلياً
  const showAllBtn = document.getElementById('showAllBtn');
  function updateShowAllVisibility() {
    const hasSearch = document.getElementById('letters').value.trim()
      || document.getElementById('number').value.trim();
    showAllBtn.style.display = hasSearch ? 'flex' : 'none';
  }

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

  function formatLastUpdated(ts) {
    if (!ts) return '—';
    const diffSec = Math.floor(Date.now() / 1000 - ts);
    if (diffSec < 60) return 'قبل لحظات';
    const diffMin = Math.floor(diffSec / 60);
    if (diffMin < 60) return `قبل ${diffMin.toLocaleString('ar')} دقيقة`;
    const diffHr = Math.floor(diffMin / 60);
    return `قبل ${diffHr.toLocaleString('ar')} ساعة`;
  }

  async function loadStats() {
    try {
      const res = await fetch('/api/stats');
      const data = await res.json();
      document.getElementById('statCount').textContent = data.count.toLocaleString('ar');
      document.getElementById('statTop').textContent = data.topAmount.toLocaleString('ar');
      document.getElementById('lastUpdated').textContent = formatLastUpdated(data.lastUpdated);
    } catch (err) {
      document.getElementById('statCount').textContent = '—';
      document.getElementById('statTop').textContent = '—';
      document.getElementById('lastUpdated').textContent = '—';
    }
  }
  loadStats();

  // ---------- Filter bar state ----------
  const sortSelect = document.getElementById('sortSelect');
  const minPriceInput = document.getElementById('minPrice');
  const maxPriceInput = document.getElementById('maxPrice');
  const applyPriceBtn = document.getElementById('applyPriceBtn');
  const clearFiltersBtn = document.getElementById('clearFiltersBtn');
  const digitChips = document.querySelectorAll('#digitChips .chip');
  const patternChips = document.querySelectorAll('#patternChips .chip');
  const letterPatternChips = document.querySelectorAll('#letterPatternChips .chip');
  const loadMoreWrap = document.getElementById('loadMoreWrap');
  const loadMoreBtn = document.getElementById('loadMoreBtn');

  let currentDigits = '';
  let currentPattern = '';
  let currentLetterPattern = '';
  let allResults = [];
  let shownCount = 0;
  const PAGE_SIZE = 30;

  digitChips.forEach((chip) => {
    chip.addEventListener('click', () => {
      digitChips.forEach((c) => c.classList.remove('active'));
      chip.classList.add('active');
      currentDigits = chip.dataset.digits;
      runSearch();
    });
  });
  patternChips.forEach((chip) => {
    chip.addEventListener('click', () => {
      patternChips.forEach((c) => c.classList.remove('active'));
      chip.classList.add('active');
      currentPattern = chip.dataset.pattern;
      runSearch();
    });
  });
  letterPatternChips.forEach((chip) => {
    chip.addEventListener('click', () => {
      letterPatternChips.forEach((c) => c.classList.remove('active'));
      chip.classList.add('active');
      currentLetterPattern = chip.dataset.letterPattern;
      runSearch();
    });
  });
  sortSelect.addEventListener('change', runSearch);
  applyPriceBtn.addEventListener('click', runSearch);
  [minPriceInput, maxPriceInput].forEach((input) => {
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') { e.preventDefault(); runSearch(); }
    });
  });
  clearFiltersBtn.addEventListener('click', () => {
    minPriceInput.value = '';
    maxPriceInput.value = '';
    sortSelect.value = 'desc';
    digitChips.forEach((c) => c.classList.remove('active'));
    document.querySelector('#digitChips .chip[data-digits=""]').classList.add('active');
    currentDigits = '';
    patternChips.forEach((c) => c.classList.remove('active'));
    document.querySelector('#patternChips .chip[data-pattern=""]').classList.add('active');
    currentPattern = '';
    letterPatternChips.forEach((c) => c.classList.remove('active'));
    document.querySelector('#letterPatternChips .chip[data-letter-pattern=""]').classList.add('active');
    currentLetterPattern = '';
    runSearch();
  });
  loadMoreBtn.addEventListener('click', renderMore);

  function buildCard(p, i) {
    const card = document.createElement('div');
    card.className = 'card';
    card.style.setProperty('--i', i % PAGE_SIZE);
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
    return card;
  }

  function renderMore() {
    const next = allResults.slice(shownCount, shownCount + PAGE_SIZE);
    next.forEach((p, idx) => results.appendChild(buildCard(p, shownCount + idx)));
    shownCount += next.length;

    loadMoreWrap.style.display = shownCount < allResults.length ? 'flex' : 'none';
    status.textContent = `${shownCount.toLocaleString('ar')} من ${allResults.length.toLocaleString('ar')} لوحة`;
  }

  async function runSearch() {
    const letters = document.getElementById('letters').value.trim();
    const number = document.getElementById('number').value.trim();
    const params = new URLSearchParams();
    if (letters) params.set('letters', letters);
    if (number) params.set('number', number);
    if (minPriceInput.value) params.set('minPrice', minPriceInput.value);
    if (maxPriceInput.value) params.set('maxPrice', maxPriceInput.value);
    if (currentDigits) params.set('digits', currentDigits);
    if (currentPattern) params.set('pattern', currentPattern);
    if (currentLetterPattern) params.set('letterPattern', currentLetterPattern);
    params.set('sort', sortSelect.value);

    btn.disabled = true;
    btn.textContent = 'بحث...';
    status.textContent = '';
    results.innerHTML = '';
    loadMoreWrap.style.display = 'none';
    shownCount = 0;
    allResults = [];

    try {
      const res = await fetch(`/api/search?${params.toString()}`);
      const data = await res.json();
      if (!Array.isArray(data)) throw new Error('bad response');
      allResults = data;

      if (!allResults.length) {
        status.textContent = 'ما فيه لوحة مطابقة حالياً';
      } else {
        renderMore();
      }
    } catch (err) {
      status.textContent = 'تعذر جلب البيانات، حاول مرة ثانية';
    } finally {
      btn.disabled = false;
      btn.textContent = 'بحث';
    }
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    runSearch();
    updateShowAllVisibility();
  });

  document.getElementById('showAllBtn').addEventListener('click', () => {
    const lettersInput = document.getElementById('letters');
    const numberInput = document.getElementById('number');
    lettersInput.value = '';
    numberInput.value = '';
    lettersInput.dispatchEvent(new Event('input'));
    numberInput.dispatchEvent(new Event('input'));
    updateShowAllVisibility();
    runSearch();
  });

  // تصفح كل اللوحات مباشرة عند فتح الصفحة
  runSearch();
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


_cache = {"data": None, "fetched_at": 0}
CACHE_SECONDS = 300  # 5 minutes - avoids hitting GitHub's 60 req/hour limit


GIST_RAW_URL = "https://gist.githubusercontent.com/Sulliiman/dc25303cebe9a0ca1b286a4db79de8c6/raw/plates.json"


def fetch_plates():
    # نقرأ من الـ Gist بدل ما نطلب أبشر مباشرة (جهاز المستخدم هو اللي يحدّث
    # الـ Gist كل فترة من بيته، ويتجنب حجب أبشر لسيرفرات الاستضافة السحابية)
    # نستخدم رابط raw (مو api.github.com) لأنه ما له حد ٦٠ طلب/ساعة الصارم
    now = time.time()
    if _cache["data"] is not None and (now - _cache["fetched_at"]) < CACHE_SECONDS:
        return _cache["data"]

    resp = requests.get(GIST_RAW_URL, timeout=15, headers={"Cache-Control": "no-cache"})
    resp.raise_for_status()
    data = json.loads(resp.text)

    _cache["data"] = data
    _cache["fetched_at"] = now
    return data


@app.route("/")
def index():
    return render_template_string(PAGE, auction_url=AUCTION_URL)


def _parse_price(value):
    try:
        return float(value) if value else None
    except ValueError:
        return None


def digit_str(plate_number):
    # تمثيل الرقم كنص بدون أصفار بادئة (المرجع لعدّ الخانات وتصنيف الأنماط)
    try:
        return str(int(plate_number))
    except (TypeError, ValueError):
        return str(plate_number).lstrip("0") or "0"


def matches_pattern(number_str, pattern):
    # مكرر: كل الخانات نفس الرقم (ثنائي/ثلاثي/رباعي فقط)
    if pattern == "repeated":
        return len(number_str) >= 2 and len(set(number_str)) == 1
    # قفل: أول رقم = آخر رقم، والوسط مب مهم — بس نستثني اللي كل خاناته متطابقة
    # (لأن هذي أصلاً "مكرر"، مو "قفل" حقيقي)
    if pattern == "lock":
        return (
            len(number_str) >= 3
            and number_str[0] == number_str[-1]
            and len(set(number_str)) > 1
        )
    return True


def letter_list(letters_ar):
    # الحروف الثلاثة بعد توحيد الألف (نفس منطق normalize())
    return letters_ar.replace("ا", "أ").split()


def matches_letter_pattern(letters, pattern):
    # الحروف دايماً 3 خانات
    if len(letters) != 3:
        return False
    # مكرر: الثلاث حروف نفس الحرف
    if pattern == "repeated":
        return len(set(letters)) == 1
    # قفل: أول حرف = آخر حرف، بس نستثني اللي الثلاثة متطابقة (نفس منطق الأرقام)
    if pattern == "lock":
        return letters[0] == letters[-1] and len(set(letters)) > 1
    return True


@app.route("/api/search")
def api_search():
    letters = add_spaces_between_letters(request.args.get("letters", "").strip())
    number = normalize_number(request.args.get("number", "").strip())
    min_price = _parse_price(request.args.get("minPrice", "").strip())
    max_price = _parse_price(request.args.get("maxPrice", "").strip())
    digits = request.args.get("digits", "").strip()
    pattern = request.args.get("pattern", "").strip()
    letter_pattern = request.args.get("letterPattern", "").strip()
    sort = request.args.get("sort", "").strip()

    try:
        plates = fetch_plates()
    except (requests.RequestException, ValueError) as e:
        print(f"[fetch_plates error - /api/search] {type(e).__name__}: {e}")
        return jsonify({"error": "تعذر جلب البيانات، حاول مرة ثانية"}), 502

    results = []
    for plate in plates:
        letters_ar = fix_encoding(plate["plateLetterAr"])
        price = plate["topBiddingAmount"]
        num_str = digit_str(plate["plateNumber"])

        if letters and normalize(letters) != normalize(letters_ar):
            continue
        if number and number != plate["plateNumber"]:
            continue
        if min_price is not None and price < min_price:
            continue
        if max_price is not None and price > max_price:
            continue
        if digits in ("1", "2", "3", "4") and len(num_str) != int(digits):
            continue
        if letter_pattern in ("repeated", "lock") and not matches_letter_pattern(
            letter_list(letters_ar), letter_pattern
        ):
            continue
        if pattern in ("repeated", "lock") and not matches_pattern(num_str, pattern):
            continue

        results.append({
            "plateNumber": plate["plateNumber"],
            "letters": letters_ar,
            "topBiddingAmount": price,
            "auctionEndDate": plate["auctionEndDate"],
            "anchor": build_plate_anchor(letters_ar, plate["plateNumber"]),
        })

    if sort == "asc":
        results.sort(key=lambda p: p["topBiddingAmount"])
    elif sort == "desc":
        results.sort(key=lambda p: p["topBiddingAmount"], reverse=True)

    return jsonify(results)


@app.route("/api/stats")
def api_stats():
    try:
        plates = fetch_plates()
    except (requests.RequestException, ValueError) as e:
        print(f"[fetch_plates error - /api/stats] {type(e).__name__}: {e}")
        return jsonify({"error": "تعذر جلب البيانات"}), 502
    count = len(plates)
    top_amount = max((p["topBiddingAmount"] for p in plates), default=0)
    return jsonify({
        "count": count,
        "topAmount": top_amount,
        "lastUpdated": _cache["fetched_at"] or None,
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)