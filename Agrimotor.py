
#========================== Parameters and constants ===========================

# Edit these to change the content and layout of the generated files
BAR_LENGTH = 12          # Number of 8th notes per bar
BARS_PER_LINE = 8
CHUNK_SIZES = (8, 16)    # Bars will be analyzed in groups of these sizes
ATTACK = 'x'
REST = '-'
# The comments in this file use 'x' as an attack and '-' as a rest


#============================= Song transcription ==============================


# The key to understanding the song. These two patterns (short and long)
# basically generate the whole song.
SHORT = ATTACK + ATTACK + REST + ATTACK      # 'xx-x'
TAIL  = REST + ATTACK                        # '-x'
LONG  = SHORT + TAIL                         # 'xx-x-x'

# Variant pattern to simplify the outro
LONG_VARIANT = REST + LONG[1:]               # '-x-x-x'

# All possible bar types occuring in the song. A dash means an 8th note rest, a
# number means a group of 8th notes attacks.
#
# Some of these look similar, but this is incidental: it only comes from them
# being "generated" by the base patterns above. The only helpful notable
# difference is the fact that bar type J is built from bar type B but with a
# rest on the third beat.
A = "2-3-1-3"
B = "-3-3-1-1"
C = "2-3-3-1"     # same as A but swap last two groups
D = "2-1-3-3"     # same as A but swap middle two groups
E = "-3-1-3-1"    # same as B but swap middle two groups
F = "-3-3-3"      # same as B but merge last 1s into a 3
G = "-1-3-1-3"
H = "-1-3-3-1"    # same as G but swap last two groups
I = "2-1-3-1-1"   # same as D but split last 3 into two 1s
J = "-3-1-1-1-1"  # same as B but with a rest on the third beat
# (A good portion of the code below assumes that these bar types are well
# formed, i.e. that they represent a bar of 12/8. More formally: the number of
# dashes plus the sum of all numbers in a bar type must equal 12)

AGRIMOTOR_BARS = [
    # 0:06
    A, B, C, B, C, B, A, B,
    D, E, F, G, B, D, E, B,
    # 0:33 (stop drone)
    D, H, A, H, F, E, B, C,
    I, A, F, G, E, C, E, D,
    # 1:00 (descending riff)
    A, B, C, B, C, B, A, B,
    C, B, A, B, C, F, F, G,
    # 1:27
    I, A, F, H, F, E, B, C,
    I, A, F, H, F, E, B, C,
    # 1:54 (repeat descending riff)
    A, B, C, B, C, B, A, B,
    C, B, A, B, C, F, F, G,
    # 2:21 (repeat 0:06 with Bs replaced by Js)
    A, J, C, J, C, J, A, J,
    A, J, C, J, C, J, A, J,
]


#================================== Functions ==================================

# Convert a bar type into a list of attacks and rests
# Example: '2-3-1-3' becomes:
# ['x', 'x', '-', 'x', 'x', 'x', '-', 'x', '-', 'x', 'x', 'x']
def bar_type_to_attacks(bar_type: str) -> list[bool]:
    notes = []
    for char in bar_type:
        if char == '-':
            notes.append(REST)
        else:  # Assume char is a number
            notes.extend([ATTACK] * int(char))
    return notes

# Convert a list of bar types into a single list of attacks and rests
def to_attack_list(bar_list: list[str]) -> list[bool]:
    attack_list = []
    for bar_type in bar_list:
        attack_list.extend(bar_type_to_attacks(bar_type))
    return attack_list

