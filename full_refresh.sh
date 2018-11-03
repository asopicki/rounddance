#!/bin/bash
# This is a small shell script do to convert all Markdown cuesheets in the
# repository into the HTML version overwriting the current HTML version
# if it exists

cd `dirname $0`
basedir=`pwd`

#find . -mindepth 2 -name \*.md -exec ./md2html.py \{\} \;

#cd scripts && python cuesheetlib.py

cd $basedir 

#/home/alex/tools/cuesheetlibrary/bin/CuesheetLibrary $basedir

export DATABASE_URL='/home/alex/.local/share/library.db'
/home/alex/cuer_manager/cuecard_indexer $basedir
