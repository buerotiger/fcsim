#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import simulation

def simuliereKredit():
	kredit = {
		'monthlyAnnuity': 3233.0,
		'yearlyDefaultRate': 0.0435,
		'principal': 100000.0,
		'id': '8148',
		'term': 3.0,
		'riskClass': 'C',
		'yearlyInterestRate': 0.1013
	}
	
	# berechne Renditen und Ausfallwahrscheinlichkeiten für den Kredit
	result1 = simulation.calcLoan(kredit, customParams = {"recoveryRate": 0.5, "recoveryLength": 18, "capitalGainsTax": 0.26375})

	# erhöhe Ausfallwahrscheinlichkeit um 2 Prozentpunkte	
	kredit["yearlyDefaultRate"] += 0.02

	# berechne Renditen und Ausfallwahrscheinlichkeiten für den Kredit
	# (mit der erhöhten Ausfallwahrscheinlichkeit)
	result2 = simulation.calcLoan(kredit, customParams = {"recoveryRate": 0.5, "recoveryLength": 18, "capitalGainsTax": 0.26375})

	pprint.pprint(result1)
	pprint.pprint(result2)
	
	print("IRR1: %5.2f%%" % (result1["result"]["meanIRR"]*100.))
	print("IRR2: %5.2f%%" % (result2["result"]["meanIRR"]*100.))
	
if __name__ == '__main__':
	simuliereKredit()
