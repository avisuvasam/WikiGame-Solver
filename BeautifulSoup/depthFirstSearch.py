from collections import deque
import numpy as np
import timeit

def dfs(links, start, target):

    stack = deque()
    visited = set()
    result = dfs_helper(links, start, target, stack, visited)

    if result:
        print(f"The shortest path between {start} and {target} is:", end = " ")
        first = stack.pop()
        print(f"{first}", end = " ")
        while len(stack) > 0:
            current = stack.pop()
            print(f"-> {current}", end = " ")
        t = timeit.Timer(lambda: dfs_helper(links, current, target, stack, visited))
        print("")
        print("Total time taken: ", t.timeit(100), "seconds")
    else:
        print(f"There is no path between {start} and {target}")
        t = timeit.Timer(lambda: dfs_helper(links, current, target, stack, visited))
        print("")
        print("Total time taken: ", t.timeit(100), "seconds")

    return result



def dfs_helper(links, article, target, stack, visited):
    visited.add(article)
    if article == target:
        stack.append(article)
        return True
    for neighbor in links[article]:
        if neighbor not in visited:
            visited.add(neighbor)
            if dfs_helper(links, neighbor, target, stack, visited):
                stack.append(article)
                return True
    return False

"""
if __name__ == "__main__":

    dict = {"A" : ["B", "C"], "B" : ["D", "E"], "C" : ["F", "G"], "D" : ["E"], "E" : ["F"], "F" : [], "G" : [], "H" : []}
    dfs(dict, "A", "F")
"""

