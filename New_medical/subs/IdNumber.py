import random

def generate_id_number():
    # 地区代码（前6位）
    area_code = "510109"  # 成都市高新区

    # 出生日期（中间8位），格式为YYYYMMDD
    year = random.randint(1970, 2000)
    month = random.randint(1, 12)
    if month < 10:
        month = f"0{month}"
    day = random.randint(1, 28)  # 为简单起见，我们将所有月份的天数设置为28天
    if day < 10:
        day = f"0{day}"
    birth_date = f"{year}{month}{day}"

    # 顺序码（第15到17位）
    sequence_code = random.randint(100, 999)

    # 前17位拼接起来
    id_without_checksum = f"{area_code}{birth_date}{sequence_code}"

    # 校验码（第18位）
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_sum_mapping = "10X98765432"
    check_sum = sum(int(id_without_checksum[i]) * weights[i] for i in range(17)) % 11
    check_digit = check_sum_mapping[check_sum]

    # 完整身份证号
    id_number = f"{id_without_checksum}{check_digit}"
    return id_number
