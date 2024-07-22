import ex1
import search
import importlib
import os
from timeit import timeit

levels_file = "sokogen-990602"
algorithm = "gbfs" #"gbfs" or "astar"

def run_problem(func, targs=(), kwargs={}):
    result = (-3, "default")
    try:
        result = func(*targs, **kwargs)

    except Exception as e:
        result = (-3, e)
    return result

def solve_problems(problem, i, algorithm, output):
    try:
        p = ex1.create_sokoban_problem(problem)
        print(f"Level {i + 1} created")
    except Exception as e:
        print(f"Error creating Level {i + 1}: ", e)
        return None

    if algorithm == "gbfs":
        result = run_problem((lambda p: search.greedy_best_first_graph_search(p, p.h)),targs=[p])
    else:
        result = run_problem((lambda p: search.astar_search(p, p.h)), targs=[p])

    output.write(f"Level {i + 1}: ")
    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        output.write(f"{len(solution)} moves\n")
        output.write(f"{solution}\n")
        print(f"Level {i + 1} solved in {len(solution)} steps", end="")
    else:
        if result[1] == "default":
            output.write("no solution\n")
            print(f"Level {i + 1} has no solution", end="")
        else:
            output.write(f"Level {i + 1} has an error\n")
            print(f"error: {result[1]}", end="")

def main():
    levels = importlib.import_module(f"levels.{levels_file}")
    if not os.path.exists('output'):
        os.makedirs('output')
    total_time = 0
    max_time, max_index = 0, 0
    with open(f"output/{levels_file}_{algorithm}.txt", 'w') as output:
        for i in range(len(levels.levels)):
            time = timeit(lambda:solve_problems(levels.levels[i], i, algorithm, output),number=1)
            total_time += time
            if time > max_time:
                max_time = time
                max_index = i
            output.write(f"Level {i + 1} solved in {time} seconds\n\n")
            print(f", {time} seconds")
        output.write(f"Total time: {total_time} seconds\n")
        output.write(f"Max time: {max_time} seconds for Level {max_index + 1}\n")

if __name__ == '__main__':
    main()