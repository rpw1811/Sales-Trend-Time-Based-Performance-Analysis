AFFICIONADO COFFEE ROASTERS Sales Trend and Time-Based Performance
Analysis ================================================

PROJECT OVERVIEW

This project analyzes transaction-level sales data for Afficionado
Coffee Roasters. The analysis focuses on hourly revenue patterns,
comparisons between store locations, and product-category performance. A
Streamlit dashboard presents the results through interactive metrics,
charts, filters, and a store-by-hour revenue heatmap.

PROJECT OBJECTIVES

-   Calculate revenue from transaction quantity and unit price.
-   Explore revenue patterns by hour of day.
-   Compare revenue across store locations.
-   Examine sales performance by product category.
-   Present findings through an interactive dashboard.
-   Provide evidence-based recommendations while stating data
    limitations.

TOOLS AND TECHNOLOGIES

-   Python
-   Pandas
-   Streamlit
-   Plotly, Matplotlib, and Seaborn (where used in the project)
-   Google Colab / Jupyter Notebook

SUGGESTED PROJECT STRUCTURE

Afficionado-Coffee-Roasters/ |– app.py |– requirements.txt |– README.txt
|– data/ | |– original_dataset.xlsx | |– cleaned_data.csv | |–
summary_files/ |– notebooks/ | |– sales_analysis.ipynb |– reports/ | |–
final_research_paper.docx | |– executive_summary.docx |– screenshots/ |–
dashboard_overview.png |– hourly_sales_analysis.png |–
store_by_hour_heatmap.png

This is a suggested structure. Use the actual filenames and folders in
your repository; do not include files that you have not created.

HOW TO RUN THE STREAMLIT DASHBOARD

Prerequisites: - Install Python. - Keep app.py, requirements.txt, and
all data files referenced by app.py available in the project folder.

Steps: 1. Open a terminal or Command Prompt in the folder containing
app.py. 2. Install the required packages:

python -m pip install -r requirements.txt

3.  Start the dashboard:

    streamlit run app.py

4.  Open the local address shown in the terminal, usually:

    http://localhost:8501

5.  Keep the terminal open while using the dashboard. Press Ctrl+C in
    the terminal to stop the application.

DATA AND METRIC NOTES

Revenue is calculated as:

    Revenue = transaction_qty * unit_price

The analysis reports revenue, quantity sold, transaction-record count,
and average revenue per record.

A transaction record is a row in the dataset. It should not
automatically be interpreted as a unique customer or visit unless the
dataset’s transaction grain confirms that interpretation.

IMPORTANT DATA LIMITATIONS

The available dataset does not contain a transaction_date field.
Therefore, this project does not claim to analyze daily, weekly,
weekday/weekend, monthly, or seasonal sales trends. The time-based
analysis is limited to the available hour-of-day information.

Revenue is not the same as profit. Profitability conclusions require
cost and margin data.

KEY ANALYSIS AREAS

-   Hourly revenue analysis
-   Store-level revenue comparison
-   Store-by-hour revenue heatmap
-   Product-category revenue analysis
-   Executive overview of key sales metrics

REPOSITORY CONTENTS

Include the files that are part of your completed submission, such as: -
Streamlit dashboard source code (app.py) - requirements.txt - Analysis
notebook - Dataset or permitted cleaned/sample data - Research paper and
executive summary - Dashboard screenshots or demonstration video

DATA SHARING

Only upload data that you are permitted to share. If the source dataset
is subject to restrictions, provide instructions for obtaining it rather
than publishing it publicly.

AUTHOR

Completed as a data analytics learning project.

DISCLAIMER

The findings describe the supplied dataset and its available fields.
Business recommendations should be validated with additional operational
information before being used to make staffing, purchasing, or financial
decisions.
