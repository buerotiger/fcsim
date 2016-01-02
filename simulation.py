#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import copy
import math
import numpy

from scipy.optimize import bisect

# calculate monthly default rate for a given
# yearly default rate
def calcMonthlyDefaultRate(yearlyDefaultRate):
	return 1.-math.exp(1./12. * math.log(1. - yearlyDefaultRate))

# calculate annuity for a given interest rate and a number of terms
# with a number of intervals, e.g. for a monthly annuity of a 3-year
# loan use intervals=12 and terms=3
def calcAnnuity(interestRate, terms, intervals = 12):
	x = (1. + interestRate / intervals)
	return math.pow(x, terms*intervals) * (x - 1.) / (math.pow(x, terms*intervals) - 1.)

# get the median from a list of values
def calcMedian(lst):
	if len(lst) == 0:
		raise ValueError("No values given")
	return numpy.median(numpy.array(lst))

# calculate the present value for a set of
# payments (t=time in years, x=payment) for
# a given interest rate
def calcPresentValue(interestRate, payments):
	if isinstance(interestRate, list):
		interestRate = interestRate[0]

	if interestRate <= -1.:
		raise ValueError("Out of bounds")

	resultValue = 0
	for payment in payments:
		resultValue += payment["x"] / (abs(1.+interestRate) ** (payment["t"]))

	return resultValue

# for a given set of payments, the interest rate
# is varied until the present value is zero to yield
# the internal return rate
def calcIRR(payments, startingValue = 0.05):
	result = bisect(calcPresentValue, -0.99999, 0.99, args=(payments,), xtol=1e-4, rtol=1e-6, maxiter=250, full_output=True, disp=False)

	if result is None:
		return None
	else:
		assert(result[1].converged)
		return result[0]

def calcLoan(loan, customParams):
	# default parameters
	effectiveParams = {
		"numIntervals": 12.,
		"recoveryRate": 0.5,
		"recoveryLength": 18,
		"capitalGainsTax": 0.,
		"serviceFeeRate": 0.01,
	}
	# update default parameters with given parameters
	effectiveParams.update(customParams)

	monthlyDefaultRate = calcMonthlyDefaultRate(loan["yearlyDefaultRate"])
	monthlyInterestRate = loan["yearlyInterestRate"] / float(effectiveParams["numIntervals"])
	monthlyServiceFeeRate = effectiveParams["serviceFeeRate"] / float(effectiveParams["numIntervals"])
	monthlyAnnuity = loan["principal"] * calcAnnuity(loan["yearlyInterestRate"], loan["term"], effectiveParams["numIntervals"])

	# check if calculated monthly annuity is compatible with loan annuity
	if "monthlyAnnuity" in loan:
		if abs(round(monthlyAnnuity, 0) - loan["monthlyAnnuity"]) > 0.:
			warnings.warn("Calculated annuity %10.2f differs from given annuity %10.2f" % (monthlyAnnuity,loan["monthlyAnnuity"]))

		if abs(round(monthlyAnnuity, 2) - loan["monthlyAnnuity"]) > 0.50:
			assert(abs(round(monthlyAnnuity, 0) - loan["monthlyAnnuity"]) == 0)

	payments = []
	probIRRs = []

	totalRepayment = 0
	residualDebt = loan["principal"]
	probToReach = 1
	cumulativeProbability = 0

	payments.append({"t": 0, "x": -1*loan["principal"] })
	for cntMonate in range(1, int(loan["term"]*effectiveParams["numIntervals"]+1)):		
		# assume a default in this month and construct
		# the resulting payments with a recovery at a later
		# time
		paymentsWithDefault = copy.deepcopy(payments)
		paymentsWithDefault.append({"t": (cntMonate+effectiveParams["recoveryLength"]) / effectiveParams["numIntervals"], "x": (effectiveParams["recoveryRate"] * residualDebt) })
		cumulativeProbability += probToReach * monthlyDefaultRate
		probIRRs.append(
			{
				"singleProbability": probToReach * monthlyDefaultRate,
				"cumulativeProbability" : cumulativeProbability,
				"internalReturnRate": calcIRR(paymentsWithDefault, startingValue = 0.),
				"absoluteReturn": totalRepayment + effectiveParams["recoveryRate"] * residualDebt,
				"relativeReturn": (totalRepayment + effectiveParams["recoveryRate"] * residualDebt) / loan["principal"]
			}
		)

		probToReach *= (1.-monthlyDefaultRate)

		# no default
		paymentInterests = residualDebt * monthlyInterestRate #Fixme loan["yearlyInterestRate"] / effectiveParams["numIntervals"]
		paymentServiceFee = residualDebt * monthlyServiceFeeRate

		effectiveRepayment = max(0, monthlyAnnuity - paymentServiceFee - paymentInterests*effectiveParams["capitalGainsTax"])
		
		totalRepayment += effectiveRepayment
		residualDebt -= (monthlyAnnuity - paymentInterests)
		payments.append({"t": float(cntMonate) / effectiveParams["numIntervals"], "x": effectiveRepayment })

	# the residual debt should be around zero
	assert(residualDebt < 0.01)
	assert(residualDebt > -0.01)

	assert(round(cumulativeProbability + probToReach, 4) == 1.)

	# return after final payment
	# the min() avoids rounding problems
	cumulativeProbability = min(1, cumulativeProbability + probToReach)
	probIRRs.append(
		{
			"singleProbability": probToReach,
			"cumulativeProbability" : cumulativeProbability,
			"internalReturnRate": calcIRR(payments, startingValue = probIRRs[-1]["internalReturnRate"]),
			"absoluteReturn": totalRepayment,
			"relativeReturn": (totalRepayment ) / loan["principal"]
		}
	)
	
	sumExpextedIRR=0
	probLoss = 0
	cumulativeProbability = 0

	medianIRR = None
	for probIRR in probIRRs:
		if probIRR["internalReturnRate"] < 0.00:
			probLoss += probIRR["singleProbability"]

		cumulativeProbability += probIRR["singleProbability"]
		if cumulativeProbability >= 0.5 and medianIRR is None:
			medianIRR = probIRR["internalReturnRate"]

		sumExpextedIRR += probIRR["singleProbability"] * probIRR["internalReturnRate"]

	# construct the result object
	ret = copy.deepcopy(loan)
	ret["parameters"] = effectiveParams
	ret["probIRRs"] = probIRRs
	ret["result"] = {
		"probLoss": round(probLoss, 6),
		"meanIRR": round(sumExpextedIRR, 6),
		"medianIRR": round(medianIRR, 6),
	}
	return ret

