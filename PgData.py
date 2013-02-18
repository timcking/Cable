import psycopg2
import sys

class PgData():
    
    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname=cable_db host=rocky user=tking password=xxxxxx")
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e    
            sys.exit(1)
            
    def getEmbassy(self):
        sql = "SELECT DISTINCT origin " +\
              "  FROM cable " +\
              "ORDER by origin;"
              
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows
                
    def doSearch(self, embassy):
        sql = "SELECT origin, date, content " +\
              "  FROM cable " +\
              " WHERE origin LIKE %s " +\
              "ORDER BY date;"
        
        cur = self.conn.cursor()
        # Parameterized query
        cur.execute(sql, (embassy, ))
        rows = cur.fetchall()
        cur.close()
        return rows
   
    def doCloseConn(self):
        self.conn.close()
