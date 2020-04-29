import pandas as pd
import pickle
import os


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

def savetxt(filename):
    # print(filename)
    lstxt = []
    path = '../dataSets/stock_KL/'+filename
    txtpath = '../dataSets/feature/'+filename.split('.')[0]+'.txt'
    # with open(path, "rb") as f:
    #     f = f.read()
    f = open(path, 'rb').read()
    data = pickle.loads(f)
    # print(data.columns)
    df = data.values.tolist()
    for i in df[:-1]:
        # print(i[0])
        openprice = float(i[1].replace(',', ''))
        closeprice = float(i[4].replace(',', ''))
        maxprice = float(i[2].replace(',', ''))
        minprice = float(i[3].replace(',', ''))
        result = calculate(openprice, closeprice, maxprice, minprice)
        newresult = i[0] + ',' + ','.join(result)
        lstxt.append(newresult)
    # print(lstxt)
    ftxt = open(txtpath, 'w')
    for i in lstxt:
        ftxt.write(i + '\n')
    ftxt.close()

def savetxt2(filename):
    # print(filename)
    lstxt = []
    path = '../dataSets/stock_KL/'+filename
    txtpath = '../dataSets/feature/'+filename.split('.')[0]+'.txt'
    # with open(path, "rb") as f:
    #     f = f.read()
    f = open(path, 'rb').read()
    df = pickle.loads(f)
    # print(data.columns)
    #df = data.values.tolist() 不转换为list
    for i in range(df.shape[0]): # 遍历 dataframe 的方式
        series_data = df.iloc[i]
        # print(i[0])
        openprice = float(series_data['开盘'])
        closeprice = float(series_data['收盘'])
        maxprice = float(series_data['最高'])
        minprice = float(series_data['最低'])
        result = calculate(openprice, closeprice, maxprice, minprice)
        newresult = i[0] + ',' + ','.join(result)
        lstxt.append(newresult)
    # print(lstxt)
    ftxt = open(txtpath, 'w')
    for i in lstxt:
        ftxt.write(i + '\n')
    ftxt.close()

def savetxt3(filename):
    # print(filename)
    lstxt = []
    path = '../dataSets/stock_KL/'+filename
    txtpath = '../dataSets/feature/'+filename.split('.')[0]+'.txt'
    # with open(path, "rb") as f:
    #     f = f.read()
    f = open(path, 'rb').read()
    df = pickle.loads(f)
    # print(data.columns)
    # df = data.values.tolist() #不转换为list
    df['result'] = df.apply(lambda x: calculate(x["开盘"],
                                                x['收盘'],
                                                x['最高'],
                                                x['最低']))
    
    return df


if __name__ == '__main__':
    filepath = '../dataSets/stock_KL'
    pathlist = os.listdir(filepath)
    # print(pathlist)
    for i in pathlist:
        if i == "_ST联谊.dataframe":
            continue
        savetxt(i)
