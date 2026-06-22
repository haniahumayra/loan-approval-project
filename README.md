# Group 7 — LoanCalc AI: Loan Approval Prediction Web App

A **Flask**-based web application that predicts loan approval eligibility in *real-time* using machine learning. This project compares several classification algorithms and deploys the best-performing **Gradient Boosting Classifier** packaged within a full preprocessing pipeline.

---

## Dataset

| Dataset | Rows | Features | Purpose |
|---|---|---|---|
| Loan Approval Dataset | 4,269 | 11 Financial Features + CIBIL Score | Model training & evaluation |

- **Split**: 80% Training (3,415 rows) & 20% Testing (854 rows)
- **Original Features**: `no_of_dependents`, `education`, `self_employed`, `income_annum`, `loan_amount`, `loan_term`, `cibil_score` (350–800), `residential_assets_value`, `commercial_assets_value`, `luxury_assets_value`, `bank_asset_value`

> **Note:** The original dataset uses a numeric `cibil_score` column (350–800). In this application, users select a **SLIK status** (Kol 1–5) from a dropdown, which is automatically converted to the equivalent CIBIL score by the backend before being passed to the model.

---

## How to Run

### Option 1 — Use the Pre-built Model

The model pipeline file (`loan_pipeline.pkl`) is already included and ready to use.

```bash
# Activate virtual environment
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

Access the application at: `http://localhost:5000`

---

### Option 2 — Rebuild the Model from Scratch

Use this option to retrain the model, for example if there is a library version mismatch or to reproduce the full analysis and model comparison pipeline.

```bash
# Create and activate a virtual environment (Python 3.8+)
py -3.x -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Open ML_Loan_Approval_Complete.ipynb
# Run all cells sequentially (via Jupyter, VS Code, or any compatible environment)
# A new pipeline will be exported to: loan_pipeline.pkl

# Start the Flask server
python app.py
```

Access the application at: `http://localhost:5000`

---

## Input Processing Flow

1. **Form Input** — The user fills in 11 features and selects a **SLIK status (Kol 1–5)**.
2. **SLIK → CIBIL Conversion** — The backend maps the selected SLIK status to a numeric CIBIL score before passing it to the model:

   | SLIK Status | Description | CIBIL Score |
   |---|---|---|
   | Kol 1 | Current / Performing | 800 |
   | Kol 2 | Special Mention | 650 |
   | Kol 3 | Substandard | 550 |
   | Kol 4 | Doubtful | 450 |
   | Kol 5 | Loss / Non-Performing | 350 |

3. **Pipeline** — Data is processed through `loan_pipeline.pkl`, which applies **SimpleImputer** (missing value handling) and **StandardScaler** (feature normalization).
4. **Prediction** — The **Gradient Boosting Classifier** outputs a final decision: **Approved** or **Rejected**.

---

## File Structure

```
Machine Learning FIX/
├── ML_Loan_Approval_Complete.ipynb  ← EDA, model comparison & pipeline export notebook
├── app.py                           ← Flask backend server (routing & controller)
├── loan_pipeline.pkl                ← Exported model pipeline file
├── requirements.txt                 ← Python dependencies
├── vercel.json                      ← Vercel deployment configuration
├── Procfile                         ← Production WSGI server configuration (Gunicorn)
├── pipeline_ml.txt                  ← ML pipeline architecture documentation
├── static/
│   ├── style.css                    ← Web interface styling
│   ├── script.js                    ← Frontend interaction logic (dropdowns, UI)
│   ├── logo_removebg.png            ← Application logo asset
│   └── background.jpg               ← Hero section background image
└── templates/
    ├── index.html                   ← Main page and prediction form
    └── about.html                   ← Team and project information page
```

---

## Troubleshooting

**`"Port 5000 is already in use"`** — Another process is occupying the port. Stop that process, or change the port in the last line of `app.py`:
```python
app.run(debug=True, port=8000)
```

**`"Model prediction error / Pickle error"`** — The installed version of `scikit-learn` does not match the version used to export the model. Align the version with `requirements.txt`, or re-run all cells in `ML_Loan_Approval_Complete.ipynb` to regenerate a compatible `loan_pipeline.pkl`.

**`"ModuleNotFoundError"`** — The virtual environment has not been activated. Run the `venv` activation command before executing `python app.py`.
