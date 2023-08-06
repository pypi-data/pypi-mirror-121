class BinarySearch:
    """
    Instantiate a multiplication operation.
    Numbers will be multiplied by the given multiplier.

    :param blist: The multiplier.
    :type blist: list
    """

    def __init__(self, blist):
        self.blist = sorted(blist)

    def search(self, data):
        """
        Search an element in the list

        :param data:The element to be searched
        :type data: int

        :return: the result
        :rtype: String
        """
        low = 0
        high = len(self.blist) - 1
        while low <= high:
            mid = (low + high) // 2
            if data > self.blist[mid]:
                low = mid + 1
            elif data < self.blist[mid]:
                high = mid - 1
            else:
                return "Found"
        return "Not Found"


# lc = [random.randint(1, 100000) for i in range(10000)]
# print(lc)
# best, others = bo.big_o(BinarySearch, lc, n_repeats=100)
# print(best)
