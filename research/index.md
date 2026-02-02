---
title: Research
layout: default
group: research
---

<div class="container">
<section style="padding: 2rem 0;">

<h1 class="section-title" style="font-size: 1.5rem; margin-bottom: 1rem;">Research</h1>

<p class="research-intro" style="margin-bottom: 2.5rem; line-height: 1.7;">
Our research combines computational biology, comparative genomics, and single-cell transcriptomics to understand how biological complexity emerges and evolves. We study the molecular and cellular changes underlying major evolutionary transitions.
</p>

{::nomarkdown}
<div class="research-projects">

<div class="research-project">
<div class="project-figure">
<img src="/static/img/research/synaptic_diversity.png" alt="Synaptic neurotransmission diversity" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
<div class="figure-placeholder" style="display: none;">
<span>Figure: Synaptic Diversity</span>
</div>
</div>
<div class="project-content">
<h2>Diversity of Synaptic Neurotransmission</h2>
<p>
We study the synaptic machinery across animals and their relatives to understand the origins and diversification of neural signaling. By characterizing neurotransmission systems in fungi and other opisthokonts, we aim to infer the ancestral state of this fundamental cellular process.
</p>
<p>
Our approach integrates phylogenetics with single-cell RNA sequencing and functional data to build a comprehensive picture of how neurons communicate and how this communication system evolved.
</p>
<ul class="project-keywords">
<li>Synaptic proteins</li>
<li>Opisthokonta</li>
<li>Phylogenetics</li>
<li>scRNA-seq integration</li>
</ul>
</div>
</div>

<div class="research-project reverse">
<div class="project-figure">
<img src="/static/img/research/cell_type_evolution.png" alt="Cell type evolution" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
<div class="figure-placeholder" style="display: none;">
<span>Figure: Cell Type Evolution</span>
</div>
</div>
<div class="project-content">
<h2>Cell Type Evolution</h2>
<p>
We build cross-species cell atlases to trace the evolutionary history of cell types across animals. By comparing single-cell transcriptomic data from diverse organisms, we investigate how neuronal cell types originated and diversified.
</p>
<p>
This work addresses fundamental questions about the emergence of cellular complexity and the molecular signatures that define distinct cell populations.
</p>
<ul class="project-keywords">
<li>Cell atlases</li>
<li>Neuronal origins</li>
<li>Cell type diversification</li>
<li>Comparative transcriptomics</li>
</ul>
</div>
</div>

<div class="research-project">
<div class="project-figure">
<img src="/static/img/research/gpcr_evolution.png" alt="Signaling receptor evolution" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
<div class="figure-placeholder" style="display: none;">
<span>Figure: GPCR Evolution</span>
</div>
</div>
<div class="project-content">
<h2>Signaling Receptor Evolution</h2>
<p>
G protein-coupled receptors (GPCRs) mediate cellular responses to a vast array of signals. We study the phylogenetics of Class A and Class C GPCRs, with particular focus on olfactory receptors and glutamate signaling.
</p>
<p>
Using protein language models, we develop classifiers to predict olfactory receptor-odorant interactions. We reconstruct ancestral receptor sequences to understand how combinatorial coding emerged and expanded during evolution.
</p>
<ul class="project-keywords">
<li>GPCR phylogenetics</li>
<li>Olfactory receptors</li>
<li>Ancestral reconstruction</li>
<li>Protein language models</li>
</ul>
</div>
</div>

<div class="research-project reverse">
<div class="project-figure">
<img src="/static/img/research/coevolution.png" alt="Protein site co-evolution" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
<div class="figure-placeholder" style="display: none;">
<span>Figure: Co-evolution</span>
</div>
</div>
<div class="project-content">
<h2>Protein Site Co-evolution</h2>
<p>
We develop and apply statistical methods to detect co-evolving residues within and between proteins. These patterns of correlated evolution reveal functional constraints and interaction interfaces.
</p>
<p>
By combining co-evolution analysis with structural data and experimental information, we aim to predict protein function from sequence alone.
</p>
<ul class="project-keywords">
<li>Co-evolution statistics</li>
<li>Protein interactions</li>
<li>Sequence-function prediction</li>
<li>Structural biology</li>
</ul>
</div>
</div>

</div>
{:/nomarkdown}

<a href="/" class="section-link" style="margin-top: 2rem; display: inline-block;">← Back to home</a>

</section>
</div>

<style>
.research-projects {
    display: flex;
    flex-direction: column;
    gap: 3rem;
}

.research-project {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 2rem;
    align-items: start;
    padding-bottom: 3rem;
    border-bottom: 1px solid #eee;
}

.research-project:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.research-project.reverse {
    grid-template-columns: 1fr 300px;
}

.research-project.reverse .project-figure {
    order: 2;
}

.research-project.reverse .project-content {
    order: 1;
}

.project-figure {
    position: relative;
}

.project-figure img {
    width: 100%;
    border-radius: 8px;
    background: #f5f5f5;
}

.figure-placeholder {
    width: 100%;
    height: 200px;
    background: linear-gradient(135deg, #f8f8f8 0%, #f0f0f0 100%);
    border: 2px dashed #ddd;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #999;
    font-size: 0.9rem;
    text-align: center;
    padding: 1rem;
}

.project-content h2 {
    margin: 0 0 1rem 0;
    font-size: 1.25rem;
    font-weight: 500;
    color: #333;
}

.project-content p {
    margin: 0 0 1rem 0;
    line-height: 1.7;
    color: #555;
}

.project-keywords {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 1rem 0 0 0;
    padding: 0;
    list-style: none;
}

.project-keywords li {
    background: #f5f5f5;
    padding: 0.25rem 0.75rem;
    border-radius: 100px;
    font-size: 0.8rem;
    color: #666;
}

@media (max-width: 768px) {
    .research-project,
    .research-project.reverse {
        grid-template-columns: 1fr;
    }
    
    .research-project.reverse .project-figure,
    .research-project.reverse .project-content {
        order: unset;
    }
    
    .project-figure {
        max-width: 300px;
    }
}
</style>
