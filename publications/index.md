---
title: Publications
layout: default
group: publications
---
{::nomarkdown}
<div class="container">
<section class="pubs-page">

<h1 class="section-title">Publications</h1>
<p class="publications-intro">Work from CGLab at IMBB-FORTH. Earlier papers are on <a href="https://scholar.google.com/citations?user=YbX4E3cAAAAJ" target="_blank" rel="noopener noreferrer">Google Scholar</a>.</p>

{% assign by_year = site.publications | sort: "date" | reverse | group_by_exp: "p", "p.date | date: '%Y'" %}
{% for year in by_year %}
<h2 class="pub-year">{{ year.name }}</h2>
<div class="pub-list">
{% for p in year.items %}{% include pub-row.html pub=p %}{% endfor %}
</div>
{% endfor %}

<a href="/" class="section-link">← Back to home</a>

</section>
</div>
{:/nomarkdown}
