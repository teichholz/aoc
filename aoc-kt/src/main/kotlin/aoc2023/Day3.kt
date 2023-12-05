package aoc2023

import Day
import okio.BufferedSource


fun main() {
    val day = Day3()
    day.solve()
}

typealias CGrid = List<String>

fun pp(grid: CGrid): String {
    return grid.joinToString(separator = "\n")
}

data class PartNumber(val number: Int, val adjacent: Set<Pair<Int, Int>>)

class Day3 : Day<CGrid>(3, 2023) {

    override fun part1(input: CGrid): Any {
        val padded = pad(input)

        return parseParts(input).filter { (_, adjacent) ->
            adjacent.any { (row, col) -> padded[row][col] != '.' }
        }.sumOf { it.number }
    }

    override fun part2(input: CGrid): Any {
        val padded = pad(input)

        val numbers: List<PartNumber> = parseParts(input)
        val stars: List<Pair<Int, Int>> = padded.flatMapIndexed { rowi, row ->
            val matches = "\\*".toRegex().findAll(row)
            matches.map { match -> rowi to match.range.first }
        }

        return stars.sumOf {star ->
            val nums = numbers.filter { part ->
                part.adjacent.contains(star)
            }
            if (nums.size == 2) {
                nums[0].number * nums[1].number
            } else {
                0
            }
        }
    }

    fun parseParts(input: CGrid): List<PartNumber> {
        val padded = pad(input)

        return padded.flatMapIndexed { rowi, row ->
            val matches = "\\d+".toRegex().findAll(row)
            matches.map { match ->
                val value: Int = Integer.parseInt(match.value)
                val xs = match.range
                val block = listOf(-1, 0, 1).flatMap { drow ->
                    (setOf(match.range.first - 1) + xs + setOf(match.range.last + 1)).map { col ->
                        rowi + drow to col
                    }
                }.toSet()
                PartNumber(value, block - xs.map { rowi to it }.toSet())
            }
        }
    }

    fun pad(grid: CGrid): CGrid {
        val colPad = grid.map { ".$it." }
        val size = colPad[0].length
        val padLine = ".".repeat(size)

        return listOf(padLine) + colPad + listOf(padLine)
    }

    override fun parse(source: BufferedSource): CGrid {
        return source.run {
            val lines = mutableListOf<String>()
            while (true) {
                val line = readUtf8Line() ?: break
                lines.add(line)
            }
            lines
        }
    }

}