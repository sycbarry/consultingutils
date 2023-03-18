
import unittest
import os



from consultingutils.llmtemplates.llmtemplates import LLMTemplate, OracleToDB2SQL
from consultingutils.db.db import Oracle,DB2 

class Test(unittest.TestCase): 

    def __init__(self, *args, **kwargs): 
        super(Test, self).__init__(*args, **kwargs)

    def test_one(self): 

        db2_pw = ""
        db2_user = ""
        db2_database = ""
        db2_hostname = ""
        db2_port = ""

        db2 = DB2(
            port = db2_port, 
            user=db2_user, 
            pw=db2_pw, 
            hostname=db2_hostname, 
            database=db2_database
        )

        rows = db2.testquery("select count(*) from maximo.asset;")

        results = db2.query("select assetnum, description from maximo.asset where 1 = 1;")

        oracle_pw = ""
        oracle_user = ""
        oracle_dsn = "" 

        oracle = Oracle(
            pw=oracle_pw, 
            user=oracle_user, 
            dsn=oracle_dsn, 
            libdir=r"C:\Users\barrys\Python_Scripts\Drivers\instantclient_21_9" # include full path here. 
        )

        sql = "select design, reportname from reportdesign where reportname in (select reportname from reportadhoc)"
        results = oracle.testquery(sql, isreturnable=True)


        sql  = "select assetnum, description from asset where 1 = 1"
        results = oracle.query(sql, ["assetnum", "description"])
        print(results[0])


        sql = "selectd design, reportname from reportdesign where reportname in (select reportname from reportadhoc)"
        testdbs = [oracle, db2, oracle]

        result = map( 
            lambda x: 
                x.testquery(sql, isreturnable=False) 
                if isinstance(x, Oracle)  
                else []
            ,
            testdbs
        )

        for i in iter(result): 
            print(isinstance(i, Exception))
            if isinstance(Exception, type(i)) == True: 
                print("asdfljkasdflkjadf")
        


