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
<img src="/static/img/research/synaptic_diversity.svg" alt="Synaptic neurotransmission diversity" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
<div class="figure-placeholder" style="display: none;">
<span>Figure: Synaptic Diversity</span>
</div>
</div>
<div class="project-content">
<h2>Diversity of Synaptic Neurotransmission <img src="/static/img/logo/elidek_logo_en.png" alt="HFRI funded" class="funding-logo"></h2>
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
<img src="/static/img/research/cell_type_evolution.svg" alt="Cell type evolution" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
<div class="figure-placeholder" style="display: none;">
<span>Figure: Cell Type Evolution</span>
</div>
</div>
<div class="project-content">
<h2>Cell Type Evolution <img src="/static/img/logo/elidek_logo_en.png" alt="HFRI funded" class="funding-logo"></h2>
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
<img src="/static/img/research/gpcr_evolution.svg" alt="GPCR and olfactory system evolution" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
<div class="figure-placeholder" style="display: none;">
<span>Figure: Olfactory System Evolution</span>
</div>
</div>
<div class="project-content">
<h2>Olfactory System Evolution</h2>
<p>
Olfactory receptors allow animals to detect and discriminate thousands of chemical compounds. We study the phylogenetics of olfactory GPCRs to understand how this sensory system expanded and diversified across animal lineages.
</p>
<p>
Using protein language models, we develop classifiers to predict olfactory receptor-odorant interactions. We reconstruct ancestral receptor sequences to understand how combinatorial coding emerged, enabling animals to perceive complex olfactory landscapes.
</p>
<ul class="project-keywords">
<li>Olfactory receptors</li>
<li>GPCR phylogenetics</li>
<li>Ancestral reconstruction</li>
<li>Protein language models</li>
</ul>
</div>
</div>

<div class="research-project reverse">
<div class="project-figure">
<img src="/static/img/research/glutamate.svg" alt="Glutamate signaling evolution" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
<div class="figure-placeholder" style="display: none;">
<span>Figure: Glutamate Signaling</span>
</div>
</div>
<div class="project-content">
<h2>Glutamate Signaling Evolution</h2>
<p>
Glutamate is the primary excitatory neurotransmitter in vertebrate nervous systems, acting through both ionotropic and metabotropic receptors. We trace the evolutionary history of glutamate signaling components across the tree of life.
</p>
<p>
By combining protein domain phylogenetics with single-cell expression data, we investigate how glutamate receptor families diversified and how their expression patterns differ across cell types and species.
</p>
<ul class="project-keywords">
<li>Glutamate receptors</li>
<li>iGluRs and mGluRs</li>
<li>Domain evolution</li>
<li>Cross-species expression</li>
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

.funding-logo {
    height: 20px;
    width: auto;
    vertical-align: middle;
    margin-left: 0.5rem;
    opacity: 0.8;
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
