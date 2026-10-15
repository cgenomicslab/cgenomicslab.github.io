---
title: "KEDROS: A Comparative Genomics and High-Resolution Phylogenetic Profiling Workspace"
authors:
  - name: Athena Marougka
    member: marouga
  - name: Jaime Huerta-Cepas
    corresponding: true
  - name: Alexandros A. Pittis
    member: pittis
    corresponding: true
date: 2026-10-11
venue: bioRxiv
status: preprint
doi: 10.64898/2026.10.08.757521
pdf: https://www.biorxiv.org/content/10.64898/2026.10.08.757521v1.full.pdf
links:
  - label: Web tool
    url: https://kedros.cgenomicslab.org
themes: [tools]
thumb: /static/img/pubs/kedros-thumb.webp
figure: /static/img/pubs/kedros-fig.webp
figure_caption: "The KEDROS workspace: (A) home page and analysis modules; (B) high-resolution phylogenetic profiling of a gene tree split into 18 subclades at inferred duplications; (C) the same subclades on the gene tree (Fig. 1)."
---
Phylogenetic profiling infers gene function from the presence and absence of genes across genomes, but it loses resolution in eukaryotes, where many protein families contain several functionally distinct paralogs. Existing resources address parts of this problem separately: web services build trees for one family at a time, orthology databases provide precomputed orthologous groups for predefined species sets, and tree-profiling tools require users to supply their own trees and groupings. Here, we present KEDROS, a web platform that builds gene trees for any protein family across UniProt reference proteomes, splits each tree into subfamilies at inferred gene duplications, and profiles each subfamily separately. The organisms, the families and the taxonomic depth at which trees are split are all chosen by the user, so the same workflow serves any question that can be posed as a contrast between two sets of organisms: a pathogen and its host, a pest and non-target species, or lineages with and without a trait. KEDROS answers such contrasts at two levels. Across families and subfamilies, it ranks those present in one set and absent from the other, pointing to lineage-specific genes and candidate targets. Within a subfamily shared by both sets, it identifies amino acid positions that differ consistently between them and may underlie functional divergence, and displays them on AlphaFold structures. All analyses run in a web browser, with no installation or programming. Each of these steps exists in some form elsewhere, but to our knowledge no other resource runs them end to end, at the scale of whole proteomes, on organism sets defined by the user. We illustrate KEDROS with two cases. In the trypanothione reductase family of trypanosomatids, it recovers parasite-specific subfamilies and the substrate-binding substitutions that separate the parasite enzyme from human glutathione reductase. In the bacterial phylum Bacillota, it recovers the sporulation machinery from phenotype labels alone across 1,218 proteomes, and ranks an uncharacterized family among the strongest markers of the trait. KEDROS thus offers a general, code-free route from a comparative question to testable hypotheses about genes and residues. KEDROS is freely available at [kedros.cgenomicslab.org](https://kedros.cgenomicslab.org).
