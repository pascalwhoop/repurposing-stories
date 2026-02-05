# The Mechanism: How Zidovudine Works Against HIV

## The Molecular Target: HIV Reverse Transcriptase

### HIV Lifecycle and the Critical Enzyme

To understand how AZT works, we must first understand HIV's unique replication strategy:

**1. Viral Entry**: HIV infects CD4+ T-lymphocytes (helper T cells) and other immune cells by binding to CD4 receptors and chemokine co-receptors (CCR5 or CXCR4) on the cell surface.

**2. Reverse Transcription (THE CRITICAL STEP)**: Unlike most viruses, HIV carries its genetic information as RNA, not DNA. To integrate into the host cell's genome, HIV must first convert its RNA into DNA using a viral enzyme called **reverse transcriptase**.[^1][^2]

**3. Integration**: The newly synthesized viral DNA integrates into the host cell's chromosomes.

**4. Viral Protein Production**: Host cell machinery produces new viral proteins.

**5. Assembly and Release**: New virus particles assemble and bud from the infected cell.

**The Vulnerability**: Reverse transcriptase is unique to retroviruses—human cells don't have this enzyme. This makes it an ideal drug target, as inhibiting reverse transcriptase selectively disrupts HIV without directly affecting normal human cellular processes.

### What is Reverse Transcriptase?

**Function**: Reverse transcriptase is a viral enzyme that synthesizes DNA from an RNA template—the reverse of the normal cellular process (DNA → RNA).

**Structure**: The enzyme is a heterodimer composed of p66 and p51 subunits, with the p66 subunit containing:
- **Polymerase domain**: Synthesizes DNA
- **RNase H domain**: Degrades RNA template after DNA synthesis
- **Connection domain**: Links the two functional domains

**Process**:
1. Reverse transcriptase binds to viral RNA
2. Synthesizes complementary DNA (cDNA) using RNA as template
3. Degrades the original RNA template
4. Synthesizes second DNA strand to create double-stranded DNA
5. This DNA is then transported to nucleus for integration

**The Key Point**: Reverse transcriptase uses nucleosides (the building blocks of DNA) to construct the viral DNA chain. This is where AZT intervenes.

## AZT's Mechanism of Action

### Step 1: Cellular Uptake and Activation

**Cellular Entry**: AZT (3'-azido-3'-deoxythymidine) is a small molecule that can cross cell membranes and enter HIV-infected cells through passive diffusion and nucleoside transporters.[^3]

**Phosphorylation Cascade**: Once inside the cell, AZT undergoes three phosphorylation steps to become active:

1. **First phosphorylation** (rate-limiting step):
   - Enzyme: Cellular thymidine kinase (TK)
   - Product: AZT-monophosphate (AZT-MP)

2. **Second phosphorylation**:
   - Enzyme: Thymidylate kinase
   - Product: AZT-diphosphate (AZT-DP)

3. **Third phosphorylation**:
   - Enzyme: Nucleoside diphosphate kinase
   - Product: AZT-triphosphate (AZT-TP or AZTTP)

**Active Form**: Only AZT-triphosphate (AZTTP) has anti-HIV activity. The unphosphorylated form (AZT) is inactive.[^1][^4]

**Intracellular Accumulation**: Studies show that AZT is preferentially activated to its triphosphate form at a 3:1 ratio in human T-lymphocytes compared to monocytes from the same individual, explaining its particular efficacy in T-cells, HIV's primary target.[^5]

### Step 2: Competitive Inhibition of Reverse Transcriptase

**Substrate Competition**: AZTTP competes with the natural nucleoside triphosphate, thymidine triphosphate (TTP), for incorporation into the growing viral DNA chain by HIV reverse transcriptase.[^1][^2]

**Structural Similarity**: AZTTP closely resembles natural TTP:
- Same sugar-phosphate backbone
- Same thymine base
- Key difference: azido group (-N₃) at the 3' position instead of hydroxyl group (-OH)

**Preferential Binding**: HIV reverse transcriptase has **higher affinity for AZTTP than for natural TTP**, providing selectivity. Studies demonstrate that AZTTP is a more effective substrate for viral reverse transcriptase than for human DNA polymerases.[^1][^6]

