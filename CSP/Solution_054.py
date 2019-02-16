import random
import time

#fro---m utils_054 import count, argmin_random_tie

identity = lambda x: x

argmin = min
argmax = max


def argmin_random_tie(seq, key=identity):
    return argmin(shuffled(seq), key=key)


def argmax_random_tie(seq, key=identity):
    return argmax(shuffled(seq), key=key)


def shuffled(iterable):
    items = list(iterable)
    random.shuffle(items)
    return items


class CSP:

    def __init__(self, variables, domains, neighbors, constraints):
        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        return count(conflict(v) for v in self.neighbors[var])

    def conflicted_vars(self, current):
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]


def min_conflicts(csp, max_steps=1000000):
    csp.current = current = {}

    steps = 0

    for var in csp.variables:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)

    for i in range(max_steps):

        if i == 0:
            print('Initial Assignment :')
            display(current)
        steps += 1

        print('Intermediate Step :')
        display(current)

        conflicted = csp.conflicted_vars(current)

        if not conflicted:
            print('# of Intermediate Steps :', steps)
            return current

        var = random.choice(conflicted)
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)

    print('# of Intermediate Steps :', steps)
    return None


def min_conflicts_value(csp, var, current):
    return argmin_random_tie(csp.domains[var],
                             key=lambda val: csp.nconflicts(var, val, current))


def queen_constraint(A, a, B, b):
    return A == B or (a != b and A + a != B + b and A - a != B - b)


class NQueensCSP(CSP):

    def __init__(self, n):
        CSP.__init__(self, list(range(n)), UniversalDict(list(range(n))),
                     UniversalDict(list(range(n))), queen_constraint)

        self.rows = [0]*n
        self.ups = [0]*(2*n - 1)
        self.downs = [0]*(2*n - 1)

    def nconflicts(self, var, val, assignment):
        n = len(self.variables)
        c = self.rows[val] + self.downs[var+val] + self.ups[var-val+n-1]
        if assignment.get(var, None) == val:
            c -= 3
        return c

    def assign(self, var, val, assignment):
        oldval = assignment.get(var, None)
        if val != oldval:
            if oldval is not None:
                self.record_conflict(assignment, var, oldval, -1)
            self.record_conflict(assignment, var, val, +1)
            CSP.assign(self, var, val, assignment)

    def unassign(self, var, assignment):
        if var in assignment:
            self.record_conflict(assignment, var, assignment[var], -1)
        CSP.unassign(self, var, assignment)

    def record_conflict(self, assignment, var, val, delta):
        n = len(self.variables)
        self.rows[val] += delta
        self.downs[var + val] += delta
        self.ups[var - val + n - 1] += delta


class UniversalDict:
    def __init__(self, value): self.value = value

    def __getitem__(self, key): return self.value

    def __repr__(self): return '{{Any: {0!r}}}'.format(self.value)


n = 8


def display(assignment):
    global n

    for val in range(n):
        for var in range(n):
            if assignment.get(var, '') == val:
                ch = 'Q'
            elif (var + val) % 2 == 0:
                ch = '.'
            else:
                ch = '-'
            print(ch, end=' ')
        print('    ', end=' ')
        print()

    print('\n\n')


start = time.time()

print('\nN = ', n)

solution = min_conflicts(NQueensCSP(n))
print('Final Solution :')
display(solution)

elapsed_time = time.time() - start
print('Elapsed Time :', elapsed_time)
