from typing import overload
from Model.Robot.baseRobot import BaseRobot
from Model.Robot.bocgRobot import BOCGRobot
from Model.Robot.pruRobot import PruRobot
from Model.Robot.axaRobot import AxaRobot
from Model.robotThread import robotThread
from Model.Robot.fwdRobot import FwdRobot
from Model.Robot.chinaLifeRobot import ChinaLifeRobot
from Model.Robot.aiaRobot import AiaRobot

class reportThread (robotThread):
    def __init__(self, type , policyList , frame, reportPath,inputPath):
        robotThread.__init__(self,type,policyList,frame, reportPath,inputPath)
        pass

    def createRobotClass(self):
        if self.type == 'AIA':
            print('AIA type')
            self.robotInstance = AiaRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()
            print('AIA completed')
        elif self.type == 'AXA':
            print('AXA type')
            self.robotInstance = AxaRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()
            print('AXA completed')
        elif self.type == 'BOCG':
            print('BOCG type')
            self.robotInstance = BOCGRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()
            print('BOCG completed')
        elif self.type == 'CHINA LIFE':
            print('CHINA LIFE type')
            self.robotInstance = ChinaLifeRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()
            print('CHINA LIFE completed')
        elif self.type == 'PRU':
            print('PRU type')
            self.robotInstance = PruRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()
            print('PRU completed')
        elif self.type == "FWD":
            print('FWD type')
            self.robotInstance = FwdRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()


    