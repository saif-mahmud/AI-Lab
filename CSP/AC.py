import queue


class CSP:
    def __init__(self, X: list, D: dict, C: dict):
        self.X = X
        self.D = D
        self.C = C
        self.arcs = list(C.keys())

    def AC1(self):
        while True:
            for (Xi, Xj) in self.arcs:
                domain_change = self.revise(Xi, Xj) | self.revise(Xj, Xi)
                
            if not domain_change:
                break

    def AC3(self):
        q = queue.Queue()

        for arc in self.arcs:
            q.put(arc)

        while not q.empty():
            (Xi, Xj) = q.get()

            if self.revise(Xi, Xj):
                if len(self.D[Xi]) == 0:
                    return False

                neighbors = [i for i in self.arcs if (i[0] == Xi and i[1] != Xj)]
                for (_Xi, Xk) in neighbors:
                    q.put((Xk, _Xi))

        return True

    def revise(self, Xi, Xj):
        revised = False

        for x in self.D[Xi]:
            if not self.satisfy_constraint(x, Xi, Xj):
                self.D[Xi].remove(x)
                revised = True
        return revised

    def satisfy_constraint(self, x, Xi, Xj):
        for y in self.D[Xj]:
            if eval(self.C[(Xi, Xj)]):
                return True
        return False

    def result(self):
        print(self.D)


X = ['A', 'B', 'C', 'D', 'E']
D = {'A': [1, 2, 3, 4, 5], 'B': [1, 2, 3, 4, 5], 'C': [1, 2, 3, 4, 5], 'D': [1, 2, 3, 4, 5], 'E': [1, 2, 3, 4, 5]}
C = {('A', 'B'): 'x > y', ('A', 'C'): 'x > y', ('A', 'D'): 'x >= y', ('A', 'E'): 'x > y', ('B', 'C'): 'x != y',
     ('B', 'E'): 'x > y', ('C', 'D'): 'x >= y', ('D', 'E'): 'x < y',
     ('B', 'A'): 'x < y', ('C', 'A'): 'x < y', ('D', 'A'): 'x <= y', ('E', 'A'): 'x < y', ('C', 'B'): 'x != y',
     ('E', 'B'): 'x < y', ('D', 'C'): 'x <= y', ('E', 'D'): 'x > y'}

csp = CSP(X, D, C)
csp.AC1()
csp.result()

csp = CSP(X, D, C)
csp.AC3()
csp.result()