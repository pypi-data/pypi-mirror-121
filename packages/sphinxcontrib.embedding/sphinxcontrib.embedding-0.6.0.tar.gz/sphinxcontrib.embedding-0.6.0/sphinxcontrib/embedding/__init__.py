"""
Embedding
"""

__copyright__ = 'Copyright (C) 2021 @koKkekoh'
__version__ = '0.6.0'
__license__ = 'BSD 2-Clause License'
__author__  = '@koKekkoh'
__url__     = 'https://qiita.com/tags/sphinxcontrib.embedding'

from pprint import pprint

from docutils import nodes, utils
from docutils.parsers.rst.states import Inliner
from sphinx.util.docutils import ReferenceRole
from sphinx.util.nodes import split_explicit_title, set_role_source_info

#------------------------------------------------------------

#common
_ifs, _ife = r'<iframe', r'></iframe>'
_scs, _sce = r'<script', r'></script>',

#youtube
_yt_src = r'src="https://www.youtube.com/embed/{0}"'
_yt_sz  = r'width="560" height="315"'
_yt_ttl = r'title="Youtube video player"'
_yt_oth = r'frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen'
_yt_all = f'{_ifs} {_yt_src} {_yt_sz} {_yt_ttl} {_yt_oth}{_ife}'

#vimeo
_vm_src = r'src="https://player.vimeo.com/video/{0}"'
_vm_sz  = r'width="640" height="360"'
_vm_oth = r'frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen'
_vm_all = f'{_ifs} {_vm_src} {_vm_sz} {_vm_oth}{_ife}'

#nikovide
_nv_src = r'src="https://embed.nicovideo.jp/watch/{0}/script?w=640&h=360"'
_nv_oth = r'type="application/javascript"'
_nv_all = f'{_scs} {_nv_oth} {_nv_src}{_sce}',

#twitter
_tw_cls = r'class="twitter-timeline"'
_tw_src = r'href="https://twitter.com/{0}?ref_src=twsrc%5Etfw"'
_tw_spt = r'async src="https://platform.twitter.com/widgets.js" charset="utf-8"'
_tw_all = f'<a {_tw_cls} {_tw_src}>Tweets by {0}</a> {_scs} {_tw_spt}{_sce}'

_embedding = {
    'yt': _yt_all, 'youtube': _yt_all, 
    'vm': _vm_all, 'vimeo': _vm_all,
    'nv': _nv_all, 'nicovideo': _nv_all,
}

def visit_Embedding(self, node):
    #設定からの取り込み.
    _embedding.update(self.config.html_embedding)

    #ノードから「:emb:`classifier<value>`」の取り込み.
    classifier = node['classifier']
    value = node['value']

    #埋め込み用の文字列を手に入れる
    try:
        formatstr = _embedding[classifier]
    except KeyError as err:
        message  = r'<strong><font color="red">Invalid Classifier[[</font>'
        message += f'{classifier}'
        message += r'<font color="red">]]</font></strong>'
        self.body.append(message)

        return

    try:
        html = formatstr.format(value)
    except TypeError as err:
        debug = utils.unescape(formatstr)
        message  = r'<strong><font color="red">Format Error[[</font>'
        message += f'{debug}'
        message += r'<font color="red">]]</font></strong>'
        self.body.append(message)

        return

    #完成したHTMLを渡す.
    self.body.append(html)

def depart_Embedding(self, node):
    pass

#------------------------------------------------------------

class Embedding(nodes.General, nodes.Element, nodes.Inline):
    pass

class EmbeddingRole(ReferenceRole):

    def run(self):
        if not self.has_explicit:
            node = nodes.Text(self.title)
        else:
            node = Embedding(self.rawtext, classifier=self.title, value=self.target)

        return [node], []

def embedding_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    has_explicit, title, target = split_explicit_title(text)

    if not has_explicit:
        # the role does not have ruby-text is converted to Text node
        node = nodes.Text(text)
    else:
        node = Embedding(rawtext, classifier=title, value=target)

    #doctest/unittestから呼び出された時はNoneになっている.
    if inliner:
        set_role_source_info(inliner, lineno, node)

    return [node], []

#------------------------------------------------------------

def setup(app):
    app.add_role('emb', embedding_role)
    app.add_role('embedding', embedding_role)
    app.add_node(Embedding, html=(visit_Embedding, depart_Embedding))

    app.add_config_value('html_embedding', {}, 'html')

    return {
            'version': __version__,
            'parallel_read_safe': True,
            'parallel_write_safe': True,
        }

#------------------------------------------------------------

class Doctest(object):
    class Config():
        def __init__(self, config={}):
            self.html_embedding = config

    def __init__(self, rawtext):
        self.config = self.Config()

        [node], message = embedding_role('emb', rawtext, rawtext, None, None)

        self.body = []
        self.node = node
        self._visit = visit_Embedding
        self._depart = depart_Embedding
    def exec_visit_method(self):
        return self._visit(self, self.node)
    def exec_depart_method(self):
        return self._depart(self, self.node)
    def do_doctest(self):
        """
        >>> suite = Doctest('yt<aaaaa>')
        >>> suite.node['classifier']
        'yt'
        >>> suite.node['value']
        'aaaaa'
        """
        pass

#------------------------------------------------------------

if __name__ == '__main__':
    import doctest
    doctest.testmod()
