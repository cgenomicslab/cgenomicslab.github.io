# CGLab Website Updates

These files fix the members page and member detail pages.

## Changes Made

### 1. `members/index.md` - Updated Members Page
- Added lab photo section (placeholder - add your photo at `/static/img/lab/lab_photo.jpg`)
- Added alumni section (now only appears here, not on homepage)
- Added interactive timeline showing when members joined/left the lab
- Timeline colors indicate position type (Group Leader, PhD, MSc, etc.)

### 2. `index.md` - Updated Homepage
- Removed alumni section (alumni now only shown on `/members` page)
- Cleaner, simpler members display

### 3. `_layouts/member.html` - Fixed Member Detail Pages
- Fixed photo display issues with proper positioning
- Improved hover effect for alt images
- Added inline styles to ensure photos display correctly regardless of main CSS
- Responsive design for mobile

### 4. `static/css/css_additions.css` - CSS Additions
- Copy the contents of this file and add to the end of your `main.css`
- Contains styles for: member photos, timeline, lab photo section, alumni list

## Installation

1. **Replace these files in your repository:**
   - `members/index.md` → replace existing file
   - `index.md` → replace existing file
   - `_layouts/member.html` → replace existing file

2. **Add CSS:**
   - Open your `static/css/main.css` file
   - Copy all contents from `static/css/css_additions.css`
   - Paste at the end of `main.css`

3. **Add lab photo (optional):**
   - Create folder: `static/img/lab/`
   - Add your lab photo as `lab_photo.jpg`

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "Fix members page: add timeline, fix photos, reorganize alumni"
   git push
   ```

## Timeline Configuration

The timeline uses the `startdate` and `enddate` fields from member files:
- Members without `enddate` are shown as current (bar extends to present)
- Colors are assigned based on `position` field:
  - **Red**: Group Leader / Principal Investigator
  - **Orange**: Postdoc
  - **Yellow**: PhD Student
  - **Teal**: MSc Student
  - **Light blue**: Undergraduate
  - **Blue**: Staff / Technician
  - **Gray**: Visitor / Intern

To customize a member's timeline color, add `timeline_group` to their YAML:
```yaml
timeline_group: "PhD Student"
```

## Lab Photo

To add a lab photo, place it at:
```
/static/img/lab/lab_photo.jpg
```

Recommended: landscape orientation, at least 800px wide.
