#-*- coding: utf-8 -*-
import datetime
import mysql.connector
import dbconfig

def getNDaysAgo(ndays=30):
    today = datetime.date.today()
    resday = today - datetime.timedelta(days=ndays)
    return resday.strftime('%Y-%m-%d')

class DBHelper:
    def __init__(self):
        self.name2CodeMap = self.buildCodeTable()
    
    def connect(self):
        #print ("Getting connection to database")
        return mysql.connector.connect(
            host=dbconfig.db_host, 
            user=dbconfig.db_user, 
            password=dbconfig.db_password,
            database=dbconfig.db_name)

    def buildCodeTable(self):
        conn = self.connect()
        cursor = conn.cursor(buffered=True)
        query = "select `code`, name from jongmok_master;"
        cursor.execute(query)
    
        table = {}
        for row in cursor:
            code = row[0]
            name = row[1]
            table[code] = name
            
        cursor.close()
        return table

    def buildCodeListFromName(self, nameStr):
        conn = self.connect()
        cursor = conn.cursor(buffered=True)
        query = "select `code`from jongmok_master where `name` like %s;" 
        cursor.execute(query, (nameStr,))
    
        code_list = []
        for row in cursor:
            code_list.append(row[0])
            
        cursor.close()
        return code_list
        
    def buildNameCodeTable(self):
        conn = self.connect()
        cursor = conn.cursor(buffered=True)
        query = "select code, name from jongmok_master;"
        cursor.execute(query)
    
        table = {}
        for row in cursor:
            code = row[0]
            name = row[1]
            table[name] = code
            
        cursor.close()
        return table
    
    def getLastDayOfPriceTable(self):
        conn = self.connect()
        cursor = conn.cursor(buffered=True)
        query = "select max(`date`) from price_table group by null"
        cursor.execute(query)
        row = cursor.fetchone()
        return row[0]
        
    def get_n_price(self, lim=10):
        connection = self.connect()
        try:
            query = """SELECT date, code, open_price, high_price, low_price, close_price, cap_amount
                    FROM price_table 
                    WHERE `date` >= %s
                    LIMIT %s""" 
            cursor = connection.cursor()
            cursor.execute(query, (self.getLastDayOfPriceTable(), lim))
            row_data_list = []
            for arow in cursor:
                row_data = {
                    'date': arow[0],
                    'name': self.name2CodeMap[arow[1]],
                    'code': arow[1],
                    'open_price': str(arow[2]),
                    'high_price': str(arow[3]),
                    'low_price': str(arow[4]),
                    'close_price': str(arow[5]),
                    'cap_amount': str(arow[6])
                }
                row_data_list.append(row_data)
            return row_data_list
        finally:
            connection.close()

    def getPriceByQuery(self, queryObj=None):
        qcond = ''
        if queryObj==None:
            self.get_n_price(lim=100)
            
        if queryObj['jm_code']==None or queryObj['jm_code']=='':
            pass
        else:
            qcode = " `code`='%s' " % queryObj['jm_code']
            qcond += qcode
        if queryObj['jm_name']==None or queryObj['jm_name']=='':
            pass
        else:
            qcond  = '' if qcond=='' else qcond+' and '
            nameStr = "'%"+queryObj['jm_name']+"%'"
            qname = "`code` in (select `code` from jongmok_master where `name` like %s )" % nameStr
            qcond += qname
        if queryObj['start_day']==None or queryObj['start_day']=='':
            pass
        else:
            qcond  = '' if qcond=='' else qcond+' and '
            qstart = " `date`>='%s' " % queryObj['start_day']
            qcond += qstart
        if queryObj['end_day']==None or queryObj['end_day']=='':
            pass
        else:
            qcond  = '' if qcond=='' else qcond+' and '
            qend = " `date`<='%s' " % queryObj['end_day']
            qcond += qend
        if queryObj['limit']==None or queryObj['limit']=='':
            pass
        else:
            qlimit = ' LIMIT %s ' % queryObj['limit']
            qcond += qlimit

        query = "SELECT `date`, `code`, open_price, high_price, low_price, close_price, cap_amount FROM price_table "
        if qcond == '':
            query = query + ' LIMIT 100 '
        else:
            query = query + ' where ' + qcond
        #print ('query=%s' % query)
            
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            row_data_list = []
            for arow in cursor:
                row_data = {
                    'date': arow[0],
                    'name': self.name2CodeMap[arow[1]],
                    'code': arow[1],
                    'open_price': str(arow[2]),
                    'high_price': str(arow[3]),
                    'low_price': str(arow[4]),
                    'close_price': str(arow[5]),
                    'cap_amount': str(arow[6])
                }
                row_data_list.append(row_data)
            return row_data_list
        finally:
            conn.close()

    def queryTemplate(self):
        conn = self.connect()
        try:
            query = "select code, name from jongmok_master;"
            cursor = conn.cursor(buffered=True)
            cursor.execute(query)
    
            table = {}
            for row in cursor:
                code = row[0]
                name = row[1]
                table[name] = code
        except Exception as e:
            print(e)    
        finally:
            conn.close()            

        return table
