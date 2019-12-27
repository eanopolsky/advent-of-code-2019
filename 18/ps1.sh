#!/bin/sh

rm solve1.speedscope
py-spy record -f speedscope -o solve1.speedscope ./solve1.py
