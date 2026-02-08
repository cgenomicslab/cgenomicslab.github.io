---
title: CGLab
layout: default
---

<section class="hero">
<div class="container">
<div class="hero-inner">
<div class="hero-content">
<h1>Comparative Genomics Lab @ IMBB-FORTH</h1>
<p class="hero-intro">
<a href="https://www.imbb.forth.gr/en/research/Alexandros-Pittis.62/" target="_blank">CGLab</a>
is based at the Institute of Molecular Biology and Biotechnology of the Foundation for Research and Technology Hellas
(<a href="https://www.imbb.forth.gr/" target="_blank">IMBB-FORTH</a>) in Heraklion, Crete. We are part of the
<a href="https://www.imbb.forth.gr/en/research/lab-Evolution-Development-Cell-Biology.4/" target="_blank">Evolution, Development &amp; Cell Biology</a> division.
</p>
</div>
<div class="hero-figure">
<img src="/static/img/logo/4squares.png" alt="Comparative Genomics" onerror="this.style.display='none'; this.parentElement.innerHTML='Add image:<br>/static/img/logo/<br>4squares.png';">
</div>
</div>
</div>
</section>
<section id="research">
<div class="container">
<h2 class="section-title">Research</h2>
<p class="research-intro">
<strong>Sequence</strong> and <strong>functional diversity</strong>, <strong>genome</strong>, <strong>protein/gene family</strong>, and <strong>cellular evolution</strong>. We are particularly focused on <strong>neural protein machinery</strong>, and work on understanding its roots and diversification in animals.
</p>
<div class="research-areas">
<div class="research-area">
<h3>Comparative Genomics</h3>
<p>We analyze genome sequences in different scales across the Tree of Life to uncover evolutionary patterns and genomic innovations linked to phenotypes and traits.</p>
</div>
<div class="research-area">
<h3>Gene Family Evolution</h3>
<p>Analyzing thoroughly gene families and their evolution to understand how molecular functions and ultimately biological systems emerged and diversify.</p>
</div>
<div class="research-area">
<h3>Molecular genetics</h3>
<p>Functional genetics to characterize gene functions and test evolutionary hypotheses. We use extensively the genetic tools of the model fungus <i>Aspergillus nidulans</i>.</p>
</div>
<div class="research-area">
<h3>Single-Cell Transcriptomics</h3>
<p>Applying single-cell and single-nucleus RNA sequencing to characterize cellular diversity and evolution. We also largely focus on integrating gene evolution to understand how gene regulation changes after gene duplication, as a model of neo- / sub-functionalization.</p>
</div>
<div class="research-area">
<h3>Computational Methods</h3>
<p>Developing computational and statistical frameworks to extract insights from large-scale datasets.</p>
</div>
</div>
<a href="/research" class="section-link">More about our Projects →</a>
</div>
</section>
{::nomarkdown}
<section id="members">
<div class="container">
<h2 class="section-title">Members</h2>
<div class="members-grid">
{% assign current_members = site.members | where_exp: "m", "m.enddate == nil" %}

{% assign group_leaders = current_members | where_exp: "m", "m.position contains 'Group Leader' or m.position contains 'Principal Investigator' or m.position contains 'PI'" | sort: "name" | sort: "startdate" %}
{% assign postdocs = current_members | where_exp: "m", "m.position contains 'Postdoc' or m.position contains 'Post-doc' or m.position contains 'Postdoctoral'" | sort: "name" | sort: "startdate" %}
{% assign phds = current_members | where_exp: "m", "m.position contains 'PhD' or m.position contains 'Ph.D.' or m.position contains 'Doctoral'" | sort: "name" | sort: "startdate" %}
{% assign mscs = current_members | where_exp: "m", "m.position contains 'MSc' or m.position contains 'M.Sc.' or m.position contains 'Master'" | sort: "name" | sort: "startdate" %}
{% assign undergrads = current_members | where_exp: "m", "m.position contains 'Undergraduate' or m.position contains 'BSc' or m.position contains 'B.Sc.' or m.position contains 'Bachelor'" | sort: "name" | sort: "startdate" %}

{% assign categorized = "" | split: "" %}
{% for m in group_leaders %}{% assign categorized = categorized | push: m.name %}{% endfor %}
{% for m in postdocs %}{% assign categorized = categorized | push: m.name %}{% endfor %}
{% for m in phds %}{% assign categorized = categorized | push: m.name %}{% endfor %}
{% for m in mscs %}{% assign categorized = categorized | push: m.name %}{% endfor %}
{% for m in undergrads %}{% assign categorized = categorized | push: m.name %}{% endfor %}

