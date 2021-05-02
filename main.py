import random
from colorama import Back, Style
from sys import setrecursionlimit

setrecursionlimit(10000)


class Maze:
    def __init__(self, n, m):
        self.solved = False
        self.n = n
        self.m = m
        self.map = []
        for i in range(n):
            self.map.append(['black'] * m)
        self.visited = []
        for i in range(n):
            self.visited.append([False] * m)


def get_neighbors(maze, i, j):
    up = [i - 2, j]
    rt = [i, j + 2]
    dw = [i + 2, j]
    lt = [i, j - 2]
    cells = [up, rt, dw, lt]
    ret = list()
    for c in cells:
        if c[0] > 0 and c[0] < maze.n and c[1] > 0 and c[1] < maze.m and maze.map[c[0]][c[1]] != 'black' and maze.visited[c[0]][c[1]] == False:
                ret.append(c)
    return ret


def remove_wall(maze, x1, y1, x2, y2):
    diff_x = x2 - x1
    diff_y = y2 - y1
    add_x = 0
    add_y = 0
    if diff_x != 0:
        add_x = diff_x // abs(diff_x)
    if diff_y != 0:
        add_y = diff_y // abs(diff_y)
    target_x = x1 + add_x
    target_y = y1 + add_y
    maze.map[target_x][target_y] = 'white'
    maze.visited[target_x][target_y] = True


def print_maze(maze):
    if maze:
        for i in range(maze.n):
            for j in range(maze.m):
                if (maze.map[i][j] == 'black'):
                    print(Back.YELLOW + ' ', end = '')
                if (maze.map[i][j] == 'white'):
                    print(Back.WHITE + ' ', end='')
                if (maze.map[i][j] == 'red'):
                    print(Back.RED + ' ', end='')
                if (maze.map[i][j] == 'blue'):
                    print(Back.BLUE + ' ', end='')
                if (maze.map[i][j] == 'green'):
                    print(Back.GREEN + ' ', end='')

            print(Style.RESET_ALL)
    print()


def dfs_generation(n, m):
    n += 1 - (n % 2)
    m += 1 - (m % 2)
    maze = Maze(n, m)
    unvisited = list()
    for i in range(n):
        for j in range(m):
            maze.visited[i][j] = False
            if (i % 2 == 0 or j % 2 == 0) or i == n - 1 or j == m - 1:
                maze.map[i][j] = 'black'
            else:
                if i != 1 or j != 1:
                    unvisited.append([i, j])
                maze.map[i][j] = 'white'
    maze.visited[1][1] = True
    st = list()
    point = [1, 1]
    st.append(st)
    while unvisited:
        neighbors = get_neighbors(maze, point[0], point[1])
        if neighbors:
            ind = random.randint(0, len(neighbors) - 1)
            neighbor_cell = neighbors[ind]
            st.append(neighbor_cell)
            remove_wall(maze, point[0], point[1], neighbor_cell[0], neighbor_cell[1])
            maze.visited[neighbor_cell[0]][neighbor_cell[1]] = True
            unvisited.remove(neighbor_cell)
            point = neighbor_cell
        elif st:
            point = st[-1]
            st.remove(st[-1])
        else:
            ind = random.randint(0, len(unvisited) - 1)
            point = unvisited[ind]
    maze.map[1][1] = 'blue'
    maze.map[-2][-2] = 'red'
    return maze


def spanning_tree_generation(n, m):
    n += 1 - (n % 2)
    m += 1 - (m % 2)
    maze = Maze(n, m)
    for i in range(n):
        for j in range(m):
            maze.visited[i][j] = False
            if (i % 2 == 0 or j % 2 == 0) or i == n - 1 or j == m - 1:
                maze.map[i][j] = 'black'
            else:
                maze.map[i][j] = 'white'
    maze.visited[1][1] = True
    edges = set()
    neighbors = get_neighbors(maze, 1, 1)
    for i in neighbors:
        edges.add(((1, 1), tuple(i)))
    while edges:
        e = random.choice(list(edges))
        edges.remove(e)
        x1 = e[0][0]
        y1 = e[0][1]
        x2 = e[1][0]
        y2 = e[1][1]
        if maze.visited[x1][y1] != maze.visited[x2][y2]:
            remove_wall(maze, x1, y1, x2, y2)
        neighbors = get_neighbors(maze, x2, y2)
        for i in neighbors:
            edges.add(((x2, y2), tuple(i)))
        maze.visited[x1][y1] = True
        maze.visited[x2][y2] = True

    maze.map[1][1] = 'blue'
    maze.map[-2][-2] = 'red'
    return maze


def find_path(maze, x=1, y=1):
    if x == maze.n - 2 and y == maze.m - 2:
        return maze
    copy = maze
    if x == 1 and y == 1:
        for i in range(copy.n):
            for j in range(copy.m):
                copy.visited[i][j] = False
    up = [x - 1, y]
    rt = [x, y + 1]
    dw = [x + 1, y]
    lt = [x, y - 1]
    cells = [up, rt, dw, lt]
    for c in cells:
        if c[0] > 0 and c[0] < maze.n and c[1] > 0 and c[1] < maze.m and maze.map[c[0]][c[1]] != 'black' and maze.visited[c[0]][c[1]] == False:
            if x != 1 or y != 1:
                copy.map[x][y] = 'green'
            copy.visited[x][y] = True
            ret = find_path(copy, c[0], c[1])
            if ret:
                return ret
            else:
                if x != 1 or y != 1:
                    copy.map[x][y] = 'white'
    return False


def save(path, maze):
    f = open(path, 'w+')
    f.seek(0)
    f.write(str(maze.solved))
    f.write('\n')
    f.write(str(maze.n))
    f.write('\n')
    f.write(str(maze.m))
    f.write('\n')
    for i in maze.map:
        for j in i:
            f.write(str(j) + '\n')
    f.close()


def load(path):
    f = open(path, 'r')
    solved = bool(f.readline())
    n = int(f.readline())
    m = int(f.readline())
    maze = Maze(n, m)
    maze.solved = solved
    for i in range(n):
        for j in range(m):
            maze.map[i][j] = f.readline()[:-1]
    f.close()
    return maze


def programm():
    while True:
        print("Do you want to load labyrinth from file? Y - yes, N - no")
        answer = input()
        maze = Maze(0, 0)
        if answer == "Y":
            print("write file name or path")
            path = input()
            maze = load(path)
        else:
            print("Enter labyrinth's width and length, or \"exit\" to exit programm")
            width = input()
            if width == "exit":
                break
            width = int(width)
            length = int(input())
            print("Enter type of labyrinth generation: 1 - dfs, 2 - spanning tree")
            labyrinth_type = input()
            if labyrinth_type == "1":
                maze = dfs_generation(width, length)
            else:
                maze = spanning_tree_generation(width, length)
        print_maze(maze)
        if maze.solved == False:
            print("Do you want to see solution? Y - yes, N - no")
            answer = input()
            if answer == "Y":
                solution = find_path(maze)
                print_maze(solution)
                solution.solved = True
            print("Do you want to save this labyrinth? Y - yes, N - no")
            answer = input()
            if answer == "Y":
                print("Write file name or path")
                path = input()
                save(path, maze)




programm()
