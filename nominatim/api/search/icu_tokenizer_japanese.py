import MeCab
import re

def convert_kanji_sequence_to_number(sequence):
  kanji_map = {
    '零': '0',
    '一': '1',
    '二': '2',
    '三': '3',
    '四': '4',  
    '五': '5',
    '六': '6',
    '七': '7',
    '八': '8',
    '九': '9'
  }
  converted = ''
  current_number = ''
  for char in sequence:
    if char in kanji_map:
      current_number += kanji_map[char]
    else:
      converted += current_number
      current_number = ''
      converted += char
  converted += current_number
  return converted

'''
def convert_zenkaku_sequence_to_number(sequence):
  zenkaku_map = {
    '１': '1',
    '２': '2',
    '３': '3',
    '４': '4',  
    '５': '5',
    '６': '6',
    '７': '7',
    '８': '8',
    '９': '9'
  }
  converted = ''
  current_number = ''
  for char in sequence:
    if char in zenkaku_map:
      current_number += zenkaku_map[char]
    else:
      converted += current_number
      current_number = ''
      converted += char
  converted += current_number
  return converted
'''

def transliterate(text: str) -> str:
    # split all words first using the normalization library
    text = convert_kanji_sequence_to_number(text)    
    pattern = r'''
           (...??[都道府県])            # [group1] prefecture
           (.+?[市区町村])              # [group2] municipalities (city/wards/towns/villages)
           (.+)                        # [group3] other words
           '''
    result = re.match(pattern, text, re.VERBOSE) # perform normalization using the pattern
    joined_group = ''.join([result.group(1),', ',result.group(2),', ',result.group(3)])
    #print(joined_group)
    return joined_group
    
# this is for debug
#tmp = '東京都千代田区丸の内１－２'
#print(transliterate(tmp))

