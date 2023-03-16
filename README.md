# Consulting Utils. 

## Tools for building AI powered automation in your workflows. 
Modularized and simple components to interface with LLMs and Databases. 


## Docs: 

### Step 1
```
pip3 install...
```

### Step 2
> Import some libs. 
```
from consultingutils.llmtemplates.llmtemplates import LLMTemplate, OracleToDB2SQL
from consultingutils.db.db import Oracle,DB2 
from consultingutils.reporting.reporting import ReportValidator
```


## Examples: 

#### Automating report validation in Maximo. 
> extract and test sql from birt reports. Ensure the sql is valid and runs against both db2 and oracle. 

1. You need an Open AI API key. 
2. An oracle database and its credentials. 
3. A DB2 database and its credentials. 
4. You need the instantclient_21_9 Oracle python driver. (very simple to download.)

```

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

        # build a ReportValidator
        report_validator = ReportValidator(sourcedb=oracle, testdbs=[oracle, db2])\
            .pull_adhoc_reports()\
            .untangle()

        # run a single test 
        test_result = report_validator.batch_test() 
        report_validator.validate(test_result)


        # run the rest of the corpus
        report_validator.process(p=70)  # 70% of the reports.


```


