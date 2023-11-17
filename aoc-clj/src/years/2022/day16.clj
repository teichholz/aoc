(ns years.2022.day16
  (:require util
            [ubergraph.core :as uber]
            [ubergraph.alg :as alg]
            [clojure.math.combinatorics :as combi]
            [com.rpl.specter :as s]
            [clojure.set :as set]))

(def input (util/read-lines 16 2022))
(defn parse [line]
  (let [matches (re-seq #"[A-Z][A-Z]|\d+" line)
        [valve cost & connections] (map read-string matches)]
    [(list valve cost) connections]))
(def connections (map parse input))

(def description
  (->> connections
       (mapcat (fn [[[valve flow] connections]]
                 [[[valve {:flow flow}]] (mapv #(vector valve %) connections)]))
       (apply concat)))
(def graph (apply uber/multigraph description))
(def !0-valves (filter #(> (uber/attr graph % :flow) 0) (uber/nodes graph)))
(defn path-cost [start end] (:cost (alg/shortest-path graph start end)))

(def state {:time 30
            :release 0
            :current 'AA
            :to-visit (set !0-valves)
            :visited #{'AA}})
(defn relieve [nodes] 
  (reduce + (map #(uber/attr graph % :flow) nodes)))
;; I first need to go here for current node then simulate
;; I can't just view every path as directly linked, I need to consider the path length
(defn sim-relieved [{:keys [current time visited]} [valve & _ :as nodes]]
  (let [arrival-time (- time (path-cost current valve))
        flows (for [node nodes] (if (visited node) 0 (uber/attr graph node :flow)))
        path-costs (map (partial apply path-cost) (partition 2 nodes))
        open-costs (map #(if (zero? %) 0 1) flows)
        time-reductions (reductions + (map + path-costs open-costs))
        pairs (map list flows (cons 0 time-reductions))
        relieves (map (fn [[cost time-reduction]] (* (- arrival-time 1 time-reduction) cost)) pairs)]
   (reduce + relieves)))
(defn max-release [{:keys [time release current to-visit visited] :as state}]
  (let [_ (println state)
        paths (map (comp alg/nodes-in-path #(alg/shortest-path graph current %)) to-visit)
        perms (s/select [s/ALL s/ALL] (map combi/permutations paths))
        perms' (filter #(not= (first %) current) perms)
        relieves (map (juxt (partial sim-relieved state) identity) perms')
        [_ [head & rest :as best]] (apply util/max-by first relieves)
        head-path-cost (path-cost current head)
        relieved (* head-path-cost (relieve visited))] 
    (println best)
    (println (sim-relieved state best))
    (cond 
      (= (set !0-valves) visited) (+ release relieved (* time (relieve visited))) 
      (< time (+ head-path-cost 2)) (+ release relieved (* time (relieve visited))) 
      :else (max-release {:time (- time head-path-cost 1)
                          :release (+ release relieved)
                          :current head
                          :to-visit (set/difference to-visit #{head}) 
                          :visited (conj visited head)}))
    ))
