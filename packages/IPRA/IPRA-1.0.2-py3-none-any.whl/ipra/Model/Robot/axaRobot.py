from ipra.Model.Robot.baseRobot import BaseRobot
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
import xlsxwriter
import threading

class AxaRobot(BaseRobot):

    def __init__(self, policyList, frame, reportPath,inputPath):
        super().__init__(policyList, frame, reportPath,inputPath)
        self.maxPolicyListSize = len(policyList)
        self.workbook = xlsxwriter.Workbook(self.reportPath+'AXA_report.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write(0, 0, "Policy No.")
 
    def waitingLoginComplete(self):
        self.browser.get("https://www.axa.com.hk/zh/login#?Tab$login-tab=consultant-login")
        self.browser.find_element_by_xpath("/html/body/div/div/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div/div/button").click()
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.frame.setStatusLableText("Waiting Login")

        while not self.isLogin and not self.isStopped:
            try:
                WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[4]/div/ul/li[1]/span")))
                self.isLogin=True  
            except:
                time.sleep(3)
        else:
            pass

        if self.isLogin:
            self.frame.setStatusLableText("Logged in")

    def scrapPolicy(self):
        url_link = "window.open('https://axaiprooffice.force.com/_ui/search/ui/UnifiedSearchResults?searchType=2&sen=a00&sen=001&sen=005&str={}');"
        for policy in self.policyList:
            if self.isStopped:
                return
            
            self.frame.setStatusLableText("Processing "+str(policy))

            policy_url_link = url_link.format(policy)
            self.browser.execute_script(policy_url_link)
            self.browser.switch_to.window(self.browser.window_handles[1])
            try:
                self.browser.find_element_by_link_text(policy).click()
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(self.reportPath+policy+".txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify()) 
                file1.close()
            except:
                print(policy+" is not in this A/C")
                self.frame.setStatusLableText(policy+" is not found")
            finally:
                self.frame.setStatusLableText(policy+" completed")
                self.frame.setStatusProgresValueByValue(1)
                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])
                self.buildReportQueue.append(policy)

    def buildReport(self):
        self.buildReportThread = threading.Thread(target = self.__buildReport)
        self.buildReportThread.start()
        self.buildReportHeaderFullFlow()
        pass

    def buildReportOnly(self):
        self.buildReportThread = threading.Thread(target = self.__buildReportOnly)
        self.buildReportThread.start()
        self.buildReportHeaderHalfFlow()
        pass

    def buildReportHeaderFullFlow(self):
        self.buildHeaderThread = threading.Thread(target = self.__buildReportHeaderFullFlow)
        self.buildHeaderThread.start()
        pass
    
    def buildReportHeaderHalfFlow(self):
        self.buildHeaderThread = threading.Thread(target = self.__buildReportHeaderHalfFlow)
        self.buildHeaderThread.start()
        pass
 
    def __buildReportHeaderFullFlow(self):
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildReportQueue:
                if self.isStopped:
                    return
                try:
                    file = open(self.reportPath+policy+".txt",encoding="utf-8")#append mode 
                    #Full Html src
                    soup_all_src = BeautifulSoup(file.read(), 'lxml')
                    file.close()

                    soup_pdBody = self.SearchByHtmlTagClassValue(soup_all_src,'div','pbBody')
                    soup_pbSubsection = self.SearchByHtmlTagClassValue(soup_pdBody,'div','pbSubsection')
                    soup_pb_header = self.SearchByHtmlTagClassValue(soup_pbSubsection,'td','labelCol')
                    
                    for col_num, strong_tag in enumerate(soup_pb_header.find_all('td')):
                        self.worksheet.write(0, col_num+1, strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        
                    #No error when building the header,break all loop and then stop this thread
                    policy_iteration = self.maxPolicyListSize + 1
                    break
                except FileNotFoundError:
                    pass
                except Exception:
                    pass
                finally:
                    policy_iteration = policy_iteration + 1
            
    def __buildReportHeaderHalfFlow(self):
        for policy in self.policyList:
            if self.isStopped:
                return
            try:
                file = open(self.inputPath+policy+".txt",encoding="utf-8")#append mode 
                #Full Html src
                soup_all_src = BeautifulSoup(file.read(), 'lxml')
                file.close()

                soup_pdBody = self.SearchByHtmlTagClassValue(soup_all_src,'div','pbBody')
                soup_pbSubsection = self.SearchByHtmlTagClassValue(soup_pdBody,'div','pbSubsection')
                soup_pb_header = self.SearchByHtmlTagClassValue(soup_pbSubsection,'td','labelCol')
                
                for col_num, strong_tag in enumerate(soup_pb_header.find_all('td')):
                    self.worksheet.write(0, col_num+1, strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    
                #No error when building the header,break all loop and then stop this thread
                break
            except FileNotFoundError as ex:
                pass
            except Exception as ex:
                pass
 
    def __buildReport(self):
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildReportQueue:
                if self.isStopped:
                    return
                self.frame.setStatusLableText("Build Report "+str(policy))
                try:
                    self.worksheet.write(policy_iteration+1,0,str(policy))
                    file = open(self.reportPath+policy+".txt",encoding="utf-8")#append mode 
                    #Full Html src
                    soup_all_src = BeautifulSoup(file.read(), 'lxml')
                    file.close()

                    soup_pdBody = self.SearchByHtmlTagClassValue(soup_all_src,'div','pbBody')
                    soup_pbSubsection = self.SearchByHtmlTagClassValue(soup_pdBody,'div','pbSubsection')
                    soup_pb_value = self.SearchByHtmlTagClassValue(soup_pbSubsection,'td','dataCol')
                    
                    for col_num,strong_tag in enumerate(soup_pb_value.find_all('td')):
                        self.worksheet.write(policy_iteration+1, col_num+1, strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        
                except FileNotFoundError:
                    self.worksheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                    self.frame.setStatusLableText("Build Report "+str(policy)+ " Not Found")
                except Exception:
                    self.worksheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!")
                    self.frame.setStatusLableText("Build Report "+str(policy)+ " Failed")
                finally:
                    self.frame.setStatusProgresValueByValue(1)
                    policy_iteration = policy_iteration + 1
                    if policy in self.buildReportQueue:
                        self.buildReportQueue.remove(policy)
        
        self.buildHeaderThread.join()
        self.workbook.close()
        self.frame.setStatusLableText("Completed")

    def __buildReportOnly(self):
        for policy_iteration,policy in enumerate(self.policyList):
            if self.isStopped:
                return
            self.frame.setStatusLableText("Build Report "+str(policy))
            try:
                self.worksheet.write(policy_iteration+1,0,str(policy))
                file = open(self.inputPath+policy+".txt",encoding="utf-8")#append mode 
                #Full Html src
                soup_all_src = BeautifulSoup(file.read(), 'lxml')
                file.close()

                soup_pdBody = self.SearchByHtmlTagClassValue(soup_all_src,'div','pbBody')
                soup_pbSubsection = self.SearchByHtmlTagClassValue(soup_pdBody,'div','pbSubsection')
                soup_pb_value = self.SearchByHtmlTagClassValue(soup_pbSubsection,'td','dataCol')
                
                for col_num,strong_tag in enumerate(soup_pb_value.find_all('td')):
                    self.worksheet.write(policy_iteration+1, col_num+1, strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    
            except FileNotFoundError:
                self.worksheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                self.frame.setStatusLableText("Build Report "+str(policy)+ " Not Found")
            except Exception:
                self.worksheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!")
                self.frame.setStatusLableText("Build Report "+str(policy)+ " Failed")
            finally:
                self.frame.setStatusProgresValueByValue(2)
        
        self.buildHeaderThread.join()
        self.workbook.close()
        self.frame.setStatusLableText("Completed")

        
