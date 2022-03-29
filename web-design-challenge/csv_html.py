import os
import pandas as pd

csv_path = "Resources/cities.csv"
read_csv = pd.read_csv(csv_path)
csv_html = read_csv.to_html('table.html', index=False, classes=['table', 'table-striped', 'table-hover'])