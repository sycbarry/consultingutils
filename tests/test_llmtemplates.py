import unittest
import os



from consultingutils.llmtemplates.llmtemplates import LLMTemplate, OracleToDB2SQL

class Test(unittest.TestCase): 

    def __init__(self, *args, **kwargs): 
        super(Test, self).__init__(*args, **kwargs)

    def test_one(self): 

        os.environ["OPENAI_API_KEY"] = ""
        sql = "select count(*) from maximo"
        result = OracleToDB2SQL().invoke(sql)

        self.assertNotEqual(None, result)



