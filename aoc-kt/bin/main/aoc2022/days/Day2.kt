package aoc2022.days

import Day
import aoc2022.days.Day2.Move
import okio.BufferedSource
import readDay

fun main() {
    Day2().solve()
}

class Day2 : Day<List<Pair<Move, Move>>>(2, 2022) {

    enum class Move {
        ROCK,
        PAPER,
        SCISSORS
    }

    fun Move.draw(other: Move) = this == other

    fun Move.counter() = when (this) {
        Move.ROCK -> Move.PAPER
        Move.PAPER -> Move.SCISSORS
        Move.SCISSORS -> Move.ROCK
    }

    fun Move.beats(other: Move): Boolean = this == other.counter()

    fun Move.points(): Int {
        return when (this) {
            Move.ROCK -> 1
            Move.PAPER -> 2
            Move.SCISSORS -> 3
        }
    }

    fun Move.toResult(other: Move): Move {
        return when (this) {
            Move.ROCK -> other.counter().counter()
            Move.PAPER -> other
            Move.SCISSORS -> other.counter()
        }
    }

    override fun part1(turns: List<Pair<Move, Move>>): Int {
        return turns.sumOf { (op, me) ->
            var points = me.points()
            if (me.beats(op)) {
                points += 6
            } else if (me.draw(op)) {
                points += 3
            }
            points
        }
    }

    override fun part2(turns: List<Pair<Move, Move>>): Int {
        return turns.sumOf { (op, me) ->
            val me = me.toResult(op)
            var points = me.points()
            if (me.beats(op)) {
                points += 6
            } else if (me.draw(op)) {
                points += 3
            }
            points
        }
    }

    override fun parse(source: BufferedSource): List<Pair<Move, Move>> =
        source.run {
            val turns = mutableListOf<Pair<Move, Move>>()

            while (true) {
                val line = readUtf8Line() ?: break
                val op: Move = when (line[0]) {
                    'A' -> Move.ROCK
                    'B' -> Move.PAPER
                    'C' -> Move.SCISSORS
                    else -> throw Exception("Invalid move")
                }
                val me: Move = when (line[2]) {
                    'X' -> Move.ROCK
                    'Y' -> Move.PAPER
                    'Z' -> Move.SCISSORS
                    else -> throw Exception("Invalid move")
                }

                turns.add(Pair(op, me))
            }

            turns
        }
}

