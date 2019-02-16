import random
from itertools import count

from utils import first, argmin_random_tie


class CSP:

    def __init__(self, X : list, D : dict, C : dict, neighbors : dict):
        self.X = X
        self.D = D
        self.C = C
        self.neighbors = neighbors

        self.current_domains = None
        self.nassigns = 0

    def assign(self, var, value, assignment):
        assignment[var] = value
        self.nassigns += 1

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, value, assignment):

        def conflict(var2):
            x = value
            y = assignment[var2]
            return (var2 in assignment and
                    not eval(self.C[(var, var2)]))
        return count(conflict(v) for v in self.neighbors[var])

    def actions(self, state):
        if len(state) == len(self.X):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.X
                               if v not in assignment])
            return [(var, value) for value in self.D[var]
                    if self.nconflicts(var, value, assignment) == 0]

    def result(self, state, action):
        (var, value) = action
        return state + ((value, value),)

    def goal_test(self, state):
        assignment = dict(state)
        return (len(assignment) == len(self.X)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.X))

    def support_pruning(self):
        if self.current_domains is None:
            self.current_domains = {v: list(self.D[v])
                                    for v in self.X}

    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.current_domains[var] if a!= value]
        self.current_domains[var] = [value]
        return removals
    
    def prune(self, var, value, removals):
        self.current_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        return (self.current_domains or self.D)[var]

    def infer_assignments(self):
        self.support_pruning()
        return {v: self.current_domains[v][0]
                for v in self.X if len(self.current_domains[v]) == 1}

    def restore(self, removals):
        for B, b in removals:
            self.current_domains[B].append(b)

    def conflicted_vars(self, current):
        return [var for var in self.X
                if self.nconflicts(var, current[var], current) > 0]

    def first_unassigned_vaiable(self, assignment):
        return first([var for var in self.X
                           if var not in assignment])

    def mrv(self, assignment):
        return argmin_random_tie([v for v in self.X
                                  if v not in assignment],
                                 key = lambda var:
                                 self.num_legal_values(var, assignment))

    def num_legal_values(self, var, assignment):
        if self.current_domains:
            return len(self.current_domains[var])
        else:
            return count(self.nconflicts(var, val, assignment) == 0
                         for val in self.D[var])

    def unordered_domain_values(self, var):
        return self.choices(var)

    def lcv(self, var, assignment):
        return sorted(self.choices(var),
                      key = lambda val: self.nconflicts(var, val, assignment))

    def no_inference(self):
        return True

    def forward_checking(self, var, value, assignment, removals):
        self.support_pruning()

        for B in self.neighbors[var]:
            if B not in assignment:
                for b in self.current_domains[B][:]:
                    if not self.constraints(var, value, B, b):
                        self.prune(B, b, removals)
                if not self.curr_domains[B]:
                    return False
        return True

    def backtracking_serach(self,
                            select_unassigned_variable=first_unassigned_vaiable,
                            order_domain_values=unordered_domain_values,
                            inference=no_inference
                            ):
        def backtrack(assignment):
            if len(assignment) == len(self.X):
                return assignment

            var = select_unassigned_variable(assignment)

            for value in order_domain_values(var, assignment):
                if self.nconflicts(var, value, assignment) == 0:
                    self.assign(var, value, assignment)
                    removals = self.suppose(var, value)

                    if inference(var, value, assignment, removals):
                        result = backtrack(assignment)

                        if result is not None:
                            return result

                        self.restore(removals)

            self.unassign(var, assignment)
            return None

        result = backtrack({})
        return result

    def min_conflicts(self, max_steps = 1000):
        current = {}

        for var in self.X:
            val = self.min_conflicts_value(var, current)
            self.assign(var, val, current)

        for i in range(max_steps):
            conflicted = self.conflicted_vars(current)

            if not conflicted:
                return current

            var = random.choice(conflicted)
            val = self.min_conflict_values(var, current)
            self.assign(var, val, current)
        return None

    def min_conflict_value(self, var, current):
        return argmin_random_tie(self.D[var],
                                 key = lambda val:
                                 self.nconflicts(var, val, current))

    def result(self, assignment):
        print(assignment)

