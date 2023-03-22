
import unittest
import os



from consultingutils.llmtemplates.llmtemplates import LLMTemplate, OracleToDB2SQL
from consultingutils.db.db import Oracle,DB2 
from consultingutils.reporting.reporting import ReportValidator

class Test(unittest.TestCase): 

    def __init__(self, *args, **kwargs): 
        super(Test, self).__init__(*args, **kwargs)

    def test_oracle_to_db2(self): 

        os.environ["OPENAI_API_KEY"] = ""

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

        libdir = r"C:\Users\barrys\Python_Scripts\Drivers\instantclient_21_9"
        oracle = Oracle(
            user=oracle_user, 
            dsn=oracle_dsn, 
            pw=oracle_pw, 
            libdir=libdir
        )


        # convert oracle query to db2 query.
        oracle_queries = [
            " SELECT purchview.contractnum,purchview.description,purchview.status,purchview.vendor,purchview.startdate,purchview.enddate,purchview.renewaldate FROM purchview  WHERE 1=1  AND (purchview.status LIKE '%APPR%'  AND purchview.enddate <= TO_DATE('2017-06-08', 'YYYY-MM-DD')  AND purchview.orgid = 'EAGLENA') ", 
            " SELECT purchview.contractnum,purchview.description,purchview.status,purchview.vendor,purchview.startdate,purchview.enddate,purchview.renewaldate FROM purchview  WHERE 1=1  AND (purchview.status LIKE '%APPR%'  AND purchview.enddate <= TO_DATE('2017-06-08', 'YYYY-MM-DD')  AND purchview.orgid = 'EAGLENA') ",
            "SELECT purchview.contractnum,purchview.description,purchview.status,purchview.vendor,purchview.startdate,purchview.enddate,purchview.renewaldate FROM purchview WHERE 1=1 AND (purchview.status LIKE '%APPR%'  AND purchview.enddate  <=  TO_DATE('2017-06-08','YYYY-MM-DD') AND purchview.orgid  =  'EAGLENA') ",
            "SELECT  inventory.itemnum,inventory.reorder,inventory.orderunit,i2.lastcost,inventory.vendor,inventory.location,inventory.siteid FROM inventory INNER JOIN invcost i2 ON i2.itemnum  =  inventory.itemnum AND i2.itemsetid = inventory.itemsetid AND i2.location = inventory.location AND i2.siteid = inventory.siteid WHERE 1=1"
        ]
        
            

        for sql in oracle_queries: 
            db2_query = OracleToDB2SQL().invoke(sql)
            # validate that both run against the db.
            try: 
                result = db2.testquery(query=db2_query, isreturnable=True)
                if isinstance(result, Exception): 
                    self.assertFalse(1 == 1)
            except Exception as e: 
                self.assertFalse(1 == 1)


    def test_one(self): 
        return
        os.environ["OPENAI_API_KEY"] = ""

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

        libdir = r"C:\Users\barrys\Python_Scripts\Drivers\instantclient_21_9"
        oracle = Oracle(
            user=oracle_user, 
            dsn=oracle_dsn, 
            pw=oracle_pw, 
            libdir=libdir
        )


        report_validator = ReportValidator(sourcedb=oracle, testdbs=[oracle, db2])\
            .pull_adhoc_reports()\
            .untangle()

        # run a single test to ensure we can run effectively runs.  
        try: 
            test_result = report_validator.batch_test() 
            obj = report_validator.validate(test_result)
            oracle_sql = obj[0]['oraclesql']
            self.assertNotIn(";", oracle_sql)
        except Exception as e: 
            print(e) 
            raise Exception("invalid test result. afiled batch testing")


        # run a single test to ensure we can run effectively runs.  
        try: 
            report_validator.process(p=20)  # 50% of the reports.
            values = report_validator.batch[0:report_validator._p]
            for i in values:
                self.assertNotIn(";", i["oraclesql"])
        except Exception as e: 
            print(e) 
            raise Exception("invalid test result. afiled batch testing")




