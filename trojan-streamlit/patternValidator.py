#from dtaidistance import dtw
import dataPrep as dp
import numpy    as np
#import bz2

#def calc_correlation(actual, predic):
#    a_diff = actual - np.mean(actual)
#    p_diff = predic - np.mean(predic)
#    numerator = np.sum(a_diff * p_diff)
#    denominator = np.sqrt(np.sum(a_diff ** 2)) * np.sqrt(np.sum(p_diff ** 2))
#    return numerator / denominator

def validatePatterns(pattern, match):
    pattern = list(pattern.iloc[:, 0])
    match   = list(match.iloc[:, 0])
    corr    = round(calc_correlation(pattern, match), 2)
    euc     = round(calc_euclidean(pattern, match), 2)
    mape    = round(calc_mape(pattern, match), 2)
    dynamic = round(calc_dtw(pattern, match), 2)
    comp    = round(calc_cbd(pattern, match), 2)
    minAll  = min(round(abs(corr - 1), 2), euc, mape, dynamic, comp)
    if(minAll < 0.1):
        decision = "Platinum"
    elif(minAll < 0.50):
        decision = "Gold"
    elif(minAll < 0.75):
        decision = "Silver"
    elif(minAll < 1):
        decision = "Bronze"
    else:
        decision = "No Match"
    return [minAll, decision, corr, euc, mape, dynamic, comp]

def calc_correlation(actual, predic):
    actual      = dp.cleanList(actual)
    predic      = dp.cleanList(predic)
    a_diff      = actual - np.mean(actual)
    p_diff      = predic - np.mean(predic)
    numerator   = round(np.sum(a_diff * p_diff), 2)
    denominator = round(np.sqrt(np.sum(a_diff ** 2)) * np.sqrt(np.sum(p_diff ** 2)), 2)
    if denominator == 0:
        denominator = 0.0000001
    return round(numerator / denominator, 2)

def calc_euclidean(actual, predic):
    return np.sqrt(np.sum((np.array(dp.cleanList(actual)) - np.array(dp.cleanList(predic))) ** 2))

def calc_mape(actual, predic):
    actual, predic = dp.cleanRemoveNaNs(actual, predic)
    actual         = dp.zeroesListToCloseToZero(actual)
    return np.mean(np.abs((np.array(actual) - np.array(predic)) / actual))

def calc_dtw(l1, l2):
    return dtw.distance_fast(np.array(dp.cleanList(l1)).astype('double'), np.array(dp.cleanList(l2)).astype('double'))

def calc_cbd(l1, l2):
    liftedLists = dp.lift(dp.cleanList(l1), dp.cleanList(l2))
    return CompressionBasedDissimilarity().calculate(np.array(liftedLists[0]), np.array(liftedLists[1]))

class CompressionBasedDissimilarity(object):

    def __init__(self, n_letters = 7):
        self.bins = None
        self.n_letters = n_letters

    def set_bins(self, bins):
        self.bins = bins

    def sax_bins(self, all_values):
        bins = np.percentile(
            all_values[all_values > 0], np.linspace(0, 100, self.n_letters + 1)
        )
        bins[0]  = 0
        bins[-1] = 1e1000
        return bins

    @staticmethod
    def sax_transform(all_values, bins):
        indices  = np.digitize(all_values, bins) - 1
        alphabet = np.array([*("abcdefghijklmnopqrstuvwxyz"[:len(bins) - 1])])
        text     = "".join(alphabet[indices])
        return str.encode(text)

    def calculate(self, m, n):
        if self.bins is None:
            m_bins = self.sax_bins(m)
            n_bins = self.sax_bins(n)
        else:
            m_bins = n_bins = self.bins
        m            = self.sax_transform(m, m_bins)
        n            = self.sax_transform(n, n_bins)
        len_m        = len(bz2.compress(m))
        len_n        = len(bz2.compress(n))
        len_combined = len(bz2.compress(m + n))
        return len_combined / (len_m + len_n)
