

import os
import urllib.request
from configparser import ConfigParser

from consultingutils.llmtemplates.llmtemplates import \
    MaximoAutomationScriptTemplateScript, \
    MaximoAutomationScriptTemplateDescription, \
    MaximoAutomationScriptTemplateName, \
    MaximoAutomationScriptTemplateScript_IntegrationInbound

from consultingutils.chain.chain import Chain


class EAM(object): 

    def __init__(
      self, 
      endpoint=None,
    ) -> None:
        self.endpoint = endpoint
        pass

    
    def test_endpoint(self):
       None


class Maximo(EAM): 
    
    def __init__(
            self, 
            endpoint=None, 
            api_key=None
            ) -> None:
        super().__init__(endpoint)
        self.api_key = api_key


    """
    Test end endpoint prior to anything.
    """
    def test_endpoint(self): 

      request = urllib.request.Request(self.endpoint, headers={"MAXAUTH": self.api_key}, method="GET")
      try: 
        with urllib.request.urlopen(request) as response: 
            return response.status
      except Exception as e: 
         raise ConnectionError(e)


    """
    General automation script
    """
    def automation_script(self): 
      self.chain = Chain(*[
         MaximoAutomationScriptTemplateScript(), 
         MaximoAutomationScriptTemplateDescription(), 
         MaximoAutomationScriptTemplateName()], 
                         source=None, 
                         description=None, 
                         autoscript=None
                         )
      return self

    def add_mapping_reference(self, path=None): 
        if path == None: 
          raise FileNotFoundError("Invalid mapping file provided.")
        self.mapping_file_path = path
        return self

    """
    Integration script
    """
    def integration_script_inbound(self): 
      self.chain = Chain(*[
         MaximoAutomationScriptTemplateScript_IntegrationInbound(), 
         MaximoAutomationScriptTemplateDescription(), 
         MaximoAutomationScriptTemplateName()], 
                         source=None, 
                         description=None, 
                         autoscript=None
                         )
      return self


    """
    Chain invokers.
    """
    def make_from_requirement(self, path=None):
      if path == None: 
        raise FileNotFoundError("no path specified")

      parser = ConfigParser()
      parser.read(path)

      requirement = parser.get('automationscript', 'requirement')
      if requirement is None: 
         raise FileExistsError("no requirement specified in .conf file")

        
      """
      name, 
      source, 
      description
      """

      return self.chain.__invoke__(requirement)
      


    def push_script(self, ds=None): 
      import json
      request = urllib.request.Request(self.endpoint + "autoscript", data=json.dumps(ds), headers={"MAXAUTH": self.api_key, "Accept": "application/json", "Content-Type": "application/json"}, method="POST")
      try: 
        with urllib.request.urlopen(request) as response: 
            return response
      except Exception as e: 
         raise ConnectionError(e)


