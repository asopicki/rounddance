#!/usr/bin/env python3
###
# Input md2html.py <cuesheetfile>
# - cuesheetfile - file in markdown format
###
import sys
import re
import logging
import os.path as path
import subprocess
import os
import fileinput

TITLE_PATTERN = re.compile('^#\s+(?P<title>.*)$')
META_PATTERN = re.compile('^\*\s+\*\*(?P<metaname>\w+)\*\*\:\s+(?P<metatext>.*)$')

meta = {
    'title': None,
    'author': None,
    'rhythm': None,
    'phase': None,
    'difficulty': None,
    'music': None,
    'description': None
}

metamappings = {
  'Choreographer': 'author',
  'Dance': 'description',
  'Rhythm': 'rhythm',
  'Phase': 'phase',
  'Difficulty': 'difficulty',
  'Music': 'music',
}

def convert_inputfile(inputfile):
    markdowninput = open(inputfile, 'r')
    for line in markdowninput.readline(4096):
        #extract title of the dance
        result = TITLE_PATTERN.match(line)
        if result and not meta['title']:
            meta['title'] = result.group('title')

        #extract additional meta information
        result = META_PATTERN.match(line)

        if result and result.group('metaname') in metamappings:
            metakey = metamappings[result.group('metaname')]
            if not meta[metakey]:
                meta[metakey] = result.group('metatext')
                
        if line.lower().startswith("# intro"):
            break;

    logging.debug('Title: %s' % meta['title'])

    for (key, metakey) in metamappings.items():
        logging.debug('%s: %s' % (key, meta[metakey]))

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
        outputfile.write(html.decode("utf-8"))

        # - Add closing html markup to file
        outputfile.write("</body>\r\n")
        outputfile.write("</html>\r\n")


if __name__ == '__main__':

    if 'MD2HTML_DEBUG' in os.environ:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if len(sys.argv) == 1:
        sys.exit("Path to input file expected as argument!")

    convert_inputfile(sys.argv[1])
