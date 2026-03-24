# Project Roadmap — Smart User Data Cleaner

> Last updated: 2026-03-24  
> Total duration: 12 weeks

---

## Phase 1 — Project Setup & Data Ingestion (Weeks 1–2)

### Tasks
- [ ] Initialise repo, add .gitignore, requirements.txt, README.md
- [ ] Create `src/` package tree with stub modules
- [ ] Write CSV loader (chardet encoding detection)
- [ ] Write JSON loader (records + column-oriented)
- [ ] Write Excel loader (openpyxl engine)
- [ ] Write SQLite/PostgreSQL loader (SQLAlchemy)
- [ ] Implement DataProfiler
- [ ] Add pre-commit hooks (Black, Flake8, isort)

### Technologies
`pandas`, `SQLAlchemy`, `openpyxl`, `chardet`, `pre-commit`, `pytest`

---

## Phase 2 — Cleaning Engine (Weeks 3–5)

### Tasks
- [ ] Missing value handler (mean/median/mode/constant/drop)
- [ ] Exact-match duplicate detection
- [ ] Fuzzy duplicate detection (thefuzz)
- [ ] Format standardisation (regex per column)
- [ ] Dtype casting with graceful error handling
- [ ] Date normalisation to ISO-8601

### Technologies
`pandas`, `thefuzz`, `python-dateutil`, `numpy`

---

## Phase 3 — Anomaly Detection & Rule Engine (Weeks 6–8)

### Tasks
- [ ] IQR-based outlier detection
- [ ] Z-score outlier detection
- [ ] Isolation Forest (scikit-learn)
- [ ] JSON rule engine (config/rules.json)
- [ ] Pydantic v2 schema validator
- [ ] Optional Great Expectations integration

### Technologies
`scikit-learn`, `pydantic>=2.0`, `scipy`, `great-expectations`

---

## Phase 4 — Reporting (Weeks 9–10)

### Tasks
- [ ] HTML report (Jinja2 template)
- [ ] PDF generation (WeasyPrint)
- [ ] Before/after diff log
- [ ] CSV export
- [ ] DB export via SQLAlchemy

### Technologies
`Jinja2`, `WeasyPrint`, `pandas`, `SQLAlchemy`

---

## Phase 5 — Interface & Deployment (Weeks 11–12)

### Tasks
- [ ] Typer CLI (clean/validate/report/profile)
- [ ] Streamlit dashboard or FastAPI
- [ ] pyproject.toml with entry point
- [ ] Dockerfile (multi-stage)
- [ ] GitHub Actions CI/CD
- [ ] Publish to TestPyPI

### Technologies
`typer`, `streamlit`, `Docker`, `GitHub Actions`

---

## Milestone Summary

| Milestone | Week | Criteria |
|-----------|------|----------|
| M1: Loaders functional | 2 | CSV/JSON/Excel/DB load without errors |
| M2: Cleaning complete | 5 | All cleaners pass unit tests |
| M3: Anomaly + rules | 8 | Rule engine processes rules.json |
| M4: Reports generated | 10 | HTML + PDF rendered |
| M5: CLI + packaging | 12 | pip install & docker run work |
