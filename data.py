import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Set Streamlit page configuration
st.set_page_config(page_title="Data Visualization Tool", layout="wide")

# App title
st.title("📊 Data Visualization Tool")
st.markdown("Upload a dataset to generate insightful visualizations effortlessly!")

# File uploader
uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Load dataset
    file_extension = uploaded_file.name.split(".")[-1]
    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # Show dataset preview
    st.subheader("Dataset Preview")
    st.dataframe(df.head())
    
    # Show dataset statistics
    st.subheader("Dataset Summary")
    st.write(df.describe())
    
    # Allow user to select columns for visualization
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Sidebar options
    st.sidebar.header("Visualization Settings")
    chart_type = st.sidebar.selectbox("Select Chart Type", ["Auto", "Scatter", "Histogram", "Boxplot", "Pie", "Correlation Matrix"])
    
    if chart_type == "Auto":
        if len(numerical_cols) >= 2:
            st.subheader("Scatter Plot (Auto-Generated)")
            fig = px.scatter(df, x=numerical_cols[0], y=numerical_cols[1], color=df[categorical_cols[0]] if categorical_cols else None)
            st.plotly_chart(fig)
        elif len(numerical_cols) == 1:
            st.subheader("Histogram (Auto-Generated)")
            fig = px.histogram(df, x=numerical_cols[0])
            st.plotly_chart(fig)
    else:
        if chart_type == "Scatter":
            x_axis = st.sidebar.selectbox("Select X-Axis", numerical_cols)
            y_axis = st.sidebar.selectbox("Select Y-Axis", numerical_cols)
            fig = px.scatter(df, x=x_axis, y=y_axis, color=df[categorical_cols[0]] if categorical_cols else None)
            st.plotly_chart(fig)
        
        elif chart_type == "Histogram":
            column = st.sidebar.selectbox("Select Column", numerical_cols)
            fig = px.histogram(df, x=column)
            st.plotly_chart(fig)
        
        elif chart_type == "Boxplot":
            column = st.sidebar.selectbox("Select Column", numerical_cols)
            fig = px.box(df, y=column, color=df[categorical_cols[0]] if categorical_cols else None)
            st.plotly_chart(fig)
        
        elif chart_type == "Pie":
            if categorical_cols:
                column = st.sidebar.selectbox("Select Category", categorical_cols)
                fig = px.pie(df, names=column)
                st.plotly_chart(fig)
            else:
                st.warning("No categorical columns available for pie chart.")
        
        elif chart_type == "Correlation Matrix":
            st.subheader("Correlation Matrix")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit")
