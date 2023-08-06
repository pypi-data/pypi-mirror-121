# Autolink References (MkDocs Plugin)

This [mkdocs plugin](http://www.mkdocs.org/user-guide/plugins/) scans articles for references to [Phabricator Tasks](https://www.phacility.com/phabricator/maniphest/) and replaces the task number (`{T0000}`) with a link to the actual task.

## Getting started

To install the plugin using `pip`:

```
pip install phabricator-task-links-mkdocs-plugin
```

Edit your `mkdocs.yml` file and configure the plugin.

```yaml
plugins:
  - phabricator_task_links:
      phabricator_url: https://URL_TO_PHABRICATOR
```

## Example

Create a `docs/index.md` file and references a phabricator task like this:

````markdown

Changelog:

- {T1000} Implement functionality from task

````

## License

MIT
