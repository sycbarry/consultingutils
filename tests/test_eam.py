
import unittest
import os



from consultingutils.llmtemplates.llmtemplates import LLMTemplate, OracleToDB2SQL
from consultingutils.eam.eam import EAM, Maximo

class Test(unittest.TestCase): 

    def __init__(self, *args, **kwargs): 
        super(Test, self).__init__(*args, **kwargs)

    def test_one(self): 

        maximo = Maximo(
            api_key="", 
            endpoint=""
        )

        # make a test to the endpoint
        #response = maximo.test_endpoint()

        os.environ["OPENAI_API_KEY"] = ""

        # invoke maximo obj
        new_script =  maximo\
            .integration_script_inbound()\
            .make_from_requirement(r"C:\Users\barrys\Python_Scripts\consultingutils\tests\requirement.conf")

            #.add_mapping_reference(r"C:\Users\barrys\Python_Scripts\consultingutils\tests\maximo.json")\

        # test script smoehow.
        print(new_script)

        # push to maximo.
        # TODO finish this.
        #response = maximo.push_script(new_script)
        #print(response)

        return None
