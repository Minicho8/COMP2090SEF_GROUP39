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
    max_digit_index = len(str(max(array)))                  #determine the maximum elements digits
    for digit_index in range(max_digit_index):              #having loop to sort by each index
        counting_sort(array,digit_index)
    return array

test_num = [3009,9873,1672,8080,2981,3,5015,837,318,936,54,1935,440,3552,996,93,579]
print("Unorted list: ",test_num)
print("Sorted result: ", radix_sort(test_num))
