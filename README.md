# Lyrical NLP Analyzer
Analyze band lyrics using NLP and visualize thematic relationships in an interactive D3.js graph.

## Setup
1. `conda env create -f environment.yml`
2. `conda activate lyrics_env`
3. Create `.env` file with `GENIUS_ACCESS_TOKEN=your_token_here`

## Pipeline Execution
To ingest, process, analyze, and build the graph for a new band:
`python -m src.run_pipeline --band "Band Name" --songs 50 --topics 5`

## Exploration
Open `src/explore.py` in VS Code as a **Jupyter Notebook** to run deep-dive visualizations (PCA, Word Clouds, Temporal Analysis).

## Web Visualization
1. Build the data first (see Pipeline).
2. Start local server: `python -m http.server 8000`
3. Navigate to `http://localhost:8000/web/`

## Project Architecture
- **Stage 0 (Collect):** Genius API integration.
- **Stage 1 (Process):** SpaCy-based NLP cleaning and lemmatization.
- **Stage 2 (Analyze):** TF-IDF and NMF Topic Modeling.
- **Stage 3 (Graph):** NetworkX-based graph serialization.
- **Stage 4 (Visualize):** D3.js interactive frontend.

## Deployment Strategy
The pipeline generates static JSON datasets in `web/export/`. The frontend is a vanilla JS application that utilizes these datasets, allowing the site to be hosted entirely on GitHub Pages without server-side compute.

