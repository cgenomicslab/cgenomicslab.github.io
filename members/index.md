---
title: Members
layout: default
group: members
---

<div class="container">
<section style="padding: 2rem 0;">

<h1 class="section-title" style="font-size: 1.5rem; margin-bottom: 1.5rem;">Lab Members</h1>

<div class="members-grid">
{% assign current_members = site.members | where_exp: "m", "m.enddate == nil" | sort: "startdate" %}
{% for member in current_members %}
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

<!-- Lab Photo -->
<div class="lab-photo-section" style="margin: 3rem 0;">
<h3 class="alumni-title">Lab Photo</h3>
<img src="/static/img/lab/lab_photo.jpg" alt="CGLab Group Photo" style="width: 100%; max-width: 800px; border-radius: 8px;" onerror="this.style.display='none'; this.parentElement.querySelector('.photo-placeholder').style.display='block';">
<p class="photo-placeholder" style="display: none; color: #888; font-style: italic;">Add lab photo at: /static/img/lab/lab_photo.jpg</p>
</div>

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

<!-- Lab Timeline -->
<div class="timeline-section" style="margin-top: 3rem;">
<h3 class="alumni-title">Lab Timeline</h3>
{% assign stretch = 60 %}
{% assign yheight = 16 %}
{% assign yspacing = 18 %}
{% assign fontsize = 12 %}
{% assign yearoffset = 2023 %}
{% assign majortick = 0.05 %}
{% assign minortick = 0.025 %}
{% assign legendboxsize = 20 %}
{% assign legendboxspacing = 24 %}
{% assign people = site.members | concat: site.alumni | sort: "startdate" %}
{% assign finalyear = "now" | date: "%Y" | plus: 1 %}
<svg width="100%" height="auto" viewBox="0 0 {{ finalyear | minus: yearoffset | plus: majortick | times: stretch }} {{ people.size | plus: 1 | times: yspacing | plus: 180 }}" xmlns="http://www.w3.org/2000/svg" style="max-width: 800px;">
{% assign i = 0 %}
{% for year in (yearoffset..finalyear)%}
  {% assign year5 = year | modulo: 5 %}
  {% if year5 == 0 %}
    {% assign tick = majortick %}
    <text x="{{ fontsize | divided_by: 4.0 | divided_by: stretch | plus: tick | plus: year | minus: yearoffset | times: stretch }}" y="{{ i | times: yspacing | plus: fontsize }}" font-family="sans-serif" font-size="{{ fontsize }}" fill="black">{{ year }}</text>
  {% else %}
    {% assign tick = minortick %}
  {% endif %}
  <rect x="{{ year | minus: yearoffset | times: stretch }}" y="0" width="{{ tick | times: stretch }}" height="{{ yheight }}" fill="black" />
{% endfor %}
{% assign i = i | plus: 1 %}
{% for member in people %}
{% assign tenures = member.startdate.size | minus: 1 %}
  {% for tenure in (0..tenures) %}
    {% assign startyear = member.startdate[tenure] | date: "%Y" | minus: yearoffset %}
    {% assign startmonth = member.startdate[tenure] | date: "%m" | minus: 1 | divided_by: 12.0 %}
    {% assign start = startyear | plus: startmonth %}
    {% if member.enddate[tenure] %}
      {% assign endyear = member.enddate[tenure] | date: "%Y" | minus: yearoffset %}
      {% assign endmonth = member.enddate[tenure] | date: "%m" | minus: 1 | divided_by: 12.0 %}
      {% assign end = endyear | plus: endmonth %}
    {% else %}
      {% assign endyear = "now" | date: "%Y" | minus: yearoffset %}
      {% assign endmonth = "now" | date: "%m" | minus: 1 | divided_by: 12.0 %}
      {% assign end = endyear | plus: endmonth %}
    {% endif %}
    {% assign duration = end | minus: start %}
    {% if duration < 0.083 %}
      {% assign duration = 0.083 %}
    {% endif %}
    {% if member.timeline_group %}
      {% assign position = member.timeline_group | downcase %}
    {% elsif member.timeline_positions %}
      {% assign position = member.timeline_positions[tenure] | downcase %}
    {% else %}
      {% assign position = member.position | downcase %}
    {% endif %}
    {% if position contains "principal investigator" or position contains "group leader" %}
      {% assign color = "#e63946" %}
    {% elsif position contains "postdoctoral" or position contains "postdoc" %}
      {% assign color = "#f4a261" %}
    {% elsif position contains "phd" or position contains "graduate student" %}
      {% assign color = "#e9c46a" %}
    {% elsif position contains "msc" or position contains "master" %}
      {% assign color = "#2a9d8f" %}
    {% elsif position contains "undergraduate" or position contains "bsc" %}
      {% assign color = "#a8dadc" %}
    {% elsif position contains "staff" or position contains "programmer" or position contains "technician" %}
      {% assign color = "#457b9d" %}
    {% elsif position contains "intern" or position contains "summer" or position contains "visitor" %}
      {% assign color = "#6c757d" %}
    {% else %}
      {% assign color = "#9b59b6" %}
    {% endif %}
    <rect x="{{ start | times: stretch }}" y="{{ i | times: yspacing }}" width="{{ duration | times: stretch }}" height="{{ yheight }}" fill="{{ color }}" rx="2" />
    {% if tenure == 0 %}
      <text text-anchor="end" x="{{ fontsize | divided_by: -4.0 | divided_by: stretch | plus: start | times: stretch | minus: 5 }}" y="{{ i | times: yspacing | plus: fontsize | minus: 2 }}" font-family="sans-serif" font-size="{{ fontsize }}" fill="#333">{% if member.timeline_name %}{{ member.timeline_name }}{% else %}{{ member.name | split: " " | first }}{% endif %}</text>
    {% endif %}
  {% endfor %}
{% assign i = i | plus: 1 %}
{% endfor %}

