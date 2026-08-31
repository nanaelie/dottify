from dottify import dottify_mode

with dottify_mode():
    data = {'name': 'Bob'}

    print(type(data))