# CGLab Website Fixes - Version 2

## Summary of Changes

### 1. Email Copy Bug Fix (`index.md`)
- Added fallback copy method using `document.execCommand('copy')` for browsers where clipboard API fails
- Now works reliably with all email addresses including imbb.forth.gr domains
- Auto-closes after copy with checkmark confirmation

### 2. Simplified Contact Section (`index.md`)
- Removed GitHub/Scholar links from contact (not needed there)
- Cleaner, simpler layout
- Removed standalone `/contact` page (all info is in section)
- **Action**: You can delete `contact/index.md` from your repo

### 3. Updated Internal Page (`internal/index.md`)
- Added RStudio Server link
- Added GitHub Organization link
- Added Notion Workspace links (main + Getting Started guide)
- Organized into "Lab Servers" and "Documentation & Code" sections

### 4. Research Page with Vertical Layout (`research/index.md`)
- New vertical layout with alternating figure placement
- Placeholder figures that show gracefully when image is missing
- Add your figures at:
  - `/static/img/research/synaptic_diversity.png`
  - `/static/img/research/cell_type_evolution.png`
  - `/static/img/research/gpcr_evolution.png`
  - `/static/img/research/coevolution.png`
- Keywords/tags for each project

### 5. Lab Photo Gallery (`members/index.md`)
- Replaced single photo with scrollable gallery
- Navigation arrows for desktop
- Swipe/scroll on mobile
- Year/label overlay on each photo
- Add photos at `/static/img/lab/`:
  - `lab_2025.jpg`
  - `lab_2024.jpg`
  - `retreat_2024.jpg`
  - (add more as needed - edit the HTML)

### 6. News Section
- The "Getting started!" post is from `_posts/2024-01-01-lab-opens.md`
- **Options**:
  - Delete the file to remove the post
  - Or delete the entire news section from `index.md` if not maintaining news
  - Or keep minimal (rename post to something like "Lab officially opens")

## Installation

### Files to Replace
```
index.md                  → replace (simplified contact, email fix)
internal/index.md         → replace (added RStudio, GitHub, Notion)
research/index.md         → replace (vertical layout with figures)
members/index.md          → replace (photo gallery)
_includes/header.html     → replace (mobile menu fix)
```

### Files to Delete (optional)
```
contact/index.md          → DELETE (redundant, all info in homepage section)
_posts/2024-01-01-lab-opens.md → DELETE if not using news
```

### Folders to Create
```
static/img/research/      → for research project figures
static/img/lab/           → for lab photos (multiple)
```

### Commit and Push
```bash
git add .
git commit -m "v2: Email fix, internal resources, research layout, photo gallery"
git push
```

## Adding Lab Photos

Edit `members/index.md` and add more `<div class="gallery-item">` blocks:

```html
<div class="gallery-item" data-label="Summer 2024">
<img src="/static/img/lab/summer_2024.jpg" alt="Lab summer 2024">
</div>
```

The `data-label` attribute appears as an overlay caption on the photo.

## Adding Research Figures

1. Create your figure (recommended: PNG, ~600px wide)
2. Save to `/static/img/research/`
3. Update the `<img src="...">` path in `research/index.md`

Until you add figures, placeholder boxes will appear with the text "Figure: [Project Name]".

## Customization Notes

### To Remove News Section Entirely
Delete this from `index.md`:
```html
<section id="news">
...
</section>
```

And remove "News" from `_includes/header.html` navigation.

### To Add More Internal Resources
Edit `internal/index.md` and add more `<a class="internal-card">` blocks following the existing pattern.
