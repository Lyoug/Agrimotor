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


This script generates 3 text files listed below (all three are available in this repository).

## Text music sheet

The first generated file (Agrimotor_music_sheet.txt) contains the whole song’s rhythm as "sheet music" in 12/8. Something like:
```
  │ ┍┯╸┍┯┑╺┯╸┍┯┑ │ ╺┯┑┍━┑┍┯╸┍━┑ │ ┍┯╸┍┯┑╺┯┑┍━┑ │ ╺┯┑┍━┑┍┯╸┍━┑ │ ...
  │ ╵╵┑╵╵╵┑╵┑╵╵╵ │ ┑╵╵╵┑╵╵╵┑╵┑╵ │ ╵╵┑╵╵╵┑╵╵╵┑╵ │ ┑╵╵╵┑╵╵╵┑╵┑╵ │
```
which should look like this:

![Text music sheet screenshot](img/text_music_sheet.png)

and is meant to emulate this:

![Acual music sheet](img/actual_music_sheet.png)


## Attacks

The second generated file (Agrimotor_attacks.txt) contains the whole song as a list of attacks and attack groups, to help look for patterns:
```
xx-xxx-x-xxx-xxx-xxx-x-xxx-xxx-xxx-x-xxx-xxx-x-…
2 3 1 3 3 3 1 3 3 3 1 3 3 1…
```

## Patterns

The third generated file (Agrimotor_patterns.txt) is the most interesting. It contains the whole song condensed into a list of base patterns:
```
aab aaab aaab aab…
2 3 3 2…
```
Keep reading for explanations, or see [this reddit post](https://old.reddit.com/r/Meshuggah/comments/zq7ogv/agrimotor_patterns_cracked/) for even more detail.

The song is made out of two base patterns:  
**a** = `xx-x`  
**b** = `-x`  
where an `x` is an attack / a hit and a `-` is a rest. Both are 8th notes.

The song starts like this (bar lines added for readability):  
`|xx-xxx-x-xxx|-xxx-xxx-x-x|xx-xxx-xxx-x|-xxx-xxx-x-x|…`

If we rewrite this in terms of the two base patterns we get `aab aaab aaab aab…`:  
`|xx-xxx-x-xxx|-xxx-xxx-x-x|xx-xxx-xxx-x|-xxx-xxx-x-x|…`  
`|a...a...b.a.|..a...a...b.|a...a...a...|b.a...a...b.|…`

The song keeps going with a mix of `a`s and `b`s. It seems natural to define longer patterns:  
**1** = `ab` = `xx-x-x`  
**2** = `aab` = `xx-xxx-x-x`  
**3** = `aaab` = `xx-xxx-xxx-x-x`  
**4** = `aaaab` = `xx-xxx-xxx-xxx-x-x`  
...

And with these longer patterns, the start of the song reduces to only **23 32**:  
`|xx-xxx-x-xxx|-xxx-xxx-x-x|xx-xxx-xxx-x|-xxx-xxx-x-x|…`  
`|a...a...b.a.|..a...a...b.|a...a...a...|b.a...a...b.|…`  
`|2.........3.|............|3...........|..2.........|…`

Last, let’s just define a few variant patterns that will make the outro simpler:  
**a'** = `-x-x` = `a` but starting with a rest = `bb`  
**2'** = `aa'b` = `abbb`  
**3'** = `aaa'b` = `aabbb`

---

Then we can rewrite the whole song in terms of the longer patterns. Broken down into chunks of 8 or 16 bars (with timecodes for reference), we get this rather neat, compressed version of the song that shows the patterns it is made out of:

*Intro*  
[0:06] **23 32 32 23**  
[0:20] **13 13 13 13 12**  
*Verse 1*  
[0:33] **124 124 124 124 124 12axx** (\*1)  
*Descending riff \\m/*  
[1:00] **23 32 32 23**  
[1:13] **32 23 36 1xx**  
*Verse 2*  
[1:27] **1 12424 124 12424 12aaa** (\*1)  
*Descending riff*  
[1:54] **23 32 32 23**  
[2:07] **32 23 36 1xx**  
*Outro*  
[2:21] **23' 32' 32' 23'** (\*2)  
[2:34] **23' 32' 32' 23'**  

(\*1) 12axx and 12aaa are just truncated versions of 124.

(\*2) The outro is actually just the same as the intro (23 32 32 23), but with rests on beat 3 of every bar:  
`|2.........3.|...... . .....|3...........|..2... . .....|…`  
`|a...a...b.a.|..a... a ...b.|a...a...a...|b.a... a ...b.|…`  
`|xx-xxx-x-xxx|-xxx-x X x-x-x|xx-xxx-xxx-x|-xxx-x X x-x-x|…` <- Intro  
`|xx-xxx-x-xxx|-xxx-x - x-x-x|xx-xxx-xxx-x|-xxx-x - x-x-x|…` <- Outro  
`|a...a...b.a.|..a... b .b.b.|a...a...a...|b.a... b .b.b.|…`  
`|2.........3'|...... . .....|3...........|..2'.. . .....|…`

Without using variant patterns, the outro would be:  
[2:21] **22bb 31bb 31bb 22bb**  
[2:34] **22bb 31bb 31bb 22bb**  
Every **2bb** comes from a **3** that was split by a rest (and every **1bb** comes from a split **2**).


## Generating the files

To generate the three text files, download Agrimotor.py, open a console and run ```python Agrimotor.py```. Tested with python 3.11, but it probably runs with earlier versions (≥ 3.6 for f-strings). Some parameters are customisable in the first few lines of the script, particularly:

- the number of bars per line in the music sheet file
- the sizes of chunks of bars to cut the song into, for the attacks and patterns files
