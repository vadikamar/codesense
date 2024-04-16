import ast
import streamlit as st
from tabulate import tabulate
from collections import Counter

def analyze_file(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()
            parsed_code = ast.parse(code)
            # Get line numbers for each node
            lines = code.split('\n')
            # Initialize counter for node types
            node_counter = Counter()
            # Traverse the AST and count each node type
            for node in ast.walk(parsed_code):
                node_type = type(node).__name__
                node_counter[node_type] += 1
            # Convert counter to a list of tuples for tabulation
            table_data = [(node_type, count) for node_type, count in node_counter.items()]
            # Generate table
            return table_data
    except FileNotFoundError:
        return f"File '{file_path}' not found."
    except SyntaxError as e:
        return f"Syntax error in code: {e}"

# Sidebar title and button
