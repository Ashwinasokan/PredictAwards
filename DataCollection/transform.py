import csv
from collections import OrderedDict
import simplejson as json

# List to hold dictionaries
awards_list = []
 
# Iterate through each row in worksheet and fetch values into dict
with open('Academy_Awards_2006.csv', 'rb') as csvfile:
	awardreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row_values in awardreader:
		award = OrderedDict()
		award['Original_Title'] = row_values[0]
		award['English_Title'] = row_values[1]
		award['Year'] = row_values[3]
		award['Country'] = row_values[4]
		award['Category'] = row_values[5]
		award['Winner?'] = row_values[6]
		award['Nominees'] = row_values[7]
		award['Academy_Awards'] = row_values[8]
		award['Item'] = row_values[9]
		awards_list.append(award)

for item in awards_list:
	print item
 
# Serialize the list of dicts to JSON
j = json.dumps(awards_list)
 
# Write to file
with open('Academy_Awards_2006.json', 'w') as f:
    f.write(j)
