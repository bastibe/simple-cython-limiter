#include <math.h>
#include "limiter.h"

#define MAX(x,y) ((x)>(y)?(x):(y))

limiter_state init_limiter(float attack_coeff, float release_coeff, int delay_len) {
    limiter_state state;
    state.attack_coeff = attack_coeff;
    state.release_coeff = release_coeff;
    state.delay_index = 0;
    state.envelope = 0;
    state.current_gain = 1;
    state.delay_length = delay_len;
    return state;
}

void limit(float *signal, int block_length, float threshold,
           float *delay_line, limiter_state *state) {
    for(int i=0; i<block_length; i++) {
        delay_line[state->delay_index] = signal[i];
        state->delay_index = (state->delay_index + 1) % state->delay_length;

        // calculate an envelope of the signal
        state->envelope *= state->release_coeff;
        state->envelope = MAX(fabs(signal[i]), state->envelope);

        // have current_gain go towards a desired limiter target_gain
        float target_gain;
        if (state->envelope > threshold)
            target_gain = (1+threshold-state->envelope);
        else
            target_gain = 1.0;
        state->current_gain = state->current_gain*state->attack_coeff +
            target_gain*(1-state->attack_coeff);

        // limit the delayed signal
        signal[i] = delay_line[state->delay_index] * state->current_gain;
    }
}
