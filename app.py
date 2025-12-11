"""
Flask Web Application for Reddit ETL Dashboard
Provides REST API endpoints to:
- Serve the HTML dashboard
- Fetch list of popular subreddits
- Trigger ETL pipeline to extract Reddit posts
- Trigger report generation with interactive visualizations
"""

from flask import Flask, jsonify, send_file, request
import subprocess
import os
import json

# Initialize Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """
    Serve the main dashboard HTML page.
    
    Returns:
        HTML file: index.html (the dashboard interface)
    """
    return send_file('index.html')

@app.route('/interactive_report.html')
def report():
    """
    Serve the interactive Plotly report.
    
    Returns:
        HTML file: interactive_report.html (the visualization report)
    """
    return send_file('interactive_report.html')

@app.route('/get-subreddits', methods=['GET'])
def get_subreddits():
    """
    Fetch and return list of popular subreddits.
    This endpoint:
    1. Runs subreddit.py to fetch latest subreddit data from Reddit
    2. Loads the cached subreddit list from subreddits.json
    3. Returns JSON array of subreddit objects with name, subscribers, and title
    
    Returns:
        JSON: List of subreddits [{'name': 'r/...', 'subscribers': int, 'title': str}, ...]
        or 400 error if file not found
    """
    try:
        # Run subreddit.py to fetch the latest subreddit list from Reddit API
        result = subprocess.run(['python', 'subreddit.py'], capture_output=True, text=True, timeout=30)
        
        # Load the cached subreddits from the JSON file that subreddit.py creates
        if os.path.exists('subreddits.json'):
            with open('subreddits.json', 'r') as f:
                subreddits = json.load(f)
            return jsonify(subreddits)
        else:
            return jsonify([]), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/run-etl', methods=['POST'])
def run_etl():
    """
    Trigger the ETL pipeline to extract posts from selected subreddit.
    
    Request JSON body:
        {'subreddit': 'r/SubredditName', 'title': 'Subreddit Title'}
    
    This endpoint:
    1. Extracts the subreddit name and title from POST request
    2. Runs etl.py as a subprocess with these parameters
    3. Returns success/error status
    
    Returns:
        JSON: {'status': 'success', 'message': '...'} on success
        or {'status': 'error', 'error': '...'} on failure (400 status code)
    """
    try:
        # Parse JSON request body
        data = request.get_json()
        
        # Extract subreddit name (default to 'r/India' if not provided)
        subreddit = data.get('subreddit', 'r/India') if data else 'r/India'
        
        # Extract subreddit title (optional)
        title = data.get('title', '') if data else ''
        
        # Execute etl.py as a subprocess, passing subreddit name and title as arguments
        result = subprocess.run(['python', 'etl.py', subreddit, title], capture_output=True, text=True, timeout=60)
        
        # Check if subprocess executed successfully (return code 0 = success)
        if result.returncode == 0:
            return jsonify({'status': 'success', 'message': 'ETL completed'})
        else:
            # Return error output from subprocess
            return jsonify({'status': 'error', 'error': result.stderr}), 400
    except subprocess.TimeoutExpired:
        return jsonify({'status': 'error', 'error': 'Timeout'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 400

@app.route('/run-report', methods=['POST'])
def run_report():
    """
    Trigger interactive report generation with Plotly visualizations.
    
    This endpoint:
    1. Runs interactive_report.py as a subprocess
    2. Generates interactive bar charts showing top posts by upvotes and comments
    3. Creates interactive_report.html with clickable post links
    
    Returns:
        JSON: {'status': 'success', 'message': '...'} on success
        or {'status': 'error', 'error': '...'} on failure (400 status code)
    """
    try:
        # Execute interactive_report.py as a subprocess
        result = subprocess.run(['python', 'interactive_report.py'], capture_output=True, text=True, timeout=60)
        
        # Check if subprocess executed successfully
        if result.returncode == 0:
            return jsonify({'status': 'success', 'message': 'Report generated'})
        else:
            # Return error output from subprocess
            return jsonify({'status': 'error', 'error': result.stderr}), 400
    except subprocess.TimeoutExpired:
        return jsonify({'status': 'error', 'error': 'Timeout'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 400

# Entry point: Start Flask web server
if __name__ == '__main__':
    # Start Flask server on localhost:5000
    # debug=False for production (set to True for development with auto-reload)
    app.run(host='localhost', port=5000, debug=False)
