"""
Docs: 

1. this library contains llm templates. 
2. these templates are used to interface with language models. 
3. each template has its own use case depending on what the user wants to do.
"""


from langchain import PromptTemplate
from langchain import OpenAI
from langchain.chains import LLMChain
import sys



"""

our base template type

"""
class LLMTemplate(object): 

    def __init__(self, prompt=None, *args, **kwargs): 

        super().__init__()

        self.prompt = prompt
        self.kwargs = kwargs 

        return self

    @property
    def  __gettemplateprompt__(self): 
        return self.template.format()

    """
    builds the templates prompt template. 
    """
    def __buildtemplate__(self): 

        if self.prompt == None: 
            return None

        self.template = PromptTemplate(
            input_variables=[*self.args], 
            template=self.prompt
        )

        return self

    """
    builds the templates chain.
    """
    def __buildchain__(self): 

        if self.template == None: 
            raise NotImplementedError("no prompt template generated")
        
        llm = OpenAI(temperature=0.9)
        self.chain = LLMChain(llm=llm, prompt=self.template)

        return self
        


    """
    Passes in a variety of inputs to the template. 
    inputs must maintain the integrity of the prompt parameters.
    def __invoke__(self, sql="select * from user", database="db2"): 
    """
    def __invoke__(self, *args): 

        if args == None or len(args) <= 0: 
            raise BaseException("require something to input.")

        return self.chain.run([*args])






"""

cleaning templates. 
these templates are good at prompting an llm 
to clean things up - organize.. 

"""
class CleaningTemplate(LLMTemplate): 

    def __init__(self): 
        super().__init__()

    


