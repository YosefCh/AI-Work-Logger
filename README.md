# 📋 Work Log Management System

An AI-powered work log system that captures, organizes, and analyzes your daily activities.
Speak naturally to record what you’ve done, what you’re working on, and what’s next and create a living log that remembers context, progress, and answers any question or query about your work.


## 🌟 Features

### Log Entry & Processing
- **AI-Powered Formatting**: Converts rough dictations or notes into clean, professional bullet-point logs
- **Automatic Keyword Extraction**: Generates concise keyword summaries for quick reference
- **Dual Storage**: Saves logs in both human-readable text format and queryable CSV format
- **Interactive Dashboard**: Jupyter notebook interface for easy log entry

### Analytics & Querying
- **SQL Queries**: Direct SQL queries on your work logs using DuckDB
- **Natural Language Queries**: Ask questions in plain English, automatically converted to SQL
- **AI-Powered Summaries**: Generate narrative summaries for any time period or topic
- **Analytical Q&A**: Get specific answers about your work patterns and productivity

## 📁 Project Structure

- work_logs.py - Core WorkLog class for processing entries
- duckdb_example.py - WorkLogQuery class for analytics
- work_log_entry_dashborard.ipynb - Interactive entry interface
- work_log_analytics.ipynb - Analytics and query interface
- AI_Class.py - OpenAI client wrapper
- work_logs.csv - Structured log storage
- work_logs.txt - Archive text logs
- config.json - API configuration

## 🚀 Setup

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository or download the files

2. Install required packages:
   - pip install openai duckdb pandas ipython

3. Configure API credentials:
   - Copy config.example.json to config.json
   - Add your OpenAI API key to config.json

## 💡 Usage

### Entering Work Logs

You’ll get the most value by *__dictating__* your updates (Ctrl + H on Windows) throughout the day or at day’s end. No overthinking and no heavy typing, just __*speak naturally*__ as you finish tasks or wrap up projects, and let the system handle the rest.
Your day's work will be:
   - Cleaned and formatted
   - Saved to a <code>.txt</code> file for readability
   - Saved to a <code>.csv</code> file to function as a database for the query and analyze tool


### Analyzing Work Logs

Open work_log_analytics.ipynb and use one of three methods:

#### 1. Direct SQL Queries
Execute SQL queries directly on your work logs. 

Example queries:
- SELECT * FROM work_logs WHERE Full_Text ILIKE '%helpdesk%' ORDER BY Date DESC
- SELECT Date, Abridged FROM work_logs WHERE Date >= '2026-01-01'
- SELECT * FROM work_logs WHERE Full_Text ILIKE '%Plex%' OR Full_Text ILIKE '%Fabric%'

#### 2. Natural Language Queries
Ask questions in plain English - the system converts them to SQL automatically.

Example questions:
- "Show me all work related to Plex from the last month"
- "What did I work on last week?"
- "Find logs mentioning Maestro or EDI"
- "Show me logs from January 2026"

#### 3. Generate Summaries
Create executive summaries for any time period or topic.

Example requests:
- "Summarize last week"
- "All work from January 2026"
- "Everything related to Plex or Fabric"
- "Help desk activities"
- "Work with Invex API"

#### 4. Ask Analytical Questions
Get specific answers, evaluations, and ratings about work performance.

Example questions:
- "Has this person been doing good work over the past 3 weeks?"
- "Rate this employee's performance from 1-5"
- "What happened with the Invex report when the API issue came up?"
- "How much time was spent on help desk vs projects?"
- "What are the key accomplishments this month?"

## 🗂️ Data Schema

### CSV Format (work_logs.csv)
- Date: Date of work log (YYYY-MM-DD)
- Full_Text: Complete formatted work log
- Abridged: Keyword summary for quick reference

## 🎯 Use Cases

- **Daily Standups**: Quickly summarize what you worked on
- **Performance Reviews**: Generate comprehensive work summaries for any time period
- **Time Tracking**: Analyze how time is distributed across projects
- **Knowledge Retrieval**: Find when you worked on specific systems or projects
- **Team Communication**: Create professional summaries for managers

## 🔧 Customization

### Adjust AI Models
Edit the reasoning level or model in work_logs.py or duckdb_example.py by modifying the OpenAIClient initialization

## ⚙️ Technical Details

- **AI Processing**: Uses OpenAI GPT models for text formatting and analysis
- **Database**: DuckDB for SQL queries (no installation required)
- **Storage**: CSV format for portability and easy querying
- **Interface**: Jupyter notebooks for interactive use

## 📝 License

This project is under the __Affero General Public License (AGPL)__

## 🤝 Contributing

Feel free to fork and adapt to your needs. Common enhancements:
- Add data visualization
- Export to different formats
- Integrate with time tracking tools
- Add team collaboration features

