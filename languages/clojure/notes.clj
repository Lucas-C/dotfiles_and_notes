;;;;;;;;
; LIBS
;;;;;;;;
Datomic ; time-based elastic ACID DB

;;;;;;;;;
; DEBUG
;;;;;;;;;
[org.clojars.gjahad/debug-repl "0.3.3"]
(use 'alex-and-georges.debug-repl)
(debug-repl)

[org.clojure/tools.trace "0.7.6"]
(use 'clojure.tools.trace)
(trace ...)

;; debugging parts of expressions
(defmacro dbg[x] `(let [x# ~x] (println "dbg:" '~x "=" x#) x#))

(def hex #(format "%x" %1))

;;;;;;;;
; JAVA
;;;;;;;;
(clojure.lang.Numbers/unchecked_multiply 2 3)

;;;;;;;;;;
; TRICKS
;;;;;;;;;;
; Number types
(= (bit-not 0) -1) ; true
(= (hex (int -1)) (hex 0xffffffff)) ; true
(= (int -1) 0xffffffff) ; false

(-> "a b c d"
  .toUpperCase
  (.replace "A" "X")
  (.split " ")
  first)
;; is the same as:
(first (.split (.replace (.toUpperCase "a b c d")
                         "A"
                         "X")
               " "))
;; AND
(-> person :employer :address :city)
;; is the same as:
(((person :employer) :address) :city)
