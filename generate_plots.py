from numpy import *
from matplotlib.pyplot import *

random.seed(0)
noise = random.randn(5000)
noise /= max(noise)
envelope = zeros(5000)
gain = ones(5000)

threshold = 0.85

for i in arange(len(noise)):
    envelope[i] = max(abs(envelope[i-1]) * 0.9998, abs(noise[i]))
    if envelope[i] > threshold:
        target_gain = 1.0 + threshold - envelope[i]
    else:
        target_gain = 1.0
    gain[i] = gain[i-1]*0.8 + target_gain*(1-0.8)

figure(figsize=(5,2.5))
plot(abs(noise), color='lightgrey', label='|noise|')
plot(envelope, color='black', linewidth=2, label='envelope')
xlabel('time/samples')
xticks(())
ylabel('gain/linear')
yticks(())
legend(loc='lower right')
tight_layout()
savefig('envelope.png')

plot((0, len(noise)),(threshold,threshold), color='grey', linewidth=2)
plot(gain-(1-threshold), color='red', linewidth=2, label='gain')
legend(loc='lower right')
savefig('gain.png')

xlim(3000,3200)
ylim(0.6,1.1)
legend().set_visible(False)
savefig('detail.png')
