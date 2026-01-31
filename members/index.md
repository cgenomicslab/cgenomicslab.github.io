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

<div class="timeline-legend">
<span><span class="legend-box" style="background: #B9375E;"></span>Group Leader</span>
<span><span class="legend-box" style="background: #BE9A60;"></span>Postdoc</span>
<span><span class="legend-box" style="background: #e9c46a;"></span>PhD</span>
<span><span class="legend-box" style="background: #CEDDBB;"></span>MSc</span>
<span><span class="legend-box" style="background: #FFE0E9;"></span>Undergraduate</span>
</div>

<div class="timeline-container" id="timeline-container">
<!-- Timeline will be generated by JavaScript -->
</div>

<div class="timeline-axis" id="timeline-axis">
<!-- Axis will be generated by JavaScript -->
</div>

</div>

{::nomarkdown}
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Collect member data
    var members = [
        {% assign all_people = site.members | concat: site.alumni | sort: "startdate" %}
        {% for member in all_people %}
        {
            name: "{{ member.name | split: ' ' | first }}",
            fullName: "{{ member.name }}",
            position: "{{ member.position }}",
            startdate: "{{ member.startdate | date: '%Y-%m-%d' }}",
            enddate: "{{ member.enddate | date: '%Y-%m-%d' }}"
        }{% unless forloop.last %},{% endunless %}
        {% endfor %}
    ];
    
    // Timeline configuration
    var startYear = 2024;
    var endYear = new Date().getFullYear() + 1;
    var totalMonths = (endYear - startYear + 1) * 12;
    var containerWidth = document.getElementById('timeline-container').offsetWidth - 120; // account for name column
    var pixelsPerMonth = containerWidth / totalMonths;
    
    // Position colors
    function getColor(position) {
        var pos = position.toLowerCase();
        if (pos.includes('group leader') || pos.includes('principal investigator') || pos.includes(' pi')) return '#B9375E';
        if (pos.includes('postdoc')) return '#BE9A60';
        if (pos.includes('phd')) return '#e9c46a';
        if (pos.includes('msc') || pos.includes('master')) return '#CEDDBB';
        if (pos.includes('undergraduate') || pos.includes('bsc')) return '#FFE0E9';
        return '#434343';
    }
    
    // Generate timeline rows
    var container = document.getElementById('timeline-container');
    var html = '';
    
    members.forEach(function(member) {
        if (!member.startdate || member.startdate === '') return;
        
        var startParts = member.startdate.split('-');
        var startYear_m = parseInt(startParts[0]);
        var startMonth = parseInt(startParts[1]) || 1;
        
        var endYear_m, endMonth;
        if (member.enddate && member.enddate !== '') {
            var endParts = member.enddate.split('-');
            endYear_m = parseInt(endParts[0]);
            endMonth = parseInt(endParts[1]) || 12;
        } else {
            var now = new Date();
            endYear_m = now.getFullYear();
            endMonth = now.getMonth() + 1;
        }
        
        // Calculate positions
        var startOffset = ((startYear_m - startYear) * 12 + (startMonth - 1)) * pixelsPerMonth;
        var endOffset = ((endYear_m - startYear) * 12 + endMonth) * pixelsPerMonth;
        var barWidth = Math.max(endOffset - startOffset, 8);
        
        // Clamp values
        if (startOffset < 0) startOffset = 0;
        
        var color = getColor(member.position);
        var dateLabel = member.startdate.substring(0, 7) + ' – ' + (member.enddate ? member.enddate.substring(0, 7) : 'present');
        
        html += '<div class="timeline-row">';
        html += '<div class="timeline-name">' + member.name + '</div>';
        html += '<div class="timeline-bar-container">';
        html += '<div class="timeline-bar" style="background: ' + color + '; left: ' + startOffset + 'px; width: ' + barWidth + 'px;" title="' + member.fullName + ': ' + dateLabel + '"></div>';
        html += '</div>';
        html += '<div class="timeline-date">' + dateLabel + '</div>';
        html += '</div>';
    });
    
    container.innerHTML = html;
    
    // Generate axis
    var axis = document.getElementById('timeline-axis');
    var axisHtml = '';
    for (var y = startYear; y <= endYear; y++) {
        var leftPos = ((y - startYear) * 12) * pixelsPerMonth;
        axisHtml += '<span style="position: absolute; left: ' + leftPos + 'px;">' + y + '</span>';
    }
    axis.innerHTML = '<div class="axis-inner">' + axisHtml + '</div>';
});
</script>
{:/nomarkdown}

<a href="/" class="section-link" style="margin-top: 2rem; display: inline-block;">← Back to home</a>

</section>
</div>

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
.timeline-container {
  position: relative;
  margin-bottom: 0.5rem;
}
.timeline-row {
  display: flex;
  align-items: center;
  margin-bottom: 0.4rem;
  height: 22px;
}
.timeline-name {
  width: 80px;
  min-width: 80px;
  text-align: right;
  padding-right: 1rem;
  font-size: 0.85rem;
  color: #434343;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.timeline-bar-container {
  position: relative;
  flex: 1;
  height: 14px;
}
.timeline-bar {
  position: absolute;
  height: 14px;
  border-radius: 3px;
  min-width: 8px;
  cursor: pointer;
}
.timeline-bar:hover {
  opacity: 0.85;
  transform: scaleY(1.1);
}
.timeline-date {
  width: 140px;
  min-width: 140px;
  padding-left: 0.75rem;
  font-size: 0.75rem;
  color: #888;
  white-space: nowrap;
}
.timeline-axis {
  position: relative;
  margin-left: 80px;
  margin-right: 140px;
  padding-left: 1rem;
  height: 24px;
  border-top: 1px solid #ddd;
}
.axis-inner {
  position: relative;
  height: 100%;
}
.timeline-axis span {
  font-size: 0.75rem;
  color: #888;
  padding-top: 4px;
}
@media (max-width: 600px) {
  .timeline-name {
    width: 60px;
    min-width: 60px;
    font-size: 0.75rem;
  }
  .timeline-date {
    display: none;
  }
  .timeline-axis {
    margin-right: 0;
  }
}
</style>
