package aoc2022.days

import Day
import com.github.h0tk3y.betterParse.combinators.oneOrMore
import com.github.h0tk3y.betterParse.combinators.or
import com.github.h0tk3y.betterParse.combinators.times
import com.github.h0tk3y.betterParse.combinators.unaryMinus
import com.github.h0tk3y.betterParse.combinators.use
import com.github.h0tk3y.betterParse.combinators.zeroOrMore
import com.github.h0tk3y.betterParse.grammar.Grammar
import com.github.h0tk3y.betterParse.grammar.parseToEnd
import com.github.h0tk3y.betterParse.grammar.parser
import com.github.h0tk3y.betterParse.lexer.literalToken
import com.github.h0tk3y.betterParse.lexer.regexToken
import com.github.h0tk3y.betterParse.parser.Parser
import okio.BufferedSource

sealed interface IFile {
    val name: String
    val size: Int

    data class File(override val name: String, override val size: Int) : IFile
    data class Folder(override val name: String, val files: Set<IFile> = mutableSetOf()) : IFile {
        override val size: Int
            get() = files.sumOf { it.size }
    }
}

fun IFile.pp(indent: Int = 0): String {
    return when (this) {
        is IFile.File -> " ".repeat(indent) + "- $name (file, $size)"
        is IFile.Folder -> {
            " ".repeat(indent) + "- $name (dir)\n" + files.joinToString("\n") { it.pp(indent + 2) }
        }
    }
}

fun IFile.Folder.addFile(file: IFile) {
    (this.files as MutableSet).add(file)
}

class Context {
    val root = IFile.Folder("/")

    var currentFolder: IFile.Folder = root
    var history: List<IFile.Folder> = listOf(root)

    fun execute(command: Command) {
        when (command) {
            is Command.Ls -> {
                command.output.forEach {
                    val unseen = !currentFolder.files.map { it.name }.contains(it.name)

                    if (unseen) {
                        if (it.size < 0 /* dir marker */) {
                            currentFolder.addFile(IFile.Folder(it.name))
                        } else /* file */ {
                            currentFolder.addFile(IFile.File(it.name, it.size))
                        }
                    }
                }
            }

            is Command.Cd -> {
                if (command.path == "..") {
                    if (currentFolder == root) {
                        return
                    }

                    history = history.dropLast(1)
                    currentFolder = history.last()
                } else {
                    if (command.path == "/") {
                        currentFolder = root
                        history = listOf(root)
                        return
                    }

                    val folder = currentFolder.files.filterIsInstance<IFile.Folder>().firstOrNull {
                        it.name == command.path
                    } ?: IFile.Folder(command.path).also { currentFolder.addFile(it) }
                    currentFolder = folder
                    history = history + folder
                }
            }
        }
    }

    fun findAtMost(size: Int): List<IFile.Folder> = find({ it.size <= size })


    /**
     * Pretty inefficient, but it works
     */
    fun find(pred: (IFile.Folder) -> Boolean, folder: IFile.Folder = root): List<IFile.Folder> {
        val folders = folder.files.filterIsInstance<IFile.Folder>()

        val found = folders.filter(pred)

        return found + folders.flatMap { find(pred, it) }
    }
}

sealed interface Command {
    data class LsOutput(val size: Int, val name: String)
    data class Ls(val output: List<LsOutput>) : Command
    data class Cd(val path: String) : Command
}

object CommandParser : Grammar<List<Command>>() {
    val SPACE by literalToken(" ", ignore = true)
    val NEWLINE by literalToken("\n", ignore = true)

    val dollar by literalToken("$")
    val cd by literalToken("cd")
    val ls by literalToken("ls")
    val dir by literalToken("dir")
    val number by regexToken("\\d+")
    val path by regexToken("[/a-zA-Z.]+")

    val cdParser by -dollar * -cd * path use { Command.Cd(text) }
    val lsOutputParser by (number or dir) * path use {
        Command.LsOutput(t1.text.let { if (it == "dir") -1 else it.toInt() }, t2.text)
    }
    val lsParser by -dollar * -ls * zeroOrMore(parser { lsOutputParser }) use {
        Command.Ls(this)
    }
    val commandParser = cdParser or lsParser
    val commandsParser by oneOrMore(commandParser)

    override val rootParser: Parser<List<Command>>
        get() = commandsParser
}

fun main() {
    Day7().solve()
}

class Day7 : Day<List<Command>>(7, 2022) {
    override fun part1(input: List<Command>): Any {
        val ctx = Context()
        input.forEach {
            ctx.execute(it)
        }

        return ctx.findAtMost(100_000).sumOf { it.size }
    }

    override fun part2(input: List<Command>): Any {
        val ctx = Context()
        input.forEach {
            ctx.execute(it)
        }

        return ctx.find({ it.size >= ctx.root.size - 40_000_000 }).map { it.size }.min()
    }

    override fun parse(source: BufferedSource): List<Command> = source.run {
        CommandParser.parseToEnd(readUtf8())
    }

}