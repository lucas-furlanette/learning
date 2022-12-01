s = input("Digite um número romano: ")


def romantoint(s: str) -> int:
    roman = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    ans = 0
    for i in range(len(s) - 1, -1, -1):
        num = roman[s[i]]
        if 4 * num < ans:
            ans = ans - num
        else:
            ans = ans + num
    return ans


###############################################
def romantoint2(s: str) -> int:
    translations = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000
    }
    number = 0
    s = s.replace("IV", "IIII")\
        .replace("IX", "VIIII")\
        .replace("XL", "XXXX")\
        .replace("XC", "LXXXX")\
        .replace("CD", "CCCC")\
        .replace("CM", "DCCCC")
    for char in s:
        number += translations[char]
    return number


###############################################

def convertroman(s: str):
    result_number = 0
    prevous_number = 0
    mapping = dict(
        I=1,
        V=5,
        X=10,
        L=50,
        C=100,
        D=500,
        M=1000)
    for symbol in s[::-1]:
        if mapping[symbol] >= prevous_number:
            result_number += mapping[symbol]
        else:
            result_number -= mapping[symbol]
        prevous_number = mapping[symbol]
    return result_number


print(
    romantoint(s),
    romantoint2(s),
    convertroman(s)
)

