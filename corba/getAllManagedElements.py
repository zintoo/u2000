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
                          notifications.PS_MAJOR,
                          notifications.PS_MINOR,
                          notifications.PS_WARNING,
                          notifications.PS_CLEARED,
                         ] 
    
    exclude_perceivedSeverity_list = CORBA.Any(notifications._tc_PerceivedSeverityList_T, perceivedSeverity)
    #exclude_perceivedSeverity_list = [] 
    #print(exclude_perceivedSeverity_list)
    #print('.value=', exclude_perceivedSeverity_list.value)
    #print('.value()=', exclude_perceivedSeverity_list.value())
    #import pdb; pdb.set_trace()
    
    
    ## try to access ManagedElement
    try:
        mn_elm = session.getManager("ManagedElement")
        mn_elm_mgr = mn_elm._narrow(managedElementManager.ManagedElementMgr_I)
        
        #import pdb; pdb.set_trace()
        elms = mn_elm_mgr.getAllManagedElements(0)
        event_iterator = elms[1]
        more = True
        event_counter = 0
        while more:
            more, seq = event_iterator.next_n(1)
            for event in seq: ## seq should only ever have one element, but loop to be safe
                event_counter+=1
                print(event_counter, event.name[1].value, event.nativeEMSName )
                #print(event)
                #import pdb; pdb.set_trace()
                
        #elm_names = mn_elm_mgr.getAllManagedElementNames(100)
        
        meName = [ globaldefs.NameAndStringValue_T(name='EMS',value='Huawei/U2000'),
                   globaldefs.NameAndStringValue_T(name='ManagedElement',value='3147354') ]
        meName = CORBA.Any(globaldefs._tc_NamingAttributes_T, meName)
        
        event_counter = 0
        active_alarms = mn_elm_mgr.getAllActiveAlarms(meName.value(), exclude_probableCause_list, exclude_perceivedSeverity_list.value(), 0)
        print("Success session.getAllActiveAlarms()")
        
        event_iterator = active_alarms[1]
        
        more = True
        while more:
            more, seq = event_iterator.next_n(1)
            for event in seq: ## seq should only ever have one element, but loop to be safe
                #print(type(event))
                #print(dir(event))
                event_counter+=1
                #import pdb; pdb.set_trace()
                #print(event.filterable_data)
                neTime = event.filterable_data[6].value.value()
                time = int(neTime[8:10]) + 7
                neTime = neTime[0:4] + '-' + neTime[4:6] +'-' + neTime[6:8] + ' ' + str(time).zfill(2) +':'+ neTime[10:12]+':'+ neTime[12:14]
                nativateEMSName = event.filterable_data[2].value.value()
                alarmSerialNo = event.filterable_data[15].value.value()[3].value
                locationInfo = event.filterable_data[15].value.value()[10].value
                print('(%d).' % (event_counter))
                print('<%s> <%s> <%s>' % (neTime, alarmSerialNo, nativateEMSName))
                locationInfos = locationInfo.split('\\')
                for locationInfo in locationInfos:
                    if len(locationInfo.strip()) != 0:
                        print('                   <%s>' % (locationInfo))
                #print(event.filterable_data[2])
                #if event_counter >= 4:
                #    more = False
                    
            if not more: ## no more seq
                break;
                
        #import pdb; pdb.set_trace()        
        #event_iterator.destroy()
        
    except Exception as ex:
        print("FAILED session.getAllActiveAlarms() -> %s" % ex)
    finally:
        pass
    ems_manager = session.getManager("EquipmentInventory")
    
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
