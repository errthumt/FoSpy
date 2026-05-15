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
        "open": "["
    },

    "key_value": {
        "delimiter": ":",
        "require_value": True,
        "prefix": False
    },
    "comment": {
        "prefix": "//",
        "allow_leading_ws": True,
    }
}


meta_keys = {
    "comments" : "_fos_comments",
    "key_comments" : "_fos_key_comments",
    "list_type" : "_list_type"
}
