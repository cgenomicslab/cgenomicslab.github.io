# CGLab Website Fixes

This package contains fixes for the following issues:

## Changes Made

### 1. Mobile Menu Auto-Close (`_includes/header.html`)
- Added JavaScript to close the dropdown menu when a link is clicked
- Menu now properly dismisses after selection on mobile devices
- Added "Internal" link in navigation (highlighted in pink)

### 2. Contact Page Map Fix (`contact/index.md`)
- Updated map coordinates to match the main page
- Now correctly points to CGLab @ IMBB-FORTH

### 3. Internal Resources Page (`internal/index.md`)
- New page for lab internal resources
- Links to:
  - **Synology DSM**: https://dsm.cgenomicslab.org/
  - **Lab Chat**: https://chat.cgenomicslab.org/
  - **JupyterHub**: https://jupyter.cgenomicslab.org/
- Clean card-based design with hover effects
- Includes note about VPN/network access requirements

### 4. Email Button Instead of Inline Display (`index.md`)
- Emails are now hidden behind a clickable "email" button
- Click to reveal the email address
- Copy button with clipboard functionality
- Shows checkmark feedback when copied

### 5. Fixed Timeline (`members/index.md`)
- Rewrote timeline with JavaScript for proper calculations
- Bars now correctly show member tenure periods
- Hover effect on bars for better interaction
- Responsive design for mobile

### 6. CSS Additions (`static/css/css_additions.css`)
- Styles for email toggle button
- Internal page card styles
- Timeline improvements
- Alumni section styling

## Installation Instructions

### Step 1: Replace Files
Copy these files to your repository, replacing existing ones:

```
_includes/header.html    → replace existing
contact/index.md         → replace existing
internal/index.md        → NEW FILE (create internal/ folder)
members/index.md         → replace existing
index.md                 → replace existing
```

### Step 2: Add CSS
Append the contents of `static/css/css_additions.css` to the end of your `static/css/main.css` file.

### Step 3: Commit and Push

```bash
git add .
git commit -m "Fix mobile menu, map, timeline, add internal page and email buttons"
git push
```

## Features Overview

### Internal Page
Access at `/internal` - provides quick links to:
- Synology DSM (file storage)
- Synology Chat (team communication)
- JupyterHub (computational notebooks)

### Email Reveal
- Click the "email" button to show member's email
- Click the copy icon to copy to clipboard
- Visual feedback (checkmark) on successful copy

### Timeline
- Automatically calculates bar positions based on dates
- Color-coded by position type
- Hover to highlight
- Shows date range on right side
- Responsive: hides dates on mobile

## Customization

### Add More Internal Resources
Edit `internal/index.md` and add more `<a class="internal-card">` blocks following the existing pattern.

### Timeline Colors
Edit the `getColor()` function in `members/index.md` to change colors for different position types.

### Timeline Date Range
The timeline currently shows 2024 to current year + 1. Modify `startYear` and `endYear` in the JavaScript to adjust.
