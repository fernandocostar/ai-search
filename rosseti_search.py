def check_heuristic(sorted_by_influence, k):
    return sum(sorted_by_influence[:k])*0.8

def check_kest(matrix, k, origin, visited): #olha os k maiores nao visitados de um vertice origem e retorna um valor de heuristica
    sorted_by_influence = [(i, matrix[i][-1]) for i in range(len(matrix[origin])-1)].sort(key=lambda x: x[1], reverse=True) #array de tuplas com o vizinho e a soma do vizinho
    k_biggest = []
    i = 0
    while(len(k_biggest) != k and i < len(matrix[i])-1):
        if not visited[sorted_by_influence[i][0]]:
            k_biggest.append(sorted_by_influence[i])
        i += 1
    return k_biggest, check_heuristic(sorted_by_influence, k)

def heuristic_test(actual, maximum):
    return 1 if actual >= maximum*0.2 else 0

def rosseti_searchUtil(matrix, visited, origin, k, max_heuristic, result):
    if visited[origin]:
        return
    visited[origin] = 1
    k_biggest, result_heuristic = check_kest(matrix, k, origin, visited)
    if heuristic_test(result_heuristic, max_heuristic):
        for each in k_biggest:
            if result[-1][1] < each[1]:
                result.pop(-1)
                result.append(each)
                result.sort(key=lambda x: x[1], reverse=True) #podia ser uma min heap
        if result_heuristic > max_heuristic:
            max_heuristic = result_heuristic
        while(len(k_biggest)):
            for each in k_biggest:
                rosseti_searchUtil(matrix, visited, each[0], k, max_heuristic, result)
    return

def rosseti_search(matrix, k):
    result = []
    visited = [0]*len(matrix)
    matrix = matrix.sort(key=lambda x: x[-1], reverse=True)
    rosseti_searchUtil(matrix, visited, matrix[0][0], k, check_kest(matrix, k, 0, visited)[1], result)
    for each in result:
        print("Node:", each[0], "Connections:", each[1])
    return

def main(max_population, k):

    adj_list = [[i] for i in range(max_population + 1)]

    with open("facebook_combined.txt", "r") as file:

        for line in file:
            origin, destiny = map(int, line.split(" "))
            adj_list[origin].append(str(destiny))
            adj_list[destiny].append(str(origin))

        [each.append(len(each)) for each in adj_list]

    rosseti_search(adj_list, k)

main(4039, 10)