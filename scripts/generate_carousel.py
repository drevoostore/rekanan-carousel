#!/usr/bin/env python3
"""
Generate carousel searchbox HTML from Google Sheets CSV
Output: outputs/carousel_dev.html  (on dev1)
        outputs/carousel_prod.html (on dev2 -- EDIT line 18 below)
Features: Horizontal carousel, randomized order, auto-scroll, SEARCH by nama/kota

HOW TO SWITCH TO PROD ON DEV2:
  Edit line 18 below:
    OUTPUT_FILE = Path("outputs") / "carousel_prod.html"
"""

import requests
import csv
from io import StringIO
from pathlib import Path
import random

# ===== CONFIGURATION =====
# EDIT THIS LINE WHEN COPYING TO DEV2:
# Change "carousel_dev.html" to "carousel_prod.html"
OUTPUT_FILE = Path("outputs") / "carousel_dev.html"
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnV37JIH3rFESwe3HLDDo1m2SNMZcft6dJivj82kSDSlntZ_Gm7bwr25eFXqMhNQnynJuH3tdJVdvL/pub?gid=0&single=true&output=csv"

# ===== CAROUSEL HTML TEMPLATE =====
CAROUSEL_HTML = r"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rekanan Directory - Carousel</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif; background: #fff; padding: 20px 20px 40px; }
    .container { max-width: 1400px; margin: 0 auto; }
    .header { text-align: center; margin-bottom: 30px; }
    .header h1 { font-size: 28px; color: #2c3e50; margin-bottom: 8px; }
    .header p { color: #666; font-size: 14px; }
    .carousel-wrapper { position: relative; overflow: hidden; padding: 20px 0; }
    .carousel-track { display: flex; gap: 20px; transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94); will-change: transform; }
    .carousel-track.dragging { transition: none; }
    .rekanan-card { flex: 0 0 350px; min-height: 320px; display: flex; flex-direction: column; background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); border: 2px solid #e8e8e8; border-radius: 12px; padding: 24px; transition: all 0.3s ease; cursor: pointer; position: relative; overflow: hidden; }
    .rekanan-card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: linear-gradient(180deg, #4a90d9 0%, #357abd 100%); opacity: 0; transition: opacity 0.3s ease; }
    .rekanan-card:hover { background: linear-gradient(135deg, #e8f4f8 0%, #f0f7fb 100%); box-shadow: 0 8px 24px rgba(74, 144, 217, 0.2); transform: translateY(-4px); border-color: #4a90d9; }
    .rekanan-card:hover::before { opacity: 1; }
    .rekanan-card strong { display: block; margin-bottom: 12px; color: #2c3e50; font-size: 18px; font-weight: 700; line-height: 1.4; }
    .rekanan-card .card-content { flex: 1 1 auto; }
    .rekanan-card .city-badge { display: inline-block; padding: 4px 12px; background: linear-gradient(135deg, #4a90d9 0%, #357abd 100%); color: #fff; border-radius: 16px; font-size: 12px; font-weight: 600; margin-bottom: 12px; }
    .rekanan-card .info-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 14px; }
    .rekanan-card .info-row svg { width: 16px; height: 16px; flex-shrink: 0; }
    .rekanan-card a { color: #E1306C; text-decoration: none; font-weight: 500; transition: color 0.3s ease; }
    .rekanan-card a:hover { color: #C13584; text-decoration: underline; }
    .rekanan-card .address { color: #666; font-size: 13px; line-height: 1.5; margin-top: auto; padding-top: 12px; border-top: 1px solid #e8e8e8; flex-shrink: 0; }
    @media (max-width: 768px) { .rekanan-card { flex: 0 0 280px; padding: 20px; min-height: 280px; } .rekanan-card strong { font-size: 16px; } .carousel-nav { width: 36px; height: 36px; } .carousel-nav svg { width: 16px; height: 16px; } }
    @media (max-width: 480px) { .rekanan-card { flex: 0 0 260px; min-height: 260px; } .header h1 { font-size: 22px; } .search-box { padding: 12px 16px 12px 40px; font-size: 14px; } }
  </style>
</head>
<body>
  <div class="container">
    <div class="search-box-wrapper">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <input type="text" class="search-box" id="searchInput" placeholder="Cari nama rekanan atau kota..." oninput="filterCards(this.value)">
    </div>
    <div class="no-results" id="noResults">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <div>Tidak ada rekanan ditemukan</div>
    </div>
    <div class="carousel-wrapper" id="carouselWrapper">
      <button class="carousel-nav prev" onclick="moveCarousel(-1)" aria-label="Previous"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg></button>
      <div class="carousel-track" id="carouselTrack">
{rekanan_cards}
      </div>
      <button class="carousel-nav next" onclick="moveCarousel(1)" aria-label="Next"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg></button>
    </div>
    <div class="carousel-dots" id="carouselDots"></div>
  </div>
  <script>
    let currentPosition = 0; let cardWidth = 370; let visibleCards = Math.floor(window.innerWidth / cardWidth); let totalCards = {total_cards}; let maxPosition = Math.max(0, totalCards - visibleCards); let autoScrollInterval = null; let isDragging = false; let startX = 0; let currentTranslate = 0; let prevTranslate = 0;
    const track = document.getElementById('carouselTrack'); const wrapper = document.getElementById('carouselWrapper'); const searchInput = document.getElementById('searchInput'); const noResults = document.getElementById('noResults');
    let allCards = Array.from(track.children);
    function initDots() { const dotsContainer = document.getElementById('carouselDots'); dotsContainer.innerHTML = ''; const totalDots = Math.ceil(totalCards / visibleCards); for (let i = 0; i < totalDots; i++) { const dot = document.createElement('div'); dot.className = 'carousel-dot' + (i === 0 ? ' active' : ''); dot.onclick = () => goToSlide(i); dotsContainer.appendChild(dot); } }
    function updateDots() { const dots = document.querySelectorAll('.carousel-dot'); const activeDot = Math.floor(currentPosition / visibleCards); dots.forEach((dot, i) => { dot.classList.toggle('active', i === activeDot); }); }
    function moveCarousel(direction) { const newPosition = currentPosition + (direction * visibleCards); currentPosition = Math.max(0, Math.min(newPosition, maxPosition)); updateCarousel(); resetAutoScroll(); }
    function goToSlide(slideIndex) { currentPosition = slideIndex * visibleCards; currentPosition = Math.min(currentPosition, maxPosition); updateCarousel(); resetAutoScroll(); }
    function updateCarousel() { track.style.transform = `translateX(-${currentPosition * cardWidth}px)`; updateDots(); sendHeight(); }
    function resetAutoScroll() { if (autoScrollInterval) clearInterval(autoScrollInterval); autoScrollInterval = setInterval(() => { if (currentPosition >= maxPosition) currentPosition = 0; else currentPosition++; updateCarousel(); }, 3000); }
    function filterCards(query) {
      const q = query.toLowerCase().trim();
      let visibleCount = 0;
      allCards.forEach(card => {
        const kota = (card.dataset.kota || '').toLowerCase();
        const nama = (card.dataset.nama || '').toLowerCase();
        const match = !q || kota.includes(q) || nama.includes(q);
        card.style.display = match ? '' : 'none';
        if (match) visibleCount++;
      });
      if (visibleCount === 0) {
        wrapper.style.display = 'none';
        document.getElementById('carouselDots').style.display = 'none';
        noResults.style.display = 'block';
      } else {
        wrapper.style.display = '';
        document.getElementById('carouselDots').style.display = '';
        noResults.style.display = 'none';
        totalCards = visibleCount;
        currentPosition = 0;
        prevTranslate = 0;
        currentTranslate = 0;
        visibleCards = Math.floor(window.innerWidth / cardWidth);
        maxPosition = Math.max(0, totalCards - visibleCards);
        track.style.transform = 'translateX(0px)';
        initDots();
        updateDots();
        sendHeight();
      }
    }
    track.addEventListener('mousedown', startDrag); track.addEventListener('touchstart', startDrag); track.addEventListener('mousemove', drag); track.addEventListener('touchmove', drag); track.addEventListener('mouseup', endDrag); track.addEventListener('touchend', endDrag); track.addEventListener('mouseleave', endDrag);
    function startDrag(e) { isDragging = true; startX = getPositionX(e); track.classList.add('dragging'); if (autoScrollInterval) clearInterval(autoScrollInterval); }
    function drag(e) { if (!isDragging) return; const currentX = getPositionX(e); const diff = currentX - startX; currentTranslate = prevTranslate + diff; track.style.transform = `translateX(${currentTranslate}px)`; }
    function endDrag() { if (!isDragging) return; isDragging = false; track.classList.remove('dragging'); const movedBy = currentTranslate - prevTranslate; if (movedBy < -100) currentPosition += visibleCards; if (movedBy > 100) currentPosition -= visibleCards; currentPosition = Math.max(0, Math.min(currentPosition, maxPosition)); prevTranslate = -currentPosition * cardWidth; currentTranslate = prevTranslate; updateCarousel(); resetAutoScroll(); }
    function getPositionX(e) { return e.type.includes('mouse') ? e.pageX : e.touches[0].clientX; }
    window.addEventListener('resize', () => { visibleCards = Math.floor(window.innerWidth / cardWidth); maxPosition = Math.max(0, totalCards - visibleCards); updateCarousel(); });
    initDots(); resetAutoScroll();
    wrapper.addEventListener('mouseenter', () => { if (autoScrollInterval) clearInterval(autoScrollInterval); });
    wrapper.addEventListener('mouseleave', () => { resetAutoScroll(); });
  </script>
  <script>
    (function() {
      function sendHeight() {
        var h = document.documentElement.scrollHeight || document.body.scrollHeight;
        if (h > 0) window.parent.postMessage({ height: h }, '*');
      }
      sendHeight();
      window.addEventListener('resize', sendHeight);
      setTimeout(sendHeight, 100);
      setTimeout(sendHeight, 500);
    })();
  </script>
</body>
</html>
"""

REKANAN_CARD_TEMPLATE = r"""        <div class="rekanan-card" data-kota="{kota}" data-nama="{nama}">
          <div class="card-content">
            <span class="city-badge">📍 {city_title}</span>
            <strong>{nama}</strong>
            <div class="info-row">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
              <a href="https://instagram.com/{instagram_link}" target="_blank">{instagram}</a>
            </div>
            <div class="info-row">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
              <span>{telp}</span>
            </div>
          </div>
          <div class="address">📍 {alamat}, {kota}</div>
        </div>
"""


def fetch_and_parse(csv_url):
    """Fetch CSV and parse data"""
    print(f"Fetching CSV from: {csv_url[:50]}...")
    response = requests.get(csv_url, timeout=30)
    response.raise_for_status()
    reader = csv.DictReader(StringIO(response.text))
    rekanans = [
        {
            'nama': r['nama'].strip(),
            'kota': r['kota'].strip(),
            'instagram': r['instagram'].strip(),
'telp': r['telp'].strip(),
            'alamat': r['alamat'].strip()
        }
        for r in reader
    ]
    print(f"✅ Parsed {len(rekanans)} rekanans")
    return rekanans


def generate_cards(rekanans):
    """Generate carousel cards"""
    randomized = rekanans.copy()
    random.shuffle(randomized)
    cards = []
    for r in randomized:
        instagram_clean = r['instagram'].lstrip('@')
        city_title = r['kota'].title()
        cards.append(REKANAN_CARD_TEMPLATE.format(
            nama=r['nama'], kota=r['kota'], city_title=city_title,
            instagram=r['instagram'], instagram_link=instagram_clean,
            telp=r['telp'], alamat=r['alamat']
        ))
    return "\n".join(cards), len(randomized)


def main():
    """Main function"""
    print("🎠 Generating Carousel Searchbox...")
    print(f"   Output: {OUTPUT_FILE}")
    rekanans = fetch_and_parse(CSV_URL)
    if not rekanans:
        print("❌ No data found!")
        return 1
    cards_html, total_cards = generate_cards(rekanans)
    html = CAROUSEL_HTML.replace('{rekanan_cards}', cards_html).replace('{total_cards}', str(total_cards))
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ Generated: {OUTPUT_FILE}")
    print(f"   Total cards: {total_cards}")
    print(f"   Layout: Horizontal carousel (randomized)")
    print(f"   Features: Auto-scroll, drag/swipe, navigation buttons, SEARCH by nama/kota")
    return 0


if __name__ == "__main__":
    exit(main())
