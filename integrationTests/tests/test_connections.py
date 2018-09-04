# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 21:53:45 2018

@author: miconzelmann
"""

import requests
import unittest
import testTools
import json

class TestNMEndpoints(unittest.TestCase):
   
   @classmethod
   def setUpClass(self):
      self.tools = testTools.Tools()
      
   def test_neo4j(self):
       ### get all docs
       self.assertEquals(requests.get(self.tools.basePath + "docs"),200,
                         "connection failed")
   
   def test_swagger(self):
       self.assertEquals(requests.get(self.tools.swaggerURL),200,
                         "connection failed")
   
   def test_nginx(self):
       self.assertEquals(requests.get(self.tools.webappURL),200,
                                      "connection failed")

   def test_controller(self):
       self.assertEquals(requests.get(self.tools.controllerURI),200,
                                      "connection failed")
   
   