import pandas as pd
import pickle


def calculate(openprice, closeprice, maxprice, minprice):
    baseprice = maxprice - minprice
    if baseprice == 0:
        return '0%', '0%', '0%'

    if (closeprice-openprice)>0:
        uppershadowprice = maxprice - closeprice
        lowershadowprice = openprice - minprice
    else:
        uppershadowprice = maxprice - openprice
        lowershadowprice = closeprice - minprice


    substanceprice = closeprice - openprice
    upperpercent = "%0.f%%"%(uppershadowprice/baseprice*100)
    lowerpercent = "%0.f%%"%(lowershadowprice/baseprice*100)
    substancepercent = "%0.f%%"%(substanceprice/baseprice*100)

    return upperpercent,lowerpercent,substancepercent

if __name__ == '__main__':
    path = '../dataSets/stock_KL/省广集团.dataframe'
    f = open(path,'rb').read()
    data = pickle.loads(f)
    # print(data.columns)
    df = data.values.tolist()
    for i in df[:-1]:
        print(i[0])
        openprice = float(i[1])
        closeprice = float(i[4])
        maxprice = float(i[2])
        minprice = float(i[3])
        result = calculate(openprice, closeprice, maxprice, minprice)

        print(result)
