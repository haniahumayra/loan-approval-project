from flask import Flask, request, render_template
import pickle
import pandas as pd
import traceback

app = Flask(__name__)

model = pickle.load(open('loan_pipeline.pkl', 'rb'))

def clean_number(val):
    return float(str(val).replace('.', '').replace(',', ''))

def slik_to_cibil(slik_category):
    mapping = {
        'Kol 1': 800,
        'Kol 2': 650,
        'Kol 3': 550,
        'Kol 4': 450,
        'Kol 5': 350
    }
    return mapping.get(slik_category, 600)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form

        input_df = pd.DataFrame([{
            'no_of_dependents': int(data.get('no_of_dependents')),
            'education': data.get('education'),
            'self_employed': data.get('self_employed'),
            'income_annum': clean_number(data.get('income_annum')),
            'loan_amount': clean_number(data.get('loan_amount')),
            'loan_term': float(data.get('loan_term')),
            'cibil_score': float(slik_to_cibil(data.get('slik_category'))),
            'residential_assets_value': clean_number(data.get('residential_assets_value')),
            'commercial_assets_value': clean_number(data.get('commercial_assets_value')),
            'luxury_assets_value': clean_number(data.get('luxury_assets_value')),
            'bank_asset_value': clean_number(data.get('bank_asset_value'))
        }])

        prediction = model.predict(input_df)[0]

        if prediction == 1 or str(prediction).lower() == "approved":
            result_text = "Disetujui"
        else:
            result_text = "Ditolak"

        return render_template('index.html', prediction=result_text, inputs=data)


    except Exception as e:
        print("ERROR:", e)
        print(traceback.format_exc())
        return render_template('index.html', prediction="Error", inputs=request.form)

if __name__ == '__main__':
    app.run(debug=True)