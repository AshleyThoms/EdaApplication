import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 EDA Streamlit Application")

# File uploader
uploaded_file = st.file_uploader(
    "Upload CSV or Excel file", 
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    try:
        file_name = uploaded_file.name.lower()

        # Task (a): Handle CSV & Excel
        if file_name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)

        elif file_name.endswith((".xlsx", ".xls")):
            data = pd.read_excel(uploaded_file)

        else:
            st.error("Unsupported file format")
            data = None

        if data is not None:
            st.success("File uploaded successfully!")

            # Show raw data
            st.subheader("📄 Dataset Preview")
            st.dataframe(data.head())

            # -----------------------------
            # NUMERICAL SUMMARY
            # -----------------------------
            st.subheader("📊 Numerical Summary")
            num_cols = data.select_dtypes(include=["number"])

            if not num_cols.empty:
                st.dataframe(num_cols.describe())
            else:
                st.warning("No numerical columns found")

            # -----------------------------
            # Task (b): NON-NUMERICAL SUMMARY (SAFE)
            # -----------------------------
            st.subheader("📝 Categorical Summary")
            cat_cols = data.select_dtypes(include=["object", "bool", "category"])

            if not cat_cols.empty:
                st.dataframe(cat_cols.describe())
            else:
                st.warning("No non-numerical columns found")

            # -----------------------------
            # Task (c): GRAPHS
            # -----------------------------

            st.subheader("📈 Visualizations")

            # Histogram
            if not num_cols.empty:
                st.write("### Histogram")
                column = st.selectbox("Select column for histogram", num_cols.columns)

                fig, ax = plt.subplots()
                sns.histplot(data[column], kde=True, ax=ax)
                st.pyplot(fig)

            # Boxplot
            if not num_cols.empty:
                st.write("### Boxplot")
                column_box = st.selectbox("Select column for boxplot", num_cols.columns, key="box")

                fig, ax = plt.subplots()
                sns.boxplot(x=data[column_box], ax=ax)
                st.pyplot(fig)

            # Correlation Heatmap
            if len(num_cols.columns) > 1:
                st.write("### Correlation Heatmap")

                fig, ax = plt.subplots()
                sns.heatmap(num_cols.corr(), annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)

            # Countplot (Categorical)
            if not cat_cols.empty:
                st.write("### Count Plot")
                cat_column = st.selectbox("Select categorical column", cat_cols.columns)

                fig, ax = plt.subplots()
                sns.countplot(x=data[cat_column], ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}")