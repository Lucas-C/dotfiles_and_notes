# REPEAT your tests !


# Valuable metrics [2]
* Use the geometric mean instead of arithmetic mean for normalized numbers [1]. "Normalized Number" : ratio of a benchmark test results / another 'reference' machine results.
Geometric mean ({a1, a2, ..., an}) = sqrt[1/n](a1 * a2 * ... * an)

* Standard deviation : To compute it on-the-fly, see 'stats' command.

* Median : The median is a fairly robust estimator of the expectation value with respect to outliers (assuming they are comparatively rare).

* Median absolute deviation : The median absolute deviation is a measure of statistical dispersion. Moreover, the MAD is a robust statistic, being more resilient to outliers in a data set than the standard deviation. In the standard deviation, the distances from the mean are squared, so large deviations are weighted more heavily, and thus outliers can heavily influence it. In the MAD, the deviations of a small number of outliers are irrelevant. [wiki]

* (exponantial) Moving average : http://en.wikipedia.org/wiki/Moving_average

* Remove outliers : all timings that deviate from the median by more than X times the MAD

* Finally:
** Expectation value : mean of the truncated distribution
** Measure of variability : MAD of the truncated distribution
** Uncertainty on the expectation value : sigma = MAD / sqrt(N) where N is the number of remaining measurements). To get a %relative error -> sigma / mean

* MAD = Median absolute deviation, !! NOT to be confused with the "Mean absolute difference"
For other measure of dispersion: https://en.wikipedia.org/wiki/Statistical_dispersion#Measures_of_statistical_dispersion


RESSOURCES:
[1] : HOW TO NOT TO LIE WITH STATISTICS: THE CORRECT WAY TO SUMMARIZE BENCHMARK RESULTS (PHILIP J. FLEMING and JOHN J. WALLACE)
[2] : http://blogs.perl.org/users/steffen_mueller/2010/09/your-benchmarks-suck.html
