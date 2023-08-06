# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxcontrib', 'sphinxcontrib.revealjs', 'sphinxcontrib.revealjs.directives']

package_data = \
{'': ['*'],
 'sphinxcontrib.revealjs': ['lib/revealjs/LICENSE',
                            'lib/revealjs/dist/reset.css',
                            'lib/revealjs/dist/reset.css',
                            'lib/revealjs/dist/reset.css',
                            'lib/revealjs/dist/reveal.css',
                            'lib/revealjs/dist/reveal.css',
                            'lib/revealjs/dist/reveal.css',
                            'lib/revealjs/dist/reveal.js',
                            'lib/revealjs/dist/reveal.js',
                            'lib/revealjs/dist/reveal.js',
                            'lib/revealjs/dist/theme/*',
                            'lib/revealjs/dist/theme/fonts/league-gothic/*',
                            'lib/revealjs/dist/theme/fonts/source-sans-pro/*',
                            'lib/revealjs/plugin/highlight/*',
                            'lib/revealjs/plugin/markdown/*',
                            'lib/revealjs/plugin/math/*',
                            'lib/revealjs/plugin/notes/*',
                            'lib/revealjs/plugin/search/*',
                            'lib/revealjs/plugin/zoom/*',
                            'theme/*']}

install_requires = \
['Sphinx>=4.1.1,<5.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'cssutils>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'sphinxcontrib-revealjs',
    'version': '0.2a0',
    'description': 'Build slides with RevealJS.',
    'long_description': "# sphinxcontrib-revealjs\n\nThis is a work in progress.\n\n## Configuration\n\n### `revealjs_vertical_slides`\n\nEnable/disable vertical slides. Defaults to `True`. Doesn't actually work right now.\n\n### `revealjs_permalinks`\n\nEnable permalinks. Defaults to False\n\n### `revealjs_theme`\n\nOverride builder's default theme.\n\n### `revealjs_theme_options`\n\n- `revealjs_theme`: Revealjs theme (see Revealjs docs for list of themes)\n\n## Automatic slide breaks\n\nHeadings 1&ndash;2 automatically create slide breaks\n\n## Directives\n\n- interslide\n- newslide\n- speaker\n- incremental\n\n## Development\n\nDepend on Revealjs (git submodule). See https://git-scm.com/book/en/v2/Git-Tools-Submodules\n\n##### Clone this repo w/ submodules\n\n```\n$ git clone --recurse-submodules <url for this repo>\n```\n\n##### Pull upstream changes\n\n```\n$ git submodule update --remote lib/revealjs\n```",
    'author': 'Ashley Trinh',
    'author_email': 'ashley@hackbrightacademy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
