# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bareasgi_session', 'bareasgi_session.storage']

package_data = \
{'': ['*']}

install_requires = \
['bareasgi>=4.0.0-alpha.5,<5.0.0']

setup_kwargs = {
    'name': 'bareasgi-session',
    'version': '4.0.0a3',
    'description': 'Session support for bareASGI',
    'long_description': "# bareASGI-session\n\nSession support for bareASGI (read the [docs](https://rob-blackbourn.github.io/bareASGI-session/)).\n\n## Overview\n\nWhen a client (e.g. a browser tab) makes HTTP requests to a server, the server\ndoes not know if the requests came from the same client. This makes it difficult\nto maintain state information (e.g. the users identity).\n\nA solution which is transparent to the client involves the server sending a\ncookie to the client. Once the cookie is sent the client will automatically add\nthe cookie to any subsequent request it makes to the server (assuming cookies\nare enabled). By checking the cookie the server can know which client has sent\nthe request.\n\n## Usage\n\nYou can add session middleware with the `add_session_middleware` helper function.\n\n```python\nfrom bareasgi import Application\nfrom bareasgi_session import (\n  add_session_middleware,\n  MemorySessionStorage\n)\n\napp = Application()\n\nadd_session_middleware(app, MemorySessionStorage())\n```\n\nThe session can be retrieved with the `session_data` helper function. This returns\nan (initially empty) dictionary.\n\n```python\nfrom datetime import datetime\nfrom bareutils import text_writer\nfrom bareasgi_session import session_data\n\nasync def session_handler(request: HttpRequest) -> HttpResponse:\n    session = session_data(request)\n    now = session.get('now')\n    message = f'The time was {now}' if now else 'First time'\n    session['now'] = datetime.now()\n    headers: List[Header] = [\n        (b'content-type', b'text/plain'),\n        (b'content-length', str(len(message)).encode('ascii'))\n    ]\n    return HttpResponse(200, headers, text_writer(message))\n```\n",
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/bareASGI-session',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
