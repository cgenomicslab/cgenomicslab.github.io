---
title: Internal
layout: default
group: internal
---

<div class="container">
<section style="padding: 2rem 0;">

<h1 class="section-title" style="font-size: 1.5rem; margin-bottom: 1.5rem;">Internal Resources</h1>

<p class="internal-intro" style="color: #666; margin-bottom: 2rem;">
Lab resources and services for CGLab members. These require network access or VPN.
</p>

<div class="internal-grid">

<a href="https://dsm.cgenomicslab.org/" target="_blank" class="internal-card">
<div class="internal-icon">
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
<line x1="8" y1="21" x2="16" y2="21"></line>
<line x1="12" y1="17" x2="12" y2="21"></line>
</svg>
</div>
<div class="internal-info">
<h3>Synology DSM</h3>
<p>File storage, backups, and server management</p>
</div>
<span class="internal-arrow">→</span>
</a>

<a href="https://chat.cgenomicslab.org/" target="_blank" class="internal-card">
<div class="internal-icon">
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
</svg>
</div>
<div class="internal-info">
<h3>Lab Chat</h3>
<p>Team messaging and communication</p>
</div>
<span class="internal-arrow">→</span>
</a>

<a href="https://jupyter.cgenomicslab.org/" target="_blank" class="internal-card">
<div class="internal-icon">
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<polyline points="16 18 22 12 16 6"></polyline>
<polyline points="8 6 2 12 8 18"></polyline>
</svg>
</div>
<div class="internal-info">
<h3>JupyterHub</h3>
<p>Computational notebooks and data analysis</p>
</div>
<span class="internal-arrow">→</span>
</a>

</div>

<div class="internal-note" style="margin-top: 2rem; padding: 1rem; background: #f9f9f9; border-radius: 8px; font-size: 0.9rem; color: #666;">
<strong>Note:</strong> Access to these services may require being on the lab network or using VPN. Contact the lab administrator if you need access.
</div>

<a href="/" class="section-link" style="margin-top: 2rem; display: inline-block;">← Back to home</a>

</section>
</div>

<style>
.internal-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
}

.internal-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.25rem;
    background: #fff;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease;
}

.internal-card:hover {
    border-color: #B9375E;
    box-shadow: 0 2px 8px rgba(185, 55, 94, 0.1);
}

.internal-card:hover .internal-arrow {
    transform: translateX(4px);
    color: #B9375E;
}

.internal-icon {
    width: 48px;
    height: 48px;
    min-width: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f5f5f5;
    border-radius: 8px;
    color: #666;
}

.internal-card:hover .internal-icon {
    background: #FFE0E9;
    color: #B9375E;
}

.internal-icon svg {
    width: 24px;
    height: 24px;
}

.internal-info {
    flex: 1;
}

.internal-info h3 {
    margin: 0 0 0.25rem 0;
    font-size: 1rem;
    font-weight: 500;
    color: #333;
}

.internal-info p {
    margin: 0;
    font-size: 0.85rem;
    color: #888;
}

.internal-arrow {
    font-size: 1.25rem;
    color: #ccc;
    transition: all 0.2s ease;
}
</style>
