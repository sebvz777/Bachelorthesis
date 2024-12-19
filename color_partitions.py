from partition import Partition


def tuple_to_partition(tup):
    """
        input: tup which represents a color partition with a tuple

        output: corresponding color Partition
        """
    if isinstance(tup, ColorPartitions):
        tup = tup.ret_tuple()
    assert len(tup) == 2
    return ColorPartitions(list(tup[0][0]).copy(), list(tup[0][1]).copy(), list(tup[1][0]).copy(), list(tup[1][1]).copy())


def add_to_set_in_dict(set_dict, partition):
    """
    Add partition into a dict of size to set.
    :param set_dict: the dict from size to set
    :param partition: the partition
    :return: the new dict
    """
    assert isinstance(partition, ColorPartitions)

    add_apbs = set_dict.get(partition.size())
    add_apbs.add(partition.ret_tuple())
    set_dict[partition.size()] = add_apbs

    return set_dict


def add_to_set_in_dict_for_composition(tuple_dict_set, partition):
    """
    Add partition into the top and bottom dict from size to set
    :param tuple_dict_set: the tuple with the dicts from size to set
    :param partition: the partition
    :return:
    """

    """add right partition in first dict for top size"""
    add_apbs_top = tuple_dict_set[0].get(len(partition.partition[0]))
    add_apbs_top.add(partition.ret_tuple())
    (tuple_dict_set[0])[len(partition.partition[0])] = add_apbs_top

    """add right partition in first dict for bottom size"""
    add_apbs_bottom = tuple_dict_set[1].get(len(partition.partition[1]))
    add_apbs_bottom.add(partition.ret_tuple())
    (tuple_dict_set[1])[len(partition.partition[1])] = add_apbs_bottom

    return tuple_dict_set


def do_unary(to_unary, all_partitions, stop_whole, already_u, max_length, all_partitions_by_size, all_partitions_by_size_top_bottom):
    """
    Do all possible combinations of unary operations
    :param to_unary: partitions on which we do the unary operations
    :param all_partitions: set in which we add the newfound partitions
    :param stop_whole: False if we found new partitions
    :param already_u: partitions we already have modified with unary operations
    :param max_length: max(n, size(biggest partition))
    :param all_partitions_by_size: all partitions stored in a dict from size to set()
    :param all_partitions_by_size_top_bottom: all partitions stored in a tuple of two dicts from size top/bottom to set()
    """

    stop = False
    while not stop:
        stop = True

        to_unary_copy = to_unary.copy()

        for pp in to_unary_copy:
            assert isinstance(pp, ColorPartitions)
            pmod = ColorPartitions(pp.partition[0].copy(), pp.partition[1].copy(), pp.color_top.copy(), pp.color_bottom.copy())

            a = ColorPartitions([], [], [], [])
            """start with rotation"""

            if pmod.partition[0]:
                a = pmod.rotation(True, True)
            elif pmod.partition[1]:
                a = pmod.rotation(False, False)

            a.hash_form()

            """add to all_partitions"""
            if a.ret_tuple() not in all_partitions:
                stop_whole = False
                stop = False
                all_partitions.add(a.ret_tuple())
                to_unary.add(a)

                """call functions which adds the partition a into the right set in the dict"""
                all_partitions_by_size = add_to_set_in_dict(all_partitions_by_size, a)
                all_partitions_by_size_top_bottom = add_to_set_in_dict_for_composition(
                        all_partitions_by_size_top_bottom, a)

            """continue with involution"""
            a = pmod.involution()

            a.hash_form()

            """add to all_partitions"""
            if a.ret_tuple() not in all_partitions:
                stop_whole = False
                stop = False
                all_partitions.add(a.ret_tuple())
                to_unary.add(a)

                """call functions which adds the partition a into the right set in the dict"""
                all_partitions_by_size = add_to_set_in_dict(all_partitions_by_size, a)
                all_partitions_by_size_top_bottom = add_to_set_in_dict_for_composition(
                        all_partitions_by_size_top_bottom, a)

            assert pmod.is_equal(pp)
            """remember already unary"""
            already_u.add(pp.ret_tuple())
            to_unary.remove(pp)

    return stop_whole, all_partitions, already_u, all_partitions_by_size, all_partitions_by_size_top_bottom


