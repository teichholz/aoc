package aoc2022.days

import Day
import okio.BufferedSource
import readDay

fun main() {
    Day6().solve()
}

class Day6 : Day<String>(6, 2022) {
    override fun part1(input: String): Any {
        val windows = input.windowed(4)
        val marker = windows.first {
            it.toSet().size == 4
        }
        val index = windows.indexOf(marker)
        return index + 4
    }

    override fun part2(input: String): Any {
        val windows = input.windowed(14)
        val marker = windows.first {
            it.toSet().size == 14
        }
        val index = windows.indexOf(marker)
        return index + 14
    }

    override fun parse(source: BufferedSource): String {
        return source.readUtf8()
    }

}