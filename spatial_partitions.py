import partition
import typing


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
        print(new_ids, q_copy_new_ids)
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


if __name__ == "__main__":

    a = SpatialPartitions([[1, 2, 3], [4, 4, 5]], [[2, 1, 3], [6, 6, 5]])
    b = SpatialPartitions([[1, 2, 3]], [[1, 4, 3], [4, 2, 3]])

    print(a.composition(b).ret_tuple())
