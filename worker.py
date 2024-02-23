# helper functions for textgrid_parser.py
import re


GA_CODE, G_CODE, ONSET, CODA = 44032, 12593, 588, 28
# The unicode representation of the Korean syllabic orthography starts with GA_CODE
# The unicode representation of the Korean phonetic (jamo) orthography starts with G_CODE

# ONSET LIST. 00 -- 18
ONSET_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# VOWEL LIST. 00 -- 20
VOWEL_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                 'ㅣ']

# CODA LIST. 00 -- 27 + 1 (1 for open syllable)
CODA_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

ipa_table = {
    # from slide 19 of Seoul Corpus documentation
    'p0': 'p', 'ph': 'pʰ', 'pp': 'p*',
    't0': 't', 'th': 'tʰ', 'tt': 't*',
    'k0': 'k', 'kh': 'kʰ', 'kk': 'k*',
    'c0': 'tɕ', 'ch': 'tɕʰ', 'cc': 'tɕ*',
    's0': 's', 'ss': 's*',
    'hh': 'h',
    'mm': 'm', 'nn': 'n', 'ng': 'ŋ', 'll': 'l',

    'ii': 'i', 'xx': 'ɯ', 'uu': 'u',
    'ee': 'ɛ', 'vv': 'ʌ', 'oo': 'o',
    'aa': 'ɑ',
    'ye': 'jɛ', 'ya': 'ja', 'yv': 'jʌ', 'yu': 'ju', 'yo': 'jo',
    'wi': 'wi', 'we': 'wɛ', 'wa': 'wa', 'wv': 'wʌ', 'xi': 'ɰi',
}

def to_jamo(word, empty_onset=False):
    split_word = list(word)
    onset_list = ONSET_LIST[:]

    if not empty_onset:
        onset_list[11]=''

    result = list()
    for letter in split_word:
        # If not Korean character, return.
        if re.match('[가-힣]', letter) is not None:
            char_code = ord(letter) - GA_CODE
            if char_code < 0:
                result.append(letter)
            onset = int(char_code / ONSET)
            result.append(onset_list[onset])

            vowel = int((char_code - (ONSET * onset)) / CODA)
            result.append(VOWEL_LIST[vowel])

            coda = int((char_code - (ONSET * onset) - (CODA * vowel)))
            result.append(CODA_LIST[coda])
        else:
            result.append(letter)
    jamo = "".join(result)
    return jamo


def to_ipa(seoul_phoneme):
    return ipa_table.get(seoul_phoneme, '')


if __name__ == '__main__':
    print(to_jamo("학 교뜰"))
