from texttable import Texttable

def get_texttable(headers, data):
    t = Texttable(max_width=120)
    t.set_deco(Texttable.HEADER)
    t.add_row(headers)
    for d in data:
        t.add_row(d)
    return t