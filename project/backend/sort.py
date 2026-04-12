

def mergeSort(list,start,end):
    if(start<end):
        mid =(start+end)//2
        mergeSort(list,start,mid)
        mergeSort(list,mid+1,end)
        merge(list,start,mid,end)
        
        
def merge(list,start,mid,end):
    
    left_array_size = mid - start + 1
    right_array_size = end - mid
    left_array=[0]*left_array_size
    right_array=[0]*right_array_size
    for i in range(left_array_size):
        left_array[i] =list[start+i]
    
    for j in range(right_array_size):
        right_array[j] = list[mid+1+j]
    
    i=0
    j=0
    k=start
    
    while(i<left_array_size and j<right_array_size):
        if(left_array[i]<=right_array[j]):
            list[k]=left_array[i]
            i+=1
            k+=1
        else:
            list[k]=right_array[j]
            j+=1
            k+=1
        
    
    
    while(i<left_array_size):
        list[k]=left_array[i]
        i+=1
        k+=1
    
    
    while(j<right_array_size):
        list[k]=right_array[j]
        j+=1
        k+=1
        



list=[0,3,5,2,1,4]

mergeSort(list,0,len(list)-1)
print(list)