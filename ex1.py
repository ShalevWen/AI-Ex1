import utils
import search
from functools import cache
from scipy.optimize import linear_sum_assignment

""" Rules """
GOAL = 1
PLAYER = 2
BLOCK = 4
WALL = 8
DEAD_END = 16
FULL = BLOCK | GOAL

class BoxMazeProblem(search.Problem):
    def __init__(self, initial, goal, board):
        self.board = board
        self.height = len(board)
        self.width = len(board[0])
        search.Problem.__init__(self, initial, goal=goal)
 
    def check_move(self, state, dx, dy):
        bound = self.height - 1 if dx else self.width - 1
        bx, by = state
        b = bx if dx else by

        if b == 0 or b == bound:
            return False
        if self.board[bx + dx][by + dy] & DEAD_END:
            return False
        if self.board[bx - dx][by - dy] & WALL:
            return False
        return True

    def successor(self, state):
        successors = []
        # generate U move
        if self.check_move(state, -1, 0):
            new_state = self.result(state, "U")
            successors.append(("U", new_state))
        # generate D move
        if self.check_move(state, 1, 0):
            new_state = self.result(state, "D")
            successors.append(("D", new_state))
        # generate L move
        if self.check_move(state, 0, -1):
            new_state = self.result(state, "L")
            successors.append(("L", new_state))
        # generate R move
        if self.check_move(state, 0, 1):
            new_state = self.result(state, "R")
            successors.append(("R", new_state))
        return successors

    def result(self, state, move):
        bx, by = state

        if move == "U":
            dx, dy = -1, 0
        elif move == "D":
            dx, dy = 1, 0
        elif move == "L":
            dx, dy = 0, -1
        elif move == "R":
            dx, dy = 0, 1

        return (bx + dx, by + dy)

    # def path_cost(self, c, state1, action, state2):
    #     """Return the cost of a solution path that arrives at state2 from
    #     state1 via action, assuming cost c to get up to state1. If the problem
    #     is such that the path doesn't matter, this function will only look at
    #     state2.  If the path does matter, it will consider c and maybe state1
    #     and action. The default method costs 1 for every step in the path."""
    #     dx, dy = state2[0] - state1[0], state2[1] - state1[1]
    #     if self.maze[]
    #     return c + 1

    def h(self, node):
        bx, by = node.state
        return abs(bx - self.goal[0]) + abs(by - self.goal[1])

    def __eq__(self, other):
        if not isinstance(other, BoxMazeProblem):
            return False
        return self.initial == other.initial and self.goal == other.goal
    
    def __hash__(self):
        return hash((self.initial, self.goal))

