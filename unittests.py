#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import unittest
from scipy.optimize import minimize

import simulation

class TestSimulation(unittest.TestCase):

	def test_calcMonthlyDefaultRate(self):
		# Berechne die monatliche Ausfallrate für eine gegebene
		# jährliche Ausfallrate hilfsweise über die Variation
		# der monatlichen Ausfallrate in der Formel
		# sum(p_monatlich*(1-p_monatlich)**n, n=0..11) = p_jaehrlich.
		def calcMonthlyDefaultRate2(yearlyDefaultRate):
			from scipy.optimize import minimize
			def fu(prob):
				ret = yearlyDefaultRate
				for i in range(12):
					ret -= prob*pow(1-prob,i)
				return abs(ret)
			tmpResult = minimize(fu, [yearlyDefaultRate/12.], method = "SLSQP", bounds=((-0.99, 0.99),) )
			return tmpResult["x"][0]

		for prob in [0.00, 0.01, 0.02, 0.03, 0.05, 0.1, 0.5]:
			self.assertAlmostEqual(simulation.calcMonthlyDefaultRate(prob), calcMonthlyDefaultRate2(prob), places=6)

	def test_calcAnnuity(self):
		# Kredit 8148
		self.assertAlmostEqual( 3233., 100000.00 * simulation.calcAnnuity(interestRate = 0.1013, terms = 3.0, intervals = 12), places=0)
		# Kredit 3576
		self.assertAlmostEqual( 7542., 250000.00 * simulation.calcAnnuity(interestRate = 0.0544, terms = 3.0, intervals = 12), places=0)
		# Kredit 4416
		self.assertAlmostEqual( 8630., 100000.00 * simulation.calcAnnuity(interestRate = 0.0651, terms = 1.0, intervals = 12), places=0)
		# Kredit 359
		self.assertAlmostEqual(  849.,  35000.00 * simulation.calcAnnuity(interestRate = 0.0768, terms = 4.0, intervals = 12), places=0)
		# Kredit 3504
		self.assertAlmostEqual(21106., 125000.00 * simulation.calcAnnuity(interestRate = 0.0448, terms = 0.5, intervals = 12), places=0)

	def test_calcMedian(self):
		with self.assertRaises(ValueError):
			simulation.calcMedian([])

		self.assertEqual(1, simulation.calcMedian([1]))
		self.assertEqual(1.5, simulation.calcMedian([2,1]))
		self.assertEqual(5, simulation.calcMedian([9,2,8,7,5,4,3,8,1]))

	def test_calcPresentValue(self):
		zahlungsstrom1 = [
			{"t": 1, "x":  103.00},
		]
		self.assertAlmostEqual(100.0, simulation.calcPresentValue(interestRate = 0.03, payments = zahlungsstrom1), places=7)

		zahlungsstrom2 = [
			{"t": 0, "x": -100.00},
			{"t": 1, "x":  103.00},
		]
		self.assertAlmostEqual(0.0, simulation.calcPresentValue(interestRate = 0.03, payments = zahlungsstrom2), places=7)

		zahlungsstrom3 = [
			{"t": 0, "x": -100.00},
			{"t": 1, "x":  100.00},
		]
		self.assertAlmostEqual(0.0, simulation.calcPresentValue(interestRate = 0.00, payments = zahlungsstrom3), places=7)

		zahlungsstrom4 = [
			{"t": 0, "x": -100.00},
			{"t": 1, "x":  	55.00},
			{"t": 2, "x":   52.50},
		]
		self.assertAlmostEqual(0.0, simulation.calcPresentValue(interestRate = 0.05, payments = zahlungsstrom4), places=7)

		zahlungsstrom5 = [
			{"t": 0, "x":  100.00},
			{"t": 1, "x":  -55.00},
			{"t": 2, "x":  -52.50},
		]
		self.assertAlmostEqual(0.0, simulation.calcPresentValue(interestRate = 0.05, payments = zahlungsstrom5), places=7)

		with self.assertRaises(ValueError):
			simulation.calcPresentValue(-1.0, [])

	def test_calcIRR(self):
		zahlungsstrom1 = [
			{"t": 0, "x": -100.00},
			{"t": 1, "x":  103.00},
		]
		self.assertAlmostEqual(0.03, simulation.calcIRR(payments = zahlungsstrom1), places=4)

		zahlungsstrom2 = [
			{"t": 0, "x": -100.00},
			{"t": 1, "x":  100.00},
		]
		self.assertAlmostEqual(0.00, simulation.calcIRR(payments = zahlungsstrom2), places=4)

		zahlungsstrom3 = [
			{"t": 0, "x": -100.00},
			{"t": 1, "x":  	55.00},
			{"t": 2, "x":   52.50},
		]
		self.assertAlmostEqual(0.05, simulation.calcIRR(payments = zahlungsstrom3), places=4)

		zahlungsstrom4 = [
			{"t": 0, "x":  100.00},
			{"t": 1, "x":  -55.00},
			{"t": 2, "x":  -52.50},
		]
		self.assertAlmostEqual(0.05, simulation.calcIRR(payments = zahlungsstrom4), places=4)

if __name__ == '__main__':
	unittest.main()
