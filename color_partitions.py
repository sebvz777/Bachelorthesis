from partition import Partition


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

    def involution_yaxis(self):
        """
        Vertical reflection with colored partition.
        """
        p = super().involution_yaxis()

        return ColorPartitions(p.partition[0], p.partition[1], list(reversed(self.color_top)), list(reversed(self.color_bottom)))

    def rotation(self, lr: bool, top: bool, hash_form=True):
        """
        Rotation with colored partition
        """
        p = super().rotation(lr, top)
        colors = Partition(self.color_top, self.color_bottom).rotation(lr, top, False)

        return ColorPartitions(p.partition[0], p.partition[1], colors.partition[0], colors.partition[1])

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

    a = ColorPartitions([2, 2, 3], [2, 2, 2], [1, 0, 1], [1, 1, 0])

    b = ColorPartitions([1, 2, 3], [2, 2, 2], [1, 0, 1], [1, 0, 1])
