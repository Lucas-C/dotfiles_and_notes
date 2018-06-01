Quicksort: stable, constant space usage, worst case O(n^2) if pivot is smallest/largest element, not good if data on disk
Merge sort : stable, O(n) space on arrays / constant space on linked lists, worst case O(n*log(n)), ok if data on disk
TimSort: used by Python, mix of merge sort & insertion sort, perform well on real-word data
IntroSort: C++ std::sort, a variation over QuickSort which "degenerates" to HeapSort when the recursion goes too deep
Radix / Counting sort: the best for ints
-> cf. include/linux/radix-tree.h / lib/radix-tree.c from the linux kernel (detailed in "linux-insides")
-> Algorithmic complexity attack, e.g. McIlroy sort killer, which build an input to make any sorting quadratic in time
Pdqsort: the best unstable sort so far -> https://github.com/orlp/pdqsort

To get a better locality of reference (= elements accessed in sequence are located in memory addresses close to each other),
binary search trees are better implemented using a contiguous array following a red-black tree's breadth-first order (like a heap basically)

Trie / directed acyclic graph can be + efficient than binary search trees / hash tables
HAMT: "achieves almost hash table-like speed while using memory much more economically. Also, a hash table may have to be periodically resized, an expensive operation, whereas HAMTs grow dynamically" -> https://en.wikipedia.org/wiki/Hash_array_mapped_trie
qp-trie > crit-bit trie > Patricia trie: http://fanf.livejournal.com/137283.html

Test set membership aka sketching data structures:
- HyperLogLog: [original paper](http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf), [2013 paper from Google](http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/40671.pdf) and [an explanation](http://research.neustar.biz/2012/10/25/sketch-of-the-day-hyperloglog-cornerstone-of-a-big-data-infrastructure/)
- Bloom filters : http://crystal.uta.edu/~mcguigan/cse6350/papers/Bloom.pdf - http://corte.si/%2Fposts/code/bloom-filter-rules-of-thumb/index.html - Invertible: http://arxiv.org/pdf/1101.2245v2.pdf (cf. Python implementations)
- "[Cuckoo filters](http://www.pdl.cmu.edu/PDL-FTP/FS/cuckoo-conext2014.pdf) support adding and removing items dynamically while achieving even higher performance than Bloom filters"
[Cuckoo Filters vs. Bloom Filters in Python](http://blog.fastforwardlabs.com/post/153566952648/probabilistic-data-structure-showdown-cuckoo)
- Counting Quotient Filter alternative to Bloom filters: https://blog.acolyer.org/2017/08/08/a-general-purpose-counting-filter-making-every-bit-count/
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
- google/highwayhash: Fast strong hash functions: SipHash/HighwayHash, faster that SipTreeHash
- [A new fast hash table (2018)](https://probablydance.com/2018/05/28/a-new-fast-hash-table-in-response-to-googles-new-fast-hash-table/)

Perceptual hashes:
- https://tech.okcupid.com/evaluating-perceptual-image-hashes-okcupid/
- cf. Python notes: LSHash, aHash, pHash, dHash, wHash

Geohash: geocoding system with a hierarchical spatial data structure that subdivides space into buckets of grid shape

[Z-Order curve / Lebesgue curve / Morton Morton code](https://en.wikipedia.org/wiki/Z-order_curve) : map multidimensional data to one dimension while preserving locality of the data points.
-> [illustrated explanation & usage example at AWS](https://aws.amazon.com/fr/blogs/database/z-order-indexing-for-multifaceted-queries-in-amazon-dynamodb-part-1/)

Compression:
- Google Snappy (10x faster, 50% worse compression than LZMA (7z))
- Google Zopfli (5% more compression, 100x slower than LZMA (7z))
- Google Brotli: better than zlib, LZMA (7z) and Snappy/Zopfli in term of speed AND compression ratio

-> Pinterest predefined dictionary to optimize Zlib DEFLATE LZ77 stage : https://engineering.pinterest.com/blog/evolving-mysql-compression-part-2

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

[A collection of links for streaming algorithms and data structures](https://gist.github.com/debasishg/8172796): hyperloglog, minhash, Q-digest, t-digest, Count-Min Sketch, sliding windows, frugal streaming...

Double-linked list C implementation in the linux kernel (detailed in "linux-insides"):
    struct list_head {
        struct  list_head   *next,  *prev;
    };
    // Usage example:
    struct nmi_desc {
        spinlock_t  lock;
        struct  list_head   head;
    };

Interesting algo to query for the min/max of a N elements collection, with 2*N space complexity & logN complexity: languages/python/battledev_regionsjobs_isograd_2016-03-22/challenge5_soluce.py
    rmq = RangeMaxQuery(heights)
    highest = rmq.max_in_range(start, end)

Top N values of a stream : [Top speed for top-k queries](http://lemire.me/blog/2017/06/21/top-speed-for-top-k-queries/)

Feistel networks pseudorandom permutation / one-to-one pseudo random mapping : cf. http://antirez.com/news/113
> It’s a building block typically used in cryptography: it creates a transformation between a sequence of bits and another sequence of bits, so that the transformation is always invertible, even if you use all the kind of non linear transformations inside the Feistel network


## Crypto

encrypting a file with its hash as the key, aka convergent encryption :
https://www.reddit.com/r/crypto/comments/40kq5x/what_are_the_ramifications_of_encrypting_a_file/
Benefit: you can easily check the file integrity
Benefit 2: if no random prefix/suffix is added (=> weaker security), it can be used as unique identifier for deduping
