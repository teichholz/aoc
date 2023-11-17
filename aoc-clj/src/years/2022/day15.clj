(ns years.2022.day15
  (:require [clojure.set :as set]
            util))


(def input (util/read-lines 15 2022))
(defn parse [line]
  (let [matches (re-seq #"-?\d+" line)
        [x1 y1 x2 y2] (map read-string matches)]
    [[x1 y1] [x2 y2]]))
(def coords (map parse input))
(def sensors (map first coords))
(def beacons (into #{} (map second coords)))
(def max-x (apply max (mapcat (partial map first) coords)))
(def min-x (apply min (mapcat (partial map first) coords)))
(defn manhatten [[[x y] [x' y']]] (+ (abs (- x x')) (abs (- y y'))))
(def manhattens (map manhatten coords))
(defn sensor-range? [[p manhattend]] (fn [p'] (>= manhattend (manhatten [p p']))))

(def some-sensor-range?
  (->> (map list sensors manhattens)
       (map sensor-range?)
       (apply some-fn)))

(def max-hatten (apply max manhattens))
(def y=2000000 (into #{} (map (fn [x] [x 2000000]) (range (- (+ min-x max-hatten)) (+ max-x max-hatten)))))
(def in-range (filter some-sensor-range? (set/difference y=2000000 beacons)))
(def part-1 (count in-range))

(def all-possible 
  (for [x (range 0 21)
        y (range 0 21)]
    [x y]))

(map some-sensor-range? all-possible)
(filter #(= nil (second %)) 
        (map (fn [p] [p (some-sensor-range? p)]) all-possible))
