import typing
import itertools


def tuple_to_partition(tup):
    """
        input: tup which represents a partition with a tuple

        output: corresponding Partition
        """
    if isinstance(tup, Partition):
        tup = tup.ret_tuple()
    assert len(tup) == 2
    return Partition(list(tup[0]).copy(), list(tup[1]).copy())


def add_to_set_in_dict(set_dict, partition):
    """
    Add partition into a dict of size to set.
    :param set_dict: the dict from size to set
    :param partition: the partition
    :return: the new dict
    """
    assert isinstance(partition, Partition)

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
            assert isinstance(pp, Partition)
            pmod = Partition(pp.partition[0].copy(), pp.partition[1].copy())

            a = Partition([], [])
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

            """end with involution y-axis"""
            a = pmod.involution_yaxis()
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


def do_unary2(to_unary, all_partitions, stop_whole, already_u, max_length, all_partitions_by_size, all_partitions_by_size_top_bottom):
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

    """0 as nothing, 1 as rotation, 2 as involution-x, 3 as involution-y, -1 as filler"""
    options = [1, 2, 3, -1]
    """for option combinations"""
    comb = set()

    for pp in to_unary:
        assert isinstance(pp, Partition)

        """generate all combinations of options length <= size(partition)"""
        for i in itertools.product(options, repeat=max_length):
            rot, invx, invy = list(i).count(1), list(i).count(2), list(i).count(3)
            if rot < pp.size() and invx <= 1 and invy <= 1:
                comb.add(i)
        pmod = Partition(pp.partition[0].copy(), pp.partition[1].copy())

        """ally generated options"""
        for i in comb:
            for ii in i:
                if ii == -1:
                    continue
                elif ii == 1:
                    if pmod.partition[0]:
                        pmod = pmod.rotation(True, True)
                    elif pmod.partition[1]:
                        pmod = pmod.rotation(True, False)
                elif ii == 2:
                    pmod = pmod.involution()
                elif ii == 3:
                    pmod = pmod.involution_yaxis()
            pmod.hash_form()

            """add to all_partitions"""
            if pmod.ret_tuple() not in all_partitions:
                stop_whole = False
                all_partitions.add(pmod.ret_tuple())

                """call functions which adds the partition a into the right set in the dict"""
                all_partitions_by_size = add_to_set_in_dict(all_partitions_by_size, pmod)
                all_partitions_by_size_top_bottom = add_to_set_in_dict_for_composition(all_partitions_by_size_top_bottom, pmod)

        """remember already unary"""
        already_u.add(pp.ret_tuple())
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
                        if len(i[0]) + len(i[1]) + len(ii[0]) + len(ii[1]) <= max_length and (i, ii) not in already_t:
                            to_tens.add((i, ii))
                            already_t.add((i, ii))
                else:
                    for ii in new_tens_temp_tensor:
                        if len(i[0]) + len(i[1]) + len(ii[0]) + len(ii[1]) <= max_length and (i, ii) not in already_t:
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
                if len(i[0]) <= max_length:
                    new_comp_temp_comp = new_comp_by_size_top_bottom[1].get(len(i[0]))
                if i in without.keys():
                    for ii in new_comp_temp_comp.difference(without.get(i)):
                        if len(i[0]) == len(ii[1]) and len(i[0]) != 0 and len(i[0]) != max_length and len(i[1]) + len(ii[0]) <= max_length:
                            to_comp.add((i, ii))
                            already_c.add((i, ii))
                        if len(ii[0]) == len(i[1]) and len(ii[0]) != 0 and len(ii[0]) != max_length and len(ii[1]) + len(i[0]) <= max_length:
                            to_comp.add((ii, i))
                            already_c.add((ii, i))
                else:
                    for ii in new_comp_temp_comp:
                        if len(i[0]) == len(ii[1]) and len(i[0]) != 0 and len(i[0]) != max_length and len(i[1]) + len(ii[0]) <= max_length:
                            to_comp.add((i, ii))
                            already_c.add((i, ii))
                        if len(ii[0]) == len(i[1]) and len(ii[0]) != 0 and len(ii[0]) != max_length and len(ii[1]) + len(i[0]) <= max_length:
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
    all_partitions = {Partition([1, 1], []).ret_tuple(), Partition([1], [1]).ret_tuple()}

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
    max_length = n

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
                    if len(i[0]) + len(i[1]) + len(ii[0]) + len(ii[1]) <= max_length:
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
            all_partitions_temp_comp = all_partitions_by_size_top_bottom[1].get(len(i[0]))
            for ii in all_partitions_temp_comp:
                if (i, ii) not in already_c:
                    if len(i[0]) == len(ii[1]) and len(i[0]) != 0 and len(i[0]) != max_length and len(i[1]) + len(ii[0]) <= max_length:
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


