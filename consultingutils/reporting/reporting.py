import os
import sys
import untangle
import csv


from consultingutils.db.db import Oracle,DB2 , DB
from consultingutils.llmtemplates.llmtemplates import LLMTemplate, OracleToDB2SQL, ParseStringToOracleSQL





class Reporting(object): 

    def __init__(self) -> None:
        pass


"""
This is a report validator class. 

what does this need? 

1. the source database to pull queries from . 
2. a list of databases to test the sql against. 

"""
class ReportValidator(Reporting):


    def __init__(self, 
        sourcedb=DB, 
        testdbs=[], 
        *args, **kwargs
    ) -> None:

        super().__init__()
        self.testdbs = [*testdbs]
        self.sourcedb = sourcedb


    """
    grab the reports, including the report name and the reportdesign from the 
    source databases
    """
    def pull_adhoc_reports(self, limit: int =None) -> None: 


        if isinstance(self.sourcedb, Oracle):

            if limit == None or not isinstance(limit, int): 
                query = " select design, reportname from reportdesign where reportname in (select reportname from reportadhoc) "
            else: 
                query = " select design, reportname from reportdesign where reportname in (select reportname from reportadhoc) fetch first " + limit.__str__() + " only "

            result = self.sourcedb.testquery(query=query, isreturnable=True)

            designs = []
            reportname  = []

            for d in result: 
                try: 
                    designs.append(d['DESIGN'])
                    reportname.append(d['REPORTNAME'])
                except Exception as e: 
                    continue

            combs = list(zip(designs, reportname))

            self.reportobjects  = [ { "xml": x[0], "reportname": x[1], "outputfile": x[1].split(".")[0] + "_rptdesignAndSQL.txt", "rawtxt": None, "oraclesql": None, "db2sql": None} for x in combs ]

            return self


        # handle for db2

        raise FileNotFoundError("Invalid Database type passed in as source.")



    """
    Parses teh raw SQL from the report. 
    This is done by finding the appropriate tag name of the xml node. 
    """
    def untangle(self):
        
        for i in range( len(self.reportobjects) ): 

            check_method = lambda x: True if x['name'] == "open" else None
    
            # grab the sql string b/w two values. 
            xml = untangle.parse(
                self.reportobjects[i]['xml'].strip()
            )
    
            # recurse to find the tag: method, where the name property = 'open'
            # append that to the elements array. 
            def find_children(obj): 
        
                #base case
                if obj.children == None or len(obj.children) <= 0:
                    if check_method(obj) is not None: 
                        self.reportobjects[i]['rawtxt'] = obj.cdata
                    else: 
                        return
            
                # recursive case (just loop through children)
                for child in obj.children:  
                    find_children(child)
            
            find_children(xml)


        self.batch_single = self.reportobjects[:1]
        self.batch = self.reportobjects
        return self



    def batch_test(self): 
        return self.clean(self.batch_single)

    """
    tunage: 
    p = % of reports we want to process. 
    """
    def process(self, p=100): 
        import math

        if p > 100 or p < 1: 
            raise Exception("cannot process more than 100% of reports. ")
        _p = math.ceil( (p / 100) * (len(self.batch)) )
        self._p = _p
        self.batch[:_p] = self.clean(self.batch[:_p])
        return self.validate(self.batch[:_p])


    """
    cleanup and translation work.
    """
    def clean(self, obj): 

        from tqdm import tqdm
        from tqdm import trange

        if obj is None: 
            raise Exception("No objects to clean")

        for i in tqdm( range( len(obj) ) ):
            # the mode cleans the text
            clean_response = ParseStringToOracleSQL().invoke(obj[i]['rawtxt'])
            obj[i]['oraclesql'] = clean_response.strip(";")

            # the model converts it into a db2 query.
            db2_conversion = OracleToDB2SQL().invoke(clean_response)
            obj[i]['db2sql'] = db2_conversion

        return obj

    
    """
    validate the integrity of the queries here.
    """
    def validate(self, obj): 

        from tqdm import trange 

        # loop through each object in our list. 
        t = trange((len(obj)), desc="testing sql", leave=True)
        for i in t:    

            # makes a single .txt file per report.
            def make_file(): 
                path = os.path.join("./")
                if not path in os.path.join("./output"):
                    os.mkdir("./output")
                file_name = './output/' + self.batch[i]['outputfile']
                if file_name in os.listdir(): 
                    os.remove(file_name)
                return file_name.__str__()
    
    
            # ensure we have the xml in the file first, 
            def write_xml(file_name, xml): 
                with open(file_name, 'w') as f: 
                    f.write(xml + "\n\n")
                    f.write("--------------------------------")
                    f.write("-------------------------------- \n\n")


            def write_sql(file_name): 

                with open((file_name), 'a') as f: 

                    def write_to_file(input):
                        f.write(input + "\n\n")


                    def oracle(sql_obj=None): 

                        if sql_obj is not None: 

                            oracle_sql = sql_obj.strip()

                            result = map( 
                                lambda x: 
                                    x.testquery(oracle_sql, isreturnable=False) 
                                    if isinstance(x, Oracle)  
                                    else [] 
                                ,
                                self.testdbs
                            )
                            for re in result: 
                                if isinstance(re, Exception) == True: 
                                    write_to_file("--- FAILED in Oracle")
                                    write_to_file(f"   Query -> {oracle_sql}")
                                    write_to_file(f"   Error -> {re}")
                                    return False
                            write_to_file("--- RAN in Oracle")
                            write_to_file(f"   Query -> {oracle_sql}")
                            return True


                    def db2(sql_obj=None): 
                        if sql_obj is not None: 
                            db2_sql = sql_obj.strip(";")
                            result = map( 
                                lambda x: 
                                    x.testquery(db2_sql, isreturnable=False) 
                                    if isinstance(x, DB2)  
                                    else [] 
                                ,
                                self.testdbs
                            )
                    
                            ## We write teh result and is sql query.
                            for re in result: 
                                if isinstance(re, Exception) == True: 
                                    write_to_file("--- FAILED in DB2")
                                    write_to_file(f"   Query -> {db2_sql}")
                                    write_to_file(f"   Error -> {re}")
                                    return False
                            write_to_file("--- RAN in DB2")
                            write_to_file(f"   Query -> {db2_sql}")
                            return True

                    obj = self.batch[i]
            
                    row = [ obj['reportname'].split("_rptdesignAndSQL.txt")[0], oracle(obj['oraclesql']), db2(obj['db2sql']) ] 

                    self.write_csv(row)
            
            

            ## main ## 
    
            # logs. 
            t.set_description(f"testing sql for report: {obj[i]['reportname']}: {i + 1}/{len(obj)}", refresh=True)
            t.refresh()

            # make the file
            file_name = make_file()
            if file_name == None: 
                continue
    
            # first write the xml to the file. 
            write_xml(file_name, self.batch[i]['xml'])
    
            # run through the sql tsting phase. 
            write_sql(file_name)


        return obj





    def write_csv(self, row): 
        path = os.path.join("./")
        if not path in os.path.join("./output"):
            os.mkdir("./output")
        file_name = './output/' + 'output.csv' 
        if os.path.exists(file_name): 
            with open(file_name, 'a', newline='') as file: 
                writer = csv.writer(file)
                writer.writerow(row)
                file.close()
            return
        else: 
            with open(file_name, 'w', newline='') as file: 
                writer = csv.writer(file)
                writer.writerow(["Report Name", "Ran in Oracle", "Ran in DB2"])
                writer.writerow(row)
                file.close()
            return



        





        



    

