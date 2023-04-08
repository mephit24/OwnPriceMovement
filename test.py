import numpy as np
from random import randint

var1 = [randint(1, 100) for x in range(100)]

positive_cc = [i + 1 for i in var1]
negative_cc = [i - (2*i) for i in var1]
no_cc = [randint(1, 100) for i in range(100)]

print(positive_cc)
print(negative_cc)
print(no_cc)

print(np.corrcoef(var1, positive_cc)[0,1])
print(np.corrcoef(var1, negative_cc)[0,1])
print(np.corrcoef(var1, no_cc)[0,1])
