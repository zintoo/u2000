#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import socket
import threading
import datetime
import time
import os
try:
    from queue import Queue
except:
    from Queue import Queue

import sys
from omniORB import CORBA
import CosNaming
import emsSessionFactory
import nmsSession, nmsSession__POA
import emsMgr
import managedElementManager
import notifications, notifications__POA
import globaldefs
from colorama import init, AnsiToWin32, Fore, Back, Style
init(wrap=False)

### class for new
class NmsSession_I(nmsSession__POA.NmsSession_I):
    pass
    
### Initialise the ORB
argv = ["-ORBInitRef", "NameService=corbaloc::100.9.2.3:12001/NameService"]
orb = CORBA.ORB_init(argv, CORBA.ORB_ID)
if orb is None:
    print("Failed ->CORBA.ORB_init(argv, CORBA.ORB_ID)")
    
### Obtain a reference to the root naming context 
obj = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)
if rootContext is None:
    print("Failed ->narrow the root naming context")
    
### Resolve the name
name = [CosNaming.NameComponent("TMF_MTNM","Class"),
        CosNaming.NameComponent("HUAWEI","Vendor"),
        CosNaming.NameComponent("Huawei/U2000","EmsInstance"),
        CosNaming.NameComponent("2.0","Version"),
        CosNaming.NameComponent("Huawei/U2000","EmsSessionFactory_I")]
try:
    obj = rootContext.resolve(name)
except CosNaming.NamingContext.NotFound as ex:
    print("Except->Name not found")
    print(ex)

### Narrow the object 
ems_session = obj._narrow(emsSessionFactory.EmsSessionFactory_I)
if ems_session is None:
    print("Object reference is not an EmsSessionFactory_I")

### get session
nms_session_i = NmsSession_I() 
nms_session_o = nms_session_i._this()               
if nms_session_o is None:
    print("Object reference is not an NmsSession_I")
    sys.exit(1)

exclude_probableCause_list = []
#print(exclude_probableCause_list)
##  PS_INDETERMINATE, 0
##  PS_CRITICAL, 1
##  PS_MAJOR, 2
##  PS_MINOR, 3
##  PS_WARNING, 4
##  PS_CLEARED 5
#perceivedSeverity = []

perceivedSeverity = [ notifications.PS_INDETERMINATE,
                      #notifications.PS_CRITICAL,
                      notifications.PS_MAJOR,
                      notifications.PS_MINOR,
                      notifications.PS_WARNING,
                      notifications.PS_CLEARED,
                     ] 

exclude_perceivedSeverity_list = CORBA.Any(notifications._tc_PerceivedSeverityList_T, perceivedSeverity)

