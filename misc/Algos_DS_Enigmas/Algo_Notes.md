Quicksort: stable, constant space usage, worst case O(n^2) if pivot is smallest/largest element, not good if data on disk
Merge sort : stable, O(n) space on arrays / constant space on linked lists, worst case O(n*log(n)), ok if data on disk
TimSort: used by Python, mix of merge sort & insertion sort, perform well on real-word data
IntroSort: C++ std::sort, a variation over QuickSort which "degenerates" to HeapSort when the recursion goes too deep
Radix / Counting sort: the best for ints
-> Algorithmic complexity attack, e.g. McIlroy sort killer, which build an input to make any sorting quadratic in time

Trie / directed acyclic graph can be + efficient than binary search trees / hash tables

Test set membership aka sketching data structures:
- HyperLogLog: [original paper](http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf), [2013 paper from Google](http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/40671.pdf) and [an explanation](http://research.neustar.biz/2012/10/25/sketch-of-the-day-hyperloglog-cornerstone-of-a-big-data-infrastructure/)
- Bloom filters : http://crystal.uta.edu/~mcguigan/cse6350/papers/Bloom.pdf - http://corte.si/%2Fposts/code/bloom-filter-rules-of-thumb/index.html - Invertible: http://arxiv.org/pdf/1101.2245v2.pdf (cf. Python implementations)
- "[Cuckoo filters](http://www.pdl.cmu.edu/PDL-FTP/FS/cuckoo-conext2014.pdf) support adding and removing items dynamically while achieving even higher performance than Bloom filters"
- Count-Mink sketch explanation: http://research.neustar.biz/2011/09/13/streaming-algorithms-and-sketches/ ; another, with Bloom filter too: http://lkozma.net/blog/sketching-data-structures/
- Use prime numbers to represent set elements: http://www.stdlib.net/~colmmacc/2010/09/02/prime-and-proper/
- with time decay: [Flower Filter](http://eng.kifi.com/flower-filter-an-update/)

(Frugal) streaming algorithms:
- Space-efficient quantiles computation / moving_window median algorithms
    * [Space-Efficient Online Computation of Quantile Summaries](http://infolab.stanford.edu/~datar/courses/cs361a/papers/quantiles.pdf)
    * [Quantiles on Streams](http://www.cs.ucsb.edu/~suri/psdir/ency.pdf) 
    * [Some moving window median algos comparison](https://github.com/kwgoodman/roly) in Python, including a double heap solution

Succint data structures: use an amount of space that is "close" to the information-theoretic lower bound but still allow for efficient query operations, by encoding data very efficiently in-place, so that it does not need to be decompressed to be used.

Hashing:
- 'fuzzy' hashing that gaves same result for inputs that have homologies : http://www.forensicswiki.org/wiki/Context_Triggered_Piecewise_Hashing
- selection from "Bloomin' Marvellous" slides: MurmurHash3, xxhash, SipHash

Compression:
- Google Snappy (10x faster, 50% worse compression than LZ)
- Google Zöpfli (5% more compression, 100x slower than LZ)

PID controller: control loop feedback mechanism, using the proportional, integral and derivative values,
    that attempts to minimize the error in outputs by adjusting the process control inputs.

Minimum spanning tree for a connected weighted graph ("arbre recouvrant de poids minimum") : Algorithme de Kruskal

HMAC > a hash with a salt, in term of security

VCDIFF : format & algorithm for delta encoding

Fisher-Yates shuffle : O(n) complexity, guaranteed uniformity, optimal asymptotic time & space complexity

product-matrix-MSR codes > Reed-Solomon codes, for fault tolerance (cf. jmason)

[Exponential Backoff algorithm](http://en.wikipedia.org/wiki/Exponential_backoff#Binary_exponential_backoff_.2F_truncated_exponential_backoff) + [applied to web-sockets](http://blog.johnryding.com/post/78544969349/how-to-reconnect-web-sockets-in-a-realtime-web-app)

[RAPTOR](http://research.microsoft.com/apps/pubs/default.aspx?id=156567) : Round-Based Public Transit Routing
-> compute all Pareto-optimal journeys in a dynamic public transit network for two criteria: arrival time and number of transfers
-> used by Navitia
