import os
import pandas as pd
import difflib
import diff_match_patch as dmp_module
from tkinter import Tk, filedialog, simpledialog

import Levenshtein

# Function to calculate the similarity score based on the raw Levenshtein distance.
# It normalizes the raw distance so that if the strings are identical the score is 100,
# and if they are very different the score will be closer to 0.
def calculate_levenshtein_score(str1, str2):
    # If both strings are empty, consider them identical
    if not str1 and not str2:
        return 100.0
    # Calculate the raw Levenshtein distance
    raw_distance = Levenshtein.distance(str1, str2)
    # Normalize the distance using the length of the longer string
    max_len = max(len(str1), len(str2))
    similarity = 1 - (raw_distance / max_len)
    # Multiply by 100 to convert to a percentage-like score
    return similarity * 100

# Function to calculate weights based on the length of the segments
def calculate_weight(str1, str2):
    return len(str1) + len(str2)

# Function to generate HTML report of differences with row-level Levenshtein scores
def generate_html_report(dmp, filename, col1_data, col2_data, diffs_list, score_column, report_name, header1, header2):
    html_report = [
        f'''
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                pre {{
                    white-space: pre-wrap; /* Allows wrapping of long lines */
                    word-wrap: break-word; /* Breaks long lines within the 'pre' tag */
                }}
            </style>
        </head>
        <body>
            <h2>Comparison Report for: {filename}</h2>
            <table>
                <tr>
                    <th>Index</th>
                    <th>{header1}</th>
                    <th>{header2}</th>
                    <th>Differences</th>
                    <th>Score</th>
                </tr>
        '''
    ]

    for i, (data1, data2, diff_html, score) in enumerate(zip(col1_data, col2_data, diffs_list, score_column)):
        html_report.append(f'<tr><td>{i + 1}</td><td>{data1}</td><td>{data2}</td><td><pre>{diff_html}</pre></td><td>{score:.2f}</td></tr>')

    html_report.append('''
        </table>
        </body>
        </html>
    ''')

    with open(f'{report_name}.html', 'w') as f:
        f.write('\n'.join(html_report))

    print(f"HTML diff report generated: {report_name}.html")

# Main function for comparison
def compare_columns_in_csv():
    # Prompt user to select a CSV file
    Tk().withdraw()
    print("Please select a CSV file.")
    csv_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not csv_file:
        print("No file selected. Exiting.")
        return
    
    # Load CSV into pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Display available columns and prompt user to select two columns
    print("Available columns:")
    for i, col in enumerate(df.columns):
        print(f"{i + 1}: {col}")
    
    col1_index = int(simpledialog.askstring("Column 1", "Select the first column index (e.g., 1, 2, ...): ")) - 1
    col2_index = int(simpledialog.askstring("Column 2", "Select the second column index (e.g., 1, 2, ...): ")) - 1
    
    col1 = df.columns[col1_index]
    col2 = df.columns[col2_index]
    
    # Get the report name from the user
    report_name = simpledialog.askstring("Report Name", "Enter the name for the HTML report (without extension): ")
    
    # Initialize diff_match_patch and lists to store results
    dmp = dmp_module.diff_match_patch()
    diffs_list = []
    score_column = []
    
    col1_data = df[col1].astype(str).tolist()
    col2_data = df[col2].astype(str).tolist()

    for val1, val2 in zip(col1_data, col2_data):
        str1 = str(val1) if pd.notna(val1) else ""
        str2 = str(val2) if pd.notna(val2) else ""

        # Calculate score using the normalized raw Levenshtein distance approach
        score = calculate_levenshtein_score(str1, str2)
        score_column.append(score)

        # Generate HTML diff using diff_match_patch
        diffs = dmp.diff_main(str1, str2)
        dmp.diff_cleanupSemantic(diffs)
        diff_html = dmp.diff_prettyHtml(diffs)
        diffs_list.append(diff_html)

    # Add the row-level score to the dataframe as a new column
    df[f"Score ({col1} vs {col2})"] = score_column

    # Prompt user to save the modified CSV with the score results
    print("Please select where to save the modified CSV file.")
    save_csv = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    df.to_csv(save_csv, index=False)
    print(f"Modified CSV saved: {save_csv}")

    # Generate the HTML report with differences and row-level scores
    generate_html_report(dmp, csv_file, col1_data, col2_data, diffs_list, score_column, report_name, col1, col2)

# Execute the script
if __name__ == "__main__":
    compare_columns_in_csv()
