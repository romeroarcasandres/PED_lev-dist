# Post Edit Distance (based on Levenshtein distance)

The **PED_lev-dist.py** script compares two columns in a CSV file by computing a similarity score based on the raw Levenshtein distance. The tool visually highlights the differences between corresponding cells in an HTML report and also appends the computed score to the CSV file for further analysis.

---

## Overview

The script prompts the users to:
- **Load a CSV file:** Select a CSV file via a file dialog.
- **Select Columns:** Choose two columns from the CSV file to compare.
- **Compute Similarity Score:** For each row, calculate a similarity score using the raw Levenshtein distance, normalized so that identical strings receive a score of 100, with lower scores indicating more differences.
- **Generate Diff Report:** Create an HTML report that visually displays the differences between the selected columns using the `diff_match_patch` library.
- **Export Results:** Save the modified CSV file with an additional column containing the similarity score.

---

## Requirements

- **Python 3**
- **Libraries:**
  - `pandas`
  - `difflib`
  - `diff_match_patch`
  - `tkinter` (standard with Python)
  - `Levenshtein` (Install via `pip install python-Levenshtein`)

---

## Files

- `PED_lev-dist.py`
- Capture1.JPG, Capture2.JPG and Capture3.JPG for reference

---

## Usage

1. **Run the Script:**
   - Execute the `compare_csv_columns.py` script.
2. **Select a CSV File:**
   - A file dialog will prompt you to choose the CSV file you wish to process.
3. **Choose Columns:**
   - The script displays all available columns and prompts you to select the two columns you want to compare.
4. **Provide Report Name:**
   - Enter a name for the HTML report (without extension).
5. **Processing:**
   - The script computes a similarity score for each row based on the normalized raw Levenshtein distance.
   - An HTML diff report is generated to visually highlight differences.
6. **Save Modified CSV:**
   - You will be prompted to select a location to save the updated CSV file that includes the computed similarity scores.
7. **View Report:**
   - Open the generated HTML report to review detailed differences and scores.

---

## Important Notes

- **Normalization Approach:**  
  The similarity score is derived by normalizing the raw Levenshtein distance against the length of the longer string. This ensures a fair comparison regardless of string length.
  
- **Columns correspondance**  
  The tool assumes that rows in both columns correspond to each other.

- **Large files**
  Very large CSV files might require significant processing time and memory. Consider splitting the CSV into smaller chunks.
---

## License

This project is available under the CC BY-NC 4.0 license. For complete details, please refer to the LICENSE file included with this project.
