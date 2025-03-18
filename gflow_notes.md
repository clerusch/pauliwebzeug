# Pauli web computer
- gives answers even when there are none (maybe use is_valid feature in the future?)

# Fixing gflow
- Their gflow (and algo) does not care about *which* zx vertextype we have and which edgetype
- Therefore, trivially both CNOT and ZZ measurements have gflow (since they are the same to gflow() function)
- It's really an OCM thing
- Note: Figure 1 from 2007 paper shows partial ordering with distinct nodes on same level, in line with gflow() dictionary output.
- Idea! this could be explained by the pauli=True call in compute_pauli_webs! It actually does care about red spiders, just not about hadamard edges?