import sys

import requests
from bs4 import BeautifulSoup

def get_translation(word, src_lang, dst_lang):

      direction = src_lang.lower() + "-" + dst_lang.lower()
      url = f"https://context.reverso.net/translation/{direction}/{word}"
      user_agent = 'Mozilla/5.0'
      respond = requests.get(url, headers={'User-Agent': user_agent})
      word_list = []
      example_list = []
      text = ""
      if respond.status_code == 200:
            soup = BeautifulSoup(respond.content, "html.parser")
            count = 0
            for link in soup.find_all("a", class_="translation"):
                  if count > 0:
                        word_list.append(link.text.strip())
                  count += 1
            count = 0
            for div in soup.find_all("div", class_="ltr"):
                  if count > 0:
                        example_list.append(div.text.strip())
                  count += 1
      else:
            if respond.status_code == 404:
                  print(f"Sorry, unable to find {word}")
                  return None
            else:
                  print("Something wrong with your internet connection")
                  return None
      text += dst_lang + " Translations\n"

      for word in word_list:
            text += word + "\n"

      text += "\n" +  dst_lang + " Examples\n"
      for word in example_list:
            text += word + "\n"

      return text

if len(sys.argv) != 4:
      exit(0)

dict_lang = {1: "arabic", 2: "german", 3: "english", 4: "spanish",
             5: "french", 6: "hebrew", 7: "japanese", 8: "dutch",
             9: "polish", 10: "portuguese", 11: "romanian",
             12: "russian", 13: "turkish"}

src_language = sys.argv[1]
if src_language not in dict_lang.values():
      print(f"Sorry, the program doesn't support {src_language}")

dst_language = sys.argv[2]
if dst_language not in dict_lang.values() and dst_language != "all":
      print(f"Sorry, the program doesn't support {dst_language}")

word = sys.argv[3]

with open(f"{word}.txt", "w", encoding="utf-8") as fout:
      if dst_language != "all":
            text = get_translation(word, src_language, dst_language)

      else:
            text = ""
            for i in range(1, len(dict_lang.keys()) + 1):
                  dst_language = dict_lang[i]
                  if dst_language != src_language:
                        buf = get_translation(word, src_language, dst_language)
                        if buf is None:
                              text = None
                              exit(0)
                        else:
                              text += buf + "\n\n"
      if text is None:
            exit(0)
      print(text.rstrip())
      print(text.rstrip(), file=fout)