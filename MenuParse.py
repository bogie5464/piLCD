from collections import namedtuple
import re

Token = namedtuple("Token", ["tag", "text"])


class LCD_Menu():
    TOKENS = None

    def __init__(self,  LCDObj, message=''):
        self.TOKENS = self.tokenize(message)
        self.LCDObj = LCDObj

    def tokenize(self, text):
        tagRex = re.compile(r"({.+?})")
        tokens = []
        pos = 0
        while pos < len(text):
            m = tagRex.search(text, pos)
            if m is None:
                # No more directives found.
                tokens.append(Token("text", text[pos:]))
                break
            else:
                # There might be text between here and the next directive.
                if m.start() > pos:
                    tokens.append(Token("text", text[pos:m.start()]))
                tokens.append(Token("expression", m.group(0)))
                pos = m.end()
        return tokens

    def parse(self):
        for i in self.TOKENS:
            if i.tag == 'text':
                self.LCDObj.send_message(i.text)
            if i.tag == 'expression':
                methodcall = self.buildCall(i.text)
                self.LCDinterface(methodcall)
        pass

    def buildCall(self, text):
        text = str(text)
        text = text.replace('{', '')
        text = text.replace('}', '')
        methodcall = text.split(':')
        return methodcall

    def LCDinterface(self, methodcall):
        args = None
        if ',' in methodcall[1]:
            args = tuple(map(str, methodcall[1].split(',')))
        else:
            args = methodcall[1]

        getattr(self.LCDObj, methodcall[0])(*args)
        pass
