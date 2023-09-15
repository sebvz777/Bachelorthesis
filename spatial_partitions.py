import math

import partition
from partition import *

import typing


def tuple_to_partition(tup):
    """
        input: tup which represents a color partition with a tuple

        output: corresponding color Partition
        """
    if isinstance(tup, SpatialPartitions):
        tup = tup.ret_tuple()
    assert len(tup) == 2
    upper = []
    for i in tup[0]:
        upper.append(list(i))
    lower = []
    for i in tup[1]:
        lower.append(list(i))

    return SpatialPartitions(upper, lower)


def add_to_set_in_dict(set_dict, partition):
    """
    Add partition into a dict of size to set.
    :param set_dict: the dict from size to set
    :param partition: the partition
    :return: the new dict
    """
    assert isinstance(partition, SpatialPartitions)

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

    size_top = (0, 0)

    if partition.partition[0]:
        size_top = (len(partition.partition[0]), 0)
        size_top = (size_top[0], len(partition.partition[0][0]))

    """add right partition in first dict for top size"""
    add_apbs_top = tuple_dict_set[0].get(size_top)
    add_apbs_top.add(partition.ret_tuple())
    (tuple_dict_set[0])[size_top] = add_apbs_top

    size_bottom = (0, 0)

    if partition.partition[1]:
        size_bottom = (len(partition.partition[1]), 0)
        size_bottom = (size_bottom[0], len(partition.partition[1][0]))

    """add right partition in first dict for bottom size"""
    add_apbs_bottom = tuple_dict_set[1].get(size_bottom)
    add_apbs_bottom.add(partition.ret_tuple())
    (tuple_dict_set[1])[size_bottom] = add_apbs_bottom

    return tuple_dict_set


def get_trace(trace, start):
    """track the trace with breath first search"""

    if start not in trace:
        print(f"Partition {start} not found in trace")

    track = [start]
    for p in track:
        if p in trace:
            print(p, " : ", trace.get(p))
            for i in trace.get(p)[0]:
                if i not in track:
                    track.append(i)


def do_unary(to_unary, all_partitions, stop_whole, already_u, max_length, all_partitions_by_size, all_partitions_by_size_top_bottom, trace):
    """
    Do all possible combinations of unary operations
    :param to_unary: partitions on which we do the unary operations
    :param all_partitions: set in which we add the newfound partitions
    :param stop_whole: False if we found new partitions
    :param already_u: partitions we already have modified with unary operations
    :param max_length: max(n, size(biggest partition))
    :param all_partitions_by_size: all partitions stored in a dict from size to set()
    :param all_partitions_by_size_top_bottom: all partitions stored in a tuple of two dicts from size top/bottom to set()
    :param optional trace: if trace is activated store traces
    """

    stop = False
    while not stop:
        stop = True

        to_unary_copy = to_unary.copy()

        for pp in to_unary_copy:
            assert isinstance(pp, SpatialPartitions)
            pmod = SpatialPartitions(pp.partition[0].copy(), pp.partition[1].copy())

            """involution"""
            a = pmod.involution()
            a.hash_form()

            """add to all_partitions and optional trace"""
            if a.ret_tuple() not in all_partitions:
                trace[a.ret_tuple()] = tuple([tuple([pmod.ret_tuple(), "i"])])
                stop_whole = False
                stop = False
                all_partitions.add(a.ret_tuple())
                to_unary.add(a)

                """call functions which adds the partition a into the right set in the dict"""
                all_partitions_by_size = add_to_set_in_dict(all_partitions_by_size, a)
                all_partitions_by_size_top_bottom = add_to_set_in_dict_for_composition(
                        all_partitions_by_size_top_bottom, a)

            """remember already unary"""
            already_u.add(pp.ret_tuple())
            to_unary.remove(pp)

    return stop_whole, all_partitions, already_u, all_partitions_by_size, all_partitions_by_size_top_bottom, trace


