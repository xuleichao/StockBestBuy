from flask import Flask
from datetime import  timedelta
from flask import render_template
from utils.dataframe_2_sql import update_db_data
from utils.KLG.graph_kl import graph_main
from flask import Flask,request
import pickle
from utils.dataframe_2_sql import df_in_db

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=0.1)

@app.route('/tagging')
def hello_world():
    result, code = graph_main()
    template = render_template('index.html', result=result, code=code)
    return template
	
@app.route('/receive')
def get_form():
    params_dct = dict(request.values)
    with open('./dataSets/data.temp', 'rb') as f:
        DF = pickle.load(f)
    df_in_db(DF[0], DF[1])
    new_dct = {}
    for i,j in params_dct.items():
        if 'dateList' not in i:
            continue
        new_dct[int(i[8: ])] = j.split('|')[1].strip()
    dct_sorted = sorted(new_dct.items(), key=lambda x: x[0])
    update_db_data(dct_sorted)
    return render_template('stop.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8998)
