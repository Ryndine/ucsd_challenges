import csv

election_csv = R'Resources\election_data.csv'

with open(election_csv, 'r') as csvfile:
    votes = csv.reader(csvfile, delimiter=",")
    next(votes)
    cvrs = [v for v in votes]

results = {}
total_votes = len(cvrs)
winner = {'name': None, 'votes': 0}

for cvr in cvrs:
    candidate = cvr[2]

    if candidate not in results:
        results[candidate] = {'total': 0, 'percentage': 0.0}
    
    results[candidate]['total'] += 1
    
with open('analysis\\results.txt', 'w+') as f:
    header = f"""Election Results
{'-'*30}
Total Votes: {total_votes}
{'-'*30}
"""
    f.write(header)
    print(header)

    for k, v in results.items():
        if results[k]['total'] > winner['votes']:
            winner['name'] = k
            winner['votes'] = results[k]['total']

        results[k]['percentage'] = v['total']/total_votes
        p = v['percentage']
        output = f"""{k}: {(str(round(p*100, ndigits=2))+'00')[:6]}% ({v['total']})
"""
        f.write(output)
        print(output)
    winner = f"""{'-'*30}
Winner: {winner['name']}
{'-'*30}
"""
    f.write(winner)
    print(winner)


