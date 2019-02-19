import random

def graph_generator(nodes, edges, d_file, c_file):

    constraint_pool = ['x > y', 'x < y', 'x < y', 'x > y', 'x + y < 5', 'x + y > 5', 'x - y > 2', 'x - y < 2',
                       'x == y', 'x == y', 'x != y', 'x != y', 'x < y**2', 'x > y**2']

    D = open(d_file, 'w')
    C = open(c_file, 'w')

    for i in range(nodes):

        domain = random.sample(range(100), random.randrange(75))

        D.write(str(i) + ' : ')

        for j in domain:
            D.write(str(j) + ' ')

        D.write('\n')

    edge_list = []

    cnt = 0

    while True:

        v = random.sample(range(nodes), 2)
        idx = random.randrange(len(constraint_pool))

        if idx % 2 == 0:
            constraint = constraint_pool[idx]
            _constraint = constraint_pool[idx + 1]

        elif idx % 2 == 1:
            constraint = constraint_pool[idx]
            _constraint = constraint_pool[idx - 1]

        if not (v[0], v[1]) in edge_list:
            edge_list.append((v[0], v[1]))
            edge_list.append((v[1], v[0]))

            cnt += 2

            if cnt == edges:
                break

            C.write(str(v[0]) + ', ' + str(v[1]) + ' : ' + constraint + '\n')
            C.write(str(v[1]) + ', ' + str(v[0]) + ' : ' + _constraint + '\n')