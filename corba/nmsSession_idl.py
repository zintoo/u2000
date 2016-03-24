# Python stubs generated by omniidl from nmsSession.idl

import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA

_omnipy.checkVersion(3,0, __file__)

# #include "session.idl"
import session_idl
_0_session = omniORB.openModule("session")
_0_session__POA = omniORB.openModule("session__POA")
# #include "globaldefs.idl"
import globaldefs_idl
_0_globaldefs = omniORB.openModule("globaldefs")
_0_globaldefs__POA = omniORB.openModule("globaldefs__POA")

#
# Start of module "nmsSession"
#
__name__ = "nmsSession"
_0_nmsSession = omniORB.openModule("nmsSession", r"nmsSession.idl")
_0_nmsSession__POA = omniORB.openModule("nmsSession__POA", r"nmsSession.idl")


# interface NmsSession_I
_0_nmsSession._d_NmsSession_I = (omniORB.tcInternal.tv_objref, "IDL:mtnm.tmforum.org/nmsSession/NmsSession_I:1.0", "NmsSession_I")
omniORB.typeMapping["IDL:mtnm.tmforum.org/nmsSession/NmsSession_I:1.0"] = _0_nmsSession._d_NmsSession_I
_0_nmsSession.NmsSession_I = omniORB.newEmptyClass()
class NmsSession_I (_0_session.Session_I):
    _NP_RepositoryId = _0_nmsSession._d_NmsSession_I[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_nmsSession.NmsSession_I = NmsSession_I
_0_nmsSession._tc_NmsSession_I = omniORB.tcInternal.createTypeCode(_0_nmsSession._d_NmsSession_I)
omniORB.registerType(NmsSession_I._NP_RepositoryId, _0_nmsSession._d_NmsSession_I, _0_nmsSession._tc_NmsSession_I)

# NmsSession_I operations and attributes
NmsSession_I._d_eventLossOccurred = ((omniORB.typeMapping["IDL:mtnm.tmforum.org/globaldefs/Time_T:1.0"], (omniORB.tcInternal.tv_string,0)), (), None)
NmsSession_I._d_eventLossCleared = ((omniORB.typeMapping["IDL:mtnm.tmforum.org/globaldefs/Time_T:1.0"], ), (), None)

# NmsSession_I object reference
class _objref_NmsSession_I (_0_session._objref_Session_I):
    _NP_RepositoryId = NmsSession_I._NP_RepositoryId

    def __init__(self):
        _0_session._objref_Session_I.__init__(self)

    def eventLossOccurred(self, *args):
        return _omnipy.invoke(self, "eventLossOccurred", _0_nmsSession.NmsSession_I._d_eventLossOccurred, args)

    def eventLossCleared(self, *args):
        return _omnipy.invoke(self, "eventLossCleared", _0_nmsSession.NmsSession_I._d_eventLossCleared, args)

    __methods__ = ["eventLossOccurred", "eventLossCleared"] + _0_session._objref_Session_I.__methods__

omniORB.registerObjref(NmsSession_I._NP_RepositoryId, _objref_NmsSession_I)
_0_nmsSession._objref_NmsSession_I = _objref_NmsSession_I
del NmsSession_I, _objref_NmsSession_I

# NmsSession_I skeleton
__name__ = "nmsSession__POA"
class NmsSession_I (_0_session__POA.Session_I):
    _NP_RepositoryId = _0_nmsSession.NmsSession_I._NP_RepositoryId


    _omni_op_d = {"eventLossOccurred": _0_nmsSession.NmsSession_I._d_eventLossOccurred, "eventLossCleared": _0_nmsSession.NmsSession_I._d_eventLossCleared}
    _omni_op_d.update(_0_session__POA.Session_I._omni_op_d)

NmsSession_I._omni_skeleton = NmsSession_I
_0_nmsSession__POA.NmsSession_I = NmsSession_I
omniORB.registerSkeleton(NmsSession_I._NP_RepositoryId, NmsSession_I)
del NmsSession_I
__name__ = "nmsSession"

#
# End of module "nmsSession"
#
__name__ = "nmsSession_idl"

_exported_modules = ( "nmsSession", )

# The end.
