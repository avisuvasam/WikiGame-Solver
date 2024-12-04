from collections import deque
import timeit

def dfs(links, start, target):

    stack = deque()
    visited = set()
    result = dfs_helper(links, start, target, stack, visited)

    if result:
        print(f"Depth First Search:")
        print(f"The shortest path between {start} and {target} is:", end = " ")
        #Prints out the URLs that lead from the start URL to the final URL
        first = stack.pop()
        print(f"{first}", end = " ")
        while len(stack) > 0:
            current = stack.pop()
            print(f"-> {current}", end = " ")
        #Prints out the average of the DFS function running for 100 times
        t = timeit.Timer(lambda: dfs_helper(links, start, target, stack, visited))
        print("")
        print("Total time taken for DFS: ", t.timeit(100), "seconds")
    else:
        #Reports if the search was unsuccessful, as well as the average time of the function
        print(f"Depth First Search Failed:")
        print(f"There is no path between {start} and {target}")
        t = timeit.Timer(lambda: dfs_helper(links, start, target, stack, visited))
        print("Total time taken for DFS: ", t.timeit(100), "seconds")

    return result



def dfs_helper(links, article, target, stack, visited):
    visited.add(article)
    if article == target:
        #When the target URL is found, it is added to the stack
        stack.append(article)
        return True
    for neighbor in links[article]:
        if neighbor in links.keys():
            if neighbor not in visited:
                visited.add(neighbor)
                if dfs_helper(links, neighbor, target, stack, visited):
                    #Once the target URL is found, all the URLs leading up to it are added recursively,
                    #So the final URL is added first and the start URL is added last
                    if article in links.keys():
                        stack.append(article)
                        return True
    return False