**Incorporation**: When reverse transcriptase encounters AZTTP, it incorporates it into the growing DNA chain, mistaking it for natural TTP.

### Step 3: DNA Chain Termination

**The Critical Mechanism**: Once AZTTP is incorporated into viral DNA, the azido group at the 3' position prevents further DNA synthesis.[^1][^2]

**Why Chain Termination Occurs**:
- DNA synthesis proceeds in the 5' to 3' direction
- Each new nucleotide is added by forming a phosphodiester bond between:
  - The 3'-hydroxyl group (-OH) of the previous nucleotide, AND
  - The 5'-triphosphate group of the incoming nucleotide
- **AZT lacks the 3'-hydroxyl group** (replaced by azido group)
- Without the 3'-OH, no phosphodiester bond can form
- DNA synthesis stops immediately

**Result**: The incomplete viral DNA cannot integrate into the host chromosome, preventing productive infection.

## Selectivity: Why AZT Affects HIV More Than Human Cells

### Differential Enzyme Affinity

**HIV Reverse Transcriptase vs. Human DNA Polymerases**:

HIV reverse transcriptase has approximately **100-fold higher affinity** for AZTTP compared to human DNA polymerase α (the main replicative polymerase).[^6] This selectivity explains why AZT can inhibit HIV at concentrations that cause relatively limited damage to host cells.

**Measured Selectivity**:
- IC₅₀ (concentration inhibiting 50% of enzyme activity) for HIV RT: ~0.01-0.04 μM AZTTP
- IC₅₀ for human DNA polymerase α: ~1-3 μM AZTTP
- **Selectivity index**: 30-300 fold (varies by study and conditions)[^6]

### Mechanism of Selectivity

Several factors contribute to AZT's selectivity for viral vs. human DNA synthesis:

**1. Enzyme Structure Differences**:
- HIV reverse transcriptase active site has different geometry than human polymerases
- Binding pocket accommodates azido group more readily
- Different amino acid residues in substrate binding region

**2. Proofreading Capability**:
- Human DNA polymerases have 3' to 5' exonuclease activity (proofreading)
- Can potentially remove incorrectly incorporated AZT
- HIV reverse transcriptase **lacks proofreading activity**
- Cannot remove AZT once incorporated, making chain termination permanent

**3. DNA Synthesis Rate**:
- HIV replicates rapidly in infected cells
- High rate of reverse transcription
- More opportunities for AZTTP incorporation
- Human cells divide more slowly (except bone marrow, intestinal lining—explaining AZT toxicity in these tissues)

**4. Mitochondrial DNA Polymerase γ (Toxicity Mechanism)**:
- AZT also inhibits mitochondrial DNA polymerase γ
- This causes mitochondrial toxicity (see below)
- Explains many of AZT's side effects[^7]

## The Blood-Brain Barrier Penetration

**Unique Property**: Unlike many antiretroviral drugs, AZT crosses the blood-brain barrier effectively.[^8]

**Mechanism**:
- Small molecular size (267 g/mol)
- Moderate lipophilicity
- Not a substrate for major efflux transporters (initially)
- Passive diffusion across endothelial cell membranes

**Clinical Significance**:
- HIV infects cells in the central nervous system (CNS)
- Can cause AIDS dementia complex and other neurological complications
- AZT was shown to improve neuropsychological, CSF, and neuropathologic evaluations in HIV dementia patients
- Optimal response requires higher (but less tolerated) dosages for CNS effects[^8]

**CSF Concentrations**: Cerebrospinal fluid levels of AZT reach approximately 60% of plasma concentrations, sufficient for anti-HIV activity in the CNS.

## Pharmacokinetics and Metabolism

### Absorption and Distribution

**Oral Bioavailability**: ~60-70% after oral administration
**Peak Plasma Concentrations**: 30-90 minutes after oral dose
**Half-Life**: ~1 hour in plasma (short half-life necessitated frequent dosing)
**Intracellular Half-Life**: 3-7 hours for AZTTP (longer than plasma half-life, allowing some forgiveness for missed doses)
**Distribution**: Widely distributed throughout body, including CNS

