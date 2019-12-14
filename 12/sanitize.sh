#!/bin/sh

cat input.txt | sed -e 's/..=//g' -e 's/>//' > sanitized.txt