# Turn a list of bar types into a list of annotated attack groups:
# Example: ["2-3-3-1", "2-1-3-3"] becomes:
# [('2', (1, 1),      # a group of 2 attacks in bar 1 starting at 8th note 1
#  ('3', (1, 4)),
#  ('3', (1, 8)),
#  ('3', (1, 12)),    # a group of 3 attacks in bar 1 starting at 8th note 12
#  ('1', (2, 4)),     # a group of 1 attack in bar 2 starting at 8th note 4
#  ('3', (2, 6)),
#  ('3', (2, 10))]
# Attack groups are merged over bar lines.
# All indexes are 1-based, so that it more naturally aligns with what we are
# used to in music.
def _annotated_attacks(
        bar_list: list[str],
        bar_length: int
    ) -> list[tuple[int, tuple[int, int]]]:
    attack_list = to_attack_list(bar_list)
    # Add one last rest to the list so that the loop below takes the last attack
    # group into account
    attack_list.append(REST)

    attack_group_length = 0
    attack_annotations = []
    # Merge attacks into groups
    for global_index, note in enumerate(attack_list):
        if note == ATTACK:
            attack_group_length += 1
        else:   # A rest, i.e. the end of an attack group
            # Figure out where we are in the music then add the annotation
            attack_start = global_index - attack_group_length
            bar_index = attack_start // bar_length + 1
            eighth_note_index = attack_start % bar_length + 1
            attack_annotations.append(
                (str(attack_group_length), (bar_index, eighth_note_index))
            )
            # Get ready for the next group
            attack_group_length = 0
    return attack_annotations

# Turn a list of bar types into a single list of attacks groups, merging attack
# groups over bar lines.
# Example: ["2-3-3-1", "2-1-3-3"] becomes:
# ['2', '3', '3', '3', '1', '3', '3']
def aggregate(bar_list: list[str], bar_length: int) -> list[int]:
    return [annotation[0] for annotation in _annotated_attacks(bar_list, bar_length)]

# Return the bar and 8th note where the given attack starts in the provided list
# of bars.
# (note: unused for now)
def position(attack_index, bar_list: list[str], bar_length: int) -> tuple[int, int]:
    return _annotated_attacks(bar_list, bar_length)[attack_index][1]

# Return a pair of strings that represent the specified bars.
# See to_attacks and to_patterns below for details.
# This is the "main" function that does all the heavy lifting.
def _process(bar_list: list[str], chunk_size: int, condense: bool, bar_length: int = 12):
    attack_text = []
    pattern_text = []
    n_chunks = len(bar_list) // chunk_size
    if len(bar_list) % chunk_size != 0:
        # For leftover bars
        n_chunks += 1
    if n_chunks == 1:
        prefix = ""

    for i in range(n_chunks):
        starting_bar = chunk_size * i
        ending_bar = min(starting_bar + chunk_size, len(bar_list))
        chunk_bars = bar_list[starting_bar : ending_bar]
        binary_bars = ''.join(to_attack_list(chunk_bars))

        # Process attacks
        grouped_bars = ' '.join(aggregate(chunk_bars, bar_length))

        # Process patterns
        # The order of replacements is important
        pattern_bars = binary_bars.replace(SHORT, "s").replace(TAIL, "t")
        pattern_bars = pattern_bars.replace("ttt", "L' ").replace("st", "L ")
        condensed_pattern_bars = pattern_bars
        # 5 is the longest streak of base pattern s in the song.
        # Iterate in reverse because we need to replace longer patterns first.
        for n_s in range(5, -1, -1):
            condensed_pattern_bars = condensed_pattern_bars.replace(
                n_s * 's' + 'L',
                str(n_s + 1)
            )

        # Add the line for the current chunk to both texts
        attack_content = grouped_bars if condense else binary_bars
        pattern_content = condensed_pattern_bars if condense else pattern_bars
        if n_chunks > 1:
            prefix = f"bars {(starting_bar + 1):02}-{(ending_bar):02}: "
        attack_text.append(prefix + attack_content)
        pattern_text.append(prefix + pattern_content)
    return ('\n'.join(attack_text), '\n'.join(pattern_text))

