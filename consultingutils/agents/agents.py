

import os
import sys

from pathlib import Path
from llama_index import download_loader
import json
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import os


class Agent(object): 


    def __init__(self) -> None:
        pass



"""
Research Agent
- Provides and answer to a specific question off a corpus of information
"""
class ResearchAgent(Agent): 

    def __init__(self) -> None:
        super().__init__()


    def ask_question(self, input=None):
        if input == None: 
            raise Exception("No question has been provided")
        
        self.question = input
        return self


    def from_document_directory(self, file_path=None): 
        if file_path == None: 
            raise Exception("No file has been provided")


        documents = SimpleDirectoryReader(file_path).load_data()
        index = GPTSimpleVectorIndex(documents)
        r = index.query(self.question)

        return r.response