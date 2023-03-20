import os
import sys
from collections import deque 
from tqdm import trange


"""
a chain is a collection of templates, that we pass in the constructor. 
the output of one template is the input of the next.

the state of each output is maintained in a data structure
that is passed in teh kwargs of the constructor.
"""

class Chain(object): 


    def __init__(self, *args, **kwargs) -> None:
        self.templates = [*args]
        self.state = kwargs
        pass

    def __invoke__(self, input=None):

        if input == None: 
            raise NotImplementedError("no initial input provided.")

        # queue of inputs to the next prompt
        queue = deque([])
        queue.append(input)

        t = trange((len(self.templates)), desc="building...", leave=True)
        for i in t:
            input = queue.pop() # pop the latest output
            response = self.templates[i].invoke(input) # feed that into the next template. 
            if response is not None: 
                for index, _key in enumerate(self.state):
                    if index == i: 
                        self.state[_key] = response.strip()
                queue.append(response) # feed teh response into the queue 

        
        return self.state



"""
The zero shot chain is a chain that attempts to improve its previous results through testing.
The idea here is that the chain will go through a self re-inforcement learning cycle with no 
initial knowledge on a subject.
"""

class ZeroShotChain(object): 


    def __init__(self, *args, **kwargs) -> None:
        super.__init__(*args, **kwargs)


    def __invoke__(input=None): 

        if input == None: 
            raise FileNotFoundError("no input provided to this chain.")


"""
Zero shot chain - this is a chain that
reads from documentation and aims to teach itself what 
to do along the way, at each point of failure. 

More robust than a single ZeroShotChain
"""
class ZeroShotChainFromDocs(ZeroShotChain): 


    def __init__(self, *args, **kwargs) -> None:
        self.__init__(*args, **kwargs)
        pass

    def __invoke__(input=None): 
        if input == None: 
            raise Exception('no input to files found.')




