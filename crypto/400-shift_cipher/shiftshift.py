#this table contain the abc from a-z each
#abc is mapped to a specific number. for example a-> 0, b->1 etc up to z-> 25
#this allow us to map a letter to a number
look_up_table = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 
    'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 
    'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 
    't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25
}

#this will allow us to map a number to a letter
reverse_look_up_table = {
    0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 
    7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 
    13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 
    19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'
}

message = input("Enter your message to encrypt:")

#go thorugh each letter in the abc and encrypt them. 
#we dont want to touch {} but we will encrypt everything else
encrypted_message = "" #we will start the encryption as blank
for letter in message:
    #make the letter lowercase
    letter = letter.lower()

    #is the "letter" some type of special character or numbers?
    if letter not in look_up_table:
        #this is true so we dont want to encrypt it, we will just add it untouched
        encrypted_message+=letter
    else:
        #we will find the position of the letter the lookup table and shift by 3
        number = look_up_table[letter]
        shift = number + 3
        #we need to check to see if we go past 26... if we do, we need to wrap around and keep counting
        #for example, 25+3 will be 28 but wrapping around it will go to 2(remember 0 is also part of the counting)
        shift  = shift % 26 # we are  using mod to wrap around, the max is 26

        encrypted_message+= reverse_look_up_table[shift]


#output the encrypted message
print(encrypted_message)
        
