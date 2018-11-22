# -*- coding: utf-8 -*-
import csv
import pandas as pd
import json
import psycopg2
#==========================================================================
#开始创建class sheet_reaction(BaseModel)中的表
#去除csv文件中的隔行问题
#处理csv数据
#方式一链接pg数据库并写入数据
#方式二链接pg数据库并写入数据
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def doCsv():#去除csv文件中的隔行问题
       origin_f = open('nistResults.csv', 'r',encoding='utf-8')
       new_f = open('result_nist.csv', 'a+',encoding='utf-8',newline='')
       reader = csv.reader(origin_f)
       writer = csv.writer(new_f)
       for index,row in enumerate(reader):
              if len(row)>0:
                     print('>>>>>>>>>>', index)
                     writer.writerow(row)
       origin_f.close()
       new_f.close()
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# def doJsonData():
#     jd = open('biblios.json',encoding='utf-8').read()
#     print(jd)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def clearData():#处理csv数据
    data = pd.read_csv('ibond.csv',encoding='utf-8',low_memory=False,header=0)# 读取csv

    data = data.reindex(columns=['name', 'Solvent', 'solvent_full_name', 'pKa', 'Method', 'method_description',
       'Ref', 'ref_content', 'doi', 'Structure'])
    data['ref_content'] = data['ref_content'].str.strip()
    data['name'] = data['name'].str.replace("'",'')
    data.drop_duplicates(inplace=True)
    data.fillna('NULL',inplace=True)
    return data
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def connPGSQL():#方式一链接pg数据库并写入数据
    data = clearData()
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(dbname='test', user='matgene', password='matgene001', port='5432', host='192.168.1.71')
        cur = conn.cursor()
        cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('ibond',))
        Boolean = cur.fetchone()[0]
        if Boolean != True:
            cur.execute('''CREATE TABLE ibond
                          (name    TEXT,
                           Solvent    TEXT,
                           solvent_full_name   TEXT,
                           pKa    TEXT,
                           Method    TEXT,
                           method_description    TEXT,
                           Ref    TEXT,
                           ref_content    TEXT,
                           doi    TEXT,
                           Structure    TEXT);''')
    except Exception as e:
        print('>>>ERROR :',e)
    finally:
        if conn:
            count = 0
            for row in data.values.tolist():
                count += 1
                try:
                    sql = 'INSERT INTO ibond values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    cur.execute(sql, tuple(row))
                    conn.commit()
                    print('>>>', count)
                except Exception as e:
                    print('ERROR INSERT:', e)
                    conn.rollback()
                # sql_select = "SELECT COUNT(*) FROM ibond WHERE  Structure='"+row[9]+"'"
                # cur.execute(sql_select)
                # num = cur.fetchone()
                # if num[0]==0:
                #     count += 1
                #     try:
                #         sql = 'INSERT INTO ibond values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                #         cur.execute(sql, tuple(row))
                #         conn.commit()
                #         print('>>>', count)
                #     except Exception as e:
                #         print('ERROR INSERT:', e)
                #         conn.rollback()
            cur.close()
            conn.close()
            print('>>> SUCCESS INSERT INTO  POSTGRESQL! count =', count)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
if __name__=='__main__':
    # doCsv()                   #处理csv文件，比如去除隔行，切割等
    clearData()               #清洗数据
    # connPGSQL()                 #写入数据库1
    # connectPostgreSQL()         #写入数据库2
