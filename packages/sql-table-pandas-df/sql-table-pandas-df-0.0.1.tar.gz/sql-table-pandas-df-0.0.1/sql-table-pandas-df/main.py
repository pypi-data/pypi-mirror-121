import pymysql
import pandas as pd

def return_pddf(host, user, passwd, database, sql_query):
    db = pymysql.connect(host=host,
                user=user,
                passwd=passwd,
                database=database)

    df = pd.read_sql(sql_query,db)

    return