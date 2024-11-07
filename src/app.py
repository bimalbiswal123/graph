from flask import Flask, render_template
import sqlite3
from graphviz import Digraph

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('graph.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS nodes (id INTEGER PRIMARY KEY, label TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS edges (source INTEGER, target INTEGER)')
    conn.commit()
    conn.close()

# Sample data
def insert_sample_data():
    conn = sqlite3.connect('graph.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO nodes (label) VALUES ("A"), ("B"), ("C")')
    cursor.execute('INSERT INTO edges (source, target) VALUES (1, 2), (2, 3), (3, 1)')
    conn.commit()
    conn.close()

# Call these functions on the first run
init_db()
insert_sample_data()

# Generate directed graph with Graphviz
def generate_graph():
    conn = sqlite3.connect('graph.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, label FROM nodes')
    nodes = cursor.fetchall()
    cursor.execute('SELECT source, target FROM edges')
    edges = cursor.fetchall()
    conn.close()

    dot = Digraph(comment="Directed Graph", format='png')
    
    for node_id, label in nodes:
        dot.node(str(node_id), label)
    
    for source, target in edges:
        dot.edge(str(source), str(target))
    
    dot.render('static/graph', format='png')  # Saves the graph as a PNG image

# Route to display the graph
@app.route('/')
def display_graph():
    generate_graph()
    return render_template('graph.html')

if __name__ == '__main__':
    app.run(debug=True)
