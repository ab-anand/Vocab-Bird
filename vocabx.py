from vocabulary.vocabulary import Vocabulary as vb
import json


def details(word):
    meaning = vb.meaning(word)
    antonym = vb.antonym(word)
    synonym = vb.synonym(word)
    usage = vb.usage_example(word)
    
    if meaning == False:
        meaning = 'Not Found'
    else:
        meaning = json.loads(meaning)
        meaning = str(meaning[0]['text'])
    if antonym == False:
        antonym = 'Not Found'
    else:
        antonym = json.loads(antonym)
        antonym = str(antonym[0]['text'])

    if synonym == False:
        synonym = 'Not Found'
    else:
        synonym = json.loads(synonym)
        synonym = str(synonym[0]['text'])

    if usage == False:
        usage = 'Not Found'
    else:
        usage = json.loads(usage)
        usage = str(usage[-1]['text'])

    values = {'meaning': meaning,
              'antonym': antonym,
              'synonym': synonym,
              'usage': usage
              }

    return values


value = details('ride')
print value
