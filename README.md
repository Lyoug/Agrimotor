# Agrimotor

A script to help study the rhythms of the song Agrimotor by Fredrik Thordendal

Listen to the song [here](https://www.youtube.com/watch?v=c8badRqKgxA)

Some [unusual unicode characters](https://en.wikipedia.org/wiki/Box-drawing_character) are used:

| Character | Used as                                             |
| :--------:|:--------------------------------------------------- |
| ╺         | beam start (rest)                                   |
| ┍         | beam start (note)                                   |
| ━         | beam middle (rest)                                  |
| ┯         | beam middle (note)                                  |
| ╸         | beam end (rest)                                     |
| ┑         | beam end (note) (also used as an 8th note rest)     |
|           |                                                     |
| ╵         | hamp                                                |
| │         | bar line                                            |


This script generates 3 text files (available in this repository):
- The whole song’s rhythm as "sheet music" in 12/8. Something like:
```
  │ ┍┯╸┍┯┑╺┯╸┍┯┑ │ ╺┯┑┍━┑┍┯╸┍━┑ │ ┍┯╸┍┯┑╺┯┑┍━┑ │ ╺┯┑┍━┑┍┯╸┍━┑ │ ...
  │ ╵╵┑╵╵╵┑╵┑╵╵╵ │ ┑╵╵╵┑╵╵╵┑╵┑╵ │ ╵╵┑╵╵╵┑╵╵╵┑╵ │ ┑╵╵╵┑╵╵╵┑╵┑╵ │
```

- The whole song as a list of attacks and attack groups, to help look for patterns:
```
  xx-xxx-x-xxx-xxx-xxx-x-xxx-xxx-xxx-x-xxx-xxx-x-...
  2 3 1 3 3 3 1 3 3 3 1 3 3 1...
```

- The whole song condensed into a list of base patterns (see [this reddit post](https://old.reddit.com/r/Meshuggah/comments/zq7ogv/agrimotor_patterns_cracked/) for more details):
```
aab aaab aaab...
```

To generate them, download Agrimotor.py, open a console and run ```python Agrimotor.py```. Tested with python 3.11, but it probably runs with earlier versions >= 3.6 (for f-strings).
