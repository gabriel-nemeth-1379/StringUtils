import sys

if __name__ == '__main__':
    subject = sys.argv[1:2]
    if not subject:
        print('No input provided. Please enter a string as a parameter. e.g.: snake \'Snake case this please\'')
        quit()

    subject = subject.pop()
    subject = subject.lower()\
        .replace(':', '')\
        .replace('"', '')\
        .replace(',', '')\
        .replace('  ', ' ')\
        .replace(' ', '_')\
        .replace('&', 'and')

    print(subject)