### Metabolism

**Primary Pathway**: Glucuronidation in the liver
- Enzyme: UDP-glucuronosyltransferase (UGT)
- Product: AZT-glucuronide (inactive metabolite)
- Excreted in urine

**Minimal CYP450 Involvement**: Unlike many drugs, AZT is not metabolized by cytochrome P450 enzymes, reducing drug-drug interaction potential.

### Elimination

**Renal Excretion**:
- ~75% excreted in urine (mostly as glucuronide conjugate)
- ~15-20% excreted as unchanged AZT
- Dose adjustment required in renal impairment

## Limitations of the Mechanism

### Drug Resistance Mechanisms

HIV can develop resistance to AZT through mutations in the reverse transcriptase gene. The primary resistance mutations occur at specific codons:[^9][^10]

**Thymidine Analog Mutations (TAMs)**:
- M41L (methionine to leucine at position 41)
- D67N (aspartate to asparagine at position 67)
- K70R (lysine to arginine at position 70)
- L210W (leucine to tryptophan at position 210)
- T215Y/F (threonine to tyrosine or phenylalanine at position 215)
- K219Q/E (lysine to glutamine or glutamate at position 219)

**Mechanism of Resistance**:
1. **Altered binding**: Mutations change the reverse transcriptase active site, reducing AZTTP binding affinity while maintaining TTP binding
2. **ATP-mediated excision**: Some mutations enable reverse transcriptase to use ATP to remove incorporated AZT from the DNA chain (pyrophosphorolysis), allowing DNA synthesis to continue[^9]

**Clinical Impact**:
- Resistance develops in most patients on AZT monotherapy within 6-12 months
- Accumulation of multiple mutations confers high-level resistance
- Cross-resistance to other thymidine analogs (d4T, stavudine)

### Mitochondrial Toxicity

**Mechanism of Toxicity**: While selective for HIV RT over nuclear DNA polymerases, AZT also inhibits mitochondrial DNA polymerase γ (pol γ), the enzyme responsible for replicating mitochondrial DNA.[^7][^11]

**Consequences**:
1. **Mitochondrial DNA depletion**: Reduced mtDNA copy number
2. **Impaired oxidative phosphorylation**: Energy production decreases
3. **Tissue-specific effects**: Organs with high energy demands (muscle, liver, bone marrow) particularly affected

**Clinical Manifestations**:
- **Myopathy**: Muscle weakness and pain from mitochondrial dysfunction in muscle tissue
- **Neuropathy**: Peripheral nerve damage
- **Lipodystrophy**: Fat redistribution syndrome
- **Lactic acidosis**: Impaired lactate metabolism (rare but serious)[^7][^11]

**Long-Term Recognition**: These mitochondrial toxicities only became fully apparent after years of AZT use, contributing to its replacement by newer NRTIs with better mitochondrial safety profiles.

### Bone Marrow Suppression

**Mechanism**: AZT affects rapidly dividing bone marrow cells:
1. Incorporated into cellular DNA during hematopoiesis
2. Inhibits DNA synthesis in progenitor cells
3. Reduces production of blood cells

**Clinical Effects**:
- **Anemia**: Reduced red blood cell production (most common, ~30-40% of patients)
- **Neutropenia**: Reduced white blood cell counts
- **Thrombocytopenia**: Reduced platelet counts (less common)

**Management**: Dose reduction, treatment interruption, or supportive care with erythropoietin (EPO) or granulocyte colony-stimulating factor (G-CSF).

### Decreased Thymidine Kinase Activity

**Cellular Resistance Mechanism**: Prolonged AZT treatment can reduce cellular thymidine kinase (TK) activity in lymphocytes, the enzyme that performs the first, rate-limiting phosphorylation step of AZT activation.[^12][^13]

**Consequence**:
- Reduced conversion of AZT to active AZTTP
- Subtherapeutic intracellular drug concentrations
- Potential for "cellular resistance" distinct from viral resistance
- May contribute to treatment failure independent of viral mutations

## Simple Analogy for Non-Scientists

