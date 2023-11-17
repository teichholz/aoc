package aoc2022.days

import Day
import okio.BufferedSource

typealias Pos = Pair<Int, Int>
typealias Grid<T> = List<List<T>>

operator fun Int.plus(other: Int?): Int? = if (other != null) this + other else null

operator fun <T> Grid<T>.get(pos: Pos): T {
    return this[pos.first][pos.second]
}

fun Pos.neighbours(): List<Pos> = listOf(
    this.first - 1 to this.second,
    this.first + 1 to this.second,
    this.first to this.second - 1,
    this.first to this.second + 1,
)

fun Pos.neighbours(grid: Grid<Int>): List<Pos> = neighbours().filter {
    it.first >= 0 && it.first < grid.size && it.second >= 0 && it.second < grid[0].size && (grid[it] - grid[this]) <= 1
}

data class Hill(val grid: Grid<Int>, val start: Pos, val end: Pos)

fun main() {
    Day12().solve()
}

class Day12: Day<Hill>(12, 2022) {

    override fun part1(input: Hill): Any {
        val (grid, start, end) = input
        val q = ArrayDeque<Pos>()
        val visited = mutableSetOf<Pos>()
        val parents = mutableMapOf<Pos, Pos>()

        q.add(start)
        while (q.isNotEmpty()) {
            val pos = q.removeFirst()
            if (pos == end) { break }
            pos.neighbours(grid).forEach {
                if (it !in visited) {
                    q.add(it)
                    visited.add(it)
                    parents[it] = pos
                }
            }
        }

        fun len(map: Map<Pos, Pos>, cur: Pos): Int? {
            if (cur == start) { return 0 }
            return 1 + map[cur]?.let { len(map, it) }
        }

        return len(parents, end) ?: Integer.MAX_VALUE
    }

    override fun part2(input: Hill): Any {
        val (grid, _, end) = input
        val starts = input.grid.flatMapIndexed { y, row ->
            row.mapIndexed { x, elevation ->
                if (elevation == 0) {
                    y to x
                } else {
                    null
                }
            }.filterNotNull()
        }
        return starts.map {
            part1(Hill(grid, it, end))
        }.minBy { it as Int }
    }

    override fun parse(source: BufferedSource): Hill = source.run {
        var start: Pos = 0 to 0
        var end: Pos = 0 to 0
        val grid = mutableListOf<List<Int>>()

        var y = 0
        while (true) {
            val line = readUtf8Line() ?: break
            grid.add(line.mapIndexed {x, char ->
                when (char) {
                    in 'a' .. 'z' -> char - 'a'
                    'S' -> { start = y to x; 0}
                    'E' -> { end = y to x; 25 }
                    else -> throw Exception("Unknown char $char")
                }
            })
            ++y
        }


        return Hill(grid, start, end)
    }

}