def do_tensor_products(all_partitions, already_t, to_tens, stop_whole, max_length, all_partitions_by_size, all_partitions_by_size_top_bottom):
    """
    Do all possible tensor products, while not repeating old calculations
    :param all_partitions: all found partitions
    :param already_t: all pairs of partitions already tensor product
    :param to_tens: pairs of partitions to tensor product
    :param stop_whole: False if new partition found
    :param max_length: max(n, size(biggest partition))
    :parem all_partitions_by_size: for improving runtime: all_partitions ordered by size
    :param all_partitions_by_size_top_bottom: all partitions stored in a tuple of two dicts from size top/bottom to set()
    """
    """analogical to all_pyrtitions_by_size in build function for new_tens"""
    new_tens_by_size = dict()
    for i in range(max_length + 1):
        new_tens_by_size[i] = set()
    """store all partitions which are new constructed by tensor product"""
    new_tens = set()
    """store for every i the ii's which are already used, to not use them in this iteration again"""
    without = {}

    """until no more new possibilities tensor"""
    stop = False
    while not stop:
        stop = True

        """if there are new partitions due to tensor and size constraint, remove pair which are already 
        calculated """
        if new_tens:
            aa = new_tens.union(all_partitions)
            for i in aa:
                """get fitting partitions in advance (improve runtime)"""
                new_tens_temp_tensor = set()
                for key in new_tens_by_size.keys():
                    if tuple_to_partition(i).size() + int(key) <= max_length:
                        new_tens_temp_tensor = new_tens_temp_tensor.union(new_tens_by_size.get(key))
                if i in without.keys():
                    for ii in new_tens_temp_tensor.difference(without.get(i)):
                        if len(i[0][1]) + len(i[0][1]) + len(ii[0][1]) + len(ii[0][1]) <= max_length and (i, ii) not in already_t:
                            to_tens.add((i, ii))
                            already_t.add((i, ii))
                else:
                    for ii in new_tens_temp_tensor:
                        if len(i[0][1]) + len(i[0][1]) + len(ii[0][1]) + len(ii[0][1]) <= max_length and (i, ii) not in already_t:
                            to_tens.add((i, ii))
                            already_t.add((i, ii))

        """do the tensor products"""
        al = to_tens.copy()
        for (i, ii) in al:
            a = tuple_to_partition(i)
            a = a.tensor_product(tuple_to_partition(ii))
            to_tens.remove((i, ii))
            if a.ret_tuple() not in all_partitions:
                if a.size() == max_length:
                    all_partitions.add(a.ret_tuple())

                    """call function which adds the partition a into the right set in the dicts"""
                    all_partitions_by_size = add_to_set_in_dict(all_partitions_by_size, a)
                    all_partitions_by_size_top_bottom = add_to_set_in_dict_for_composition(
                        all_partitions_by_size_top_bottom, a)

                    stop_whole = False
                else:
                    all_partitions.add(a.ret_tuple())

                    """call function which adds the partition a into the right set in the dicts"""
                    all_partitions_by_size = add_to_set_in_dict(all_partitions_by_size, a)
                    all_partitions_by_size_top_bottom = add_to_set_in_dict_for_composition(
                        all_partitions_by_size_top_bottom, a)
                    new_tens_by_size = add_to_set_in_dict(new_tens_by_size, a)

                    stop_whole = False
                    new_tens.add(a.ret_tuple())
                    stop = False
            else:
                """remove not fitting candidates for further iterations"""
                if i not in without.keys():
                    without[i] = {ii}
                else:
                    without.get(i).add(ii)

    return all_partitions, already_t, stop_whole, all_partitions_by_size, all_partitions_by_size_top_bottom


