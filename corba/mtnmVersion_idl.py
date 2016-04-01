# Python stubs generated by omniidl from mtnmVersion.idl

import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA

_omnipy.checkVersion(3,0, __file__)


#
# Start of module "mtnmVersion"
#
__name__ = "mtnmVersion"
_0_mtnmVersion = omniORB.openModule("mtnmVersion", r"mtnmVersion.idl")
_0_mtnmVersion__POA = omniORB.openModule("mtnmVersion__POA", r"mtnmVersion.idl")


# interface Version_I
_0_mtnmVersion._d_Version_I = (omniORB.tcInternal.tv_objref, "IDL:mtnm.tmforum.org/mtnmVersion/Version_I:1.0", "Version_I")
omniORB.typeMapping["IDL:mtnm.tmforum.org/mtnmVersion/Version_I:1.0"] = _0_mtnmVersion._d_Version_I
_0_mtnmVersion.Version_I = omniORB.newEmptyClass()
class Version_I :
    _NP_RepositoryId = _0_mtnmVersion._d_Version_I[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_mtnmVersion.Version_I = Version_I
_0_mtnmVersion._tc_Version_I = omniORB.tcInternal.createTypeCode(_0_mtnmVersion._d_Version_I)
omniORB.registerType(Version_I._NP_RepositoryId, _0_mtnmVersion._d_Version_I, _0_mtnmVersion._tc_Version_I)

# Version_I operations and attributes
Version_I._d_getVersion = ((), ((omniORB.tcInternal.tv_string,0), ), None)

# Version_I object reference
class _objref_Version_I (CORBA.Object):
    _NP_RepositoryId = Version_I._NP_RepositoryId

    def __init__(self):
        CORBA.Object.__init__(self)

    def getVersion(self, *args):
        return _omnipy.invoke(self, "getVersion", _0_mtnmVersion.Version_I._d_getVersion, args)

    __methods__ = ["getVersion"] + CORBA.Object.__methods__

omniORB.registerObjref(Version_I._NP_RepositoryId, _objref_Version_I)
_0_mtnmVersion._objref_Version_I = _objref_Version_I
del Version_I, _objref_Version_I

# Version_I skeleton
__name__ = "mtnmVersion__POA"
class Version_I (PortableServer.Servant):
    _NP_RepositoryId = _0_mtnmVersion.Version_I._NP_RepositoryId


    _omni_op_d = {"getVersion": _0_mtnmVersion.Version_I._d_getVersion}

Version_I._omni_skeleton = Version_I
_0_mtnmVersion__POA.Version_I = Version_I
omniORB.registerSkeleton(Version_I._NP_RepositoryId, Version_I)
del Version_I
__name__ = "mtnmVersion"

#
# End of module "mtnmVersion"
#
__name__ = "mtnmVersion_idl"

_exported_modules = ( "mtnmVersion", )

# The end.