from bs4 import BeautifulSoup
import requests
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('native')
arg_parser.add_argument('foreign')
arg_parser.add_argument('word')

args = arg_parser.parse_args()
native = args.native
foreign = args.foreign
word = args.word

HEADERS = {'User-Agent': 'Mozilla/5.0'}

lang = ['Arabic', "German", 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese',
        'Romanian', 'Russian', 'Turkish']


def parser(word, native, foreign):
    url = 'https://context.reverso.net/translation/{fst}-{sec}/{thd}'.format(fst=native.lower(),
                                                                             sec=foreign.lower(),
                                                                             thd=word)
    r = requests.get(url, headers=HEADERS)
    if not check(1, r.status_code):
        return
    soup = BeautifulSoup(r.content, 'html.parser')

    translations = soup.find(id="translations-content")
    word_l = []
    try:
        for t in translations.find_all(['a', 'div']):
            word_l.append(t.text.strip())
        word_l = list(filter(lambda x: x != '', word_l))
    except AttributeError:
        print("Sorry, unable to find {}".format(word))
        return

    example = soup.find(id="examples-content")
    sentences = []
    for s in example.find_all('span', {'class': 'text'}):
        sentences.append(s.text.strip())
    return word_l, sentences


def how(word, sentences):
    x = 5 if len(word) > 5 else len(word)
    y = 10 if len(sentences) > 10 else len(sentences)
    return x, y


def check(x, *status_code):
    lang = ['Arabic', "German", 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese',
            'Romanian', 'Russian', 'Turkish', 'All']
    if x == 0:
        if native.capitalize() not in lang or foreign.capitalize() not in lang:
            print("Sorry, the program doesn't support {}".format(native)) and native.capitalize() not in lang
            print("Sorry, the program doesn't support {}".format(foreign)) and foreign.capitalize() not in lang
            return 0
        else:
            return 1
    if x == 1:
        if status_code == 200:
            return 0
        else:
            return 1


def main():
    if not check(0):
        return
    if foreign == 'all':
        all_lang_translator(word, native)
        return
    translator(word, native, foreign)
    return


def translator(word, native, foreign):
    file = open('{}.txt'.format(word), 'w', encoding='utf-8')
    word, sentences = parser(word, native, foreign)

    res = '{} Translations:\n'.format(foreign.capitalize())
    w_x, s_y = how(word, sentences)
    for x in range(w_x):
        res += word[x] + '\n'
    res += ('\n{} Examples:\n'.format(foreign.capitalize()))
    file.write(res)
    for x in range(0, s_y, 2):
        sentences[x] += '\n'
    for x in range(1, s_y, 2):
        if x == 9:
            break
        sentences[x] += '\n\n'
    for x in range(10):
        res += sentences[x][:len(sentences[x])]
        file.write(sentences[x])
    print(res)
    file.close()


def all_lang_translator(word, native_l):
    file = open('{}.txt'.format(word), 'w', encoding='utf-8')
    res_ = ''
    for x in range(13):
        if lang[x] != native_l.capitalize():
            try:
                word_, sentence = parser(word, native_l, lang[x])
            except TypeError:
                return
            res = "{lan} Translation:\n{word}\n\n{lan1} Example:\n{e1}\n{e2}\n\n\n".format(
                lan=lang[x], word=word_[0], lan1=lang[x], e1=sentence[0], e2=sentence[1])
            if x == 12:
                res = res[:len(res) - 3]
            res_ += res[:len(res)]
            file.write(res)
    print(res_)
    file.close()


if __name__ == '__main__':
    main()
