# -*- coding: utf-8 -*-
"""

!!!! TO BE IMPLEMENTED !!!

"""

import requests
import unittest
import testTools
import json
import network.createNetwork as net
import time

class TestAgentEndpoints(unittest.TestCase):
   
   @classmethod
   def setUpClass(self):
      self.endpoints = testTools.Endpoints()
      self.headers = self.endpoints.getHeaders()
      self.agents = self.endpoints.agents
      self.basePath = "http://10.200.1.83:5000/"
      self.dstNet = "10.0.3.0/24"
#   
#   def setup(self):
#      
#   
#   def teradown(self):
#      self.deleteDoc()
   
   def test_insertProperty(self):
      exampleData = {
                    "out_rate": "100mbps",
                    "in_rate": "100mbps",
                    "rules": [
                      {
                        "dst_net": self.dstNet,
                        "out_rate": "10mbps",
                        "delay": "10ms",
                        "dispersion": "10ms",
                        "loss": "0.1",
                        "corrupt": "0.1",
                        "duplicate": "0.1",
                        "reorder": "0.1"
                      }
                    ]
                  }
      return requests.post(self.basePath + "tc-config/",
                        json.dumps(exampleData),headers = self.headers)