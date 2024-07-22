import ex1
import search


def run_problem(func, targs=(), kwargs={}):
    result = (-3, "default")
    try:
        result = func(*targs, **kwargs)

    except Exception as e:
        result = (-3, e)
    return result

# check_problem: problem, search_method, timeout
# timeout_exec: search_method, targs=[problem], timeout_duration=timeout
def solve_problems(problem, algorithm):

    # for row in problem:
    #     print(row)

    try:
        p = ex1.create_sokoban_problem(problem)
    except Exception as e:
        print("Error creating problem: ", e)
        return None

    if algorithm == "gbfs":
        result = run_problem((lambda p: search.greedy_best_first_graph_search(p, p.h)),targs=[p])
    else:
        result = run_problem((lambda p: search.astar_search(p, p.h)), targs=[p])

    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        print(len(solution), solution)
    else:
        print("no solution")
problem0 = ((0,0,0,0),
			(8,0,8,0),
			(8,4,8,0),
			(1,0,0,2))
#optimal solution for problem 0: ['U', 'U', 'U', 'L', 'L', 'D', 'D', 'U', 'U', 'R', 'R', 'D', 'D', 'D', 'L', 'L']

problem_test = ((2, 4, 1),
                (8,8,8))
#optimal solution for problem test: ['R']

problem1 = ((0, 0, 8, 8, 8, 8, 8, 0),
            (8, 8, 8, 0, 0, 0, 8, 0),
            (8, 0, 2, 0, 0, 0, 8, 0),
            (8, 8, 8, 0, 0, 0, 8, 0),
            (8, 0, 8, 8, 4, 0, 8, 0),
            (8, 0, 8, 0, 1, 0, 8, 8),
            (8, 0, 0, 5, 0, 0, 0, 8),
            (8, 0, 0, 0, 0, 0, 0, 8),
            (8, 8, 8, 8, 8, 8, 8, 8))
#optimal solution for problem 1: ['R', 'R', 'D', 'D']

problem2 = ((8, 8, 8, 8, 8, 8, 8, 8),
            (8, 0, 0, 0, 0, 8, 8, 8),
            (8, 0, 8, 0, 1, 0, 0, 8),
            (8, 0, 2, 0, 1, 0, 0, 8),
            (8, 0, 0, 4, 4, 0, 0, 8),
            (8, 8, 0, 0, 0, 0, 0, 8),
            (8, 0, 0, 0, 0, 0, 0, 8),
            (8, 8, 8, 8, 8, 8, 8, 8))
#optimal solution for problem 2: ['D', 'D', 'R', 'U', 'L', 'U', 'R', 'D', 'R', 'D', 'R', 'U', 'U', 'R', 'U', 'L']

problem3 = ((8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0),
            (8, 0, 2, 0, 8, 8, 8, 1, 0, 1, 8, 8),
            (8, 0, 4, 0, 8, 0, 0, 0, 0, 0, 1, 8),
            (8, 0, 0, 4, 8, 0, 0, 8, 0, 0, 1, 8),
            (8, 0, 0, 4, 0, 0, 0, 8, 8, 8, 8, 8),
            (8, 0, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0),
            (8, 8, 8, 8, 8, 0, 4, 8, 0, 0, 0, 0),
            (0, 0, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0),
            (0, 0 ,0, 0, 8, 8, 8, 8, 0, 0, 0, 0))

problem4 = ((8,8,8,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0),
            (8,0,0,0,8,8,8,8,8,0,0,0,0,0,0,0,0,0),
            (8,0,4,0,0,0,0,0,8,0,0,8,8,8,8,8,0,0),
            (8,0,4,8,0,2,8,0,8,8,8,8,1,0,1,8,8,8),
            (8,0,4,0,4,8,8,0,8,0,0,0,0,0,1,1,1,8),
            (8,8,8,4,0,0,0,0,8,0,0,8,8,0,1,1,1,8),
            (0,0,8,0,0,0,0,4,0,0,0,0,8,8,0,8,8,8),
            (0,0,8,8,8,8,0,0,8,8,4,4,0,0,0,8,0,0),
            (0,0,0,0,0,8,8,8,8,8,0,0,8,8,8,8,0,0),
            (0,0,0,0,0,0,0,0,0,8,0,0,8,0,0,0,0,0),
            (0,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0,0))

problem5 = ((8,1,1,0),
            (8,8,0,0),
            (0,4,0,0),
            (0,4,0,8),
            (2,0,0,8))

problem29 = ((8, 8, 8, 8, 8, 8, 8, 8),
		    (8, 0, 0, 0, 8, 0, 0, 8),
		    (8, 0, 0, 0, 0, 0, 0, 8),
		    (8, 8, 0, 8, 1, 0, 0, 8),
		    (8, 0, 0, 0, 0, 8, 8, 8),
		    (8, 0, 8, 0, 1, 0, 8, 0),
		    (8, 0, 4, 4, 8, 0, 8, 0),
		    (8, 8, 8, 0, 0, 2, 8, 0),
		    (0, 0, 8, 8, 8, 8, 8, 0))

problem73 = ((8, 8, 8, 8, 0, 0, 0, 0),
            (8, 0, 0, 8, 8, 8, 8, 8),
            (8, 0, 4, 4, 0, 4, 0, 8),
            (8, 0, 0, 0, 0, 0, 0, 8),
            (8, 8, 0, 8, 8, 0, 8, 8),
            (8, 1, 1, 1, 8, 2, 8, 0),
            (8, 0, 8, 8, 8, 0, 8, 8),
            (8, 0, 0, 0, 0, 0, 0, 8),
            (8, 0, 0, 8, 0, 0, 0, 8),
            (8, 8, 8, 8, 8, 8, 8, 8))

def main():
    problem = problem3
    algorithm = "astar"#"gbfs" #or "astar"

    solve_problems(problem, algorithm)

if __name__ == '__main__':
    main()