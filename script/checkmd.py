# 修正提取数字的代码
# 由于字符串前面有换行符，所以正确的提取方式应该是 [1:-1]
def check_question_number(matched_strings):
    # 提取数字
    numbers = [int(s[1:-1]) for s in matched_strings]

    # 找到跳过的数字
    missing_numbers = [i for i in range(numbers[0], numbers[-1] + 1) if i not in numbers]

    print(f"The missing numbers are {missing_numbers}.")
