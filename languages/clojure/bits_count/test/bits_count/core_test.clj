(ns bits_count.core-test
  (:require [clojure.test :refer :all]
            [bits_count.core :refer :all]))

(deftest type-int-test
  (testing "type int"
    (is (= java.lang.Integer (type (int 0))))))

(deftest bits-count-long-test
  (testing "bits-count-long"
    (is (= 0 (bits-count-long 0)))
    (is (= 1 (bits-count-long 1)))
    (is (= 1 (bits-count-long 2)))
    (is (= 2 (bits-count-long 3)))
    (is (= 2 (bits-count-long 10)))
    (is (= 8 (bits-count-long 0xff)))
    (is (= 1 (bits-count-long 0x100)))
    (is (= 15 (bits-count-long 0x7fff)))
    (is (= 16 (bits-count-long 0xffff)))
    (is (= 31 (bits-count-long 0x7fffffff)))
    (is (= 64 (bits-count-long -1)))
  ))

(deftest bits-count-int-test
  (testing "bits-count-int"
    (is (= 0 (bits-count-int (int 0))))
    (is (= 1 (bits-count-int (int 1))))
    (is (= 1 (bits-count-int (int 2))))
    (is (= 2 (bits-count-int (int 3))))
    (is (= 2 (bits-count-int (int 10))))
    (is (= 8 (bits-count-int (int 0xff))))
    (is (= 1 (bits-count-int (int 0x100))))
    (is (= 15 (bits-count-int (int 0x7fff))))
    (is (= 16 (bits-count-int (int 0xffff))))
    (is (= 31 (bits-count-int (int 0x7fffffff))))
    (is (= 32 (bits-count-int (int -1))))
  ))
