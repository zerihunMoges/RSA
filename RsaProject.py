import random



def checkprime(x,y):
    primess = []
    while len(primess) < 2:
        me = 0
        while me != 1:
            num = genratepossibleprime(x,y)
            me = lowest(7, num - 1, num)
        primess.append(num)
    return primess


def genratepossibleprime(x,y):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
              89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193,
              197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
              317, 331]

    randomnumber = random.randint(x,y)
    i = 0
    while i in range(len(primes)):
        rem = randomnumber % primes[i]
        if rem == 0:
            randomnumber = 2*random.randint(x,y) - 1
            i=0
        i+=1

    return randomnumber


def lowest(base, exponent, n):

    while exponent > 1:
        rem = 1
        while exponent > 1:
            if exponent % 2 != 0:
                rem *= base
                rem %= n
            base = (base ** 2) % n

            exponent = exponent // 2
            if exponent == 1:
                return (rem * base) % n


def gcd(number_1, number_2):
    rem = number_1 % number_2
    number_1 = number_2
    if rem == 0:
        return number_2

    return gcd(number_1, rem)


def public_key(p, q):
    phi_n = (p - 1) * (q - 1)

    e = random.randint(99999, 999999999)

    isfound = True
    while isfound:
        gcd_req = gcd(phi_n, e)
        if gcd_req != 1:
            e = random.randint(99999, 999999999)
        elif gcd_req == 1:
            isfound = False
            break

    return e

def encrypt(files, n, e):
    messageasci = ''

    file = open(files, 'r')
    encryptedfile = open('encryptedfile.txt','w+')

    message = file.read()
    index = 0
    messageline = message.split('\n')
    for message in messageline:
        for letter in message:
            if index == len(message) - 1:
                messageasci += (str(ord(letter)))
                break
            messageasci += (str(ord(letter)) + '34535')
            index += 1
        if messageasci != '':
            messageasci = int(messageasci)
            encryptedfile.writelines(str(lowest(messageasci, e, n))+'\n')
        messageasci = ''
    file.close()

def decrypt(file, d, n):
    encrypted_file = open(file,'r+')
    decfile = open('decrfile.txt', 'w+')
    line = encrypted_file.readline()

    while line != '':
        message_line = lowest(int(line), d, n)
        message_asci = str(message_line).split('34535')
        stringmessage = ''
        for asci in message_asci:
            if asci != '':
                stringmessage += chr(int(asci))
        decfile.writelines(stringmessage+ '\n')
        line = encrypted_file.readline()
    encrypted_file.close()
    decfile.close()

choice = input('what do you want to do?\n'
               '1. generate public key\n'
               '2. encrypt message\n'
               '3. decrypt message \n')

if choice == '1':
    digit = eval(input("how digits of public key do you want"))
    x = 10 ** (digit - 1)
    y = 10 * x
    primes = checkprime(x,y)
    p = primes[0]
    q = primes[1]

    phi_n = (p-1) * (q-1)
    n = p*q
    e = public_key(p, q)
    d = pow(e, -1, phi_n)
    write_privatekey = open('rsaprivate.txt', 'w+')
    write_publickeys = open('rsapublic.txt', 'w+')
    publickey_e = 'pulic_exponent: ' + str(e)
    publickey_n = 'public_n: ' + str(n)

    write_publickeys.writelines(publickey_n + "\n " + publickey_e)
    write_privatekey.writelines(str(d))

elif choice == '2':
    public_keysfile = open('rsapublic.txt', 'r+')

    n = int((public_keysfile.readline()).split('public_n:')[1])
    e = int((public_keysfile.readline()).split('pulic_exponent:')[1])

    file = input('enter file to be encrypted')
    encrypt(file, n, e)

elif choice == '3':
    public_keysfile = open('rsapublic.txt', 'r+')
    private_keyfile = open('rsaprivate.txt', 'r')
    d = int(private_keyfile.read())

    n = int((public_keysfile.readline()).split('public_n:')[1])

    file = input('enter file to be decrypted')
    decrypt(file, d,n)
