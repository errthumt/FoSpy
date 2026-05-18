from FoSpy._debug import Debug
_debug = Debug()
_debug.on = True

from FoSpy._debug import all_debugs_on
all_debugs_on()

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


from FoSpy.parsing.syntax import SYNTAX


def deep_diff(d1, d2, path=""):
    """
    Recursively diff two nested dict/list structures.
    Ignores calculated comments (strings starting with SYNTAX["calc_comment"]["prefix"]).
    """

    calc_prefix = SYNTAX["calc_comment"]["prefix"]
    diffs = []

    # Helper: detect calculated comment strings
    def is_calc_comment(x):
        return isinstance(x, str) and x.strip().startswith(calc_prefix)

    # Case 1 — both dicts
    if isinstance(d1, dict) and isinstance(d2, dict):
        # keys only in d1
        for k in d1.keys() - d2.keys():
            diffs.append(f"{path}/{k}: missing in d2")

        # keys only in d2
        for k in d2.keys() - d1.keys():
            diffs.append(f"{path}/{k}: missing in d1")

        # keys in both
        for k in d1.keys() & d2.keys():
            diffs.extend(deep_diff(d1[k], d2[k], f"{path}/{k}"))

        return diffs

    # Case 2 — both lists
    if isinstance(d1, list) and isinstance(d2, list):
        # Filter out calculated comments
        f1 = [x for x in d1 if not is_calc_comment(x)]
        f2 = [x for x in d2 if not is_calc_comment(x)]

        # length mismatch
        if len(f1) != len(f2):
            diffs.append(f"{path}: list length {len(f1)} != {len(f2)}")
            min_len = min(len(f1), len(f2))
        else:
            min_len = len(f1)

        # compare element‑wise
        for i in range(min_len):
            diffs.extend(deep_diff(f1[i], f2[i], f"{path}[{i}]"))

        return diffs

    # Case 3 — scalar mismatch
    if d1 != d2:
        # Ignore calculated comments entirely
        if is_calc_comment(d1) or is_calc_comment(d2):
            return diffs

        diffs.append(f"{path}: {d1!r} != {d2!r}")

    return diffs



def retTest(old_dict, new_fp):
    print('##### RETENTION TEST #####')

    print(f"Generating a new dictionary from: {new_fp}")
    new_dict = dict_from_file(new_fp)

    print(f'Testing to see if original dictionary from read test matches new dictionary')
    diffs = deep_diff(old_dict,new_dict)
    passed = diffs == []
    print(f'>>> User-level Retention Test: {"passed" if passed else "failed"}')
    if not passed:
        pprint(diffs)

    print("Taking the new dictionary on a round trip to file and back")
    old_dict = new_dict
    write_dict_to_file(old_dict, new_fp)
    new_dict = dict_from_file(new_fp)

    print("Testing to see if dictionary was preserved on round trip:")
    diffs = deep_diff(old_dict,new_dict)
    passed = diffs == []
    print(f'>>> Script-level Retention Test: {"passed" if passed else "failed"}')
    if not passed:
        pprint(diffs)

def test1():
    readResult = readTest(False)
    writeResult = writeTest(readResult)
    retResult = retTest(*writeResult)

    #return retResult

def syntaxSwap():
    readResult = readTest()

    from FoSpy.parsing.syntax import SYNTAX
    from FoSpy.parsing.regex import refresh

    SYNTAX["comment"]["prefix"] = "#"
    SYNTAX["key_value"]["prefix"] = "_"
    SYNTAX["key_value"]["delimiter"] = " "
    SYNTAX["nested"]["open"] = "{"
    SYNTAX["nested"]["close"] = "}"
    refresh()

    writeResult = writeTest(readResult)
    retResult = retTest(*writeResult)

if __name__ == "__main__":
    #syntaxSwap()
    test1()
    pass



