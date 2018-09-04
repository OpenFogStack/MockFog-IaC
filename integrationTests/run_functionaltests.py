# -*- coding: utf-8 -*-
"""


"""

import unittest

import tests.test_endpoints_basic as testEndpoints
import tests.test_basic_network as Testnet


# init testsuite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# adding tests

# testing endpoints
suite.addTests(loader.loadTestsFromModule(testEndpoints))

# testing network creation

## single net, multiple nodes
for nodes in range(1,5):
   nets=1
   suite.addTest(Testnet.TestBasicNetwork("test_network",nets,nodes,"all"))


##  multiple nets, one n ode per net, all subnets connected
nodes = 1
for nets in range(1,4):
   suite.addTest(Testnet.TestBasicNetwork("test_network",nets,nodes,"all"))

##  multiple nets, one n ode per net, subnets connected in a row
for nets in range(1,5):
   suite.addTest(Testnet.TestBasicNetwork("test_network",nets,nodes,"streight"))

loader.sortTestMethodsUsing = None

# run tests
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
