(ns years.2022.day17
  (:require [clojure.core.match :as m]
            util
            [clojure.string :as string]
            [com.rpl.specter :as s])
  (:use debux.core))

(def input (string/trim-newline (util/read 17 2022)))
(def turns 2022)
(def turns2 1000000000000)
(def shapes [[2r0011110] [2r0001000 2r0011100 2r0001000] [2r0000100 2r0000100 2r0011100] [2r0010000 2r0010000 2r0010000 2r0010000] [2r0011000 2r0011000]])
(def shaft 2r1111111)
(def jets (map (fn [c] (m/match c \> :right \< :left)) input))

(defn collides? [lines shape] (some (complement zero?) (map bit-and shape lines)))
(defn push-right [shape] (map #(bit-shift-right % 1) shape))
(defn push-left [shape]  (map #(bit-shift-left % 1) shape))
(defn bit-set? [n shape] (some true? (map #(bit-test % n) shape)))
(def right-border? (partial bit-set? 0))
(def left-border? (partial bit-set? 6))
(defn right-block? [lines shape] (or (right-border? shape) (collides? lines (push-right shape))))
(defn left-block? [lines shape] (or (left-border? shape) (collides? lines (push-left shape))))
(defn maybe-push
  ([pred-r pred-l shape jet]
   (m/match jet
     :right (if (pred-r shape) shape (push-right shape))
     :left (if (pred-l shape) shape (push-left shape))))
  ([shape jet] (maybe-push right-border? left-border? shape jet))
  ([lines shape jet] (maybe-push (partial right-block? lines) (partial left-block? lines) shape jet)))
(defn height [lines] (dec (count (drop-while zero? lines))))
#_{:clj-kondo/ignore [:redefined-var]}
(defn merge [lines other-lines] (vec (map bit-or lines (concat other-lines (cycle [0])))))
(defn merge-in [start end-exc shape all-lines] (s/setval (s/srange start end-exc) (merge shape (subvec all-lines start end-exc)) all-lines))
(defn pp [line*s]
  (cond (coll? line*s) (string/join "\n" (map pp line*s))
        :else (let [binary-string (apply str (map #(if (= % \1) \# \.) (Integer/toBinaryString line*s)))]
                (str (apply str (repeat (max 0 (- 7 (count binary-string))) \.)) binary-string))))

(def state {:lines (list shaft)
            :jets (cycle jets)
            :shapes (cycle shapes)})
(defn turn [{:keys [lines jets shapes]}]
  (let [[shape & rest-shapes] shapes
        pushed (reduce maybe-push shape (take 3 jets)) 
        span (count pushed)
        padded-lines (vec (concat (repeat span 0) lines))
        parts (partition span 1 padded-lines)]
    (loop [pushed pushed [part & rest-parts] parts prev-index -1 [jet & rest-jets :as all-jets] (drop 3 jets)]
      (if (collides? pushed part)
        {:lines (drop-while zero? (merge-in prev-index (+ prev-index span) pushed padded-lines))
         :jets all-jets
         :shapes rest-shapes}
        (recur (maybe-push part pushed jet) rest-parts (inc prev-index) rest-jets)))))

(def part1 (height (:lines (nth (iterate turn state) turns))))
;; maybe housekeep the lines whenever you have a 2r1111111 line and incrementally sum up the heights
;; (def part2 (height (:lines (nth (iterate turn state) turns2))))