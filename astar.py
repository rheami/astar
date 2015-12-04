import fileinput


class Node:

    def __init__(self, x, y, parent, f, g, h):
        self.parent = parent
        self.x = x
        self.y = y
        self.f = f
        self.g = g
        self.h = h

    def __repr__(self):
        #return repr((self.x, self.y, self.f, self.g, self.h, self.parent))
        return "{} - ({}, {})".format(self.parent, self.x, self.y)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self == other


def heuristic(node, goal):
    dx = abs(node.x - goal.x)
    dy = abs(node.y - goal.y)
    return dx + dy


# A*
def a_star(start, goal, mazemap):

    closed = []
    opened = [start]

    while len(opened) != 0:

        opened = sorted(opened, key=lambda node: node.f)
        q = opened.pop(0)
        successors = generate_successors(q, mazemap)

        for successor in successors:
            if successor == goal:
                return successor

            successor.h = heuristic(successor, goal)
            successor.f = successor.g + successor.h

            if skip_this_successor(opened, successor):
                continue
            if skip_this_successor(closed, successor):
                continue
            opened.append(successor)

        closed.append(q)
    return None


def skip_this_successor(alist, successor):
    for x in alist:
        if x == successor and x.f < successor.f:
            return True
    return False


def generate_successors(node, mazemap):
    """
            x-1, y-1  | x, y-1    | x+1, y-1
            x-1, y    | --------- | x+1, y
            x-1, y+1  | x, y+1    | x+1, y+1
    """
    numrows = len(mazemap)
    numcols = len(mazemap[0])

    successors = []
    for i in range(-1, 2):
        x = i + node.x
        if not (0 <= x < numcols):
            continue
        for j in range(-1, 2):
            y = j + node.y
            if not (0 <= y < numrows) or i == 0 and j == 0 or mazemap[y][x] == '1':
                continue

            g = 1 + node.g if i == 0 or j == 0 else 1.5 + node.g  # square_root of 2 = 1.414
            successors.append(Node(x, y, node, 0, g, 0))

    return successors


def show_path(start, goal, mazemap):
    parent = goal.parent
    while parent != start:
        mazemap[parent.y][parent.x] = '*'
        parent = parent.parent


def show_maze_map(mazemap):
    print('\n'.join([''.join(['{:2}'.format(item) for item in row])
        for row in mazemap]))


def main():
    start, goal, mazemap = init()

    goal = a_star(start, goal, mazemap)

    if goal is None:
        print("no solution found")
        return

    print("path is {}".format(goal))

    show_path(start, goal, mazemap)
    show_maze_map(mazemap)


def init():
    f = fileinput.input()
    dim_l, dim_h = [int(x) for x in f.readline().split(',')]
    #print(dim_l, dim_h)
    mazemap = []
    for j in range(dim_h):
        line = list(f.readline().strip('\n'))
        mazemap.append(line)
    x, y = [int(x) for x in f.readline().split(',')]
    mazemap[y][x] = 'S'
    print("start is {}, {}".format(x, y))
    start = Node(x, y, "", 0, 0, 0)
    x, y = [int(x) for x in f.readline().split(',')]
    mazemap[y][x] = 'X'
    print("goal is {}, {}".format(x, y))
    goal = Node(x, y, None, 0, 0, 0)
    #print(mazemap)
    f.close()

    show_maze_map(mazemap)

    return start, goal, mazemap


if __name__ == "__main__":
    main()