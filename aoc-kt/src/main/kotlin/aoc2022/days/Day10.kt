package aoc2022.days

import Day
import okio.BufferedSource
import readDay
import kotlin.math.absoluteValue

fun main() {
    Day10().solve()
}

sealed interface Op {
    data object Noop : Op
    data class Addx(val x: Int) : Op
}

class Day10 : Day<List<Op>>(10, 2022) {

    class CPU(val observe: CPU.() -> Unit) {
        var cycle = 0
        var register = 1

        fun cycle() {
            cycle += 1
            observe(this)
        }

        fun run(op: Op) {
            when (op) {
                is Op.Noop -> {
                    cycle()
                }
                is Op.Addx -> {
                    cycle()
                    cycle()
                    register += op.x
                }
            }
        }
    }

    override fun part1(input: List<Op>): Any {
        var strength = 0

        val cpu = CPU {
            if ((cycle - 20) % 40 == 0 && cycle <= 220) {
                strength += cycle * register
            }
        }
        input.forEach(cpu::run)

        return strength
    }

    override fun part2(input: List<Op>): Any {
        val CRT = mutableListOf<Char>()
        val cpu = CPU {
            if ((register - (cycle % 40) + 1).absoluteValue <= 1) {
                CRT.add('#')
            } else {
                CRT.add('.')
            }
        }
        input.forEach(cpu::run)

        return CRT.chunked(40).map { it.joinToString("") }.joinToString("\n")
    }

    override fun parse(source: BufferedSource): List<Op> = source.run {
        val ops = mutableListOf<Op>()

        while (true) {
            val line = readUtf8Line() ?: break
            if (line == "noop") {
                ops.add(Op.Noop)
            } else {
                val (_, arg) = line.split(" ")
                ops.add(Op.Addx(arg.toInt()))
            }
        }

        ops
    }

}