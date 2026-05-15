from FoSpy._debug import Debug
_debug = Debug()
_debug.on = True

from FoSpy import parsing
parsing._debug.on = True

from FoSpy.parsing import dict_from_file, write_dict_to_file
from FoSpy.parsing import syntax as snt

from pprint import pprint

READ_PATH = "tests/test_fos/read_test.fos"
WRITE_PATH = "tests/test_fos/write_test.fos"

def readTest(report=False):
    print('##### READ TEST #####')
    file_dict = dict_from_file(READ_PATH)
    print(f'Dictionary read from file: {READ_PATH}')
    if report:
        print_dict = file_dict.copy()

        comments = print_dict.pop(snt.meta_keys["comments"])

        for blockname, blocks in print_dict.items():
            print(f'NEW BLOCK: {blockname}')
            print('Block comments:')
            try:
                for comment in comments.get(blockname):
                    print(comment)
            except TypeError:
                pass
            print('-----')


            for idx, block in enumerate(blocks):
                print(f'(subblock {idx})')
                pprint(block,sort_dicts=False)

    return file_dict

def writeTest(file_dict):
    print('##### WRITE TEST #####')

    new_fp = WRITE_PATH
    write_dict_to_file(file_dict,new_fp)
    print(f'Wrote read test result to new file: {new_fp}')

    return file_dict, new_fp

def retTest(old_dict, new_fp):

    def deep_diff(d1, d2, path=""):
        diffs = []

        # keys only in d1
        for k in d1.keys() - d2.keys():
            diffs.append(f"{path}/{k}: missing in d2")

        # keys only in d2
        for k in d2.keys() - d1.keys():
            diffs.append(f"{path}/{k}: missing in d1")

        # keys in both
        for k in d1.keys() & d2.keys():
            v1, v2 = d1[k], d2[k]
            new_path = f"{path}/{k}"

            if isinstance(v1, dict) and isinstance(v2, dict):
                diffs.extend(deep_diff(v1, v2, new_path))
            elif v1 != v2:
                diffs.append(f"{new_path}: {v1} != {v2}")

        return diffs



    print('##### RETENTION TEST #####')

    print(f"Generating a new dictionary from: {new_fp}")
    new_dict = dict_from_file(new_fp)

    print(f'Testing to see if original dictionary from read test matches new dictionary')
    passed = old_dict == new_dict
    print(f'>>> User-level Retention Test: {"passed" if passed else "failed"}')
    if not passed:
        pprint(deep_diff(old_dict, new_dict))

    print("Taking the new dictionary on a round trip to file and back")
    old_dict = new_dict
    write_dict_to_file(old_dict, new_fp)
    new_dict = dict_from_file(new_fp)

    print("Testing to see if dictionary was preserved on round trip:")
    passed = old_dict == new_dict
    print(f'>>> Script-level Retention Test: {"passed" if passed else "failed"}')
    if not passed:
        pprint(deep_diff(old_dict, new_dict))

def test1():
    readResult = readTest(False)
    writeResult = writeTest(readResult)
    retResult = retTest(*writeResult)

    #return retResult

def syntaxSwap():
    readResult = readTest()
    snt.key_delimiter = "="
    snt.indent = ""
    writeResult = writeTest(readResult)

test1()

pass


