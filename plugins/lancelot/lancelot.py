# -*- coding: utf-8 -*-
# This file is public domain according to its author, the Cloisted Monkey

"""Shortcode for non-restructured text inter-site links.
Re-write of the ``doc`` plugin to allow alternative titles outside of RST
The documentation seems to indicate that this should work but it uses angle
brackets <> and something is converting them to less than and greater
than HTML symbols.
"""

from nikola.plugin_categories import ShortcodePlugin
from nikola.utils import LOGGER, slugify


class Plugin(ShortcodePlugin):
    """Plugin for non-rst inter-site links."""

    name = "lancelot"

    def handler(self, title=None, site=None, data=None, lang=None,
                date=None, post=None):
        """Create an inter-site link

        Note:
         if you don't use the keyword "title" in the shortcode, nikola will
        pass the string as the first argument to this method (using the *args
        trick). So for my future self: put the title first or never
        forget the keyword.

        Args:
         title: optional argument to specify a different title from the post

        Returns:
         output HTML to replace the shortcode
        """
        success, twin_slugs, title, permalink, slug = lancelot_link(
            site=site,
            slug=data,
            title=title)
        if success:
            if twin_slugs:
                LOGGER.warning(
                    ('More than one post with the same slug. '
                     f'Using "{permalink}" '
                     'for lancelot shortcode'))
            output = f'<a href="{permalink}">{title}</a>'
        else:
            LOGGER.error(
                f'"{slug}" slug doesn\'t exist.')
            output = ('<span class="error text-error" style="color: red;">'
                      f'Invalid link: {data}</span>')
        return output, []


def lancelot_link(site, slug, title):
    """process the slug, check if it exists or is duplicated

    if `title` is None this will grab the post-title

    Args:
     site: the Nikola object
     slug: the text between the shortcode tags
     title: the title passed in by the user (if any)

    Returns:
     tuple (success, has duplicate slugs, title, permalink, slug)
    """
    if '#' in slug:
        slug, fragment = slug.split('#', 1)
    else:
        fragment = None
    slug = slugify(slug)

    twin_slugs = False
    post = None
    for p in site.timeline:
        if p.meta('slug') == slug:
            if post is None:
                post = p
            else:
                twin_slugs = True
                break
    try:
        if post is None:
            raise ValueError("No post with matching slug found.")
    except ValueError:
        return False, False, title, None, slug

    if title is None:
        title = post.title()

    permalink = post.permalink()
    if fragment:
        permalink += '#' + fragment

    return True, twin_slugs, title, permalink, slug
