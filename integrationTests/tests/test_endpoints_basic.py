# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 17:51:26 2018

"""
import requests
import unittest
import testTools
import json

class TestNMEndpoints(unittest.TestCase):

   @classmethod
   def setUpClass(self):
      self.endpoints = testTools.Tools()
      self.headers = self.endpoints.getHeaders()
      self.basePath = self.endpoints.getBasepath()
      self.testDocName = "testDoc"
      self.docID = -1

   def setUp(self):
      self.createReq = self.createDoc()
      self.docID = self.createReq.json()["id"]
      
   def tearDown(self):
      self.deleteDoc()
   
   def test_001createDoc(self,delete = True):
      if self.createReq.status_code == 200:
         self.docID = self.createReq.json()["id"]
         getReq = requests.get(self.basePath + "doc/" + str(self.docID),headers = self.headers)
         if getReq.status_code == 200: 
            self.assertEqual(getReq.json()["docName"],self.testDocName,"retreived Doc not identical to created Doc.")         
         else: self.fail("could not retreive Doc with docID: " + str(self.docID))
      else: self.fail("could not create Doc.Code: " + str(self.createReq.status_code) + ". Error: " + self.createReq.text)
      if delete: self.deleteDoc()

   def test_002deleteDoc(self):
      if self.docID != -1:
         getReq = requests.get(self.basePath + "doc/" + str(self.docID),headers = self.headers)
         if getReq.json()["docName"] == self.testDocName:
            deleteReq = requests.delete(self.basePath + "doc/" + str(self.docID))
            if deleteReq.status_code == 200:
               getReq = requests.get(self.basePath + "doc/" + str(self.docID),headers = self.headers)
               stateExpected = str(self.endpoints.nmSwaggerData["paths"]["/doc/{docId}"]["delete"]["responses"].keys()[1])
               self.assertEqual(stateExpected,str(getReq.status_code),"Delete Status Swagger: " + stateExpected + ". Status return: " + str(getReq.status_code))               
            else: self.fail("document " + str(self.docID) + " could not be deleted.")
         else: self.fail("docid : " + str(self.docID) + " not found.")
      else: self.fail("no document Created")
      
   def test_003createNode(self):            
      if self.docID != -1:
         nodeData,nodeRequ = self.createNode()
         if nodeRequ.status_code == 200:
            nodeID = nodeRequ.json().keys()[0]
            nodeGetReq = requests.get(self.basePath + "doc/" + str(self.docID) + "/vertex/" + str(nodeID),
                                      headers = self.headers)
            if nodeGetReq.status_code == 200:
               for attr in nodeData.keys(): 
                  returnData = nodeGetReq.json()[str(nodeID)]
                  self.assertEqual(nodeData[attr],returnData[attr],
                                         "attribute " + attr + " of node " + str(nodeID) + " not matching.")
            else: self.fail("could not retreive node " + str(nodeID))
         else: self.fail("could not create Node. Code: " + str(nodeRequ.status_code) + ". Error: " + nodeRequ.text)
      else: self.fail("no document Created")
      
   def test_004CreateSubnet(self):
      if self.docID != -1:
         netData,netReq = self.createSubnet()
         if netReq.status_code == 200:
            netID = netReq.json().keys()[0]
            nodeGetReq = requests.get(self.basePath + "doc/" + str(self.docID) + "/vertex/" + str(netID),headers = self.headers)
            if nodeGetReq.status_code == 200:
               for attr in netData.keys(): 
                  returnData = nodeGetReq.json()[str(netID)]
                  self.assertEqual(netData[attr],returnData[attr],
                                         "attribute " + attr + " of node " + str(netID) + " not matching.")
            else: self.fail("could not retreive node " + str(netID))
         else: self.fail("could not create Node. Code: " + str(netReq.status_code) + ". Error: " + netReq.text)
      else: self.fail("no document Created")
   
   def test_005CreateEdge(self):
      if self.docID != -1:
         netData,netReq = self.createSubnet()
         netID = netReq.json().keys()[0]
         nodeData,nodeReq = self.createNode()
         nodeID = nodeReq.json().keys()[0]
         req = requests.post(self.basePath + "doc/" + str(self.docID) + "/edge/" + str(netID) + "/" + str(nodeID),headers = self.headers)
         if req.status_code == 200:
            reqGet = requests.get(self.basePath + "doc/" + str(self.docID) + "/edge/" + str(netID) + "/" + str(nodeID),headers = self.headers)
            self.assertEqual(200,reqGet.status_code,"could not retreive Edge created from " + netID + " to " + nodeID)
         else: self.fail("could not create Edge from " + str(netID) + " tp " + str(nodeID) + ". Code: " + str(netReq.status_code) + ". Error: " + netReq.text)
      else: self.fail("no document Created")

   def createDoc(self):
      return requests.post(self.basePath + "doc/",data = json.dumps({"docName":self.testDocName}),headers = self.headers)

   def deleteDoc(self):
      return requests.delete(self.basePath + "doc/" + str(self.docID))

   def createNode(self):
      nodeData = self.endpoints.getSwaggerData("/doc/{docId}/node")
      return nodeData,requests.post(self.basePath + "doc/" + str(self.docID) + "/node",
                                  data = json.dumps(nodeData), headers = self.headers)

   def createSubnet(self):
      netData = self.endpoints.getSwaggerData("/doc/{docId}/net")
      return netData,requests.post(self.basePath + "doc/" + str(self.docID) + "/net",
                           data = json.dumps(netData),headers = self.headers)
            