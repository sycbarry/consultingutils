"""

"""

from consultingutils.llmtemplates.llmtemplates import LLMTemplate, OracleToDB2SQL
from consultingutils.db.db import DB, Oracle, DB2 
from consultingutils.reporting.reporting import ReportValidator


class StoredProcedure(object):
    
    def __init__(self, db=None) -> None:
        if not isinstance(db, DB):
            raise TypeError("Database is not a DB Type")
        self.db = db
        pass



    @property
    def  __getdb__(self) -> DB: 
        return self.db



    """
    Pull a single procedure from db.
    """
    def pull_single_procedure(self, procedure_name=None): 
        if procedure_name == None: 
            raise Exception("no procedure name included")
        if self.db == None: 
            raise Exception("no database included.")


        self.procedure = self.db.query(f"select text from user_source where name = '{procedure_name}' ", ["text"])
        
        return self


    """
    Pre-procesing - explain the stored procedure.
    """
    def explain_procedure(self): 
        None


    """
    Post-processing - clean Procedure - simplify the procedure
    """
    def clean_procedure(self): 
        None


    """ 
    ##
    Functional processing methods.
    ##
    """ 
    """
    extract all sql statements into a list. 
    """
    def translate_procedure_json(self): 
        None
