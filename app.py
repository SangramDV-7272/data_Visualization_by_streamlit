import streamlit as st
import dask.dataframe as dd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data with optimized data types and use blocksize to enhance performance
dtype_ratings = {'UserID': 'int32', 'MovieID': 'int32', 'Rating': 'int8', 'Timestamp': 'int32'}
dtype_users = {'UserID': 'int32', 'Gender': 'category', 'Age': 'int8', 'Occupation': 'int8', 'Zip-code': 'category'}
dtype_movies = {'MovieID': 'int32', 'Title': 'object', 'Genres': 'object'}

ratings = dd.read_csv('d:/for practice/ml-1m/ratings.dat', delimiter='::', engine='python', 
                      names=['UserID', 'MovieID', 'Rating', 'Timestamp'], encoding='latin-1', dtype=dtype_ratings, blocksize=None)
users = dd.read_csv('d:/for practice/ml-1m/users.dat', delimiter='::', engine='python', 
                    names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], encoding='latin-1', dtype=dtype_users, blocksize=None)
movies = dd.read_csv('d:/for practice/ml-1m/movies.dat', delimiter='::', engine='python', 
                     names=['MovieID', 'Title', 'Genres'], encoding='latin-1', dtype=dtype_movies, blocksize=None)

# Drop missing values in all datasets
ratings = ratings.dropna()
users = users.dropna()
movies = movies.dropna()

# Extract year from movie titles and convert to int16 in a single step
movies['Year'] = movies['Title'].str.extract(r'\((\d{4})\)')[0].astype('int16')
movies = movies.dropna(subset=['Year'])

# Split genres into a list and expand into multiple rows efficiently
movies = movies.assign(Genres=movies['Genres'].str.split('|')).explode('Genres')

# Merge datasets lazily to avoid redundant computations
merged_df = ratings.merge(users, on='UserID', how='inner').merge(movies, on='MovieID', how='inner')

# Apply mappings in one step
age_groups = {1: 'Under 18', 18: '18-24', 25: '25-34', 35: '35-44', 45: '45-49', 50: '50-55', 56: '56+'}
profession_dict = {0: "other or not specified", 1: "academic/educator", 2: "artist", 3: "clerical/admin", 
                   4: "college/grad student", 5: "customer service", 6: "doctor/health care", 7: "executive/managerial", 
                   8: "farmer", 9: "homemaker", 10: "K-12 student", 11: "lawyer", 12: "programmer", 
                   13: "retired", 14: "sales/marketing", 15: "scientist", 16: "self-employed", 
                   17: "technician/engineer", 18: "tradesman/craftsman", 19: "unemployed", 20: "writer"}

merged_df = merged_df.assign(AgeGroup=merged_df['Age'].map(age_groups), 
                             Occupation=merged_df['Occupation'].map(profession_dict))

# Compute final dataframe from Dask
merged_df = merged_df.compute()

# Streamlit application interface
st.title('Movie Ratings Dashboard')

option = st.selectbox('Select Visualization', [
    'Distribution of Ratings by Genres and Years',
    'Popular Genres by Gender',
    'Count of Ratings by Genre and Age Group',
    'Popular Genres by Occupation',
    'Heatmap Showing the Correlation Between Genres, User Activity, and Ratings'
])

# Generate selected visualization
if option == 'Distribution of Ratings by Genres and Years':
    st.header('Distribution of Ratings by Genres and Years')
    fig, ax = plt.subplots(figsize=(20, 8))
    sns.histplot(data=merged_df, x='Year', hue='Genres', multiple='stack', kde=True, ax=ax)
    st.pyplot(fig)

elif option == 'Popular Genres by Gender':
    st.header('Popular Genres by Gender')
    fig, ax = plt.subplots(figsize=(20, 8))
    sns.countplot(data=merged_df, x='Genres', hue='Gender', ax=ax)
    st.pyplot(fig)

elif option == 'Count of Ratings by Genre and Age Group':
    st.header('Count of Ratings by Genre and Age Group')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(data=merged_df, x='Genres', hue='AgeGroup', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif option == 'Popular Genres by Occupation':
    st.header('Popular Genres by Occupation')
    fig, ax = plt.subplots(figsize=(20, 8))
    sns.countplot(data=merged_df, x='Genres', hue='Occupation', ax=ax)
    st.pyplot(fig)

elif option == 'Heatmap Showing the Correlation Between Genres, User Activity, and Ratings':
    st.header('Heatmap Showing the Correlation Between Genres, User Activity, and Ratings')
    pivot_table = merged_df.pivot_table(index='Genres', columns='Occupation', values='Rating', aggfunc='mean')
    fig, ax = plt.subplots(figsize=(20, 8))
    sns.heatmap(pivot_table, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
