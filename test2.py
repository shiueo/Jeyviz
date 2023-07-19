import argparse
from random import randint
import math


def primes(n):
    b = [True] * (n + 1)
    ps = []
    for p in range(2, n + 1):
        if b[p]:
            ps.append(p)
            for i in range(p, n + 1, p):
                b[i] = False
    return ps


def modular_inv(a, b):
    if b == 0:
        return 1, 0, a
    q, r = divmod(a, b)
    x, y, g = modular_inv(b, r)
    return y, x - q * y, g


def elliptic_add(p, q, a, b, m):
    if p[2] == 0:
        return q
    if q[2] == 0:
        return p
    if p[0] == q[0]:
        if (p[1] + q[1]) % m == 0:
            return 0, 1, 0
        num = (3 * p[0] * p[0] + a) % m
        denom = (2 * p[1]) % m
    else:
        num = (q[1] - p[1]) % m
        denom = (q[0] - p[0]) % m
    inv, _, g = modular_inv(denom, m)
    if g > 1:
        return 0, 0, denom
    z = (num * inv * num * inv - p[0] - q[0]) % m
    return z, (num * inv * (p[0] - z) - p[1]) % m, 1


def elliptic_mul(k, p, a, b, m):
    r = (0, 1, 0)
    while k > 0:
        if p[2] > 1:
            return p
        if k % 2 == 1:
            r = elliptic_add(p, r, a, b, m)
        k = k // 2
        p = elliptic_add(p, p, a, b, m)
    return r


def lenstra(n, limit):
    g = n
    while g == n:
        q = randint(0, n - 1), randint(0, n - 1), 1
        a = randint(0, n - 1)
        b = (q[1] * q[1] - q[0] * q[0] * q[0] - a * q[0]) % n
        g = math.gcd(4 * a * a * a + 27 * b * b, n)
    if g > 1:
        return g
    for p in primes(limit):
        pp = p
        while pp < limit:
            q = elliptic_mul(p, q, a, b, n)
            if q[2] > 1:
                return math.gcd(q[2], n)
            pp = p * pp
    return False


def main():
    s = set()
    while 1:
        s.add(
            lenstra(
                801239812381249127412412412423423423423121231212412412234433000000,
                10000,
            )
        )
        if len(s) > 20:
            break
    print(s)


if __name__ == "__main__":
    main()