def do_composition(all_partitions, already_c, stop_whole, max_length, to_comp, all_partitions_by_size, all_partitions_by_size_top_bottom):
    """
    Do all possible compositions
    :param all_partitions: all found partitions
    :param already_c: all pairs of partitions already composition
    :param to_comp: pairs of partitions to composition
    :param stop_whole: False if new partition found
    :param max_length: max(n, size(biggest partition))
    :param all_partitions_by_size: all partitions stored in a dict from size to set()
    :param all_partitions_by_size_top_bottom: all partitions stored in a tuple of two dicts from size top/bottom to set()
    """

    """add newfound partitions due comp"""
    new_comp = set()

    """new_comp stored in tuple with a dict for top and bottom size (analogical to the technique in build function)"""
    new_comp_by_size_top_bottom = (dict(), dict())
    for i in range(max_length+1):
        (new_comp_by_size_top_bottom[0])[i] = set()
        (new_comp_by_size_top_bottom[1])[i] = set()

    """store for every i the ii's which are already used, to not use them in this iteration again"""
    without = {}

    """until no more new possibilities compose"""
    stop = False
    while not stop:
        stop = True

        """if there are new partitions due to composition, remove pair which are already calculated"""
        if new_comp:
            aa = new_comp.union(all_partitions)
            for i in aa:
                """get fitting partitions in advance (improve runtime)"""
                new_comp_temp_comp = set()
                if len(i[0][0]) <= max_length:
                    new_comp_temp_comp = new_comp_by_size_top_bottom[1].get(len(i[0][0]))
                if i in without.keys():
                    for ii in new_comp_temp_comp.difference(without.get(i)):
                        if len(i[0][0]) == len(ii[0][1]) and len(i[0][0]) != 0 and len(i[0][0]) != max_length and len(i[0][1]) + len(ii[0][0]) <= max_length and tuple_to_partition(i).color_top == tuple_to_partition(ii).color_bottom:
                            to_comp.add((i, ii))
                            already_c.add((i, ii))
                        if len(ii[0][0]) == len(i[0][1]) and len(ii[0][0]) != 0 and len(ii[0][0]) != max_length and len(ii[0][1]) + len(i[0][0]) <= max_length and tuple_to_partition(ii).color_top == tuple_to_partition(i).color_bottom:
                            to_comp.add((ii, i))
                            already_c.add((ii, i))
                else:
                    for ii in new_comp_temp_comp:
                        if len(i[0][0]) == len(ii[0][1]) and len(i[0][0]) != 0 and len(i[0][0]) != max_length and len(i[0][1]) + len(ii[0][0]) <= max_length and tuple_to_partition(i).color_top == tuple_to_partition(ii).color_bottom:
                            to_comp.add((i, ii))
                            already_c.add((i, ii))
                        if len(ii[0][0]) == len(i[0][1]) and len(ii[0][0]) != 0 and len(ii[0][0]) != max_length and len(ii[0][1]) + len(i[0][0]) <= max_length and tuple_to_partition(ii).color_top == tuple_to_partition(i).color_bottom:
                            to_comp.add((ii, i))
                            already_c.add((ii, i))

        """do the compositions"""
        al = to_comp.copy()

        for (i, ii) in al:
            a = tuple_to_partition(i).composition(tuple_to_partition(ii))
            if a.ret_tuple() not in all_partitions:
                all_partitions.add(a.ret_tuple())

                """call function which adds the partition a into the right set in the dicts"""
                all_partitions_by_size = add_to_set_in_dict(all_partitions_by_size, a)
                all_partitions_by_size_top_bottom = add_to_set_in_dict_for_composition(
                    all_partitions_by_size_top_bottom, a)
                new_comp_by_size_top_bottom = add_to_set_in_dict_for_composition(new_comp_by_size_top_bottom, a)

                stop_whole = False
                new_comp.add(a.ret_tuple())
                stop = False
            else:
                """remove not fitting candidates for further iterations"""
                to_comp.remove((i, ii))
                if i not in without.keys():
                    without[i] = {ii}
                else:
                    without.get(i).add(ii)

    return all_partitions, already_c, stop_whole, all_partitions_by_size, all_partitions_by_size_top_bottom


