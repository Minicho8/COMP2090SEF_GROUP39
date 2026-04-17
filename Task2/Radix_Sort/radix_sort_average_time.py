import time,random

def counting_sort(array,exp):
    bucket = [[] for _ in range(10)]                        #create the bucket of exch digit(0-9), clear after every loop of index
    
    for num in array:                                       #according to the values of each number current index's digit, add it to the required digit bucket
        digit_value = (num // (10**exp)) % 10
        bucket[digit_value].append(num)
    
    array.clear()                                           #clear the unsorted array 
    for num in bucket:                                      # push the sorted number back to the list
        array.extend(num)

def radix_sort(array):
    if not array:                                           #stop the process if array is empty
        return array
    print("Unorted list:: ",array)
    max_digit_index = len(str(max(array)))                  #determine the maximum elements digits
    for digit_index in range(max_digit_index):              #having loop to sort by each index
        counting_sort(array,digit_index)
    print("Sorted result: ",array)

def radix_timer(test_num):
    start_time = time.time()
    result = radix_sort(test_num)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Running time: {total_time}")
    return total_time

def radix_average_time():
    test_time = []
    for i in range(100):
        ran_num = [random.randint(1,10000) for _ in range(100)]
        print("-"*40)
        test_time.append(radix_timer(ran_num))
    print("-"*40)
    return sum(test_time)/100
print(f"The avrange running time for radix sort sorting 100 elements is: {radix_average_time()} sec.")
