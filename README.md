# JNVST Data Analysis: Spatial Econometrics and Educational Equity

This repository contains the quantitative analysis of the **Jawahar Navodaya Vidyalaya Selection Test (JNVST)** dataset. Unlike state board examinations, the JNVST is nationally standardized and administered uniformly, providing a clean dependent variable free from localized grade inflation. This makes it an ideal proxy for measuring cognitive outcomes and educational parity across India.

---

## Research Framework (Tier 1)

The analysis is structured around four core pillars of inquiry, focusing on the spatial and demographic drivers of performance.

### 1. The Spatial Variance Paradox
We investigate the extreme divergence in performance across state lines using the JNVST as a benchmark.
* **Core Question:** Why does Bihar record a mean score of **97.2** while Puducherry scores **60.8** on the identical standardized instrument? 
* **Focus:** Is this variance driven by cultural educational premiums, institutional efficiency, or underlying socio-economic demographics?

### 2. Heterogeneity in the Gender Gap
Leveraging district-level cut-offs for Boys vs. Girls, we analyze the spatial distribution of gender parity.
* **Objective:** Map districts where the gender gap is reversed or absent.
* **Impact:** This serves as a standalone study on gender parity within high-stakes educational competition.

### 3. Stability of Quota Hierarchies
We examine the consistency of the institutional hierarchy (e.g., **OPEN-UR** vs. **RURAL-OBC**) across different geographies.
* **Analysis:** Does the ranking of these categories hold at the district level? 
* **Indicator:** Areas where the rural-urban gap collapses may signal localized convergence in school quality and educational infrastructure.

### 4. Rank Persistence (2025–2026 Panel)
Using a two-year panel, we compute rank correlations to distinguish between structural and idiosyncratic factors.
* **High Persistence:** Indicates that long-term structural factors dominate the results.
* **Low Persistence:** Suggests that outcomes are significantly influenced by measurement noise or transient shocks.

---

## Methodological Approach

### Spatial Autocorrelation
To determine the necessity of spatial econometrics versus OLS with State Fixed Effects (FE), we calculate **Moran’s I** to identify clustering among high-performing districts (e.g., Bihar, West Bengal, and Maharashtra):

$$I = \frac{n}{S_0} \frac{\sum_{i=1}^n \sum_{j=1}^n w_{ij}(z_i - \bar{z})(z_j - \bar{z})}{\sum_{i=1}^n (z_i - \bar{z})^2}$$

Where:
* $w_{ij}$ is the spatial weight matrix (contiguity or inverse distance).
* $z$ represents the district-level cut-off score.

### Empirical Strategy
* **Python:** Used for spatial data processing, Moran's I calculation, and heatmapping.
* **Stata:** Used for rigorous econometric modeling, including Fixed Effects (FE) and panel data analysis.

---

## Repository Structure

* `data/`: Contains cleaned JNVST cut-off scores and district-level demographics.
* `scripts/`: 
    * `.py`: Spatial clustering and visualization scripts.
    * `.do`: Stata scripts for econometric regressions and correlation analysis.
* `output/`: Regression tables, spatial weight matrices, and Moran's I scatterplots.

---

## Data Sources
The primary data is derived from official JNVST results. For supplemental variables (district GDP, literacy rates, etc.), the following databases are utilized:
* **RBI Database** (State-level finances)
* **FRED** (Macro-indicators)
* **CEIC** (Socio-economic data)
