#!/usr/bin/python
# -*- coding: UTF-8 -*-
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import os
import cx_Oracle
from urllib import request

#数据库连接
source_ora_conn = ''
sina_page_num = ''
sina_page_list = ''

def get_source():
    Source_file = os.getcwd()+"\Source.xml"
    try:
        for event, elem in ET.iterparse(Source_file):            # reads a xml file
            tag_name = elem.tag
            if event == 'end':
                if tag_name == 'oracle_conn01':  self.source_ora_conn = elem.text if elem.text is not None else Exception("Can't get the connection of oracle")
                elif tag_name == 'stock_pagenum':self.sina_page_num = elem.text if elem.text is not None else Exception("Can't get the count of page")
                elif tag_name == 'stock_list':   self.sina_page_list = elem.text if elem.text is not None else Exception("Can't get the list of the stock")
        print(self.source_ora_conn)
        print(self.source_ora_conn)
        print(self.source_ora_conn)
    except Exception as e:
        print(e)
def get_stocklist():
    # oracle conn
    conn = cx_Oracle.connect('jack/jack@localhost/JACK')
    cursor = conn.cursor ()
    response = request.urlopen("http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/index.aspx?type=s&sortType=C&sortRule=-1&pageSize=20&page=1&jsName=quote_123&style=33")
    content = response.read().decode('utf-8').replace('"',',')
    count = len(content)
    start_count = content.find('pages:' )+6
    pages_count = int(content[start_count:count-1])
    pages_start = 1
    while pages_start< pages_count:
        i = 1;
        sub_response = request.urlopen("http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/index.aspx?type=s&sortType=C&sortRule=-1&pageSize=20&page="+str(pages_start)+"&jsName=quote_123&style=33")
        sub_content = sub_response.read().decode('utf-8').replace('"',',')
        stock_list = sub_content.split(',')
        col_count = len(stock_list)
        while i< col_count:
            cursor.execute ("INSERT INTO T_PY_STOCKLIST "
                            "("
                            "eastmoney_code,"
                            "stock_code,"
                            "stock_name,"
                            "yes_values,"
                            "open_values,"
                            "new_values,"
                            "high_values,"
                            "low_values,"
                            "turnover_value,"
                            "turnover,"
                            "pricechangeratio_value,"
                            "pricechangeratio,"
                            "average_price,"
                            "amplitude,"
                            "weibi,"
                            "INSERT_DATE"
                            ")"
                            "VALUES("+
                                 "'"+stock_list[i]+"'"+",'"+stock_list[i+1]+"'"+",'"+stock_list[i+2]+"'"
                                +','+stock_list[i+3] +','+stock_list[i+4] +','+stock_list[i+5]
                                +','+stock_list[i+6] +','+stock_list[i+7] +','+stock_list[i+8]
                                +','+stock_list[i+9] +','+stock_list[i+10]+",'"+stock_list[i+11]+"'"
                                +','+stock_list[i+12]+",'"+stock_list[i+13]+"'"+",'"+stock_list[i+14]+"'"
                                +','+"sysdate"
                            +")")
            i = i+35
        pages_start = pages_start+1
    conn.commit()
    cursor.close ()
get_source();