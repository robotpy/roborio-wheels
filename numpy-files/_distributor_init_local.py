import ctypes

lib = ctypes.CDLL("/usr/local/lib/libopenblas.so.0", ctypes.RTLD_GLOBAL)
