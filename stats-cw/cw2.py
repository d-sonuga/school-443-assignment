import numpy as np 
from scipy.stats import norm

mean, std_dev, max_days = 300, 50, 365
z_score = (max_days - mean) / std_dev
prob = norm.cdf(z_score)
print(f"Estimated prob that bulb will last at most {max_days} days: {prob:.4f}")
