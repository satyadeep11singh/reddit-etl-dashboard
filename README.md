# Reddit ETL Dashboard

A complete **Extract-Transform-Load (ETL) pipeline** with an interactive web dashboard to fetch Reddit posts, analyze them, and visualize data with beautiful interactive charts.

## 🚀 Try It Now!

**Live Demo**: [https://reddit-etl-dashboard.onrender.com/](https://reddit-etl-dashboard.onrender.com/)

No installation needed - just visit the link and start exploring!

## 🌟 Features

- **🌐 Web Dashboard**: User-friendly interface to control the entire pipeline
- **📊 Subreddit Selection**: Searchable dropdown with popular subreddits
- **🔄 ETL Pipeline**: Automatically extract top 100 posts from any subreddit
- **📈 Interactive Charts**: Beautiful Plotly visualizations showing:
  - Most Upvoted Posts (sorted by upvotes)
  - Most Commented Posts (sorted by comments)
- **🔗 Clickable Links**: Click post titles directly in charts to open Reddit posts
- **💾 SQLite Database**: Persistent storage of all post data
- **🎯 Real-time Status**: Live feedback on ETL and report generation progress

## 📋 Project Structure

```
reddit-etl-dashboard/
├── app.py                      # Flask web server & API endpoints
├── etl.py                      # Extract-Transform-Load pipeline
├── subreddit.py                # Fetch popular subreddits list
├── interactive_report.py       # Generate interactive Plotly charts
├── index.html                  # Web dashboard interface
├── subreddits.json            # Cached list of popular subreddits
├── universities.db            # SQLite database (auto-created)
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/reddit-etl-dashboard.git
   cd reddit-etl-dashboard
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install requests pandas plotly flask sqlalchemy
   ```

3. **Run the Flask server**
   ```bash
   python app.py
   ```
   
   Server starts at: `http://localhost:5000`

4. **Open in browser**
   - Navigate to `http://localhost:5000`
   - Select a subreddit from the dropdown
   - Click "Run ETL" to fetch posts
   - Click "Generate Report" to view interactive charts

## 📖 How It Works

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/1f009521-9786-4c5d-83b6-b2e61a8f5e5b" />


### 1. **Extract** (subreddit.py & etl.py)
- Fetches top 100 posts from the past year
- Uses Reddit's public JSON API
- Includes: title, author, upvotes, comments, URL, score, etc.

### 2. **Transform** (etl.py)
- Cleans and structures Reddit API data
- Selects relevant columns
- Removes duplicates

### 3. **Load** (etl.py)
- Stores data in SQLite database (universities.db)
- Replaces existing data with fresh data
- Enables quick access for reporting

### 4. **Visualize** (interactive_report.py)
- Queries top 10 posts from database
- Creates two interactive Plotly bar charts
- Generates clickable HTML report
- Shows post title, author, and engagement metrics

## 🎮 Usage

### From Web Dashboard
1. **Select Subreddit**: Type in search box to find subreddit
2. **View Details**: See subscriber count and subreddit title
3. **Run ETL**: Fetch latest posts from selected subreddit
4. **Generate Report**: Create interactive visualization
5. **View Charts**: Click titles to open posts on Reddit

⚠️ **Important**: When you click "Generate Report", your browser may block the popup window. **Allow popups** in your browser to view the interactive report. Check for popup notifications in your browser's address bar.

### From Terminal
```bash
# Run ETL for specific subreddit
python etl.py r/India

# Generate report
python interactive_report.py

# Fetch subreddit list
python subreddit.py
```

## 📊 Data Collected

For each post, the system captures:
- **id**: Unique Reddit post ID
- **title**: Post title (truncated to 50 chars in charts)
- **author**: Username of post creator
- **score**: Total upvote score
- **ups**: Number of upvotes
- **downs**: Number of downvotes
- **num_comments**: Comment count
- **upvote_ratio**: Ratio of upvotes to downvotes
- **url**: Direct link to post
- **permalink**: Reddit post URL
- **created_utc**: Post creation timestamp
- **subreddit_name_prefixed**: Subreddit name (e.g., r/India)

## 🛠️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve dashboard (index.html) |
| GET | `/interactive_report.html` | Serve interactive report |
| GET | `/get-subreddits` | Get list of popular subreddits |
| POST | `/run-etl` | Trigger ETL pipeline |
| POST | `/run-report` | Generate interactive report |

## 📝 Example API Requests

### Get Subreddits
```bash
curl http://localhost:5000/get-subreddits
```

### Run ETL
```bash
curl -X POST http://localhost:5000/run-etl \
  -H "Content-Type: application/json" \
  -d '{"subreddit": "r/India", "title": "India"}'
```

### Generate Report
```bash
curl -X POST http://localhost:5000/run-report
```

## 🔧 Configuration

### Modify ETL Limits
Edit `etl.py` to change the number of posts fetched:
```python
url = f"https://www.reddit.com/r/{subreddit}/top.json?limit=100&t=year"
# Change limit=100 to desired number
```

### Change Report Post Count
Edit `interactive_report.py`:
```python
LIMIT 10  # Change to show more/fewer posts in charts
```

## 📦 Dependencies

- **requests**: HTTP library for Reddit API calls
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualization library
- **flask**: Web framework for dashboard
- **sqlalchemy**: Database ORM
- **sqlite3**: Built-in database (no installation needed)

## 🤝 Contributing

Feel free to fork this project and submit pull requests with improvements!

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

- This project uses Reddit's public API with standard user-agent headers
- Respect Reddit's terms of service and rate limiting
- This is for educational and personal use

## 🐛 Troubleshooting

### Port 5000 Already in Use
```bash
# Change port in app.py
app.run(host='localhost', port=5001, debug=False)
```

### Database Not Found
The database is auto-created on first ETL run. Make sure you have write permissions in the project directory.

### No Posts Displayed
- Check internet connection (fetches from Reddit)
- Verify subreddit name is correct
- Wait 30+ seconds for ETL to complete

## 📞 Questions?

For issues or questions, open an issue on GitHub or contact the project maintainer.

---

**Happy analyzing! 🚀**
