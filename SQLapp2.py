import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import numpy as np
import pandas as pd

# Sample data for tables
def generate_sample_data():
    # Table A - Employees
    df_a = pd.DataFrame({
        'emp_id': [1, 2, 3, 4, 5],
        'name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
        'department': ['IT', 'HR', 'IT', 'Finance', 'Marketing']
    })
    
    # Table B - Salaries
    df_b = pd.DataFrame({
        'emp_id': [2, 3, 4, 6, 7],
        'salary': [60000, 75000, 65000, 80000, 70000],
        'bonus': [5000, 7500, 6000, 8000, 7000]
    })
    
    return df_a, df_b

def execute_join(df_a, df_b, join_type):
    if join_type == "INNER JOIN":
        return pd.merge(df_a, df_b, on='emp_id', how='inner')
    elif join_type == "FULL JOIN":
        return pd.merge(df_a, df_b, on='emp_id', how='outer')
    elif join_type == "FULL JOIN WITH NULLS":
        merged = pd.merge(df_a, df_b, on='emp_id', how='outer')
        return merged[merged['name'].isna() | merged['salary'].isna()]
    elif join_type == "LEFT JOIN":
        return pd.merge(df_a, df_b, on='emp_id', how='left')
    elif join_type == "LEFT JOIN WITH NULL":
        merged = pd.merge(df_a, df_b, on='emp_id', how='left')
        return merged[merged['salary'].isna()]
    elif join_type == "RIGHT JOIN":
        return pd.merge(df_a, df_b, on='emp_id', how='right')
    elif join_type == "RIGHT JOIN WITH NULL":
        merged = pd.merge(df_a, df_b, on='emp_id', how='right')
        return merged[merged['name'].isna()]

def create_venn_diagram(sets, labels=('A', 'B'), colors=('lightgray', 'lightgray'), title="", subset_colors=None):
    plt.figure(figsize=(6, 4))
    v = venn2(sets, set_labels=labels)
    
    if subset_colors:
        for id, color in subset_colors.items():
            if v.get_patch_by_id(id):
                v.get_patch_by_id(id).set_color(color)
    
    plt.title(title)
    return plt

