(ns example.test
  (:import [org.openqa.selenium By WebElement]
           [org.openqa.selenium.remote RemoteWebDriver])
  (:require [clojure.test :refer [deftest is]]
            [examinant.core :refer [remote-tests wait-until]]))


;; The url of the remote provider (with credentials)
(def url (str "http://"
              (System/getenv "SAUCE_USERNAME")
              ":"
              (System/getenv "SAUCE_ACCESS_KEY")
              "@ondemand.saucelabs.com/wd/hub"))


;;Our browser specifications (using Sauce Labs platform names), as a vector of maps
(def browser-specs [{:browserName "chrome" :version "38" :platform "Windows 8.1"}
                    {:browserName "safari" :version "8" :platform "OS X 10.10"}
                    {:browserName "android" :version "4.4" :platform "LINUX"
                     :device-orientation "portrait" :deviceName "Google Nexus 7 HD Emulator"}
                    {:browserName "iPhone" :version "8.1" :platform "OS X 10.9"
                     :device-orientation "portrait"}])


;; Each test is just a function taking the RemoteWebDriver as an argument; 
;; note the use of the clojure.test/is macro
(defn google-logo
  "Checks whether the google logo has the correct title"
  [^RemoteWebDriver driver]
  (.get driver "http://www.google.co.uk")
  (let [^WebElement logo-div (.findElementById driver "hplogo")
        title (.getAttribute logo-div "title")]
    (is (= title "Google"))))


;; Add all the tests to a vector
(def tests [google-logo])


;; Run the tests in parallel against the remote provider using Examinant
(deftest remote-google-tests
  (remote-tests url browser-specs tests))
