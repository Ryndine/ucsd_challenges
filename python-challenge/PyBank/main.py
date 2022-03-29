import csv

budget_csv = R'Resources\budget_data.csv'

with open(budget_csv, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=",")
    next(csv_reader)
    rows = [d for d in csv_reader]
    
changes = []
totals = 0
months = len(rows)

with open('analysis\\results.txt', 'w+') as f:
    for i in range(len(rows)):
        this_row = rows[i]
        totals += int(this_row[1])
        if i == len(rows)-1:
            break
        next_row = rows[i+1]
        change = int(next_row[1]) - int(this_row[1])
        changes.append(change)

    minch = min(changes)
    maxch = max(changes)
    minrow = changes.index(minch)
    maxrow = changes.index(maxch)
    average = round(sum(changes)/len(changes), 2)

    output = f"""Financial Anaysis
{'-'*30}
Total Months: {months}
Total: ${totals}
Average  Change: ${average}
Greatest Increase in Profits: {rows[maxrow+1][0]} (${maxch})
Greatest Decrease in Profits: {rows[minrow+1][0]} (${minch})
"""

    print(output)
    f.write(output)
