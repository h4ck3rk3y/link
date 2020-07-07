# link
fetch's link to the rest of the world

![Link](https://imgur.com/2RUClFK.png)

## Getting Started

### clone the repository

```bash
git clone https://github.com/h4ck3rk3y/link
```

### install the requirements

```bash
pip install -r requirements.txt

```

### run tests

```
python -m unittest discover
```

## Relevant API docs

1. [Stack Overflow](https://api.stackexchange.com/docs)
2. [Slack](https://api.slack.com/methods/search.messages)
3. [Trello](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#search)
4. [Github](https://docs.github.com/en/rest/reference/search)

## Contract

This is a libary that allows you to, query all enabled integrations. You can filter to specific sources, dates if you want to.
Link ranks and sorts the results for you, it paginates for free as well. Well it will do all this when we start writing some code.

## Versioning

If you are developing Link, make sure that you handle versioning correctly. Link follows semver but in addition to the semantic versioning we also have tags like "1.x" and "2.x", we do this till we have our own self hosted
artifactory

1. Change the version in setup.py
2. Get the PR merged
3. Tag github with the new tag that you used in setup.py
4. Use the major version from that tag and push another tag whihc looks like "MAJOR_VERSION.x"