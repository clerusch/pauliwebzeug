from stim import Circuit, target_rec
import numpy as np
import matplotlib.pyplot as plt

shots = 100_000
pers = np.linspace(0,0.3,1000)
lers = []

for per in pers:
    l_errors = 0
    circ = Circuit()

    circ.append("M", [0])
    circ.append("X_error", [0], per)
    circ.append("M", [0])
    circ.append("DETECTOR", [target_rec(-2), target_rec(-1)])

    

    sampler = circ.compile_detector_sampler()
    result = sampler.sample(shots=shots)

    for row in result:
        if row[-1]:
            l_errors +=1
    lers.append(l_errors/shots)

plt.plot(pers, lers)
plt.savefig("img/test_stim.png")