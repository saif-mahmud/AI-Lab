import copy
import queue
import random
import time

import matplotlib.pyplot as plt

from GraphGenerator_054 import graph_generator


class CSP:
    def __init__(self, X: list, D: dict, C: dict):
        self.X = copy.deepcopy(X)
        self.D = copy.deepcopy(D)
        self.C = copy.deepcopy(C)
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


ac1 = []
ac2 = []
ac3 = []
ac4 = []

no_of_nodes = []
no_of_edges = []
D_size = []


for k in range(10, 250):

    print('\nNodes :', k)

    #n = 2
    n = random.randrange(2, 4)

    vertex = k
    arc = n * k

    if arc % 2 == 1:
        arc = arc - 1

    domain_size = random.randrange(75, 126)

    no_of_nodes.append(vertex)
    no_of_edges.append(arc)
    D_size.append(domain_size)

    d_file = 'D' + str(k - 10) + '.txt'
    c_file = 'C' + str(k - 10) + '.txt'

    # d_file = 'D.txt'
    # c_file = 'C.txt'

    graph_generator(vertex, arc, domain_size, d_file, c_file)

    X = []
    D = {}
    C = {}

    tempList = open(d_file).read().splitlines()

    for s in tempList:
        domain_desc = s.split(':')
        key = domain_desc[0].strip()
        val = domain_desc[1].split()

        val = list(map(int, val))

        X.append(key)
        D[key] = val

    constraint_list = open(c_file).read().splitlines()

    for c in constraint_list:
        c_desc = c.split(':')

        c_desc[0] = c_desc[0].strip()
        nodes = c_desc[0].split(',')

        key = (nodes[0].strip(), nodes[1].strip())

        c_desc[1] = c_desc[1].strip()
        val = c_desc[1]

        C[key] = val

    print(CSP(X, D, C).AC3())


    print('\nAC1 :')
    time0 = time.time()

    csp1 = CSP(X, D, C)
    csp1.AC1()
    csp1.result()

    time1 = time.time()
    ac1_time = (time1 - time0) * 1000
    print('AC1 Elapsed Time :', ac1_time)
    ac1.append(ac1_time)

    print('\nAC2 :')
    csp2 = CSP(X, D, C)
    csp2.AC2()
    csp2.result()

    time2 = time.time()
    ac2_time = (time2 - time1) * 1000
    print('AC2 Elapsed Time :', ac2_time)
    ac2.append(ac2_time)

    print('\nAC3 :')
    csp3 = CSP(X, D, C)
    csp3.AC3()
    csp3.result()

    time3 = time.time()
    ac3_time = (time3 - time2) * 1000
    print('AC3 Elapsed Time :', ac3_time)
    ac3.append(ac3_time)

    print('\nAC4 :')
    csp4 = CSP(X, D, C)
    csp4.AC4()
    csp4.result()

    time4 = time.time()
    ac4_time = (time4 - time3) * 1000
    print('AC4 Elapsed Time :', ac4_time)
    ac4.append(ac4_time)


with open('AC1.txt', 'w') as ac1_out:
    for item in ac1:
        ac1_out.write("%s\n" % item)

with open('AC2.txt', 'w') as ac2_out:
    for item in ac2:
        ac2_out.write("%s\n" % item)

with open('AC3.txt', 'w') as ac3_out:
    for item in ac3:
        ac3_out.write("%s\n" % item)

with open('AC4.txt', 'w') as ac4_out:
    for item in ac4:
        ac4_out.write("%s\n" % item)


plt.plot(no_of_nodes, ac1, label = 'AC1')
plt.plot(no_of_nodes, ac2, label = 'AC2')
plt.plot(no_of_nodes, ac3, label = 'AC3')
plt.plot(no_of_nodes, ac4, label = 'AC4')

plt.xlabel('# of Nodes')
plt.ylabel('Elapsed Time')
plt.legend()
plt.grid(True)

plt.savefig('fig7.png', bbox_inches='tight')
plt.show()
