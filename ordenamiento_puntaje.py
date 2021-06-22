
#Codigo tomado de https://www.programmersought.com/article/58117572404/
#Se modifico el codigo, para que afecte a tanto la lista de nombres como la lista de puntajes
def partition_desc(A, B, p, r):
    if r>p:
        #Used to indicate the position of <x
        i = p-1
        #Used to move traversal
        j = p
        #Main element
        x = A[r]
        #Traversal [p, r-1] interval
        for j in range(p, r):
            if A[j]>=x:
                #Move the partition indicating the cursor, add a position
                i += 1
                #Add the partition element at the last position of the partition
                A[i],A[j] = A[j],A[i]
                B[i],B[j] = B[j],B[i]
        #Now, any e1∈A[p, i], e1>=x; any e1∈A[p, r-1], e1<x
        #Exchange A[i+1] and A[r], generate a new process area
        A[i+1],A[r] = A[r],A[i+1]
        B[i+1],B[r] = B[r],B[i+1]
        
        q = i + 1
        return A, B, q
    else:
        return A, B, p

def quick_sort_desc(A, B, p, r):
    A, B, q = partition_desc(A, B, p, r)
    if p<r:
        A, B = quick_sort_desc(A, B, p, q-1)
        A, B = quick_sort_desc(A, B, q+1, r)
        return A, B
    else:
        return A, B

#---------Hasta aqui el codigo tomado del sitio web---------#
names_list = []
Scores_list = []
def ordenar_puntajes():
    global names_list, Scores_list
    file= open("Scores.txt","r")
    
    for line in file.readlines():
        name =""
        score = ""
        split = False
        for char in line:
            if char == "$":
                split = True
            elif split:
                score+=char
            else:
                name+=char
        names_list.append(name)
        Scores_list.append(int(score))
    quick_sort_desc(Scores_list,names_list,0,len(Scores_list)-1)


if __name__ == "__main__":
    ordenar_puntajes()
    for i in range(0,len(names_list)-1):
        print(names_list[i], Scores_list[i])