def build(p, n):
    """
    Build all possible partitions of size n with list of partitions p
    :param p: list of partitions
    :param n: size of outcome partitions
    :return: list of all partitions size n constructed from partitions in p
    """

    assert isinstance(p, list)
    assert isinstance(n, int)

    """store all candidates found"""
    all_partitions = {ColorPartitions([1], [1], [0], [0]).ret_tuple(), ColorPartitions([1], [1], [1], [1]).ret_tuple(), ColorPartitions([1, 1], [], [0, 1], []).ret_tuple(), ColorPartitions([1, 1], [], [1, 0], []).ret_tuple(), ColorPartitions([], [], [], []).ret_tuple()}

    """all candidates stored in dict from size to partition"""
    all_partitions_by_size = dict()

    """all candidates stored in tuple with a dict for top and bottom size"""
    all_partitions_by_size_top_bottom = (dict(), dict())

    """store partitions already unary"""
    already_u = set()

    """store partitions already tensor product"""
    already_t = set()

    """store partitions already composition"""
    already_c = set()

    """end output: All partitions found of size n """
    all_partitions_of_size_n = set()

    """all candidates for unary operations"""
    to_unary = set(p.copy())

    """compare allowed expansion size with max(n, max_length)"""
    max_length = max(n, 2)

    """get max length of a partition"""
    for i in p:
        if i.size() > max_length:
            max_length = i.size()

    """define for all i <= size an empty set in which we fill the corresponding partition of size i (for tensor)"""
    for i in range(max_length+1):
        all_partitions_by_size[i] = set()

    """define for all bottom and top size an empty set in which we fill the corresponding partition"""
    for i in range(max_length+1):
        (all_partitions_by_size_top_bottom[0])[i] = set()
        (all_partitions_by_size_top_bottom[1])[i] = set()

    """add all partitions in p to all_partitions_by_size and all_partitions_by_size_top_bottom"""
    tuple_list_all_partitions = []
    for i in all_partitions:
        tuple_list_all_partitions.append(tuple_to_partition(i))
    for i in p + tuple_list_all_partitions:
        all_partitions_by_size = add_to_set_in_dict(all_partitions_by_size, i)
        all_partitions_by_size_top_bottom = add_to_set_in_dict_for_composition(all_partitions_by_size_top_bottom, i)

    """while new were found apply on them unary tensor and composition"""
    stop_whole = False
    while not stop_whole:
        stop_whole = True

        """add new found partitions in the unary operation candidate list"""
        for i in all_partitions:
            if i not in already_u:
                to_unary.add(tuple_to_partition(i))

        """fist phase: all possible combinations of unary operations"""
        stop_whole, all_partitions, already_u, all_partitions_by_size, all_partitions_by_size_top_bottom = do_unary(to_unary, all_partitions, stop_whole, already_u, max_length, all_partitions_by_size, all_partitions_by_size_top_bottom)

        """store pairs that are candidates to get tensor product"""
        to_tens = set()

        """get all pairs to tensor"""
        for i in all_partitions:
            """get fitting partitions in advance (improve runtime)"""
            all_partitions_temp_tensor = set()
            for key in all_partitions_by_size.keys():
                if tuple_to_partition(i).size() + int(key) <= max_length:
                    all_partitions_temp_tensor = all_partitions_temp_tensor.union(all_partitions_by_size.get(key))
            for ii in all_partitions_temp_tensor:
                if (i, ii) not in already_t:
                    if len(i[0][0]) + len(i[0][1]) + len(ii[0][0]) + len(ii[0][1]) <= max_length:
                        to_tens.add((i, ii))
                        already_t.add((i, ii))

        """second phase: all possible tensor product operations which aren't redundant (don't do tensor products 
        twice) """
        all_partitions, already_t, stop_whole, all_partitions_by_size, all_partitions_by_size_top_bottom = do_tensor_products(all_partitions, already_t, to_tens, stop_whole, max_length, all_partitions_by_size, all_partitions_by_size_top_bottom)

        """add new variations by tensor product or composition with all others"""
        to_comp = set()

        """get all pairs to compose"""
        for i in all_partitions:
            """get in advance the right second candidate (regarding format)"""
            all_partitions_temp_comp = all_partitions_by_size_top_bottom[1].get(len(i[0][0]))
            for ii in all_partitions_temp_comp:
                if (i, ii) not in already_c:
                    if len(i[0][0]) == len(ii[0][1]) and len(i[0][0]) != 0 and len(i[0][0]) != max_length and len(i[0][1]) + len(ii[0][0]) <= max_length and tuple_to_partition(i).color_top == tuple_to_partition(ii).color_bottom:
                        to_comp.add((i, ii))
                        already_c.add((i, ii))

        """third phase: all possible compositions which aren't redundant (don't do tensor products twice)"""
        all_partitions, already_c, stop_whole, all_partitions_by_size, all_partitions_by_size_top_bottom = do_composition(all_partitions, already_c, stop_whole, max_length, to_comp, all_partitions_by_size, all_partitions_by_size_top_bottom)

    """remove all partitions without size n"""
    for i in all_partitions:
        if tuple_to_partition(i).size() == n:
            if i not in all_partitions_of_size_n:
                all_partitions_of_size_n.add(i)

    """format every tuple to partition and return"""

    partitions = []
    for i in all_partitions_of_size_n:
        partitions.append(tuple_to_partition(i))

    return partitions


