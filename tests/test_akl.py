from akl.echo import dd, echo, echo_format

x = []
for i in range(37, 52):
    x.append((i, '.'*i))

blip = [1, 2, 3, 4, x, ['list1', 'list2', {'some_dict_key': ('a tuple 1', 'a tuple 2')}]]

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

if __name__ == '__main__':
    main()
