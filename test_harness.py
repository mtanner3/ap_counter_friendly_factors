
import counter_factors as cf

FH = open ("primes_from_2053_to_4194301.txt")
for line in FH.readlines():
    target = int(line)
    factors = cf.get_counter_factors(target)
    if factors is None:
        print "No solution found for %d" % target
        continue
    product = factors[0] * factors[1]
    print "target %7d f1 %4d f2 %4d product %7d off %d" % (target, factors[0], factors[1], product, target - product)


