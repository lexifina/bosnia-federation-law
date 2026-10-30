# Federation of Bosnia and Herzegovina: law history in git

The law of the Federation of Bosnia and Herzegovina (Federacija Bosne i Hercegovine), one of the two entities of Bosnia and Herzegovina, as a git history: one file per article, one commit per law, dated the day it took effect, with the law as the commit's author. `git log` lists every change to an article; checking out a date gives the text in force that day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `ba-bih/`. The state's own law is in [lexifina/bosnia-and-herzegovina-law](https://github.com/lexifina/bosnia-and-herzegovina-law).

The text is in Bosnian (Latin script), as the Government of the Federation publishes it.

## What this repository holds

Laws published in the Službene novine Federacije BiH from 2019 to 2026 that no later law has amended, repealed, interpreted or re-enacted, each in its text as enacted, which is therefore also its current text. One folder per law.

Not included yet: the Constitution of the Federation (the only free text found is a consolidation that stops at Amendment CIX of 2008, while later amendments are attached only as scanned images); laws that were later amended; laws before 2019; annual budget laws; and the laws whose page could not be read cleanly.

## Source

The Government of the Federation of Bosnia and Herzegovina (Vlada Federacije Bosne i Hercegovine), <https://fbihvlada.gov.ba/bs/zakoni>: its chronological registers of the laws published in each year's Službene novine Federacije BiH (gazette number and date for each law), and its page for each law, which gives the promulgating decree and the text as published.

## Dates

- Each law's commit is dated at **noon, Europe/Sarajevo, on the day it took effect**: the gazette date in the Government's register, plus the days the law's own final article names (most often the eighth day after publication).
- Versions that take effect after the retrieval day would go on the `buducnost` branch, never merged into `main`.

## Files

`<law>/clan-001.md` is Član 1, `clan-005-a.md` Član 5a. `ukaz.md` holds the President's decree promulgating the law, `naslov.md` the title, `potpis.md` the signatures. Chapter headings stay in the file of the article they stand before. One paragraph per line.

## How it is checked

- Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`.
- The letters and digits of every law equal those of the Government's page, read independently with a different HTML reader, from the first paragraph to the last.
- Whether a law was later amended or repealed is judged from the registers by title. A law is left out on any doubt, but a law repealed by a law of a different name could still appear.
- Health checks: no merge commits, commit dates never go backwards, nothing dated in the future, and every commit's trailers parse.

## What "author" means

The author of a commit is the law that made it, named by its gazette number, with an e-mail address that cannot exist (`<key>@fbihvlada.gov.ba.invalid`). The committer is always Lexifina.

## Limits

This is not an official publication. The binding text is the one published in the Službene novine Federacije BiH. Only the laws listed in `data/versions.json` are included.
