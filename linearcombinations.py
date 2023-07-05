import random
import warnings
from partition import Partition
from sympy import *
from sympy.abc import d
import itertools


def get_zero_points(operation: "Operations"):
    """
    Given an operation object, calculate it's zero points
    :param operation
    :return: List of zero points
    """
    assert isinstance(operation, Operations)
    term = 0

    for i in operation.partition_sum.copy():
        term = term + i[0]

    return solve(Eq(term, 0))


def build_pn(n: int) -> "Operations":
    """
    Build non-crossing neighboring bottom partition sum
    :param n: size of partitions
    :return: Whole sum of the partitions
    """

    """size 2^(n-1), if 1 -> connect else not connect"""
    partitions_binary = set()

    """partitions as tuple generated from partitions_binary"""
    partitions = set()

    """get all binary numbers of size n-1"""
    for i in itertools.product([0, 1], repeat=n-1):
        partitions_binary.add(i)

    """connect if 1 else not"""
    for nn in partitions_binary:
        p = list(range(1, n+1))
        for i, nnn in enumerate(nn):
            if nnn:
                p[i+1] = p[i]
        partitions.add(tuple(p))

    """final output of partition sum"""
    p_n = Operations([[]])

    """add the partitions to p_n with a coefficient of -1^(n-number of blocks)"""
    for i in partitions:
        p = Partition([], list(i))
        p.hash_form()
        p_n.partition_sum += [[int((-1) ** (n - number_of_blocks_for_build_pn(p))), p]]

    return p_n


def generate_A_B_random(n: int, size: int, k: int, l: int):
    """
    generate and print out a random list of length n with variations of multiplications of A_k_l and B_k_l and their
    zero points
    :param n: length of printed out list
    :param size: upper bound for number of multiplications
    :param k: upper bound for k values
    :param l: upper bound for l values
    """

    """increment if we have generated a sequence which we already calculated"""
    mini_counter = 0

    """increment if we generated a new sequence"""
    counter = 0

    """set of already generated sequences"""
    already_generated = set()

    first_k_plus_l = 0

    """operate as long as we have less than n sequences generated"""
    while counter < n:

        """get sequence size"""
        number_of_ab = random.randint(1, size)

        """store sequence"""
        a_b_constellation = []

        """calculate multiplicands with their k and l"""
        for i in range(number_of_ab):

            a_or_b = random.randint(0, 1)

            rand_k = random.randint(0, k)
            rand_l = random.randint(0, l)

            """to later check assumption: term of form d*(d - 2)*(d - 1)**q with q = sum of first k and l of 
            multiplication"""
            if i == 0:
                first_k_plus_l = rand_k + rand_l

            if a_or_b:
                a_b_constellation.append(("A", rand_k, rand_l))
            else:
                a_b_constellation.append(("B", rand_k, rand_l))

        """check whether we generated a new sequence"""
        if tuple(a_b_constellation) not in already_generated:
            already_generated.add(tuple(a_b_constellation))
            mini_counter = 0
        else:
            """if not warn the user if there is suspicion of a to big n value"""
            if mini_counter >= 5000:
                warnings.warn("Warning...........your n may be to big for your 'size', 'k' and 'l'")
                print("       ")
                val = input(f"You have until now {counter} found, want to terminate? [y/n]")
                if val.lower() == "y":
                    return
            mini_counter += 1
            continue

        """iterate through sequence and create the multiplication term"""
        if a_b_constellation[0][0] == "B":
            term = Operations([[1, Partition(list(range(1, a_b_constellation[0][1] + a_b_constellation[0][2] + 1 + 3)), [])]]) * B_k_l(a_b_constellation[0][1], a_b_constellation[0][2])
            upper_partitions = 2 + a_b_constellation[0][1] + a_b_constellation[0][2]
        else:
            term = Operations([[1, Partition(list(range(1, a_b_constellation[0][1] + a_b_constellation[0][2] + 1 + 2)), [])]]) * A_k_l(a_b_constellation[0][1], a_b_constellation[0][2])
            upper_partitions = 3 + a_b_constellation[0][1] + a_b_constellation[0][2]
        for ii in a_b_constellation[1:]:
            if ii == "B":
                if upper_partitions == 3 + ii[1] + ii[2]:
                    term *= B_k_l(ii[1], ii[2])
                    upper_partitions = 2 + ii[1] + ii[2]
                else:
                    break
            else:
                if upper_partitions == 2 + ii[1] + ii[2]:
                    term *= A_k_l(ii[1], ii[2])
                    upper_partitions = 3 + ii[1] + ii[2]
                else:
                    break

        """simplify term and get zero points"""
        term *= build_pn(upper_partitions)
        term.simplify_operation()
        zero = get_zero_points(term)

        """check whether assumption: term of form d*(d - 2)*(d - 1)**q with q = sum of first k and l of multiplication
        """
        if str(factor(term.partition_sum[0][0]))[-1] == ")":
            assert first_k_plus_l + 1 == 1
        else:
            assert first_k_plus_l + 1 == int(str(factor(term.partition_sum[0][0]))[-1])
        """print zero points"""
        print("zero points of " + str(a_b_constellation) + f" are " + str(zero), f" with the term {term} and the factorization {factor(term.partition_sum[0][0])}")

        counter += 1