{% assign others = "" | split: "" %}
{% for m in current_members %}
  {% unless categorized contains m.name %}
    {% assign others = others | push: m %}
  {% endunless %}
{% endfor %}
{% assign others = others | sort: "name" | sort: "startdate" %}

{% assign sorted_members = group_leaders | concat: postdocs | concat: phds | concat: mscs | concat: undergrads | concat: others %}

{% for member in sorted_members %}
<div class="member">
<div class="member-photo">
{% if member.image %}
<img src="{{ member.image }}" alt="{{ member.name }}" class="main-img">
{% if member.altimage %}
<img src="{{ member.altimage }}" alt="" class="alt-img">
{% endif %}
{% else %}
<div class="member-photo-placeholder">{{ member.name | slice: 0 }}{{ member.name | split: ' ' | last | slice: 0 }}</div>
{% endif %}
</div>
<div class="member-name"><a href="{{ member.url }}">{{ member.name }}</a></div>
<div class="member-position">{{ member.position }}</div>
{% if member.email %}
<button class="email-toggle-btn" onclick="toggleEmail(this)" data-email="{{ member.email }}" title="Show email">
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
<span class="email-label">email</span>
</button>
<div class="email-display" style="display: none;">
<span class="email-text"></span>
<button class="email-copy-btn" onclick="copyEmail(this)" title="Copy to clipboard">
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
</button>
</div>
{% endif %}
<div class="member-links">
{% if member.orcid %}<a href="https://orcid.org/{{ member.orcid }}" target="_blank" class="icon-link" title="ORCID"><svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zM7.369 4.378c.525 0 .947.431.947.947s-.422.947-.947.947a.95.95 0 0 1-.947-.947c0-.525.422-.947.947-.947zm-.722 3.038h1.444v10.041H6.647V7.416zm3.562 0h3.9c3.712 0 5.344 2.653 5.344 5.025 0 2.578-2.016 5.025-5.325 5.025h-3.919V7.416zm1.444 1.303v7.444h2.297c3.272 0 4.022-2.484 4.022-3.722 0-2.016-1.284-3.722-4.097-3.722h-2.222z"/></svg></a>{% endif %}
{% if member.scholar %}<a href="https://scholar.google.com/citations?user={{ member.scholar }}" target="_blank" class="icon-link" title="Google Scholar"><svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M12 24a7 7 0 1 1 0-14 7 7 0 0 1 0 14zm0-24L0 9.5l4.838 3.94A8 8 0 0 1 12 9a8 8 0 0 1 7.162 4.44L24 9.5z"/></svg></a>{% endif %}
{% if member.github %}<a href="https://github.com/{{ member.github }}" target="_blank" class="icon-link" title="GitHub"><svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg></a>{% endif %}
</div>
</div>
{% endfor %}
</div>
{% assign alumni = site.alumni | sort: "enddate" | reverse %}
{% if alumni.size > 0 %}
<div class="alumni-section">
<h3 class="alumni-title">Alumni</h3>
<div class="alumni-list">
{% for alum in alumni %}
<div class="alumni-item">
<a href="{{ alum.url }}">{{ alum.name }}</a>
<span class="alumni-position">({{ alum.position }}, {{ alum.startdate | date: "%Y" }}–{{ alum.enddate | date: "%Y" }})</span>
{% if alum.subsequent %}
<span class="alumni-now">→ now {{ alum.subsequent }}</span>
{% endif %}
</div>
{% endfor %}
</div>
</div>
{% endif %}
<a href="/members" class="section-link">All members →</a>
</div>
</section>

<script>
function toggleEmail(btn) {
    var email = btn.getAttribute('data-email');
    var display = btn.nextElementSibling;
    var emailText = display.querySelector('.email-text');

    if (display.style.display === 'none') {
        emailText.textContent = email;
        display.style.display = 'inline-flex';
        btn.style.display = 'none';
    }
}

function copyEmail(btn) {
    var emailText = btn.previousElementSibling.textContent;
    var display = btn.parentElement;
    var toggleBtn = display.previousElementSibling;

    // Try modern clipboard API first, with fallback
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(emailText).then(function() {
            showCopySuccess(btn, display, toggleBtn);
        }).catch(function() {
            // Fallback for clipboard API failure
            fallbackCopy(emailText, btn, display, toggleBtn);
        });
    } else {
        // Fallback for older browsers
        fallbackCopy(emailText, btn, display, toggleBtn);
    }
}

