import time

def radix_sort(alist):
    offset = abs(min(alist)) if min(alist) < 0 else 0   #shift all the value of the list by the min number's value to solve the negative number
    alist = [ num + offset for num in alist]
    max_digit = len(str(max(alist)))

    if offset != 0:
        print(f"Because the list contain negative number, the list would be ajust temporary:\n{alist}\n")
        time.sleep(1)

    for index in range(max_digit):
        bucket = [[] for _ in range(10)]       #create the bucket of exch digit(0-9), clear after every loop of index
        
        print("Sorting the",index,"index")
        for num in alist:                       #according to the values of each number current index's digit, add it to the required digit bucket
            digit = (num // (10**index)) % 10
            print(f"The digit of {num} in index {index + 1} is {digit}.")
            bucket[digit].append(num)
            
            print("\t",bucket)
            time.sleep(1)
        time.sleep(1)
        print("-"*50)
        
        alist = []                                  # push the sorted number back to the list
        for num in bucket:
            alist.extend(num)

        print(f"Current list: {alist}")
        print("-"*50)
        time.sleep(1)

    alist = [ num - offset for num in alist]
    if offset != 0:
        print(f"Re-ajust the list back to original value:\n{alist}\n")
        time.sleep(1)

    return alist                 #shifting all the value of the list back to original values


test_num = [1556,4,-3556,593,408,4386,902,7,8157,-86,9637,29]
print("Unorted list: ",test_num)
print("-"*50)
time.sleep(2)
print("Sorted result: ", radix_sort(test_num))
