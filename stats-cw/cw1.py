import numpy as np
from scipy.stats import norm

mean, std_dev, eliz_score, sample_size = 850, 100, 940, 100_000
scores = np.random.normal(850, 100, sample_size)
higher_scores = (scores > eliz_score).sum()
proportion = higher_scores / sample_size
print("Estimated proportion of students with a higher score that Elizabeth:", f"{proportion: .4f}")
