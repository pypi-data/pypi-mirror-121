Bidi_control_characters = {"RI" : "\u2066",
                           "RLI" : "\u2067",
                           "FSI" : "\u2068",
                           "LRE" : "\u202a",
                           "RLE" : "\u202b",
                           "LRO" : "\u202d",
                           "RLO" : "\u202e",
                           "PDF" : "\u202c",
                           "PDI" : "\u2069"}

bidi_chars_info = {
                  "RI" : "RI	LEFT-TO-RIGHT ISOLATE	U+2066	dir = \"ltr\"	sets base direction to LTR and isolates the embedded content from the surrounding text",
                  "RLI" : "RLI	RIGHT-TO-LEFT ISOLATE	U+2067	dir = \"rtl\"	ditto, but for RTL",
                  "FSI" : "FSI	FIRST-STRONG ISOLATE	U+2068	dir = \"auto\"	isolates the content and sets the direction according to the first strongly typed directional character",
                  "LRE" : "LRE	LEFT-TO-RIGHT EMBEDDING	U+202A	dir = \"ltr\"	sets base direction to LTR but allows embedded text to interact with surrounding content, so risk of spillover effects",
                  "RLE" : "RLE	RIGHT-TO-LEFT EMBEDDING	U+202B	dir = \"rtl\"	ditto, but for RTL",
                  "LRO" : "LRO	LEFT-TO-RIGHT OVERRIDE	U+202D	<bdo dir = \"ltr\">	overrides the bidirectional algorithm to display characters in memory order, progressing from left to right",
                  "RLO" : "RLO	RIGHT-TO-LEFT OVERRIDE	U+202E	<bdo dir = \"rtl\">	as previous, but display progresses from right to left",
                  "PDF" : "POP DIRECTIONAL FORMATTING",
                  "PDI" : "POP DIRECTIONAL ISOLATE",
                  "source" : 'https://www.w3.org/International/questions/qa-bidi-unicode-controls#basedirection'}

BCC =  Bidi_control_characters.copy()              

class Bidi():

    def __init__(self, body):
        self.body = body
        self.paras = self.body.split('\n')
        return None

    def LeftToRightIsolate(self):
        return self.ParasHandler('LRI', 'PDI')

    def RightToLeftIsolate(self):
        return self.ParasHandler('RLI', 'PDI')
    
    def FirstStrongIsolate(self):
        return self.ParasHandler('FSI', 'PDI')
    
    def LeftToRightEmbedding(self):
        return self.ParasHandler('LRE', 'PDF')

    def RightToLeftEmbedding(self):
        return self.ParasHandler('RLE', 'PDF')

    def LeftToRightOverride(self):
        return self.ParasHandler('LRO', 'PDF')

    def RightToLeftOverride(self):
        return self.ParasHandler('RLO', 'PDF')

    def ParasHandler(self, controlCharacter, ClosingCharacter):
        return '\n'.join([f'{BCC[controlCharacter]}{self.chop}{BCC["PDI"]}' for self.chop in self.paras])
    
