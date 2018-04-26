x = 0
lista = [1, 2, 2, 1, 2, 2, 6]
middle = lista.__len__() // 2
say = 0;
while True:
    say+=1
    if lista[middle] < lista[middle+1]:
        print(middle)
        lista = lista[middle + 1:]
        middle = lista.__len__() // 2

    elif lista[middle] < lista[middle-1]:
        lista = lista[0:middle - 1]
        middle = lista.__len__() // 2
    else:
        x = lista[middle]
        break;
print(x)
print(say)

