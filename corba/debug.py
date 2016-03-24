import sys
from omniORB import CORBA
import CosNaming
import emsSessionFactory
import nmsSession, nmsSession__POA
import emsMgr
import managedElementManager
import notifications, notifications__POA
import globaldefs




meName = [globaldefs.NameAndStringValue_T(name='EMS',value='ZTE/1')]
#meName = CORBA.Any(globaldefs._tc_NameAndStringValue_T, meName)
meName = CORBA.Any(globaldefs._tc_NamingAttributes_T, meName)
import pdb; pdb.set_trace()

probableCauses = ["one", "two", "three"]
exclude_probableCause_list = CORBA.Any(notifications._tc_ProbableCauseList_T, probableCauses)
### ok cast to Corba type
print(exclude_probableCause_list)
     
##  PS_INDETERMINATE, 0
##  PS_CRITICAL, 1
##  PS_MAJOR, 2
##  PS_MINOR, 3
##  PS_WARNING, 4
##  PS_CLEARED 5
perceivedSeverity = [0, 1, 2, 3, 4, 5] 
exclude_perceivedSeverity_list = CORBA.Any(notifications._tc_PerceivedSeverity_T, perceivedSeverity)
print(exclude_perceivedSeverity_list)


### test iterator
#event_iterator = alarms_tuple[1]
#event_counter = 0
#more = True
#while more:
#    more, seq = event_iterator.next_n(1)
#    for event in seq: ## seq should only ever have one element, but loop to be safe
#        #print(type(event))
#        #print(dir(event))
#        event_counter+=1
        # #import pdb; pdb.set_trace()
        # #print(event.filterable_data)
        # emsTime = event.filterable_data[5].value.value()
        # emsTime = emsTime[0:4] + '-' + emsTime[4:6] +'-' + emsTime[6:8] + ' ' + emsTime[8:10] +':'+ emsTime[10:12]
        # nativateEMSName = event.filterable_data[2].value.value()
        # alarmSerialNo = event.filterable_data[15].value.value()[2].value
        # locationInfo = event.filterable_data[15].value.value()[9].value
        # print('%s %s %s' % (emsTime, alarmSerialNo, nativateEMSName))
        # print('%d   \t%s' % (event_counter, locationInfo))
        # #print(event.filterable_data[2])
        # if event_counter >= 1:
            # more = False