def radix_sort(alist):
    offset = abs(min(alist)) if min(alist) < 0 else 0   #shift all the value of the list by the min number's value to solve the nagative number
    alist = [ num + offset for num in alist]
    max_digit = len(str(max(alist)))

    for index in range(max_digit):
        bucket = [[] for _ in range(10)]       #create the bucket of exch digit(0-9), clear after every loop of index
        
        for num in alist:                       #according to the values of each number current index's digit, add it to the required digit bucket
            digit = (num // (10**index)) % 10
            bucket[digit].append(num)
        
        alist = []                                  # push the sorted number back to the list
        for num in bucket:
            alist.extend(num)

    return [ num - offset for num in alist]                 #shifting all the value of the list back to original values


test_num = [1556,4,-3556,593,408,4386,902,7,8157,-86,9637,29]
print("Unorted list: ",test_num)
print("Sorted result: ", radix_sort(test_num))
