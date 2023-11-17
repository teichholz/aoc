package aoc2022.days

import Day
import okio.BufferedSource
import readDay


class Tree(val height: Int)

fun visible(line: List<Tree>): Set<Tree> {
    return buildSet {
        var max = -1
        line.forEach {
            if (it.height > max) {
                max = it.height
                add(it)
            }
        }
    }
}

fun distance(line: List<Tree>): Int {
    val house = line[0]
    var score = 0

    for (tree in line.drop(1)) {
        if (tree.height < house.height) {
            score += 1
        } else {
            return score + 1
        }
    }

    return score
}

fun main() {
    Day8().solve()
}

class Day8 : Day<List<List<Tree>>>(8, 2022) {
    override fun part1(input: List<List<Tree>>): Any {
        val lr = input.map {
            visible(it) + visible(it.reversed())
        }.reduce(Set<Tree>::union)
        val tb = zip(*input.toTypedArray()).map {
            visible(it) + visible(it.reversed())
        }.reduce(Set<Tree>::union)

        return (lr + tb).count()
    }

    override fun part2(input: List<List<Tree>>): Any {
        val rows = input
        val cols = zip(*input.toTypedArray())
        val ind = rows.size - 1

        return (0..ind).flatMap { x ->
            (0..ind).map { y ->
                distance(rows.get(x).drop(y)) *
                distance(cols.get(y).drop(x)) *
                distance(rows.get(x).reversed().drop(ind - y)) *
                distance(cols.get(y).reversed().drop(ind - x))
            }
        }.max()
    }

    override fun parse(source: BufferedSource): List<List<Tree>> = source.run {
        val grid = mutableListOf<List<Tree>>()

        while (true) {
            val line = readUtf8Line() ?: break
            val trees = mutableListOf<Tree>()
            line.forEach { trees.add(Tree(it.digitToInt())) }
            grid.add(trees)
        }

        grid
    }

}