# -*- coding: utf-8 -*-
"""

"""

def test_008cycledNetworks(self):
      self.createTestNet(3,1,"all")
      time.sleep(2)
      self.assertFalse(self.Thenetwork.checkAllEdges,"cyclic net created")