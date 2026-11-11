# Federation of Bosnia and Herzegovina: law history in git

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is the law of Federation of Bosnia and Herzegovina, Bosnia and Herzegovina, which global-law reads at `bosnia-and-herzegovina/federation/acts/`.

The law of the Federation of Bosnia and Herzegovina (Federacija Bosne i Hercegovine), one of the two entities of Bosnia and Herzegovina, as a git history: one file per article, one commit per law, dated the day it took effect, with the law as the commit's author. `git log` lists every change to an article; checking out a date gives the text in force that day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `ba-bih/`. The state's own law is in [lexifina/bosnia-and-herzegovina-law](https://github.com/lexifina/bosnia-and-herzegovina-law).

The text is in Bosnian (Latin script), as the Government of the Federation publishes it.

## What this repository holds

Laws of the Federation published in the Službene novine Federacije BiH, each in its text as enacted (one version, in force on the day its own final article names):

- `zakon/<year>/sn<issue>-<id>/`: laws from 2001 on whose Government page reads cleanly, listed in [registry/ACTS.md](registry/ACTS.md) and [registry/data/acts.json](registry/data/acts.json) (status, gazette issue, official page). Amending laws are published as acts of their own.
- `<law>/` folders at the top: the first build (October 2026), 38 laws of 2019 to 2026, listed in [data/versions.json](data/versions.json).

A law later amended is published as enacted all the same and labelled `amended, not consolidated` in `registry/data/acts.json`, with the amending laws named (`amended_by`); no consolidated text is made, so its text here is the text as enacted, not the text in force. The Government publishes no consolidated texts.

Not included: the laws listed in [data/held.json](data/held.json), each with the reason (most often: the Government's register has no free page for it, or its only free copy is an old transliteration without diacritics; laws of 1994 to 2000 are mostly of this kind); the Constitution of the Federation (the only free text is a consolidation that stops at Amendment CIX of 2008); laws passed but not yet in force ([data/pending.json](data/pending.json)).

## Freshness

Every version names the official page it was read from (its `Source:` trailer, and `portal` in the act indexes), so every act can be checked against its source.

<!-- freshness-summary -->
Checked against the official sources: 2026-11-11; 99% of acts verified in the last 7 days, 99% in the last 30 ([data/freshness.json](data/freshness.json)).
<!-- /freshness-summary -->

`python tools/freshness.py <act>` gives an act's status, its last check and the official link; `python tools/freshness.py --summary` the overall picture. An act is checked by reading the gazette publisher's index of Službene novine Federacije BiH (every issue, every act's title) through the newest issue and matching every law that amends, repeals, interprets or corrects it, and by reading the Government's register of laws for new texts. The check runs daily; [data/status.json](data/status.json) says whether updates are running and when each official source last answered. Threshold: 7 days (every act here is a law). Statuses (`current`, `pending-change`, `stale`, `unverified`, `source-unavailable`) and columns are explained in [data/freshness.json](data/freshness.json). Acts labelled `amended, not consolidated` are `pending-change`: the gazette lists an amendment that no consolidated text here applies; their amending laws are named in [registry/data/acts.json](registry/data/acts.json) (`amended_by`).

Laws of the Federation in the gazette that are not here are listed, each with its reason and official page, in [data/held.json](data/held.json); laws passed but not yet in force in [data/pending.json](data/pending.json), appended on the day they take effect.

## Sources

- The gazette publisher's index of the Službene novine Federacije BiH (JP NIO Službeni list BiH, <https://www.sluzbenilist.ba/>): every issue, its date and every act's issuer and title. It gives each law's issue date and lists the laws that amend it. The gazette texts themselves need a subscription and are not used.
- The Government of the Federation of Bosnia and Herzegovina (Vlada Federacije Bosne i Hercegovine), <https://fbihvlada.gov.ba/bs/zakoni>: its chronological registers of the laws published in each year's Službene novine Federacije BiH, and its page for each law, which gives the text as published.

## Dates

- Each law's commit is dated at **noon, Europe/Sarajevo, on the day it took effect**: the gazette issue date, plus the days the law's own final article names (most often the eighth day after publication).
- Versions that take effect after the retrieval day would go on the `buducnost` branch, never merged into `main`.

## Files

In `zakon/`: `art-001.md` is Član 1, `art-005-a.md` Član 5a; a chapter heading is its own file after the article it follows (`art-002-zz-heading-1.md`, before Član 1 `0-heading-1.md`). In the first build's folders: `clan-001.md` is Član 1, `ukaz.md` the President's decree promulgating the law, `naslov.md` the title, `potpis.md` the signatures.

## How it is checked

- Every version is read back from git on the day it took effect and on the day before (`registry/tools/build/check_repo.py`, `tools/check_repo.py`).
- Health checks: no merge commits, commit dates never go backwards, nothing dated in the future, and every commit's trailers parse.

## What "author" means

The author of a commit is the law that made it, named by its gazette number, with an e-mail address that cannot exist (`<key>@fbihvlada.gov.ba.invalid`). The committer is always Lexifina.

## Limits

This is not an official publication. The binding text is the one published in the Službene novine Federacije BiH.
