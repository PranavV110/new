import streamlit as st
import pandas as pd
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Function to load CSV data
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['publication_date'] = pd.to_datetime(df['publication_date'], format='mixed')
    df.fillna('N/A', inplace=True)
    return df

# Function to convert DataFrame to CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Function to create a hyperlink for the title
def make_clickable(title, link):
    if pd.notna(link):
        return f'<a href="{link}" target="_blank">{title}</a>'
    return title  # Return just the title if link is not available

# Function to find similar entries using cosine similarity for any column (titles/authors)
def find_similar_entries(query, column_data):
    # Create TF-IDF vectors for the column data (either titles or author names)
    vectorizer = TfidfVectorizer(stop_words='english')
    column_vectors = vectorizer.fit_transform(column_data)
    
    # Vectorize the query
    query_vector = vectorizer.transform([query])
    
    # Compute cosine similarities
    cosine_similarities = cosine_similarity(query_vector, column_vectors).flatten()
    
    # Get indices of entries with highest similarity scores
    similar_indices = cosine_similarities.argsort()[::-1]  # Sort in descending order of similarity
    
    # Get similar entries (use a threshold to filter out low similarity)
    similar_entries = [column_data.iloc[i] for i in similar_indices if cosine_similarities[i] > 0.1]
    
    return similar_entries

# Pagination function
def paginate_data(data, page, page_size):
    return data.iloc[page * page_size:(page + 1) * page_size]

# Streamlit app interface
st.sidebar.title("Enter Search Parameters")

# Specify the path to your CSV file
csv_file_path = "papers.csv"

# Load data
data = load_data(csv_file_path)
data = data[data['data_source'] != 'dblp']
data['title'] = data['title'].astype(str)

# Get min and max dates from the dataframe
min_date = data['publication_date'].min().date()
max_date = data['publication_date'].max().date()

# Set current date within the valid range
current_date = datetime.date.today()
if current_date < min_date:
    current_date = min_date
if current_date > max_date:
    current_date = max_date

# Set default end date to current date and start date to one year before
default_end_date = current_date
default_start_date = current_date - datetime.timedelta(days=365)

# Ensure the default start date is within the valid range
if default_start_date < min_date:
    default_start_date = min_date

# Date range selection with default current date
st.sidebar.write("Select date range:")
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Start date", value=default_start_date, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("End date", value=default_end_date, min_value=min_date, max_value=max_date)

# Keyword search input fields
title_keyword = st.sidebar.text_input("Enter a keyword to search in titles:")
author_keyword = st.sidebar.text_input("Enter a keyword to search in author names:")

# Checkboxes for data sources
st.sidebar.write("Select Source(s):")
data_sources = [source.strip() for source in data['data_source'].unique().tolist() if source.strip()]
selected_sources = [source for source in data_sources if st.sidebar.checkbox(source, key=f'source_{source}')]

# Checkboxes for types
st.sidebar.write("Select Type(s):")
unique_types = [t.strip() for t in data['type'].dropna().unique().tolist() if t.strip()]
selected_types_checkboxes = [t for t in unique_types if st.sidebar.checkbox(t, key=f'type_{t}')]

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state['page'] = 0

# Search button
if st.sidebar.button("Search"):
    with st.spinner('Filtering data...'):
        # Ensure publication_date is in datetime format
        data['publication_date'] = pd.to_datetime(data['publication_date'], errors='coerce')
        
        # Perform filtering
        mask = (data['publication_date'] >= pd.Timestamp(start_date)) & (data['publication_date'] <= pd.Timestamp(end_date))
        
        # Apply search using similarity for both title and author
        if title_keyword:
            # Find similar titles using cosine similarity
            similar_titles = find_similar_entries(title_keyword, data['title'])
            mask &= data['title'].isin(similar_titles)

        if author_keyword:
            # Find similar authors using cosine similarity
            similar_authors = find_similar_entries(author_keyword, data['full_name'].astype(str))
            mask &= data['full_name'].isin(similar_authors)

        if selected_sources:
            mask &= data['data_source'].isin(selected_sources)

        if selected_types_checkboxes:
            mask &= data['type'].isin(selected_types_checkboxes)

        filtered_data = data[mask]

        # Store results in session state
        st.session_state['filtered_data'] = filtered_data
        st.session_state['page'] = 0  # Reset to the first page

# Display title
st.markdown("<h1 style='text-align: center;'>Filtered Results</h1>", unsafe_allow_html=True)

# Display filtered data
if 'filtered_data' in st.session_state:
    filtered_data = st.session_state['filtered_data'].copy()

    # Make title column clickable using the link
    filtered_data['title'] = filtered_data.apply(lambda x: make_clickable(x['title'], x['link']), axis=1)

    # Clean up special characters in the DataFrame
    filtered_data.replace({r'\n': ' ', r'\r': ' '}, regex=True, inplace=True)

    filtered_data = filtered_data.astype(str)

    # Pagination controls
    page_size = 100
    total_pages = (len(filtered_data) + page_size - 1) // page_size  # Compute total pages
    page = st.session_state['page']

    paginated_data = paginate_data(filtered_data, page, page_size)

    # Remove the 'link' column
    paginated_data = paginated_data.drop(columns=['link'])

    # Convert the DataFrame to HTML and style it
    filtered_data_html = paginated_data[["full_name", "title", "publication_date", "data_source"]].to_html(index=False, escape=False)

    # Apply CSS to prioritize width for 'title' and 'full_name' columns and limit row height
    st.markdown("""
        <style>
        .dataframe {
            width: 100%;
            table-layout: auto;
            overflow-x: wrap;
            margin-left: 0px; /* Shift table slightly to the left */
        }
        .dataframe th, .dataframe td {
            white-space: normal;
            overflow: scroll;
            text-overflow: clip;
            max-width: 100px;
            max-height: 2em;
            line-height: 2em;
            padding: 0.01em;
        }
        .dataframe td:nth-child(1), .dataframe td:nth-child(2) {
            max-width: 700px;
        }
        .dataframe td:nth-child(5) {
            max-width: 100px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Render the HTML using st.markdown to ensure links are clickable
    st.markdown(filtered_data_html, unsafe_allow_html=True)

    # Display number of results on the current page and total number of filtered results
    current_page_results = len(paginated_data)
    total_results = len(filtered_data)
    start_idx = page * page_size + 1
    end_idx = start_idx + current_page_results - 1
    st.subheader(f"Showing {start_idx}-{end_idx} of {total_results} results")

    # Convert filtered data to CSV
    csv = convert_df_to_csv(filtered_data)

    # Download button on the sidebar
    st.sidebar.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )

    # Pagination controls
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Previous"):
            if st.session_state['page'] > 0:
                st.session_state['page'] -= 1
                st.rerun()
    with col2:
        if st.button("Next"):
            if st.session_state['page'] < total_pages - 1:
                st.session_state['page'] += 1
                st.rerun()

else:
    st.write("Please set your filters and press 'Search' to see the results.")