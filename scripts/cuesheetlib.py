#!/usr/bin/env python
#############################
#
# A small tool which will generate an overview of the available cuesheets
# in the repository.
#
#   - dynamic overview page with filters
#
#############################

import os
import os.path
import re
from datetime import datetime
from json import dumps
from base64 import b64encode


metamappings = {
  'Choreographer': 'author',
  'Dance': 'description',
  'Rhythm': 'rhythm',
  'Phase': 'phase',
  'Difficulty': 'difficulty',
  'Music': 'music',
}

phasemapping = {
  'I': 0,
  'II': 1,
  'III': 2,
  'IV': 3,
  'V': 4,
  'VI': 5,
  'UNPHASED': 6
}

phasermapping = ['I', 'II', 'III', 'IV', 'V', 'VI', 'UNPHASED']

TITLE_PATTERN = re.compile('^#\s+(?P<title>.*)$')
META_PATTERN = re.compile('^\*\s+\*\*(?P<metaname>\w+)\*\*\:\s+(?P<metatext>.*)$')
PHASE_PATTERN = re.compile('^(I|II|III|IV|V|VI)\s*(\+.*)?$')

def _meta(cuesheetpath):
    meta = {
        'title': None,
        'author': None,
        'rhythm': None,
        'phase': None,
        'difficulty': None,
        'music': None,
        'description': None,
        '_phasekey': None,
        '_phasenumeric': 6
    }

    # - Extract information from file
    with open(cuesheetpath) as input:
        for line in input.readlines(4096):

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

    return meta

def _phase(phasedesc):
  if phasedesc != None:
    r = PHASE_PATTERN.match(phasedesc)

    if r:
      return r.group(1)

  return 'UNPHASED'

def _header(cuesheets):
  headerfile = open('header.tl')
  header = headerfile.read()
  headerfile.close()

  return header

def _list(cuesheets, phase, libpath):
  staticlist = "<ul id=\"phase%s\">\r\n" % phase

  for filename,meta in cuesheets.items():
    filename = os.path.relpath(filename, libpath).replace('.md', '.html')
    staticlist += "<li><a href=\"%s\" data-meta=\"%s\" class=\"cuesheet\" target=\"_blank\" rel=\"noopener noreferer\">%s %s</a></li>\r\n" % (
      filename,
      b64encode(dumps(meta)),
      meta['title'],
      meta['phase'])

    #print 'Phase: %s Title: %s' % (phase, meta['title'])

  return staticlist + "</ul>\r\n\r\n"

def _content(cuesheets, libpath):

  content = ''

  for idx,files in enumerate(cuesheets):
    content += "<div class=\"list\"><h2>Phase %s</h2>\r\n\r\n" % phasermapping[idx]

    content += _list(files, phasermapping[idx], libpath)

    content += "</div>\r\n"

  return content

def _footer():
  footerfile = open('footer.tl')
  footer = footerfile.read()
  footerfile.close()

  footer = footer.replace('###TIMESTAMP###', datetime.now().strftime('%x %X'))

  return footer


def cuesheetlist(libpath):
    cuesheets = [{}, {}, {}, {}, {}, {}, {}]

    dirs = os.walk(libpath)

    for path in dirs:
        if path[0] == libpath:
            continue

        if path[0].count('.git') > 0:
            continue

        for filename in path[2]:
            if filename.lower().endswith('.md'):
                cuesheetpath = os.path.join(path[0], filename)
                meta = _meta(cuesheetpath)
                meta['_phasekey'] = _phase(meta['phase'])
                meta['_phasenumeric'] = phasemapping[meta['_phasekey']]
                cuesheets[meta['_phasenumeric']][cuesheetpath] = meta

    return cuesheets

def generate(outfile, cuesheets, libpath):

  with open(outfile, 'w') as out:
    out.write(_header(cuesheets))
    out.write(_content(cuesheets, libpath))
    out.write(_footer())

def main():
    '''
    Main function for initialising variables and starting the appliction
    '''
    libpath = os.path.dirname(os.getcwd())
    overview = libpath + '/overview.html'

    generate(overview, cuesheetlist(libpath), libpath)

if __name__ == '__main__':
    main()
