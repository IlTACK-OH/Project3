from flask import Blueprint, render_template, request
import pandas as pd
import pickle

predict_bp = Blueprint('predict', __name__)
model = pickle.load(open('./model/model.pickle', 'rb'))

@predict_bp.route('/predict')
def predict():
    return render_template('index.html'), 200

@predict_bp.route('/predict', methods = ['POST'])
def predict_result():
    if request.method =='POST':
        S1 = float(request.form["S1"])
        S2 = float(request.form["S2"])
        S3 = float(request.form["S3"])
        S4 = float(request.form["S4"])
        S5 = float(request.form["S5"])
        S6 = float(request.form["S6"])
        S7 = float(request.form["S7"])
        S8 = float(request.form["S8"])
        S9 = float(request.form["S9"])
        S10 = float(request.form["S10"])
        S11 = float(request.form["S11"])
        S12 = float(request.form["S12"])
        S13 = float(request.form["S13"])
        S14 = float(request.form["S14"])
        S15 = float(request.form["S15"])

        predict_list = [[S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,S11,S12,S13,S14,S15]]

        col_name = ['Cycle', 'LPC_outlet_T', 'HPC_outlet_T', 'LPT_outlet_T', 'HPC_outlet_P',
        'Physical_fan_speed', 'Physical_core_speed', 'HPC_outlet_SP',
        'Ratio_of_fuel_flow', 'Corrected_fan_S', 'Corrected_core_S', 'Bypass_R',
        'BE', 'HP_turbines_Caf', 'LP_turbines_Caf']

        predict_df = pd.DataFrame(data=predict_list,columns=col_name)
        predict_value = int(model.predict(predict_df)[0])
        return render_template('index2.html',predict_value=predict_value)
