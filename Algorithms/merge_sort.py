"""
MergeSort is a divide-and-conquer algorithm that splits a list into two halves, recursively sorts each half,
and then merges the sorted halves back together.
The "divide" step keeps breaking the list down until sublists of size one are reached (which are inherently sorted).
The "merge" step combines the sorted sublists into a larger sorted list by comparing elements one by one.

The functions below are split the same way, "merge" merges tho sorted list into one sorted list.
mergesort splits the two list into two list and recursively sorts the lists.

Before starting this exercise try to understand why this is a divide and conquer algorithm.
"""

def mergesort(list_):
    """
    One step in the merge sort algorithm.
    Here, you split the list sort them both, and then merge them.

    You have to use merge.

    :param list_: An unsorted list that needs to be sorted.
    :type list_: list[int/float]
    :return: The sorted list.
    :rtype: list[int/float]
    """
    if len(list_) <= 1:
        return list_
    middle = len(list_)//2
    list1 = list_[:middle]
    list2 = list_[middle:]
    a = mergesort(list1)
    b = mergesort(list2)
    return merge(a, b)


def merge(list1, list2):
    """
    This method merges two sorted lists into one new sorted list, in O(n).

    You are not allowed to use sorted as this is at least O(n log(n)).

    :param list1: A sorted list that needs to be merged.
    :type list1: list[int/float]
    :param list2: A sorted list that needs to be merged.
    :type list2: list[int/float]
    :return: The sorted list.
    :rtype: list[int/float]
    """
    newlist = []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            newlist.append(list1[i])
            i += 1
        else:
            newlist.append(list2[j])
            j += 1
    
    if len(list1) > i:
        newlist += list1[i:]
    if len(list2) > j:
        newlist += list2[j:]
    return newlist


if __name__ == "__main__":
    lst = [3, 4, 1, 10, 2, 7, 1]
    print(f"The ordered version of the list {lst} is {mergesort(lst)}")