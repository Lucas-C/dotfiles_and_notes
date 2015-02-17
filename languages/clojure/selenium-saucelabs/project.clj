(defproject selenium-saucelabs "0.1.0-SNAPSHOT"
  :description "Learning test for brightnorth/examinant"
  :dependencies [[org.clojure/clojure "1.6.0"],
                 [brightnorth/examinant "0.1.3"],
                 [midje "1.6.3" :exclusions [org.clojure/clojure]]]
  :profiles {:dev {:plugins [[lein-midje "3.1.3"]]}})
