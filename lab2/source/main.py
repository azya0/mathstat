import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


sns.set(style="whitegrid")


def analyze_distribution(distribution, params, sample_sizes, distribution_name):
    results = []
    
    for size in sample_sizes:
        if distribution == 'normal':
            data = np.random.normal(params[0], params[1], size)
        elif distribution == 'cauchy':
            data = np.random.standard_cauchy(size)
        elif distribution == 'poisson':
            data = np.random.poisson(params[0], size)
        elif distribution == 'uniform':
            data = np.random.uniform(params[0], params[1], size)

        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = data[(data < lower_bound) | (data > upper_bound)]
        num_outliers = len(outliers)

        results.append({'Sample Size': size, 'Outliers': num_outliers})

        plt.figure(figsize=(8, 5))
        sns.boxplot(data=data)
        plt.title(f'Box Plot of {distribution_name} Distribution (n={size})')
        plt.ylabel('Value')
        plt.show()

    return pd.DataFrame(results)


sample_sizes = [20, 100, 1000]

normal_results = analyze_distribution('normal', (0, 1), sample_sizes, 'Normal N(0, 1)')
cauchy_results = analyze_distribution('cauchy', None, sample_sizes, 'Cauchy C(0, 1)')
poisson_results = analyze_distribution('poisson', (10,), sample_sizes, 'Poisson P(10)')
uniform_results = analyze_distribution('uniform', (-np.sqrt(3), np.sqrt(3)), sample_sizes, 'Uniform U(-sqrt(3), sqrt(3))')

summary_results = pd.concat([normal_results, cauchy_results, poisson_results, uniform_results], keys=['Normal', 'Cauchy', 'Poisson', 'Uniform'])


print(summary_results)
