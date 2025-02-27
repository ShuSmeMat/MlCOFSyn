import numpy as np
from scipy.stats import norm

def expected_improvement(model, obj, jitter=0.01):
    domain = obj.domain

    # 只使用已经获得的结果进行 EI 评估
    if len(obj.results) == 0:
        max_observed = 0
    else:
        target_column = obj.results.columns[-1] if obj.target == -1 else obj.target
        max_observed = obj.results.sort_values(by=target_column).iloc[-1]
        # max_observed = max_observed[obj.target]
        max_observed = max_observed.iloc[obj.target]

    mean, variance = model.predict(domain)
    stdev = np.sqrt(variance) + 1e-6

    z = (mean - max_observed - jitter) / stdev
    imp = mean - max_observed - jitter
    zzz = norm.cdf(z)
    ttt = norm.pdf(z)
    ei = imp * norm.cdf(z) + stdev * norm.pdf(z)

    return ei
