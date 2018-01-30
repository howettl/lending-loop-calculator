#!/usr/bin/env python

from os import path
from argparse import ArgumentParser
from csv import reader
from datetime import datetime

def is_valid_file(parser, arg):
	if not path.isfile(arg):
		parser.error('The file %s does not exist' % arg)
	else:
		return arg

def main():
	"""Main function"""
	parser = ArgumentParser(description='Calculate the date on which you should be able to make your next Lending Loop commitment.')
	parser.add_argument('--portfolio_path', '-p', help='Path to the exported portfolio file in .csv format', metavar='FILE', type=lambda x: is_valid_file(parser, x), required=True)
	args = parser.parse_args()

	current_balance = raw_input('Please enter your current Lending Loop balance (ie. 2.13), or type q to quit: ')
	if current_balance is None or current_balance == '' or current_balance == 'q':
		exit(1)
	current_balance = float(current_balance)

	all_payments = []

	with open(args.portfolio_path, 'rb') as csv_file:
		csv_reader = reader(csv_file, delimiter=',')
		all_payments = [x for x in csv_reader if x and x[-1] == 'Scheduled']

	all_payments = sorted(all_payments, key=lambda payment: payment[-3])

	for row in all_payments:
		payment_amount = float(row[-8])
		payment_date = datetime.strptime(row[-3].translate(None, ':-'), '%Y%m%d').strftime("%d %B %Y")
		current_balance = current_balance + payment_amount
		if current_balance >= float(25.0):
			print 'You will have enough balance available to commit to another loan on %s' % payment_date
			exit(0)

	print 'You do not have enough payments scheduled to reach the loan commitment threshold.'
	exit(0)

if __name__ == '__main__':
	main()