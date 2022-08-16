# start date of the project 23/April/2021
# Purpose Of This Project: To Know More About Hash Algorithms
# This Project Will
# case "$input" in
# 1) Create Hashes; Given Text Or Numbers;;
# 2) Create Hashes; Given Binary Data; Images; Files; Videos;;
# 3) Crack Hashes; Faster; With The Use Of Threading ;;
# 4) Check For Integrity;;
# 5) And More On Its Way;;
# esac

import hashlib
import os


def CreateDataHash(password, algorithm):

    """"
    :parameter password :type str :raises nothing:
    :parameter algorithm :type str :raises ValueError: If Specified Algorithm Is Not Supported

    this function will produce a hash value given a text
    it will also produce hash value for an empty value ''
    letting the user choose a vali encoding
    """

    password = password.encode('utf-8')

    try:
        return hashlib.new(algorithm, password).hexdigest()
    except ValueError:
        return '[-]: Unsupported Hash Type.'

def CreateFileHash(algorithm):

    """"
    :argument algorithm     :raises ValueError = If Algorithm Specified Is Not Supported :type  Algorithm Must Be
    [md4, md5, sha1, sha256, sha512, sha384 ...]
    :returns the hashed value of the given file
    """
    path = str(input('[*]: Enter File Absolute Path: '))

    if os.path.exists(path):

        os.chdir(os.path.dirname(path))
        basename = os.path.basename(path)

        try:
            handler = open(basename, 'rb')
        except FileNotFoundError:
            return '[-]: Could Not Find Specified File'

        try:
            return hashlib.new(algorithm, handler.read()).hexdigest()
        except ValueError:
            return '[-]: Unsupported Hash Type.'

    else:
        return '[-]: Path Specified Does Not Exist.'

def IntegrityCheck(hash_value, algorithm):

    """"
    :parameter hash_value :type str :raises nothing
    :parameter algorithm :type str :raises ValueError. If Algorithm Is Not Supported
    :returns str. If File Is Save Or If File Is UnSafe.
    """
    path = str(input('[*]: Enter File Absolute Path: '))

    if os.path.exists(path):

        os.chdir(os.path.dirname(path))
        basename = os.path.basename(path)

        try:
            handler = open(basename, 'rb')
        except FileNotFoundError:
            return '[-]: Could Not Find Specified File'

        try:
            file_hash_value = hashlib.new(algorithm, handler.read()).hexdigest()
        except ValueError:
            return '[-]: Unsupported Hash Algorithm -> {0}'.format(algorithm)

        if file_hash_value == hash_value:
            return '[+]: File Is Safe'

        return '[-]: File Not Save'

    else:
        return '[-]: Specified Path Does Not Exist -> {0}'.format(path)

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

print(hashCracker('f95f37eb7e16e77affc1cb2d28b1a67c'))





