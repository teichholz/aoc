(ns util
  (:require [java-time.api :as t]))

(defn read [day year] 
  (slurp (str (System/getenv "$HOME") "aoc/input/" year "/day" day)))