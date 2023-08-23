import random
'''
SHARES GENERATION
'''
def generate(s, t, n, p):#p must be a prime number larger than n and k must be an integer from 0 to p-1
    polynomial = [s]
    for i in range(t-1):
        coefficent = random.randint(1, p-1)
        polynomial.append(coefficent)

    shares = generate_shares(polynomial, n, p)
    return shares


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

def evaluate(coefficients, x):
    acc = 0
    power = 1
    for c in coefficients:
        acc += c * power
        power *= x
    return acc

def generate_shares(polynomial, n, p):#this function generate shares that is distributed individually to all participants

    shares = [] 

    x = []
    for i in range(n):
        new_x = random.randint(1, p-1)
        while new_x in x:  # x must be distinct
            new_x = random.randint(1, p-1)
        x.append(new_x)
    for value in x:
        y = evaluate(polynomial, value) #sub in the x value to get y coordinate
        shares.append([value, y % p])

    return shares

'''
reconstruction
'''

def interpolate(x_values, y_values, p):

    n = len(x_values)
    secret = 0

    for i in range(n):
        num = 1
        den = 1
        xi = x_values[i]

        for j in range(n):
            if i != j:
                num = (num * (0 - x_values[j])) % p
                den = (den * (xi - x_values[j])) % p

        li = (num * pow(den, -1, p)) % p #pow(den, -1, p) calculates the modular inverse of den with respect to p.
        secret = (secret + (y_values[i] * li) % p) % p

    return secret




