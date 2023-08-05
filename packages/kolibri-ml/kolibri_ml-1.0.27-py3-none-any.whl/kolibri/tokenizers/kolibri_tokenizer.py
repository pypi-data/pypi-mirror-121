#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'mohamedbenhaddou'

import regex as re
from kolibri.tokenizers.tokenizer import Tokenizer
from kolibri.stopwords import get_stop_words
from kdmt.dict import update
import numpy as np
from kolibri.data.ressources import resources
from pathlib import Path
from kdmt.file import read_json_file
from kolibri.tools import regexes as common_regs
patterns_file=resources.get(str(Path('modules', 'tokenizers', 'default_regexes.json'))).path
regexes=read_json_file(patterns_file)





class KolibriTokenizer(Tokenizer):
    provides = ["tokens"]

    defaults = {
        "fixed": {
        },

        "tunable": {
            "abstract-entities": {
                "value": True,
                "type": "categorical",
                "values": [True, False]
            },
            "group-entities": {
                "value": False,
                "type": "categorical",
                "values": [True, False]
            }

        }
    }

    def __init__(self, hyperparameters=None):
        super().__init__(hyperparameters)

        for (name, regex_variable) in regexes.items():
            if isinstance(regex_variable, str):
                # The regex variable is a string, compile it and put it in the
                # global scope
                setattr(self, name, regex_variable)


        self.stopwords = None
        if "language" in self.hyperparameters:
            self.language = self.hyperparameters["fixed"]["language"]
            self.stopwords = get_stop_words(self.language)


        lang=self.language.upper()

        #self.master_pat = re.compile(r'|'.join(
        pattern =[self.CANDIDATE, self.OTHER, self.EXCEPTIONS, self.ACORNYM, self.NUM, r'(?<__URL__>'+common_regs.URL.pattern[1:-1]+')',  r'(?<__MONEY__>'+common_regs.MONEY.pattern[1:-1]+')']
        if lang in common_regs.DATE:
            pattern.append(r'(?<__DATE__>'+common_regs.DATE[lang].pattern+')')

        pattern.append(r'(?<__TIME__>'+common_regs.TIME.pattern+')')
        if lang in common_regs.MONTH:
            pattern.append(r'(?<__URL__>'+common_regs.MONTH[lang].pattern+')')
        pattern.append(r'(?<__MONTH__>'+common_regs.CODE.pattern+')')
        if lang in common_regs.DURATION:
            pattern.append(r'(?<__DURATION__>'+common_regs.DURATION[lang].pattern+')')

        pattern.extend([self.OPENPARENTHESIS, self.CLOSEPARENTHESIS, self.WS, self.MULTIPLEWORD, self.PLUS, self.MINUS, self.ELLIPSIS, self.DOT, self.TIMES, self.EQ,
                 self.QUESTION,
                 self.EXLAMATION, self.COLON, self.COMA, self.SEMICOLON, self.OPENQOTE, self.ENDQOTE, self.DOUBLEQOTE, self.SINGLEQOTE, self.PIPE,  self.WORD])

        self.master_pat = re.compile(r'|'.join(pattern), re.UNICODE)

    def tokenize(self, text):
        text = str(text).replace(r'\u2019', '\'')
        scanner = self.master_pat.scanner(text)

        tokens= [(m.group().strip(), m.lastgroup) for m in iter(scanner.match, None) if m.group().strip()!=""]
        if self.get_parameter("abstract-entities"):
            tokens=[t[1] if t[1] in ['WA', 'EMAIL', 'MONEY', 'DATE', 'MONTH', 'DURATION', 'NUM_TS', 'NUM', 'FILE'] else t[0] for t in tokens]
        else:
            tokens=[(t[0], t[1])  for t in tokens]
        return tokens

    def transform(self, X):
        if not isinstance(X, list) and not isinstance(X, np.ndarray):
            X=[X]
        return [self.tokenize(x) for x in X]


    def update_default_hyper_parameters(self):
        self.defaults=update(self.defaults, KolibriTokenizer.defaults)
        super().update_default_hyper_parameters()



from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(KolibriTokenizer.name, KolibriTokenizer)



if __name__=='__main__':
    tokenizer = KolibriTokenizer()
    text = """This automated mail is triggered for $ 123 to inform you a rescind has been executed in Change Job with an effective date of 2019 10 01"""
    tokens = tokenizer.transform(text)

    print(tokens)