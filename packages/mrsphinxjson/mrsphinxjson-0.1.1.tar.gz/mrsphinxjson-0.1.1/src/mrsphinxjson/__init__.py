# -*- coding: utf-8 -*-

"""Sphinx extension to include JSON-files in the documentation.

:copyright: Copyright 2021 by Michael Rippstein <info@anatas.ch>
:license: AGPL-3.0, see LICENSE for details.

.. moduleauthor:: Michael Rippstein <michael@anatas.ch>
"""

from importlib.metadata import version, PackageNotFoundError
from typing import Any, Dict, List
from pathlib import Path
import json

from docutils import nodes
from docutils.nodes import Node
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.directives.code import container_wrapper

try:
    __version__ = version('mrsphinxjson')
except PackageNotFoundError:
    # package is not installed
    pass


class JsonDirective(SphinxDirective):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    #     option_spec = {'alt': directives.unchanged,
    #                    'height': directives.nonnegative_int,
    #                    'width': directives.nonnegative_int,
    #                    'scale': directives.nonnegative_int,
    #                    'align': align,
    #                    }
    has_content = False

    def run(self) -> List[Node]:
        basepath = Path(self.config.mrsphinxjson_basepath)
        json_filename = self.arguments[0]
        json_filepath = basepath.joinpath(json_filename)
        json_filepath = json_filepath.resolve()
        with json_filepath.open() as json_file:
            generic_json = json.load(json_file)
        json_node = nodes.literal_block(text=json.dumps(generic_json, indent=4))
        json_node['language'] = 'json'
        json_node = container_wrapper(self, json_node, str(json_filepath))
        return [json_node]


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_directive('json', JsonDirective)

    app.add_config_value('mrsphinxjson_basepath', app.srcdir, 'env')

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
