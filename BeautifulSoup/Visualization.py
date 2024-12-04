import tkinter as tk
from tkinter import scrolledtext, messagebox
from AdjList import AdjList
import breadthFirstSearch
import depthFirstSearch
import asyncio
import threading
import sys
import time
import webbrowser
from pyvis.network import Network

# Redirects print statements to the UI
#Ref: https://stackoverflow.com/questions/12351786/how-to-redirect-print-statements-to-tkinter-text-widget
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)

    def flush(self):
        pass  # Required for compatibility with Python's standard output

# Ref https://www.geeksforgeeks.org/python-gui-tkinter/
class WikiGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WikiGame Solver")
        self.graph = {}

        # UI Layout
        tk.Label(root, text="Start URL:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.start_url = tk.Entry(root, width=50)
        self.start_url.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="End URL:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.end_url = tk.Entry(root, width=50)
        self.end_url.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(root, text="Build Graph", command=self.build_graph).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Run BFS", command=self.run_bfs).grid(row=3, column=0, pady=5)
        tk.Button(root, text="Run DFS", command=self.run_dfs).grid(row=3, column=1, pady=5)

        self.output = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
        self.output.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Button to open the graph visualization
        self.visualize_button = tk.Button(
            root, text="Open Graph Visualization", command=self.open_graph, state=tk.DISABLED
        )
        self.visualize_button.grid(row=5, column=0, columnspan=2, pady=10)

    def log_message(self, message):
        # Logs messages to the output area
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)

    def build_graph(self):
        # Builds the adjacency list graph
        start = self.start_url.get()
        end = self.end_url.get()

        if not start or not end:
            messagebox.showerror("Error", "Both Start and End URLs must be provided.")
            return

        self.log_message(f"Building graph from {start} to {end}...")

        def task():
            adjlist = AdjList(start, end)

            # Run the coroutine in an event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(adjlist.buildAdjList(time.time()))
            loop.close()

            # Update graph
            self.graph = adjlist.dictURL
            self.log_message("Graph built successfully!")

            # Generate graph visualization
            self.generate_graph_visualization()

       # Ref https://www.geeksforgeeks.org/multithreading-python-set-1/
        threading.Thread(target=task).start() #Allows for faster processing

    def generate_graph_visualization(self):
        # Generates an interactive graph visualization using pyvis, with BFS and distributed connections.
        if not self.graph:
            self.log_message("Error: Graph is empty. Cannot generate visualization.")
            return

        start = self.start_url.get()
        end = self.end_url.get()
        max_nodes = 100  # Maximum number of nodes to display
        #Ref for using pyvis https://stackoverflow.com/questions/77331482/how-can-we-plot-a-network-graph-using-pyvis-in-a-browser
        net = Network(height="750px", width="100%", directed=True)
        net.toggle_physics(True)  # Enable physics for better layout handling

        # Get BFS path using breadthFirstSearch
        path_str = breadthFirstSearch.bfs(self.graph, start, end)
        path = path_str.split(" -> ") if path_str else []

        # Visualize BFS path
        added_nodes = set()
        node_count = 0

        if path:
            bfs_slots = max_nodes - len(path)  # Remaining slots after BFS nodes
            path_with_connections = path[:-1]  # Exclude the end node from connection distribution
            per_bfs_node = bfs_slots // len(path_with_connections) if path_with_connections else 0

            for i in range(len(path) - 1):
                if node_count >= max_nodes:
                    break

                # Add BFS nodes
                net.add_node(path[i], label=path[i], color="green")
                net.add_node(path[i + 1], label=path[i + 1], color="green")
                net.add_edge(path[i], path[i + 1], color="green", arrowsize=1.5)
                added_nodes.add(path[i])
                added_nodes.add(path[i + 1])
                node_count += 2

                # Add outgoing connections for the BFS node
                if path[i] in path_with_connections:
                    connections = 0
                    for neighbor in self.graph.get(path[i], []):
                        if connections >= per_bfs_node or node_count >= max_nodes:
                            break
                        if neighbor not in added_nodes:
                            net.add_node(neighbor, label=neighbor)
                            net.add_edge(path[i], neighbor, color="blue", arrowsize=1)
                            added_nodes.add(neighbor)
                            node_count += 1
                            connections += 1

        # Add remaining nodes and edges
        for node, edges in self.graph.items():
            if node_count >= max_nodes:
                break
            if node not in added_nodes:
                net.add_node(node, label=node)
                added_nodes.add(node)
                node_count += 1
            for edge in edges:
                if node_count >= max_nodes:
                    break
                if edge not in added_nodes:
                    net.add_node(edge, label=edge)
                    added_nodes.add(edge)
                    node_count += 1
                net.add_edge(node, edge, color="blue", arrowsize=1)

        # Save and enable visualization
        net.save_graph("graph_visualization.html")
        self.log_message("Graph visualization saved as 'graph_visualization.html'.")
        self.visualize_button.config(state=tk.NORMAL)

    def open_graph(self):
        # Opens the graph visualization
        webbrowser.open("graph_visualization.html")
        self.log_message("Opening graph visualization in the browser...")

    def run_bfs(self):
        if not self.graph:
            messagebox.showerror("Error", "Please build the graph first.")
            return

        start = self.start_url.get()
        end = self.end_url.get()

        self.log_message("Running BFS...")
        old_stdout = sys.stdout
        sys.stdout = TextRedirector(self.output)
        breadthFirstSearch.bfs(self.graph, start, end)
        sys.stdout = old_stdout

    def run_dfs(self):
        if not self.graph:
            messagebox.showerror("Error", "Please build the graph first.")
            return

        start = self.start_url.get()
        end = self.end_url.get()

        self.log_message("Running DFS...")
        old_stdout = sys.stdout
        sys.stdout = TextRedirector(self.output)
        depthFirstSearch.dfs(self.graph, start, end)
        sys.stdout = old_stdout
