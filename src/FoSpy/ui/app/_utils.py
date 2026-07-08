def _get_label(blk, i=None):        
    id_key, id_txt = blk.get_id()
    label = f"{i} - " if i is not None else ""
    label += id_txt

    if id_key is None:
        label += " Object"

    return label