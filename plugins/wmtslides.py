# -*- coding: utf-8 -*-

# Copyright © 2012-2015 Roberto Alsina and others.

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import unicode_literals

import sys
import uuid

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from nikola.plugin_categories import RestExtension


class Plugin(RestExtension):

    name = "rest_slides"

    def set_site(self, site):
        self.site = site
        directives.register_directive('slides', Slides)
        Slides.site = site
        return super(Plugin, self).set_site(site)

class SlideItem(object):
    def __init__(self):
        self.image = ''
        self.link = ''
        self.text = ''
    def __repr__(self):
        return repr(self.__dict__)

def split_content(lines):
    item = SlideItem()
    for line in lines:
        line = line.strip()
        if not line: continue
        if line == "---":
            sys.stderr.write("%r\n" % item)
            yield item
            item = SlideItem()
            continue
        if not item.image:
            item.image = line
        elif not item.link:
            item.link = line
        else:
            item.text += '\n' + line


class Slides(Directive):
    """ Restructured text extension for inserting slideshows."""
    has_content = True

    def run(self):
        if len(self.content) == 0:
            return

        items = []

        for item in split_content(self.content):
            items.append(item)

        if self.site.invariant:  # for testing purposes
            carousel_id = 'slides_' + 'fixedvaluethatisnotauuid'
        else:
            carousel_id = 'slides_' + uuid.uuid4().hex

        output = self.site.template_system.render_template(
            'wmtslides.tmpl',
            None,
            {
                'slides_content': items,
                'carousel_id': carousel_id,
            }
        )
        return [nodes.raw('', output, format='html')]


directives.register_directive('wmtslides', Slides)
