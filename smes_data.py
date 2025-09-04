import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration for a wide layout
st.set_page_config(layout="wide")

# Title of the dashboard
st.title('SME Performance Dashboard')
st.markdown('### Insights and Visualizations')

# File uploader widget
st.markdown('### Upload your Excel or CSV file to get started')
uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])

# Define the required columns to validate the uploaded file
REQUIRED_COLUMNS = [
    'SME Name', 'PPT Count','Total Videos','Joining Year','Present Year','Total Videos','Total Duration' ,'Tenure (Months)', 'PPT per Month', 
    'Videos per Month', 'Duration per Month', 'Overall Performance Score'
]

# Function to normalize column names
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
    return df

if uploaded_file is not None:
    try:
        # Check file type and read the data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        
        # Clean column names to handle potential whitespace issues
        df = clean_column_names(df)

        # Check for required columns again after cleaning
        if not all(col in df.columns for col in REQUIRED_COLUMNS):
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            st.error(f"The uploaded file is missing the following required columns: {', '.join(missing_cols)}")
            st.error("Please ensure the column headers in your file exactly match the list.")
        else:
            st.success("File uploaded successfully! The dashboard is now updated with your data.")
            
            # --- Visualizations Section ---
            st.header('Key Performance Indicators (KPIs)')
            
            # Use tabs for a cleaner layout and different views
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["PPTs per Month", "Videos per Month", "Duration per Month", "Overall Score", "PPT Count Distribution"])
            
            with tab1:
                st.subheader('PPTs per Month')
                fig_ppt = px.bar(df, x='SME Name', y='PPT per Month', title='PPTs per Month for each SME',
                                 labels={'SME Name': 'SME', 'PPT per Month': 'PPTs per Month'},
                                 color='SME Name',
                                 hover_data=['PPT Count', 'Tenure (Months)'])
                st.plotly_chart(fig_ppt, use_container_width=True)
            
            with tab2:
                st.subheader('Videos per Month')
                fig_videos = px.bar(df, x='SME Name', y='Videos per Month', title='Videos per Month for each SME',
                                    labels={'SME Name': 'SME', 'Videos per Month': 'Videos per Month'},
                                    color='SME Name')
                st.plotly_chart(fig_videos, use_container_width=True)
            
            with tab3:
                st.subheader('Duration per Month')
                fig_duration = px.bar(df, x='SME Name', y='Duration per Month', title='Duration per Month for each SME',
                                      labels={'SME Name': 'SME', 'Duration per Month': 'Duration per Month (hours)'},
                                      color='SME Name')
                st.plotly_chart(fig_duration, use_container_width=True)
            
            with tab4:
                st.subheader('Overall Performance Score')
                fig_score = px.bar(df, x='SME Name', y='Overall Performance Score', title='Overall Performance Score for each SME',
                                   labels={'SME Name': 'SME', 'Overall Performance Score': 'Score'},
                                   color='SME Name')
                st.plotly_chart(fig_score, use_container_width=True)
                
            with tab5:
                st.subheader('PPT Count Contribution by SME')
                fig_pie_ppt = px.pie(df, values='PPT Count', names='SME Name', title='Percentage Contribution of PPT Count by SME',
                                     labels={'SME Name': 'SME', 'PPT Count': 'PPTs'})
                st.plotly_chart(fig_pie_ppt, use_container_width=True)
            
            # --- Individual Performance Analysis ---
            st.header('Individual SME Performance')
            st.markdown('Select an SME to view their performance metrics on a single graph.')
            
            sme_list = df['SME Name'].tolist()
            selected_sme = st.selectbox('Choose an SME', sme_list)
            
            if selected_sme:
                # Filter data for the selected SME
                individual_df = df[df['SME Name'] == selected_sme].iloc[0]
            
                # Create a DataFrame for plotting
                individual_metrics_df = pd.DataFrame({
                    'Metric': ['PPT per Month', 'Videos per Month', 'Duration per Month', 'Overall Performance Score'],
                    'Value': [
                        individual_df['PPT per Month'], 
                        individual_df['Videos per Month'],
                        individual_df['Duration per Month'], 
                        individual_df['Overall Performance Score']
                    ]
                })
            
                # Create a horizontal bar chart
                fig_individual = px.bar(individual_metrics_df, x='Value', y='Metric', orientation='h', 
                                         title=f'Performance Metrics for {selected_sme}',
                                         labels={'Value': 'Value', 'Metric': 'Performance Metric'},
                                         color='Metric',
                                         color_discrete_map={
                                             'PPT per Month': '#1f77b4', 
                                             'Videos per Month': '#ff7f0e', 
                                             'Duration per Month': '#2ca02c', 
                                             'Overall Performance Score': '#d62728'
                                         })
                st.plotly_chart(fig_individual, use_container_width=True)
            
           # --- Top Performers Ranking and Performance ---
            st.header('Top Performers Ranking and Performance')
            st.markdown('This section ranks employees with a tenure of more than 12 months based on their PPT count.')

            # Filter data for tenure > 12 months
            filtered_df = df[df['Tenure (Months)'] > 12].copy()
            
            
            # Sort the data by PPT Count to rank the performers
            ranked_df = filtered_df.sort_values(by='PPT Count', ascending=False)

                
            # Create a scatter plot to visualize the relationship between Tenure and PPT Count
            fig_scatter = px.scatter(ranked_df, 
                                         x='Tenure (Months)', 
                                         y='PPT Count',
                                         size='PPT Count',
                                         color='SME Name',
                                         hover_name='SME Name',
                                         title='PPT Count vs. Tenure for Top Performers',
                                         labels={'Tenure (Months)': 'Tenure in Months', 'PPT Count': 'PPT Count'},
                                         size_max=60)
            st.plotly_chart(fig_scatter, use_container_width=True)
            #Top 5 Performers by Overall Performance Score ---
            st.header('Top 5 Performers by Overall Performance Score')
            st.markdown('The top 5 employees with a tenure of 12 or more months, ranked by their Overall Performance Score.')
            
            # Filter for tenure >= 12 and sort by Overall Performance Score
            top_5_df = df[df['Tenure (Months)'] >= 12].sort_values(by='Overall Performance Score', ascending=False).head(5)
            
            if top_5_df.empty:
                st.info("No employees with a tenure of 12 or more months found in the dataset.")
            else:
                # Create a bar chart to visualize the top 5
                fig_top5 = px.bar(top_5_df, 
                                  x='SME Name', 
                                  y='Overall Performance Score', 
                                  color='SME Name',
                                  title='Top 5 Performers (Tenure >= 12 Months)',
                                  labels={'SME Name': 'SME', 'Overall Performance Score': 'Performance Score'},
                                  hover_data=['PPT per Month', 'Videos per Month', 'Tenure (Months)'])
                st.plotly_chart(fig_top5, use_container_width=True)
                
                # Display the data in a table
                st.table(top_5_df[['SME Name', 'Tenure (Months)', 'Overall Performance Score', 'PPT Count', 'Total Videos']])
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.error("Please ensure your uploaded file has the correct columns and data format.")
        st.info("The required columns are: 'SME Name', 'PPT Count', 'Tenure (Months)', 'PPT per Month', 'Videos per Month', 'Duration per Month', 'Overall Performance Score'")

else:
    st.info("Please upload your data file to see the visualizations.")

    