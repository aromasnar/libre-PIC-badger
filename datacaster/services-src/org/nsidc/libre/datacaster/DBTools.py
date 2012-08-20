"""
author: Geoff Anderson

----------------------
This package (org.nsidc.libre.datacaster) contains
classes related to the Libre-Datacasting project.
----------------------
"""

import psycopg2


class DBQuery:
    def __init__(self,db_connection_string):
               self.conn = psycopg2.connect(db_connection_string)
               self.cur=self.conn.cursor()
               #self.cur.execute("DELETE FROM datacaster_parameter");

    def query(self,sql):
        
        self.cur.execute(sql)

        return self.cur

class GCMD_Param_Loader:
   def __init__(self,db_connection_string):
       self.conn = psycopg2.connect(db_connection_string)
       self.cur=self.conn.cursor()
       self.cur.execute("DELETE FROM datacaster_parameter");
       self.conn.commit()

   def put_param(self,param):
       category=param.getCat()
       topic=param.getTopic()
       term=param.getTerm()
       json=param.as_json()
       levels=":"
       for level in param.getLevels():
           levels += level + ":"
       levels=levels.strip()[:len(levels)-1]
       keywords=category + " " + topic + " "+ term + " " + levels
       self.cur.execute("INSERT INTO datacaster_parameter (category,topic,term,levels,keywords,json) VALUES (%s, %s, %s, %s, %s, %s)",   (category,topic,term,levels,keywords,json))

   def __del__(self):
       #Clean up
       try:
        self.conn.commit()
        self.cur.close()
        self.conn.close()
       except:
           pass


       
