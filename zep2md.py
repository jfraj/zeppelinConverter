import sys
import json


def printNested(element):
    """Prints the nested objects"""
    if not hasattr(element, '__iter__'):
        print("Not iterable")
        return
    for ikey in element:
        print(ikey)

def genericCode2MD(codeText):
    """ Turns any code to mark down
    """
    return "\n``` \n"+codeText+"\n```\n"

def paragraph2MD(paragraph, keepOnlyText):
    """ Translate paragraph into markdown
    """
    magic = None
    if paragraph['text'][0] == '%':
        magic = paragraph['text'].split()[0]
        if magic == '%md':
            return paragraph['text'][len(magic):]
        ## These magic can be returned without results
        if magic in keepOnlyText:
            return genericCode2MD(paragraph['text'][len(magic):])
        ##TODO implement other magic translation
        print("\n\n NOT implemented magic {}\n".format(magic))
    ## Making it to this point means the cell is scala (no magic changing the language)
    ## For now, let's keep it as generic code
    return genericCode2MD(paragraph['text']) + genericCode2MD(paragraph['result']['msg'])


def convert2Markdown(zeppelinJsonPath, outMdPath):
    keepOnlyText = ('%dep',)
    jsonData = open(zeppelinJsonPath).read()
    data = json.loads(jsonData)
    fZep2MD = open(outMdPath, 'w')

    #Print paragraph
    for ipar in data["paragraphs"]:
        fZep2MD.write(paragraph2MD(ipar, keepOnlyText).encode("utf-8"))

if __name__ == "__main__":
    try:
        convert2Markdown(sys.argv[1], sys.argv[2])
    except IndexError:
        print("\n\nUsage: python <zeppelin export> <Mardown output>\n")
