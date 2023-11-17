package aoc2022.days

import Day
import okio.BufferedSource
import readDay
import kotlin.math.absoluteValue
import kotlin.math.sign


fun follow(head: Pair<Int, Int>, tail: Pair<Int, Int>): Pair<Int, Int> {
    val (x, y) = head
    val (tx, ty) = tail
    val (dx, dy) = x - tx to y - ty
    val follow = (x - tx).absoluteValue > 1 || (y - ty).absoluteValue > 1
    return if (follow) { tx + dx.sign to ty + dy.sign } else { tail }
}

fun main() {
    Day9().solve()
}

class Day9 : Day<List<Pair<Int, Int>>>(9, 2022) {
    override fun part1(input: List<Pair<Int, Int>>): Any {
        var head = 0 to 0
        var tail = 0 to 0
        val positions = mutableSetOf(tail)
        input.forEach {
            head = head.first + it.first to head.second + it.second
            var prev: Pair<Int, Int>
            do {
                prev = tail
                tail = follow(head, tail)
                positions.add(tail)
            } while (prev != tail)
        }


        return positions.size
    }

    override fun part2(input: List<Pair<Int, Int>>): Any {
        return "TODO"
    }

    override fun parse(source: BufferedSource): List<Pair<Int, Int>> = source.run {
        val motions = mutableListOf<Pair<Int, Int>>()

        while (true) {
            val line = readUtf8Line() ?: break
            val (direction, amount) = line.split(" ")
            val i = amount.toInt()
            when (direction) {
                "U" -> motions.add(0 to -i)
                "D" -> motions.add(0 to i)
                "L" -> motions.add(-i to 0)
                "R" -> motions.add(i to 0)
            }
        }

        motions
    }

}