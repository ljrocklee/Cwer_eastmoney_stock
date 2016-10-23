#!/usr/bin/python
# -*- coding: UTF-8 -*-
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import os
import time
import pymysql
from urllib import request

def get_stocklist():
    # 资源文件位置
    Source_file = os.getcwd()+"\Sourcefile\Source.xml"
    # 资源文件中，mysql的连接信息。
    source_mysql_host = ''
    source_mysql_username = ''
    source_mysql_password = ''
    source_mysql_db = '';
    source_mysql_port = '';
    # 获得股票页数的链接
    sina_page_num = ''
    # 获得每页股票的链接
    sina_page_list = ''
    # 收集网页中获得的股票数据
    stock_values=[]
    # 得到一个运行时间
    key_time = str(time.strftime("%Y-%m-%d %H:%M:%S"))
    # 插入mysql数据库表T_PY_STOCKLIST
    ins_list_sql = "INSERT INTO T_PY_STOCKLIST (eastmoney_code,stock_code,stock_name,yes_values,open_values,new_values," \
                   "high_values,low_values,turnover_value,turnover,pricechange_value,pricechange_ratio,average_price," \
                   "amplitude,weibi,INSERT_DATE)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        for event, elem in ET.iterparse(Source_file):            # reads a xml file
            tag_name = elem.tag
            if event == 'end':
                if tag_name == 'my01_hostname':  source_mysql_host = elem.text if elem.text is not None else Exception("Can't get the hostname of mysql")
                elif tag_name == 'my01_username':source_mysql_username = elem.text if elem.text is not None else Exception("Can't get the username of mysql")
                elif tag_name == 'my01_password':source_mysql_password = elem.text if elem.text is not None else Exception("Can't get the password of mysql")
                elif tag_name == 'my01_db':source_mysql_db = elem.text if elem.text is not None else Exception("Can't get the db name of mysql")
                elif tag_name == 'my01_port':source_mysql_port = elem.text if elem.text is not None else Exception("Can't get the port of mysql")
                elif tag_name == 'stock_pagenum':sina_page_num = elem.text if elem.text is not None else Exception("Can't get the count of page")
                elif tag_name == 'stock_list':   sina_page_list = elem.text if elem.text is not None else Exception("Can't get the list of the stock")

        conn= pymysql.connect(host=source_mysql_host, port=int(source_mysql_port), user=source_mysql_username, passwd=source_mysql_password,db = source_mysql_db, charset='UTF8')
        sto_cursor = conn.cursor()
        # 解析网页
        response = request.urlopen(sina_page_num)
        content = response.read().decode('utf-8').replace('"',',')
        count = len(content)
        start_count = content.find('pages:' )+6
        pages_count = int(content[start_count:count-1])
        pages_start = 1
        # 对每一个网页进行分析
        while pages_start< pages_count:
            i = 1;
            sub_response = request.urlopen(sina_page_list % str(pages_start))
            print(sina_page_list % str(pages_start))
            sub_content = sub_response.read().decode('utf-8').replace('"',',')
            stock_list = sub_content.split(',')
            col_count = len(stock_list)
            # 收集股票结果
            while i< col_count:
                stock_values.append((stock_list[i],stock_list[i+1],stock_list[i+2],stock_list[i+3] ,stock_list[i+4] ,
                                    stock_list[i+5],stock_list[i+6] ,stock_list[i+7] ,stock_list[i+8],stock_list[i+9] ,
                                    stock_list[i+10],stock_list[i+11],stock_list[i+12],stock_list[i+13],stock_list[i+14],
                                    key_time))

                i = i+35
            pages_start = pages_start+1
        # 插入数据库中
        sto_cursor.executemany(ins_list_sql,stock_values)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        sto_cursor.close()
        conn.close()
get_stocklist()
