import numpy as np
from funwavetvdtools.error import FunException

def iterator(x0, f, df, tolerence=10**-5, max_iterations=10):

    for i in range(max_iterations):

        cor = f(x0)/df(x0)
        x0 = x0 - cor
        err = np.abs(cor/x0)

        if err < tolerence: return x0

    # Raises exception if iterative scheme does not reach 
    # error tolerence within max iteration count
    brief = "Iterative scheme did not convergece"
    desc = "Newton-Raphson iterative scheme did not converenge."
    raise FunException(brief, desc)


  



            
 

