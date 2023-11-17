package aoc2022.days

import Day
import okio.BufferedSource
import readDay
import java.math.BigDecimal


data class Monkey(
    val items: MutableList<Int>,
    val op: (Int) -> Int,
    val pred: Int,
    val thn: Int,
    val els: Int
)

fun main() {
    Day11().solve()
}

class Day11 : Day<List<Monkey>>(11, 2022) {
    override fun part1(input: List<Monkey>): Any {
        val inspects: MutableMap<Int, Int> = mutableMapOf()

        repeat(20) {
            for (i in 0..input.size) {
                val monki = i % input.size
                val monk = input[monki]
                val toRemove = mutableListOf<Int>()
                for (item in monk.items) {
                    inspects[monki] = (inspects[monki] ?: 0) + 1
                    toRemove.add(item)
                    val newItem = monk.op(item) / 3
                    if (newItem % monk.pred == 0) {
                        input[monk.thn].items.add(newItem)
                    } else {
                        input[monk.els].items.add(newItem)
                    }
                }
                monk.items.removeAll(toRemove)
            }
        }

        return inspects.values.sorted().takeLast(2).reduce(Int::times)
    }

    override fun part2(input: List<Monkey>): Any {
        val modulo = input.map {it.pred}.reduce(Int::times)
        val inspects: MutableMap<Int, Long> = mutableMapOf()

        repeat(10_000) {
            for (i in 0..input.size) {
                val monki = i % input.size
                val monk = input[monki]
                val toRemove = mutableListOf<Int>()
                for (item in monk.items) {
                    inspects[monki] = (inspects[monki] ?: 0) + 1
                    toRemove.add(item)
                    val newItem = monk.op(item) % modulo
                    if (newItem % monk.pred == 0) {
                        input[monk.thn].items.add(newItem)
                    } else {
                        input[monk.els].items.add(newItem)
                    }
                }
                monk.items.removeAll(toRemove)
            }
        }

        return inspects.values.sorted().takeLast(2).map(BigDecimal::valueOf).reduce(BigDecimal::times)
    }

    override fun parse(source: BufferedSource): List<Monkey> =  source.run {
        val monkeys = mutableListOf<Monkey>()

        while (true) {
            val monk = readUtf8Line() ?: break
            val items = readUtf8Line() ?: break
            val op = readUtf8Line() ?: break
            val pred = readUtf8Line() ?: break
            val thn = readUtf8Line() ?: break
            val els = readUtf8Line() ?: break

            fun addMonkey() {
                val items = items.split(": ")[1].split(", ").mapTo(mutableListOf()) { it.toInt() }
                val op: (Int) -> Int = when {
                    "*" in op -> { x ->
                        op.split(" * ")[1].let {
                            if (it == "old") {
                                x * x
                            } else {
                                x * it.toInt()
                            }
                        }
                    }
                    "+" in op -> { x -> x + op.split(" + ")[1].toInt() }
                    else -> throw Exception("Unknown op")
                }
                val pred = pred.split(" by ")[1].toInt()
                val thn = thn.split(" monkey ")[1].toInt()
                val els = els.split(" monkey ")[1].toInt()


                monkeys.add(Monkey(items, op, pred, thn, els))
            }

            addMonkey()
            readUtf8Line() ?: break
        }

        monkeys
    }
}