class Partition:

    def __init__(self, top: typing.List, bottom: typing.List):
        """
        :param top: Upper points of partitions as list
        :param bottom: Lower points of partition as list
        """
        assert (isinstance(top, typing.List)), f"invalid type: got {type(top).__name__} but needed List"
        assert (isinstance(bottom, typing.List)), f"invalid type: got {type(top).__name__} but needed List"

        self.partition = [top, bottom]

    def helper_new_id_values(self, x: "Partition") -> "Partition":
        """
            input: x as Partition
            output: x as Partition which is equal but has new id's

            Output a semantically identical Partition which has new number values.
            """

        assert isinstance(x, Partition), f"invalid type: got {type(x).__name__} but needed Partition"

        x = Partition(x.partition[0].copy(), x.partition[1].copy())
        top_bottom = self.partition[0].copy() + self.partition[1].copy()

        if top_bottom:
            new_id = max(list(set(top_bottom))) + 1
        else:
            new_id = 1

        partitions_x = list(set(x.partition[0].copy() + x.partition[1].copy()))
        new_ids = dict()

        for n in partitions_x:
            new_ids[n] = new_id
            new_id += 1

        for i, n in enumerate(x.partition[0]):
            x.partition[0][i] = new_ids.get(n)

        for i, n in enumerate(x.partition[1]):
            x.partition[1][i] = new_ids.get(n)

        return x

    def hash_form(self):
        """
            input: x as Partition
            output: x as Partition which is equal but has new id's

            Output a semantically identical Partition which has new number values from 1 to number of Partitions
            """
        new_id = 1
        new_ids = dict()
        self.partition = Partition([len(self.partition[0]) + len(self.partition[1])], []).helper_new_id_values(self).partition

        for i, n in enumerate(self.partition[0]):
            if self.partition[0][i] not in new_ids:
                new_ids[self.partition[0][i]] = new_id
                self.partition[0][i] = new_id
                new_id += 1
            else:
                self.partition[0][i] = new_ids.get(self.partition[0][i])
        for i, n in enumerate(self.partition[1]):
            if self.partition[1][i] not in new_ids:
                new_ids[self.partition[1][i]] = new_id
                self.partition[1][i] = new_id
                new_id += 1
            else:
                self.partition[1][i] = new_ids.get(self.partition[1][i])

    def tensor_product(self, x: "Partition"):
        """
            Apply on self tensor product with x
            :param x: Partition
            :return: Solution of tensor product of self and x
            """
        ret = Partition(self.partition[0].copy(), self.partition[1].copy())
        a = ret.helper_new_id_values(x)
        ret.partition[0] += a.partition[0]
        ret.partition[1] += a.partition[1]
        ret.hash_form()

        return ret

    def involution(self):
        """
            involute self regarding x-axis
            :return: Solution of involution of self
            """
        ret = Partition(self.partition[0].copy(), self.partition[1].copy())
        p0 = ret.partition[0]
        ret.partition[0] = ret.partition[1]
        ret.partition[1] = p0
        self.hash_form()

        return ret

    def involution_yaxis(self):
        """
            involute self regarding y-axis
            :return: solution of y-axis involution of self
            """
        ret = Partition(self.partition[0].copy(), self.partition[1].copy())
        ret.partition[0] = list(reversed(ret.partition[0]))
        ret.partition[1] = list(reversed(ret.partition[1]))
        ret.hash_form()

        return ret

    def rotation(self, lr: bool, top: bool, hash_form=True):
        """
            input: lr whether left (true) or right (false)
                    top whether top (true) or bottom (false) rotation

            Changes self regarding operation
            """
        if top:
            assert self.partition[0], f"Got no partition reaching top"
        if not top:
            assert self.partition[1], f"Got no partition reaching bottom"

        ret = Partition(self.partition[0].copy(), self.partition[1].copy())

        if lr:
            if top:
                a = ret.partition[0][0]
                del ret.partition[0][0]
                ret.partition[1] = [a] + ret.partition[1]
            else:
                a = ret.partition[1][0]
                del ret.partition[1][0]
                ret.partition[0] = [a] + ret.partition[0]
        else:
            if top:
                a = ret.partition[0][-1]
                del ret.partition[0][-1]
                ret.partition[1].append(a)
            else:
                a = ret.partition[1][-1]
                del ret.partition[1][-1]
                ret.partition[0].append(a)
        if hash_form:
            ret.hash_form()
        return ret

    def composition(self, q: "Partition", loop=False):
        assert isinstance(q, Partition), f"invalid type: got {type(q).__name__} but needed Partition"
        assert len(self.partition[0]) == len(q.partition[1]), "format not fitting"

        """work with copies to not change the main partition"""
        self_copy = Partition(self.partition[0].copy(), self.partition[1].copy())

        """new_ids dicts store the new Value we need to assign to the partition in order to connect new segments"""
        q_copy_new_ids = self_copy.helper_new_id_values(q).partition
        self_copy = self_copy.partition
        new_ids = dict()

        """fitting the second partition-values to the first and changing if connection"""
        for i, n in enumerate(q_copy_new_ids[1]):

            if n not in new_ids:

                new_ids[n] = self.partition[0][i]
            else:

                if self.partition[0][i] in new_ids and new_ids.get(n) in new_ids:

                    """Do path compression if we have the case that we need to merge two tree's together and
                    the nodes we operate on are not a root or a leaf"""
                    for ii in [n]:
                        path = [ii]
                        already_in = set()
                        already_in.add(new_ids.get(ii))
                        z = new_ids.get(ii)
                        while z in new_ids:
                            path.append(z)
                            already_in.add(z)
                            z = new_ids.get(z)
                            if z in already_in:
                                break
                        path.append(z)
                        for nn in path[:-1]:
                            new_ids[nn] = path[-1]
                    new_ids[new_ids.get(n)] = self.partition[0][i]
                else:
                    if new_ids.get(n) not in new_ids:
                        new_ids[new_ids.get(n)] = self.partition[0][i]
                    else:
                        new_ids[self.partition[0][i]] = new_ids.get(n)

        """Path compression"""
        for ii in new_ids.keys():
            path = [ii]
            already_in = set()
            already_in.add(new_ids.get(ii))
            z = new_ids.get(ii)
            while z in new_ids:
                path.append(z)
                already_in.add(z)
                z = new_ids.get(z)
                if z in already_in:
                    break
            path.append(z)
            for nn in path[:-1]:
                new_ids[nn] = path[-1]

        """giving the top part new values"""
        for i, n in enumerate(q_copy_new_ids[0]):
            if n in new_ids:
                q_copy_new_ids[0][i] = new_ids.get(n)

        """giving the bottom part new values"""
        for i, n in enumerate(self.partition[1]):
            if n in new_ids:
                self_copy[1][i] = new_ids.get(n)

        """removing the middle by just changing the top of our partition to the adjusted top of the second partition"""
        ret = Partition(q_copy_new_ids[0], self_copy[1])
        ret.hash_form()

        """calculating removed related components (loop)"""
        if loop:
            related_comp = set()
            return_partition_as_set = set(q_copy_new_ids[0] + self_copy[1])

            """calculate new ids for middle nodes, which are under normal circumstances omitted"""
            for i, n in enumerate(q_copy_new_ids[1]):
                if n in new_ids:
                    q_copy_new_ids[1][i] = new_ids.get(n)

            for i, n in enumerate(self.partition[0]):
                if n in new_ids:
                    self_copy[0][i] = new_ids.get(n)

            """if there is a ID in the middle part which is not in result partition set we know, that this is a loop"""
            for co in q_copy_new_ids[1]+self_copy[0]:
                if co not in return_partition_as_set:
                    related_comp.add(co)

            return ret, len(related_comp)

        return ret

    def is_equal(self, q: "Partition") -> bool:
        assert isinstance(q, Partition), f"invalid type: got {type(q).__name__} but needed Partition"

        self.hash_form()
        q.hash_form()

        """compare top and bottom"""
        return self.partition[0] == q.partition[0] and self.partition[1] == q.partition[1]

    def size(self):
        """
            Output: Size of self (regarding nodes)
            """
        return len(self.partition[0] + self.partition[1])

    def ret_tuple(self):
        """
            Output: tuple form of self to be able to get hashed
            """
        return tuple([tuple(self.partition[0].copy()), tuple(self.partition[1].copy())])

    def __repr__(self):
        return f"[{self.partition[0]} \n {self.partition[1]}]"

    def __eq__(self, q: "Partition") -> bool:
        assert isinstance(q, Partition), f"invalid type: got {type(q).__name__} but needed Partition"

        self.hash_form()
        q.hash_form()

        """compare top and bottom"""
        return self.partition[0] == q.partition[0] and self.partition[1] == q.partition[1]

    def __hash__(self):
        self.hash_form()
        return hash(tuple([tuple(self.partition[0].copy()), tuple(self.partition[1].copy())]))


if __name__ == "__main__":

    print(len(build([], 10)))
