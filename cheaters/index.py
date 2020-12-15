import algoliasearch_django as algoliasearch
from algoliasearch_django.decorators import register

from cheaters.models import Entry


@register(Entry)
class EntryIndex(algoliasearch.AlgoliaIndex):
    """
        Class to index Cheaters for Algolia Search engine.
    """
    fields = ('key', 'value')
    settings = {'searchableAttributes': ['value']}
    index_name = 'cheaters'
