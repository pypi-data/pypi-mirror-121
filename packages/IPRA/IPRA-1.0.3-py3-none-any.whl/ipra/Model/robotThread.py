from ipra.Model.Robot.baseRobot import BaseRobot
from ipra.Model.Robot.bocgRobot import BOCGRobot
from ipra.Model.Robot.pruRobot import PruRobot
from ipra.Model.Robot.axaRobot import AxaRobot
from ipra.Model.Robot.chinaLifeRobot import ChinaLifeRobot
from ipra.Model.Robot.fwdRobot import FwdRobot
from ipra.Model.Robot.aiaRobot import AiaRobot
import threading




class robotThread (threading.Thread):
    def __init__(self, type , policyList , frame , reportPath, inputPath):
        threading.Thread.__init__(self)
        self.type = type
        self.policyList = policyList
        self.frame = frame
        self._stopevent = threading.Event()
        self.robotInstance = None
        self.reportPath = reportPath
        self.inputPath = inputPath

    def run(self):
        print("Starting " + self.type)
        self.createRobotClass()
        print("Exiting " + self.name)

    def join(self, timeout):
        self._stopevent.set()
        if self.robotInstance != None:
            self.robotInstance.setIsStopped(True)
        threading.Thread.join(self, timeout)

    def createRobotClass(self):
        if self.type == 'AIA':
            print('AIA type')
            self.robotInstance = AiaRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execRobot()
            print('AIA completed')
        elif self.type == 'AXA':
            print('AXA type')
            self.robotInstance = AxaRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execRobot()
            print('AXA completed')
        elif self.type == 'BOCG':
            print('BOCG type')
            self.robotInstance = BOCGRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execRobot()
            print('BOCG completed')
        elif self.type == 'CHINA LIFE':
            print('CHINA LIFE type')
            self.robotInstance = ChinaLifeRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execRobot()
            print('CHINA LIFE completed')
        elif self.type == 'PRU':
            print('PRU type')
            self.robotInstance = PruRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execRobot()
            print('PRU completed')
        elif self.type == "FWD":
            print('FWD type')
            self.robotInstance = FwdRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execRobot()


    