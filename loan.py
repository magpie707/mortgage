#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import argparse
import decimal

DOLLAR_QUANTIZE = decimal.Decimal('.01')

def dollar(f, round=decimal.ROUND_CEILING):
    """
    This function rounds the passed float to 2 decimal places.
    """
    if not isinstance(f, decimal.Decimal):
        f = decimal.Decimal(str(f))
    return f.quantize(DOLLAR_QUANTIZE, rounding=round)

class Loan:
    def __init__(self, interest, years, paymentsperyear, amount):
        self._interest = float(interest)
        self._years = float(years)
        self._paymentsperyear = int(paymentsperyear)
        self._amount = dollar(amount)

    def rate(self):
        return self._interest

    def period_growth(self):
        return 1. + self._interest / self._paymentsperyear

    def apy(self):
        return self.period_growth() ** self._paymentsperyear - 1

    def loan_years(self):
        return self._years

    def loan_periods(self):
        return self._years * self._paymentsperyear
    def amount(self):
        return self._amount

    def period_payment(self):
        pre_amt = float(self.amount()) * self.rate() / (float(self._paymentsperyear) * (1.-(1./self.period_growth()) ** self.loan_periods()))
        return dollar(pre_amt, round=decimal.ROUND_CEILING)

    def total_value(self, p_payment):
        return p_payment / self.rate() * (float(self._paymentsperyear) * (1.-(1./self.period_growth()) ** self.loan_periods()))

    def annual_payment(self):
        return self.period_payment() * self._paymentsperyear

    def total_payout(self):
        return self.period_payment() * decimal.Decimal(self.loan_periods())

    def period_payment_schedule(self):
        period = self.period_payment()
        balance = dollar(self.amount())
        rate = decimal.Decimal(str(self.rate())).quantize(decimal.Decimal('.000001'))
        while True:
            interest_unrounded = balance * rate * decimal.Decimal(1)/self._paymentsperyear
            interest = dollar(interest_unrounded, round=decimal.ROUND_HALF_UP)
            if period >= balance + interest:
                yield balance, interest, balance
                break
            principle = period - interest
            yield principle, interest, balance
            balance -= principle

def print_summary(m):
    print('{0:>25s}:  {1:>12.6f}'.format('Rate', m.rate()))
    print('{0:>25s}:  {1:>12.6f}'.format('Period Growth', m.period_growth()))
    print('{0:>25s}:  {1:>12.6f}'.format('APY', m.apy()))
    print('{0:>25s}:  {1:>12.0f}'.format('Payoff Years', m.loan_years()))
    print('{0:>25s}:  {1:>12.0f}'.format('Payoff Periods', m.loan_period()))
    print('{0:>25s}:  {1:>12.2f}'.format('Amount', m.amount()))
    print('{0:>25s}:  {1:>12.2f}'.format('Period Payment', m.period_payment()))
    print('{0:>25s}:  {1:>12.2f}'.format('Annual Payment', m.annual_payment()))
    print('{0:>25s}:  {1:>12.2f}'.format('Total Payout', m.total_payout()))

def main():
    parser = argparse.ArgumentParser(description='Loan Amortization Tools')
    parser.add_argument('-i', '--interest', default=6, dest='interest')
    parser.add_argument('-y', '--loan-years', default=30, dest='years')
    parser.add_argument('-p', '--loan-paymentsperyear', default=None, dest='paymentsperyear')
    parser.add_argument('-a', '--amount', default=100000, dest='amount')
    args = parser.parse_args()

    if args.paymentsperyear:
        m = Loan(float(args.interest) / 100, float(args.paymentsperyear), args.amount)
    else:
        m = Loan(float(args.interest) / 100, float(args.years) * self._paymentsperyear, args.amount)

    print_summary(m)

if __name__ == '__main__':
    main()
