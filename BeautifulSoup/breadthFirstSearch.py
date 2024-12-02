from collections import deque
import timeit



def bfs(links, start, target):
    queue = deque([start])
    visited = set()
    #Stores every URL that goes from the start URL to the url acting as a key
    paths = {start : f"{start}"}
    result = bfs_helper(links, start, target, queue, visited, paths)
    if result:
        #Prints out the shortest path from the start URL to the final URL
        print(f"Breadth First Search:")
        print(f"The shortest path between {start} and {target} is: {paths[target]}")
        #Prints out the average of the BFS function running 100 times
        t = timeit.Timer(lambda: bfs_helper(links, start, target, queue, visited, paths))
        print("Total time taken for BFS: ", t.timeit(100), "seconds")
    else:
        #Reports if the search was unsuccessful, as well as the average time of the function
        print(f"Breadth First Search Failed:")
        print(f"There is no path between {start} and {target}")
        t = timeit.Timer(lambda: bfs_helper(links, start, target, queue, visited, paths))
        print("Total time taken for BFS: ", t.timeit(100), "seconds")

def bfs_helper(links, start, target, queue, visited, paths):
    visited.add(start)
    while len(queue) != 0:
        #During each loop, the URL at the front of the queue is removed
        current = queue.popleft()
        #Checks if any of the URLs that the current URL links to is the final URL
        for neighbor in links[current]:
            if neighbor == target:
                #Records the urls that lead up to the final URL from the start URL in the paths dictionary
                paths[target] = paths[current] + f" -> {neighbor}"
                return True
            if neighbor not in visited:
                #Every other URL is added to the queue, marked as a visited URL, and has the path leading
                #up to it from the start URL recorded
                if neighbor in links.keys():
                    queue.append(neighbor)
                    visited.add(neighbor)
                    paths[neighbor] = paths[current] + f" -> {neighbor}"
    return False
"""
if __name__ == "__main__":

    diction = {"A" : ["B", "C"], "B" : ["D", "E"], "C" : ["F", "G"], "D" : ["E"], "E" : ["F"], "F" : [], "G" : [], "H" : []}
    bfs(diction, "A", "F")
"""


