#!/usr/bin/env python
###
# Input md2html.py <cuesheetfile>
# - cuesheetfile - file in markdown format
###
import sys
import re
import logging
import os.path as path
import subprocess

logging.basicConfig(level=logging.DEBUG)
TITLE_PATTERN = re.compile('^#\s+(?P<title>.*)$')
META_PATTERN = re.compile('^\*\s+\*\*(?P<metaname>\w+)\*\*\:\s+(?P<metatext>.*)$')

inputfile = sys.argv[1]

meta = {'title': None, 'author': None, 'description': None}

# - Extract information from file
with open(inputfile) as input:
    for line in input.readlines(4096):
        #extract title of the dance
        if (not meta['title']):
            result = TITLE_PATTERN.match(line)
            if (result):
                meta['title'] = result.group('title')
        #extract the author information
        if (not meta['author']):
            result = META_PATTERN.match(line)
            if (result and result.group('metaname') == 'Choreographer'):
                meta['author'] = result.group('metatext')
        #extract some keywords like the dance and phase of the dance
        if (not meta['description']):
            result = META_PATTERN.match(line)
            if (result and result.group('metaname') == 'Dance'):
                meta['description'] = result.group('metatext')


logging.debug('Title: %s' % meta['title'])
logging.debug('Author: %s' % meta['author'])
logging.debug('Description: %s' % meta['description'])

filename = path.join(path.dirname(inputfile), path.basename(inputfile).rstrip('.md')+'.html')
logging.debug(filename)
# - Open html output file
with open(filename, 'w') as outputfile:
    # - Write html header to file
    outputfile.write("<!DOCTYPE html>\r\n")
    outputfile.write("<html lang=\"en\">\r\n")
    outputfile.write("<head>\r\n")
    outputfile.write("<meta charset=\"utf-8\">\r\n")
    outputfile.write("<title>%s</title>\r\n" % meta['title'])
    outputfile.write("<meta name=\"author\" content=\"%s\">\r\n" % meta['author'])
    outputfile.write("<meta name=\"description\" content=\"%s\">\r\n" % meta['description'])
    outputfile.write("<body>\r\n")

    # - Write markdown output to file
    html = subprocess.check_output(["markdown", inputfile])
    outputfile.write(html)

    # - Add closing html markup to file
    outputfile.write("</body>\r\n")
    outputfile.write("</html>\r\n")
