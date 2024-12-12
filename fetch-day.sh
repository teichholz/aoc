#!/bin/bash

YEAR=$1
DAY=$2
DIR="./input/$YEAR"

print-usage () {
    echo "Usage: fetch-day.sh <year> <day>"
    exit 1
}

if [[ -z "$YEAR" || -z $DAY ]] ; then
    print-usage
fi

if [[ -z "$AOCSESSION" ]] ; then 
    echo "AOCSESSION not set" && exit 1
fi

if [[ $DAY =~ ([0-9]+)-([0-9]+) ]] ; then
    START=${BASH_REMATCH[1]}
    END=${BASH_REMATCH[2]}
else 
    START=$DAY
    END=$DAY
fi

fetch-day () {
    local y=$1
    local d=$2

    local file="$DIR/$d"
    local url="https://adventofcode.com/$y/day/$d/input"

    curl -o "$file" -H "Cookie: session=$AOCSESSION" "$url"
    if [[ $? ]] ; then
        echo "Fetched Year $y Day $d"
    else
        echo "Failed to fetch Year $y Day $d"
    fi
}

mkdir -p "$DIR"

for ((DAY="$START";DAY<="$END";DAY++)); do
    fetch-day "$YEAR" $DAY
done
