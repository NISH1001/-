#!/usr/bin/env python3


"""
accepts a cnf string
where synonyms are separated by ^^
eg: my^^i name is nishan^^mark
"""
def cnf_separator( cnf):
    # contains the cnf separated raw sentences(seq/tuple)
    raw = []

    # recursive cnf separator
    def cnf_recur(pre, post):
        if len(post) == 1:
            for x in post[0]:
                raw.append( tuple((pre + " " + x).split()) )
        else:
            for x in post[0]:
                cnf_recur(pre+" "+x, post[1:])

    splitted = cnf.split()
    separated = [ tuple(word.split('^^')) for word in splitted]
    if not separated:
        return []
    cnf_recur("", separated)

    return raw


def main():
    cnftest = "my^^i name is nishan^^mark"
    print(cnf_separator(cnftest))

if __name__=="__main__":
    main()

