plugins {
    kotlin("jvm") version "1.9.0"
}

group = "aoc"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(kotlin("test"))
    implementation("com.squareup.okio:okio:3.6.0")
    implementation("com.github.h0tk3y.betterParse:better-parse:0.4.4")
}

tasks.test {
    useJUnitPlatform()
}

kotlin {
    jvmToolchain(8)
}