package aoc2022.days

import Day
import com.github.h0tk3y.betterParse.grammar.parseToEnd
import okio.BufferedSource

fun main() {
    Day7S().solve()
}

class Day7S : Day<List<Command>>(7, 2022) {
    override fun part1(input: List<Command>): Any {
        val dirs = mutableMapOf("/" to 0)
        val history = ArrayDeque<String>()
        history.add("/")

        input.drop(1).forEach {
            when (it) {
                is Command.Cd -> {
                    when (it.path) {
                        ".." -> {
                            history.removeLast()
                        }
                        else -> {
                            history.addLast(history.last() + "/" + it.path)
                        }
                    }
                }
                is Command.Ls -> {
                    it.output.forEach { out ->
                        if (out.size >= 0) {
                            history.forEach { dir ->
                                dirs[dir] = (dirs[dir] ?: 0) + out.size
                            }
                        }
                    }
                }
            }
        }

        println(dirs)

        return dirs.values.filter {
            it <= 100_000
        }.sum()
    }

    override fun part2(input: List<Command>): Any {
        return "TODO"
    }

    override fun parse(source: BufferedSource): List<Command> = source.run {
        CommandParser.parseToEnd(readUtf8())
    }

}