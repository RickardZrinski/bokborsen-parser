from bs4 import BeautifulSoup, element
import csv
import re

# For conversion of <label>(s) into suitable dict keys
label_conversions = {
	'Beställning nr': 'order_nr',
	'Lagd': 'order_date',
	'Kategori': 'category',
	'Annons-id': 'ad_id',
	'Författare,Artist..': 'author-artist-etc',
	'Titel': 'title',
	'Pris': 'price'
}

# Returns a dictionary with <label> and <span> values
def get_label_value_pairs(tag):
	pairs = {}

	label_tags = tag.find_all('label')
	value_tags = tag.find_all('span')

	for idx, label_tag in enumerate(label_tags):

		# Convert <label>(s) into suitable dict keys
		label_converted = label_conversions[label_tag.string]

		if value_tags[idx].string is not None:
			pairs[label_converted] = value_tags[idx].string
		else:
			pairs[label_converted] = ''

	return pairs

# Parses and writes bokborsen.se book orders list to CSV file
def parse_html():

	# Read HTML file
	with open('orders.html', 'r', encoding='iso-8859-1') as f:
		html = f.read()

	# Initialize BS
	soup = BeautifulSoup(html, 'html.parser')

	# Find orders table
	orders = soup.find(class_='compact')

	# Open orders.csv for writing orders to
	with open('orders.csv', 'w', newline='') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',')

		# Loop through each order
		for order in orders.children:
			if type(order) == element.Tag:
				left_data = get_label_value_pairs(order.contents[0])
				right_data = get_label_value_pairs(order.contents[2])

				# Join data together into one dictionary
				data = {**left_data, **right_data}

				# Write order to CSV file
				csv_writer.writerow([
					data['order_date'],
					data['ad_id'],
					data['author-artist-etc'],
					data['title']
				])

	print('Done.')
	input('Press enter to exit.')

if __name__ == '__main__':
	parse_html()