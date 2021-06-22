import random
import time
#Codigo tomado de https://www.programmersought.com/article/58117572404//
def partition_desc(A, p, r):
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
        #Now, any e1∈A[p, i], e1>=x; any e1∈A[p, r-1], e1<x
        #Exchange A[i+1] and A[r], generate a new process area
        A[i+1],A[r] = A[r],A[i+1]
        q = i + 1
        return A, q
    else:
        return A, p

def quick_sort_desc(A, p, r):
    A, q = partition_desc(A, p, r)
    if p<r:
        A = quick_sort_desc(A, p, q-1)
        A = quick_sort_desc(A, q+1, r)
        return A
    else:
        return A

# -+-=> Evaluacion Experimental del Tiempo de Ejecucion del Algoritmo Quicksort <=-+- #


def Algoritmo():
    # -- >Lista Aleatoria< -- #
    randomlist = random.sample(range(0,10000),10000)

    # -- ><> Tiempo de Ejecucion <>< -- #
    Tiempo_Inicial = time.time()

    quick_sort_desc(randomlist,0,len(randomlist)-1)

    Tiempo_Final = time.time() - Tiempo_Inicial
    
    return Tiempo_Final

Suma_de_Tiempos = 0
for i in range(1,16):
    Tiempo = Algoritmo()
    print(f"Intento: {i}  | Tiempo de Ejecucion: {Tiempo}" if i<10 else f"Intento: {i} | Tiempo de Ejecucion: {Tiempo}")
    Suma_de_Tiempos += Tiempo
print(f"Tiempo de Ejecucion promedio:      {Suma_de_Tiempos/15}")