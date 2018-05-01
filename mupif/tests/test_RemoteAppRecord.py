import unittest
import sys
sys.path.append('../..')

from mupif import *
import math
import numpy as np
import pyvtk
import types

class test_RemoteAppRecord(unittest.TestCase):
    def setUp(self):
        rar = RemoteAppRecord.__init__("app", "appTunnel", "jobMan", "jobManTunnel", "jobID")
        rar.appendNextApplication(self, "app", "appTunnel", "jobID")
        r = rar.getApplication()
        uri = rar.getApplicationUri()
        jm = rar.getJobManager
        id = rar.getJobID()
        rar.terminateApp()
        rar.terminateAll()

# python test_Mesh.py for stand-alone test being run
if __name__=='__main__': unittest.main()
