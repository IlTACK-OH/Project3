import pandas as pd
import numpy as np


col_name = [
    'Engine','Cycle',
    'Setting_1','Setting_2','Setting_3',
    'Fan_inlet_T',
    'LPC_outlet_T',
    'HPC_outlet_T',
    'LPT_outlet_T',
    'Fan_inlet_P',
    'bypass_duct_P',
    'HPC_outlet_P',
    'Physical_fan_speed',
    'Physical_core_speed',
    'Engine_P_R',
    'HPC_outlet_SP',
    'Ratio_of_fuel_flow',
    'Corrected_fan_S',
    'Corrected_core_S',
    'Bypass_R',
    'Burner_f_a_R',
    'BE',
    'Requried_fan_S',
    'Requried_fan_Conv_S',
    'HP_turbines_Caf',
    'LP_turbines_Caf'
]

train = pd.read_csv('./model/train_FD001.txt',sep = '\s+',names = col_name) 

Max_cycle = train.groupby(by='Engine').Cycle.max()
Max_cycle_df = pd.DataFrame(Max_cycle)

train['Max_cycle']=train.merge(Max_cycle_df,left_on='Engine',right_on='Engine').iloc[:,-1]
drop_line=np.quantile(train['Max_cycle'],0.9)
drop_index = train['Max_cycle'][train['Max_cycle']>= drop_line].index
train.drop(index = drop_index,inplace=True)
train.reset_index(inplace=True,drop=True)

train['RUL'] = train['Max_cycle'] - train['Cycle']
train.drop(columns=['Max_cycle','Engine'],inplace=True)

corr = train.corr()
drop_cols = corr.RUL[corr.RUL.isnull()].index
train.drop(columns=drop_cols,inplace=True)
train.drop(columns=['Setting_1','Setting_2','bypass_duct_P'],inplace=True)

target = 'RUL'
features = train.drop(columns=target).columns
X = train[features]
y = train[target]
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline

pipe_XGB = make_pipeline(MinMaxScaler(),
                        RandomForestRegressor(random_state=42,n_estimators=391,max_depth=5))

pipe_XGB.fit(X, y)

import pickle 
with open('model.pickle','wb') as fw:
    pickle.dump(pipe_XGB, fw)