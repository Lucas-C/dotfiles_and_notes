(ns bits_count.core)
(use 'alex-and-georges.debug-repl) ; provides (debug-repl) == pdb.set_trace() - START WITH: (use 'bits_count.core)
(use 'clojure.tools.trace) ; provides dotrace, trace, deftrace...

; !! Clojure bit-* operators only return Long values

; The definition of those masks may look like voodoo ;
; truth is they could as well be hardcoded.
; I just found a relation between same so that it is possible
; to generate them based on a int/long size in bits
(defn mask4 [size]
  (if (= size 8) 1
    (+ 1 (bit-shift-left (mask4 (- size 8)) 8))))
(defn mask3 [size]
  (* 15 (mask4 size)))
(defn mask2 [size]
  (* 51 (mask4 size)))
(defn mask1 [size]
  (* 85 (mask4 size)))

; int/long => different multiplication function
(defn mul-op [size]
  ; we needd to use 'unchecked-multiply' to ignore the remainder (an avoid an OVERFLOW for Longs)
  (if (= size Integer/SIZE)
    unchecked-multiply-int
    ; + the ugly 'long' cast here is mandatory, see https://groups.google.com/forum/#!topic/clojure/Jl994FEuUD0
    (fn [a b] (unchecked-multiply (long a) (long b)))))

; ALGO FROM: http://graphics.stanford.edu/~seander/bithacks.html
(defn bits-count [n, size]
  (let [v (- n (bit-and (bit-shift-right n 1) (mask1 size)))                        ; v = n - ((n >> 1) & MASK1)
        v (+ (bit-and v (mask2 size)) (bit-and (bit-shift-right v 2) (mask2 size))) ; v = (v & MASK2) + ((v >> 2) & MASK2)
        v (bit-and (+ v (bit-shift-right v 4)) (mask3 size))]                       ; v = (v + (v >> 4)) & MASK3
       (bit-shift-right ((mul-op size) v (mask4 size)) (- size 8))))                ; c = (v * MASK4) >> (sizeof(T) - 1) * CHAR_BIT

(defn bits-count-int [n]
  (assert (= java.lang.Integer (type n)))
  (bits-count n Integer/SIZE))
(defn bits-count-long [n]
  (bits-count n Long/SIZE))

(defn -main []
    (def data [0 1 2 3 10 0xf 0x10 0xff 0x100 0x7fff 0xffff 0x7fffffff -1])
    (dorun (map #(println (str %1 (format " (0x%x) has " %1) (bits-count-long %1) " bits")) data))
    (dorun (map #(println (str %1 (format " (0x%x) has " %1) (bits-count-int %1) " bits")) (map int data)))
)

