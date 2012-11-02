import numpy as np
cimport numpy as np
cimport limiter as lim

DTYPE = np.float32
ctypedef np.float32_t DTYPE_t

cdef class Limiter:
    cdef lim.limiter_state state
    cdef np.ndarray delay_line
    def __init__(self, float attack_coeff, float release_coeff,
                 int delay_length):
        self.state = lim.init_limiter(attack_coeff, release_coeff, delay_length)
        self.delay_line = np.zeros(delay_length, dtype=DTYPE)

    def limit(self, np.ndarray[DTYPE_t,ndim=1] signal, float threshold):
        lim.limit(<float*>np.PyArray_DATA(signal),
                   <int>len(signal), threshold,
                   <float*>np.PyArray_DATA(self.delay_line),
                   <lim.limiter_state*>&self.state)