def send2LineBotServer(ip, port, message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(15)
        sock.connect((ip, port))
        sock.send(message)
        response = sock.recv(1024)
    except Exception as exp:
        print("send2LineBotServer()", exp)
        
class RLOSMonitor(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.rlos_dict = dict()
        self.rlos_new = dict()
        self.rlos_removed = dict()
        
         
    def setup(self, q):
        self.q = q
        self.session = None
            
    def run(self):
        while True:
            #print('Checking  %d %s' % (round(time.time()), time.strftime("%Y-%m-%d %H:%M:%S")) )
            try:
                query_mtime = round(time.time())
                
                self.session = ems_session.getEmsSession("NMAClient", "my123456", nms_session_o)
                ems = self.session.getManager("EMS")
                
                alarms_tuple = ems.getAllEMSAndMEActiveAlarms(exclude_probableCause_list, exclude_perceivedSeverity_list.value(), 1)
                event_iterator = alarms_tuple[1]
                #more = True
                more = (event_iterator is not None)
                neOldDate = ''
                
                nowday = datetime.date.today()
                today = nowday.strftime('%Y-%m-%d')
                tomonth = nowday.strftime('%Y-%m')
                toyear = nowday.strftime('%Y')
                
                rlos_query = dict()
                self.rlos_new.clear()
                self.rlos_removed.clear()
                event_counter = 0
                
                while more:
                    more, seq = event_iterator.next_n(1)
                    for event in seq: ## seq should only ever have one element, but loop to be safe
                        #print(type(event))
                        #print(dir(event))
                        
                        nativeProbableCause = event.filterable_data[3].value.value()
                        probableCause = event.filterable_data[9].value.value()
                        neTime = event.filterable_data[6].value.value()
                        th_time = int(neTime[8:10])# + 7
                        neTime = neTime[0:4] + '-' + neTime[4:6] +'-' + neTime[6:8] + ' ' + str(th_time).zfill(2) +':'+ neTime[10:12]+':'+ neTime[12:14]
                        dt_neTime = datetime.datetime.strptime(neTime, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=7)
                        
                        neTime = dt_neTime.strftime('%Y-%m-%d %H:%M:%S')
                        neDate = dt_neTime.strftime('%Y-%m-%d')
                        neOnlyTime = dt_neTime.strftime('     "     %H:%M:%S')
                        
                        nativateEMSName = event.filterable_data[2].value.value()
                        alarmSerialNo = event.filterable_data[15].value.value()[3].value
                        locationInfo = event.filterable_data[15].value.value()[10].value
                        
                        additionalText = event.filterable_data[14].value.value()
                            
                        cause = 'Unknow'
                        if nativeProbableCause.find('R_LOS') >= 0:
                            #print('\t(%s/%s)' % (nativateEMSName, nativeProbableCause))
                            causes = nativeProbableCause.split('/')
                            if len(causes) > 0:
                                cause = causes[len(causes)-1]
                                #print(cause)
                            node_selected = False
                            if nativateEMSName.find('AMR-') >= 0:
                                node_selected = True
                            if nativateEMSName.find('BRM-') >= 0:
                                node_selected = True
                            if nativateEMSName.find('CPM-') >= 0:
                                node_selected = True
                            if nativateEMSName.find('NMA') >= 0:
                                node_selected = True
                            if nativateEMSName.find('NMNMAO1501(HUAWEI)-26-JD16-2') >= 0:
                                node_selected = True
                            if nativateEMSName.find('SRI-001') >= 0:
                                node_selected = True
                            if nativateEMSName.find('NKR') >= 0:
                                node_selected = True
                            if nativateEMSName.find('SRN-') >= 0:
                                node_selected = True
                            if nativateEMSName.find('SSK-') >= 0:
                                node_selected = True
                            if nativateEMSName.find('YST-') >= 0:
                                node_selected = True
                            if nativateEMSName.find('UBN-') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8039-MDH-009_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8038-NPM-002_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8037-NPM-018_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8036-SNK-001_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8035-SNK-006_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8034-SNK-010_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8033-UDN-006_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8032-UDN-004_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8031-KKN-026_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8029-KKN-045_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8045-MKM-007_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8044-MKM-008_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8043-KSN-021_H') >= 0:
                                node_selected = True
                            if nativateEMSName.find('8042-RET-007_H') >= 0:
                                node_selected = True
                            if node_selected:
                                nodename = nativateEMSName.split(';')[1]
                                key = '%s#%s#%s' % (neTime, cause, nodename)
                                rlos_query[key] = (neTime, cause, nodename)
                                
                                if neTime.find(today) >= 0:
                                    event_counter+=1
                                    if neDate != neOldDate:
                                        print(Style.BRIGHT + Fore.MAGENTA + '%d   \t%s \t%s \t%s' % (event_counter, neTime, cause.ljust(10), nodename))
                                        neOldDate = neDate
                                    else:
                                        print(Style.BRIGHT + Fore.MAGENTA + '%d   \t%s \t%s \t%s' % (event_counter, neOnlyTime, cause.ljust(10), nodename))
                                        
                                    if key not in self.rlos_dict.keys():
                                        self.rlos_new[key] = (neTime, cause, nodename)
                                        
                                else:                                    
                                    #import pdb; pdb.set_trace()
                                    if neTime.find(tomonth) >= 0:
                                        event_counter+=1
                                        if neDate != neOldDate:
                                            print(Style.BRIGHT + Fore.YELLOW + '%d   \t%s \t%s \t%s' % (event_counter, neTime, cause.ljust(10), nodename))
                                            neOldDate = neDate
                                        else:
                                            print(Style.BRIGHT + Fore.YELLOW + '%d   \t%s \t%s \t%s' % (event_counter, neOnlyTime, cause.ljust(10), nodename))
                                    elif neTime.find(toyear) >= 0:
                                        event_counter+=1
                                        if neDate != neOldDate:
                                            print(Style.BRIGHT + Fore.GREEN + '%d   \t%s \t%s \t%s' % (event_counter, neTime, cause.ljust(10), nodename))
                                            neOldDate = neDate
                                        else:
                                            print(Style.BRIGHT + Fore.GREEN + '%d   \t%s \t%s \t%s' % (event_counter, neOnlyTime, cause.ljust(10), nodename))
                                    else:
                                        break;
                                        event_counter+=1
                                        if neDate != neOldDate:
                                            print(Style.RESET_ALL + Fore.RESET + '%d   \t%s \t%s \t%s' % (event_counter, neTime, cause.ljust(10), nodename))
                                            neOldDate = neDate
                                        else:
                                            print(Style.RESET_ALL + Fore.RESET + '%d   \t%s \t%s \t%s' % (event_counter, neOnlyTime, cause.ljust(10), nodename))
                                                            #print('%d   \t%s \t%s' % (event_counter, neTime, nodename))
                    if not more: ## no more seq
                        break
                ### check for removed
                rlos_query_keys = rlos_query.keys()
                for k, value in self.rlos_dict.items():
                    if k not in rlos_query_keys:
                        self.rlos_removed[k] = value
                
                print(Style.BRIGHT + Fore.RED + "", self.rlos_new)
                print(Style.BRIGHT + Fore.YELLOW + "%d R_LOS" % len(self.rlos_dict))
                print(Style.BRIGHT + Fore.GREEN + "", self.rlos_removed)
                
                for k, value in self.rlos_removed.items():
                    rlos_msg ="CLEAR>> %s %s \n\t%s" % (value[2], value[1], value[0])
                    send_data="ccadc20b3a4365ee37f6c45150143c203=%s&" % rlos_msg
                    buffer = str(send_data).encode('utf-8')
                    send2LineBotServer("192.168.99.100", 54321, buffer)
                    del self.rlos_dict[k]
                        
                for k, value in self.rlos_new.items():
                    rlos_msg ="%s %s \n\t%s" % (value[2], value[1], value[0])
                    send_data="ccadc20b3a4365ee37f6c45150143c203=%s&" % rlos_msg
                    buffer = str(send_data).encode('utf-8')
                    send2LineBotServer("192.168.99.100", 54321, buffer)
                    self.rlos_dict[k] = value
                        
                self.session.endSession()    
                           
                sleep = abs(305 - abs(round(time.time()) - query_mtime))
                if sleep > 305:
                    sleep = 305
                print('-->[%s] Lastest Running Sleep %.2f mins      ' % ( time.strftime("%Y-%m-%d %H:%M:%S"),(int(sleep)/60.0)) )
                #print(self.q)
                time.sleep(sleep)
                #break
            except Exception as e:
                print('Error %s' % e)
                #break

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    q = Queue()
    rlos_query = RLOSMonitor()
    rlos_query.run()
    

