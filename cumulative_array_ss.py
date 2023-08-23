import itertools
from shamir_ss import generate, interpolate

def is_positive_integer(value):
    try:
        int_value = int(value)
        return int_value >= 0
    except ValueError:
        return False
    
def is_prime(number):#return true if the numebr is prime
    if number <= 1:
        return False
    elif number <= 3:
        return True
    elif number % 2 == 0 or number % 3 == 0:
        return False

    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6

    return True

#generate the max unauthorised subset, which is the all the possible combination of t-1 number of participants
def generate_max_unauthorised_subset(t, n):

    all_numbers = []
    for j in range(1, n + 1):
        all_numbers.append(j)

    MUS=[]
    
    for i in itertools.combinations(all_numbers, t-1):
        MUS.append(list(i))

    return MUS

def generate_cumulative_array(n, MUS):

    width = len(MUS)

    p = []#1 or 0, determine whether to assign shares, assign if p not in the set
    for i in range(1, n+1):
        P_i = []
        for j in range(width):
            if i not in MUS[j]: P_i.append(1)
            else: P_i.append(0)

        p.append(P_i)

    return p


def setup(s, t, n, p):
    mus = generate_max_unauthorised_subset(t, n)
    ca = generate_cumulative_array(n, mus)
    m = len(mus)
    shares = generate(s, m, m, p) #generate m(size of the MUS) numbers of shares using shamir secret sharing scheme(m, m)

    #assign shares to each participant
    keys = []
    for p in ca: 
        b = []
        for i in range(len(p)):
            if p[i] == 1:
                b.append(shares[i])

        keys.append(b)

    return keys

'''
recontruction
'''

def reconstruct(shares, p):
    combine = []
    for share in shares:
        for s in share:
            if not s in combine:
                combine.append(s)

    x_values = []
    y_values = []
    for values in combine:
        x_values.append(values[0])
        y_values.append(values[1])

    secret = interpolate(x_values, y_values, p)

    return secret

