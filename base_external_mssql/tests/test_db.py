from unittest import TestCase
from odoo.tests.common import TransactionCase

import pyodbc



#SERVER = 'localhost,1433'
SERVER = 'localhost'
# DATABASE = 'tempdb'
DATABASE = 'SchnittstellenDB'
USERNAME = 'odoo'
PASSWORD = 'uri%oodoJ2024'

# this is need otherwise pyodbc will not work
pyodbc.setDecimalSeparator(".")


#class TestMssqlInsert(TestCase):
    
class TestMssqlInsert(TransactionCase):

    def setUp(self):
        connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};TrustServerCertificate=yes;'
        # self.conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD,
         #                   database=DATABASE, port=1433)
        self.conn = pyodbc.connect(connection_string, autocommit=True)
        self.cursor = self.conn.cursor()
    
    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    def test_select_data(self):
        SQL_QUERY = """
            SELECT 
            TOP 5 * 
            FROM 
            PPG_Artikel;
            """
        rows = self.cursor.execute(SQL_QUERY)
        records = self.cursor.fetchall()
        self.assertGreater(len(records), 0)


    def test_insert_data(self):
        conn = self.conn
        cursor = self.cursor
        # query = "INSERT TZ VALUES ('Hana');" 
        query = "INSERT INTO PPG_Artikel (Artikelid, Artikelbezeichnung, STATUS, Info1, Info2, Info3, Info4, ChVerw, SnVerw, Suchbegriff, Artikelgruppe, Einheit, Row_Create_Time, Row_Update_Time, isFIFO) VALUES (100501, 'KProdukt 801', 2, '', '', '', '', '', '', '', '', '', 'Sep 19 2024  2:48PM', 'Sep 19 2024  2:48PM', '')"
        res = cursor.execute(query) 
        last_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchval()
        # insert_cursor = conn.execute(query) 
        # cursor.execute(query);  

        # conn.commit()
        #insert_cursor = conn.execute("SELECT SCOPE_IDENTITY()")
        #res = cursor.execute('SELECT SCOPE_IDENTITY() AS [SCOPE_IDENTITY];')
        # last_id = res.fetchval()
        #last_id = insert_cursor.fetchval()
        print('last_id: ', last_id)
        


        # error message in case if test case got failed 
        message = f'last id is {last_id} and is not greater that second value.'

        self.assertGreater(last_id, 0, message) 
        

