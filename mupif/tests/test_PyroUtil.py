import unittest
import sys
sys.path.append('../..')

from mupif import *
import math
import numpy as np
import pyvtk
import types

class test_PyroUtil(unittest.TestCase):
    def setUp(self):
        context = PyroUtil.SSHContext._init__('nitram','manual')
        tunnel  = PyroUtil.sshTunnel.__init__(self, "remoteHost", "userName", "localPort", "remotePort", 'ssh')
        tunnel.connectNameServer("nshost", "nsport", "hkey")
        tunnel.terminate()
# python test_Mesh.py for stand-alone test being run
if __name__=='__main__': unittest.main()
