#coding=utf-8

import datetime
import tushare as ts
import pymysql
import baostock as bs
import pandas as pd

import requests
import lxml
import re
import time
from lxml import etree

class StockDataOperator:
    token = ""
    ts_pro = None
    stock_code_list = []
    ip = None
    user = None
    password = None
    dbname = None
    stock_info = None

    def __init__(self):
        self.token = '212d8b49da92c719416a4e01e4c56938fe8c45dc1e024bc6a118e7d4'
        ts.set_token(self.token)
        self.ts_pro = ts.pro_api()

    def init_db_info(self, ip ='127.0.0.1', user = 'root', password = '', dbname = 'STOCKDB'):
        self.ip = ip
        self.user = user
        self.password = password
        self.dbname = dbname

    def load_stock_info(self):
        # 连接数据库
        db = pymysql.connect(host=self.ip, user=self.user, passwd=self.password, db=self.dbname, charset='utf8')
        cursor = db.cursor()

        try:
            sql_done_set = "SELECT * FROM STOCK_INFO ORDER BY STOCK_CODE"
            cursor.execute(sql_done_set)
            done_set = cursor.fetchall()
        except Exception as err:
            print(err)

        if len(done_set) == 0:
            return None

        cursor.close()
        db.close()
        return done_set

    def load_all_stock_code(self):
        # 连接数据库
        db = pymysql.connect(host=self.ip, user=self.user, passwd=self.password, db=self.dbname, charset='utf8')
        cursor = db.cursor()

        try:
            sql_done_set = "SELECT DISTINCT STOCK_CODE FROM STOCK_INFO ORDER BY STOCK_CODE"
            cursor.execute(sql_done_set)
            done_set = cursor.fetchall()
        except Exception as err:
            print(err)

        if len(done_set) == 0:
            return None

        stock_code_list = []
        for i in range(len(done_set)):
            stock_code_list.append(done_set[i][0])

        cursor.close()
        db.close()
        return stock_code_list

    def fetch_all_stock_code(self):
        stock_code_list = []
        self.stock_info = ts.get_stock_basics()


        for stock_code in self.stock_info.index:
            if stock_code.startswith('6'):
                stock_code_list.append(stock_code + ".SH")
            else:
                stock_code_list.append(stock_code + ".SZ")
        stock_code_list.sort()
        return stock_code_list

    # ['603912.SH','300666.SZ','300618.SZ','002049.SZ','300672.SZ']
    def append_stock_code(self, stock_code):
        self.stock_code_list.append(stock_code)

    # 日期, 开盘, 收盘, 最高, 最低, 成交量, 代码
    def load_stock_data(self, stock_code, require_type, start_dt, end_dt, order_by='ASC'):
        # 建立数据库连接，获取日线基础行情(开盘价，收盘价，最高价，最低价，成交量，成交额)
        db = pymysql.connect(host=self.ip, user=self.user, passwd=self.password, db=self.dbname, charset='utf8')
        cursor = db.cursor()
        if order_by == 'ASC':
            sql_select = "SELECT STATE_DT,STOCK_CODE,OPEN,CLOSE,HIGH,LOW,VOL,AMOUNT,PRE_CLOSE,AMT_CHANGE,PCT_CHANGE FROM STOCK_ALL WHERE STOCK_CODE = '%s' AND STATE_DT >= '%s' AND STATE_DT <= '%s' ORDER BY STATE_DT ASC" % (stock_code, start_dt, end_dt)
        else:
            sql_select = "SELECT STATE_DT,STOCK_CODE,OPEN,CLOSE,HIGH,LOW,VOL,AMOUNT,PRE_CLOSE,AMT_CHANGE,PCT_CHANGE FROM STOCK_ALL WHERE STOCK_CODE = '%s' AND STATE_DT >= '%s' AND STATE_DT <= '%s' ORDER BY STATE_DT DESC" % (stock_code, start_dt, end_dt)

        cursor.execute(sql_select)
        done_set = cursor.fetchall()

        if len(done_set) == 0:
            cursor.close()
            db.close()

            return None

        state_dt_list = []
        stock_code_list = []
        open_list = []
        close_list = []
        high_list = []
        low_list = []
        vol_list = []
        amount_list = []
        pre_close_list = []
        amt_change_list = []
        pct_change_list = []

        for i in range(len(done_set)):
            state_dt_list.append(done_set[i][0])
            stock_code_list.append(done_set[i][1])
            open_list.append(float(done_set[i][2]))
            close_list.append(float(done_set[i][3]))
            high_list.append(float(done_set[i][4]))
            low_list.append(float(done_set[i][5]))
            vol_list.append(float(done_set[i][6]))
            amount_list.append(float(done_set[i][7]))
            pre_close_list.append(float(done_set[i][8]))
            amt_change_list.append(float(done_set[i][9]))
            pct_change_list.append(float(done_set[i][10]))
        cursor.close()
        db.close()

        if require_type == 'all':
            return done_set
        elif require_type == 'date':
            return state_dt_list
        elif require_type == 'open':
            return open_list
        elif require_type == 'close':
            return close_list
        elif require_type == 'high':
            return high_list
        elif require_type == 'low':
            return low_list
        elif require_type == 'vol':
            return vol_list
        elif require_type == 'amount':
            return amount_list
        elif require_type == 'pre_close':
            return pre_close_list
        elif require_type == 'amt_change':
            return amt_change_list
        elif require_type == 'pct_change':
            return pct_change_list
        else:
            return None

    def fetch_stock_info(self):

        # 连接数据库
        db = pymysql.connect(host=self.ip, user=self.user, passwd=self.password, db=self.dbname, charset='utf8')
        cursor = db.cursor()

        try:
            sql_truncate = "TRUNCATE TABLE STOCK_INFO"
            cursor.execute(sql_truncate)
            db.commit()
        except Exception as err:
            print(err)

        stock_info = ts.get_stock_basics()

        for index in stock_info.index:
            stock_code = index

            if stock_code.startswith('6'):
                stock_code = stock_code + ".SH"
            else:
                stock_code = stock_code + ".SZ"

            name = stock_info.loc[index].values[0]
            industry = stock_info.loc[index].values[1]
            area = stock_info.loc[index].values[2]
            pe = stock_info.loc[index].values[3]
            outstanding = stock_info.loc[index].values[4]
            totals = stock_info.loc[index].values[5]
            totalAssets = stock_info.loc[index].values[6]
            liquidAssets = stock_info.loc[index].values[7]
            fixedAssets = stock_info.loc[index].values[8]
            reserved = stock_info.loc[index].values[9]
            reservedPerShare = stock_info.loc[index].values[10]
            esp = stock_info.loc[index].values[11]
            bvps = stock_info.loc[index].values[12]
            pb = stock_info.loc[index].values[13]
            timeToMarket = stock_info.loc[index].values[14]
            undp = stock_info.loc[index].values[15]
            perundp = stock_info.loc[index].values[16]
            rev = stock_info.loc[index].values[17]
            profit = stock_info.loc[index].values[18]
            gpr = stock_info.loc[index].values[19]
            npr = stock_info.loc[index].values[20]
            holders = stock_info.loc[index].values[21]

            try:
                sql_insert = "INSERT INTO STOCK_INFO VALUES ('%s','%s','%s','%s','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d')" %(stock_code,name,industry,area,pe,outstanding,totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,esp,bvps,pb,timeToMarket,undp,perundp,rev,profit,gpr,npr,holders)
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                continue

        cursor.close()
        db.close()

    def fetch_lastweek_data(self):
        time_temp1 = datetime.datetime.now() - datetime.timedelta(days=7)
        start_datetime = time_temp1.strftime('%Y-%m-%d')

        time_temp2 = datetime.datetime.now()
        end_datetime = time_temp2.strftime('%Y-%m-%d')

        self.fetch_history_data(start_dt = start_datetime, end_dt = end_datetime)

    def fetch_yesterday_data(self):
        time_temp1 = datetime.datetime.now() - datetime.timedelta(days=2)
        start_datetime = time_temp1.strftime('%Y-%m-%d')

        time_temp2 = datetime.datetime.now()
        end_datetime = time_temp2.strftime('%Y-%m-%d')

        self.fetch_history_data(start_dt = start_datetime, end_dt = end_datetime)

    def load_liu_analyze_stock_bottom(self):
        # 连接数据库
        db = pymysql.connect(host=self.ip, user=self.user, passwd=self.password, db=self.dbname, charset='utf8')
        cursor = db.cursor()

        sql_done_set = "SELECT DISTINCT STOCK_CODE, DAYS, ANALYZE_DAYS, OFFSET, RATIO FROM STOCK_REPORT_LIU_BOTTOM WHERE ANALYZE_DT = (SELECT MAX(ANALYZE_DT) FROM STOCK_REPORT_LIU_BOTTOM) ORDER BY DAYS DESC"
        cursor.execute(sql_done_set)
        done_set = cursor.fetchall()

        if len(done_set) == 0:
            return None

        cursor.close()
        db.close()
        return done_set

    def load_liu_analyze_stock_trend(self):
        # 连接数据库
        db = pymysql.connect(host=self.ip, user=self.user, passwd=self.password, db=self.dbname, charset='utf8')
        cursor = db.cursor()

        sql_done_set = "SELECT DISTINCT STOCK_CODE, TREND, ANALYZE_DAYS FROM STOCK_REPORT_LIU_TREND WHERE ANALYZE_DT = (SELECT MAX(ANALYZE_DT) FROM STOCK_REPORT_LIU_TREND) ORDER BY TREND, STOCK_CODE"
        cursor.execute(sql_done_set)
        done_set = cursor.fetchall()

        if len(done_set) == 0:
            return None

        cursor.close()
        db.close()
        return done_set

    def write_liu_analyze_stock_bottom(self, stock_bottom):
        # 连接数据库
        db = pymysql.connect(host=self.ip, user=self.user, passwd=self.password, db=self.dbname, charset='utf8')
        cursor = db.cursor()

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for stock in stock_bottom:
            try:

                code = stock['stock_code']
                days = int(stock['days'])
                analyze_days = int(stock['analyze_days'])
                offset = float(stock['offset'])
                ratio = float(stock['ratio'])

                sql_insert = "INSERT INTO STOCK_REPORT_LIU_BOTTOM VALUES ('%s', '%s', '%d', '%d', '%f', '%f')" % (now, code, days, analyze_days, offset, ratio)
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                continue

        cursor.close()
        db.close()

    def write_liu_analyze_stock_trend(self, stock_trend):
        # 连接数据库
        db = pymysql.connect(host=self.ip, user=self.user, passwd=self.password, db=self.dbname, charset='utf8')
        cursor = db.cursor()

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for stock in stock_trend:
            try:
                code = stock['stock_code']
                trend = stock['stock_trend']
                analyze_days = stock['analyze_days']

                sql_insert = "INSERT INTO STOCK_REPORT_LIU_TREND VALUES ('%s', '%s', '%s', '%d')" % (now, code, trend, analyze_days)
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                continue

        cursor.close()
        db.close()


    def fetch_history_data_from_baostock(self, start_dt, end_dt, stock_code=None):

        lg = bs.login()

        # 连接数据库
        db = pymysql.connect(host=self.ip, user=self.user, passwd=self.password, db=self.dbname, charset='utf8')
        cursor = db.cursor()

        stock_pool = []

        if stock_code is None:
            stock_pool = self.stock_code_list
        else:
            stock_pool.append(stock_code)

        stock_count = len(stock_pool)

        if stock_count == 0:
            print("no stocks to be load")
            return 0

        for i in range(stock_count):
            stock_code = stock_pool[i]
            code = stock_code[0:len(stock_code) - 3]
            if 'SH' in stock_code:
                code = "sh." + code
            else:
                code = "sz." + code

            rs = bs.query_history_k_data(code, "date,code,open,high,low,close,volume,amount,preclose,pctChg", start_date=start_dt, end_date=end_dt, frequency="d", adjustflag="3")

            data_list = []
            while (rs.error_code == '0') & rs.next():
                data = rs.get_row_data()
                try:
                    state_dt = data[0]
                    stock_code = data[1]
                    open_price = data[2]
                    close_price = data[3]
                    high_price = data[4]
                    low_price = data[5]
                    vol = data[6]
                    amount = data[7]
                    pre_close_price = data[8]
                    amt_change = 0
                    pct_change = data[9]

                    sql_insert = "INSERT INTO STOCK_ALL(STATE_DT,STOCK_CODE,OPEN,CLOSE,HIGH,LOW,VOL,AMOUNT,PRE_CLOSE,AMT_CHANGE,PCT_CHANGE) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f','%.2f','%.2f')" % (
                        state_dt, stock_code, float(open_price), float(close_price), float(high_price),
                        float(low_price), float(vol),
                        float(amount), float(pre_close_price), float(amt_change), float(pct_change))
                    cursor.execute(sql_insert)
                    db.commit()
                except Exception as err:
                    print(err)
                    continue
        bs.logout()

    def fetch_history_data_from_163(self, start_dt, end_dt, stock_code=None):

        print(start_dt)
        print(end_dt)

        start = start_dt[0:4] + start_dt[5:7] + start_dt[8:10]
        end = end_dt[0:4] + end_dt[5:7] + end_dt[8:10]

        # 连接数据库
        db = pymysql.connect(host=self.ip, user=self.user, passwd=self.password, db=self.dbname, charset='utf8')
        cursor = db.cursor()

        stock_pool = []

        if stock_code is None:
            stock_pool = self.stock_code_list
        else:
            stock_pool.append(stock_code)

        stock_count = len(stock_pool)

        if stock_count == 0:
            print("no stocks to be load")
            return 0

        for i in range(stock_count):
            stock_code = stock_pool[i]
            code = stock_code[0:len(stock_code) - 3]
            print(code)
            if 'SH' in stock_code:
                download_url="http://quotes.money.163.com/service/chddata.html?code=0" + code + "&start=" + start + "&end=" + end + "&fields=TOPEN;TCLOSE;HIGH;LOW;VOTURNOVER;VATURNOVER;LCLOSE;CHG;PCHG;"
            else:
                download_url="http://quotes.money.163.com/service/chddata.html?code=1" + code + "&start=" + start + "&end=" + end + "&fields=TOPEN;TCLOSE;HIGH;LOW;VOTURNOVER;VATURNOVER;LCLOSE;CHG;PCHG;"

            print(download_url)
            data=requests.get(download_url)
            f = open(stock_code + '.txt', 'wb')

            for chunk in data.iter_content(chunk_size=10000):
                if chunk:
                    f.write(chunk)

            f.close()

            f = open(stock_code + '.txt')
            f.readline()
            line=f.readline()
            while line:
                print(line)

                try:
                    line=f.readline()

                    segments=line.split(',')

                    state_dt=segments[0]
                    stock_code=stock_code
                    open_price=segments[3]
                    close_price=segments[4]
                    high_price=segments[5]
                    low_price=segments[6]
                    vol=segments[7]
                    amount=segments[8]
                    pre_close_price=segments[9]
                    amt_change=segments[10]
                    pct_change=segments[11]

                    sql_insert = "INSERT INTO STOCK_ALL(STATE_DT,STOCK_CODE,OPEN,CLOSE,HIGH,LOW,VOL,AMOUNT,PRE_CLOSE,AMT_CHANGE,PCT_CHANGE) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f','%.2f','%.2f')" % (
                    state_dt, stock_code, float(open_price), float(close_price), float(high_price), float(low_price), float(vol),
                    float(amount), float(pre_close_price), float(amt_change), float(pct_change))


                    cursor.execute(sql_insert)

                    db.commit()
                except Exception as err:
                    # print(err.message)
                    print("Exception")
                    continue

            f.close()

    def fetch_history_data(self, start_dt, end_dt, stock_code=None, source='tushare'):
        if source=='163':
            self.fetch_history_data_from_163(start_dt, end_dt, stock_code)
        elif source=='baostock':
            self.fetch_history_data_from_baostock(start_dt, end_dt, stock_code)
        elif source=="tushare":
            self.fetch_history_data_from_tushare(start_dt, end_dt, stock_code)
        else:
            pass


    # 如start_dt='2010-01-01', end_dt='2018-10-01'
    def fetch_history_data_from_tushare(self, start_dt, end_dt, stock_code=None):

        start = start_dt[0:4] + start_dt[5:7] + start_dt[8:10]
        end = end_dt[0:4] + end_dt[5:7] + end_dt[8:10]

        # 连接数据库
        db = pymysql.connect(host = self.ip, user = self.user, passwd = self.password, db = self.dbname, charset='utf8')
        cursor = db.cursor()

        stock_pool = []

        if stock_code is None:
            stock_pool = self.stock_code_list
        else:
            stock_pool.append(stock_code)

        stock_count = len(stock_pool)

        if stock_count == 0:
            print ("no stocks to be load")
            return 0

        # 循环获取单个股票的日线行情
        for i in range(stock_count):
            try:
                # 从接口里取数据
                #df = self.ts_pro.daily(ts_code=stock_pool[i], start_date=start, end_date=end)
                df = ts.pro_bar(pro_api=self.ts_pro, ts_code=stock_pool[i], asset='E', adj='qfq', start_date=start, end_date=end)
                c_len = df.shape[0]

                print("tushare正在执行 %d 中的第 %d 支股票数据的抓取，代码为 %s, 数目为 %d " %(stock_count, i, stock_pool[i], c_len))

            except Exception as aa:
                print('错误: 没有数据，股票代码为: ' + str(stock_pool[i]))
                continue

            for j in range(c_len):
                resu0 = list(df.ix[c_len-1-j])
                resu = []
                for k in range(len(resu0)):
                    if str(resu0[k]) == 'nan':
                        resu.append(-1)
                    else:
                        resu.append(resu0[k])

                state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
                
                try:
                    sql_insert = "INSERT INTO STOCK_ALL(STATE_DT,STOCK_CODE,OPEN,CLOSE,HIGH,LOW,VOL,AMOUNT,PRE_CLOSE,AMT_CHANGE,PCT_CHANGE) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f','%.2f','%.2f')" % (state_dt,str(resu[0]),float(resu[2]),float(resu[5]),float(resu[3]),float(resu[4]),float(resu[9]),float(resu[10]),float(resu[6]),float(resu[7]),float(resu[8]))
                    cursor.execute(sql_insert)
                    db.commit()
                except Exception as err:
                    #print err.message
                    continue
        cursor.close()
        db.close()


if __name__ == '__main__':
    token = '212d8b49da92c719416a4e01e4c56938fe8c45dc1e024bc6a118e7d4'
    ts.set_token(token)
    ts_pro = ts.pro_api()
    data = ts_pro.stock_basic()

    df = ts_pro.daily(ts_code='002630.SZ', start_date='20010701', end_date='20190718')
    print(df)