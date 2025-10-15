# 📊 Data Science Portfolio

Welcome! I'm Blaise, a Data Science student at UST with a passion for machine learning, financial analytics, and applied AI. This portfolio showcases selected projects, laboratory activities, and exercises demonstrating skills in Python, machine learning, data visualization, and more.

## Repository Overview
This repository contains topic-focused subfolders. Each folder typically includes one or more Jupyter notebooks and, when needed, supporting data or utility scripts.

Top-level folders:
- Anaplan Consolidation — Scripts for consolidating data from Anaplan exports.
- Constructive Heuristics Induction for Language Learning (CHILL) Replica — A small replica/experiment for CHILL parsing with Python scripts and a demo notebook.
- Error Based Learning — Notebook(s) demonstrating error-driven learning concepts; includes small train/test CSVs.
- Geospatial Analysis — Geospatial EDA and visualization with provided datasets (regions GeoJSON, population, median pay, rice consumption).
- Network Analysis — Network/graph analysis notebook and sample training JSON.
- Similarity Based Learning — Notebook exploring similarity-based methods, with sample Airbnb-like listings data.
- Student Depression Prediction — A classification project on a provided dataset.
- Targeted Wellness Identification via Classification and Evaluation (TWICE) — A self-harm detection project; includes data splits, a HuggingFace tokenizer/config, and a small Tagalog stopwords utility.
- Time Series — Time series analysis notebook and a supporting diagram.


## Project Highlights
- Similarity Based Learning
  - Notebook: Similarity Based Learning/Similarity_Based_Learning.ipynb
  - Focus: distance metrics, nearest neighbors, similarity-driven modeling.
- Error Based Learning
  - Notebook: Error Based Learning/Error_Based_Learning.ipynb
  - Focus: error-driven learning paradigms and evaluation using provided train/test CSVs.
- Geospatial Analysis
  - Notebook: Geospatial Analysis/Geospatial_Analysis.ipynb
  - Data: regions.0.1.json, population_by_location.csv, median_pay.csv, rice_consumption.csv
  - Focus: maps, choropleths, spatial joins, regional comparisons.
- Time Series
  - Notebook: Time Series/Time_Series_Analysis.ipynb
  - Focus: stationarity, decomposition, forecasting workflows.
- Network Analysis
  - Notebook: Network Analysis/Network_Analysis.ipynb
  - Focus: basic graph analytics and visualization.
- Student Depression Prediction
  - Notebook: Student Depression Prediction/Student_Depression_Prediction.ipynb
  - Focus: text/tabular classification and evaluation.
- TWICE: Targeted Wellness Identification via Classification and Evaluation
  - Notebook: Targeted Wellness Identification via Classification and Evaluation (TWICE)/main.ipynb
  - Utils: util/tl_stop_words.py
  - Model assets: twice_roberta_selfharm/* (tokenizer/config)
  - Data: harm_* splits, adversarial prompts and validation sets (English/Tagalog)
  - Focus: self-harm detection with transformer-based models and evaluation.
- CHILL Replica (Constructive Heuristics Induction for Language Learning)
  - Files: general_parser.py, ILP_parser.py, chill3.ipynb, sample.py, ph-brgy-list.json
  - Focus: rule induction/parsing experiments inspired by CHILL.
- Anaplan Consolidation
  - Script: Anaplan Consolidation/consolidate.py
  - Note: see Anaplan Consolidation/requirements.txt for dependencies.

## Reproducibility Notes
- Random seeds: Where applicable, notebooks set seeds for basic reproducibility; results can still vary by library versions.
- Environment: Consider creating a per-project virtual environment if you plan to install specific versions for a given notebook.

## Data and Privacy
- Included CSV/JSON files are provided strictly for educational and demonstration purposes. Some datasets are small samples derived for coursework.
- Please verify licensing/usage constraints before reusing any data or assets.

## How to Cite / Contact
- Author: Blaise Geronimo
- Email: bvgeronimo@gmail.com
- If you have questions or feedback, feel free to open an issue or reach out.

Last updated: 2025-10-15
