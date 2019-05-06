"""Missing: DOCSTRING"""

from rest_framework.renderers import BrowsableAPIRenderer

class NoHTMLFormBrowsableAPIRenderer(BrowsableAPIRenderer):
    """Missing: DOCSTRING"""
    def get_rendered_html_form(self, *args, **kwargs):
        """Missing: DOCSTRING"""
        return ""
