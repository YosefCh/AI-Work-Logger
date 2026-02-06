import datetime
import csv
import os
from AI_Class import OpenAIClient




class WorkLog:
    def __init__(self):
        self.ai = OpenAIClient(reasoning="high") 

    def summarize_log(self, raw_log):
        summary_prompt = f"""
                    You are a formatting assistant that rewrites a daily work log into a clean, professional, plain-text format suitable for storage in a text file.

                    ### Input:
                    A rough, unstructured dictation or set of notes describing what was done during the workday.
                    Here is the work log to format:

                    {raw_log}

                    ### Output:
                    Return only the formatted text. Do not include explanations, headings, or Markdown. Do not include unicode characters that might cause errors such as this error: "UnicodeEncodeError: 'charmap' codec can't encode character '\u2192' " or other such characters.
                    Follow this structure exactly:

                    - Write each major action as a single bullet point, starting with a clear verb (e.g., "Reviewed", "Updated", "Met with").
                    - Group related details as nested bullets *only when necessary* to clarify substeps or structure (e.g., when describing a process explained by someone or a multi-part task).
                    - Remove filler, hesitation, or irrelevant personal thoughts.
                    - Keep concise but preserve meaningful technical, procedural, or context information that may be useful for future reference (e.g., systems, tools, people, report names, file paths, or concepts).
                    - Avoid over-summarizing; keep specific names of reports, folders, and systems when mentioned.
                    - End with a single closing bullet if any cleanup, final documentation, or wrap-up occurred.

                    Return only the formatted list, ready to append to a `.txt` file.
                    """.strip()

        return self.ai.get_response(summary_prompt)
        

    def write_to_text_file(self, text_log):
        
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        separator = "\n" + "*" * 40 + "\n"
        with open(r"C:\Users\yosefb\OneDrive - Lerman Enterprise\Documents\Yosef Logs\work_logs.txt", "a") as file:
            date_str = f"--- {date_str} ---"
            file.write(date_str + "\n")
            file.write(text_log + "\n")
            file.write(separator)
        print("Work log written to file.")


    def generate_key_words(self, text_log):
        keywords_prompt = f"""
                    You are a keyword extraction assistant.

                    Your task: Given a formatted daily work log (a list of bullet points), produce a concise one-line summary made up only of keywords and short phrases.

                    Guidelines:
                    - Use 5-12 concise keywords or short phrases separated by commas.
                    - Focus on main systems, projects, processes, and people mentioned (e.g., Invex, PFEP, Helpdesk, Maestro, EDI, ByRequest, Work Log Program).
                    - Do not include filler words, dates, or generic verbs (like reviewed, fixed, updated).
                    - Maintain original capitalization of system or product names.
                    - Output must fit on one line and contain no extra explanation, punctuation, or markdown — just the comma-separated keywords.

                    Return only the keyword line.

                    Here is the work log to extract keywords from: {text_log}
                    """.strip()
        print(self.ai.get_response(keywords_prompt))


        return self.ai.get_response(keywords_prompt)


    def write_to_csv(self, cleaned_text, abridged_summary):
        """
        Write work log data to CSV file with columns: Date, Full Text (Logs), Abridged
        Creates the file with headers if it doesn't exist, otherwise appends.
        """
        csv_file_path = r"C:\Users\yosefb\OneDrive - Lerman Enterprise\Documents\Yosef Logs\work_logs.csv"
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Replace newlines with space for better CSV display
        cleaned_text_single_line = cleaned_text.replace('\n', ' ').strip()
        
        # Check if file exists to determine if we need to write headers
        file_exists = os.path.isfile(csv_file_path)
        
        with open(csv_file_path, "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write headers if file is new
            if not file_exists:
                writer.writerow(["Date", "Full Text (Logs)", "Abridged"])
            
            # Write the data row
            writer.writerow([date_str, cleaned_text_single_line, abridged_summary])
        
        print("Work log written to CSV.")

    def process_log(self, raw_log):
        """
        Main function that chains all steps together:
        1. Summarize the raw log
        2. Write formatted log to text file
        3. Generate keywords
        4. Write to CSV with both formatted log and keywords
        """
        print("Step 1: Cleaning and formatting log...")
        formatted_log = self.summarize_log(raw_log)
        
        print("\nStep 2: Writing to text file...")
        self.write_to_text_file(formatted_log)
        
        print("\nStep 3: Generating keywords...")
        keywords = self.generate_key_words(formatted_log)
        
        print("\nStep 4: Writing to CSV...")
        self.write_to_csv(formatted_log, keywords)
        
        print("\n✓ All steps completed successfully!")
        return formatted_log, keywords


# if __name__ == "__main__":


              
    