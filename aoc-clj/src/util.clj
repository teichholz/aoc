(ns util
  (:require [clojure.string :as string]) 
  (:import [clojure.lang IFn]))

(defn read [day year] 
  (slurp (str (System/getenv "HOME") "/git/aoc/input/" year "/" day)))

(defn read-lines [day year] 
  (->> (read day year)
       (string/split-lines)))

(def $ partial)

(defrecord point [x y]
  IFn
  (invoke [_] (fn [m] (get-in m [x y])))
  (invoke [_ m] (get-in m [x y]))
  (invoke [_ m default] (get-in m [x y] default)))
  
(defn max-by 
  ([f]
   (partial reduce (fn [x y] (if (> (f y) (f x)) y x))))
  ([f & more] 
   ((max-by f) more)))

(def side-print (fn [p] (let [evald (eval p)] evald)))