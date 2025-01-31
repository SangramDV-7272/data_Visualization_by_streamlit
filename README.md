# data_Visualization_by_streamlit

# Movie Ratings Dashboard

## Description

This project aims to create an interactive dashboard for analyzing movie ratings using Streamlit. The dashboard provides insights into the distribution of ratings by genres and years, popular genres by user demographics, and correlations between genres, user activity, and ratings. The data is loaded and processed using optimized data types and Dask for enhanced performance.

## Features

- Load and preprocess movie ratings, user demographics, and movie information data.
- Extract year from movie titles and split genres into individual rows.
- Merge datasets to create a comprehensive DataFrame for analysis.
- Visualize the distribution of ratings by genres and years using various plots.
- Analyze popular genres by user demographics.
- Create heatmaps to show correlations between genres, user activity, and ratings.

## Data Files

The dataset consists of three files:

1. **ratings.dat**:
   - Contains user ratings for movies.
   - Format: `UserID::MovieID::Rating::Timestamp`
   - Example: `1::1193::5::978300760`

2. **users.dat**:
   - Contains user demographic information.
   - Format: `UserID::Gender::Age::Occupation::Zip-code`
   - Example: `1::F::1::10::48067`

3. **movies.dat**:
   - Contains movie information.
   - Format: `MovieID::Title::Genres`
   - Example: `1::Toy Story (1995)::Animation|Children's|Comedy`
