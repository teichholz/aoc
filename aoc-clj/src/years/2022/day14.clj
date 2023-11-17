(ns years.2022.day14
  (:require [clojure.core.match :refer [match]]
            [clojure.string :as string]
            [com.rpl.specter :as s]
            util))

(def input (util/read-lines 14 2022))
(def sand-origin [500 0])

(defn parse-point
  [str]
  (mapv #(Integer/parseInt %) (string/split str #",")))

(def plines
  (->> (map #(string/split % #" -> ") input)
       (map (partial map parse-point))))

(defn pline->points
  [pair]
  (let [sorted (sort pair)
        [[ox oy] [dx dy]] sorted]
    (for [x (range ox (inc dx))
          y (range oy (inc dy))]
      [x y])))

(def points
  (->> plines
       (map (partial partition 2 1))
       (mapcat (partial map pline->points))
       (apply concat)))

(def g "#")
(def s "o")
(def max-x (apply max (map first points)))
(def max-y (apply max (map second points)))
(def grid
  (mapv (fn [_] (vec (repeat (inc max-x) ".")))
        (vec (repeat (+ max-y 3) "."))))

(def ground
  (->>
   (reduce (fn [grid [x y]] (assoc-in grid [y x] "#")) grid points)
   (s/transform [s/LAST s/ALL] (constantly "#"))))

(def reservoir
  (loop [[x y] sand-origin ground ground dropped 0]
    (match [(> dropped 21131) (get-in ground [y (dec x)]) (get-in ground [y x]) (get-in ground [y (inc x)] "#")]
      [true _ _ _] ground
      [false _ "." _] (recur [x (inc y)] ground dropped)
      [false "." (:or "o" "#") _] (recur [(dec x) (inc y)] ground dropped)
      [false (:or "o" "#") (:or "o" "#") "."] (recur [(inc x) (inc y)] ground dropped)
      [false (_ :guard #(or (= % "#") (= % "o"))) (_ :guard #(or (= % "#") (= % "o"))) (_ :guard #(or (= % "#") (= % "o")))] (recur sand-origin (assoc-in ground [(dec y) x] "o") (inc dropped)))))


(spit "ground.txt"
      (apply str (interleave (map (partial apply str) reservoir) (cycle "\n"))))