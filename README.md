# CGLab website

Website of the **Comparative Genomics Lab (CGLab)** at IMBB-FORTH — <https://cgenomicslab.org>.

A single-page-scroll [Jekyll](https://jekyllrb.com/) site hosted on **GitHub Pages**. The
structure is based on the [Fraser Lab](https://github.com/fraserlab) site template, and the
visual design is inspired by the [UW Interactive Data Lab](https://idl.uw.edu/) — a near-white,
minimal layout with a left sidebar, a cursor-repelling pixel logo, and an IDL-style "People" page.

Feel free to clone and adapt it for your own lab.

---

## How it works

- **Jekyll 4** builds the static site from Markdown/HTML + [Liquid](https://shopify.github.io/liquid/) templates.
- **GitHub Pages** rebuilds and deploys automatically on every push to `main`
  (via `.github/workflows/jekyll.yml`). No manual build/upload step.
- Content lives in a few small places (below); most edits are one-line changes.

### Run it locally

```bash
bundle install                 # first time only
bundle exec jekyll serve       # then open http://localhost:4000
```

Changes to files rebuild automatically (except `_config.yml`, which needs a restart).

---

## Project structure

```
index.md                      Homepage: header, mission, and all sections
_config.yml                   Site settings and collections
_layouts/default.html         Page shell (sidebar + content + footer)
_includes/
  header.html                 Left sidebar: logo, nav, IMBB/FORTH logos
  footer.html                 Footer
  pixel-logo.html             Animated pixel "CGLab" logo (cursor-repel)
  projects-spotlight.html     Rotating Research spotlight (homepage)
  lab-gallery.html            Lab photo carousel
  lab-timeline.html           Members timeline (auto-built from dates)
  interns-list.html           Interns text list
_members/*.md                 One file per current lab member
_alumni/*.md                  One file per past member
_data/interns.yml             Interns (plain-text list)
research/index.html           Full Research page
teaching/index.html           Full Teaching page
join/ internal/               Other sub-pages
static/css/main.css           All site styling
static/img/                   Images (members, lab, research, logos, teaching)
```

---

## Editing content

### People (current members)

Add or edit a file in `_members/`, e.g. `_members/surname.md`:

```yaml
---
name: Firstname Lastname
startdate: 2025-01-01        # used by the timeline
position: PhD Student        # Group Leader / Postdoc / PhD Student / MSc Student / Undergraduate
tagline: Comparative genomics, protein evolution, tea   # one line shown under the name
image: /static/img/members/surname.jpg
altimage: /static/img/members/surname_alt.jpg           # optional: shown on hover
email: name@example.com
orcid: 0000-0000-0000-0000   # optional
scholar: XXXXXXXX            # optional (Google Scholar user id)
github: username            # optional
---

Free text for the person's own page (bio, education, research interests).
```

- `position` drives grouping/ordering (Group Leader → Postdoc → PhD → MSc → Undergraduate) and the timeline colours.
- Photos go in `static/img/members/`. Square images look best.

### Alumni

Same as members but in `_alumni/`, with `enddate` (and optional `subsequent`):

```yaml
enddate: 2026-03-31
subsequent: PhD at University of X    # optional "→ now …"
```

Alumni show as a plain-text list (no photos).

### Interns

Edit `_data/interns.yml`:

```yaml
- name: Intern Name
  origin: University of Crete, Heraklion    # shown on the right, in accent colour
  # url: /members/someone/                  # optional link, only if a page exists
```

### Research

- The **homepage spotlight** (rotating figures + titles): edit the `PROJECTS` array at the top of
  `_includes/projects-spotlight.html` (image, title, blurb). `INTERVAL` sets the rotation speed.
- The **full Research page**: `research/index.html`.
- Figures live in `static/img/research/`.

### Teaching / lab photos / navigation

- **Teaching**: text on the homepage `#teaching` section (`index.md`) and the full `teaching/index.html`.
- **Lab photos**: drop images in `static/img/lab/` and add `<div class="gallery-item">` blocks in `_includes/lab-gallery.html`.
- **Navigation / sidebar**: `_includes/header.html` (nav links, and the IMBB/FORTH footer logos).

---

## Customizing the look

### Colours & fonts

All theme colours are CSS variables at the top of `static/css/main.css`:

```css
:root {
  --primary: #652c90;   /* purple accent (links, highlights) */
  --accent:  #d5a928;   /* amber */
  --text:    #1b1b1b;
  --border:  #e5e7eb;
  ...
}
```

Fonts use an Avenir → Nunito Sans stack (Avenir is native on Apple devices; Nunito Sans is the
web fallback, loaded in `_layouts/default.html`).

### The pixel logo

`_includes/pixel-logo.html` draws the "CGLab" logo on a `<canvas>`. Each square springs to its
home position and flees the cursor (à la idl.uw.edu). Tunables are at the top:

| Constant | Meaning |
|----------|---------|
| `BOX`    | square size (px) |
| `PAD`    | empty room around the word so squares can fly out |
| `REPEL` / `RANGE` | how hard / how far the cursor pushes squares |
| `SPRING` / `DAMP` | how quickly squares return / how smooth the motion |
| `GHOST`  | faint colour revealed underneath |
| `COLORS` | the three letter colours (C / G / Lab) |

**Changing the logo shape:** edit `static/img/logo/new_logo.svg` (grid of coloured `<rect>`s),
then regenerate the coordinate list (`CELLS`) that the canvas uses:

```bash
python3 - <<'PY'
import re
s=open('static/img/logo/new_logo.svg').read()
BW=7.8633113; order={'#939597':0,'#652c90':1,'#d5a928':2}
cells=[]
for r in re.findall(r'<rect\b[^>]*/>', s, re.S):
    f=re.search(r'fill:(#[0-9a-fA-F]{6})',r).group(1)
    x=float(re.search(r'\bx="([-0-9.]+)"',r).group(1)); y=float(re.search(r'\by="([-0-9.]+)"',r).group(1))
    t=(re.search(r'transform="([^"]+)"',r) or [None,''])[1]
    if t=='':mx,my=x,y
    elif t=='rotate(90)':mx,my=-y-BW,x
    elif t=='scale(-1,1)':mx,my=-x-BW,y
    elif t.startswith('matrix(0,1,1,0,0,0)'):mx,my=y,x
    cells.append((mx,my,order[f]))
minx=min(c[0] for c in cells); miny=min(c[1] for c in cells)
cells=sorted(((round((mx-minx)/BW,3),round((my-miny)/BW,3),ci) for mx,my,ci in cells), key=lambda c:(c[1],c[0]))
mx=max(c[0] for c in cells); my=max(c[1] for c in cells)
print('GRID_W',round(mx+1,3),'GRID_H',round(my+1,3))
print('var CELLS=['+','.join('[%s,%s,%d]'%c for c in cells)+'];')
PY
```

Paste the printed `CELLS` and `GRID_W`/`GRID_H` values into `_includes/pixel-logo.html`.

---

## Deploying

Just commit and push to `main`:

```bash
git add -A
git commit -m "Update content"
git push
```

GitHub Actions rebuilds and publishes the site within a minute or two.

---

## Credits

- Template structure: [Fraser Lab](https://github.com/fraserlab)
- Design inspiration: [UW Interactive Data Lab](https://idl.uw.edu/)
- Built with [Jekyll](https://jekyllrb.com/) and GitHub Pages.
