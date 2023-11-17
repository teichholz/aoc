(ns years.2022.day13
  (:require [clojure.core.match :refer [match]]
            util))

(def input (util/read-lines 13 2022))

(def pairs
  (->> (filter not-empty input)
       (map load-string)
       (partition 2)))
      
(defn cmp [left right]
  (match [left right]
    [_ :guard number? _ :guard number?] (compare left right)
    [l :guard number? r :guard vector?] (cmp [l] r)
    [l :guard vector r :guard number?] (cmp l [r])
    [[] []] 0
    [[] [_ & _]] -1
    [[_ & _] []] 1
    [[l & ls] [r & rs]] (let [c (cmp l r)]
                          (if (zero? c)
                            (cmp ls rs)
                            c))))

(def part1
  (->> (map (partial apply cmp) pairs)
       (map-indexed (fn [i v] (if (= -1 v) (inc i) 0)))
       (reduce +)))