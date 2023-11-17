(ns years.2022.day17
  (:require [clojure.core.match :as m]
            util
            [clojure.string :as string]
            [com.rpl.specter :as s])
  (:use debux.core))

(def input ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>" #_(string/trim-newline (util/read 17 2022)))
(def turns 2022)
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

;; left-most rock is 2 away from left
;; bottom-most rock is 3 away from bottom
;; cycles between push and fall
(def state {:lines (list shaft)
            :jets (cycle jets)
            :shapes (cycle shapes)})
(defn turn [{:keys [lines jets shapes]}]
  (let [[shape & rest-shapes] shapes
        pushed (reduce maybe-push shape (take 3 jets)) ;; is 3 right?
        span (count pushed)
        padded-lines (vec (concat (repeat span 0) lines))
        parts (partition span 1 padded-lines)]
    (loop [pushed pushed [part & rest-parts] parts prev (cycle [0]) prev-index -1 [jet & rest-jets] (drop 3 jets)]
      (if (collides? pushed part)
        {:lines (drop-while zero? (merge-in prev-index (+ prev-index span) pushed padded-lines))
         :jets rest-jets
         :shapes rest-shapes}
        (recur (maybe-push part pushed jet) rest-parts part (inc prev-index) rest-jets)))))

;; [1 2 3 4 5]
;; span 3
;; [1 2 3] [2 3 4] [3 4 5]

;; [1 1] span 2
;; [0 0 0 0 0]
;; 0-1 1-2 2-3 3-4 
;; [0 0] [0 0] [0 0] [0 0]
;; [0 0] [0 0] [0 0] [1 1]

;; if coll merge with previous?
;; be careful with the jets

(def part1 (height (:lines (nth (iterate turn state) turns))))