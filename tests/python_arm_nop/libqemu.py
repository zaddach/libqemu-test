import ctypes
from llvmlite.binding.ffi import LLVMModuleRef, LLVMValueRef
from llvmlite.binding.module import ModuleRef
from llvmlite.binding.value import ValueRef

#class _ArmCodeFlags(ctypes.Structure):
#    _fields_ = [
#        ("thumb",       ctypes.c_uint64, 1),
#        ("veclen",      ctypes.c_uint64, 3),
#        ("vecstride",   ctypes.c_uint64, 3),
#        ("vfpen",       ctypes.c_uint64, 1),
#        ("condexec",    ctypes.c_uint64, 8),
#        ("bswap_code",  ctypes.c_uint64, 1),
#        ("xscale_cpar", ctypes.c_uint64, 2),
#        ("ns",          ctypes.c_uint64, 1)]
#
#class _X86CodeFlags(ctypes.Structure):
#    _fields_ = [
#        ("cpl", ctypes.c_uint64, 2),
#        ("softmmu", ctypes.c_uint64, 1),
#        ("inhibit_irq", ctypes.c_uint64, 1),
#        ("cs32", ctypes.c_uint64, 1),
#        ("ss32", ctypes.c_uint64, 1),
#        ("addseg", ctypes.c_uint64, 1),
#        ("pe", ctypes.c_uint64, 1),
#        ("tf", ctypes.c_uint64, 1),
#        ("mp", ctypes.c_uint64, 1),
#        ("em", ctypes.c_uint64, 1),
#        ("ts", ctypes.c_uint64, 1),
#        ("iopl", ctypes.c_uint64, 2),
#        ("lma", ctypes.c_uint64, 1),
#        ("cs64", ctypes.c_uint64, 1),
#        ("rf", ctypes.c_uint64, 1),
#        ("vm", ctypes.c_uint64, 1),
#        ("ac", ctypes.c_uint64, 1),
#        ("smm", ctypes.c_uint64, 1),
#        ("svme", ctypes.c_uint64, 1),
#        ("svmi", ctypes.c_uint64, 1),
#        ("osfxsr", ctypes.c_uint64, 1),
#        ("smap", ctypes.c_uint64, 1),
#        ("iobpt", ctypes.c_uint64, 1)]
#    
#
#class CodeFlags(ctypes.Union):
#    _fields_ = [
#        ("arm", _ArmCodeFlags),
#        ("x86", _X86CodeFlags),
#        ("_value", ctypes.c_uint64)]

class ArmCodeFlags():
    thumb = False

    def __init__(self, *args, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    @property
    def _value(self):
        return int(self.thumb) << 0

_libqemu_load_func = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint, ctypes.c_bool, ctypes.c_bool)
_libqemu_store_func = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint64, ctypes.c_uint, ctypes.c_bool, ctypes.c_bool, ctypes.c_uint64)

class LibqemuModuleRef(ModuleRef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Destructor needs to be overridden,
    # Module is destructed by libqemu
    def _dispose(self):
        pass

class LibqemuError(RuntimeError):
    def __init__(self, errorcode):
        self.code = errorcode

class Libqemu():
    def __init__(self, load_callback, library):
        self._handle = ctypes.CDLL(library)
        self._handle.libqemu_init.argtypes = [_libqemu_load_func, _libqemu_store_func]
        self._handle.libqemu_init.restype = ctypes.c_int 
        self._handle.libqemu_get_module.argtypes = []
        self._handle.libqemu_get_module.restype = LLVMModuleRef
        self._handle.libqemu_gen_intermediate_code.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_bool, ctypes.POINTER(LLVMValueRef)]
        self._handle.libqemu_gen_intermediate_code.restype = ctypes.c_int 
        self._handle.libqemu_raise_error.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self._handle.libqemu_raise_error.restype = None
        self._handle.libqemu_get_target_name.argtypes = []
        self._handle.libqemu_get_target_name.restype = ctypes.c_char_p
        self._load_callback = _libqemu_load_func(lambda env, addr, size, signed, code: load_callback(self, env, addr, size, signed, code))
        error = self._handle.libqemu_init(self._load_callback, _libqemu_store_func())
        if error != 0:
            raise LibqemuError(error)
        self.module = LibqemuModuleRef(self._handle.libqemu_get_module())

    def gen_intermediate_code(self, pc, code_flags, single_inst = True):
        llvm_func = LLVMValueRef()
        error = self._handle.libqemu_gen_intermediate_code(pc, code_flags._value, single_inst, ctypes.byref(llvm_func))
        if error != 0:
            raise LibqemuError(error)
        return ValueRef(llvm_func, module = self.module)

    def raise_error(self, env, error_code):
        self._handle.libqemu_raise_error(env, error_code)

    @property
    def target_name(self):
        return self._handle.libqemu_get_target_name().decode(encoding = "ISO-8859-1")