def main():
    st.set_page_config(layout="wide")
    st.title("Interactive SQL JOIN Types Visualizer")
    st.write("Explore different types of SQL JOINs with real data examples")

    # Generate sample data
    df_a, df_b = generate_sample_data()

    # Define the JOIN types and their explanations
    joins = {
        "INNER JOIN": {
            "query": """
            SELECT *
            FROM employees A
            INNER JOIN salaries B ON A.emp_id = B.emp_id
            """,
            "sets": (1, 1, 1),
            "colors": {'10': 'white', '01': 'white', '11': '#90EE90'},
            "description": "Returns only the matching records from both tables"
        },
        "FULL JOIN": {
            "query": """
            SELECT *
            FROM employees A
            FULL JOIN salaries B ON A.emp_id = B.emp_id
            """,
            "sets": (1, 1, 1),
            "colors": {'10': '#90EE90', '01': '#90EE90', '11': '#90EE90'},
            "description": "Returns all records from both tables, matching where possible"
        },
        "FULL JOIN WITH NULLS": {
            "query": """
            SELECT *
            FROM employees A
            FULL JOIN salaries B ON A.emp_id = B.emp_id
            WHERE A.emp_id IS NULL OR B.emp_id IS NULL
            """,
            "sets": (1, 1, 1),
            "colors": {'10': '#90EE90', '01': '#90EE90', '11': 'white'},
            "description": "Returns only non-matching records from both tables"
        },
        "LEFT JOIN": {
            "query": """
            SELECT *
            FROM employees A
            LEFT JOIN salaries B ON A.emp_id = B.emp_id
            """,
            "sets": (1, 1, 1),
            "colors": {'10': '#90EE90', '01': 'white', '11': '#90EE90'},
            "description": "Returns all records from table A and matching records from table B"
        },
        "LEFT JOIN WITH NULL": {
            "query": """
            SELECT *
            FROM employees A
            LEFT JOIN salaries B ON A.emp_id = B.emp_id
            WHERE B.emp_id IS NULL
            """,
            "sets": (1, 1, 1),
            "colors": {'10': '#90EE90', '01': 'white', '11': 'white'},
            "description": "Returns only records from table A that don't match table B"
        },
        "RIGHT JOIN": {
            "query": """
            SELECT *
            FROM employees A
            RIGHT JOIN salaries B ON A.emp_id = B.emp_id
            """,
            "sets": (1, 1, 1),
            "colors": {'10': 'white', '01': '#90EE90', '11': '#90EE90'},
            "description": "Returns all records from table B and matching records from table A"
        },
        "RIGHT JOIN WITH NULL": {
            "query": """
            SELECT *
            FROM employees A
            RIGHT JOIN salaries B ON A.emp_id = B.emp_id
            WHERE A.emp_id IS NULL
            """,
            "sets": (1, 1, 1),
            "colors": {'10': 'white', '01': '#90EE90', '11': 'white'},
            "description": "Returns only records from table B that don't match table A"
        }
    }

    # Sidebar
    st.sidebar.title("Controls")
    selected_join = st.sidebar.selectbox(
        "Select JOIN Type",
        list(joins.keys())
    )
    
    show_tables = st.sidebar.checkbox("Show Sample Tables", True)
    show_result = st.sidebar.checkbox("Show JOIN Result", True)
    
    # Main content area
    if show_tables:
        st.subheader("Sample Tables")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Table A (Employees)")
            st.dataframe(df_a, use_container_width=True)
        
        with col2:
            st.write("Table B (Salaries)")
            st.dataframe(df_b, use_container_width=True)
    
    st.markdown("---")
    
    # Visualization and Query
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Visual Representation")
        fig = create_venn_diagram(
            joins[selected_join]["sets"],
            labels=('Employees', 'Salaries'),
            title=selected_join,
            subset_colors=joins[selected_join]["colors"]
        )
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("SQL Query")
        st.code(joins[selected_join]["query"], language="sql")
        st.subheader("Description")
        st.write(joins[selected_join]["description"])
    
    if show_result:
        st.markdown("---")
        st.subheader("JOIN Result")
        result_df = execute_join(df_a, df_b, selected_join)
        st.dataframe(result_df, use_container_width=True)

    # Interactive Features
    st.markdown("---")
    with st.expander("💡 Learning Resources"):
        st.markdown("""
        ### Key Concepts
        - **Primary Key**: A unique identifier for each record (emp_id in our example)
        - **Foreign Key**: A field that links to a primary key in another table
        - **NULL values**: Represent missing or non-matching data
        
        ### Common Use Cases
        1. **INNER JOIN**: Finding employees with salary records
        2. **LEFT JOIN**: Getting all employees, even those without salaries
        3. **RIGHT JOIN**: Getting all salary records, even for departed employees
        4. **FULL JOIN**: Complete view of all employee and salary data
        
        ### Tips for Choosing JOINs
        - Use INNER JOIN when you need only complete records
        - Use LEFT/RIGHT JOIN when you need all records from one table
        - Use FULL JOIN when you need all records from both tables
        - Use WITH NULL variants to find missing or unmatched records
        """)

    with st.expander("🔍 Query Builder"):
        st.write("Build your own custom JOIN query")
        custom_join_type = st.selectbox(
            "JOIN Type",
            ["INNER", "LEFT", "RIGHT", "FULL"]
        )
        custom_condition = st.text_input(
            "JOIN Condition",
            value="A.emp_id = B.emp_id"
        )
        custom_where = st.text_input(
            "WHERE Clause (optional)",
            value=""
        )
        
        custom_query = f"""
        SELECT *
        FROM employees A
        {custom_join_type} JOIN salaries B
        ON {custom_condition}
        {f'WHERE {custom_where}' if custom_where else ''}
        """
        
        st.code(custom_query, language="sql")

if __name__ == "__main__":
    main()
