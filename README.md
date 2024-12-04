# WikiGame Solver

## By: Ashton Visuvasam, Russell Ryan, Ari Tramont

## Concept
The WikiGame Solver automates the WikiGame, where the goal is to navigate from one Wikipedia page to another by only using the links within the Wikipedia pages. The application provides features like breadth-first and depth-first traversals and a visualization of the graph.

## How the Code Works
To start, the user inputs two Wikipedia URLs: a start URL and an end URL. The application then builds a graph using the links found on the Wikipedia pages. Once the graph is built, users can perform the following actions:
- Run a **Breadth-First Search (BFS)** to find the shortest path between the start and end URLs.
- Run a **Depth-First Search (DFS)** to explore the graph in a depth-first manner.
- Visualize the graph in an interactive browser-based graph, highlighting the BFS path and other connections.

## How to Run the Code

### Prerequisites
1. Clone the repository and ensure all files are located in the same directory.
2. Install the required Python libraries: Aiohttp, Asyncio, BeautifulSoup, queue:Queue, Collections:deque, Timeit, Time, tkinter, threading, sys, webbrowser, pyvis

## Using the Application

1. Enter two Wikipedia URLs in the text boxes at the top of the UI.  
   - **Example URL**: `https://en.wikipedia.org/wiki/Professional_wrestling`
   - For the best experience, consider using Words provided by [The WikiGame](https://www.thewikigame.com/group) and then finding the corresponding wikipedia page in a separate browser

2. Click the **Build Graph** button and wait for a success message in the output area:  
   _"Graph built successfully!"_

3. Perform graph traversals:
   - **Run BFS**: Click the **Run BFS** button to perform a breadth-first search. The path and traversal time will be displayed.
   - **Run DFS**: Click the **Run DFS** button to perform a depth-first search. The path and traversal time will be displayed.

4. Visualize the graph:  
   Once the graph is built, click the bottom-most button to open an interactive graph visualization in your browser.

---

## Troubleshooting

- **If the graph fails to build**:
  - Ensure the URLs are valid Wikipedia links.
  - Try using different URLs if the current ones fail.

- **If the application becomes unresponsive**:
  - Restart the application.