Think of HIV as a copycat that infiltrates your immune system's command centers (T-cells). To blend in and take control, HIV must translate its RNA genetic instructions into DNA that can be inserted into the cell's control room.

Reverse transcriptase is HIV's translator—it reads the viral RNA and writes out DNA instructions. This DNA translation process requires building blocks called nucleosides, which the translator assembles in a specific sequence, like beads on a string.

AZT is a sabotaged building block. It looks almost identical to a normal thymidine building block, so reverse transcriptase picks it up and adds it to the growing chain. But AZT is missing a critical connector piece (the 3'-hydroxyl group). Once AZT gets added to the chain, the next building block can't attach. The chain stops growing. The translation fails. Without complete DNA instructions, HIV can't take over the cell.

Human cells have their own translators (DNA polymerases), but they're much pickier about building blocks and less likely to grab the sabotaged AZT. This selectivity means HIV gets blocked more than human cells—though not perfectly, which explains AZT's side effects.

Unfortunately, HIV mutates rapidly. Over time, its translator (reverse transcriptase) can change shape slightly, learning to reject the sabotaged AZT building block while still accepting natural ones. This is drug resistance, and why AZT alone eventually fails—leading to combination therapy with multiple sabotaged building blocks that work in different ways.

---

[^1]: https://pubmed.ncbi.nlm.nih.gov/12023803/ - Gaudreau S et al., "Interaction of AZT with human serum albumin," J Biomol Struct Dyn 2002

[^2]: https://pubmed.ncbi.nlm.nih.gov/3322638/ - Tartaglione TA and Collier AC, "Development of antiviral agents for the treatment of HIV infection," Clin Pharm 1987

[^3]: https://pubmed.ncbi.nlm.nih.gov/25317835/ - Palafox MA, "Structure and conformational analysis of the anti-HIV reverse transcriptase inhibitor AZT using MP2 and DFT methods," Phys Chem Chem Phys 2014

[^4]: https://pubmed.ncbi.nlm.nih.gov/10904870/ - Periclou AP et al., "Pharmacodynamic studies of didanosine alone and in combination with azidothymidine in human T-cells," In Vivo 2000

[^5]: https://pubmed.ncbi.nlm.nih.gov/10904870/ - Periclou AP et al., "Pharmacodynamic studies (PD) of didanosine (ddI) alone and in combination with azidothymidine (AZT)," In Vivo 2000

[^6]: https://pubmed.ncbi.nlm.nih.gov/17092793/ - Arts EJ et al., "Mechanisms of clinical resistance by HIV-I variants to zidovudine," Drug Resist Updat 1998

[^7]: https://pubmed.ncbi.nlm.nih.gov/24067671/ - Gardner K et al., "HIV treatment and associated mitochondrial pathology: review of 25 years of in vitro, animal, and human studies," Toxicol Pathol 2014

[^8]: https://pubmed.ncbi.nlm.nih.gov/9101009/ - Melton ST et al., "Pharmacotherapy of HIV dementia," Ann Pharmacother 1997

[^9]: https://pubmed.ncbi.nlm.nih.gov/17092793/ - Arts EJ et al., "Mechanisms of clinical resistance by HIV-I variants to zidovudine and the paradox of reverse transcriptase sensitivity," Drug Resist Updat 1998

[^10]: https://pubmed.ncbi.nlm.nih.gov/7541064/ - Shafer RW et al., "Drug resistance and heterogeneous long-term virologic responses to zidovudine and didanosine combination therapy," J Infect Dis 1995

[^11]: https://pubmed.ncbi.nlm.nih.gov/22848552/ - Kunz A et al., "Zidovudine Exposure in HIV-1 Infected Tanzanian Women Increases Mitochondrial DNA Levels in Placenta and Umbilical Cords," PLoS One 2012

[^12]: https://pubmed.ncbi.nlm.nih.gov/9675644/ - Gröschel B et al., "Viral and cellular factors for resistance against antiretroviral agents," Intervirology 1997

[^13]: https://pubmed.ncbi.nlm.nih.gov/15646066/ - Turriziani O and Antonelli G, "Host factors and efficacy of antiretroviral treatment," New Microbiol 2004
