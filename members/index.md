---
title: Members
layout: default
group: members
---

<div class="container">
<section style="padding: 2rem 0;">

<h1 class="section-title" style="font-size: 1.5rem; margin-bottom: 1.5rem;">Lab Members</h1>

{::nomarkdown}
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
{% if member.scholar or member.github or member.orcid %}
<div class="member-links">
{% if member.orcid %}<a href="https://orcid.org/{{ member.orcid }}" target="_blank" class="icon-link" title="ORCID"><svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zM7.369 4.378c.525 0 .947.431.947.947s-.422.947-.947.947a.95.95 0 0 1-.947-.947c0-.525.422-.947.947-.947zm-.722 3.038h1.444v10.041H6.647V7.416zm3.562 0h3.9c3.712 0 5.344 2.653 5.344 5.025 0 2.578-2.016 5.025-5.325 5.025h-3.919V7.416zm1.444 1.303v7.444h2.297c3.272 0 4.022-2.484 4.022-3.722 0-2.016-1.284-3.722-4.097-3.722h-2.222z"/></svg></a>{% endif %}
{% if member.scholar %}<a href="https://scholar.google.com/citations?user={{ member.scholar }}" target="_blank" class="icon-link" title="Google Scholar"><svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M12 24a7 7 0 1 1 0-14 7 7 0 0 1 0 14zm0-24L0 9.5l4.838 3.94A8 8 0 0 1 12 9a8 8 0 0 1 7.162 4.44L24 9.5z"/></svg></a>{% endif %}
{% if member.github %}<a href="https://github.com/{{ member.github }}" target="_blank" class="icon-link" title="GitHub"><svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg></a>{% endif %}
</div>
{% endif %}
</div>
{% endfor %}
</div>
{:/nomarkdown}

<!-- Lab Photo -->
<div class="lab-photo-section" style="margin: 3rem 0;">
<h3 class="alumni-title">Lab Photo</h3>
<img src="/static/img/lab/lab_photo.jpg" alt="CGLab Group Photo" style="width: 100%; max-width: 800px; border-radius: 8px;" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
<p style="display: none; color: #888; font-style: italic;">Add lab photo at: /static/img/lab/lab_photo.jpg</p>
</div>

{::nomarkdown}
<!-- Alumni Section -->
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
{:/nomarkdown}

<!-- Lab Timeline -->
<div class="timeline-section" style="margin-top: 3rem;">
<h3 class="alumni-title">Lab Timeline</h3>

<style>
.timeline-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}
.timeline-legend span {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}
.legend-box {
  display: inline-block;
  width: 14px;
  height: 14px;
  border-radius: 3px;
}
.timeline-row {
  display: flex;
  align-items: center;
  margin-bottom: 0.4rem;
}
.timeline-name {
  width: 100px;
  text-align: right;
  padding-right: 1rem;
  font-size: 0.9rem;
  color: #434343;
  font-weight: 500;
}
.timeline-bar {
  height: 14px;
  border-radius: 3px;
  min-width: 8px;
}
.timeline-date {
  padding-left: 0.75rem;
  font-size: 0.8rem;
  color: #666;
  white-space: nowrap;
}
.timeline-axis {
  display: flex;
  justify-content: space-between;
  margin-left: 100px;
  margin-top: 0.75rem;
  padding-right: 100px;
  font-size: 0.75rem;
  color: #888;
  border-top: 1px solid #ddd;
  padding-top: 0.5rem;
}
</style>

<div class="timeline-legend">
<span><span class="legend-box" style="background: #B9375E;"></span>Group Leader</span>
<span><span class="legend-box" style="background: #BE9A60;"></span>Postdoc</span>
<span><span class="legend-box" style="background: #e9c46a;"></span>PhD</span>
<span><span class="legend-box" style="background: #CEDDBB;"></span>MSc</span>
<span><span class="legend-box" style="background: #FFE0E9;"></span>Undergraduate</span>
</div>

{::nomarkdown}
<div class="timeline-container">
{% assign all_people = site.members | concat: site.alumni | sort: "startdate" %}
{% for member in all_people %}
{% assign pos = member.position | downcase %}
{% if pos contains "group leader" or pos contains "principal investigator" or pos contains "pi" %}
  {% assign barcolor = "#B9375E" %}
{% elsif pos contains "postdoc" %}
  {% assign barcolor = "#BE9A60" %}
{% elsif pos contains "phd" %}
  {% assign barcolor = "#e9c46a" %}
{% elsif pos contains "msc" or pos contains "master" %}
  {% assign barcolor = "#CEDDBB" %}
{% elsif pos contains "undergraduate" or pos contains "bsc" %}
  {% assign barcolor = "#FFE0E9" %}
{% else %}
  {% assign barcolor = "#434343" %}
{% endif %}
<div class="timeline-row">
<div class="timeline-name">{{ member.name | split: " " | first }}</div>
<div class="timeline-bar" style="background: {{ barcolor }}; margin-left: {% assign sy = member.startdate | date: '%Y' | plus: 0 %}{% assign sm = member.startdate | date: '%m' | plus: 0 %}{% assign startoff = sy | minus: 2024 | times: 100 | plus: sm | times: 8 %}{% if startoff < 0 %}{% assign startoff = 0 %}{% endif %}{{ startoff }}px; width: {% if member.enddate %}{% assign ey = member.enddate | date: '%Y' | plus: 0 %}{% assign em = member.enddate | date: '%m' | plus: 0 %}{% else %}{% assign ey = 2026 %}{% assign em = 2 %}{% endif %}{% assign months = ey | minus: sy | times: 12 | plus: em | minus: sm %}{% if months < 2 %}{% assign months = 2 %}{% endif %}{% assign barwidth = months | times: 8 %}{{ barwidth }}px;"></div>
<div class="timeline-date">{{ member.startdate | date: "%b %Y" }}–{% if member.enddate %}{{ member.enddate | date: "%b %Y" }}{% else %}present{% endif %}</div>
</div>
{% endfor %}
</div>
{:/nomarkdown}

<div class="timeline-axis">
<span>2024</span>
<span>2025</span>
<span>2026</span>
</div>

</div>

<a href="/" class="section-link" style="margin-top: 2rem; display: inline-block;">← Back to home</a>

</section>
</div>
