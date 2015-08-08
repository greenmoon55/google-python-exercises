def create_multipliers():
    return [lambda x: i * x for i in xrange(5)]

for multiplier in create_multipliers():
    print multiplier(2)


def create_multipliers_def():
    multipliers = []
    for i in xrange(5):
        def multiplier(x):
            return i * x
        multipliers.append(multiplier)
    print "You can still access i here, i = %d" % i
    return multipliers

for multiplier in create_multipliers_def():
    print multiplier(2)
