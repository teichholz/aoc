(ns years.2022.day17
  (:require [clojure.core.match :as m]
            util
            [clojure.string :as string])
  (:use debux.core))

(def input ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>" #_(string/trim-newline (util/read 17 2022)))
(def turns 2022)
(def shapes [[2r0011110] [2r0001000 2r0011100 2r0001000] [2r0000100 2r0000100 2r0011100] [2r0010000 2r0010000 2r0010000 2r0010000] [2r0011000 2r0011000]])
(def shaft 2r1111111)
(def jets (map (fn [c] (m/match c \> :right \< :left)) input))

;; this probably is buggy
(defn collides? [line*s shape]
  (cond (coll? line*s) (some #(collides? % shape) line*s)
        (nil? line*s) false
        :else (some (fn [[i shape]] (if (not (zero? (bit-and shape line*s))) i false)) (map-indexed list shape))))
(defn push-right [shape] (map #(bit-shift-right % 1) shape))
(defn push-left [shape]  (map #(bit-shift-left % 1) shape))
(defn bit-set? [n shape] (some true? (map #(bit-test % n) shape)))
(def right-border? (partial bit-set? 0))
(def left-border? (partial bit-set? 6))
(defn right-block? [shape lines] (or (right-border? shape) (collides? lines (push-right shape))))
(defn left-block? [shape lines] (or (left-border? shape) (collides? lines (push-left shape))))
(defn maybe-push [shape jet]
  (m/match jet
    :right (if (right-border? shape) shape (push-right shape))
    :left (if (left-border? shape) shape (push-left shape))))
(defn maybe-push' [lines shape jet]
  (m/match jet
    :right (if (right-block? shape lines) shape (push-right shape))
    :left (if (left-block? shape lines) shape (push-left shape))))
(defn height [lines] (dec (count (drop-while zero? lines)))) ;; dec because of the shaft
(defn merge [shape lines] (map bit-or shape (concat lines (cycle [0]))))

;; left-most rock is 2 away from left
;; bottom-most rock is 3 away from bottom
;; cycles between push and fall
(def state {:lines (list shaft)
            :jets (cycle jets)
            :shapes (cycle shapes)})
(defn turn [{:keys [lines jets shapes]}]
  (let [[shape & rest-shapes] shapes
        pushed (reduce maybe-push shape (take 4 jets))]
    (loop [shape pushed [jet & rest-jets] (drop 4 jets) [line & rest-lines] lines dropped-lines []]
      (if-let  [i (collides? line shape)] ;; my collide simulates dropping, so I need to use jets here as well
        (let [intersection (concat (take-last (- (count shape) i) dropped-lines) (take i lines))
              pushed (if (> i 0) (reduce (partial maybe-push' intersection) shape (take i jets)) shape)]
          {:lines (concat (drop-last (- (count pushed) i) dropped-lines) (merge pushed intersection) (drop i lines))
           :jets (drop i rest-jets)
           :shapes rest-shapes})
        (let [pushed (maybe-push' (or (take-last (count shape) dropped-lines) []) shape jet)] ;; this might be wrong
          (recur pushed rest-jets rest-lines (conj dropped-lines line)))))))

(def part1 (height (:lines (nth (iterate turn state) turns))))