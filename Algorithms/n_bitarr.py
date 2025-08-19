

def n_bitArr(n):
    """
    Implement a function that returns a (list of) every list of 0's and 1's of length n 
    (in any order)

    For example, n_bitArr(1) -> [[0],[1]]
    For example, n_bitArr(2) -> [[0,0],[0,1],[1,0],[1,1]]  

    :return: A list containing all lists of 1's 0's of lenght n 
    :rtype: list[list[int]]
    """
    
    res = []

    def generate(current):
        if len(current) == n:
            res.append(current)
        else:
            generate(current + [0])
            generate(current + [1])
        return

    generate([])
    return res
