const search = instantsearch({
    appId: 'XFIFHM1HXM',
    apiKey: 'db0c2fa34c2f04bc1cca51e7afc2d55a',
    indexName: 'cheaters',
    routing: true
});


search.addWidget(
    instantsearch.widgets.searchBox({
        container: '#search-box',
        placeholder: 'Искать мошенника...'
    })
);


search.addWidget(
    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            empty: 'No results',
            item: '<li><em>Hit {{objectID}}</em>: {{{key}}} {{{value}}}</li>'
        }
    })
);
search.addWidget(
    instantsearch.widgets.pagination({
        container: '#pagination-container',
        maxPages: 10,
        padding: 10,
        scrollTo: false,
        showFirstLast: false,
    })
);


search.start();
