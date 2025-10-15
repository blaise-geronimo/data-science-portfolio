# ==============================================================================
# Reach Report Consolidator
#
# This script consolidates multiple Monthly or Weekly Reach Reports by Product
# or Brand into a single CSV file. It uses Tkinter for a simple GUI interface.
#
# Author: Blaise Geronimo
# Date: 07-10-25
# ==============================================================================

import os
import sys
import glob
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# ------------------------------------------------------------------------------
# Define file patterns for each combination of level (monthly/weekly)
# and category (product/brand)
# ------------------------------------------------------------------------------
PATTERNS = {
    ("monthly", "product"): "*Monthly Reach Report by Product*.xls",
    ("weekly", "product"): "*Weekly Reach Report by Product*.xls",
    ("monthly", "brand"): "*Monthly Reach Report by Brand*.xls",
    ("weekly", "brand"): "*Weekly Reach Report by Brand*.xls",
}

def consolidate(level, category, input_dir, output_dir):
    """
    Consolidate multiple Excel reach reports into a single CSV file.

    Parameters:
        level (str): 'monthly' or 'weekly'
        category (str): 'product' or 'brand'
        input_dir (str): folder containing input files
        output_dir (str): folder where output CSV will be saved

    Returns:
        str: summary of consolidation results
    """

    # determine file matching pattern
    key = (level.lower(), category.lower())
    if key not in PATTERNS:
        return f"Unknown combination: {key}"

    pattern = PATTERNS[key]

    # get list of matching files
    files = glob.glob(os.path.join(input_dir, pattern))
    if not files:
        return f"No files found matching pattern '{pattern}' in {input_dir}."

    dfs = []          # list to collect all dataframes
    error_files = []  # list to keep filenames that fail to read

    for f in files:
        try:  # load the Excel file and its second sheet
            xls = pd.ExcelFile(f, engine="xlrd")
            sheet = xls.sheet_names[1]  # we assume the second sheet contains the data
            temp = pd.read_excel(f, sheet_name=sheet, header=None, engine="xlrd")

            try:  # extract Year value from cell A2 (row 1 index-based)
                year_val = int(temp.iat[1, 0])
            except Exception:
                year_val = None  # fallback if value is missing or invalid

            # detect header row (where any column equals "Market")
            is_market = temp.astype(str).apply(
                lambda col: col.str.strip().str.lower() == "market"
            )
            mask = is_market.any(axis=1)
            if not mask.any():
                # skip file if no header row found
                continue

            header_row = mask.idxmax()
            temp.columns = temp.iloc[header_row].tolist()  # set header
            df = temp.iloc[header_row + 1:].reset_index(drop=True)  # actual data below header

            # standardize 'Month' column name
            month_candidates = [c for c in df.columns
                                if str(c).strip().lower().startswith("month")]
            if month_candidates:
                month_col = month_candidates[0]
                df = df.rename(columns={month_col: "Month"})
            else:
                month_col = None  # unlikely, but handle missing Month column

            # insert 'Year' column after 'Month' if available, else at the end
            if month_col or "Month" in df.columns:
                idx = df.columns.get_loc("Month")
                df.insert(idx + 1, "Year", year_val)
            else:
                df["Year"] = year_val

            dfs.append(df)

        except Exception:
            # Record file that caused error, continue processing others
            error_files.append(os.path.basename(f))

    # build return message summarising results
    lines = []

    if dfs:
        # concatenate all dataframes and export as CSV
        outname = f"{level.capitalize()} Reach by {category.capitalize()}.csv"
        outpath = os.path.join(output_dir, outname)
        try:
            pd.concat(dfs, ignore_index=True).to_csv(outpath, index=False)
            lines.append(f"✔ Written: {outpath}")
        except Exception as e:
            lines.append(f"✘ error writing output → {e}")
    else:
        lines.append(f"No valid data for {level} {category}.")

    # list files that failed to process
    if error_files:
        lines.append("Files with errors:")
        for fn in error_files:
            lines.append(f'✘ error reading file: "{fn}"')

    return "\n".join(lines)

# ==============================================================================
# Tkinter GUI Application
# ==============================================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reach Report Consolidator")
        self.resizable(False, False)

        # Tkinter variables
        self.level = tk.StringVar(value="monthly")
        self.category = tk.StringVar(value="product")
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()

        # --- UI Layout ---

        # Period selection
        level_frame = tk.LabelFrame(self, text="Select Period")
        level_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Radiobutton(level_frame, text="Monthly", variable=self.level, value="monthly").pack(anchor="w")
        tk.Radiobutton(level_frame, text="Weekly", variable=self.level, value="weekly").pack(anchor="w")

        # Category selection
        cat_frame = tk.LabelFrame(self, text="Select Category")
        cat_frame.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        tk.Radiobutton(cat_frame, text="Product", variable=self.category, value="product").pack(anchor="w")
        tk.Radiobutton(cat_frame, text="Brand", variable=self.category, value="brand").pack(anchor="w")

        # Input directory
        tk.Label(self, text="Input Directory:").grid(row=1, column=0, padx=10, sticky="e")
        tk.Entry(self, textvariable=self.input_dir, width=40).grid(row=1, column=1, padx=10)
        tk.Button(self, text="Browse...", command=self.browse_input).grid(row=1, column=2, padx=5)

        # Output directory
        tk.Label(self, text="Output Directory:").grid(row=2, column=0, padx=10, sticky="e")
        tk.Entry(self, textvariable=self.output_dir, width=40).grid(row=2, column=1, padx=10)
        tk.Button(self, text="Browse...", command=self.browse_output).grid(row=2, column=2, padx=5)

        # Run button
        tk.Button(self, text="Run Consolidation", command=self.run).grid(row=3, column=1, pady=10)

    def browse_input(self):
        """Open file dialog to select input directory."""
        directory = filedialog.askdirectory(title="Select Input Directory")
        if directory:
            self.input_dir.set(directory)

    def browse_output(self):
        """Open file dialog to select output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)

    def show_result(self, result):
        """Display result in a custom Toplevel window with left-justified text."""
        win = tk.Toplevel(self)
        win.title("Consolidation Result")
        tk.Label(win, text="Consolidation Result", font=("Arial", 12, "bold")).pack(pady=(10, 0))
        text = tk.Text(win, wrap="word", width=80, height=20)
        text.insert("1.0", result)
        text.config(state="disabled")  # make it read-only
        text.pack(padx=10, pady=10)
        tk.Button(win, text="Close", command=win.destroy).pack(pady=(0, 10))

    def run(self):
        """Run consolidation process and display result."""
        in_dir = self.input_dir.get().strip()
        out_dir = self.output_dir.get().strip()
        if not os.path.isdir(in_dir) or not os.path.isdir(out_dir):
            messagebox.showerror("Error", "Please select valid input and output directories.")
            return

        result = consolidate(self.level.get(), self.category.get(), in_dir, out_dir)
        self.show_result(result)

# ==============================================================================
# Main execution
# ==============================================================================
if __name__ == "__main__":
    app = App()
    app.mainloop()