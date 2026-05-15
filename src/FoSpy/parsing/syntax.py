line_comment = "//"
key_delimiter = ":"
indent = "    "

SYNTAX = {
    "block_header": {
        "single": {
            "open": "[",
            "close": "]",
        },
        "list": {
            "open": "[[",
            "close": "]]",
        }
    },
    "nested": { 
        "open": "[",
        "close" : "]"
    },

    "key_value": {
        "delimiter": ":",
        "require_value": True,
        "prefix": False
    },
    "comment": {
        "prefix": "//",
        "allow_leading_ws": True,
    },
    "indent_size": 4
}


meta_keys = {
    "comments" : "_fos_comments",
    "key_comments" : "_fos_key_comments",
    "list_type" : "_list_type"
}

meta_defaults = {
    "_fos_comments" : [],
    "_fos_key_comments" : [],
    "_list_type" : ""
}
