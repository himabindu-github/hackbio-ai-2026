
# Exploring Genomics and Pathway Determinants of Drug Sensitivity in Cancer Cell Lines
This project analyzes pharmacogenomics data from the Genomics of Drug Sensitivity in Cancer (GDSC) database to identify how cellular pathways, tissue types, and multi-omic features dictate therapeutic responses in cancer cell lines.
## 📊 Dataset Profile
The analysis uses a comprehensive GDSC dataset containing 162,103 rows and 19 columns. It bridges the gap between drug compound potency and the molecular profiles of targeted cell lines.
Core Metadata Fields
•	Identifiers: COSMIC_ID, CELL_LINE_NAME, DRUG_ID, DRUG_NAME
•	Metrics: LN_IC50 (Potency), AUC (Efficacy), Z_SCORE (Standardized deviation)
•	Biological Context: TCGA_DESC, Cancer Type, GDSC Tissue descriptors 1 & 2, MSI_STATUS
•	Multi-Omics Features (Binary): CNA (Copy Number Alterations), Gene Expression, Methylation
•	Mechanistic Targets: TARGET, TARGET_PATHWAY
 
## 🔑 Key Insights & Findings
1. Drug Potency & Pathway Profiles
•	Broad vs. Selective Efficacy: The overall distribution of LN_IC50 values is left-skewed. Only a small subset of drugs exhibit high universal potency.
•	Top Performers: The most broadly effective drugs include Romidepsin, Bortezomib, and Sepantronium bromide.
•	Mechanism Matters: Grouping drugs by biological function reveals that targeting core proliferative machinery (Mitosis, DNA Replication) yields broad effectiveness. Inhibiting signaling pathways (RTK, PI3K/MAPK) results in highly variable, context-dependent responses.
2. Tissue & Cancer Type Sensitivities
•	Hematological vs. Solid: Hierarchical clustering separates cancer types into two major response profiles. Hematological malignancies (CLL, LAML, ALL, DLBC) are consistently highly sensitive to cell cycle and apoptotic agents. Solid tumors (PAAD, MESO, UCEC, LIHC) display widespread resistance and heterogeneous profiles.
•	Shared Biologies: Sub-clusters among distinct anatomical solid tumors indicate that drug sensitivity is heavily driven by shared underlying pathway dependencies rather than tissue origin.
3. Multi-Omic Influences & Class Imbalance
•	Data Limitation: Evaluating categorical features (CNA, Gene Expression, Methylation) revealed extreme class imbalances between modified ("Y") and unmodified ("N") groups across specific drug slices. This prevents reliable classical statistical testing.
•	Modest Drivers: Aggregate median shifts indicate that genomic changes (CNA) and epigenomic shifts (Methylation) show more stable and consistent influences on drug response distributions than global transcriptomic variations.
 
## 🛠️ Code Workflow & Implementation
The analysis pipeline is built entirely inside Python (optimized for Google Colab) across four sequential steps:
1.	Preprocessing & Normalization: Standardizes multi-format missing values (NA, null, ""), checks for row duplicates, strips whitespaces, and normalizes column headers into clean snake-case (IC50, TISSUE_DESC, GENE_EXPR).
2.	Descriptive Aggregations: Calculates robust baseline metrics (median and standard deviations) per drug and pathway to mitigate the skewing effects of outlier cell lines.
3.	Statistical Modeling & Correlation: Converts long-format trial metrics into a cell-line-by-drug pivot matrix to construct Pearson/Spearman correlation matrices.
4.	Visual Explorations: Generates custom distributions using matplotlib and seaborn (histograms, error-bar plots, boxplots, pathway scatterplots, and dual-metric clustered heatmaps).
 