def generate_A_B(n: int, k: int, l: int):
    """
    Systematically generate multiplication of A_k_l and B_k_l with all combinations in which the k and l values
    are consistent per sequence. Print out respective zero points.
    :param k: upper bound for k values
    :param l: upper bound for l values
    :param n: sequence size
    """

    counter = 0
    """generate all A B sequences of size n"""
    for i in itertools.product(["A", "B"], repeat=n):
        """get every sequence combination for vales <= k and <= l"""
        for lii in range(l+1):
            for kii in range(k+1):
                """iterate through sequence and construct multiplication term"""
                if i[0] == "B":
                    term = Operations([[1, Partition(list(range(1, lii + kii + 1 + 3)), [])]]) * B_k_l(kii, lii)
                    upper_partitions = 2 + kii + lii
                else:
                    term = Operations([[1, Partition(list(range(1, lii + kii + 1 + 2)), [])]]) * A_k_l(kii, lii)
                    upper_partitions = 3 + kii + lii
                for ii in i[1:]:
                    if ii == "B":
                        if upper_partitions == 3 + kii + lii:
                            term *= B_k_l(kii, lii)
                            upper_partitions = 2 + kii + lii
                        else:
                            break
                    else:
                        if upper_partitions == 2 + kii + lii:
                            term *= A_k_l(kii, lii)
                            upper_partitions = 3 + kii + lii
                        else:
                            break

                """simplify term and get zero points"""
                term *= build_pn(upper_partitions)
                term.simplify_operation()
                zero = get_zero_points(term)

                """print out each combination with zero points"""
                print("zeropoints of " + str(i) + f" with k = {kii} and l = {lii} are " + str(zero))

                counter += 1


def number_of_blocks_for_build_pn(p: Partition) -> int:
    """
    Get the number of blocks as a helper function of build_pn
    :param p: Partition on which we need number of blocks
    :return: number of blocks
    """
    return max(p.partition[0] + p.partition[1])


def A_k_l(k: int, l: int):
    base = Partition([1], [1])

    a1 = Partition([1, 2, 3], [1, 3])
    a2 = Partition([1, 2, 1], [1, 1])

    for i in range(k):
        a1 = base.tensor_product(a1)
        a2 = base.tensor_product(a2)

    for i in range(l):
        a1 = a1.tensor_product(base)
        a2 = a2.tensor_product(base)

    return Operations([[1, a1], [-1, a2]])


def B_k_l(k: int, l: int):
    base = Partition([1], [1])

    b1 = Partition([1, 2], [1, 3, 2])
    b2 = Partition([1, 2], [1, 1, 2])
    b3 = Partition([1, 2], [1, 2, 2])
    b4 = Partition([1, 1], [1, 1, 1])

    for i in range(k):
        b1 = base.tensor_product(b1)
        b2 = base.tensor_product(b2)
        b3 = base.tensor_product(b3)
        b4 = base.tensor_product(b4)

    for i in range(l):
        b1 = b1.tensor_product(base)
        b2 = b2.tensor_product(base)
        b3 = b3.tensor_product(base)
        b4 = b4.tensor_product(base)

    return Operations([[1, b1], [-1, b2], [-1, b3], [1, b4]])


class Operations:

    def __init__(self, ap):
        """
        create Operations object with a list of lists of term and partition,
        in which the elements in the inner lists are
        products and the lists in the outer list are sums
        :param ap: List[Lists[term with d, partition]]
        """
        assert (isinstance(i, list) for i in ap)
        self.partition_sum = []

        if ap == [[]]:
            self.partition_sum = []
            return

        for i, ii in ap:
            """checking types"""
            assert isinstance(ii, Partition)
            assert isinstance(i, Pow) or isinstance(i, Mul) or isinstance(i, Add) or isinstance(i, int) or isinstance(i, float) or isinstance(i, Integer) or isinstance(i, Symbol), f"wrong type = {type(i).__name__}"

            self.partition_sum += [[i, ii]]

        """simplify regarding removing zero summand and distributivity"""
        self.simplify_operation()

    def __add__(self, o):
        """
        do the sum of two elements of Operations object
        :param o: Operations object
        :return: the sum
        """
        assert isinstance(o, Operations)

        out = self.partition_sum.copy()
        """iterate over the objects lists"""
        for ii in o.partition_sum:
            for index, i in enumerate(out): # potential to do faster with f.e. dict or set
                """if a partition equals ii, only sum the terms"""
                if ii[1].is_equal(i[1]):
                    out[index] = [expand(out[index][0] + ii[0]), out[index][1]]
                    break
            else:
                """if no partition in self equals ii, just add ii to our output"""
                out += [ii]
        return Operations(out)

    def __mul__(self, o):
        """
        do the product of two elements of Operations object
        :param o: Operations object
        :return: the product
        """
        assert isinstance(o, Operations)
        out = []
        """iterate over the objects lists and do the product for each pair"""
        for i in self.partition_sum.copy():
            for ii in o.partition_sum.copy():
                """get the composition with the loop level"""
                composition, loop = i[1].composition(ii[1], True)
                """add the simplified form to the output with d^loops"""
                out += [[expand(i[0]*ii[0]*(d**loop)), composition]]

        return Operations(out)

    def __repr__(self):
        repr_to_operate = []
        for i in self.partition_sum:
            repr_to_operate.append(str([i[0], i[1].ret_tuple()]))
        return str(repr_to_operate)

    def simplify_operation(self):
        """
        Simplify term by removing zero summand and distributivity
        """
        partitions = dict()

        for i, (i1, i2) in enumerate(self.partition_sum.copy()):
            """removing zero summand"""
            if not i1:
                self.partition_sum.remove([i1, i2])
                continue
            """simplifying distributivity"""
            if i2 not in partitions:
                partitions[i2] = i1
            else:
                self.partition_sum.remove([i1, i2])
                self.partition_sum.remove([(partitions.get(i2)), i2])
                self.partition_sum.append([partitions.get(i2) + i1, i2])
                partitions[i2] = partitions.get(i2) + i1
