#!/usr/bin/env python
import math

MAX_TARGET = 2**11


# From: http://stackoverflow.com/a/22808285/1193738
def get_prime_factors(n):
    """Computes the prime factors of n."""
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def is_prime(n):
    """Returns true if n is a prime number."""
    if n < 2 or n % 2 == 0:
        return False
    for i in xrange(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def get_counter_factors(n):
    """Calculates the number of counters and the targets required to count to n."""
    if n < 1: 
        raise ValueError('target must be > 0')
    elif n <= MAX_TARGET:
        return [n]
    elif n > MAX_TARGET**2:
        raise NotImplementedError('target must be <= {}'.format(MAX_TARGET**2))

    prime_factors = get_prime_factors(n)

    # If n is prime or has a prime factor larger than the max target of a 
    # single counter, we can only implement it with 3 counters (TODO). 
    # 
    if is_prime(n) or max(prime_factors) > MAX_TARGET:
        raise NotImplementedError('target must be non-prime or have prime factors <= {}'.format(MAX_TARGET))

    # Otherwise, n is factorable into 2 factors, each of which is less than
    # the max target of a single counter.
    #
    else:
        counter_factors = []
        max_factor = prime_factors.pop()

        while len(prime_factors) > 0:
            factor = prime_factors.pop()
            if max_factor * factor > MAX_TARGET:
                counter_factors.append(max_factor)
                max_factor = factor
            else:
                max_factor *= factor
        counter_factors.append(max_factor)
        return counter_factors
        

if __name__ == '__main__':
    assert(get_counter_factors(1) == [1])
    assert(get_counter_factors(2047) == [2047])
    assert(get_counter_factors(2048) == [2048])
    assert(get_counter_factors(2049) == [683, 3])
    assert(get_counter_factors(10000) == [1250, 8])
    assert(get_counter_factors(1000000) == [625, 1600])


# vim: nu:et:ts=4:sw=4:fdm=indent
