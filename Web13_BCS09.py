import math
import sympy

from sympy import I
from sympy.abc import d

"""
The following functions have the purpose the evaluate results, regarding the papers [Web13] and [BCS09]:

"""

def g(n):
    outlist = []
    for i in range(n+1):
        if i % 2 != 0:
            out = 0
        else:
            out = 1
            for ii in range(i+1):
                if ii % 2 != 0:
                    out *= ii

        outlist.append(out)

    return outlist


def sc(n):
    outlist = []
    for i in range(n + 1):
        if i % 2 != 0:
            out = 0
        else:

            out = math.comb(i, i // 2) // (1+i//2)

        outlist.append(out)

    return outlist


def shift(f):
    outlist = []
    for k in range(len(f)):
        out = 0
        for i in range(k+1):
            out += math.comb(k, i) * f[i]
        outlist.append(int(out))

    return outlist


def squeezed_complex(f):
    outlist = []
    for k in range(len(f)):
        if k % 2 != 0:
            outlist.append(0)
        else:
            out = 0
            for i in range(k // 2 + 1):
                out += (math.comb(k // 2, i) * f[2*i] * f[k-2*i])
            out = out // 2**(k//2)

            outlist.append(out)

    return outlist


def squeezed_complex2(l): #not done!
    outlist = []
    for k in range(len(l)):
        if k % 2 != 0:
            outlist.append(0)
        else:
            out = 0
            for i in range(k // 2 + 1):
                out += math.comb(k // 2, i) * sympy.re(l[2 * i]) * sympy.im(l[k - 2 * i])
            outlist.append(out)

    return outlist


def make_complex(l):
    complex_l = []
    for k in range(len(l)):
        a_k = 0
        for i in range(k+1):
            a_k += math.comb(k, i) * I**i * l[k-i] * l[i]
        a_k *= (1 / (sympy.sqrt(2)**k))
        complex_l.append(a_k)
    return complex_l


def shift_complex(l):
    outlist = []
    for k in range(len(l)):
        out = 0
        for i in range(k + 1):
            out += math.comb(k, i) * l[i]
        outlist.append(out)

    return outlist


def bell_numbers(i):

    if i == 0:
        return 1
    else:
        res = 0
        for l in range(i):
            res += math.comb(i-1, l) * bell_numbers(l)
        return res


def inf_bessel(i):

    if i == 0:
        return 1
    else:
        res = 0
        for l in range(0, i):
            res += math.comb(i, l) * math.comb(i-1, l) * inf_bessel(l)
        return int(res)


def s_bessel(k, s):
    return int(1/(s * k + 1) * math.comb(s*k + k, k))


def transform(l):
    out = []
    for i in range(len(l)):
        out.append(l[i] * (i + 1))
    return out


if __name__ == "__main__":

    print(g(10))  # Partitions with block size 2

    print(shift(g(10)))  # Partitions with block size 1 and 2 (and even part)

    print(sc(10))  # non-crossing partitions with block size 2

    print(squeezed_complex(g(10)))  # balanced partitions with block size 2

    print(shift(sc(10)))  # non-crossing partitions with block size 1 and 2

    for i in range(9):
        print(bell_numbers(i))  # all partitions (even part of all partitions)
