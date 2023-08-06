import re
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options


def replace_task_link(markdown, phabricator_url):

    pattern = re.compile("(?P<task>\{(T[0-9]{4,6})\})")

    def ref_replace(matchobj):
        task = matchobj.group("task").strip("{").strip("}")

        return f"[{task}]({phabricator_url}/{task})"

    markdown = re.sub(pattern, ref_replace, markdown)

    return markdown


class PhabricatorTaskLinks(BasePlugin):

    config_scheme = (("phabricator_url", config_options.Type(str, required=True)),)

    def on_page_markdown(self, markdown, **kwargs):
        """
        Takes an article written in markdown and looks for the
        presence of a ticket reference and replaces it with autual link
        to the ticket.

        :param markdown: Original article in markdown format
        :param kwargs: Other parameters (won't be used here)
        :return: Modified markdown
        """
        markdown = replace_task_link(markdown, self.config["phabricator_url"])

        return markdown
