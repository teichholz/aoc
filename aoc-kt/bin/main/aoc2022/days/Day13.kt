package aoc2022.days

import Day
import okio.BufferedSource

typealias Two<T> = Pair<T, T>

sealed interface DeepList {
    data class Atom(val value: Int) : DeepList
    data class Seq(val list: List<DeepList>) : DeepList
}

fun DeepList.pp(): String = when (this) {
    is DeepList.Atom -> "$value"
    is DeepList.Seq -> "[${list.joinToString(",") { it.pp() }}]"
}

fun Int.deepSeqAtom(): DeepList.Atom = DeepList.Atom(this)
fun DeepList.deepen(): DeepList.Seq = DeepList.Seq(listOf(this))

fun DeepList.cmp(other: DeepList): Int = when (this) {
    is DeepList.Atom -> when (other) {
        is DeepList.Atom -> value compareTo other.value
        is DeepList.Seq -> deepen().cmp(other)
    }
    is DeepList.Seq -> when (other) {
        is DeepList.Atom -> cmp(other.deepen())
        is DeepList.Seq -> {
            val ordered = list.zip(other.list).map { (left, right) -> left.cmp(right) }
            var cmp: Int? = null
            for (i in ordered) { if (i < 0 || i > 0) { cmp = i; break; } }
            cmp ?: (list.size compareTo other.list.size)
        }
    }
}

fun main() {
    Day13().solve()
}

class Day13 : Day<List<Two<DeepList>>>(13, 2022) {
    override fun part1(input: List<Two<DeepList>>): Any {
        return input
            .map { (left, right) -> left.cmp(right) }
            .mapIndexed { i, ordered -> if (ordered < 0) i + 1 else 0 }
            .sum()
    }

    override fun part2(input: List<Two<DeepList>>): Any {
        val div1 = 2.deepSeqAtom().deepen().deepen()
        val div2 = 6.deepSeqAtom().deepen().deepen()
        return input
            .flatMap { (left, right) -> listOf(left, right) }
            .let { it + div1 + div2 }
            .sortedWith { a, b -> a.cmp(b) }
            .let { (it.indexOf(div1) + 1) * (it.indexOf(div2) + 1) }
    }

    override fun parse(source: BufferedSource): List<Two<DeepList>> = source.run {
        val lines = mutableListOf<Two<DeepList>>()
        while (true) {
            val left = readUtf8Line()!!
            val right = readUtf8Line()!!

            fun isList(str: String): Boolean = str.startsWith("[") && str.endsWith("]")
            fun parse(str: String): DeepList = if (isList(str)) {
                val content = str.drop(1).dropLast(1)
                val items: MutableList<String> = mutableListOf()
                var brackets = 0
                var lastChar = 0
                content.forEachIndexed { i, char ->
                    when (char) {
                        '[' -> brackets++
                        ']' -> brackets--
                        ',' -> {
                            if (brackets == 0) {
                                items.add(content.substring(lastChar, i))
                                lastChar = i + 1
                            }
                        }

                        else -> {}
                    }
                }
                items.add(content.substring(lastChar, content.length))

                DeepList.Seq(items.filter { it.isNotEmpty() }.map { parse(it) })
            } else {
                DeepList.Atom(str.toInt())
            }
            lines.add(parse(left) to parse(right))

            readUtf8Line() ?: break
        }

        lines
    }
}