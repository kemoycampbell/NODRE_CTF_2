import time
import random

#this is a helper function which will allow us to generate a number between 0-9
def get_random_number():
    number = random.randint(0, 9)
    return number


#setup the current time
system_start_time = int(time.time())

#we want our watch to all sync so that it is the same for everyone. 
#We will use the system start time as the seed to sync all watches so that the result is always the same
random.seed(system_start_time)

#goes on forever until they get it right
while True:
    #we wan to generate 4 pin numbers with the last one being blank
    #we will only do 3 cause the last one is blank
    pins = ""
    for i in range(3):
        next_digit = get_random_number()
        pins += str(next_digit)
    
    #show the 3 numbers with _ as 4th
    pins+="__"
    print(pins)

    #secretly create the 4th number then ask the user for it
    fourth_number = get_random_number()
    answer = int(input("What is the 4th number:"))

    #if the guess is correct then they are one of our script kidddie so we will show them the flag
    if fourth_number == answer:
        with open('flag.txt') as file:
            #show the flag as they
            print(file.read())
            break
    else:
        print("Incorrect last digit pin number. Try again")
    

    #show how long the system has been up
    now_time = int(time.time())

    total_amount_of_time_passed = now_time - system_start_time
    print("Uptime:" + str(total_amount_of_time_passed))
        


    

