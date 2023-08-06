Embedding

.. warning::

   this is an alpha version.

example
-------

youtube:

.. code-block:: rst

   :emb:`youtube<identifier>`
   
   :emb:`yt<identifier>`

vimeo:
   
.. code-block:: rst

   :emb:`vimeo<identifier>`

   :emb:`vm<identifier>`

nicovideo:
   
.. code-block:: rst

   :emb:`nicovideo<identifier>`

   :emb:`nv<identifier>`

conf.py
-------
you can register new embedding.
you have to change the indentifier to '{0}'.

.. code-block:: python

   html_embedding = {
           'youtube': r'<script type="application/javascript" src="https://embed.nicovideo.jp/watch/{0}/script?w=640&h=360"></script>'
           }
