#!/usr/bin/env python
import math

MAX_TARGET = 2**11

"""
An AP counter (gen1 E6LA device) can support a target value of at most 2^11.
If a user wants to count higher than this, they need to connect two counters
in series with each other with a buffer STE inserted between the output of the 
first counter and the count-input of the second counter. 

With two counters, the user should be able to reach counter target values
between 2^11 and 2^22. But not all numbers are reachable. With two counters
connected in series, the full target value is the product of the specific
target values in each of the individual counters. 

For example, to count up to 10,000 one counter could contain a value of 250
and the other counter could contain a value of 40; 250 * 40 = 10,000

Restated - The full target value is the product of two lesser counter target 
values (each one being at most 2^11 or 2048). 

Given the constraints described above, the goal of this program is, for a 
given integer (the TARGET value):
    * Find two numbers, each less than 2049, the product of which is equal to
    the TARGET value.
    * If the TARGET value cannot be reached: find two numbers that, when
    multiplied together, come as close as possible to the TARGET value. 

Examples:
    input_1  = 10,000
    output_1 = [250, 40] an exact answer

    input_2  = 338323
    output_2 = EITHER  [998, 339]  product = 338322 off by -1
                 OR    [1124, 301] product = 338324 off by +1

"""

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

def group_factors(factors):
    """Group the factor list into 2 groups where the product of each group is less than 2048"""
    factors.sort()
    while len(factors) > 2:
        if factors[-1] * factors[0] <= 2048:
            m1 = factors.pop(0)
            m2 = factors.pop()
            factors.append(m1*m2)
        else: 
            m1 = factors.pop(0)
            m2 = factors.pop(0)
            factors.append(m1*m2)
            factors.sort()
    if max(factors) > 2048:
        return None
    factors.sort()
    return factors
    
def get_counter_factors(target):
    """Calculates the number of counters and the targets required to count to target."""
    if target < 1: 
        raise ValueError('target must be > 0')
    elif target <= MAX_TARGET:
        return [target]
    elif target > MAX_TARGET**2:
        raise NotImplementedError('target must be <= {}'.format(MAX_TARGET**2))

    for delta in range(3000): # go +/- up to 3000 integers away from target
        # find solutions at (when delta=0) or just below (when delta>0) the target 
        prime_factors = get_prime_factors(target - delta)
        if max(prime_factors) <= MAX_TARGET:
            # might work - try grouping them together.
            factors = group_factors(prime_factors)
            if factors is not None:
                return factors

        if delta > 0: # don't waste time on delta=0 again.
            # find solutions just above the target 
            prime_factors = get_prime_factors(target + delta)
            if max(prime_factors) > MAX_TARGET:
                # can't do it. Move on to the next delta
                continue
            factors = group_factors(prime_factors)
            if factors is not None:
                return factors
    return None


   # # If target is prime or has a prime factor larger than the max target of a 
   # # single counter, we can only implement it with 3 counters (TODO). 
   # # 
   # if is_prime(target) or max(prime_factors) > MAX_TARGET:
   #     raise NotImplementedError('target must be non-prime or have prime factors <= {}'.format(MAX_TARGET))

   # # Otherwise, target is factorable into 2 factors, each of which is less than
   # # the max target of a single counter.
   # #
   # else:
   #     counter_factors = []
   #     max_factor = prime_factors.pop()

   #     while len(prime_factors) > 0:
   #         factor = prime_factors.pop()
   #         if max_factor * factor > MAX_TARGET:
   #             counter_factors.append(max_factor)
   #             max_factor = factor
   #         else:
   #             max_factor *= factor
   #     counter_factors.append(max_factor)
   #     return counter_factors
        

if __name__ == '__main__':
    assert(get_counter_factors(1) == [1])
    assert(get_counter_factors(2047) == [2047])
    assert(get_counter_factors(2048) == [2048])
    assert(get_counter_factors(2049) == [3, 683])
    assert(get_counter_factors(10000) == [5, 2000])
    assert(get_counter_factors(1000000) == [625, 1600])

    """
    This exhaustive test takes about 35 minutes to run on my home computer.
    Might run faster on a beefier machine. Mine: Intel(R) Core(TM) i5-3450 CPU @ 3.10GHz 

    Near the end we get a whole lot of "coundn't figure out" messages. The
    distance between multiples gets relatively high. 
        2048*2048 = 4194304
        2048*2047 = 4192256 delta 2k
        2047*2047 = 4190209 delta 2k
        2048*2046 = 4190208
        2047*2046 = 4188162 delta 2k
        2048*2045 = 4188160
        2046*2046 = 4186116 delta 2k
        2047*2045 = 4186115
        2046*2045 = 4184070 delta 2k
        2045*2045 = 4182025
    """
    for x in range((2**11)+1, (2**22)):
        factors = get_counter_factors(x)
        if factors is None:
            print "couldn't figure out %d" % x
            continue
        product = factors[0] * factors[1]
        print "target %7d f1 %4d f2 %4d product %7d off %d" % (x, factors[0], factors[1], product, x-product)



# vim: nu:et:ts=4:sw=4:fdm=indent
