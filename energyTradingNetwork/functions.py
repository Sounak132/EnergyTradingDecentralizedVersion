from random import randint

# class AddressGenerator:
def generateAddress():
    listOfCharacters  = "QWERTYUIOPLKJHGFDSAZX14352754764572CVBNMmnb56709872vcxzlkjhgfdsapoiuyVBNMmnbvcxzlkjtrewq12345OPLKJHGFD67ERTYUIOPLK89345OPLKJ0"
    length = len(listOfCharacters)
    address = ""
    for i in range(32):
        address += listOfCharacters[randint(0,length-1)]
    return address

