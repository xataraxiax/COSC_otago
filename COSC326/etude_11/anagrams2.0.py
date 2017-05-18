'''
    Etude 11: Anagrams
    File name: anagrams.py
    Authors: Stefan Pedersen 1427681, Jono Sue 4097307
    Date created: 24/01/2017
    Date last modified: 27/01/2017
    Python Version: 2.7
'''
import sys, string, time, hashlib

# start = time.time()

MIN_WORD_SIZE = 1 # min size of a word in the output

# Records the valid characters of the target string and places them in a
# dicitonary. The input dictionary is loaded and words that cannot be in
# an anagram are removed:
# i.e. Words that contain a letter not in the target are removed
#      Words that contain more than the number of a letter in target
# Returns a list of valid anagrams from makeAnagrams().
def inputPrep(target):
    targetDictionary = {} # letter dict for target word
    dictionary = {} # words from input dictionary
    dictList = [] # only dictionary words with letters making up target word

    # Clean up input string
    target = target.replace(' ', '')
    clean = target.translate(None, string.punctuation).lower()

    for i in range(len(clean)):
        if clean[i] in targetDictionary:
            targetDictionary[clean[i]] += 1
        else:
            if clean[i] == " ":
                continue
            targetDictionary[clean[i]] = 1
    for line in sys.stdin:
        dictionary[line.rstrip("\n")] = '_'
    for word in dictionary.keys():
        for letter in word:
            if letter not in targetDictionary:
                # so delete the item from dictionary
                dictionary.pop(word, None)
                break
    dictList = dictionary.keys()
    dictList.sort()
    return makeAnagrams(dictList, clean)

# Creates and returns a tree representation of the dictionary
# of words passed in.
def load_dictionary(dictList):
    result = Node()
    for i in range(len(dictList)):
        word = dictList[i]
        result.add(word)
    return result

# Finds a list of valid anagrams(not valid english words) by traversing the
# dictionary tree. Anagrams with the same combination of letters are excluded
# by sorting each anagram alphabetically and storing it as a hash signature
# in wordCache. Only unique combinations are appended to the anagram list.
def makeAnagrams(dictList, clean):
    wordCache = {} # stors hash signature of found anagrams to avoid duplicate
    anagrams = [] # unique anagrams
    words = load_dictionary(dictList)
    for word in words.anagram(clean):
        word = word.split()
        word.sort()
        hash_object = hashlib.sha1(' '.join(word))
        hexadecimalDigest = hash_object.hexdigest()

        if hexadecimalDigest in wordCache and wordCache[hexadecimalDigest] == word:
            continue
        else:
            wordCache[hexadecimalDigest] = word
            anagrams.append(word)

    return anagrams

# Formats an anagram list according to the constraints provided in the
# etude. 
def output(anagrams):
    working = []
    sameFirstWord = []

    # sorts the words in each anagram by descending length
    for i in range(len(anagrams)):
        for j in anagrams[i]:
            anagrams[i].sort(key=len, reverse=True)
    # sorts anagram list alphabetically by first word
    anagrams.sort()
    # sorts anagram list by increasing number of words in each anagram
    anagrams.sort(key=len)
    # For anagrams of a certain number of words, radix sort is used to
    # put precedence on word length over alphabetical order
    for a in range(len(anagrams)):
        sameFirstWord.append(anagrams[a])
        if a == len(anagrams)-1:
            for x in range(len(anagrams[a])-1, -1, -1):
                sameFirstWord.sort(key=lambda z: len(z[x]), reverse=True)
            working.extend(sameFirstWord)
            sameFirstWord = []
        if a != len(anagrams)-1 and len(anagrams[a]) < len(anagrams[a+1]):
            for x in range(len(anagrams[a])-1, -1, -1):
                sameFirstWord.sort(key=lambda z: len(z[x]), reverse=True)
            working.extend(sameFirstWord)
            sameFirstWord = []
    anagrams = working
    # prints list of anagrams
    for sorted in anagrams:
        for word in sorted:
            print word,
        print

        
class Node(object):
    def __init__(self, letter='', final=False, depth=0):
        self.letter = letter
        self.final = final
        self.depth = depth
        self.children = {}
    def add(self, letters):
        node = self
        for index, letter in enumerate(letters):
            if letter not in node.children:
                node.children[letter] = Node(letter, index==len(letters)-1, index+1)
            node = node.children[letter]
    def anagram(self, letters):
        tiles = {}
        for letter in letters:
            tiles[letter] = tiles.get(letter, 0) + 1
        min_length = len(letters)
        return self._anagram(tiles, [], self, min_length)
    def _anagram(self, tiles, path, root, min_length):
        max_words = int(sys.argv[2])
        if self.final and self.depth >= MIN_WORD_SIZE:
            word = ''.join(path)
            length = len(word.replace(' ', ''))
            if int(len(word.split())) <= max_words:
                if length >= min_length:
                    yield word
                path.append(' ')
                for word in root._anagram(tiles, path, root, min_length):
                    yield word
                path.pop()
        for letter, node in self.children.iteritems():
            count = tiles.get(letter, 0)
            if count == 0:
                continue
            tiles[letter] = count - 1
            path.append(letter)
            for word in node._anagram(tiles, path, root, min_length):
                yield word
            path.pop()
            tiles[letter] = count

def main():
    target = sys.argv[1]
    anagrams = inputPrep(target)
    output(anagrams)

if __name__ == '__main__':
    main()

# end = time.time()
# print end-start
