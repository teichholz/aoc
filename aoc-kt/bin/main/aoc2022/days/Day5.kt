package aoc2022.days

import Day
import com.github.h0tk3y.betterParse.combinators.or
import com.github.h0tk3y.betterParse.combinators.separatedTerms
import com.github.h0tk3y.betterParse.combinators.times
import com.github.h0tk3y.betterParse.combinators.unaryMinus
import com.github.h0tk3y.betterParse.combinators.use
import com.github.h0tk3y.betterParse.grammar.Grammar
import com.github.h0tk3y.betterParse.grammar.parseToEnd
import com.github.h0tk3y.betterParse.lexer.literalToken
import com.github.h0tk3y.betterParse.lexer.regexToken
import com.github.h0tk3y.betterParse.parser.Parser
import okio.BufferedSource

data class Move(val quantity: Int, val from: Int, val to: Int)
data class In(val stacks: List<ArrayDeque<Char>>, val moves: List<Move>)

inline fun <T> zip(vararg lists: List<T>): List<List<T>> {
    return zip(*lists, transform = { it })
}

fun <T, V> zip(vararg lists: List<T>, transform: (List<T>) -> V): List<V> {
    val minSize = lists.map(List<T>::size).min()
    val list = ArrayList<V>(minSize)

    val iterators = lists.map { it.iterator() }
    var i = 0
    while (i < minSize) {
        list.add(transform(iterators.map { it.next() }))
        i++
    }

    return list
}

fun <T> ArrayDeque<T>.move(other: ArrayDeque<T>, quantity: Int) {
    repeat(quantity) {
        val crate = removeFirst()
        other.addFirst(crate)
    }
}

fun interprete(stacks: List<ArrayDeque<Char>>, move: Move) {
    val from = stacks[move.from - 1]
    val to = stacks[move.to - 1]

    from.move(to, move.quantity)
}

fun interprete2(stacks: List<ArrayDeque<Char>>, move: Move) {
    val from = stacks[move.from - 1]
    val to = stacks[move.to - 1]

    val stack = ArrayDeque<Char>()

    from.move(stack, move.quantity)
    stack.move(to, move.quantity)
}


fun main() {
    Day5().solve()
}

class Day5: Day<In>(5, 2022) {
    override fun part1(input: In): Any {
        input.moves.forEach {
            interprete(input.stacks, it)
        }

        return input.stacks.map { it.first() }.joinToString(separator = "")
    }

    override fun part2(input: In): Any {
        input.moves.forEach {
            interprete2(input.stacks, it)
        }

        return input.stacks.map { it.first() }.joinToString(separator = "")
    }

    object StacksParser : Grammar<List<Char?>>() {
        val lpar by literalToken("[")
        val rpar by literalToken("]")
        val word by regexToken("[A-Z]")
        val sep by literalToken(" ")
        val crate by -lpar * word * -rpar
        val noCrate by -lpar * sep * -rpar

        val crateParser: Parser<Char> by crate use { text[0] }
        val noCrateParser: Parser<Char?> by noCrate use { null }
        val maybeCreateParser: Parser<Char?> by noCrateParser or crateParser
        val cratesParser: Parser<List<Char?>> by separatedTerms(maybeCreateParser, sep)

        override val rootParser: Parser<List<Char?>> = cratesParser
    }

    object MoveParser : Grammar<Move>() {
        val move by literalToken("move")
        val from by literalToken("from")
        val to by literalToken("to")
        val num by regexToken(" (\\d+) ?")

        val moveParser: Parser<Move> by -move * num * -from * num * -to * num use {
            Move(t1.text.trim().toInt(), t2.text.trim().toInt(), t3.text.trim().toInt())
        }

        override val rootParser: Parser<Move> = moveParser
    }

    override fun parse(source: BufferedSource): In {
        return source.run {
            val first = mutableListOf<String>()
            val second = mutableListOf<String>()
            var use = first

            while (true) {
                val line = readUtf8Line() ?: break

                if (line.isEmpty()) {
                    use.removeLast()
                    use = second
                    continue
                }

                use.add(line)
            }

            val stacks = first.map {
                StacksParser.parseToEnd(it)
            }.let { zip(*it.toTypedArray()) }
             .map { it.filterNotNull() }

            val moves = second.map {
                MoveParser.parseToEnd(it)
            }

            In(stacks.map { ArrayDeque(it) }, moves)
        }
    }

}