class ColorPartitions(Partition):

    def __init__(self, top, bottom, color_top, color_bottom):
        """
        Initialize colored partition
        :param top: Upper points of partition as list
        :param bottom: Lower points of partition as list
        :param color_top: Color of upper points of Partition in {0,1} as list
        :param color_bottom: Color of lower points of Partition in {0,1} as list
        """

        super().__init__(top, bottom)

        self.color_top = color_top
        self.color_bottom = color_bottom

    def tensor_product(self, x: "ColorPartitions"):
        """
        Tensor product with colored partitions
        """

        p = super().tensor_product(Partition(x.partition[0], x.partition[1]))

        return ColorPartitions(p.partition[0], p.partition[1], self.color_top + x.color_top, self.color_bottom + x.color_bottom)

    def involution(self):
        """
        Involution with colored partitions
        """
        p = super().involution()

        return ColorPartitions(p.partition[0], p.partition[1], self.color_bottom.copy(), self.color_top.copy())

    def composition(self, q: "ColorPartitions", loop=False):
        """
        Composition with colored partition. Check whether format fits first.
        """
        assert q.color_bottom == self.color_top, f"invalid format: violation of colors"

        p = super().composition(Partition(q.partition[0], q.partition[1]), loop)

        return ColorPartitions(p.partition[0], p.partition[1], q.color_top, self.color_bottom)

    def rotation(self, lr: bool, top: bool):
        """
            input: lr whether left (true) or right (false)
                    top whether top (true) or bottom (false) rotation

            Changes self regarding operation
            """
        if top:
            assert self.partition[0], f"Got no partition reaching top"
        if not top:
            assert self.partition[1], f"Got no partition reaching bottom"

        ret = ColorPartitions(self.partition[0].copy(), self.partition[1].copy(), self.color_top.copy(), self.color_bottom.copy())

        if lr:
            if top:
                a = ret.partition[0][0]
                del ret.partition[0][0]
                ret.partition[1] = [a] + ret.partition[1]

                a = ret.color_top[0]
                del ret.color_top[0]
                ret.color_bottom = [int(not bool(a))] + ret.color_bottom
            else:
                a = ret.partition[1][0]
                del ret.partition[1][0]
                ret.partition[0] = [a] + ret.partition[0]

                a = ret.color_bottom[0]
                del ret.color_bottom[0]
                ret.color_top = [int(not bool(a))] + ret.color_top

        else:
            if top:
                a = ret.partition[0][-1]
                del ret.partition[0][-1]
                ret.partition[1].append(a)

                a = ret.color_top[-1]
                del ret.color_top[-1]
                ret.color_bottom.append(int(not bool(a)))
            else:
                a = ret.partition[1][-1]
                del ret.partition[1][-1]
                ret.partition[0].append(a)

                a = ret.color_bottom[-1]
                del ret.color_bottom[-1]
                ret.color_top.append(int(not bool(a)))

        return ret

    def hash_form(self):
        """
        Analogical to hash_form() for partitions
        """
        p = Partition(self.partition[0], self.partition[1])

        p.hash_form()
        self.partition = p.partition

    def ret_tuple(self):
        """
        Return a tuple form of a colored partition to be hashable
        """
        return tuple([super().ret_tuple(), tuple([tuple(self.color_top), tuple(self.color_bottom)])])

    def __repr__(self):
        """
        Return string presentation of colored partition
        """
        upper = []
        for i in range(len(self.partition[0])):
            upper.append([self.partition[0][i], self.color_top[i]])

        lower = []
        for i in range(len(self.partition[1])):
            lower.append([self.partition[1][i], self.color_bottom[i]])

        return f"[{upper} \n {lower}]"

    def __eq__(self, other: "ColorPartitions"):
        """
        Check whether two colored partitions are equal
        """
        return super().__eq__(other) and other.color_bottom == self.color_bottom and other.color_top == self.color_top

    def __hash__(self):
        """
        Transform colored partition in hashable form
        """
        self.hash_form()
        return hash(self.ret_tuple())


if __name__ == "__main__":

    aa = ColorPartitions([2, 2, 3], [2, 2, 2], [1, 0, 1], [1, 1, 0])

    b = ColorPartitions([1, 2, 3], [2, 2, 2], [1, 0, 1], [1, 0, 1])

    print(len(build([ColorPartitions([1], [1], [1], [0])], 6)))
