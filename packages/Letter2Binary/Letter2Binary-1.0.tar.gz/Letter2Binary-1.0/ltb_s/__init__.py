class binary:
    def binarynya(letter):
        string = letter

        convert = ''.join(format(ord(i), '08b') for i in string)

        return f'Result: {convert}'

def genbinary(text_letter):
    try:
        print(binary.binarynya(text_letter))
    except:
        return 'ERROR. Try msg the developer(iFanpS)'

genbinary('Aku anak anjing')