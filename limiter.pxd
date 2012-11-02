cdef extern from "limiter.h":
    ctypedef struct limiter_state:
        int delay_index
        int delay_length
        float envelope
        float current_gain
        float attack_coeff
        float release_coeff

    limiter_state init_limiter(float attack_factor, float release_factor, int delay_len)
    void limit(float *signal, int block_length, float threshold,
               float *delay_line, limiter_state *state)
