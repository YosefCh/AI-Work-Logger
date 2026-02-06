"""
Work Log Query Module
Provides clean query interface for work log CSV data using DuckDB
"""

import duckdb
import pandas as pd
from AI_Class import OpenAIClient
from IPython.display import display, Markdown, HTML
import time


class WorkLogQuery:
    """
    Query interface for work logs stored in CSV format.
    
    Provides two query methods:
    1. Direct SQL queries
    2. Natural language queries (AI-powered)
    """
    
    def __init__(self, csv_path='work_logs.csv'):
        """
        Initialize the query interface.
        
        Args:
            csv_path (str): Path to the work logs CSV file
        """
        self.csv_path = csv_path
        self.ai = OpenAIClient()
        self.backup_ai = OpenAIClient(model_name="gpt-4.1-mini")
    
    def run_sql_query(self, sql_query):
        """
        Execute a direct SQL query on the work logs.
        
        Args:
            sql_query (str): SQL query string (use 'work_logs' as table name)
        
        Returns:
            pandas.DataFrame: Query results
        """
        con = duckdb.connect()
        
        # Replace work_logs reference with actual CSV path
        query_with_table = sql_query.replace('work_logs', f"'{self.csv_path}'")
        result = con.execute(query_with_table).fetchdf()
        con.close()
        
        self._display_results(result)
        return result
    
    def run_natural_language_query(self, question):
        """
        Execute a natural language query using AI to convert to SQL.
        
        Args:
            question (str): Question in plain English
        
        Returns:
            pandas.DataFrame: Query results or None if query invalid
        """
        display(Markdown(f"**Your question:** {question}"))
        print('Generating SQL query...')
        time.sleep(1)
        
        # Get sample data for context
        con = duckdb.connect()
        sample_data = con.execute(f"SELECT * FROM '{self.csv_path}' LIMIT 3").fetchdf()
        
        # Build AI context
        context = f"""I have a work log system that stores daily work entries in a CSV file.
Convert the user's natural language question into a DuckDB-compatible SQL query.

The table is accessed as '{self.csv_path}' and has these columns:
- Date: The date of the work log (format: YYYY-MM-DD)
- Full_Text: The complete work log entry text
- Abridged: A summary/keywords from the log

Sample data:
{sample_data.to_string()}

Rules:
- Query MUST be DuckDB-compatible SQL syntax
- Use ILIKE for case-insensitive text searches
- Use % wildcards for partial matches
- For date filtering, use Date >= 'YYYY-MM-DD' format
- Always use '{self.csv_path}' as the table name (keep the quotes)
- Return only the SQL query, no explanations or backticks
- If the question is incoherent, respond with "Invalid Query."

User question: {question}
"""
        
        # Generate SQL with AI
        sql_query = self.ai.get_response(context)
        
        # Fallback to backup model if needed
        if sql_query.startswith("An error occurred"):
            sql_query = self.backup_ai.get_response(context)
        
        # Check if query is valid
        if sql_query == "Invalid Query.":
            display(Markdown("### ⚠️ Unable to generate a valid query. Please rephrase your question."))
            con.close()
            return None
        
        # Display generated query
        display(Markdown(f"**Generated SQL:**\n```sql\n{sql_query}\n```"))
        time.sleep(0.5)
        
        # Execute query
        try:
            result = con.execute(sql_query).fetchdf()
            con.close()
            self._display_results(result, table_id="nl_results")
            return result
        except Exception as e:
            display(Markdown(f"### ❌ Error executing query:\n```\n{e}\n```"))
            con.close()
            return None
    
    def _display_results(self, result, table_id="query_results"):
        """
        Display query results in a formatted HTML table.
        
        Args:
            result (pandas.DataFrame): Query results
            table_id (str): HTML element ID for the table
        """
        # Create scrollable HTML table
        html_table = result.to_html(escape=False, table_id=table_id)
        
        # Add CSS for scrolling and better formatting (works in both light and dark mode)
        scrollable_html = f"""
        <style>
        #{table_id} {{
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid rgb(110, 140, 210);
            font-family: monospace;
            background-color: rgb(220, 230, 220);
            color: black;
        }}
        #{table_id} th {{
            background-color: rgb(100, 100, 100);
            color: white;
            position: sticky;
            top: 0;
            z-index: 10;
            font-weight: bold;
        }}
        #{table_id} td, #{table_id} th {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid var(--jp-border-color2, #ccc);
        }}
        
        #{table_id} tr:nth-child(even) {{
            background-color: rgb(220, 255, 255);
        }}
        </style>
        <div>
        <h4>Query Results ({len(result)} rows)</h4>
        {html_table}
        </div>
        """
        display(HTML(scrollable_html))
    
    def generate_summary(self, time_period_or_query):
        """
        Generate a narrative summary of work logs for a given time period or query.
        
        This method uses a two-step approach:
        1. LLM generates SQL query based on the request
        2. Query results are fed back to LLM for summarization
        
        Args:
            time_period_or_query (str): Natural language description like:
                - "last week"
                - "January 2026"
                - "when I worked on Plex"
                - "help desk activities"
        
        Returns:
            str: Formatted summary text
        """
        display(Markdown(f"**Summary request:** {time_period_or_query}"))
        print('Step 1: Generating query to retrieve relevant logs...')
        time.sleep(0.5)
        
        # Step 1: Generate SQL query
        con = duckdb.connect()
        sample_data = con.execute(f"SELECT * FROM '{self.csv_path}' LIMIT 3").fetchdf()
        
        query_gen_prompt = f"""I have a work log system that stores daily work entries in a CSV file.
Generate a DuckDB-compatible SQL query to retrieve the relevant work logs for creating a summary.

The table is accessed as '{self.csv_path}' and has these columns:
- Date: The date of the work log (format: YYYY-MM-DD)
- Full_Text: The complete work log entry text
- Abridged: A summary/keywords from the log

Sample data:
{sample_data.to_string()}

Rules:
- Query MUST be DuckDB-compatible SQL syntax
- For time periods like "last week", calculate the date range (today is {pd.Timestamp.now().strftime('%Y-%m-%d')})
- Use ILIKE for case-insensitive text searches with % wildcards
- Return ALL relevant columns (Date, Full_Text, Abridged)
- Order by Date DESC for chronological summaries
- Always use '{self.csv_path}' as the table name (keep the quotes)
- Return ONLY the SQL query, no explanations

User request: {time_period_or_query}
"""
        
        sql_query = self.ai.get_response(query_gen_prompt)
        if sql_query.startswith("An error occurred"):
            sql_query = self.backup_ai.get_response(query_gen_prompt)
        
        # Clean the SQL query - remove markdown code fences and extra whitespace
        sql_query = sql_query.strip()
        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        elif sql_query.startswith("```"):
            sql_query = sql_query.replace("```", "").strip()
        
        display(Markdown(f"**Generated query:**\n```sql\n{sql_query}\n```"))
        print('Step 2: Executing query...')
        time.sleep(0.5)
        
        # Step 2: Execute query
        try:
            result = con.execute(sql_query).fetchdf()
            con.close()
            
            if result.empty:
                display(Markdown("### ⚠️ No matching logs found for this time period/query."))
                return None
            
            display(Markdown(f"**Retrieved {len(result)} log entries**"))
            print('Step 3: Generating summary...')
            time.sleep(0.5)
            
        except Exception as e:
            display(Markdown(f"### ❌ Error executing query:\n```\n{e}\n```"))
            con.close()
            return None
        
        # Step 3: Generate summary from results
        summary_prompt = f"""You are a professional work summary assistant.

**IMPORTANT:** The user's specific request was: "{time_period_or_query}"

The work log data below may contain entries covering multiple topics. Your task is to:
- FOCUS ONLY on content related to the user's request: "{time_period_or_query}"
- IGNORE or minimize unrelated work from those same days
- Extract and summarize only the relevant portions that match the user's request
- Organize into logical categories (Projects, Systems Work, Support/Help Desk, Learning/Training, Administrative)
- Highlight completed deliverables related to the topic
- Note ongoing work and blockers related to the topic
- Mention key collaborators
- Uses bullet points for readability
- Is suitable for sharing with a manager

Work log data ({len(result)} entries from {result['Date'].min()} to {result['Date'].max()}):

{result.to_string()}

Remember: Filter your summary to focus ONLY on "{time_period_or_query}" - ignore other unrelated work from these days.

Generate a professional summary in markdown format with headers and bullets.
"""
        
        summary = self.ai.get_response(summary_prompt)
        if summary.startswith("An error occurred"):
            summary = self.backup_ai.get_response(summary_prompt)
        
        # Display the summary
        display(Markdown("---"))
        display(Markdown("# 📋 Work Summary"))
        display(Markdown(summary))
        
        return summary
    
    def ask_question(self, question):
        """
        Answer a specific analytical question about work logs.
        
        This method uses a two-step approach:
        1. LLM generates SQL query based on the question
        2. Query results are analyzed to answer the specific question
        
        Args:
            question (str): Specific question about work logs like:
                - "Has this person been doing good work over the past 3 weeks?"
                - "What happened with the Invex report when the API issue came up?"
                - "How much time was spent on help desk vs projects?"
                - "Rate this employee's performance from 1-5"
        
        Returns:
            str: Detailed answer to the question
        """
        display(Markdown(f"**Question:** {question}"))
        print('Step 1: Generating query to retrieve relevant data...')
        time.sleep(0.5)
        
        # Step 1: Generate SQL query
        con = duckdb.connect()
        sample_data = con.execute(f"SELECT * FROM '{self.csv_path}' LIMIT 3").fetchdf()
        
        query_gen_prompt = f"""I have a work log system that stores daily work entries in a CSV file.
Generate a DuckDB-compatible SQL query to retrieve the relevant work logs needed to answer the user's question.

The table is accessed as '{self.csv_path}' and has these columns:
- Date: The date of the work log (format: YYYY-MM-DD)
- Full_Text: The complete work log entry text
- Abridged: A summary/keywords from the log

Sample data:
{sample_data.to_string()}

Rules:
- Query MUST be DuckDB-compatible SQL syntax
- For time periods like "past 3 weeks", calculate the date range (today is {pd.Timestamp.now().strftime('%Y-%m-%d')})
- Use ILIKE for case-insensitive text searches with % wildcards
- Return ALL relevant columns (Date, Full_Text, Abridged)
- Order by Date DESC for chronological context
- Always use '{self.csv_path}' as the table name (keep the quotes)
- Return ONLY the SQL query, no explanations

User question: {question}
"""
        
        sql_query = self.ai.get_response(query_gen_prompt)
        if sql_query.startswith("An error occurred"):
            sql_query = self.backup_ai.get_response(query_gen_prompt)
        
        # Clean the SQL query - remove markdown code fences
        sql_query = sql_query.strip()
        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        elif sql_query.startswith("```"):
            sql_query = sql_query.replace("```", "").strip()
        
        display(Markdown(f"**Generated query:**\n```sql\n{sql_query}\n```"))
        print('Step 2: Executing query...')
        time.sleep(0.5)
        
        # Step 2: Execute query
        try:
            result = con.execute(sql_query).fetchdf()
            con.close()
            
            if result.empty:
                display(Markdown("### ⚠️ No matching logs found to answer this question."))
                return None
            
            display(Markdown(f"**Retrieved {len(result)} log entries**"))
            print('Step 3: Analyzing data to answer your question...')
            time.sleep(0.5)
            
        except Exception as e:
            display(Markdown(f"### ❌ Error executing query:\n```\n{e}\n```"))
            con.close()
            return None
        
        # Step 3: Answer the question based on results
        answer_prompt = f"""You are an analytical assistant answering specific questions about work log data.

**User's Question:** {question}

**Work Log Data:** ({len(result)} entries from {result['Date'].min()} to {result['Date'].max()})

{result.to_string()}

**Context:**
- Help desk coverage is mandatory one day per week - this is a required part of the job, not a negative

**Instructions:**
- Answer the SPECIFIC question asked - do not create a general summary
- Be direct and analytical
- Provide evidence from the logs to support your answer
- If asked for a rating or evaluation, provide it with clear justification
- If asked about specific events or issues, trace them chronologically
- Use bullet points for clarity when listing evidence
- Be concise but thorough

Answer the question now:
"""
        
        answer = self.ai.get_response(answer_prompt)
        if answer.startswith("An error occurred"):
            answer = self.backup_ai.get_response(answer_prompt)
        
        # Display the answer
        display(Markdown("---"))
        display(Markdown("# 💡 Answer"))
        display(Markdown(answer))
        
        return answer
