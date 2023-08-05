.. image:: assets/GlowCordBanner.svg
   :alt: glowcord

.. image:: https://discord.com/api/guilds/794739329956053063/embed.png
   :target: https://discord.gg/ZASMEtS4kg
   :alt: Discord server invite
.. image:: https://img.shields.io/pypi/v/glowcord.svg
   :target: https://pypi.python.org/pypi/glowcord
   :alt: PyPI version info
.. image:: 	https://img.shields.io/pypi/dm/glowcord?color=informational&label=Pypi%20downloads
   :target: https://pypi.python.org/pypi/glowcord
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/glowcord.svg
   :target: https://pypi.python.org/pypi/glowcord
   :alt: PyPI supported Python versions
.. image:: https://img.shields.io/readthedocs/glowcord/1.0?label=GlowCordDocs
   :target: https://glowcord.readthedocs.io/en/latest/
   :alt: Glowcord documentation
   
GlowCord
--------
   
A Modern Discord API Wrapper For Python 

Fork notice
--------------------------

This is a fork of discord.py, which unfortunately has been `officially discontinued <https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1/>`_ on 28th August 2021.
If You Want This To Be A Replacement Well Lucky For You We're Gonna Be Updating It Alot And If You Want You Can Add A Feature Via Pull Request 

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``
- Proper rate limit handling
- Optimised in both speed and memory

Installing
----------

**Python 3.8 or higher is required**

To install the library without full voice support, you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U GlowCord

    # Windows
    py -3 -m pip install -U GlowCord

Otherwise to get voice support you should run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U "GlowCord[voice]"

    # Windows
    py -3 -m pip install -U GlowCord[voice]

To install additional packages for speedup, run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U "GlowCord[speed]"

    # Windows
    py -3 -m pip install -U GlowCord[speed]


To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/cordcord/glowcord/
    $ cd glowcord
    $ python3 -m pip install -U .[voice]


Optional Packages
~~~~~~~~~~~~~~~~~~

* `PyNaCl <https://pypi.org/project/PyNaCl/>`__ (for voice support)
* `aiodns <https://pypi.org/project/aiodns/>`__, `Brotli <https://pypi.org/project/Brotli/>`__, `cchardet <https://pypi.org/project/cchardet/>`__ (for aiohttp speedup)
* `orjson <https://pypi.org/project/orjson/>`__ (for json speedup)

Please note that on Linux installing voice you must install the following packages via your favourite package manager (e.g. ``apt``, ``dnf``, etc) before running the above commands:

* libffi-dev (or ``libffi-devel`` on some systems)
* python-dev (e.g. ``python3.6-dev`` for Python 3.6)


Quick Example
~~~~~~~~~~~~~

.. code:: py

    from glowcord.ext import commands


    bot = commands.Bot(command_prefix='$')

    @bot.command()
    async def ping(ctx):
        await ctx.reply('Pong!')

    bot.run('token')


You can find more examples in the examples directory.

**NOTE:** It is not advised to leave your token directly in your code, as it allows anyone with it to access your bot. If you intend to make your code public you should `store it securely <https://github.com/GlowCord/GlowCord/blob/master/examples/secure_token_storage.py/>`_.

Links
------

- `Documentation <https://glowcord.readthedocs.io/en/latest/>`_
- `Official Discord Server <https://discord.gg/VkXmkMd7au>`_
- `Discord API <https://discord.gg/discord-api>`_
