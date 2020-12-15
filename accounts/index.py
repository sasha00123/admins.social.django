import algoliasearch_django as algoliasearch
from algoliasearch_django.decorators import register

from accounts.models import Group


@register(Group)
class GroupIndex(algoliasearch.AlgoliaIndex):
    """
        Class registers Group model in Algolia Search engine.
    """
    fields = ('gid', 'name', 'screen_name', 'photo', 'members')
    settings = {'searchableAttributes': ['gid', 'name', 'screen_name']}
    index_name = 'groups'
