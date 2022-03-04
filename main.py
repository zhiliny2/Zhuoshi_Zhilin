import requests
import datetime
import csv
import os
import time
import pandas as pd
import datetime
# 获取a股个股最新历史数据，最新在最前，每行为一天的数据
# format:DATE,收盘价,最高价,最低价,涨跌额,涨跌幅,换手率,成交量,成交金额,总市值,流通市值

def get_daily(code, start, end,filename):

    url_mod = "http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s"
    url = url_mod % (code, start, end)
    i=0
    while i<5:
        try:
            df = pd.read_csv(url, encoding='GB18030')
            df.to_csv(filename,mode='a+', encoding='utf-8-sig',header=None)
            break
        except:
            time.sleep(i)
            i+=1

    # print(df)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df = pd.read_excel('wind.xls',engine='xlrd',dtype=str)
    code_list_raw = list(df.iloc[:, 0])
    code_list=[]
    for code_raw in code_list_raw:
        flag=code_raw.split('.')[1]
        # 沪市前面加0，深市前面加1，比如0000001，是上证指数，1000001是中国平安
        if flag=='SZ':
            code_list.append('1'+code_raw.split('.')[0])
        else:
            code_list.append('0'+code_raw.split('.')[0])
    filename='2021-2022.csv'
    # 文件不存在则创建，并写入表头
    if not os.path.exists(filename):
        csv_head = ['#','日期', '股票代码', '名称', '收盘价', '最高价', '最低价', '开盘价', '前收盘', '涨跌额', '涨跌幅', '换手率', '成交量', '成交金额', '总市值', '流通市',
                '成交笔数']

        with open(filename, 'a+',encoding='utf-8-sig', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(csv_head)
    # 计算当前日期的前一天
    current_date = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    before_current_date = current_date - delta
    before_current_date=before_current_date.strftime('%Y%m%d')
    # get_daily函数第一个参数是股票代码，第二个参数是起始日期，第三个参数是结束日期，空的话表示最新，最后一个参数为存在本地的文件名
    for code in code_list:
        get_daily(code,before_current_date, '',filename)
        print(code,'done')

        # break

