"""
Python Extract Transform Load (ETL) Example
This script fetches Reddit posts from a specified subreddit, 
transforms the data, and loads it into a SQLite database.
"""

import requests
import pandas as pd
from sqlalchemy import create_engine
import sys

def extract_data(subreddit='r/India', title='')-> dict:
    """
    Extract data from Reddit's public API.
    
    Args:
        subreddit (str): Subreddit name to fetch posts from (with or without 'r/' prefix)
        title (str): Subreddit title (for logging purposes)
    
    Returns:
        tuple: (list of post data, subreddit title)
    """
    # Remove 'r/' prefix if it exists to normalize the subreddit name
    if subreddit.startswith('r/'):
        subreddit = subreddit[2:]
    
    # Construct Reddit API URL to fetch top 100 posts from the past year
    url = f"https://www.reddit.com/r/{subreddit}/top.json?limit=100&t=year"
    
    # Set User-Agent header (required by Reddit API)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Make HTTP request to Reddit API
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Extract the nested posts list from the API response and return with title
    return data['data']['children'], title

def transform_data(data: dict) -> pd.DataFrame:
    """
    Transform extracted Reddit API data into a clean pandas DataFrame.
    
    Args:
        data (list): Raw post data from Reddit API
    
    Returns:
        pd.DataFrame: Cleaned dataframe with selected columns
    """
    # Convert list of post objects into a DataFrame
    df = pd.DataFrame([item['data'] for item in data])
    
    # Select only the relevant columns we need for analysis
    df = df[['id','score', 'ups', 'downs', 'upvote_ratio','num_comments', 'title', 'author', 'permalink','subreddit_name_prefixed', 'url','created_utc']]
    return df

def load_data(df: pd.DataFrame) -> None:
    """
    Load transformed data into SQLite database.
    
    Args:
        df (pd.DataFrame): DataFrame to load into database
    """
    # Create SQLAlchemy engine for SQLite database connection
    engine = create_engine('sqlite:///posts.db')
    
    # Write DataFrame to 'posts' table, replacing existing data
    df.to_sql('posts', engine, if_exists='replace', index=False)

if __name__ == "__main__":
    # Get subreddit name from command line argument (default: 'r/India')
    subreddit = sys.argv[1] if len(sys.argv) > 1 else 'r/India'
    
    # Get subreddit title from command line argument (optional)
    title = sys.argv[2] if len(sys.argv) > 2 else ''
    
    # EXTRACT: Fetch posts from Reddit API
    data, subreddit_title = extract_data(subreddit, title)
    
    # TRANSFORM: Clean and structure the data
    df = transform_data(data)
    
    # LOAD: Save data to SQLite database
    load_data(df)
    
    # Print success message with subreddit info
    message = f"ETL process completed successfully for {subreddit}!"
    if subreddit_title:
        message += f" ({subreddit_title})"
    print(message) 
