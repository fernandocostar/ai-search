adj_list = [[] for i in range(4039)]

def check_heuristic(sorted_by_influence, k):
    return sum(sorted_by_influence[:k])*0.8

def check_kest(matrix, k, origin, visited): #olha os k maiores nao visitados de um vertice origem e retorna um valor de heuristica
    sorted_by_influence = [(i, matrix[i][-1]) for i in range(len(matrix[origin])-1)].sort(key=lambda x: x[1], reverse=True) #array de tuplas com o vizinho e a soma do vizinho
    k_biggest = []
    i = 0
    while(len(k_biggest) != k and i < len(i)):
        if not visited[sorted_by_influence[i][0]]:
            k_biggest.append(sorted_by_influence[i])
        i += 1
    return k_biggest, check_heuristic(sorted_by_influence, k)

def heuristic_test(actual, maximum):
    return 1 if actual >= maximum*0.2 else 0

def rosseti_search(matrix, visited, origin, k, max_heuristic, result):
    k_biggest, result_heuristic = check_heuristic(matrix, k, origin, visited)
    visited[origin] = 1
    if heuristic_test(result_heuristic, max_heuristic):
        for each in k_biggest:
            if result[-1][1] < each[1]:
                result.pop(-1)
                result.append(each)
                result.sort(key=lambda x: x[1], reverse=True)

        while(len(k_biggest) and total >= total_max*0.80):
            if total > total_max:
                total_max = total
            for each in k_biggest:
                return rosseti_search(matrix, visited, each, k, total_max, result)
    return

with open("facebook_combined.txt", "r") as file:

    for line in file:
        origin, destiny = map(int, line.split(" "))
        adj_list[origin].append(str(destiny))
        adj_list[destiny].append(str(origin))

    [each.append(len(each)) for each in adj_list]

    for each in adj_list:
        reachable = each[-1]
        for i in range(reachable):