def do_tensor_products(all_partitions, already_t, to_tens, stop_whole, max_length, all_partitions_by_size, all_partitions_by_size_top_bottom, trace):
    """
    Do all possible tensor products, while not repeating old calculations
    :param all_partitions: all found partitions
    :param already_t: all pairs of partitions already tensor product
    :param to_tens: pairs of partitions to tensor product
    :param stop_whole: False if new partition found
    :param max_length: max(n, size(biggest partition))
    :parem all_partitions_by_size: for improving runtime: all_partitions ordered by size
    :param all_partitions_by_size_top_bottom: all partitions stored in a tuple of two dicts from size top/bottom to set()
    :param optional trace: if trace is activated store traces
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
                        if tuple_to_partition(i).size() + tuple_to_partition(ii).size() <= max_length and (i, ii) not in already_t:
                            to_tens.add((i, ii))
                            already_t.add((i, ii))
                else:
                    for ii in new_tens_temp_tensor:
                        if tuple_to_partition(i).size() + tuple_to_partition(ii).size() <= max_length and (i, ii) not in already_t:
                            to_tens.add((i, ii))
                            already_t.add((i, ii))

        """do the tensor products"""
        al = to_tens.copy()
        for (i, ii) in al:
            a = tuple_to_partition(i)
            b = tuple_to_partition(ii)
            if a.get_dimension() == b.get_dimension():
                a = a.tensor_product(b)
            to_tens.remove((i, ii))
            if a.ret_tuple() not in all_partitions:
                trace[a.ret_tuple()] = ((i, ii), "t")
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

    return all_partitions, already_t, stop_whole, all_partitions_by_size, all_partitions_by_size_top_bottom, trace


def do_composition(all_partitions, already_c, stop_whole, max_length, to_comp, all_partitions_by_size, all_partitions_by_size_top_bottom, trace):
    """
    Do all possible compositions
    :param all_partitions: all found partitions
    :param already_c: all pairs of partitions already composition
    :param to_comp: pairs of partitions to composition
    :param stop_whole: False if new partition found
    :param max_length: max(n, size(biggest partition))
    :param all_partitions_by_size: all partitions stored in a dict from size to set()
    :param all_partitions_by_size_top_bottom: all partitions stored in a tuple of two dicts from size top/bottom to set()
    :param optional trace: if trace is activated store traces
    """

    """add newfound partitions due comp"""
    new_comp = set()

    """new_comp stored in tuple with a dict for top and bottom size (analogical to the technique in build function)"""
    new_comp_by_size_top_bottom = (dict(), dict())
    for i in range(max_length+1):
        for ii in range(max_length+1):
            (new_comp_by_size_top_bottom[0])[(i, ii)] = set()
            (new_comp_by_size_top_bottom[1])[(i, ii)] = set()

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
                    size_comp = (0, 0)
                    if i[0]:
                        size_comp = (len(i[0]), len(i[0][0]))
                    new_comp_temp_comp = new_comp_by_size_top_bottom[1].get(size_comp)
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
            a = tuple_to_partition(i)
            if tuple_to_partition(i).get_dimension() == tuple_to_partition(ii).get_dimension():
                a = tuple_to_partition(i).composition(tuple_to_partition(ii))
            if a.ret_tuple() not in all_partitions and a.size() <= max_length:
                trace[a.ret_tuple()] = ((i, ii), "c")
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

    return all_partitions, already_c, stop_whole, all_partitions_by_size, all_partitions_by_size_top_bottom, trace


def build(p, n, tracing=False, max_artificial=0):
    """
    Build all possible partitions of size n with list of partitions p
    :param p: list of partitions
    :param n: size of outcome partitions
    :param tracing: outputs also trace of every partition
    :param max_artificial > 0 if we need to increase the extinction
    :return: list of all partitions size n constructed from partitions in p
    """

    assert isinstance(p, list)
    assert isinstance(n, int)

    """store all candidates found + base partitions to m = 3"""
    all_partitions = set()
    dim = 0
    if p:
        dim = p[0].get_dimension()
        for i in p:
            assert i.get_dimension() == dim, "all input partitions need same dimension"

    all_partitions.add(SpatialPartitions([list(range(1, dim+1))], [list(range(1, dim+1))]).ret_tuple())
    all_partitions.add(SpatialPartitions([], [list(range(1, dim+1)), list(range(1, dim+1))]).ret_tuple())

    """trace dictionary"""
    trace = dict()

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

    if max_artificial:
        max_length = max(max_length, max_artificial)

    """define for all i <= size an empty set in which we fill the corresponding partition of size i (for tensor)"""
    for i in range(max_length+1):
        all_partitions_by_size[i] = set()

    """define for all bottom and top size an empty set in which we fill the corresponding partition"""
    for i in range(max_length+1):
        for ii in range(max_length+1):
            (all_partitions_by_size_top_bottom[0])[(i, ii)] = set()
            (all_partitions_by_size_top_bottom[1])[(i, ii)] = set()

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
        stop_whole, all_partitions, already_u, all_partitions_by_size, all_partitions_by_size_top_bottom, trace = do_unary(to_unary, all_partitions, stop_whole, already_u, max_length, all_partitions_by_size, all_partitions_by_size_top_bottom, trace)

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
                    if tuple_to_partition(i).size() + tuple_to_partition(ii).size() <= max_length:
                        to_tens.add((i, ii))
                        already_t.add((i, ii))

        """second phase: all possible tensor product operations which aren't redundant (don't do tensor products 
        twice) """
        all_partitions, already_t, stop_whole, all_partitions_by_size, all_partitions_by_size_top_bottom, trace = do_tensor_products(all_partitions, already_t, to_tens, stop_whole, max_length, all_partitions_by_size, all_partitions_by_size_top_bottom, trace)

        """add new variations by tensor product or composition with all others"""
        to_comp = set()

        """get all pairs to compose"""
        for i in all_partitions:
            """get in advance the right second candidate (regarding format)"""
            size_comp = (0, 0)
            if i[0]:
                size_comp = (len(i[0]), len(i[0][0]))
            all_partitions_temp_comp = all_partitions_by_size_top_bottom[1].get(size_comp)
            for ii in all_partitions_temp_comp:
                if (i, ii) not in already_c:
                    if len(i[0]) == len(ii[1]) and len(i[0]) != 0 and len(i[0]) != max_length and len(i[1]) + len(ii[0]) <= max_length:
                        to_comp.add((i, ii))
                        already_c.add((i, ii))

        """third phase: all possible compositions which aren't redundant (don't do tensor products twice)"""
        all_partitions, already_c, stop_whole, all_partitions_by_size, all_partitions_by_size_top_bottom, trace = do_composition(all_partitions, already_c, stop_whole, max_length, to_comp, all_partitions_by_size, all_partitions_by_size_top_bottom, trace)

    """remove all partitions without size n"""
    for i in all_partitions:
        #if tuple_to_partition(i).size() == n:
        #if i not in all_partitions_of_size_n:
        all_partitions_of_size_n.add(i)

    """format every tuple to partition and return"""

    partitions = []
    for i in all_partitions_of_size_n:
        partitions.append(tuple_to_partition(i))

    if tracing:
        return partitions, trace

    return partitions


class SpatialPartitions:

    def __init__(self, top: typing.List, bottom: typing.List):
        """
        :param top: Upper points of partitions as list of lists
        :param bottom: Lower points of partition as list of lists
        """
        assert (isinstance(top, typing.List)), f"invalid type: got {type(top).__name__} but needed List"
        assert (isinstance(bottom, typing.List)), f"invalid type: got {type(top).__name__} but needed List"

        self.partition = [top, bottom]

    def tensor_product(self, x: "SpatialPartitions"):
        """
            Apply on self tensor product with x
            :param x: SpatialPartition
            :return: Solution of tensor product of self and x
            """
        assert self.get_dimension() == x.get_dimension(), "partitions need to have same dimension m"
        ret = SpatialPartitions(self.partition[0].copy(), self.partition[1].copy())
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
        ret = SpatialPartitions(self.partition[0].copy(), self.partition[1].copy())
        p0 = ret.partition[0]
        ret.partition[0] = ret.partition[1]
        ret.partition[1] = p0
        ret.hash_form()
        return ret

    def composition(self, q: "SpatialPartitions"):
        assert isinstance(q, SpatialPartitions), f"invalid type: got {type(q).__name__} but needed Partition"
        assert len(self.partition[0]) == len(q.partition[1]), "format not fitting"

        """work with copies to not change the main partition"""
        self_copy = SpatialPartitions(self.partition[0].copy(), self.partition[1].copy())

        """new_ids dicts store the new Value we need to assign to the partition in order to connect new segments"""
        q_copy_new_ids = self_copy.helper_new_id_values(q).partition
        self_copy = self_copy.partition
        new_ids = dict()

        """fitting the second partition-values to the first and changing if connection"""
        for i, n in enumerate(q_copy_new_ids[1]):
            for inner_i, inner_n in enumerate(n):
                if inner_n not in new_ids:

                    new_ids[inner_n] = self.partition[0][i][inner_i]
                else:
                    if self.partition[0][i][inner_i] in new_ids and new_ids.get(inner_n) in new_ids:
                        """Do path compression if we have the case that we need to merge two tree's together and
                        the nodes we operate on are not a root or a leaf"""

                        for ii in [inner_n]:
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
                        new_ids[new_ids.get(inner_n)] = self.partition[0][i][inner_i]
                    else:
                        if new_ids.get(inner_n) not in new_ids:
                            new_ids[new_ids.get(inner_n)] = self.partition[0][i][inner_i]
                        else:
                            new_ids[self.partition[0][i][inner_i]] = new_ids.get(inner_n)

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
            for ii, nn in enumerate(n):
                if nn in new_ids:
                    q_copy_new_ids[0][i][ii] = new_ids.get(nn)

        """giving the bottom part new values"""
        for i, n in enumerate(self.partition[1]):
            for ii, nn in enumerate(n):
                if nn in new_ids:
                    self_copy[1][i][ii] = new_ids.get(nn)

        """removing the middle by just changing the top of our partition to the adjusted top of the second partition"""
        ret = SpatialPartitions(q_copy_new_ids[0], self_copy[1])
        ret.hash_form()

        return ret

    def hash_form(self):
        """
            input: x as SpatialPartition
            output: x as SpatialPartition which is equal but has new id's

            Output a semantically identical Partition which has new number values from 1 to number of Partitions
            """
        new_id = 1
        new_ids = dict()
        self.partition = SpatialPartitions([[len(self.partition[0]) + len(self.partition[1])]], []).helper_new_id_values(self).partition

        for i, n in enumerate(self.partition[0]):
            for ii, nn in enumerate(n):
                if self.partition[0][i][ii] not in new_ids:
                    new_ids[self.partition[0][i][ii]] = new_id
                    self.partition[0][i][ii] = new_id
                    new_id += 1
                else:
                    self.partition[0][i][ii] = new_ids.get(self.partition[0][i][ii])
        for i, n in enumerate(self.partition[1]):
            for ii, nn in enumerate(n):
                if self.partition[1][i][ii] not in new_ids:
                    new_ids[self.partition[1][i][ii]] = new_id
                    self.partition[1][i][ii] = new_id
                    new_id += 1
                else:
                    self.partition[1][i][ii] = new_ids.get(self.partition[1][i][ii])

    def helper_new_id_values(self, x: "SpatialPartitions") -> "SpatialPartitions":
        """
            input: x as Partition
            output: x as Partition which is equal but has new id's

            Output a semantically identical Partition which has new number values.
            """

        assert isinstance(x, SpatialPartitions), f"invalid type: got {type(x).__name__} but needed Partition"

        x = SpatialPartitions(x.partition[0].copy(), x.partition[1].copy())

        top_bottom = []

        for i in self.partition[0].copy() + self.partition[1].copy():
            for ii in i:
                top_bottom.append(ii)

        if top_bottom:
            new_id = max(list(set(top_bottom))) + 1
        else:
            new_id = 1

        partitions_x = []

        for i in x.partition[0].copy() + x.partition[1].copy():
            for ii in i:
                partitions_x.append(ii)

        new_ids = dict()

        for n in set(partitions_x):
            new_ids[n] = new_id
            new_id += 1

        for i, n in enumerate(x.partition[0]):
            for ii, nn in enumerate(n):
                x.partition[0][i][ii] = new_ids.get(nn)

        for i, n in enumerate(x.partition[1]):
            for ii, nn in enumerate(n):
                x.partition[1][i][ii] = new_ids.get(nn)

        return x

    def ret_tuple(self):

        tup_top = []

        for i in self.partition[0]:
            tup_top.append(tuple(i))

        tup_bottom = []

        for i in self.partition[1]:
            tup_bottom.append(tuple(i))

        return tuple([tuple(tup_top), tuple(tup_bottom)])

    def size(self):
        size = 0
        for i in self.partition[0] + self.partition[1]:
            size += len(i)
        return size

    def get_dimension(self):

        if self.partition[0]:
            for i in self.partition[0]:
                if i:
                    return len(i)
        elif self.partition[1]:
            for i in self.partition[1]:
                if i:
                    return len(i)
        return 0

    def check_same_dim(self):
        a = Partition([i[0] for i in self.partition[0]], [i[0] for i in self.partition[1]])
        for ii in range(self.get_dimension()):
            if not a.is_equal(Partition([i[ii] for i in self.partition[0]], [i[ii] for i in self.partition[1]])):
                return False
        return True

    def __eq__(self, other: "SpatialPartitions"):
        """
        Check whether two spatial partitions are equal
        """
        self.hash_form()
        other.hash_form()
        return self.partition == other.partition

    def __hash__(self):
        """
        Transform spatial partition in hashable form
        """
        self.hash_form()
        return hash(self.ret_tuple())


if __name__ == "__main__":
    pass
    """example of 4.12.2. plus you have to remove base partitions"""
    """a = SpatialPartitions([], [[1, 1]])
    b = SpatialPartitions([[1, 1]], [[1, 1]])
    c = SpatialPartitions([[1, 2]], [[1, 3], [3, 2]])
    d = SpatialPartitions([[1, 2], [2, 3]], [[1, 2], [2, 3]])

    p, trace = build([a, b, c], 8, True, 10)

    get_trace(trace, d.ret_tuple())"""

    """[P]^(2)"""
    """a = SpatialPartitions([], [[1, 2]])"""
    """b = SpatialPartitions([[1, 2], [1, 3]], [[1, 2], [1, 3]])
    c = SpatialPartitions([[1, 2], [3, 4]], [[3, 2], [1, 4]])
    d = SpatialPartitions([], [[1, 1]])

    bb = SpatialPartitions([[1, 2], [3, 2]], [[1, 2], [3, 2]])
    cc = SpatialPartitions([[1, 2], [3, 4]], [[1, 4], [3, 2]])

    p, t = build([b, c, d], 8, True, 10)

    get_trace(t, bb.ret_tuple())
    print("--------------------------------------")
    get_trace(t, cc.ret_tuple())
    print("--------------------------------------")

    p, t = build([bb, c, d], 8, True, 10)

    get_trace(t, b.ret_tuple())
    print("--------------------------------------")
    get_trace(t, cc.ret_tuple())
    print("--------------------------------------")

    p, t = build([b, cc, d], 8, True, 10)

    get_trace(t, bb.ret_tuple())
    print("--------------------------------------")
    get_trace(t, c.ret_tuple())
    print("--------------------------------------")

    e = SpatialPartitions([[1, 2]], [[1, 3], [3, 2]])

    p, t = build([e, d], 8, True, 10)

    get_trace(t, b.ret_tuple())
    print("--------------------------------------")
    get_trace(t, c.ret_tuple())
    print("--------------------------------------")
    get_trace(t, bb.ret_tuple())
    print("--------------------------------------")
    get_trace(t, cc.ret_tuple())
    print("--------------------------------------")"""

    """P^(2)_2"""
    """a = SpatialPartitions([], [[1, 1]])
    cc = SpatialPartitions([[1, 2]], [[1, 3], [3, 2]])

    b = SpatialPartitions([[1, 2], [1, 3]], [[4, 2], [4, 3]])
    c = SpatialPartitions([[1, 2], [3, 2]], [[1, 4], [3, 4]])
    d = SpatialPartitions([[1, 2], [3, 4]], [[1, 4], [3, 2]])
    dd = SpatialPartitions([[1, 2], [3, 4]], [[3, 2], [1, 4]])
    e = SpatialPartitions([[1, 1]], [[1, 1]])

    pp, tt = build([a, c, dd], 8, True, 10)

    get_trace(tt, b.ret_tuple())
    print("..............................")
    get_trace(tt, dd.ret_tuple())"""
    """print("..............................")
    get_trace(tt, d.ret_tuple())
    print("..............................")
    get_trace(tt, dd.ret_tuple())
    print("..............................")"""

    """for i in p:
        print(i.ret_tuple())"""

    """[NC]^(2)_2"""

    """p = build([SpatialPartitions([[1, 2]], [[1, 2]]), SpatialPartitions([], [[1, 2], [1, 2]])], 12)

    print(len(p))
    
    for i in p:
        print(i.ret_tuple())"""

    """[P^(2)]_2"""
    """a = SpatialPartitions([[1, 2], [3, 4]], [[3, 4], [1, 2]])

    p = build([a], 12)

    print(len(p))

    for i in p:
        print(i.ret_tuple())"""

    """P^(2)"""
    """a = SpatialPartitions([], [[1, 2]])
    b = SpatialPartitions([[1, 2], [1, 3]], [[1, 2], [1, 3]])
    c = SpatialPartitions([[1, 2], [3, 2]], [[1, 2], [3, 2]])
    d = SpatialPartitions([[1, 2], [3, 4]], [[1, 4], [3, 2]])
    dd = SpatialPartitions([[1, 2], [3, 4]], [[3, 2], [1, 4]])
    ee = SpatialPartitions([], [[1, 1]])

    #p = build([a, b, c, d, e], 0)

    #print(len(p))

    #p = build([a, b, c, d, e], 2)

    #print(len(p))

    #p = build([a, b, c, d, e], 4)

    #print(len(p))

    p, t = build([a, c, d, ee], 6, True)
    s0 = 0
    s1 = 0
    s2 = 0
    s3 = 0
    s4 = 0
    s5 = 0
    s6 = 0
    s7 = 0
    s8 = 0
    for i in p:
        match i.size():
            case 0:
                s0 += 1
            case 1:
                s1 += 1
            case 2:
                s2 += 1
            case 3:
                s3 += 1
            case 4:
                s4 += 1
            case 5:
                s5 += 1
            case 6:
                s6 += 1
            case 7:
                s7 += 1
            case 8:
                s8 += 1
    print(s0)
    print(s1)
    print(s2)
    print(s3)
    print(s4)
    print(s5)
    print(s6)
    print(s7)
    print(s8)
    get_trace(t, dd.ret_tuple())

    print(".......................")

    get_trace(t, b.ret_tuple())

    print(".......................")

    get_trace(t, c.ret_tuple())"""

    """print(len(p))

    p = build([a, b, c, d, e], 8)

    print(len(p))

    p = build([a, b, c, d, e], 10)

    print(len(p))

    p = build([a, b, c, d, e], 12)

    print(len(p))"""
