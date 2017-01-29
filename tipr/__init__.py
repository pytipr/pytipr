def write_file(filename, text='Hello world!'):
    with open(str(filename), 'w') as f:
        f.write(text)
