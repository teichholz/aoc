package aoc2022.days

import Day
import okio.BufferedSource
import readDay

fun main() {
    Day1().solve()
}

class Day1 : Day<List<List<Int>>>(1, 2022) {

    override fun part1(input: List<List<Int>>): Int {
        val max = input.map {
            it.reduce(Int::plus)
        }.max()

        return max
    }

    override fun part2(input: List<List<Int>>): Int {
        val max = input.map {
            it.reduce(Int::plus)
        }.sortedDescending().take(3).sum()

        return max
    }

    override fun parse(source: BufferedSource): List<List<Int>> =
        source.run {
            val allCalories = mutableListOf<List<Int>>()
            val calories = mutableListOf<Int>()

            while (true) {
                val line = readUtf8Line() ?: break
                if (line.isNotEmpty()) {
                    calories.add(Integer.valueOf(line))
                } else {
                    allCalories.add(calories.toList())
                    calories.clear()
                }
            }

            allCalories
        }
}