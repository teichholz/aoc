import okio.BufferedSource
import okio.FileSystem
import okio.Path.Companion.toPath
import okio.buffer

fun <T> readDay(year: Int, day: Int, block: BufferedSource.() -> T): T {
    val home = System.getenv("HOME").toPath()
    val path = home.resolve("git/aoc/input/$year/$day".toPath())

    FileSystem.SYSTEM.source(path).use { fileSource ->
        fileSource.buffer().use { bufferedFileSource ->
            return block(bufferedFileSource)
        }
    }
}

abstract class Day<T>(val day: Int, val year: Int) {
    abstract fun part1(input: T): Any
    abstract fun part2(input: T): Any
    abstract fun parse(source: BufferedSource): T

    fun solve () {
        println("Part 1:\n${part1(readDay(year, day) { parse( this) })}")
        println("Part 2:\n${part2(readDay(year, day) { parse( this) })}")
    }
}