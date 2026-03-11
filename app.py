import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Global Disease Data Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #000000;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .plot-container {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Helper Functions
def load_data(file):
    try:
        df = pd.read_csv(file)
        # Required columns check
        required_columns = ['date', 'country', 'cases', 'deaths', 'recovered']
        if not all(col in df.columns for col in required_columns):
            st.error(f"Missing required columns. Please ensure the CSV has: {', '.join(required_columns)}")
            return None
        
        # Data Cleaning
        df = df.dropna()
        df['date'] = pd.to_datetime(df['date'])
        
        # Ensure numeric types
        for col in ['cases', 'deaths', 'recovered']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def main():
    st.title("🧬 Global Disease Data Dashboard")
    st.markdown("---")

    # SIDEBAR
    st.sidebar.header("📁 Data Management")
    uploaded_file = st.sidebar.file_uploader("Upload Disease CSV", type=["csv"])
    
    # Use sample data if no file is uploaded
    if uploaded_file is not None:
        df = load_data(uploaded_file)
    else:
        st.sidebar.info("Currently using sample data. Upload a CSV to visualize your own data.")
        df = load_data("sample_data.csv")

    if df is not None:
        # INTERACTIVE FILTERS
        st.sidebar.header("🔍 Filters")
        
        # Country Selector
        countries = sorted(df['country'].unique())
        selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries)
        
        # Date Range Selector
        min_date = df['date'].min().to_pydatetime()
        max_date = df['date'].max().to_pydatetime()
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        # Apply Filters
        filtered_df = df[df['country'].isin(selected_countries)]
        if len(date_range) == 2:
            start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
            filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

        # METRICS CALCULATIONS
        total_cases = filtered_df['cases'].sum()
        total_deaths = filtered_df['deaths'].sum()
        total_recovered = filtered_df['recovered'].sum()
        mortality_rate = (total_deaths / total_cases * 100) if total_cases > 0 else 0

        # DISPLAY METRICS
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Cases", f"{total_cases:,}")
        with col2:
            st.metric("Total Deaths", f"{total_deaths:,}")
        with col3:
            st.metric("Total Recovered", f"{total_recovered:,}")
        with col4:
            st.metric("Mortality Rate", f"{mortality_rate:.2f}%")

        st.markdown("---")

        # VISUALIZATIONS
        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            st.subheader("📈 Case Trends Over Time")
            # Group by date for line chart
            daily_data = filtered_df.groupby('date')[['cases', 'deaths', 'recovered']].sum().reset_index()
            fig_line = px.line(daily_data, x='date', y='cases', 
                               title='Cumulative Cases Evolution',
                               template='plotly_white',
                               line_shape='spline',
                               color_discrete_sequence=['#3366cc'])
            st.plotly_chart(fig_line, use_container_width=True)

        with row1_col2:
            st.subheader("🌍 Total Cases by Country")
            country_data = filtered_df.groupby('country')['cases'].sum().reset_index().sort_values('cases', ascending=False)
            fig_bar = px.bar(country_data, x='country', y='cases', 
                             title='Distribution by Country',
                             color='cases',
                             color_continuous_scale='Blues')
            st.plotly_chart(fig_bar, use_container_width=True)

        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            st.subheader("⚖️ Death vs Recovery Distribution")
            distribution_data = pd.DataFrame({
                'Status': ['Deaths', 'Recovered'],
                'Count': [total_deaths, total_recovered]
            })
            fig_pie = px.pie(distribution_data, values='Count', names='Status', 
                             title='Patient Outcomes',
                             color_discrete_sequence=['#ef553b', '#00cc96'],
                             hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)

        with row2_col2:
            st.subheader("🆕 Daily New Cases")
            daily_data['new_cases'] = daily_data['cases'].diff().fillna(0)
            fig_trend = px.area(daily_data, x='date', y='new_cases', 
                                title='Daily New Infections Trend',
                                color_discrete_sequence=['#ab63fa'])
            st.plotly_chart(fig_trend, use_container_width=True)

        # Data Preview
        with st.expander("📋 View Raw Data Summary"):
            st.dataframe(filtered_df.head(100), use_container_width=True)

    else:
        st.warning("Please upload a valid CSV file to get started.")

if __name__ == "__main__":
    main()
