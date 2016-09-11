class Dict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def main():
    d = {'a': 'A', 'b': 'B'}
    e = Dict(d)
    print(e.a)
    e.c = 'C'
    print(e.c)
    del e.b
    print('b' not in d)
    print(e.d)  # will raise a KeyError

if __name__ == '__main__':
    main()
