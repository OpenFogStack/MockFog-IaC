
"""
See Documentation -> Quality of Service
"""

import unittest
import testTools
import json
from pingAgent import Agent

class TestProperties(unittest.TestCase):
   
   def __init__(self, testname, network, property_):
      super(TestProperties, self).__init__(testname)
      self.property_ = property_
      self.network = network
      
#   @classmethod
#   def setUpClass(self):
   def setUp(self):
      self.tools = testTools.Tools()
#   def tearDown(self):
      

   def test_injection(self):
      
      agents = Agent(self.tools.getAgents(),"shell")
      agents.addHostsToNodes
      self.assertTrue(self.tools.checkNodesAlive(),"created nodes not online...")
      testProp = json.dumps({
           "in_rate": "1000000",
           "out_rate": "1000000",
           "delay": "10",
           "dispersion": "0",
           "loss": "0.0",
           "corrupt": "0.0",
           "duplicate": "0.0",
           "reorder": "0.0"
         })
      nodes = self.network.nodeIDs
      edge = self.network.getNodeEdge(nodes[0])
      self.network.putEdge(edge[0],edge[1],testProp)
      
      self.assertTrue(self.tools.destroyNet(),"created Nodes still online.")
      self.tools.deleteDoc()
      
    
   
   

   
   
   