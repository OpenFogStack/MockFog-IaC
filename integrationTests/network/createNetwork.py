# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 09:59:49 2018

@author: miconzelmann
"""

import requests
import json
import time

class createTestNetwork():
   """ generates Networks for testing purpose """

   
       
   def __init__(self,basePath,headers):
       self.headers = headers
       self.basePath = basePath
       self.subNetIDs = []
       self.error = ""
       self.edges = []
       self.nodeEdges = []
       self.nodeIDs = []
       self.nodeIDPool = range(999,0,-1)
       
   def createDoc(self,docName):
       ## Create DOc
       postPath = self.basePath + "doc"        
       r = requests.post(postPath,
                         data = json.dumps({"docName":docName,
                                            "addr":"192.168.100.0/24"}),
                         headers = self.headers)
       if self.evalResponse(r):        
           rJson = r.json()
           self.docID = rJson["id"]
           print("doc " + docName + " with docID: " + str(self.docID) + " created.")        
           return self.docID    
       else : return None
       
   def createNets(self,nNets):
      for i in range(1,nNets+1):
         time.sleep(1)
         postPath = self.basePath + "doc/" + str(self.docID) + "/net"        
         print("create subnet" + str(i) + " in docID " + str(self.docID))
         r = requests.post(postPath,
                           data = json.dumps({"name":"subnet" \
                                             + str(i),"addr":"10." + str(i) \
                                             + ".0.0"  "/24"}),
                           headers = self.headers)
         print("Status: " + str(r.status_code))
         if self.evalResponse(r):
            netID = r.json().keys()[0]
            self.subNetIDs.append(netID)
            print("Created subnet " + str(id) + ". ID: " + netID)
         else: return False
      return True
    
   def createNodesInNets(self,nNodes):
      for netID in self.subNetIDs:
         for i in range(1,nNodes+1):
            time.sleep(1)
            postPath = self.basePath + "doc/" + str(self.docID) + "/node"
            print("create Node Node" + str(self.nodeIDPool.pop()) \
                  + " in Subnet Subnet" + str(netID))
            nodeData = json.dumps({"name": "node" + str(self.nodeIDPool.pop()),
                                   "flavor": "Banana Pi",
                                   "image": "ubuntu-16.04"})
            r = requests.post(postPath,data = nodeData,headers = self.headers)
            if self.evalResponse(r):
               nodeID = r.json().keys()[0]
               self.nodeIDs.append(nodeID)
               if self.createEdge(nodeID,netID) : 
                  self.nodeEdges.append([nodeID,netID])
               else:
                  return False                        
            else: return False
      return True
                
   def connectNets(self,mode):
      if mode == "all":
         # connect all subnets with each other
         for netIDfrom in self.subNetIDs:
            for netIDTo in self.subNetIDs:
               if netIDfrom != netIDTo:
                  time.sleep(0.25)
                  if self.createEdge(netIDfrom,netIDTo):
                     self.edges.append([netIDfrom,netIDTo])

      elif mode == "streight":
         for i in range(0,len(self.subNetIDs)-1):
            if self.createEdge(self.subNetIDs[i],self.subNetIDs[i+1]):
               self.edges.append([self.subNetIDs[i],self.subNetIDs[i+1]])
            
            
   def checkAllEdges(self):
      for edge in self.edges:
         path_ = self.basePath + "doc/" + str(self.docID) \
                     + "/edge/" + str(edge[0]) +"/" + str(edge[1])
         r = requests.get(path_,headers=self.headers)
         if r.status_code != 200: return False
      return True
   
   def createEdge(self,fromID,toID):
      postPath = self.basePath + "doc/" + str(self.docID) + "/edge/" + str(toID) +"/" + str(fromID)
      print("Create edge from id " + fromID + " to " + toID + ".")
      r = requests.post(postPath,headers = self.headers)
      return self.evalResponse(r)
    
   def putEdge(self, fromID, toID, props):
      path = self.basePath + "doc/" + str(self.docID) + "/edge/" + str(toID) +"/" + str(fromID)
      print("Change edge from id " + fromID + " to " + toID + ".")
      r = requests.put(path, data=props, headers = self.headers)
      return self.evalResponse(r)
      
   def getNodeEdge(self,nodeID):
      for edge in self.nodeEdges:
         if edge[0] == nodeID: return edge
      
   def deleteAll(self):
        # DELETE ALL Docs 
      docIDResponse = requests.get(self.basePath + "doc/").json()
      for docIDtmp in docIDResponse["docs"]:    
         print("DELETE doc: " + str(docIDtmp["id"]))
         r = requests.delete(self.basePath + "doc/" + str(docIDtmp["id"]),headers = self.headers)
         print(r.status_code)
          
   def buildNetwork(self,cloud):
        # Create .yml configuration and execute with ansible
      print "building network..." + self.basePath + "doc/" + str(self.docID) + "/bootstrap/" + cloud
      r = requests.get(self.basePath + "doc/" + str(self.docID) + "/bootstrap/" + cloud)
      return self.evalResponse(r)
      
   def evalResponse(self,r):
      if r.status_code != 200 : 
         print("Request failed. Status Code: " + str(r.status_code) + ". Error:" + r.text)
         self.error = r.text
         return False
      else :
         print("Success. Response: " + r.text[0:30])                        
         return True
   
   def destroyNetwork(self):
      r = requests.delete(self.basePath + "doc/" + str(self.docID) +"/destroy/os")
      return self.evalResponse(r)