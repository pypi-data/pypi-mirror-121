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

example:

.. code-block:: python

   html_embedding = {
       'foo': r'<script type="TYPE_INFO" src="THE_URL/{0}/param?arg1=val1&arg2=val2"></script>'
   }
