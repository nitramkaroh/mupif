import unittest
import sys
sys.path.append('../..')

from mupif import *
import math
import numpy as np
import pyvtk
import types

class Operator_TestCase(unittest.TestCase):
    def setUp(self):
        operator = operatorUtil.OperatorEMailInteraction(From='appAPI@gmail.com',
                                                              To='operator@gmail.com',
                                                              smtpHost='smtp.something.com',
                                                              imapHost='imap.gmail.com',
                                                              imapUser='appAPI')
        operator.inputs = {}
        operator.outputs = {}
        operator.key = 'Operator-results'

        operator.contactOperator("CS", "J01", "message")
        operator.checkOperatorResponse (self, "workflowID", "jobID")
  
# python test_Mesh.py for stand-alone test being run
if __name__=='__main__': unittest.main()