"""

DB2 To Oracle SQL Conversion Template
-- converting a db2 query to an oracle sql query.

"""
class OracleToDB2SQL(LLMTemplate): 


    def __init__(self, sql=None, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.args = ["raw_sql"]

        self.prompt = """
        Here is a DB2 SQL query: {raw_sql}. 
    
        Follow these rules for converting the Oracle SQL Query to a DB2 SQL Query: 

        1. Replace all Oracle specific keywords and functions with the equivalent DB2 keywords and functions.
        2. Make sure to use the appropriate data types (e.g. VARCHAR2 in Oracle vs VARCHAR in DB2).
        3. Verify that the syntax for any JOINs is correct for DB2.
        4. If the Oracle query uses an outer join, make sure to use the correct syntax for DB2.
        5. If the Oracle query uses the CONNECT BY PRIOR clause, replace it with a recursive common table expression in DB2.
        6. Pay attention to the way NULLs are handled.
        7. If the Oracle query uses PL/SQL variables, make sure to replace them with appropriate DB2 variables.
        8. Make sure to use the correct value for the MAXIMO database name in the query.
        9. Change all references to the keyword 'SYSDATE' to 'CURRENT TIMESTAMP'.
        10. If the table name starts with 'MAXIMO_', prefix it with 'MAXIMO'.
        12. Replace the keyword 'NVL' with 'COALESCE'.
        13. Replace the keyword 'ROWNUM' with 'ROW_NUMBER() OVER'.
        14. Replace the keyword 'CONCAT' with '||'.
        15. Replace the keyword 'CONNECT BY' with 'WITH RECURSIVE'.
        16. Use the 'MAXIMO.TABLE_NAME' syntax for table names, and suffix with an alias.
        17. Use the 'MAXIMO.COLUMN_NAME' syntax for column names.
        18. Replace the keyword 'INSTR' with 'LOCATE'.

        19. Keep single quotes as they are, and do not try and wrap double quotes around single quotes. 
        20. remove all semicolons at the end of the query.

        21: Always leave a space before the closing parenthesis when writing a SQL statement.

        22. Do not include a time zone in the query.

        Return only the new SQL statement. Do not include anything other than the SQL in your reponse. 

        """

    def invoke(self, input):
        super().__buildtemplate__()
        super().__buildchain__()
        return super().__invoke__(input)


"""

String To Oracle SQL Conversion Template
-- cleaning up a string to an oracle query.

"""
class ParseStringToOracleSQL(LLMTemplate): 


    def __init__(self, sql=None, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.args = ["raw_sql"]

        self.prompt = """
        Here is a string. It represents an Oracle SQL Query: {raw_sql}.
    
        I want you to: 
    
        1. extract and concatenate the SQL from the string of the sqlText variable up to the point that the sqlText variable ends with a semicolon.
        2. replace params["where"] with 1=1
        3. Ensure that the syntax of this query is appropriate for an Oracle databases. 
        4. Remove the semicolon from the end of the statement. 
    
        Return only the new SQL statement. Do not include anything other than SQL in your response. 

        """

    def invoke(self, input):
        super().__buildtemplate__()
        super().__buildchain__()
        return super().__invoke__(input)


"""

White label templates.
the user can pass in whatever prompt he/she wants with args.

"""
class WhiteLabelTemplate(LLMTemplate): 


    def __init__(self, prompt=None, *args, **kwargs):
        super().__init__()
        self.prompt = prompt
        if type(args.__class__()) is not type([].__class__()): 
            raise Exception("Invalid args: ['1', '2'] needed")
        self.args = args
        self.kwargs = kwargs




"""
Maximo Automation Script template - script generation
"""
class MaximoAutomationScriptTemplateScript(LLMTemplate): 

    def __init__(self, input=None, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.args = ["requirement"]
        self.input = input

        self.prompt = """
        Here is an IBM Maximo EAM requirement. The requirement is as follows: {requirement}.
    
        The user intends to write a Maximo Automation Script in the Jython programming language. 

        I want you to: 
    
        1. Convert the requirement in Jython. 
        2. The Maximo system does not include access to the os or system libraries. Try and use the native mbo and jython libraries in your output.
    
        Return only the code. Do not include anything other than the code in your response. 
        """

    def invoke(self, input):
        super().__buildtemplate__()
        super().__buildchain__()
        return super().__invoke__(input)

"""
Maximo Automation Script template - script for inboud integration 
"""
class MaximoAutomationScriptTemplateScript_IntegrationInbound(LLMTemplate): 

    def __init__(self, input=None, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.args = [ "requirement" ]
        self.input = input

        self.prompt = """
        Here is an IBM Maximo EAM requirement. The requirement is as follows: {requirement}.
    
        The user intends to write a Maximo Automation Script in the Jython programming language. 

        This script is an inbound integration. Meaning, that the script will activate at some point in the message queue when the user is sending data from an external system into Maximo.

        I want you to: 
    
        1. Convert the requirement in Jython. 
        2. The Maximo system does not include access to the os or system libraries. Try and use the native mbo and jython libraries in your output.
        3. The script has access to certain implicit variables, meaning that when the script activates, it can access the inbound record by using the irData and erData respectively. 

        Return only the code. Do not include anything other than the code in your response. 

        """

    def invoke(self, input):
        super().__buildtemplate__()
        super().__buildchain__()
        return super().__invoke__(input)


"""
Maximo Automation Script template - description generation

** args = takes in the original requirement as input.

"""
class MaximoAutomationScriptTemplateDescription(LLMTemplate): 

    def __init__(self, input=None, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.args = ["requirement"]
        self.input = input

        self.prompt = """
        Here is an IBM Maximo Automation requirement. The requirement is as follows: {requirement}.
    
        I just asked you to write the script for it, however.

        I want you to: 
    
        1. Convert this requirement into a small, 50 word long description. 
        2. The description must simplify the requirement that I just passed to you. 
    
        Return only the description. Nothing else. 
        """

    """
    input must be the original requirement
    """
    def invoke(self, input):
        super().__buildtemplate__()
        super().__buildchain__()
        return super().__invoke__(input)


"""
Maximo Automation Script template - automation script name generation

** args = takes in the original requirement as input.

"""
class MaximoAutomationScriptTemplateName(LLMTemplate): 

    def __init__(self, input=None, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.args = ["requirement"]
        self.input = input

        self.prompt = """
        Here is an IBM Maximo Automation requirement. The requirement is as follows: {requirement}.
    
        I just asked you to write the script for it, however.

        I want you to: 
    
        1. Give this requirement a simple name.  
        2. The name must be in all upper case characters and consist of underscore _ values in between each word. 
        2. The name cannot be longer than 20 characters long.
    
        Return only the name. Nothing else.
        """

    """
    input must be the original requirement
    """
    def invoke(self, input):
        super().__buildtemplate__()
        super().__buildchain__()
        return super().__invoke__(input)
    

























