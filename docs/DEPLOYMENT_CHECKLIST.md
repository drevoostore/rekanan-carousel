# Production Deployment Checklist

## Pre-Deployment Verification

### 1. Code Review ✅
- [ ] All changes committed to `main` branch
- [ ] CHECKPOINT.md updated with latest fixes
- [ ] No debug console.log statements in production code
- [ ] Git status clean (no uncommitted changes)

### 2. Testing on Dev (dev1) ✅
- [ ] Autorotate working (2 seconds per card)
- [ ] Search displays ALL results in grid layout
- [ ] No autorotate during search mode
- [ ] Mouse hover doesn't trigger autorotate in search mode
- [ ] Clear search returns to carousel mode
- [ ] Mobile responsive (1 card <420px, 2 cards 420-720px, 3 cards 720-1000px, 4 cards >1000px)
- [ ] iframe auto-height working (no scrollbar in PageFly)

### 3. Cloudflare Pages (Dev) ✅
- [ ] Latest commit deployed to https://rekanan-carousel.pages.dev/carousel_dev.html
- [ ] Hard refresh (Ctrl+Shift+R) shows latest version
- [ ] Console shows no errors

---

## Production Deployment Steps

### Step 1: Update Production Configuration
- [ ] Edit `scripts/generate_carousel.py` line 17:
  ```python
  OUTPUT_FILE = Path("outputs") / "carousel_prod.html"  # Change from carousel_dev.html
  ```
- [ ] Verify CSV URL points to production Google Sheet (if different)
- [ ] Verify `CARDS_PER_VISIT = 16` (or desired number)
- [ ] Verify autorotate interval `}, 2000);` (2 seconds)

### Step 2: Generate Production HTML
```bash
cd /home/dev/rekanan-carousel
python3 scripts/generate_carousel.py
```
Expected output:
```
✅ Generated: outputs/carousel_prod.html
Total rekanans embedded: 493
Cards shown per visit: 16 (randomized in browser)
```

### Step 3: Verify Production HTML
- [ ] Open `outputs/carousel_prod.html` in browser
- [ ] Test autorotate (2 seconds per card)
- [ ] Test search (all results in grid, no autorotate)
- [ ] Test mobile responsive
- [ ] Check browser console (no errors)

### Step 4: Commit Production File
```bash
git add outputs/carousel_prod.html
git commit -m "prod: generate carousel_prod.html for deployment"
git push
```

### Step 5: Cloudflare Pages Production
- [ ] Go to Cloudflare Dashboard → Pages → rekanan-carousel
- [ ] Verify production branch is `main`
- [ ] Check deployment status
- [ ] Wait for deployment to complete (~1-2 minutes)

### Step 6: Verify Production URL
- [ ] Open production URL: `https://rekanan-carousel.pages.dev/carousel_prod.html`
- [ ] Hard refresh (Ctrl+Shift+R)
- [ ] Test all features:
  - [ ] Carousel shows 16 random cards
  - [ ] Autorotate every 2 seconds
  - [ ] Search shows all results in grid
  - [ ] No autorotate during search
  - [ ] Clear search returns to carousel
  - [ ] Mobile responsive works
  - [ ] No console errors

### Step 7: PageFly Integration (Production)
- [ ] Update PageFly iframe src to production URL:
  ```html
  <iframe src="https://rekanan-carousel.pages.dev/carousel_prod.html" ...>
  ```
- [ ] Test in PageFly editor
- [ ] Verify auto-height working
- [ ] Test on mobile preview
- [ ] Publish PageFly page

### Step 8: Final Verification
- [ ] Visit live PageFly page
- [ ] Test carousel on desktop
- [ ] Test carousel on mobile
- [ ] Test search functionality
- [ ] Verify all rekanans searchable (493 total)
- [ ] Check page load speed

---

## Rollback Plan (If Issues)

### Quick Rollback to Dev
If production has issues, revert PageFly iframe to dev URL:
```html
<iframe src="https://rekanan-carousel.pages.dev/carousel_dev.html" ...>
```

### Restore Previous Production
```bash
git log --oneline -10  # Find last good production commit
git checkout <commit-hash> -- outputs/carousel_prod.html
python3 scripts/generate_carousel.py
git add outputs/carousel_prod.html
git commit -m "rollback: restore previous production version"
git push
```

---

## Post-Deployment Monitoring

### Day 1
- [ ] Monitor Cloudflare Pages deployment logs
- [ ] Check for any error reports from users
- [ ] Verify analytics (if enabled)

### Week 1
- [ ] Collect user feedback
- [ ] Monitor performance metrics
- [ ] Check search usage patterns

---

## Production URLs

**Cloudflare Pages Production:**
```
https://rekanan-carousel.pages.dev/carousel_prod.html
```

**PageFly Production Page:**
```
[Insert PageFly URL here]
```

---

## Contacts

- **Developer:** [Your contact]
- **Customer:** [Customer contact]
- **Support:** [Support contact]

---

**Deployment Date:** _______________
**Deployed By:** _______________
**Status:** ☐ Success ☐ Issues (see notes)

**Notes:**
_______________________________________________
_______________________________________________
