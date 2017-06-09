Statistics & benchmarking
=========================

Tools for server banchmarking aka stress / load / performances testing: cf. bookmarks

    ab -n5000 -c50 "http://path/to/app?params" # Apache Benchmarking - Alt: tarekziade/boom (Python), locustio/locust (Python), wg/wrk (C), JoeDog/siege (C), shoreditch-ops/artillery (NodeJS), tsenart/vegeta (Go)

# REPEAT your tests !

Gil Tene (Mr. Java HdrHistogram): always "calibrate" latency tools with ^Z tests. If ^Z results don't make sense, don't use tool.
<img src="http://www.infoq.com/resource/presentations/latency-lessons-tools/en/slides/sl29.jpg" style="width:50%"/>
See detailed discussion starting around 38:30 in this talk: http://www.infoq.com/presentations/latency-lessons-tools

Also: When you talk about a 99% requirement:
<img src="http://www.infoq.com/resource/presentations/latency-lessons-tools/en/slides/sl24.jpg" style="width:50%"/>

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
For space-effecient sketch / streaming algorithm to compute quantiles, cf. Algo_Notes.md
For other measure of dispersion: https://en.wikipedia.org/wiki/Statistical_dispersion#Measures_of_statistical_dispersion

Spearman’s rank correlation coefficient: a number between 1 and -1 indicating if two lists of items are ordered the same, in reverse, or not in the same order at all

HdrHistogram: a better latency capture method

[Statistics for Engineers : Applying statistical techniques to operations data](http://queue.acm.org/detail.cfm?id=2903468) : include the name of a useful "barcode" graph : the rug plot

RESSOURCES:
[1] : HOW TO NOT TO LIE WITH STATISTICS: THE CORRECT WAY TO SUMMARIZE BENCHMARK RESULTS (PHILIP J. FLEMING and JOHN J. WALLACE)
[2] : http://blogs.perl.org/users/steffen_mueller/2010/09/your-benchmarks-suck.html
