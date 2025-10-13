from string import punctuation


def remove_spaces(string: str):
    return string.replace(" ", "").replace("\n", "")


def strip_text(string: str, exceptions: set[str] = set()) -> str:
    return "".join(
        [
            a if 65 <= ord(str.upper(a)[0]) <= 90 or str.upper(a) in exceptions else ""
            for a in list(string)
        ]
    )


def factorial(n: int):
    result = 1
    for num in range(1, n + 1):
        result *= num
    return result


def choose_function(n: int, k: int):
    return factorial(n) / (factorial(k) * factorial(n - k))


def gcd(a, b) -> int:
    while b:
        a, b = b, a % b
    return a


# ax + by = gcd(a, b)
def extended_euclidean_algorithm(a: int, b: int) -> tuple[int, int, int]:
    old_s, old_t = 1, 0
    s, t = 0, 1
    old_r, r = a, b
    while r:
        q = int(old_r / r)
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
        old_r, r = r, old_r - q * r
    return (
        old_s,
        old_t,
        old_r,
    )  # (x, y, gcd(a, b)) -> x and y are the Bezout coefficients


def modular_inverse(a, m):
    x, y, gcd = extended_euclidean_algorithm(a, m)
    if gcd != 1:
        return None  # no modular inverse as a, m are not coprime
    x = (x % m + m) % m
    return x


def normalise_value(current_value, min_value, max_value):
    return (current_value - min_value) / (max_value - min_value)
