def no_of_digits(n):
    if n < 10:
        return 1
    return 1 + no_of_digits(n / 10)

def extract_middle(num):
    digits = no_of_digits(num)
    for _ in range(digits // 2):
        num = num // 10
    return num % 10

def middlesquare(xi):
    square = xi ** 2
    middle = extract_middle(square)
    return middle

def gen_four_tuple(seed):
    x0 = middlesquare(seed)
    x1 = middlesquare(x0)
    x2 = middlesquare(x1)
    x3 = middlesquare(x2)
    return f"{x0}{x1}{x2}{x3}"

def gen_recharge_card():
    seeds = [0, 1, 2, 3]
    card_num = ""
    for seed in seeds:
        card_num += gen_four_tuple(seed)
    return card_num

print("The recharge card:", gen_recharge_card())
