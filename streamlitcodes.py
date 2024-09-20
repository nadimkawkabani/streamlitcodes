import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Electricity Distribution Across Lebanon",
    layout="wide",
    initial_sidebar_state="expanded",
)



st.title("Electricity Distribution Across Lebanon")



@st.cache_data
def load_data(path):
    """
    Load data from a CSV file.

    Parameters:
    - path (str): The file path to the CSV file.

    Returns:
    - pd.DataFrame: The loaded DataFrame.
    """
    try:
        data = pd.read_csv(path)
        return data
    except FileNotFoundError:
        st.error(f"File not found: {path}")
        return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

data_path = "https://linked.aub.edu.lb/pkgcube/data/f05a9a699ec7a1e8f8b9ae4c468e5134_20240909_161947.csv"

df = load_data(data_path)

if df is not None:
   
    if st.checkbox("Show Raw Data"):
        st.subheader("Raw Data")
        st.dataframe(df.head())

    
    df_counts = df.groupby(by=["refArea"]).size().reset_index(name="counts")

    st.subheader("Electricity Distribution Counts by Area")
    st.dataframe(df_counts)

   
    st.sidebar.header("Scatter Plot Configuration")

    min_count = int(df_counts['counts'].min())
    max_count = int(df_counts['counts'].max())

    count_range = st.sidebar.slider(
        "Select Count Range",
        min_value=min_count,
        max_value=max_count,
        value=(min_count, max_count),
        step=1,
        help="Filter areas based on the number of counts."
    )

    
    filtered_df = df_counts[
        (df_counts['counts'] >= count_range[0]) &
        (df_counts['counts'] <= count_range[1])
    ]

    st.subheader("Filtered Electricity Distribution Data")
    st.write(f"Displaying {filtered_df.shape[0]} out of {df_counts.shape[0]} areas based on the selected count range.")

    st.subheader("Scatter Plot of Electricity Distribution")

    scatter_fig = px.scatter(
        filtered_df,
        x='refArea',
        y='counts',
        size='counts',
        color='refArea',
        hover_name='refArea',
        title="Electricity Distribution Across Different Areas",
        labels={'refArea': 'Area', 'counts': 'Count'},
        template="plotly_white"
    )

    scatter_fig.update_layout(
        xaxis_title="Area",
        yaxis_title="Count",
        showlegend=False,
        height=600,
        width=1000
    )

    st.plotly_chart(scatter_fig, use_container_width=True)

   
    st.sidebar.header("Download Options")
    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.sidebar.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_electricity_distribution.csv',
        mime='text/csv',
    )
st.write("This scatter plot shows the distribution of the acceptable power grid across different Lebanese districts. We can see that there is a huge difference in distribution where Akkar district has the largest number, while Tripoly and Hermel have the lowest amount. This scatter plot proves that power grinds in Lebanon are in serious need for repair and maintenanace ")



import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# Streamlit App Configuration
# =========================


# =========================
# App Title
# =========================
st.title("Electricity Distribution Across Lebanon")

# =========================
# Data Loading
# =========================
@st.cache_data
def load_data(path):
    try:
        data = pd.read_csv(path)
        return data
    except FileNotFoundError:
        st.error(f"File not found: {path}")
        return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Update the path as per your environment
data_path = "https://linked.aub.edu.lb/pkgcube/data/f05a9a699ec7a1e8f8b9ae4c468e5134_20240909_161947.csv"
df = load_data(data_path)

