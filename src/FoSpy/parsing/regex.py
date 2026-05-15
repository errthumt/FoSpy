import re

BLOCK_HEADER = re.compile(r"^(?:\[\[(?P<list_name>[^\]]+)\]\]|\[(?P<single_name>[^\]]+)\])$")

KEY_VALUE = re.compile(r"^(?P<key>[^:]+)\s*:\s*(?P<val>.+)$")

NESTED_START = re.compile(r"^\[(?P<list>\[)?(?P<rest>.*)$")

LOOP_KEY = re.compile(r"^:(?P<key>[^:]+)$")

COMMENT_LINE = re.compile(r"^\s*//(?P<text>.*)$")





