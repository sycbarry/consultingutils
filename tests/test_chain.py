

import unittest
import os

from consultingutils.llmtemplates.llmtemplates import LLMTemplate, OracleToDB2SQL
from consultingutils.eam.eam import EAM, Maximo
from consultingutils.chain.chain import ZeroShotChain, ZeroShotChainFromDocs

class Test(unittest.TestCase): 

    def __init__(self, *args, **kwargs): 
        super(Test, self).__init__(*args, **kwargs)

    def test_one(self): 
        self.assertTrue(True, True)

        chain = ZeroShotChainFromDocs()