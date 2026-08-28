# alfred-workflow-bunpro

Alfred Workflow to search [BunPro](https://bunpro.jp) grammar points.

## Commands

### `bps <query>` - grammar point search

Live search over BunPro grammar points. Type kana, romaji, or English. Selecting a row opens that grammar point's page on [https://bunpro.jp](https://bunpro.jp).

## Install

1. Download the latest `BunPro.alfredworkflow` from [Releases](https://github.com/aleksgorbenko/alfred-workflow-bunpro/releases).
2. Double-click it - Alfred will prompt to import.
3. Requires [Alfred](https://www.alfredapp.com) with a Powerpack license.

## Development

`data/grammar.json` is a static export, generated from BunPro's public grammar list at [bunpro.jp/grammar_points](https://bunpro.jp/grammar_points).

```sh
make check   # lint + format check + tests
make test
make lint
make format
make build   # package dist/BunPro.alfredworkflow
make release VERSION=v1.0.0
make sync-plist WORKFLOW_DIR=/path/to/installed/workflow
```

## My Other Workflows

- [WaniKani for Alfred](https://github.com/aleksgorbenko/alfred-workflow-wanikani)
- [2Do for Alfred](https://github.com/aleksgorbenko/alfred-workflow-2do)