function fallbackCopy(text, btn, display, toggleBtn) {
    // Create temporary textarea
    var textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    textarea.style.top = '0';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();

    try {
        document.execCommand('copy');
        showCopySuccess(btn, display, toggleBtn);
    } catch (err) {
        console.error('Copy failed:', err);
        // Still close after a moment even if copy fails
        setTimeout(function() {
            display.style.display = 'none';
            toggleBtn.style.display = 'inline-flex';
        }, 2000);
    }

    document.body.removeChild(textarea);
}

function showCopySuccess(btn, display, toggleBtn) {
    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="2" width="12" height="12"><polyline points="20 6 9 17 4 12"></polyline></svg>';
    setTimeout(function() {
        display.style.display = 'none';
        toggleBtn.style.display = 'inline-flex';
        btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>';
    }, 1000);
}
</script>

<style>
.email-toggle-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.25rem 0.5rem;
    background: #f5f5f5;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    font-size: 0.75rem;
    color: #666;
    cursor: pointer;
    transition: all 0.2s;
    margin-top: 0.25rem;
}
.email-toggle-btn:hover {
    background: #FFE0E9;
    border-color: #B9375E;
    color: #B9375E;
}
.email-display {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.2rem 0.4rem;
    background: #f9f9f9;
    border-radius: 4px;
    font-size: 0.75rem;
    color: #555;
    margin-top: 0.25rem;
}
.email-text {
    font-family: monospace;
    font-size: 0.7rem;
    user-select: all;
}
.email-copy-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.2rem;
    background: transparent;
    border: none;
    cursor: pointer;
    color: #888;
    border-radius: 3px;
}
.email-copy-btn:hover {
    background: #e5e5e5;
    color: #333;
}
</style>
{:/nomarkdown}
<section id="join">
<div class="container">
<h2 class="section-title">Join</h2>
<div class="join-content">
<p>
We are always open to discuss with motivated people at all career stages who share an interest in computational and evolutionary biology.
</p>
<p>
If interested contact <a href="#contact">Alexandros Pittis</a> with a short CV and your interests.
</p>
</div>
<a href="/join" class="section-link">More information →</a>
</div>
</section>
<section id="publications">
<div class="container">
<h2 class="section-title">Publications</h2>
<p class="publications-intro">
For a publication list, see
<a href="https://scholar.google.com/citations?user=YbX4E3cAAAAJ" target="_blank">Google Scholar</a>.
</p>
</div>
</section>
<section id="contact">
<div class="container">
<h2 class="section-title">Contact</h2>
<div class="contact-simple">
<div class="contact-info">
<h3>Alexandros Pittis</h3>
<p>
Group Leader · IMBB-FORTH<br>
<a href="mailto:alexandros.pittis@gmail.com">alexandros.pittis@gmail.com</a><br>
<a href="mailto:alexandros.pittis@imbb.forth.gr">alexandros.pittis@imbb.forth.gr</a><br>
+30 2810 391024
</p>
<p class="contact-address">
Main Building, FORTH · Floor -2, Room Δ030<br>
N. Plastira 100, Vassilika Vouton<br>
70013 Heraklion, Crete
</p>
</div>
<div class="contact-map">
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3183.980555435395!2d25.069276075546192!3d35.30462035057078!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x149a570027ec31bd%3A0xaaccc8115f93751f!2sComparative%20Genomics%20Lab%20%40%20IMBB-FORTH!5e1!3m2!1sen!2sgr!4v1769297448751!5m2!1sen!2sgr" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
<a href="https://maps.app.goo.gl/zGpFGo7fDnC1gNFm7" target="_blank" class="map-link">Open in Google Maps ↗</a>
</div>
</div>
</div>
</section>

<style>
.contact-simple {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    align-items: start;
}
.contact-info h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
    font-weight: 500;
}
.contact-info p {
    margin: 0 0 1rem 0;
    line-height: 1.6;
}
.contact-info a {
    color: #B9375E;
}
.contact-address {
    color: #666;
    font-size: 0.9rem;
}
.contact-map {
    position: relative;
}
.contact-map iframe {
    width: 100%;
    height: 200px;
    border: none;
    border-radius: 8px;
}
.map-link {
    display: block;
    margin-top: 0.5rem;
    font-size: 0.85rem;
    color: #666;
}
@media (max-width: 768px) {
    .contact-simple {
        grid-template-columns: 1fr;
    }
}
</style>
