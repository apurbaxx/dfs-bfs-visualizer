import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import time

class GraphVisualizer:
    def __init__(self):
        self.graph = {}
        self.pos = None
        
    def add_edge(self, u, v):
        """Add an edge between nodes u and v"""
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)
    
    def create_sample_graph(self):
        """Create a sample graph for demonstration"""
        edges = [
            (0, 1), (0, 2), (1, 3), (1, 4),
            (2, 5), (2, 6), (3, 7), (4, 7)
        ]
        for u, v in edges:
            self.add_edge(u, v)
    
    def display_graph_structure(self):
        """Display the graph structure in terminal"""
        print("\n" + "="*50)
        print(" SAMPLE GRAPH STRUCTURE ".center(50))
        print("="*50)
        print("""
        0
       / \\
      1   2
     / \\ / \\
    3  4 5  6
     \\ /
      7
        """)
        print("="*50)
        print("\nGraph Connections:")
        for node in sorted(self.graph.keys()):
            neighbors = sorted(self.graph[node])
            print(f"  Node {node} → {neighbors}")
        print("="*50)
    
    def draw_graph(self, visited=None, current=None, title="Graph"):
        """Draw the graph with highlighted nodes"""
        plt.clf()
        
        G = nx.Graph()
        for node in self.graph:
            for neighbor in self.graph[node]:
                G.add_edge(node, neighbor)
        
        if self.pos is None:
            self.pos = nx.spring_layout(G, seed=42)
        
        # Color nodes based on state
        node_colors = []
        for node in G.nodes():
            if current is not None and node == current:
                node_colors.append('red')  # Current node being explored
            elif visited is not None and node in visited:
                node_colors.append('lightgreen')  # Already visited
            else:
                node_colors.append('lightblue')  # Not visited yet
        
        nx.draw(G, self.pos, with_labels=True, node_color=node_colors,
                node_size=800, font_size=16, font_weight='bold',
                edge_color='gray', linewidths=2)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.pause(0.8)
    
    def bfs(self, start_node):
        """Breadth-First Search visualization"""
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)
        
        print(f"\n{'='*50}")
        print("BFS Traversal Order:")
        print(f"{'='*50}")
        
        plt.figure(figsize=(10, 8))
        self.draw_graph(visited=visited, current=start_node, 
                       title="BFS - Starting Node")
        
        traversal_order = []
        
        while queue:
            current = queue.popleft()
            traversal_order.append(current)
            print(f"Visiting Node: {current}")
            
            self.draw_graph(visited=visited, current=current,
                          title=f"BFS - Visiting Node {current}")
            
            for neighbor in sorted(self.graph[current]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    print(f"  → Added {neighbor} to queue")
        
        self.draw_graph(visited=visited, title="BFS - Complete!")
        print(f"\nTraversal Order: {' → '.join(map(str, traversal_order))}")
        print(f"{'='*50}\n")
        plt.show()
    
    def dfs(self, start_node):
        """Depth-First Search visualization"""
        visited = set()
        traversal_order = []
        
        print(f"\n{'='*50}")
        print("DFS Traversal Order:")
        print(f"{'='*50}")
        
        plt.figure(figsize=(10, 8))
        
        def dfs_recursive(node):
            visited.add(node)
            traversal_order.append(node)
            print(f"Visiting Node: {node}")
            
            self.draw_graph(visited=visited, current=node,
                          title=f"DFS - Visiting Node {node}")
            
            for neighbor in sorted(self.graph[node]):
                if neighbor not in visited:
                    print(f"  → Exploring {neighbor}")
                    dfs_recursive(neighbor)
        
        dfs_recursive(start_node)
        
        self.draw_graph(visited=visited, title="DFS - Complete!")
        print(f"\nTraversal Order: {' → '.join(map(str, traversal_order))}")
        print(f"{'='*50}\n")
        plt.show()


def main():
    """Main function to run the visualizer"""
    print("\n" + "="*50)
    print(" GRAPH ALGORITHM VISUALIZER ".center(50))
    print("="*50)
    
    visualizer = GraphVisualizer()
    visualizer.create_sample_graph()
    visualizer.display_graph_structure()
    
    # Choose algorithm
    while True:
        print("\n" + "="*50)
        print("Select Algorithm:")
        print("1. BFS (Breadth-First Search)")
        print("2. DFS (Depth-First Search)")
        print("3. Both (BFS then DFS)")
        print("4. Exit")
        
        algo_choice = input("\nEnter your choice (1-4): ").strip()
        
        if algo_choice in ['1', '2', '3']:
            start_node = int(input("Enter start node: ").strip())
            
            if start_node not in visualizer.graph:
                print(f"✗ Node {start_node} not in graph!")
                print(f"Available nodes: {sorted(visualizer.graph.keys())}")
                continue
            
            if algo_choice == '1':
                visualizer.bfs(start_node)
            elif algo_choice == '2':
                visualizer.dfs(start_node)
            else:
                visualizer.bfs(start_node)
                visualizer.pos = None  # Reset position for DFS
                visualizer.dfs(start_node)
        elif algo_choice == '4':
            print("\nGoodbye! 👋")
            break
        else:
            print("✗ Invalid choice!")


if __name__ == "__main__":
    main()
