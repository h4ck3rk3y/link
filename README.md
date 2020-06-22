# link
fetch's link to the rest of the world

![Link](https://imgur.com/2RUClFK.png)

## Relevant docs

1. [Stack Overflow](https://api.stackexchange.com/docs)
2. [Slack](https://api.slack.com/methods/search.messages)
3. [Trello](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#search)
4. [Github](https://developer.github.com/v3/search/)

## Contract

This is a service that accepts the users identity and enabled integrations as an input along with the search term. It returns
you the results of the search query, ranked along with some statistics about the number of matches per source. It also
takes care of pagination for you.

This will also allow you to filter queries to sources and to relevant dates.