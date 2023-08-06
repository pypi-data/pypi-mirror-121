#!/usr/bin/env python
""" Unicode 2 Ascii command-line tool and library
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import locale
import logging
import os
import sys
import unicodedata

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: unicode2ascii - Unicode to Ascii command-line tool and library v1.1.1 (September 26, 2021) by Hubert Tournier $"

# Conversion table for Unicode characters incorrectly translated to ASCII:
corrected_unicode_to_ascii = {
    "¼": "1/4",
    "½": "1/2",
    "¾": "3/4",
    "⅐": "1/7",
    "⅑": "1/9",
    "⅒": "1/10",
    "⅓": "1/3",
    "⅔": "2/3",
    "⅕": "1/5",
    "⅖": "2/5",
    "⅗": "3/5",
    "⅘": "4/5",
    "⅙": "1/6",
    "⅚": "5/6",
    "⅛": "1/8",
    "⅜": "3/8",
    "⅝": "5/8",
    "⅞": "7/8",
    "⅟": "1/",
    "↉": "0/3",
}

# Conversion table for Unicode characters with no translation to ASCII:
additional_unicode_to_ascii = {
    "‱": " ",  # PER TEN THOUSAND SIGN
    "—": "-",  # EM DASH
    "–": "-",  # EN DASH
    "‒": "-",  # FIGURE DASH
    "―": "-",  # HORIZONTAL BAR
    "‐": "-",  # HYPHEN
    "⁃": "-",  # HYPHEN BULLET
    "‧": "-",  # HYPHENATION POINT
    "˗": "-",  # MODIFIER LETTER MINUS SIGN
    "‑": "-",  # NON-BREAKING HYPHEN
    "ʽ": ",",  # MODIFIER LETTER REVERSED COMMA
    "ʻ": ",",  # MODIFIER LETTER TURNED COMMA
    "⁏": ";",  # REVERSED SEMICOLON
    "ˑ": ":",  # MODIFIER LETTER HALF TRIANGULAR COLON
    "˸": ":",  # MODIFIER LETTER RAISED COLON
    "ː": ":",  # MODIFIER LETTER TRIANGULAR COLON
    "⁝": ":",  # TRICOLON
    "⁞": ":",  # VERTICAL FOUR DOTS
    "¡": "!",  # INVERTED EXCLAMATION MARK
    "¬": "!",  # NOT SIGN
    "‽": "?!",  # INTERROBANG
    "¿": "?",  # INVERTED QUESTION MARK
    "⁙": ".....",  # FIVE DOT PUNCTUATION
    "⁛": "....",  # FOUR DOT MARK
    "⁘": "....",  # FOUR DOT PUNCTUATION
    "⁖": "...",  # THREE DOT PUNCTUATION
    "⁚": "..",  # TWO DOT PUNCTUATION
    "•": ".",  # BULLET
    "·": ".",  # MIDDLE DOT
    "⁜": ".+.",  # DOTTED CROSS
    "※": ".x.",  # REFERENCE MARK
    "⁗": "''''",  # QUADRUPLE PRIME
    "‷": "'''",  # REVERSED TRIPLE PRIME
    "‴": "'''",  # TRIPLE PRIME
    "″": "''",  # DOUBLE PRIME
    "˶": "''",  # MODIFIER LETTER MIDDLE DOUBLE ACUTE ACCENT
    "‶": "''",  # REVERSED DOUBLE PRIME
    "ˊ": "'",  # MODIFIER LETTER ACUTE ACCENT
    "ʼ": "'",  # MODIFIER LETTER APOSTROPHE
    "ˏ": "'",  # MODIFIER LETTER LOW ACUTE ACCENT
    "ʹ": "'",  # MODIFIER LETTER PRIME
    "′": "'",  # PRIME
    "‵": "'",  # REVERSED PRIME
    "’": "'",  # RIGHT SINGLE QUOTATION MARK
    "‚": "'",  # SINGLE LOW-9 QUOTATION MARK
    "°": "°",  # DEGREE SIGN
    "©": "(c)",  # COPYRIGHT SIGN
    "¶": "(p)",  # PILCROW SIGN
    "⁋": "(q)",  # REVERSED PILCROW SIGN
    "®": "(r)",  # REGISTERED SIGN
    "§": "(s)",  # SECTION SIGN
    "⁅": "[",  # LEFT SQUARE BRACKET WITH QUILL
    "⁆": "]",  # RIGHT SQUARE BRACKET WITH QUILL
    "⁌": "*",  # BLACK LEFTWARDS BULLET
    "⁍": "*",  # BLACK RIGHTWARDS BULLET
    "⁕": "*",  # FLOWER PUNCTUATION MARK
    "⁎": "*",  # LOW ASTERISK
    "×": "*",  # MULTIPLICATION SIGN
    "‣": "*",  # TRIANGULAR BULLET
    "⁑": "**",  # TWO ASTERISKS ALIGNED VERTICALLY
    "⁂": "***",  # ASTERISM
    "÷": "/",  # DIVISION SIGN
    "⁄": "/",  # FRACTION SLASH
    "‟": '"',  # DOUBLE HIGH-REVERSED-9 QUOTATION MARK
    "„": '"',  # DOUBLE LOW-9 QUOTATION MARK
    "ˮ": '"',  # MODIFIER LETTER DOUBLE APOSTROPHE
    "ʺ": '"',  # MODIFIER LETTER DOUBLE PRIME
    "”": '"',  # RIGHT DOUBLE QUOTATION MARK
    "⁒": "%",  # COMMERCIAL MINUS SIGN
    "‰": "%0",  # PER MILLE SIGN
    "‘": "`",  # LEFT SINGLE QUOTATION MARK
    "ˋ": "`",  # MODIFIER LETTER GRAVE ACCENT
    "ˎ": "`",  # MODIFIER LETTER LOW GRAVE ACCENT
    "˴": "`",  # MODIFIER LETTER MIDDLE GRAVE ACCENT
    "‛": "`",  # SINGLE HIGH-REVERSED-9 QUOTATION MARK
    "“": "``",  # LEFT DOUBLE QUOTATION MARK
    "˵": "``",  # MODIFIER LETTER MIDDLE DOUBLE GRAVE ACCENT
    "‸": "^",  # CARET
    "ˆ": "^",  # MODIFIER LETTER CIRCUMFLEX ACCENT
    "˰": "^",  # MODIFIER LETTER LOW UP ARROWHEAD
    "˄": "^",  # MODIFIER LETTER UP ARROWHEAD
    "˖": "+",  # MODIFIER LETTER PLUS SIGN
    "±": "+/-",  # PLUS-MINUS SIGN
    "˿": "<-",  # MODIFIER LETTER LOW LEFT ARROW
    "˂": "<",  # MODIFIER LETTER LEFT ARROWHEAD
    "˱": "<",  # MODIFIER LETTER LOW LEFT ARROWHEAD
    "‹": "<",  # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    "«": "<<",  # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    "˲": ">",  # MODIFIER LETTER LOW RIGHT ARROWHEAD
    "˃": ">",  # MODIFIER LETTER RIGHT ARROWHEAD
    "›": ">",  # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    "»": ">>",  # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    "¦": "|",  # BROKEN BAR
    "‖": "||",  # DOUBLE VERTICAL LINE
    "˷": "~",  # MODIFIER LETTER LOW TILDE
    "⁓": "~",  # SWUNG DASH
    "↊": "2",  # TURNED DIGIT TWO
    "↋": "3",  # TURNED DIGIT THREE
    "¢": "c",  # CENT SIGN
    "¤": "currency",  # CURRENCY SIGN
    "£": "GBP",  # POUND SIGN
    "¥": "JPY",  # YEN SIGN
    "µ": "mu",  # MICRO SIGN
    "˅": "v",  # MODIFIER LETTER DOWN ARROWHEAD
    "˯": "v",  # MODIFIER LETTER LOW DOWN ARROWHEAD
    "ↀ": "_I",  # ROMAN NUMERAL ONE THOUSAND C D
    "ↁ": "_V",  # ROMAN NUMERAL FIVE THOUSAND
    "ↂ": "_X",  # ROMAN NUMERAL TEN THOUSAND
    "ↆ": "L",  # ROMAN NUMERAL FIFTY EARLY FORM
    "ↇ": "_L",  # ROMAN NUMERAL FIFTY THOUSAND
    "ↈ": "_C",  # ROMAN NUMERAL ONE HUNDRED THOUSAND
    "ↅ": "6",  # ROMAN NUMERAL SIX LATE FORM
    "Æ": "AE",  # LATIN CAPITAL LETTER AE
    "Ǽ": "AE",  # LATIN CAPITAL LETTER AE WITH ACUTE
    "Ǣ": "AE",  # LATIN CAPITAL LETTER AE WITH MACRON
    "æ": "ae",  # LATIN SMALL LETTER AE
    "ǽ": "ae",  # LATIN SMALL LETTER AE WITH ACUTE
    "ǣ": "ae",  # LATIN SMALL LETTER AE WITH MACRON
    "Ⱥ": "A",  # LATIN CAPITAL LETTER A WITH STROKE
    "Ƀ": "B",  # LATIN CAPITAL LETTER B WITH STROKE
    "ƀ": "b",  # LATIN SMALL LETTER B WITH STROKE
    "Ɓ": "B",  # LATIN CAPITAL LETTER B WITH HOOK
    "Ƃ": "B",  # LATIN CAPITAL LETTER B WITH TOPBAR
    "ƃ": "b",  # LATIN SMALL LETTER B WITH TOPBAR
    "Ȼ": "C",  # LATIN CAPITAL LETTER C WITH STROKE
    "ȼ": "c",  # LATIN SMALL LETTER C WITH STROKE
    "Ƈ": "C",  # LATIN CAPITAL LETTER C WITH HOOK
    "ƈ": "c",  # LATIN SMALL LETTER C WITH HOOK
    "ↄ": "c",  # LATIN SMALL LETTER REVERSED C
    "Ↄ": "C",  # ROMAN NUMERAL REVERSED ONE HUNDRED
    "Đ": "D",  # LATIN CAPITAL LETTER D WITH STROKE
    "đ": "d",  # LATIN SMALL LETTER D WITH STROKE
    "Ð": "ETH",  # LATIN CAPITAL LETTER ETH
    "ð": "eth",  # LATIN SMALL LETTER ETH
    "ȸ": "db",  # LATIN SMALL LETTER DB DIGRAPH
    "Ɖ": "D",  # LATIN CAPITAL LETTER AFRICAN D
    "Ɗ": "D",  # LATIN CAPITAL LETTER D WITH HOOK
    "Ƌ": "D",  # LATIN CAPITAL LETTER D WITH TOPBAR
    "ƌ": "d",  # LATIN SMALL LETTER D WITH TOPBAR
    "ȡ": "d",  # LATIN SMALL LETTER D WITH CURL
    "Ɇ": "E",  # LATIN CAPITAL LETTER E WITH STROKE
    "ɇ": "e",  # LATIN SMALL LETTER E WITH STROKE
    "Ǝ": "E",  # LATIN CAPITAL LETTER REVERSED E
    "ǝ": "e",  # LATIN SMALL LETTER TURNED E
    "Ə": "SCHWA",  # LATIN CAPITAL LETTER SCHWA
    "ə": "schwa",  # LATIN SMALL LETTER SCHWA
    "Ɛ": "E",  # LATIN CAPITAL LETTER OPEN E
    "Ƒ": "F",  # LATIN CAPITAL LETTER F WITH HOOK
    "ƒ": "f",  # LATIN SMALL LETTER F WITH HOOK
    "Ǥ": "G",  # LATIN CAPITAL LETTER G WITH STROKE
    "ǥ": "g",  # LATIN SMALL LETTER G WITH STROKE
    "Ɠ": "G",  # LATIN CAPITAL LETTER G WITH HOOK
    "Ɣ": "g",  # LATIN CAPITAL LETTER GAMMA
    "Ƣ": "OI",  # LATIN CAPITAL LETTER OI
    "ƣ": "oi",  # LATIN SMALL LETTER OI
    "Ħ": "H",  # LATIN CAPITAL LETTER H WITH STROKE
    "ħ": "h",  # LATIN SMALL LETTER H WITH STROKE
    "ƕ": "hv",  # LATIN SMALL LETTER HV
    "Ƕ": "HWAIR",  # LATIN CAPITAL LETTER HWAIR
    "ʱ": "h",  # MODIFIER LETTER SMALL H WITH HOOK
    "ı": "i",  # LATIN SMALL LETTER DOTLESS I
    "Ɨ": "I",  # LATIN CAPITAL LETTER I WITH STROKE
    "Ɩ": "I",  # LATIN CAPITAL LETTER IOTA
    "ȷ": "j",  # LATIN SMALL LETTER DOTLESS J
    "Ɉ": "J",  # LATIN CAPITAL LETTER J WITH STROKE
    "ɉ": "j",  # LATIN SMALL LETTER J WITH STROKE
    "Ƙ": "K",  # LATIN CAPITAL LETTER K WITH HOOK
    "ƙ": "k",  # LATIN SMALL LETTER K WITH HOOK
    "Ł": "L",  # LATIN CAPITAL LETTER L WITH STROKE
    "ł": "l",  # LATIN SMALL LETTER L WITH STROKE
    "Ƚ": "L",  # LATIN CAPITAL LETTER L WITH BAR
    "ƚ": "l",  # LATIN SMALL LETTER L WITH BAR
    "ȴ": "l",  # LATIN SMALL LETTER L WITH CURL
    "ƛ": "l",  # LATIN SMALL LETTER LAMBDA WITH STROKE
    "Ɲ": "N",  # LATIN CAPITAL LETTER N WITH LEFT HOOK
    "Ƞ": "N",  # LATIN CAPITAL LETTER N WITH LONG RIGHT LEG
    "ƞ": "n",  # LATIN SMALL LETTER N WITH LONG RIGHT LEG
    "ȵ": "n",  # LATIN SMALL LETTER N WITH CURL
    "Ŋ": "ENG",  # LATIN CAPITAL LETTER ENG
    "ŋ": "eng",  # LATIN SMALL LETTER ENG
    "Ø": "O",  # LATIN CAPITAL LETTER O WITH STROKE
    "Ǿ": "O",  # LATIN CAPITAL LETTER O WITH STROKE AND ACUTE
    "ø": "o",  # LATIN SMALL LETTER O WITH STROKE
    "ǿ": "o",  # LATIN SMALL LETTER O WITH STROKE AND ACUTE
    "Œ": "OE",  # LATIN CAPITAL LIGATURE OE
    "œ": "oe",  # LATIN SMALL LIGATURE OE
    "Ɔ": "O",  # LATIN CAPITAL LETTER OPEN O
    "Ɵ": "O",  # LATIN CAPITAL LETTER O WITH MIDDLE TILDE
    "Ȣ": "OU",  # LATIN CAPITAL LETTER OU
    "ȣ": "ou",  # LATIN SMALL LETTER OU
    "Ƥ": "P",  # LATIN CAPITAL LETTER P WITH HOOK
    "ƥ": "p",  # LATIN SMALL LETTER P WITH HOOK
    "ȹ": "qp",  # LATIN SMALL LETTER QP DIGRAPH
    "Ɋ": "Q",  # LATIN CAPITAL LETTER SMALL Q WITH HOOK TAIL
    "ɋ": "q",  # LATIN SMALL LETTER Q WITH HOOK TAIL
    "ĸ": "kra",  # LATIN SMALL LETTER KRA
    "Ʀ": "YR",  # LATIN LETTER YR
    "Ɍ": "R",  # LATIN CAPITAL LETTER R WITH STROKE
    "ɍ": "r",  # LATIN SMALL LETTER R WITH STROKE
    "ʴ": "r",  # MODIFIER LETTER SMALL TURNED R
    "ʵ": "r",  # MODIFIER LETTER SMALL TURNED R WITH HOOK
    "ɼ": "r",  # LATIN SMALL LETTER R WITH LONG LEG
    "ʶ": "R",  # MODIFIER LETTER SMALL CAPITAL INVERTED R
    "ß": "ss",  # LATIN SMALL LETTER SHARP S
    "ȿ": "s",  # LATIN SMALL LETTER S WITH SWASH TAIL
    "Ʃ": "ESH",  # LATIN CAPITAL LETTER ESH
    "ƪ": "esh",  # LATIN LETTER REVERSED ESH LOOP
    "Ŧ": "T",  # LATIN CAPITAL LETTER T WITH STROKE
    "ŧ": "t",  # LATIN SMALL LETTER T WITH STROKE
    "Ⱦ": "T",  # LATIN CAPITAL LETTER T WITH DIAGONAL STROKE
    "ƫ": "t",  # LATIN SMALL LETTER T WITH PALATAL HOOK
    "Ƭ": "T",  # LATIN CAPITAL LETTER T WITH HOOK
    "ƭ": "t",  # LATIN SMALL LETTER T WITH HOOK
    "Ʈ": "T",  # LATIN CAPITAL LETTER T WITH RETROFLEX HOOK
    "ȶ": "t",  # LATIN SMALL LETTER T WITH CURL
    "Ʉ": "U",  # LATIN CAPITAL LETTER U BAR
    "Ɯ": "M",  # LATIN CAPITAL LETTER TURNED M
    "Ʊ": "U",  # LATIN CAPITAL LETTER UPSILON
    "Ʋ": "V",  # LATIN CAPITAL LETTER V WITH HOOK
    "Ʌ": "V",  # LATIN CAPITAL LETTER TURNED V
    "Ɏ": "Y",  # LATIN CAPITAL LETTER Y WITH STROKE
    "ɏ": "y",  # LATIN SMALL LETTER Y WITH STROKE
    "Ƴ": "Y",  # LATIN CAPITAL LETTER Y WITH HOOK
    "ƴ": "y",  # LATIN SMALL LETTER Y WITH HOOK
    "Ȝ": "YOGH",  # LATIN CAPITAL LETTER YOGH
    "ȝ": "yogh",  # LATIN SMALL LETTER YOGH
    "ƍ": "d",  # LATIN SMALL LETTER TURNED DELTA
    "Ƶ": "Z",  # LATIN CAPITAL LETTER Z WITH STROKE
    "ƶ": "z",  # LATIN SMALL LETTER Z WITH STROKE
    "Ȥ": "Z",  # LATIN CAPITAL LETTER Z WITH HOOK
    "ȥ": "z",  # LATIN SMALL LETTER Z WITH HOOK
    "ɀ": "z",  # LATIN SMALL LETTER Z WITH SWASH TAIL
    "Ʒ": "EZH",  # LATIN CAPITAL LETTER EZH
    "Ǯ": "EZH",  # LATIN CAPITAL LETTER EZH WITH CARON
    "ʒ": "ezh",  # LATIN SMALL LETTER EZH
    "ǯ": "ezh",  # LATIN SMALL LETTER EZH WITH CARON
    "Ƹ": "EZH",  # LATIN CAPITAL LETTER EZH REVERSED
    "ƹ": "ezh",  # LATIN SMALL LETTER EZH REVERSED
    "ƺ": "ezh",  # LATIN SMALL LETTER EZH WITH TAIL
    "Þ": "THORN",  # LATIN CAPITAL LETTER THORN
    "þ": "thorn",  # LATIN SMALL LETTER THORN
    "Ƿ": "WYNN",  # LATIN CAPITAL LETTER WYNN
    "ƿ": "wynn",  # LATIN LETTER WYNN
    "ƻ": "2",  # LATIN LETTER TWO WITH STROKE
    "Ƨ": "2",  # LATIN CAPITAL LETTER TONE TWO
    "ƨ": "2",  # LATIN SMALL LETTER TONE TWO
    "Ƽ": "5",  # LATIN CAPITAL LETTER TONE FIVE
    "ƽ": "5",  # LATIN SMALL LETTER TONE FIVE
    "Ƅ": "6",  # LATIN CAPITAL LETTER TONE SIX
    "ƅ": "6",  # LATIN SMALL LETTER TONE SIX
    "ǃ": "!",  # LATIN LETTER RETROFLEX CLICK
    'Ѐ': "IE", # CYRILLIC CAPITAL LETTER IE WITH GRAVE
    'Ё': "IO", # CYRILLIC CAPITAL LETTER IO
    'Ђ': "DJE", # CYRILLIC CAPITAL LETTER DJE
    'Ѓ': "GJE", # CYRILLIC CAPITAL LETTER GJE
    'Є': "IE", # CYRILLIC CAPITAL LETTER UKRAINIAN IE
    'Ѕ': "DZE", # CYRILLIC CAPITAL LETTER DZE
    'І': "I", # CYRILLIC CAPITAL LETTER BYELORUSSIAN-UKRAINIAN I
    'Ї': "YI", # CYRILLIC CAPITAL LETTER YI
    'Ј': "JE", # CYRILLIC CAPITAL LETTER JE
    'Љ': "LJE", # CYRILLIC CAPITAL LETTER LJE
    'Њ': "NJE", # CYRILLIC CAPITAL LETTER NJE
    'Ћ': "TSHE", # CYRILLIC CAPITAL LETTER TSHE
    'Ќ': "KJE", # CYRILLIC CAPITAL LETTER KJE
    'Ѝ': "I", # CYRILLIC CAPITAL LETTER I WITH GRAVE
    'Ў': "U", # CYRILLIC CAPITAL LETTER SHORT U
    'Џ': "DZHE", # CYRILLIC CAPITAL LETTER DZHE
    'А': "A", # CYRILLIC CAPITAL LETTER A
    'Б': "BE", # CYRILLIC CAPITAL LETTER BE
    'В': "VE", # CYRILLIC CAPITAL LETTER VE
    'Г': "GHE", # CYRILLIC CAPITAL LETTER GHE
    'Д': "DE", # CYRILLIC CAPITAL LETTER DE
    'Е': "IE", # CYRILLIC CAPITAL LETTER IE
    'Ж': "ZHE", # CYRILLIC CAPITAL LETTER ZHE
    'З': "ZE", # CYRILLIC CAPITAL LETTER ZE
    'И': "I", # CYRILLIC CAPITAL LETTER I
    'Й': "I", # CYRILLIC CAPITAL LETTER SHORT I
    'К': "KA", # CYRILLIC CAPITAL LETTER KA
    'Л': "EL", # CYRILLIC CAPITAL LETTER EL
    'М': "EM", # CYRILLIC CAPITAL LETTER EM
    'Н': "EN", # CYRILLIC CAPITAL LETTER EN
    'О': "O", # CYRILLIC CAPITAL LETTER O
    'П': "PE", # CYRILLIC CAPITAL LETTER PE
    'Р': "ER", # CYRILLIC CAPITAL LETTER ER
    'С': "ES", # CYRILLIC CAPITAL LETTER ES
    'Т': "TE", # CYRILLIC CAPITAL LETTER TE
    'У': "U", # CYRILLIC CAPITAL LETTER U
    'Ф': "EF", # CYRILLIC CAPITAL LETTER EF
    'Х': "HA", # CYRILLIC CAPITAL LETTER HA
    'Ц': "TSE", # CYRILLIC CAPITAL LETTER TSE
    'Ч': "CHE", # CYRILLIC CAPITAL LETTER CHE
    'Ш': "SHA", # CYRILLIC CAPITAL LETTER SHA
    'Щ': "SHCHA", # CYRILLIC CAPITAL LETTER SHCHA
    'Ы': "YERU", # CYRILLIC CAPITAL LETTER YERU
    'Э': "E", # CYRILLIC CAPITAL LETTER E
    'Ю': "YU", # CYRILLIC CAPITAL LETTER YU
    'Я': "YA", # CYRILLIC CAPITAL LETTER YA
    'а': "a", # CYRILLIC SMALL LETTER A
    'б': "be", # CYRILLIC SMALL LETTER BE
    'в': "ve", # CYRILLIC SMALL LETTER VE
    'г': "ghe", # CYRILLIC SMALL LETTER GHE
    'д': "de", # CYRILLIC SMALL LETTER DE
    'е': "ie", # CYRILLIC SMALL LETTER IE
    'ж': "zhe", # CYRILLIC SMALL LETTER ZHE
    'з': "ze", # CYRILLIC SMALL LETTER ZE
    'и': "i", # CYRILLIC SMALL LETTER I
    'й': "i", # CYRILLIC SMALL LETTER SHORT I
    'к': "ka", # CYRILLIC SMALL LETTER KA
    'л': "el", # CYRILLIC SMALL LETTER EL
    'м': "em", # CYRILLIC SMALL LETTER EM
    'н': "en", # CYRILLIC SMALL LETTER EN
    'о': "o", # CYRILLIC SMALL LETTER O
    'п': "pe", # CYRILLIC SMALL LETTER PE
    'р': "er", # CYRILLIC SMALL LETTER ER
    'с': "es", # CYRILLIC SMALL LETTER ES
    'т': "te", # CYRILLIC SMALL LETTER TE
    'у': "u", # CYRILLIC SMALL LETTER U
    'ф': "ef", # CYRILLIC SMALL LETTER EF
    'х': "ha", # CYRILLIC SMALL LETTER HA
    'ц': "tse", # CYRILLIC SMALL LETTER TSE
    'ч': "che", # CYRILLIC SMALL LETTER CHE
    'ш': "sha", # CYRILLIC SMALL LETTER SHA
    'щ': "shcha", # CYRILLIC SMALL LETTER SHCHA
    'ы': "yeru", # CYRILLIC SMALL LETTER YERU
    'э': "e", # CYRILLIC SMALL LETTER E
    'ю': "yu", # CYRILLIC SMALL LETTER YU
    'я': "ya", # CYRILLIC SMALL LETTER YA
    'ѐ': "ie", # CYRILLIC SMALL LETTER IE WITH GRAVE
    'ё': "io", # CYRILLIC SMALL LETTER IO
    'ђ': "dje", # CYRILLIC SMALL LETTER DJE
    'ѓ': "gje", # CYRILLIC SMALL LETTER GJE
    'є': "ie", # CYRILLIC SMALL LETTER UKRAINIAN IE
    'ѕ': "dze", # CYRILLIC SMALL LETTER DZE
    'і': "i", # CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I
    'ї': "yi", # CYRILLIC SMALL LETTER YI
    'ј': "je", # CYRILLIC SMALL LETTER JE
    'љ': "lje", # CYRILLIC SMALL LETTER LJE
    'њ': "nje", # CYRILLIC SMALL LETTER NJE
    'ћ': "tshe", # CYRILLIC SMALL LETTER TSHE
    'ќ': "kje", # CYRILLIC SMALL LETTER KJE
    'ѝ': "i", # CYRILLIC SMALL LETTER I WITH GRAVE
    'ў': "u", # CYRILLIC SMALL LETTER SHORT U
    'џ': "dzhe", # CYRILLIC SMALL LETTER DZHE
    'Ѡ': "OMEGA", # CYRILLIC CAPITAL LETTER OMEGA
    'ѡ': "omega", # CYRILLIC SMALL LETTER OMEGA
    'Ѣ': "YAT", # CYRILLIC CAPITAL LETTER YAT
    'ѣ': "yat", # CYRILLIC SMALL LETTER YAT
    'Ѥ': "E", # CYRILLIC CAPITAL LETTER IOTIFIED E
    'ѥ': "e", # CYRILLIC SMALL LETTER IOTIFIED E
    'Ѧ': "YUS", # CYRILLIC CAPITAL LETTER LITTLE YUS
    'ѧ': "yus", # CYRILLIC SMALL LETTER LITTLE YUS
    'Ѩ': "YUS", # CYRILLIC CAPITAL LETTER IOTIFIED LITTLE YUS
    'ѩ': "yus", # CYRILLIC SMALL LETTER IOTIFIED LITTLE YUS
    'Ѫ': "YUS", # CYRILLIC CAPITAL LETTER BIG YUS
    'ѫ': "yus", # CYRILLIC SMALL LETTER BIG YUS
    'Ѭ': "YUS", # CYRILLIC CAPITAL LETTER IOTIFIED BIG YUS
    'ѭ': "yus", # CYRILLIC SMALL LETTER IOTIFIED BIG YUS
    'Ѯ': "KSI", # CYRILLIC CAPITAL LETTER KSI
    'ѯ': "ksi", # CYRILLIC SMALL LETTER KSI
    'Ѱ': "PSI", # CYRILLIC CAPITAL LETTER PSI
    'ѱ': "psi", # CYRILLIC SMALL LETTER PSI
    'Ѳ': "FITA", # CYRILLIC CAPITAL LETTER FITA
    'ѳ': "fita", # CYRILLIC SMALL LETTER FITA
    'Ѵ': "IZHITSA", # CYRILLIC CAPITAL LETTER IZHITSA
    'ѵ': "izhitsa", # CYRILLIC SMALL LETTER IZHITSA
    'Ѷ': "IZHITSA", # CYRILLIC CAPITAL LETTER IZHITSA WITH DOUBLE GRAVE ACCENT
    'ѷ': "izhitsa", # CYRILLIC SMALL LETTER IZHITSA WITH DOUBLE GRAVE ACCENT
    'Ѹ': "UK", # CYRILLIC CAPITAL LETTER UK
    'ѹ': "uk", # CYRILLIC SMALL LETTER UK
    'Ѻ': "OMEGA", # CYRILLIC CAPITAL LETTER ROUND OMEGA
    'ѻ': "omega", # CYRILLIC SMALL LETTER ROUND OMEGA
    'Ѽ': "OMEGA", # CYRILLIC CAPITAL LETTER OMEGA WITH TITLO
    'ѽ': "omega", # CYRILLIC SMALL LETTER OMEGA WITH TITLO
    'Ѿ': "OT", # CYRILLIC CAPITAL LETTER OT
    'ѿ': "ot", # CYRILLIC SMALL LETTER OT
    'Ҁ': "KOPPA", # CYRILLIC CAPITAL LETTER KOPPA
    'ҁ': "koppa", # CYRILLIC SMALL LETTER KOPPA
    'Ҋ': "I", # CYRILLIC CAPITAL LETTER SHORT I WITH TAIL
    'ҋ': "i", # CYRILLIC SMALL LETTER SHORT I WITH TAIL
    'Ҏ': "ER", # CYRILLIC CAPITAL LETTER ER WITH TICK
    'ҏ': "er", # CYRILLIC SMALL LETTER ER WITH TICK
    'Ґ': "GHE", # CYRILLIC CAPITAL LETTER GHE WITH UPTURN
    'ґ': "ghe", # CYRILLIC SMALL LETTER GHE WITH UPTURN
    'Ғ': "GHE", # CYRILLIC CAPITAL LETTER GHE WITH STROKE
    'ғ': "ghe", # CYRILLIC SMALL LETTER GHE WITH STROKE
    'Ҕ': "GHE", # CYRILLIC CAPITAL LETTER GHE WITH MIDDLE HOOK
    'ҕ': "ghe", # CYRILLIC SMALL LETTER GHE WITH MIDDLE HOOK
    'Җ': "ZHE", # CYRILLIC CAPITAL LETTER ZHE WITH DESCENDER
    'җ': "zhe", # CYRILLIC SMALL LETTER ZHE WITH DESCENDER
    'Ҙ': "ZE", # CYRILLIC CAPITAL LETTER ZE WITH DESCENDER
    'ҙ': "ze", # CYRILLIC SMALL LETTER ZE WITH DESCENDER
    'Қ': "KA", # CYRILLIC CAPITAL LETTER KA WITH DESCENDER
    'қ': "ka", # CYRILLIC SMALL LETTER KA WITH DESCENDER
    'Ҝ': "KA", # CYRILLIC CAPITAL LETTER KA WITH VERTICAL STROKE
    'ҝ': "ka", # CYRILLIC SMALL LETTER KA WITH VERTICAL STROKE
    'Ҟ': "KA", # CYRILLIC CAPITAL LETTER KA WITH STROKE
    'ҟ': "ka", # CYRILLIC SMALL LETTER KA WITH STROKE
    'Ҡ': "KA", # CYRILLIC CAPITAL LETTER BASHKIR KA
    'ҡ': "ka", # CYRILLIC SMALL LETTER BASHKIR KA
    'Ң': "EN", # CYRILLIC CAPITAL LETTER EN WITH DESCENDER
    'ң': "en", # CYRILLIC SMALL LETTER EN WITH DESCENDER
    'Ҥ': "ENGHE", # CYRILLIC CAPITAL LIGATURE EN GHE
    'ҥ': "enghe", # CYRILLIC SMALL LIGATURE EN GHE
    'Ҧ': "PE", # CYRILLIC CAPITAL LETTER PE WITH MIDDLE HOOK
    'ҧ': "pe", # CYRILLIC SMALL LETTER PE WITH MIDDLE HOOK
    'Ҩ': "HA", # CYRILLIC CAPITAL LETTER ABKHASIAN HA
    'ҩ': "ha", # CYRILLIC SMALL LETTER ABKHASIAN HA
    'Ҫ': "ES", # CYRILLIC CAPITAL LETTER ES WITH DESCENDER
    'ҫ': "es", # CYRILLIC SMALL LETTER ES WITH DESCENDER
    'Ҭ': "TE", # CYRILLIC CAPITAL LETTER TE WITH DESCENDER
    'ҭ': "te", # CYRILLIC SMALL LETTER TE WITH DESCENDER
    'Ү': "U", # CYRILLIC CAPITAL LETTER STRAIGHT U
    'ү': "u", # CYRILLIC SMALL LETTER STRAIGHT U
    'Ұ': "U", # CYRILLIC CAPITAL LETTER STRAIGHT U WITH STROKE
    'ұ': "u", # CYRILLIC SMALL LETTER STRAIGHT U WITH STROKE
    'Ҳ': "HA", # CYRILLIC CAPITAL LETTER HA WITH DESCENDER
    'ҳ': "ha", # CYRILLIC SMALL LETTER HA WITH DESCENDER
    'Ҵ': "TETSE", # CYRILLIC CAPITAL LIGATURE TE TSE
    'ҵ': "tetse", # CYRILLIC SMALL LIGATURE TE TSE
    'Ҷ': "CHE", # CYRILLIC CAPITAL LETTER CHE WITH DESCENDER
    'ҷ': "che", # CYRILLIC SMALL LETTER CHE WITH DESCENDER
    'Ҹ': "CHE", # CYRILLIC CAPITAL LETTER CHE WITH VERTICAL STROKE
    'ҹ': "che", # CYRILLIC SMALL LETTER CHE WITH VERTICAL STROKE
    'Һ': "SHHA", # CYRILLIC CAPITAL LETTER SHHA
    'һ': "shha", # CYRILLIC SMALL LETTER SHHA
    'Ҽ': "CHE", # CYRILLIC CAPITAL LETTER ABKHASIAN CHE
    'ҽ': "che", # CYRILLIC SMALL LETTER ABKHASIAN CHE
    'Ҿ': "CHE", # CYRILLIC CAPITAL LETTER ABKHASIAN CHE WITH DESCENDER
    'ҿ': "che", # CYRILLIC SMALL LETTER ABKHASIAN CHE WITH DESCENDER
    'Ӏ': "PALOCHKA", # CYRILLIC LETTER PALOCHKA
    'Ӂ': "ZHE", # CYRILLIC CAPITAL LETTER ZHE WITH BREVE
    'ӂ': "zhe", # CYRILLIC SMALL LETTER ZHE WITH BREVE
    'Ӄ': "KA", # CYRILLIC CAPITAL LETTER KA WITH HOOK
    'ӄ': "ka", # CYRILLIC SMALL LETTER KA WITH HOOK
    'Ӆ': "EL", # CYRILLIC CAPITAL LETTER EL WITH TAIL
    'ӆ': "el", # CYRILLIC SMALL LETTER EL WITH TAIL
    'Ӈ': "EN", # CYRILLIC CAPITAL LETTER EN WITH HOOK
    'ӈ': "en", # CYRILLIC SMALL LETTER EN WITH HOOK
    'Ӊ': "EN", # CYRILLIC CAPITAL LETTER EN WITH TAIL
    'ӊ': "en", # CYRILLIC SMALL LETTER EN WITH TAIL
    'Ӌ': "CHE", # CYRILLIC CAPITAL LETTER KHAKASSIAN CHE
    'ӌ': "che", # CYRILLIC SMALL LETTER KHAKASSIAN CHE
    'Ӎ': "EM", # CYRILLIC CAPITAL LETTER EM WITH TAIL
    'ӎ': "em", # CYRILLIC SMALL LETTER EM WITH TAIL
    'ӏ': "palochka", # CYRILLIC SMALL LETTER PALOCHKA
    'Ӑ': "A", # CYRILLIC CAPITAL LETTER A WITH BREVE
    'ӑ': "a", # CYRILLIC SMALL LETTER A WITH BREVE
    'Ӓ': "A", # CYRILLIC CAPITAL LETTER A WITH DIAERESIS
    'ӓ': "a", # CYRILLIC SMALL LETTER A WITH DIAERESIS
    'Ӕ': "AIE", # CYRILLIC CAPITAL LIGATURE A IE
    'ӕ': "aie", # CYRILLIC SMALL LIGATURE A IE
    'Ӗ': "IE", # CYRILLIC CAPITAL LETTER IE WITH BREVE
    'ӗ': "ie", # CYRILLIC SMALL LETTER IE WITH BREVE
    'Ә': "SCHWA", # CYRILLIC CAPITAL LETTER SCHWA
    'ә': "schwa", # CYRILLIC SMALL LETTER SCHWA
    'Ӛ': "SCHWA", # CYRILLIC CAPITAL LETTER SCHWA WITH DIAERESIS
    'ӛ': "schwa", # CYRILLIC SMALL LETTER SCHWA WITH DIAERESIS
    'Ӝ': "ZHE", # CYRILLIC CAPITAL LETTER ZHE WITH DIAERESIS
    'ӝ': "zhe", # CYRILLIC SMALL LETTER ZHE WITH DIAERESIS
    'Ӟ': "ZE", # CYRILLIC CAPITAL LETTER ZE WITH DIAERESIS
    'ӟ': "ze", # CYRILLIC SMALL LETTER ZE WITH DIAERESIS
    'Ӡ': "DZE", # CYRILLIC CAPITAL LETTER ABKHASIAN DZE
    'ӡ': "dze", # CYRILLIC SMALL LETTER ABKHASIAN DZE
    'Ӣ': "I", # CYRILLIC CAPITAL LETTER I WITH MACRON
    'ӣ': "i", # CYRILLIC SMALL LETTER I WITH MACRON
    'Ӥ': "I", # CYRILLIC CAPITAL LETTER I WITH DIAERESIS
    'ӥ': "i", # CYRILLIC SMALL LETTER I WITH DIAERESIS
    'Ӧ': "O", # CYRILLIC CAPITAL LETTER O WITH DIAERESIS
    'ӧ': "o", # CYRILLIC SMALL LETTER O WITH DIAERESIS
    'Ө': "O", # CYRILLIC CAPITAL LETTER BARRED O
    'ө': "o", # CYRILLIC SMALL LETTER BARRED O
    'Ӫ': "O", # CYRILLIC CAPITAL LETTER BARRED O WITH DIAERESIS
    'ӫ': "o", # CYRILLIC SMALL LETTER BARRED O WITH DIAERESIS
    'Ӭ': "E", # CYRILLIC CAPITAL LETTER E WITH DIAERESIS
    'ӭ': "e", # CYRILLIC SMALL LETTER E WITH DIAERESIS
    'Ӯ': "U", # CYRILLIC CAPITAL LETTER U WITH MACRON
    'ӯ': "u", # CYRILLIC SMALL LETTER U WITH MACRON
    'Ӱ': "U", # CYRILLIC CAPITAL LETTER U WITH DIAERESIS
    'ӱ': "u", # CYRILLIC SMALL LETTER U WITH DIAERESIS
    'Ӳ': "U", # CYRILLIC CAPITAL LETTER U WITH DOUBLE ACUTE
    'ӳ': "u", # CYRILLIC SMALL LETTER U WITH DOUBLE ACUTE
    'Ӵ': "CHE", # CYRILLIC CAPITAL LETTER CHE WITH DIAERESIS
    'ӵ': "che", # CYRILLIC SMALL LETTER CHE WITH DIAERESIS
    'Ӷ': "GHE", # CYRILLIC CAPITAL LETTER GHE WITH DESCENDER
    'ӷ': "ghe", # CYRILLIC SMALL LETTER GHE WITH DESCENDER
    'Ӹ': "YERU", # CYRILLIC CAPITAL LETTER YERU WITH DIAERESIS
    'ӹ': "yeru", # CYRILLIC SMALL LETTER YERU WITH DIAERESIS
    'Ӻ': "GHE", # CYRILLIC CAPITAL LETTER GHE WITH STROKE AND HOOK
    'ӻ': "ghe", # CYRILLIC SMALL LETTER GHE WITH STROKE AND HOOK
    'Ӽ': "HA", # CYRILLIC CAPITAL LETTER HA WITH HOOK
    'ӽ': "ha", # CYRILLIC SMALL LETTER HA WITH HOOK
    'Ӿ': "HA", # CYRILLIC CAPITAL LETTER HA WITH STROKE
    'ӿ': "ha", # CYRILLIC SMALL LETTER HA WITH STROKE
}

# Conversion table from Unicode categories to text:
categories_to_text = {
    "L": "Letter",
    "Lu": "Letter, uppercase",
    "Ll": "Letter, lowercase",
    "Lt": "Letter, titlecase",
    "Lm": "Letter, modifier",
    "Lo": "Letter, other",
    "M": "Mark",
    "Mn": "Mark, nonspacing",
    "Mc": "Mark, spacing combining",
    "Me": "Mark, enclosing",
    "N": "Number",
    "Nd": "Number, decimal digit",
    "Nl": "Number, letter",
    "No": "Number, other",
    "P": "Punctuation",
    "Pc": "Punctuation, connector",
    "Pd": "Punctuation, dash",
    "Ps": "Punctuation, open",
    "Pe": "Punctuation, close",
    "Pi": "Punctuation, initial quote",
    "Pf": "Punctuation, final quote",
    "Po": "Punctuation, other",
    "S": "Symbol",
    "Sm": "Symbol, math",
    "Sc": "Symbol, currency",
    "Sk": "Symbol, modifier",
    "So": "Symbol, other",
    "Z": "Separator",
    "Zs": "Separator, space",
    "Zl": "Separator, line",
    "Zp": "Separator, paragraph",
    "C": "Other",
    "Cc": "Other, control",
    "Cf": "Other, format",
    "Cs": "Other, surrogate",
    "Co": "Other, private use",
    "Cn": "Other, not assigned",
}

# Default parameters. Can be overcome by command line options
parameters = {
    "Filter": True,
    "Encoding": "",
    "Force UTF-8": False,
    "Analyze": False,
    "Translated": False,
    "Untranslated": False,
}


################################################################################
def initialize_debugging(program_name):
    """Debugging set up"""
    console_log_format = program_name + ": %(levelname)s: %(message)s"
    logging.basicConfig(format=console_log_format, level=logging.DEBUG)
    logging.disable(logging.INFO)


################################################################################
def display_help():
    """Displays usage and help"""
    print(
        "usage: unicode2ascii [-a|--analyze] [-f|--force] [-t|--translated] [-u|--untranslated]",
        file=sys.stderr,
    )
    print("       [--debug] [--help|-?] [--version] [--]", file=sys.stderr)
    print(
        "  ------------------  --------------------------------------------------",
        file=sys.stderr,
    )
    print("  -a|--analyze        Analyze Unicode characters", file=sys.stderr)
    print("  -f|--force          Assume standard input is UTF-8", file=sys.stderr)
    print("  -t|--translated     Report translated Unicode characters", file=sys.stderr)
    print(
        "  -u|--untranslated   Report untranslated Unicode characters", file=sys.stderr
    )
    print("  --debug             Enable debug mode", file=sys.stderr)
    print(
        "  --help|-?           Print usage and this help message and exit",
        file=sys.stderr,
    )
    print("  --version           Print version and exit", file=sys.stderr)
    print("  --                  Options processing terminator", file=sys.stderr)
    print(file=sys.stderr)


################################################################################
def process_environment_variables():
    """Process environment variables"""

    if "UNICODE2ASCII_DEBUG" in os.environ.keys():
        logging.disable(logging.NOTSET)

    logging.debug("process_environment_variables(): parameters:")
    logging.debug(parameters)


################################################################################
def process_command_line():
    """Process command line options"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    # option letters followed by : expect an argument
    # same for option strings followed by =
    character_options = "aftu?"
    string_options = [
        "analyze",
        "debug",
        "force",
        "help",
        "translated",
        "untranslated",
        "version",
    ]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        logging.critical("Syntax error: %s", error)
        display_help()
        sys.exit(1)

    for option, _ in options:

        if option in ("-a", "--analyze"):
            parameters["Filter"] = False
            parameters["Analyze"] = True

        if option in ("-f", "--force"):
            parameters["Force UTF-8"] = True

        elif option in ("-t", "--translated"):
            parameters["Filter"] = False
            parameters["Translated"] = True

        elif option in ("-u", "--untranslated"):
            parameters["Filter"] = False
            parameters["Untranslated"] = True

        elif option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("--help", "-?"):
            display_help()
            sys.exit(0)

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

    logging.debug("process_command_line(): parameters:")
    logging.debug(parameters)
    logging.debug("process_command_line(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def _print_in_table_format(character, ascii_equivalent=""):
    """Internal - print character in ready to use conversion table format"""

    logging.debug("character = '%s'", character)
    logging.debug('ascii_equivalent = "%s"', ascii_equivalent)

    if ascii_equivalent:
        try:
            print(
                "    '{}': \"{}\", # {}".format(
                    character, ascii_equivalent, unicodedata.name(character)
                )
            )
        except ValueError:
            print("    '{}': \"{}\", # UNKNOWN character in unicodedata.name()".format(character, ascii_equivalent))
        else:
            try:
                print("    '{}': \"\", # {}".format(character, unicodedata.name(character)))
            except ValueError:
                print("    '{}': \"\", # UNKNOWN character in unicodedata.name()".format(character))


################################################################################
def is_unicode_category(character, category):
    """Return True if character belongs to the specified Unicode category"""
    if ord(character) > 127:
        return unicodedata.category(character)[0] == category

    return False


################################################################################
def is_unicode_letter(character):
    """Return True if character is a Unicode letter"""
    return is_unicode_category(character, "L")


################################################################################
def is_unicode_mark(character):
    """Return True if character is a Unicode mark"""
    return is_unicode_category(character, "M")


################################################################################
def is_unicode_number(character):
    """Return True if character is a Unicode number"""
    return is_unicode_category(character, "N")


################################################################################
def is_unicode_punctuation(character):
    """Return True if character is a Unicode punctuation"""
    return is_unicode_category(character, "P")


################################################################################
def is_unicode_symbol(character):
    """Return True if character is a Unicode symbol"""
    return is_unicode_category(character, "S")


################################################################################
def is_unicode_separator(character):
    """Return True if character is a Unicode separator"""
    return is_unicode_category(character, "Z")


################################################################################
def is_unicode_other(character):
    """Return True if character is a Unicode other"""
    return is_unicode_category(character, "C")


################################################################################
def unicode_category(category):
    """Return Unicode category description"""
    try:
        return categories_to_text[category]
    except ValueError:
        return ""


################################################################################
def unicode_to_ascii_character(character, default=""):
    """Return Unicode letters to their ASCII equivalent and the rest unchanged"""
    if ord(character) < 128:
        return character

    if character in corrected_unicode_to_ascii:
        return corrected_unicode_to_ascii[character]

    ascii_equivalent = (
        unicodedata.normalize("NFKD", character)
        .encode("ASCII", "ignore")
        .decode("utf-8")
    )
    if ascii_equivalent:
        return ascii_equivalent

    if character in additional_unicode_to_ascii:
        return additional_unicode_to_ascii[character]

    return default


################################################################################
def unicode_to_ascii_string(characters, default=""):
    """Return Unicode letters to their ASCII equivalent and the rest unchanged"""
    new_string = ""
    for character in characters:
        new_string = new_string + unicode_to_ascii_character(character, default)
    return new_string


################################################################################
def analyze_unicode_character(character):
    """Return all information about a Unicode character"""
    if ord(character) > 127:
        print("Character: '{}'".format(character))
        try:
            print("Name: {}".format(unicodedata.name(character)))
        except ValueError:
            print("Name: UNKNOWN")
        try:
            print("Decimal value: {}".format(unicodedata.decimal(character)))
        except ValueError:
            pass
        try:
            print("Digit value: {}".format(unicodedata.digit(character)))
        except ValueError:
            pass
        try:
            print("Numeric value: {}".format(unicodedata.numeric(character)))
        except ValueError:
            pass
        category = unicodedata.category(character)
        print("Category: {} / {}".format(category, unicode_category(category)))
        print("Bidirectional class: {}".format(unicodedata.bidirectional(character)))
        print("Combining class: {}".format(unicodedata.combining(character)))
        print("East Asian width: {}".format(unicodedata.east_asian_width(character)))
        print("Mirrored property: {}".format(unicodedata.mirrored(character)))
        print('Decomposition: "{}"'.format(unicodedata.decomposition(character)))
        print('Normal NFC form: "{}"'.format(unicodedata.normalize("NFC", character)))
        print('Normal NFKC form: "{}"'.format(unicodedata.normalize("NFKC", character)))
        print('Normal NFD form: "{}"'.format(unicodedata.normalize("NFD", character)))
        print('Normal NFKD form: "{}"'.format(unicodedata.normalize("NFKD", character)))
        print(
            'ASCII NFC form: "{}"'.format(
                unicodedata.normalize("NFC", character)
                .encode("ASCII", "ignore")
                .decode("utf-8")
            )
        )
        print(
            'ASCII NFKC form: "{}"'.format(
                unicodedata.normalize("NFKC", character)
                .encode("ASCII", "ignore")
                .decode("utf-8")
            )
        )
        print(
            'ASCII NFD form: "{}"'.format(
                unicodedata.normalize("NFD", character)
                .encode("ASCII", "ignore")
                .decode("utf-8")
            )
        )
        print(
            'ASCII NFKD form: "{}"'.format(
                unicodedata.normalize("NFKD", character)
                .encode("ASCII", "ignore")
                .decode("utf-8")
            )
        )
        print(
            'unicode_to_ascii_character(): "{}"'.format(
                unicode_to_ascii_character(character)
            )
        )
        print()


################################################################################
def get_encoding():
    """Try to get the input encoding"""
    encoding = locale.getpreferredencoding()
    if not encoding:
        encoding = locale.getdefaultlocale()[1]
    if not encoding:
        # Assume default UTF-8 encoding:
        encoding = "UTF-8"

    return encoding


################################################################################
def convert_encoding(text, convert_from, convert_to="UTF-8"):
    """Try to convert the input encoding"""
    return text.encode('latin1').decode(convert_from).encode(convert_to)


################################################################################
def main():
    """The program's main entry point"""
    program_name = os.path.basename(sys.argv[0])

    initialize_debugging(program_name)
    process_environment_variables()
    process_command_line()

    if parameters["Force UTF-8"]:
        parameters["Encoding"] = "UTF-8"
    else:
        parameters["Encoding"] = get_encoding()

    for line in sys.stdin:
        for character in line:
            if parameters["Encoding"] != "UTF-8":
                character = convert_encoding(character, parameters["Encoding"])

            ascii_equivalent = unicode_to_ascii_character(character)

            if parameters["Filter"]:
                print(ascii_equivalent, end="")
            elif character != os.linesep:
                if parameters["Analyze"]:
                    analyze_unicode_character(character)

                if not ascii_equivalent:
                    if parameters["Untranslated"]:
                        _print_in_table_format(character)
                else:
                    if parameters["Translated"]:
                        _print_in_table_format(character, ascii_equivalent)

    sys.exit(0)


if __name__ == "__main__":
    main()
