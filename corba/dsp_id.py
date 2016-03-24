#!/usr/bin/env python

import sys
from omniORB import CORBA
import CosNaming
import emsSessionFactory
import nmsSession, nmsSession__POA
import emsMgr
import managedElementManager
import notifications, notifications__POA
import globaldefs
import sys
from colorama import init, AnsiToWin32, Fore, Back, Style
init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream

### class for new
class NmsSession_I(nmsSession__POA.NmsSession_I):
    pass
    
### for get Alarms
#class ProbableCauseList_T(notifications__POA.ProbableCauseList_T):
#    pass
### for get Alarms
#class PerceivedSeverityList_T(notifications__POA.PerceivedSeverityList_T):
#    pass
    
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

session = None
try: 
    session = ems_session.getEmsSession("NMAClient", "my123456", nms_session_o)
    ems = session.getManager("EMS")
    
    #probableCauses = ["one", "two", "three"]
    #exclude_probableCause_list = CORBA.Any(notifications._tc_ProbableCauseList_T, probableCauses)
    ### ok cast to Corba type
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
                          #notifications.PS_MAJOR,
                          #notifications.PS_MINOR,
                          notifications.PS_WARNING,
                          notifications.PS_CLEARED,
                         ] 
    
    exclude_perceivedSeverity_list = CORBA.Any(notifications._tc_PerceivedSeverityList_T, perceivedSeverity)
    #exclude_perceivedSeverity_list = [] 
    #print(exclude_perceivedSeverity_list)
    #print('.value=', exclude_perceivedSeverity_list.value)
    #print('.value()=', exclude_perceivedSeverity_list.value())
    #import pdb; pdb.set_trace()
    
    try:
        ems_obj = ems.getEMS()
        #print("Success ems.getEMS()")
    except Exception as ex:
        print("FAILED ems.getEMS() -> %s" % ex)
        
    try:
        event_counter = 0
        alarms_tuple = ems.getAllEMSAndMEActiveAlarms(exclude_probableCause_list, exclude_perceivedSeverity_list.value(), 1)
        #print("Success ems.getAllEMSAndMEActiveAlarms()")
        
        import datetime
        today = datetime.date.today()
        today = today.strftime('%Y-%m-%d')
        print('Check Alarm on U2000 via corba 100.9.2.3:12001/NameService @2015-07-15')
        print('----------------------------------------------------------------------')
        event_iterator = alarms_tuple[1]
        
        more = True
        neOldDate = ''
        while more:
            more, seq = event_iterator.next_n(1)
            for event in seq: ## seq should only ever have one element, but loop to be safe
                #print(type(event))
                #print(dir(event))
                
                #print(event.filterable_data)
                try:
                    print("%s/%s/%s" %(event.filterable_data[1].value.value()[1].name, event.filterable_data[1].value.value()[1].value, event.filterable_data[2].value.value()))
                except:
                    pass
                nativeProbableCause = event.filterable_data[3].value.value()
                probableCause = event.filterable_data[9].value.value()
                neTime = event.filterable_data[6].value.value()
                time = int(neTime[8:10])# + 7
                neTime = neTime[0:4] + '-' + neTime[4:6] +'-' + neTime[6:8] + ' ' + str(time).zfill(2) +':'+ neTime[10:12]+':'+ neTime[12:14]
                dt_neTime = datetime.datetime.strptime(neTime, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=7)
                
                neTime = dt_neTime.strftime('%Y-%m-%d %H:%M:%S')
                neDate = dt_neTime.strftime('%Y-%m-%d')
                neOnlyTime = dt_neTime.strftime('     "     %H:%M:%S')
                
                nativateEMSName = event.filterable_data[2].value.value()
                alarmSerialNo = event.filterable_data[15].value.value()[3].value
                locationInfo = event.filterable_data[15].value.value()[10].value
                
                additionalText = event.filterable_data[14].value.value()
                

                #print(event.filterable_data[2])
                #if event_counter >= 100:
                #    more = False
                #if nativateEMSName.find('CPM-') >= 0:
                #    print('\t(%s/%s)' % (nativateEMSName, nativeProbableCause))
                #if nativateEMSName.find('8039-MDH-009_H') >= 0:
                #    print('\t(%s/%s)' % (nativateEMSName, nativeProbableCause))
                cause = 'Unknow'
                if nativeProbableCause.find('R_LOS') >= 0 or nativeProbableCause.find('TEMP_') >= 0:
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
                        event_counter+=1
                        nodename = nativateEMSName.split(';')[1]
                        if neTime.find(today) >= 0:
                            if neDate != neOldDate:
                                print >> stream, Style.BRIGHT + Fore.MAGENTA + '%d   \t%s \t%s \t%s' % (event_counter, neTime, cause.ljust(10), nodename)
                                neOldDate = neDate
                            else:
                                print >> stream, Style.BRIGHT + Fore.MAGENTA + '%d   \t%s \t%s \t%s' % (event_counter, neOnlyTime, cause.ljust(10), nodename)
                            #print >> stream, Style.BRIGHT + Fore.RED + '%d   \t%s \t%s' % (event_counter, neTime, nodename)
                        else:
                            #import pdb; pdb.set_trace()
                            if neDate != neOldDate:
                                print >> stream, Style.RESET_ALL + Fore.RESET + '%d   \t%s \t%s \t%s' % (event_counter, neTime, cause.ljust(10), nodename)
                                neOldDate = neDate
                            else:
                                print >> stream, Style.RESET_ALL + Fore.RESET + '%d   \t%s \t%s \t%s' % (event_counter, neOnlyTime, cause.ljust(10), nodename)
                        #print('%d   \t%s \t%s' % (event_counter, neTime, nodename))
                        #print('\t(%s) %s' % (alarmSerialNo, nativateEMSName))
                        #print('%d   \t%s' % (event_counter, locationInfo))

                        #import pdb; pdb.set_trace()
                        #print('\t%s' % (additionalText))
                        #print('\t%s' % (probableCause))
                        #print('\t%s' % (nativeProbableCause))
                        #print('------------------------------------------------')
                    
                if not more: ## no more seq
                    break;
        #event_iterator.destroy()
        
    except Exception as ex:
        print("FAILED ems.getAllEMSAndMEActiveAlarms() -> %s" % ex)
    finally:
        print('----------------------------------------------------------------------')
        print("%d \tAlarms" % event_counter)    
        print('======================================================================')
        
    ### try to access ManagedElement
    # try:
        # mn_elm = session.getManager("ManagedElement")
        # mn_elm_mgr = mn_elm._narrow(managedElementManager.ManagedElementMgr_I)
        
        ##elms = mn_elm_mgr.getAllManagedElements(100)
        ##elms = mn_elm_mgr.getAllManagedElementNames(100)
        
        # meName = [ globaldefs.NameAndStringValue_T(name='EMS',value='Huawei/U2000'),
                   # globaldefs.NameAndStringValue_T(name='ManagedElement',value='3147354') ]
        # meName = CORBA.Any(globaldefs._tc_NamingAttributes_T, meName)
        
        # event_counter = 0
        # active_alarms = mn_elm_mgr.getAllActiveAlarms(meName.value(), exclude_probableCause_list, exclude_perceivedSeverity_list.value(), 0)
        # print("Success session.getAllActiveAlarms()")
        
        # event_iterator = active_alarms[1]
        
        # more = True
        # while more:
            # more, seq = event_iterator.next_n(1)
            # for event in seq: ## seq should only ever have one element, but loop to be safe
                ##print(type(event))
                ##print(dir(event))
                # event_counter+=1
                ##import pdb; pdb.set_trace()
                ##print(event.filterable_data)
                # neTime = event.filterable_data[6].value.value()
                # time = int(neTime[8:10]) + 7
                # neTime = neTime[0:4] + '-' + neTime[4:6] +'-' + neTime[6:8] + ' ' + str(time).zfill(2) +':'+ neTime[10:12]+':'+ neTime[12:14]
                # nativateEMSName = event.filterable_data[2].value.value()
                # alarmSerialNo = event.filterable_data[15].value.value()[3].value
                # locationInfo = event.filterable_data[15].value.value()[10].value
                # print('(%d).' % (event_counter))
                # print('<%s> <%s> <%s>' % (neTime, alarmSerialNo, nativateEMSName))
                # locationInfos = locationInfo.split('\\')
                # for locationInfo in locationInfos:
                    # if len(locationInfo.strip()) != 0:
                        # print('                   <%s>' % (locationInfo))
                ##print(event.filterable_data[2])
                ##if event_counter >= 4:
                ##    more = False
                    
            # if not more: ## no more seq
                # break;
                
        ##import pdb; pdb.set_trace()        
        ##event_iterator.destroy()
        
    # except Exception as ex:
        # print("FAILED session.getAllActiveAlarms() -> %s" % ex)
    # finally:
        # pass
    #ems_manager = session.getManager("EquipmentInventory")
    
except Exception as exp:
    print(exp)
finally:
    if session:
        session.endSession()
#orb.shutdown(0)
raw_input('Press <ENTER> to exit.')
### omniORB.CORBA.BAD_PARAM: CORBA.BAD_PARAM(omniORB.BAD_PARAM_WrongPythonType, CORBA.COMPLETED_NO)
### Exception AttributeError: "'NoneType' object has no attribute 'path'" in 
### <bound method TypeCode_alias.__del__ of CORBA.TypeCode("IDL:omg.org/PortableServer/ObjectId:1.0")> ignored

#import pdb; pdb.set_trace()
