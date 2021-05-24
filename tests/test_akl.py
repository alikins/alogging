from alogging.echo import echo, echo_format


def gen_x():
    _x = []
    for i in range(37, 52):
        _x.append((i, '.' * i))
    return _x


def gen_blip(_x):
    _blip = [1, 2, 3, 4, _x, ['list1', 'list2', {'some_dict_key': ('a tuple 1', 'a tuple 2')}]]
    return _blip


x = gen_x()
blip = gen_blip(x)


def blorp(thing):
    for i in 'adfafadfasdf':
        echo(i)

    echo(thing)


def main():

    print('echo(blip)')
    echo(blip)

    foo = echo_format(blip)
    print('echo_format(blip)')
    print(foo)

    print('echo(4 + 2)')
    echo(4 + 2)

    print('echo([z for z in x if z[0] % 2])')
    echo([z for z in x if z[0] % 2])

    print('blorp()')
    blorp(blip)


# These are all printing to stdout, so not much to test
# until we either stop side effect or capture stdout
# and examine. TODO...
def test_main():
    main()


def test_blorp():
    blorp(blip)


if __name__ == '__main__':
    main()
