import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast
from collections import Counter
import radon.complexity as radon_cc
from wordcloud import WordCloud
import seaborn as sns
import re

def analyze_ast(file_content):
    try:
        code = file_content.decode('utf-8')
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
        return table_data
    except SyntaxError as e:
        return f"Syntax error in code: {e}"

def rate_code(cyclomatic_complexity):
    # Simple scoring system based on Cyclomatic Complexity
    if cyclomatic_complexity <= 5:
        rating = (10, "🟢")  # Very good
    elif cyclomatic_complexity <= 10:
        rating = (8, "🟢")  # Good
    elif cyclomatic_complexity <= 20:
        rating = (6, "🟡")  # Average
    elif cyclomatic_complexity <= 30:
        rating = (4, "🔴")  # Below average
    else:
        rating = (2, "🔴")  # Bad

    return rating

def analyze_comments(code):
    # Analyze comments in the code
    comment_lines = [line for line in code.split('\n') if line.strip().startswith('#')]
    total_lines = len(code.split('\n'))
    comment_percentage = (len(comment_lines) / total_lines) * 100
    return comment_percentage

def analyze_variable_names(code):
    # Analyze variable names in the code
    # We'll consider variable names that are too short or not descriptive as bad
    variable_names = re.findall(r'\b[A-Za-z_]\w*\b', code)
    bad_variable_names = [name for name in variable_names if len(name) <= 2 or name.islower()]
    total_variables = len(variable_names)
    bad_variable_percentage = (len(bad_variable_names) / total_variables) * 100
    return bad_variable_percentage

def analyze_code(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        # Calculate Cyclomatic Complexity
        complexity = radon_cc.cc_visit(code)
        total_complexity = sum([node.complexity for node in complexity])

        # Rate the code based on Cyclomatic Complexity
        score = rate_code(total_complexity)

        # Analyze comments
        comment_percentage = analyze_comments(code)

        # Analyze variable names
        bad_variable_percentage = analyze_variable_names(code)

        # Construct analysis results list
        analysis_result = []
        analysis_result.append(f"Code analysis results for file '{file_path}':\n")
        analysis_result.append(f"Cyclomatic Complexity: {total_complexity}\n")
        analysis_result.append(f"Code Rating: {score[0]}/10, {score[1]}\n")
        analysis_result.append(f"Comment Percentage: {comment_percentage:.2f}%\n")
        analysis_result.append(f"Bad Variable Name Percentage: {bad_variable_percentage:.2f}%\n")

        return analysis_result
    except FileNotFoundError:
        return f"File '{file_path}' not found."

# Sidebar title and buttons
with st.sidebar:
    st.title("CodeSense: A code analyzer")
    uploaded_file = st.file_uploader("Upload Python file", type=["py"])

    if uploaded_file is not None:
        st.write("File uploaded successfully!")

    start_button = st.button("Start")

# Main title
st.title("Code Analyzer")

if start_button and uploaded_file:
    custom_css = """
    <style>
    .title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .stat {
        font-size: 18px;
        margin-bottom: 8px;
    }
    </style>
    """
    # AST Analysis
    code_result = analyze_code(uploaded_file.name)
    st.subheader("Code Analysis Result:")
    if len(code_result) == 0:
        st.error(code_result)
    else:
        for line in code_result:
            st.write(line)

    ast_result = analyze_ast(uploaded_file.getvalue())
    st.subheader("AST Analysis Result:")
    if isinstance(ast_result, str):
        st.error(ast_result)
    else:
        # Extract node types and their counts for visualization
        node_types, counts = zip(*ast_result)
        
        # Create a bar chart
        
        ast_df = pd.DataFrame(ast_result, columns=['Node Type', 'Count'])

        # Display DataFrame with progress graph
        st.dataframe(
            ast_df,
            column_order=("Node Type", "Count"),
            hide_index=True,
            width=None,
            column_config={
                "Node Type": st.column_config.TextColumn("Node Type"),
                "Count": st.column_config.ProgressColumn(
                    "Count",
                    format="%d",
                    min_value=0,
                    max_value=int(ast_df['Count'].max())  # Convert NumPy int64 to standard Python integer
                )
            }
        )

        # Word cloud
        wordcloud_data = {node_type: count for node_type, count in ast_result}
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_data)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        # Display the word cloud using st.image()
        st.image(wordcloud.to_array())

        ast_df = pd.DataFrame(ast_result, columns=['Node Type', 'Count'])

        # Sort DataFrame by node count in descending order
        ast_df = ast_df.sort_values(by='Count', ascending=False)

        # Create a heatmap using Seaborn
        plt.figure(figsize=(10, 6))
        sns.heatmap(data=ast_df.set_index('Node Type'), annot=True, cmap='YlGnBu', fmt='d')
        plt.title('AST Node Type Heatmap')
        plt.xlabel('Count')
        plt.ylabel('Node Type')

        # Display the heatmap using st.pyplot() with the figure object
        st.pyplot(plt.gcf())
