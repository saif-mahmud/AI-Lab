import queue


class CSP:
    def __init__(self, X: list, D: dict, C: dict):
        self.X = X
        self.D = D
        self.C = C
        self.arcs = list(C.keys())

    def AC1(self):
        while True:
            domain_change = False

            for (Xi, Xj) in self.arcs:
                domain_change = self.revise(Xi, Xj) or self.revise(Xj, Xi)

            if not domain_change:
                break

    def AC2(self):
        q1 = queue.Queue()
        q2 = queue.Queue()

        for k in self.X:

            for e in self.X:
                if e < k and (e, k) in self.arcs:
                    q1.put((k, e))
                    q2.put((e, k))

            while not q1.empty():
                while not q1.empty():
                    (A, B) = q1.get()

                    if self.revise(A, B):
                        neighbors = [i for i in self.arcs if (i[0] == A and i[1] != B)]

                        for (_A, C) in neighbors:
                            q2.put((C, _A))

                q1 = q2
                q2 = queue.Queue()



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

    def AC4(self):
        q = queue.Queue()
        S = {}
        counter = {}

        for (vi, vj) in self.C.keys():
            for ai in self.D[vi]:
                counter[(vi, ai, vj)] = 0
                S[(vi, ai)] = []

        for (vi, vj) in self.C.keys():
            for ai in self.D[vi][:]:
                for aj in self.D[vj]:
                    x = ai
                    y = aj

                    if eval(self.C[(vi, vj)]):
                        counter[(vi, ai, vj)] += 1
                        S[(vj, aj)].append((vi, ai))

                if counter[(vi, ai, vj)] == 0:
                    q.put((vi, ai))
                    self.D[vi].remove(ai)

        while not q.empty():
            (vj, aj) = q.get()

            for (vi, ai) in S[(vj, aj)]:
                if ai in self.D[vi]:
                    counter[(vi, ai, vj)] -= 1

                    if counter[(vi, ai, vj)] == 0:
                        q.put((vi, ai))
                        self.D[vi].remove(ai)



    def revise(self, Xi, Xj):
        revised = False

        for x in self.D[Xi][:]:
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


X = []
D = {}
C = {}

tempList = open('D.txt').read().splitlines()

for str in tempList:
    domain_desc = str.split(':')
    key = domain_desc[0].strip()
    val = domain_desc[1].split()

    val = [int(i) for i in val]

    X.append(key)
    D[key] = val

constraint_list = open('C.txt').read().splitlines()

for c in constraint_list:
    c_desc = c.split(':')

    c_desc[0] = c_desc[0].strip()
    nodes = c_desc[0].split(',')

    key = (nodes[0].strip(), nodes[1].strip())

    c_desc[1] = c_desc[1].strip()
    val = c_desc[1]

    C[key] = val


print('Variables :')
print(X)

print('Domains :')
print(D)

print('Contraints :')
print(C)

print('Arc Consistency :')
csp = CSP(X, D, C)
csp.AC1()
csp.result()
