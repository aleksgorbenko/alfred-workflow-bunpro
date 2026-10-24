<p align="center">
  <img src="icon.png" width="128" alt="BunPro for Alfred icon">
</p>

<h1 align="center">BunPro for Alfred</h1>

<p align="center">Search BunPro grammar points and review your progress from Alfred.</p>

<p align="center">
  <a href="https://github.com/aleksgorbenko/alfred-workflow-bunpro/actions/workflows/ci.yml"><img src="https://github.com/aleksgorbenko/alfred-workflow-bunpro/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI status"></a>
  <a href="https://github.com/aleksgorbenko/alfred-workflow-bunpro/releases/latest"><img src="https://img.shields.io/github/v/release/aleksgorbenko/alfred-workflow-bunpro?label=release&color=4c8dff" alt="Latest release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-blue" alt="Licence MIT"></a>
  <img src="https://img.shields.io/badge/macOS-14%2B-black?logo=apple" alt="macOS 14 or later">
  <a href="https://www.alfredapp.com/powerpack/"><img src="https://img.shields.io/badge/Alfred-5%20Powerpack-5c1f87" alt="Alfred 5 Powerpack"></a>
</p>

<p align="center">
  <a href="#usage">Usage</a> ·
  <a href="#install">Install</a> ·
  <a href="#development">Development</a>
</p>

Search BunPro grammar points and review your personal progress from Alfred.

## Usage

| Keyword | Function |
| --- | --- |
| `bps` | Search BunPro grammar points by kana, romaji, or English. |
| `bp` | Browse your dashboard summary, statistics, levels, forecast, and leeches. |

- `bp <page>` opens a page: `summary`, `stats`, `levels`, `forecast`, `leeches`.
- Text after the page filters its rows, e.g. `bp forecast tomorrow`.
- Delete the page name to go back to the menu.
- Pages load in the background: `Loading <page>…` shows until the data arrives, then cached pages open instantly.
- First row on every page is the page itself: `Enter` opens the dashboard, `Tab` goes back.

![BunPro dashboard menu](images/about/main.png)

![BunPro grammar search](images/about/search.png)

Open the Summary view to see your current BunPro progress.

![BunPro dashboard summary](images/about/summary.png)

### Maintenance

- `:bp` - cache size (Enter reveals the folder) and Empty Cache.

## Install

1. Download the latest `BunPro.alfredworkflow` from [Releases](https://github.com/aleksgorbenko/alfred-workflow-bunpro/releases).
2. Double-click it and let Alfred import it.
3. Requires [Alfred](https://www.alfredapp.com) with a Powerpack licence.

## Development

- Python 3.14, standard library only.
- `data/grammar.json` contains the searchable grammar reference.
- Runtime code is in `src/bunpro/`.

```sh
make setup   # install dev tools and the Python environment
make ci      # everything CI runs
make check   # lint, format check, and tests
make build   # package dist/BunPro.alfredworkflow
make release VERSION=v1.0.0
make sync-plist WORKFLOW_DIR=/path/to/installed/workflow
```

## My Other Workflows

- [Nihongo for Alfred](https://github.com/aleksgorbenko/alfred-workflow-nihongo)
- [WaniKani for Alfred](https://github.com/aleksgorbenko/alfred-workflow-wanikani)
- [Netlify for Alfred](https://github.com/aleksgorbenko/alfred-workflow-netlify)
- [2Do for Alfred](https://github.com/aleksgorbenko/alfred-workflow-2do)
- [Discogs for Alfred](https://github.com/aleksgorbenko/alfred-workflow-discogs)
- [Bandcamp for Alfred](https://github.com/aleksgorbenko/alfred-workflow-bandcamp)
- [config](https://github.com/aleksgorbenko/config)
