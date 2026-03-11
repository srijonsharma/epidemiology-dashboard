# Global Disease Data Dashboard 🧬

A powerful, interactive dashboard built with **Python**, **Streamlit**, and **Plotly** to visualize and analyze infectious disease datasets.

## Features
- **File Upload**: Support for custom CSV datasets.
- **Data Cleaning**: Automatic handling of missing values and data types.
- **Key Metrics**: Real-time calculation of Total Cases, Deaths, Recovered, and Mortality Rate.
- **Interactive Visualizations**:
  - Line charts for cumulative trends.
  - Bar charts for regional analysis.
  - Pie charts for outcome distribution.
  - Area charts for daily new cases.
- **Filters**: Filter data by country and date range.

## Required Dataset Format
The CSV should contain the following columns:
- `date` (YYYY-MM-DD)
- `country`
- `cases`
- `deaths`
- `recovered`

## Installation

1. Clone or download the project.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Execute the following command in your terminal:
```bash
streamlit run app.py
```

## Sample Data
A `sample_data.csv` file is included to help you get started immediately.