# Return a string that represents the attacks in the specified bars.
# The string is divided into several lines, each containing a chunk of the bars.
# Each line is prefixed by the bar numbers that the line corresponds to (unless
# the chunk size is bigger than the number of bars, i.e. the bars are "divided"
# into a single chunk)
#
# Example: with ["2-3-1-3", "-3-3-1-1", "2-3-3-1", "2-1-3-3"] as the bar list,
# the result can be:
#
# - with a chunk size of 2, condense set to False:
#   "bars 01-02: xx-xxx-x-xxx-xxx-xxx-x-x
#    bars 03-04: xx-xxx-xxx-xxx-x-xxx-xxx"
#
# - with a chunk size of 2, condense set to True:
#   "bars 01-02: 2 3 1 3 3 3 1 1
#    bars 03-04: 2 3 3 3 1 3 3"
#
# - with a chunk size of 4, condense set to False:
#   "xx-xxx-x-xxx-xxx-xxx-x-xxx-xxx-xxx-xxx-x-xxx-xxx"
#   (no prefix)
#
# - with a chunk size of 4, condense set to True:
#   "2 3 1 3 3 3 1 3 3 3 3 1 3 3"
#   (no prefix)
def to_attacks(bar_list: list[str], chunk_size: int, condense: bool, bar_length: int):
    return _process(bar_list, chunk_size, condense, bar_length)[0]

# Look for base patterns s ('xx-x'), t ('-x') and L ('xx-x-x') in the given list
# of bars. Return a string containing the sequence of base patterns (and any
# remaining attacks) that represents the list of bars, divided into chunks of
# the specified size.
# If condense is set to True, sequences 'L', 'sL', 'ssL', 'sssL' (and so on) are
# replaced by '1', '2', '3', '4' (and so on).
#
# Example: with ["2-3-3-1", "-3-3-3", "-3-3-3", "-1-3-1-3"] as the bar list,
# the result can be:
#
# - with a chunk size of 2, condense set to False:
#   "bars 01-02: ssLssxx
#    bars 03-04: tssLLxx"
# 
# - with a chunk size of 2, condense set to True:
#   "bars 01-02: 3ssxx
#    bars 03-04: t31xx"
#
# - with a chunk size of 4, condense set to False:
#   "ssLsssssLLxx"
#
# - with a chunk size of 4, condense set to True:
#   "361xx"
def to_patterns(bar_list: list[str], chunk_size: int, condense: bool):
    return _process(bar_list, chunk_size, condense)[1]

# [/!\ Assumes 12/8]
# Return a pair of strings that looks like 12/8 sheet music.
# Example: the bar type '2-3-1-3' becomes:
# ("┍┯╸┍┯┑╺┯╸┍┯┑", "╵╵┑╵╵╵┑╵┑╵╵╵")
# which, if printed on two lines, is:
# ┍┯╸┍┯┑╺┯╸┍┯┑
# ╵╵┑╵╵╵┑╵┑╵╵╵
def to_beams(bar_type: str) -> tuple[str, str]:
    bar = bar_type_to_attacks(bar_type)
    sheet_music = [[], []]  # start with two empty 'strings'
    # Process the bar in chunks of three 8th notes
    # (we assume there are 12 characters in the bar)
    for quarter in range(4):
        for triplet in range(3):
            attack = (bar[3 * quarter + triplet] == ATTACK)
            # first line, beams
            if triplet == 0:
                sheet_music[0].append('┍' if attack else '╺')
            elif triplet == 1:
                sheet_music[0].append('┯' if attack else '━')
            elif triplet == 2:
                sheet_music[0].append('┑' if attack else '╸')
            # second line, hamps or rests
            sheet_music[1].append('╵' if attack else '┑')
    return (''.join(sheet_music[0]), ''.join(sheet_music[1]))

# [/!\ Assumes 12/8]
# Return a list of lines that represents the 12/8 sheet music of the specified
# list of bar types
def score(bar_list: list[str], bars_per_line: int = 8) -> list[str]:
    sheet_music = [to_beams(bar_type) for bar_type in bar_list]
    lines = []
    for i, bar in enumerate(sheet_music):
        if i % bars_per_line == 0:
            lines.append([])        # Empty line
            lines.append([])        # Beams
            lines.append([])        # Hamps
            lines[-2].append('│')   # Bar line
            lines[-1].append('│')
        lines[-2].extend([' ', bar[0], ' │'])
        lines[-1].extend([' ', bar[1], ' │'])
    return [''.join(line) for line in lines]


#============================ Generating the files =============================

