import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import numpy as np
import pandas as pd
import io

def load_sample_data():
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

def execute_join(df_a, df_b, join_type, key_a, key_b):
    if join_type == "INNER JOIN":
        return pd.merge(df_a, df_b, left_on=key_a, right_on=key_b, how='inner')
    elif join_type == "FULL JOIN":
        return pd.merge(df_a, df_b, left_on=key_a, right_on=key_b, how='outer')
    elif join_type == "FULL JOIN WITH NULLS":
        merged = pd.merge(df_a, df_b, left_on=key_a, right_on=key_b, how='outer')
        return merged[merged[df_a.columns[0]].isna() | merged[df_b.columns[0]].isna()]
    elif join_type == "LEFT JOIN":
        return pd.merge(df_a, df_b, left_on=key_a, right_on=key_b, how='left')
    elif join_type == "LEFT JOIN WITH NULL":
        merged = pd.merge(df_a, df_b, left_on=key_a, right_on=key_b, how='left')
        return merged[merged[df_b.columns[0]].isna()]
    elif join_type == "RIGHT JOIN":
        return pd.merge(df_a, df_b, left_on=key_a, right_on=key_b, how='right')
    elif join_type == "RIGHT JOIN WITH NULL":
        merged = pd.merge(df_a, df_b, left_on=key_a, right_on=key_b, how='right')
        return merged[merged[df_a.columns[0]].isna()]

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
    st.write("Upload your own datasets and explore different types of SQL JOINs")

    # Data Upload Section
    st.sidebar.title("Data Upload")
    use_sample_data = st.sidebar.checkbox("Use Sample Data", True)
    
    if use_sample_data:
        df_a, df_b = load_sample_data()
        key_a = 'emp_id'
        key_b = 'emp_id'
    else:
        st.sidebar.markdown("### Upload Your Data")
        st.sidebar.markdown("Upload CSV files for both tables")
        
        # File uploaders
        file_a = st.sidebar.file_uploader("Choose Table A (CSV)", type=['csv'])
        file_b = st.sidebar.file_uploader("Choose Table B (CSV)", type=['csv'])
        
        # Load and validate the uploaded files
        if file_a is not None and file_b is not None:
            try:
                df_a = pd.read_csv(file_a)
                df_b = pd.read_csv(file_b)
                
                # Select join keys
                st.sidebar.markdown("### Select Join Keys")
                key_a = st.sidebar.selectbox("Select key column for Table A", df_a.columns)
                key_b = st.sidebar.selectbox("Select key column for Table B", df_b.columns)
                
            except Exception as e:
                st.error(f"Error loading files: {str(e)}")
                return
        else:
            st.warning("Please upload both CSV files or use sample data")
            return

    # Define the JOIN types and their explanations
    joins = {
        "INNER JOIN": {
            "query": f"""
            SELECT *
            FROM table_a A
            INNER JOIN table_b B ON A.{key_a} = B.{key_b}
            """,
            "sets": (1, 1, 1),
            "colors": {'10': 'white', '01': 'white', '11': '#90EE90'},
            "description": "Returns only the matching records from both tables"
        },
        "FULL JOIN": {
            "query": f"""
            SELECT *
            FROM table_a A
            FULL JOIN table_b B ON A.{key_a} = B.{key_b}
            """,
            "sets": (1, 1, 1),
            "colors": {'10': '#90EE90', '01': '#90EE90', '11': '#90EE90'},
            "description": "Returns all records from both tables, matching where possible"
        },
        # ... [other JOIN definitions remain the same, just update the key references]
    }

    # Controls
    st.sidebar.title("Controls")
    selected_join = st.sidebar.selectbox(
        "Select JOIN Type",
        list(joins.keys())
    )
    
    show_tables = st.sidebar.checkbox("Show Tables", True)
    show_result = st.sidebar.checkbox("Show JOIN Result", True)

    # Display Table Information
    if show_tables:
        st.subheader("Input Tables")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Table A")
            st.write(f"Shape: {df_a.shape}")
            st.dataframe(df_a, use_container_width=True)
            st.write(f"Join Key: {key_a}")
        
        with col2:
            st.write("Table B")
            st.write(f"Shape: {df_b.shape}")
            st.dataframe(df_b, use_container_width=True)
            st.write(f"Join Key: {key_b}")

    st.markdown("---")

    # Visualization and Query
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Visual Representation")
        fig = create_venn_diagram(
            joins[selected_join]["sets"],
            labels=(f'Table A\n({len(df_a)} records)', f'Table B\n({len(df_b)} records)'),
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

    # Show JOIN Result
    if show_result:
        st.markdown("---")
        st.subheader("JOIN Result")
        result_df = execute_join(df_a, df_b, selected_join, key_a, key_b)
        st.write(f"Result Shape: {result_df.shape}")
        st.dataframe(result_df, use_container_width=True)

    # Download Results
    if show_result:
        csv = result_df.to_csv(index=False)
        st.download_button(
            label="Download JOIN Result as CSV",
            data=csv,
            file_name=f'join_result_{selected_join.lower().replace(" ", "_")}.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()