<!-- Legend -->
{% assign legendy = i | times: yspacing | plus: 20 %}
{% assign fontsize = 11 %}
<rect x="10" y="{{ legendy }}" width="{{ legendboxsize }}" height="{{ legendboxsize }}" fill="#e63946" rx="2" />
<text x="{{ legendboxsize | plus: 15 }}" y="{{ legendy | plus: 15 }}" font-family="sans-serif" font-size="{{ fontsize }}" fill="#333">Group Leader / PI</text>
{% assign legendy = legendy | plus: legendboxspacing %}
<rect x="10" y="{{ legendy }}" width="{{ legendboxsize }}" height="{{ legendboxsize }}" fill="#f4a261" rx="2" />
<text x="{{ legendboxsize | plus: 15 }}" y="{{ legendy | plus: 15 }}" font-family="sans-serif" font-size="{{ fontsize }}" fill="#333">Postdoctoral Fellow</text>
{% assign legendy = legendy | plus: legendboxspacing %}
<rect x="10" y="{{ legendy }}" width="{{ legendboxsize }}" height="{{ legendboxsize }}" fill="#e9c46a" rx="2" />
<text x="{{ legendboxsize | plus: 15 }}" y="{{ legendy | plus: 15 }}" font-family="sans-serif" font-size="{{ fontsize }}" fill="#333">PhD Student</text>
{% assign legendy = legendy | plus: legendboxspacing %}
<rect x="10" y="{{ legendy }}" width="{{ legendboxsize }}" height="{{ legendboxsize }}" fill="#2a9d8f" rx="2" />
<text x="{{ legendboxsize | plus: 15 }}" y="{{ legendy | plus: 15 }}" font-family="sans-serif" font-size="{{ fontsize }}" fill="#333">MSc Student</text>
{% assign legendy = legendy | plus: legendboxspacing %}
<rect x="10" y="{{ legendy }}" width="{{ legendboxsize }}" height="{{ legendboxsize }}" fill="#a8dadc" rx="2" />
<text x="{{ legendboxsize | plus: 15 }}" y="{{ legendy | plus: 15 }}" font-family="sans-serif" font-size="{{ fontsize }}" fill="#333">Undergraduate</text>
{% assign legendy = legendy | plus: legendboxspacing %}
<rect x="10" y="{{ legendy }}" width="{{ legendboxsize }}" height="{{ legendboxsize }}" fill="#457b9d" rx="2" />
<text x="{{ legendboxsize | plus: 15 }}" y="{{ legendy | plus: 15 }}" font-family="sans-serif" font-size="{{ fontsize }}" fill="#333">Staff / Technician</text>
{% assign legendy = legendy | plus: legendboxspacing %}
<rect x="10" y="{{ legendy }}" width="{{ legendboxsize }}" height="{{ legendboxsize }}" fill="#6c757d" rx="2" />
<text x="{{ legendboxsize | plus: 15 }}" y="{{ legendy | plus: 15 }}" font-family="sans-serif" font-size="{{ fontsize }}" fill="#333">Visitor / Intern</text>
</svg>
</div>

<a href="/" class="section-link" style="margin-top: 2rem; display: inline-block;">← Back to home</a>

</section>
</div>