def detail_attacks(bar_list: list[str], chunk_sizes: list[int], title: str, bar_length: int):
    text = []
    
    # Whole list of bars
    for condensed in (False, True):
        text.append(f"{title}{', grouped' if condensed else ''}:")
        text.append(to_attacks(bar_list, len(bar_list), condensed, bar_length))
        text.append('')

    # Chunks of bars
    for chunk_size in chunk_sizes:
        for condensed in (False, True):
            text.append(f"In chunks of {chunk_size} bars"
                f"{', grouped' if condensed else ''}:")
            text.append(to_attacks(bar_list, chunk_size, condensed, bar_length))
            text.append('')
    return text

def detail_patterns(bar_list: list[str], chunk_sizes: list[int], title: str):
    text = []

    # General information about base patterns
    text.append(f"Base patterns, where {ATTACK} is a note and {REST} is a rest:")
    text.append(f"s: {SHORT}")
    text.append(f"L: {LONG}")
    text.append("Longer, condensed patterns:")
    for i in range(1, 5):
        text.append(f"{i}: {'s' * (i-1)}L ({SHORT * (i-1) + LONG})")
    text.append("...")
    text.append("Variant patterns:")
    text.append(f"L': {LONG_VARIANT}")
    for i in range(2, 4):
        text.append(f"{i}': {'s' * (i-1)}L' ({SHORT * (i-1) + LONG_VARIANT})")
    text.append("\n")

    # Whole list of bars
    for condensed in (False, True):
        text.append(f"{title}, as {'condensed' if condensed else 'base'} patterns:")
        text.append(to_patterns(bar_list, len(bar_list), condensed))
        text.append('')

    # Chunks of bars
    for chunk_size in chunk_sizes:
        for condensed in (False, True):
            text.append(f"In chunks of {chunk_size} bars,"
                f" as {'condensed' if condensed else 'base'} patterns:")
            text.append(to_patterns(bar_list, chunk_size, condensed))
            text.append('')
    return text

def detail_score(bar_list: list[str], bars_per_line: int = 8):
    text = score(bar_list, bars_per_line)
    # Each line of bars takes 3 lines of text
    n_lines_per_system = 3
    # Add bar numbers at the start of every line of bars
    for i in range(0, len(text), n_lines_per_system):
        text[i] = f"{bars_per_line * i // n_lines_per_system + 1}"
    # If we’re writing the whole song with the default 8 bars per line,
    # manually add in timecodes and a few comments
    if bar_list == AGRIMOTOR_BARS and bars_per_line == 8:
        text[0 * n_lines_per_system] += " [0:06]"
        text[1 * n_lines_per_system] += " [0:20]"
        text[2 * n_lines_per_system] += " [0:33] Stop drone"
        text[3 * n_lines_per_system] += " [0:47]"
        text[4 * n_lines_per_system] += " [1:00] Descending riff \\m/"
        text[6 * n_lines_per_system] += " [1:27]"
        text[8 * n_lines_per_system] += " [1:54] Repeat descending riff"
        text[10 * n_lines_per_system] += " [2:21] Repeat 0:06 but with rests on beat 3"
    return text

def main():
    with open("Agrimotor_attacks.txt", 'w', encoding="utf-8") as f:
        f.write("Agrimotor - Attacks\n")
        f.write("===================\n\n")
        f.write('\n'.join(detail_attacks(
            AGRIMOTOR_BARS,
            chunk_sizes=CHUNK_SIZES,
            title="Whole song",
            bar_length=BAR_LENGTH
        )))

    with open("Agrimotor_patterns.txt", 'w', encoding="utf-8") as f:
        f.write("Agrimotor - Patterns\n")
        f.write("====================\n\n")
        f.write('\n'.join(detail_patterns(
            AGRIMOTOR_BARS,
            chunk_sizes=CHUNK_SIZES,
            title="Whole song"
        )))

    with open("Agrimotor_music_sheet.txt", 'w', encoding="utf-8") as f:
        f.write("Agrimotor - Music sheet\n")
        f.write("=======================\n\n")
        f.writelines('\n'.join(detail_score(
            AGRIMOTOR_BARS,
            bars_per_line=BARS_PER_LINE
        )))

if __name__ == '__main__':
    main()
