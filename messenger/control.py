########################################################################
# COMPONENT:
#    CONTROL
# Author:
#    Br. Helfrich, Kyle Mueller, <Christian Speelman>
# Summary: 
#    This class stores the notion of Bell-LaPadula
########################################################################

# you may need to put something here...

from enum import Enum

class SecurityLevel(Enum):
    Public = 1
    Confidential = 2
    Privileged = 3
    Secret = 4 

#SecurityLevel = Enum('SecurityLevel', ['Public', 'Confidential', 'Privileged', 'Secret'])

def securityConditionRead(assetControl : SecurityLevel, subjectControl : SecurityLevel):
    return subjectControl.value >= assetControl.value

def securityConditionWrite(assetControl : SecurityLevel, subjectControl : SecurityLevel):
    return subjectControl.value <= assetControl.value
    
