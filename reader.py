import hashlib
import os

def hashCracker(hash_value):
    """"
    hashCracker Function will try to the cleartext form of the given hash.
    it will try to check a single hash with multiple hashing algorithms supported by hashlib.
    if the algorithm is given it will crack for that single hash algorithm.
    if no algorithm is given then it will fin the has of every value.
    :parameter hash_value :type str
    """
    found = 0

    wordlist_path = str(input('[*]: Enter Absolute Path Of the Wordlist: '))   # must handle the wordlist dir

    if not os.path.basename(wordlist_path) in os.listdir(os.getcwd()):
        os.chdir(os.path.dirname(wordlist_path))

    if not os.path.exists(wordlist_path):
        return 'Directory Specifed Does Not Exist.'

    encodings = ['utf-8', 'utf-16', 'utf-32', 'utf-32le', 'utf-16le']

    with open(os.path.basename(wordlist_path), 'r') as words:

        for line in words.readlines():

            word = line.strip()

            for algos in hashlib.algorithms_available:

                for encodes in encodings:

                    try:
                        output = hashlib.new(algos, word.encode(encodes)).hexdigest()
                        print(output, encodes, algos, word)
                    except TypeError:
                        continue

                    if output == hash_value:
                        found = 1
                        break

                if found:
                    break

            if found:
                break

    if found:
        return '[+]: {0} = {1} = {2}'.format(hash_value, word, algos)
    return '[-]: Not Found In Wordlist Specified.'

print(hashCracker('f95f37eb7e16e77affc1cb2d28b1a67d'))





