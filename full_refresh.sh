#!/bin/bash
# This is a small shell script do to convert all Markdown cuesheets in the
# repository into the HTML version overwriting the current HTML version
# if it exists

cd `dirname $0`

find . -mindepth 2 -name \*.md -exec ./md2html.py \{\} \;
