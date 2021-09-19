from utils import *
import hashlib
import os
import random

# data structure: [[address1, balance1],[address2, balance2]]
# value : "address balance"
random.seed(297)


def getRandomAddress():
    return ('%030x' % random.randrange(16**43))[0:40]


def getRandomBalance(digit=6):
    return random.randint(0, 10**(digit+1))


def getRandomData():
    return getRandomAddress(), getRandomBalance()


def createSortedData(count=40):
    addresses = []
    for i in range(count):
        addresses.append(getRandomData())
    addresses.sort()
    return addresses


def createTXT(data=createSortedData()):
    file = open('data.txt', 'w')
    for i in data:
        address, balance = i
        file.write(address + ' ' + str(balance) + '\n')
    file.close()


def TXTtoData():
    # read txt and put data into data structure
    allFiles = os.listdir()
    data = []
    for i in allFiles:
        if '.txt' in i:
            file = open(i, "r")
            lines = file.readlines()
            for line in lines:
                data.append(line.replace("\n", ""))

    return data


def hash(input):
    m = hashlib.sha256(input.encode())
    return m.hexdigest()


class MerkleTree:
    def __init__(self):
        pass

    def findMerkleRoot(self, leafHash):
        hash1 = []
        hash2 = []
        if len(leafHash) % 2 != 0:  # repeat the last element
            leafHash.extend(leafHash[-1:])

        for leaf in sorted(leafHash):
            hash1.append(leaf)
            if len(hash1) % 2 == 0:  # only add secondary hash if there are two first hash
                # hash both hashes
                hash2.append(hash(hash1[0]+hash1[1]))
                hash1 == []  # reset first hash
        if len(hash2) == 1:  # at the root
            return hash2
        else:
            return self.findMerkleRoot(hash2)  # recurse with hash2


if __name__ == "__main__":
    # createTXT() # used to created a txt file
    accounts = TXTtoData()
    leafHash = []
    for account in accounts:
        leafHash.append(hash(account))

    mt = MerkleTree()
    print(mt.findMerkleRoot(leafHash))
