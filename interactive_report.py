"""
Interactive Report Generator using Plotly
This script creates an interactive dashboard with:
- Most Upvoted Posts (top bar chart)
- Most Commented Posts (bottom bar chart)
Both charts include clickable post titles that open Reddit posts in new tabs.
"""

import sqlite3
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ===== EXTRACT DATA FROM DATABASE =====
# Connect to SQLite database containing Reddit posts
conn = sqlite3.connect('universities.db')

# Query the top 10 posts with relevant columns
# SUBSTR() truncates title to first 50 characters
# datetime() converts Unix timestamp to readable format
df = pd.read_sql_query("""
SELECT 
  SUBSTR(title, 1, 50) AS title,
  author,
  url,
  score,
  num_comments,
  ups,
  subreddit_name_prefixed,
  datetime(created_utc, 'unixepoch') AS date
FROM universities
ORDER BY score DESC
LIMIT 10
""", conn)
conn.close()

# ===== PREPARE DATA FOR VISUALIZATION =====
# Sort by ups (upvotes) in descending order (highest first)
df = df.sort_values('ups', ascending=False)

# Reverse the dataframe for proper Plotly horizontal bar display
# (Plotly draws first item at bottom, so we reverse to show highest on top)
df_plot = df.iloc[::-1].reset_index(drop=True)

# Create clickable HTML anchor tags for post titles
# Each title becomes a link that opens the Reddit post in a new tab
df_plot['title_link'] = df_plot.apply(
    lambda row: f'<a href="{row["url"]}" target="_blank">{row["title"]}</a>',
    axis=1
)

# ===== CREATE FIGURE WITH TWO SUBPLOTS =====
# Create a 2-row, 1-column subplot layout for vertical stacking
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=("Most Upvoted Posts", "Most Commented Posts"),
    specs=[[{"type": "bar"}], [{"type": "bar"}]]
)

# ===== CHART 1: MOST UPVOTED POSTS (TOP) =====
# Add horizontal bar chart for upvotes
fig.add_trace(
    go.Bar(
        y=df_plot['title_link'],  # Y-axis: clickable post titles (HTML links)
        x=df_plot['ups'],  # X-axis: number of upvotes
        orientation='h',  # Horizontal bars
        name='Upvotes',
        marker_color='steelblue',  # Blue color for upvotes
        text=df_plot['ups'],  # Show upvote count on bars
        textposition='outside',  # Place text outside bars
        customdata=df_plot[['title', 'author']],  # Data for hover display
        # Hover template shows title and author (without HTML tags)
        hovertemplate='<b>%{customdata[0]}</b><br>By: %{customdata[1]}<br>Upvotes: %{x}<extra></extra>'
    ),
    row=1, col=1
)

# ===== CHART 2: MOST COMMENTED POSTS (BOTTOM) =====
# Sort by num_comments in descending order (highest comments first)
df_comments = df.sort_values('num_comments', ascending=False)

# Reverse for proper Plotly horizontal bar display
df_comments = df_comments.iloc[::-1].reset_index(drop=True)

# Create clickable titles for comments chart
df_comments['title_link'] = df_comments.apply(
    lambda row: f'<a href="{row["url"]}" target="_blank">{row["title"]}</a>',
    axis=1
)

# Add horizontal bar chart for comments
fig.add_trace(
    go.Bar(
        y=df_comments['title_link'],  # Y-axis: clickable post titles (HTML links)
        x=df_comments['num_comments'],  # X-axis: number of comments
        orientation='h',  # Horizontal bars
        name='Comments',
        marker_color='coral',  # Coral/orange color for comments
        text=df_comments['num_comments'],  # Show comment count on bars
        textposition='outside',  # Place text outside bars
        customdata=df_comments[['title', 'author']],  # Data for hover display
        # Hover template shows title and author (without HTML tags)
        hovertemplate='<b>%{customdata[0]}</b><br>By: %{customdata[1]}<br>Comments: %{x}<extra></extra>'
    ),
    row=2, col=1
)

# ===== UPDATE AXES LABELS =====
# Set X-axis label for upvotes chart
fig.update_xaxes(title_text="No. of Upvotes", row=1, col=1)

# Set X-axis label for comments chart
fig.update_xaxes(title_text="No. of Comments", row=2, col=1)

# Set Y-axis label for both charts
fig.update_yaxes(title_text="Post Title", row=1, col=1)
fig.update_yaxes(title_text="Post Title", row=2, col=1)

# ===== GENERATE AND SAVE HTML =====
# Get the subreddit name from the first row (all rows have the same subreddit)
subreddit_name = df['subreddit_name_prefixed'].iloc[0] if len(df) > 0 else 'Reddit'

# Convert Plotly figure to HTML (full page with Plotly library from CDN)
fig_html = fig.to_html(full_html=True, include_plotlyjs='cdn')

# Enhance HTML with CSS styling for clickable links and heading
# This makes the y-axis labels (with links) properly styled and clickable
enhanced_html = fig_html.replace(
    '</head>',
    '''<style>
    .ytick a { color: #0066cc; text-decoration: underline; cursor: pointer; }
    .ytick a:hover { color: #0044aa; }
    h1 { text-align: center; color: #333; font-family: Arial, sans-serif; margin: 20px 0; }
    .back-button { 
        display: inline-block; 
        margin: 20px; 
        padding: 12px 24px; 
        background-color: #0066cc; 
        color: white; 
        text-decoration: none; 
        border-radius: 5px; 
        font-size: 14px; 
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .back-button:hover { background-color: #0044aa; }
    .header-container { text-align: center; }
    </style>
    </head>'''
)

# Insert heading with subreddit name and back button at the beginning of the body
enhanced_html = enhanced_html.replace(
    '<body>',
    f'''<body>
    <div class="header-container">
        <a href="/" class="back-button">← Back to Dashboard</a>
        <h1>Top 10 Reddit Posts for {subreddit_name}</h1>
    </div>'''
)

# Write the enhanced HTML to file
with open('interactive_report.html', 'w', encoding='utf-8') as f:
    f.write(enhanced_html)

# Print success message
# print("Interactive report saved as 'interactive_report.html' (with clickable title links)")
# print("Open the file in your browser and click titles to open posts!")
