
import unittest
import os



from consultingutils.llmtemplates.llmtemplates import LLMTemplate, OracleToDB2SQL
from consultingutils.db.db import Oracle,DB2 
from consultingutils.reporting.reporting import ReportValidator

class Test(unittest.TestCase): 

    def __init__(self, *args, **kwargs): 
        super(Test, self).__init__(*args, **kwargs)

    def test_one(self): 

        os.environ["OPENAI_API_KEY"] = ""

        oracle_pw = ""
        oracle_user = ""
        oracle_dsn = "" 

        oracle = Oracle(
            pw=oracle_pw, 
            user=oracle_user, 
            dsn=oracle_dsn, 
            libdir=r"C:\Users\barrys\Python_Scripts\consultingutils\instantclient_21_9" # include full path here. 
        )

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

        report_validator = ReportValidator(sourcedb=oracle, testdbs=[oracle, db2])\
            .pull_adhoc_reports()\
            .untangle()

        # run a single test to ensure we can run effectively runs.  
        try: 
            test_result = report_validator.batch_test() 
            report_validator.validate(test_result)
        except Exception as e: 
            print(e) 
            raise Exception("invalid test result. afiled batch testing")


        # run a single test to ensure we can run effectively runs.  
        try: 
            report_validator.process(p=10)  # 50% of the reports.
        except Exception as e: 
            print(e) 
            raise Exception("invalid test result. afiled batch testing")



