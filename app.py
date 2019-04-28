from flask import Flask
from flask import render_template
from utils.KLG.graph_kl import graph_main
from flask import Flask,request

app = Flask(__name__)

@app.route('/tagging')
def hello_world():
    result = graph_main()
    template = render_template('index.html', result=result, code='002400')
    return template
	
@app.route('/receive')
def get_form():
    params_dct = dict(request.values)
    
    new_dct = {}
    for i,j in params_dct.items():
        if 'dateList' not in i:
            continue
        new_dct[int(i[8: ])] = j.split('|')[1].strip()
    dct_sorted = sorted(new_dct.items(), key=lambda x: x[0])

    return render_template('stop.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8998)
