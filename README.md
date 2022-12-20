# Agrimotor

A script to help study the rhythms of the song [Agrimotor by Fredrik Thordendal](https://www.youtube.com/watch?v=c8badRqKgxA).

Some [unusual unicode characters](https://en.wikipedia.org/wiki/Box-drawing_character) are used:

| Character | Used as                                             |
| :--------:|:--------------------------------------------------- |
| ╺         | beam start (rest)                                   |
| ┍         | beam start (note)                                   |
| ━         | beam middle (rest)                                  |
| ┯         | beam middle (note)                                  |
| ╸         | beam end (rest)                                     |
| ┑         | beam end (note) (also used as an 8th note rest)     |
| ╵         | hamp                                                |
| │         | bar line                                            |


This script generates 3 text files listed below (all three are available in this repository):

## Text music sheet

It contains the whole song’s rhythm as "sheet music" in 12/8. Something like:
```
  │ ┍┯╸┍┯┑╺┯╸┍┯┑ │ ╺┯┑┍━┑┍┯╸┍━┑ │ ┍┯╸┍┯┑╺┯┑┍━┑ │ ╺┯┑┍━┑┍┯╸┍━┑ │ ...
  │ ╵╵┑╵╵╵┑╵┑╵╵╵ │ ┑╵╵╵┑╵╵╵┑╵┑╵ │ ╵╵┑╵╵╵┑╵╵╵┑╵ │ ┑╵╵╵┑╵╵╵┑╵┑╵ │
```
which should look like this:

![Text music sheet screenshot](img/text_music_sheet.png)

and is meant to emulate this:

![Acual music sheet](img/actual_music_sheet.png)


## Attacks

The whole song as a list of attacks and attack groups, to help look for patterns:
```
  xx-xxx-x-xxx-xxx-xxx-x-xxx-xxx-xxx-x-xxx-xxx-x-...
  2 3 1 3 3 3 1 3 3 3 1 3 3 1...
```

## Patterns

The whole song condensed into a list of base patterns (see [this reddit post](https://old.reddit.com/r/Meshuggah/comments/zq7ogv/agrimotor_patterns_cracked/) for more details):
```
aab aaab aaab...
```

## Generating the files

To generate the three text files, download Agrimotor.py, open a console and run ```python Agrimotor.py```. Tested with python 3.11, but it probably runs with earlier versions (≥ 3.6 for f-strings). Some parameters are customisable in the first few lines of the script.

