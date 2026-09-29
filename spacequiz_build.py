#!/usr/bin/env python3
import json
import io

#Localization
UI_LANGUAGES=['en','it','de','fr','es']
UI_TEXT={}
LOCALIZED_QUESTION_BANKS={}
for lang in UI_LANGUAGES:
    with io.open(f"lang/ui_{lang}.json",mode="r",encoding="utf-8") as f:
        UI_TEXT[lang]=json.load(f)
    with io.open(f"lang/questions_{lang}.json",mode="r",encoding="utf-8") as f:
        LOCALIZED_QUESTION_BANKS[lang]=json.load(f)

with io.open("src/spacequiz_src.py",mode="r",encoding="utf-8") as fr:
    with io.open("spacequiz.py",mode="w",encoding="utf-8") as fw:
        fw.write(fr.read().replace('@@@@UI_TEXT@@@@',json.dumps(UI_TEXT)).replace('@@@@LOCALIZED_QUESTION_BANKS@@@@',json.dumps(LOCALIZED_QUESTION_BANKS)))

