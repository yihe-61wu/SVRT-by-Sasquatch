from classifier import *
from dinnerParty import *

N = int(sys.argv[1]) # number of positive and negative training examples
S = int(sys.argv[2]) # number of samples

averages = []
errors = []

def task(t):
    return Bayesian_classifier(t,N,S)
    


T = 23

a = parallel_map(task, list(range(1,T+1)), cores = T)
a = [eval(x) for x in a ]
print a