if df is not None:
    # Display raw data toggle
    if st.checkbox("Show Raw Data", key="unique_key_1"):
        st.subheader("Raw Data")
        st.dataframe(df.head())

    # Display column names
    st.subheader("Dataset Overview")
    st.write("Columns in the dataset:", df.columns.tolist())

    # Identify column types
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # =========================
    # Sidebar for User Inputs
    # =========================
    st.sidebar.header("Scatter Plot Configuration")
    
    # Scatter Plot Configuration
    scatter_x = st.sidebar.selectbox(
        "Select X-axis for Scatter Plot",
        options=df.columns.tolist(),
        index=0
    )
    
    scatter_y = st.sidebar.selectbox(
        "Select Y-axis for Scatter Plot",
        options=df.columns.tolist(),
        index=1
    )
    
    scatter_color = st.sidebar.selectbox(
        "Select Color Dimension",
        options=[None] + categorical_cols,
        index=0
    )
    
    st.sidebar.header("Heatmap Configuration")
    
    # Heatmap Configuration
    heatmap_row = st.sidebar.selectbox(
        "Select Row Dimension for Heatmap",
        options=categorical_cols,
        index=0
    )
    
    heatmap_col = st.sidebar.selectbox(
        "Select Column Dimension for Heatmap",
        options=categorical_cols,
        index=1
    )
    
    heatmap_value_option = st.sidebar.selectbox(
        "Select Value for Heatmap",
        options=["Count"] + numerical_cols,
        index=0
    )

    # =========================
    # Scatter Plot Section
    # =========================
    st.subheader("Interactive Scatter Plot")

    # Handle color dimension
    color_dim = scatter_color if scatter_color else None

    # Create scatter plot using Plotly Express
    scatter_fig = px.scatter(
        df,
        x=scatter_x,
        y=scatter_y,
        color=color_dim,
        size= (df[scatter_y] if scatter_y in numerical_cols else None),
        hover_name='refArea' if 'refArea' in df.columns else None,
        title=f"Scatter Plot of {scatter_y} vs {scatter_x}",
        template="plotly_white"
    )

    # Update layout for better visuals
    scatter_fig.update_layout(
        xaxis_title=scatter_x,
        yaxis_title=scatter_y,
        legend_title= scatter_color if scatter_color else "",
        height=600,
        width=800,
    )

    # Display the scatter plot
    st.plotly_chart(scatter_fig, use_container_width=True)

    # =========================
    # Heatmap Section
    # =========================
    st.subheader("Interactive Heatmap")

    # Prepare data for heatmap
    if heatmap_value_option == "Count":
        # Group by selected dimensions and count occurrences
        heatmap_data = df.groupby([heatmap_row, heatmap_col]).size().reset_index(name='count')
        heatmap_pivot = heatmap_data.pivot_table(
            index=heatmap_row,
            columns=heatmap_col,
            values='count',
            fill_value=0
        )
        heatmap_title = f"Heatmap of Counts by {heatmap_row} and {heatmap_col}"
        z_data = heatmap_pivot.values
        color_label = "Count"
    else:
        # Aggregate based on selected numerical column
        if heatmap_value_option not in df.columns:
            st.error(f"Selected value column '{heatmap_value_option}' does not exist in the dataset.")
            z_data = None
            heatmap_pivot = None
        else:
            heatmap_data = df.groupby([heatmap_row, heatmap_col])[heatmap_value_option].sum().reset_index(name='value')
            heatmap_pivot = heatmap_data.pivot_table(
                index=heatmap_row,
                columns=heatmap_col,
                values='value',
                fill_value=0
            )
            heatmap_title = f"Heatmap of {heatmap_value_option} by {heatmap_row} and {heatmap_col}"
            z_data = heatmap_pivot.values
            color_label = heatmap_value_option

    if z_data is not None:
        # Create heatmap using Plotly Graph Objects for more customization
        heatmap_fig = go.Figure(data=go.Heatmap(
            z=z_data,
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            colorscale='Viridis',
            colorbar=dict(title=color_label),
            hoverongaps=False,
            hovertemplate=
                f"<b>{heatmap_row}</b>: %{{y}}<br>" +
                f"<b>{heatmap_col}</b>: %{{x}}<br>" +
                f"<b>{color_label}</b>: %{{z}}<extra></extra>"
        ))

        # Update layout for better visuals
        heatmap_fig.update_layout(
            title=heatmap_title,
            xaxis_title=heatmap_col,
            yaxis_title=heatmap_row,
            height=600,
            width=800,
            template="plotly_white",
            yaxis_autorange='reversed',  # Keeps the first category at the top
        )

        # Display the heatmap
        st.plotly_chart(heatmap_fig, use_container_width=True)

    # =========================
    # Optional: Download Data
    # =========================
    st.sidebar.header("Download Options")
    download_option = st.sidebar.selectbox(
        "Select Data to Download",
        options=["None", "Scatter Plot Data", "Heatmap Data"]
    )

    if download_option == "Scatter Plot Data":
        scatter_data = df[[scatter_x, scatter_y, scatter_color]].dropna()
        csv = scatter_data.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="Download Scatter Plot Data as CSV",
            data=csv,
            file_name='scatter_plot_data.csv',
            mime='text/csv',
        )
    elif download_option == "Heatmap Data":
        if heatmap_value_option == "Count":
            download_data = heatmap_data
        else:
            download_data = heatmap_data
        csv = download_data.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="Download Heatmap Data as CSV",
            data=csv,
            file_name='heatmap_data.csv',
            mime='text/csv',
        )

st.write("This heatmap shows the distribution of electricity across different Lebanese districts. We can customize the shown data by filtering it using the drop down menu to the left in order to see for example the type of power sourse, their condition, and others related to electricity distribution in Lebanon.  ")
















