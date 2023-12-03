from random import random

def generate_discrete_var(vars, probs):
    if sum(probs) != 1:
        raise Exception("This is not a probability distribution.")
    
    prob_func = sorted(zip(vars, probs), key=lambda x: x[1], reverse=True)
    u = random()
    acc = 0
    gen_var = None
    for var, prob in prob_func:
        acc += prob
        if u <= acc:
            gen_var = var
            break
    
    return gen_var