class SokobanProblem(search.Problem):
    """This class implements a sokoban problem"""
    def __init__(self, initial):
        self.dead_end = False

        self.height = len(initial)
        self.width = len(initial[0])

        self.goals = []
        # convert the state to a mutable object
        initial = [list(row) for row in initial]

        for i in range(self.height):
            for j in range(self.width):
                if initial[i][j] & PLAYER:
                    initial.append((i, j))
                if initial[i][j] & GOAL:
                    self.goals.append((i, j))
                if self.is_space_dead_end(initial, i, j):
                    initial[i][j] |= DEAD_END
        
        self.goals_len = len(self.goals)

        # convert the state back to an immutable object
        initial = tuple([tuple(row) for row in initial])
        self.goals = tuple(self.goals)

        search.Problem.__init__(self, initial)

    # put the function inside the class to reset the cache for each problem
    @cache
    def astar_search(self, problem):
        return search.astar_search(problem, problem.h)

    def is_space_dead_end(self, state, i, j):
        if state[i][j] & WALL:
            return True
        # block is allowed to be stuck on a goal
        if state[i][j] & GOAL:
            return False
        
        stuck_u = i == 0 or state[i - 1][j] & WALL
        stuck_d = i == self.height - 1 or state[i + 1][j] & WALL
        stuck_l = j == 0 or state[i][j - 1] & WALL
        stuck_r = j == self.width - 1 or state[i][j + 1] & WALL
        stuck_v = stuck_u or stuck_d
        stuck_h = stuck_l or stuck_r
        # check if the block is stuck in a corner
        if stuck_v and stuck_h:
            return True
        # check if the block is stuck on a horizontal wall
        if stuck_v:
            blocked_left = False
            for y in range(j - 1, -1, -1):
                if state[i][y] & GOAL and not stuck_r:
                    break
                if state[i][y] & (WALL | DEAD_END):
                    blocked_left = True
                    break
                if (i == 0 or i == self.height - 1
                        or state[i - 1][y] & WALL or state[i + 1][y] & WALL):
                    continue
                break
            else:
                blocked_left = True
            if blocked_left:
                for y in range(j + 1, self.width):
                    if state[i][y] & GOAL and not stuck_l:
                        break
                    if state[i][y] & (WALL | DEAD_END):
                        return True
                    if (i == 0 or i == self.height - 1
                            or state[i - 1][y] & WALL or state[i + 1][y] & WALL):
                        continue
                    break
                else:
                    return True
        # check if the block is stuck on a vertical wall
        if stuck_h:
            blocked_up = False
            for x in range(i - 1, -1, -1):
                if state[x][j] & GOAL and not stuck_d:
                    return False
                if state[x][j] & (WALL | DEAD_END):
                    blocked_up = True
                    break
                if (j == 0 or j == self.width - 1
                        or state[x][j - 1] & WALL or state[x][j + 1] & WALL):
                    continue
                break
            else:
                blocked_up = True
            if blocked_up:
                for x in range(i + 1, self.height):
                    if state[x][j] & GOAL and not stuck_u:
                        return False
                    if state[x][j] & (WALL | DEAD_END):
                        return True
                    if (j == 0 or j == self.width - 1
                            or state[x][j - 1] & WALL or state[x][j + 1] & WALL):
                        continue
                    return False
                else:
                    return True
        return False
 
    def check_move(self, state, dx, dy, bound):
        px, py = state[-1]
        p = px if dx else py
        # is the space standable
        if p == bound or state[px + dx][py + dy] & WALL:
            return False
        # is the space empty
        if not state[px + dx][py + dy] & BLOCK:
            return True
        # is the pushing possible and useful
        if (p == bound - dx - dy
                or state[px + 2*dx][py + 2*dy] & (BLOCK | DEAD_END)):
            return False
        return True

    def successor(self, state):
        successors = []
        # generate U move
        if self.check_move(state, -1, 0, 0):
            new_state = self.result(state, "U")
            successors.append(("U", new_state))
        # generate D move
        if self.check_move(state, 1, 0, self.height - 1):
            new_state = self.result(state, "D")
            successors.append(("D", new_state))
        # generate L move
        if self.check_move(state, 0, -1, 0):
            new_state = self.result(state, "L")
            successors.append(("L", new_state))
        # generate R move
        if self.check_move(state, 0, 1, self.width - 1):
            new_state = self.result(state, "R")
            successors.append(("R", new_state))
        return successors

    def result(self, state, move):
        px, py = state[-1]
        # copy the state to a mutable object
        new_state = [list(row) for row in state]

        if move == "U":
            dx, dy = -1, 0
        elif move == "D":
            dx, dy = 1, 0
        elif move == "L":
            dx, dy = 0, -1
        elif move == "R":
            dx, dy = 0, 1
        
        if state[px + dx][py + dy] & BLOCK:
            new_state[px + dx][py + dy] ^= BLOCK
            new_state[px + 2*dx][py + 2*dy] |= BLOCK
        new_state[-1] = (px + dx, py + dy)
        
        # copy the state back to an immutable object
        new_state = tuple([tuple(row) for row in new_state])
        return new_state

    def goal_test(self, state):
        for i, j in self.goals:
            if not state[i][j] & BLOCK:
                return False
        return True

    def h(self, node):
        state = node.state
        blocks = []
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                if state[i][j] & BLOCK:
                    state[i][j] & GOAL or blocks.append((i, j))
                    count += 1
                    if count == self.goals_len:
                        break
            if count == self.goals_len:
                break
            
        px, py = state[-1]
        min_dist = utils.infinity
        UNREACHABLE = self.height * self.width * len(blocks)
        cost_matrix = []
        for b0, b1 in blocks:
            dist = abs(b0 - px) + abs(b1 - py)
            if dist < min_dist:
                min_dist = dist
            # create a cost matrix for the linear sum assignment
            cost_matrix.append([])
            for g0, g1 in self.goals:
                if state[g0][g1] & BLOCK:
                    continue
                p = BoxMazeProblem((b0, b1), (g0, g1), self.initial)
                s = self.astar_search(p)
                if not s:
                    cost_matrix[-1].append(UNREACHABLE)
                else:
                    # don't include the root node
                    cost = len(s[0].path()) - 1
                    cost_matrix[-1].append(cost)
        total = 0
        if cost_matrix:
            total = min_dist - 1
            # find the min cost perfect matching between blocks and goals
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
            for i in range(len(row_ind)):
                cost = cost_matrix[row_ind[i]][col_ind[i]]
                if cost < UNREACHABLE:
                    total += cost
                else:
                    return utils.infinity
        
        return total


def create_sokoban_problem(game):
    """ Create a sokoban problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return SokobanProblem(game)
