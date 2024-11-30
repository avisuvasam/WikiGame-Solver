from collections import deque
import timeit



def bfs(links, start, target):
    queue = deque([start])
    visited = set()
    paths = {start : f"{start}"}
    result = bfs_helper(links, start, target, queue, visited, paths)
    if result:
        print(f"The shortest path between {start} and {target} is: {paths[target]}")
        t = timeit.Timer(lambda: bfs_helper(links, start, target, queue, visited, paths))
        print("Total time taken: ", t.timeit(100), "seconds")
    else:
        print(f"There is no path between {start} and {target}")
        t = timeit.Timer(lambda: bfs_helper(links, start, target, queue, visited, paths))
        print("Total time taken: ", t.timeit(100), "seconds")

def bfs_helper(links, start, target, queue, visited, paths):
    visited.add(start)
    while len(queue) != 0:
        current = queue.popleft()

        for neighbor in links[current]:
            if neighbor == target:

                paths[target] = paths[current] + f" -> {neighbor}"
                return True
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                paths[neighbor] = paths[current] + f" -> {neighbor}"
    return False
"""
if __name__ == "__main__":

    diction = {"A" : ["B", "C"], "B" : ["D", "E"], "C" : ["F", "G"], "D" : ["E"], "E" : ["F"], "F" : [], "G" : [], "H" : []}
    bfs(diction, "A", "F")
"""


