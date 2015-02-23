# -*- coding: utf-8 -*-

from scipy.optimize import minimize
import numpy as np
import math
import pandas
from datetime import datetime

class HawkesProcess(object):

    def __init__(self):
        pass

    def _loglikelihood(self, params):
        (mu, alpha, beta) = params
        tlist = np.array(sorted(self.events_int))
        r = np.zeros(len(tlist))
        for i in xrange(1, len(tlist)):
            r[i] = math.exp(-beta*(tlist[i]-tlist[i-1]))*(1+r[i-1])
        loglik  = -tlist[-1] * mu
        loglik = loglik+alpha/beta*sum(np.exp(-beta*(tlist[-1]-tlist))-1)
        loglik = loglik+np.sum(np.log(mu+alpha*r))
        return -loglik

    def fit(self, events):
        self.events = events
        self.events_int = self._convert_events_to_int(self.events)
        ret = minimize(self._loglikelihood,
                       (0.01, 0.1, 0.1),
                       method='Nelder-Mead',
                       args=())
        self.mu, self.alpha, self.beta = ret.x
        self.likelihood = -ret.fun
        return True

    def evaluate(self, _from, _to, interval):
        intensities = []
        _from_int = self._convert_datetime_to_int(_from)
        _to_int = self._convert_datetime_to_int(_to)
        interest_point = range(int(_from_int), int(_to_int), int(interval))
        memory = {}
        m = max(interest_point)
        for t in interest_point:
            v = self.mu
            for ti in self.events_int:
                if t <= ti: break
                tti = t-ti
                if tti in memory:
                    v += memory[tti]
                    continue
                n = self.alpha*math.exp(-self.beta*(tti))
                v += n
                memory[tti] = n
            intensities.append( v )
        return intensities

    def _convert_events_to_int(self, df):
        return [i for i, value in enumerate(df.values) if value > 0]

    def _convert_datetime_to_int(self, date):
        for i, e in enumerate(sorted(self.events.index)):
            if date < e.to_datetime():
                return i
        return i

    def _g(self, ti, tj):
        return self.alpha * (math.exp(-self.beta * (tj - ti)))

    def evaluate_selfreinforce(self,
                               effect_point,          # ti
                               objective_point,       # tj
                               individual_data):
        numerator = self._g(effect_point, objective_point)
        denominator = 0.0
        for tp in individual_data:
            if tp >= objective_point: break
            denominator += self._g(tp, objective_point)
        denominator += self.mu
        return float(numerator/denominator)
