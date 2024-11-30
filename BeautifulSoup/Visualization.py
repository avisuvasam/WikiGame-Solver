import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

# Streamlit UI
st.title("WikiGame Solver")

# Create two columns
col1, col2 = st.columns([1, 3])  # Adjust the proportions as needed (e.g., 1:3 for left:right)

# Left column for input fields and link
with col1:
    st.markdown("[Play WikiGame](https://www.thewikigame.com/)")

    # Input fields for start and end pages
    start_page = st.text_input("Start:", "Albert Einstein")
    end_page = st.text_input("Goal:", "String theory")

    # Traversals section
    st.write("### Traversals")

    # Buttons for DFS and BFS
    dfs_clicked = st.button("Depth-First Search")
    bfs_clicked = st.button("Breadth-First Search")

# Right column for graph visualization
with col2:
    st.write("Graph Visualization:")

    # Create a placeholder graph for now (replace with dynamic graph later)
    fig, ax = plt.subplots(figsize=(10, 8))
    G = nx.DiGraph()
    G.add_edge(start_page, end_page)  # Example edge
    nx.draw_networkx(G, with_labels=True, node_size=2000, font_size=10, node_color="skyblue", ax=ax)

    # Display the graph
    st.pyplot(fig)
