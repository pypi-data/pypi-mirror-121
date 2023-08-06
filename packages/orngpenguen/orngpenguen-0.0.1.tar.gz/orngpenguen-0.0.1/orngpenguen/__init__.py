from math import log10
import random


def bnny_code_encryption(code, key, hash_code_len):

    printable = '23456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#%&\()+,-./:;<=>?^_{|}@$[]'
    mode = len(key) % 3
    j = 1

    key = key.swapcase()
    seed_code = abs(int(10 * log10(len(key))))
    random.seed(seed_code)
    random.shuffle(list(code))
    code = ''.join(code)

    if mode == 0:
        mode = 1

    for i in range(len(key)):
        code = code[:i] + key[j] + code[i:]
        j = j + mode
        if j >= len(key):
            break

    seed_code = abs(int(10 * log10(len(key))))
    random.seed(seed_code)
    random.shuffle(list(code))
    code = ''.join(code)

    for i in code:
        if i not in printable:
            code = code.replace(i, '')

    seed_code = abs(int(10 * log10(len(key))))
    random.seed(seed_code)
    random.shuffle(list(code))
    code = ''.join(code)

    return code[1:hash_code_len + 1]


def str_to_binary(text):
    text = ''.join(format(ord(i), '08b') for i in text)
    return text


def byte_shuffler2(passwd, key):
    characters1 = '137G\(EFz#sxytu&)+,-5C/:;'
    characters2 = '24VWvw9XYZ!D68U%AB.'
    if passwd[0] in characters1:
        passwd = passwd[::-1]
        byte_key = str_to_binary(key)
        passwd = passwd[:1] + key + byte_key + '0ra' + passwd[1:] + key
        passwd = key + 'zAB' + byte_key + passwd[::-1]
        passwd = passwd[::-1]

    elif (passwd[0] in characters2) and (passwd[-1] in characters1) or (len(passwd) % 5 == 0):
        byte_key = str_to_binary(key)
        passwd = passwd[:1] + key + 'z070997' + byte_key[::-1] + '011' + passwd[1:] + key[::-1]
        passwd = passwd[::-1] + '0010110'

    elif (passwd[0] in characters1) and (key[1] in characters1):
        byte_key = str_to_binary(key)
        passwd = passwd[:1] + key + 'e1cret1m' + byte_key[::-1] + '01111' + passwd[1:] + key[::-1]
        passwd = passwd[::-1] + '1110110'

    else:
        byte_key = str_to_binary(key + key[::-1] + 'pica' + passwd + 'rd')
        passwd = passwd + byte_key[:-1]
        passwd = passwd[::-1] + '0010101010' + byte_key + key[1] + '0'

    return passwd


def binary_to_decimal(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while binary != 0:
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


def binary_to_str(bin_data):
    str_data = ' '

    for i in range(0, len(bin_data), 7):
        temp_data = int(bin_data[i:i + 7])
        decimal_data = binary_to_decimal(temp_data)
        str_data = str_data + chr(decimal_data)
    return str_data


def key_to_string_generator(passwd, key):

    key = str(key[::-1]) + str(10 * log10(len(key) + len(passwd))) + str(key) + str(
        0.5 + 10 * log10(len(key) + len(passwd)))
    key = str(str_to_binary(key) + '011010010110110001111001' + str_to_binary(
        passwd[::-1]) + str_to_binary(
        key + passwd[::-1]))
    key = key.replace(" ", "")

    if len(key) % 8 != 0:
        mode = len(key) % 8
        for i in range(mode + 2):
            key = key + '1'

    [key[i:i + 8] for i in range(0, len(key), 8)]
    ' '.join([key[i:i + 8] for i in range(0, len(key), 8)])
    key = binary_to_str(key)

    return key


def byte_shuffler1(passwd, key):
    characters1 = '5792y#U468sVWXPFx./:;'
    characters2 = 'BC13YRS)+tQA,-EzZ!uvD%G'
    if passwd[0] in characters1:

        passwd = passwd[::-1]
        byte_key = str_to_binary(key)
        passwd = byte_key + passwd[:-1] + key + byte_key + passwd[1:] + key
        passwd = passwd[::-1] + byte_key

    elif (passwd[0] in characters2) or (key[1] in characters1) or (len(passwd) % 3 == 0):
        byte_key = str_to_binary(key)
        passwd = byte_key + passwd[:-1] + key + byte_key[::-1] + '011' + passwd[1:] + key[::-1]
        passwd = passwd[::-1]


    elif (passwd[0] in characters1) and (passwd[2] in characters1):
        byte_key = str_to_binary(key)
        passwd = passwd[:1] + key + '23crebnnyt1m' + byte_key[::-1] + '01001' + passwd[1:] + key[::-1]
        passwd = passwd[::-1] + '111110'

    else:
        byte_key = str_to_binary(key[::-1])
        byte_key = byte_key[:5]
        passwd = '11100' + passwd[:1] + '101' + byte_key + key[1] + '0' + passwd[1:] + key[::-1]
    return passwd

    return code


class Penguen(object):

    def hash_generator(passwd, key, hash_code_len=15):
        key = key_to_string_generator(passwd, key)
        if len(key) % 2 == 0 and len(passwd) % 2 == 0:
            code = byte_shuffler1(passwd, key) + byte_shuffler2(key, passwd)
        elif len(key) % 2 != 0 and len(passwd) % 2 == 0:
            code = byte_shuffler2(passwd, key) + byte_shuffler1(key, passwd)
        elif len(key) % 2 != 0 and len(passwd) % 2 != 0:
            code = byte_shuffler1(passwd, key) + byte_shuffler2(passwd, key)
        else:
            code = byte_shuffler2(passwd, key) + byte_shuffler2(key, passwd)

        code = bnny_code_encryption(code, key, hash_code_len)

        return code
    @staticmethod
    def input_hash():
        x = True
        while x:
            key = input("Enter a key for your own hash generator:  ")
            re_key = input("Enter your key again:  ")
            if key == re_key:
                x = False
            else:
                print("Keys are not matched, please enter the same keys")
        x = True
        while x:
            passwd = input("Enter your password:  ")
            re_passwd = input("Enter your password again:  ")
            if passwd == re_passwd:
                x = False
            else:
                print("Keys are not matched, please enter the same keys")
        return passwd, key

