#!/usr/bin/env python
from __future__ import print_function
import sys
sys.path.extend(['..', '../../..'])
from mupif import *
import conf_vpn as cfg
import logging
log = logging.getLogger()

import time as timeTime
start = timeTime.time()
log.info('Timer started')

#locate nameserver
ns = PyroUtil.connectNameServer(nshost=cfg.nshost, nsport=cfg.nsport, hkey=cfg.hkey)
#localize JobManager running on (remote) server and create a tunnel to it
#allocate the thermal server
solverJobManRecNoSSH = (cfg.serverPort, cfg.serverPort, cfg.server, '', cfg.jobManName)

jobNatport = -1

try:
    appRec = PyroUtil.allocateApplicationWithJobManager( ns, solverJobManRecNoSSH, jobNatport, sshClient='manual', options='', sshHost = '' )
    log.info("Allocated application %s" % appRec)
    thermal = appRec.getApplication()
except Exception as e:
    log.exception(e)
else:
    if thermal is not None:
        appsig=thermal.getApplicationSignature()
        log.info("Working thermalServer " + appsig)
        mechanical = PyroUtil.connectApp(ns, 'mechanical')
        time  = 0.
        dt = 0.
        timestepnumber = 0
        targetTime = 10.0

        while (abs(time - targetTime) > 1.e-6):

            log.debug("Step: %g %g %g"%(timestepnumber,time,dt))
            # create a time step
            istep = TimeStep.TimeStep(time, dt, timestepnumber)

            try:
                thermal.solveStep(istep)
                f = thermal.getField(FieldID.FID_Temperature, istep.getTime())
                data = f.field2VTKData().tofile('T_%s'%str(timestepnumber))

                mechanical.setField(f)
                sol = mechanical.solveStep(istep) 
                f = mechanical.getField(FieldID.FID_Displacement, istep.getTime())
                data = f.field2VTKData().tofile('M_%s'%str(timestepnumber))

                thermal.finishStep(istep)
                mechanical.finishStep(istep)

                # determine critical time step
                dt = min (thermal.getCriticalTimeStep(), mechanical.getCriticalTimeStep())

                # update time
                time = time+dt
                if (time > targetTime):
                    # make sure we reach targetTime at the end
                    time = targetTime
                timestepnumber = timestepnumber+1

            except APIError.APIError as e:
                log.error("Following API error occurred:",e)
                break
        mechanical.terminate();     

    else:
        log.debug("Connection to thermal server failed, exiting")

finally:
    if appRec: appRec.terminateAll()


