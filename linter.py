#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Dan Flettre
# Copyright (c) 2015 Dan Flettre
#
# License: MIT
#

"""This module exports the StandardX plugin class."""

from SublimeLinter.lint import NodeLinter
import re


class StandardX(NodeLinter):
    """Provides an interface to standard."""

    syntax = ('javascript', 'html', 'javascriptnext', 'javascript 6to5', 'javascript (babel)', 'vue')
    cmd = 'standardx --stdin --verbose'
    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 3.7.2'
    regex = r'^\s.+:(?P<line>\d+):(?P<col>\d+):(?P<message>.+)'
    selectors = {
        'html': 'source.js.embedded.html',
        'vue': 'source.js.embedded.html'
    }

    html_pattern = re.compile(r'(^.*\n)\s+$', re.DOTALL)
    javascript_tag_pattern = re.compile(r'(?i)<script.*?>(.*?)</script>', re.S)

    npm_name = 'standardx'
    defaults = {
        'enable_if_dependency': True,
        'disable_if_not_dependency': False
    }

    def run(self, cmd, code):
        """
        If HTML syntax and the last line is just whitespace then remove it.

        Its probably just space before closing.
        script tag
        """
        if code and self.syntax == 'html':
            match = self.html_pattern.match(code)
            if match:
                code = match.group(1)
        elif code and self.syntax == 'vue':
            vue_match = self.javascript_tag_pattern.match(code)
            if vue_match:
                code = vue_match.group(1)
        return super(StandardX, self).run(cmd, code)
