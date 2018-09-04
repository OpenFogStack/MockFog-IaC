
"""
See Documentation -> Quality of Service
"""

import unittest
import testTools
import time


class TestBasicNetwork(unittest.TestCase):
   
   def __init__(self, testname, nodes, nets, mode):
      super(TestBasicNetwork, self).__init__(testname)
      self.nodes = nodes
      self.nets = nets
      self.mode = mode
   
#   @classmethod
#   def setUpClass(self):
#   def setUp(self):
#   def tearDown(self):
      

   def test_network(self):
      self.tools = testTools.Tools()
      self.tools.createTestNet(self.nets,self.nodes,self.mode)
      time.sleep(1)
      build = False
      build = self.tools.buildTestNet()
      self.assertTrue(build,"Network could not be instantiated.")
      status = self.tools.checkStatus()
      self.assertTrue(status[0],status[1])
      time.sleep(20)
      self.tools.getAgents()
      self.assertTrue(self.tools.checkNodesAlive(),"created nodes not online...")      
      self.assertTrue(self.tools.destroyNet(),"created Nodes still online.")
      self.tools.deleteDoc()
      
    
   
   

   
   
   