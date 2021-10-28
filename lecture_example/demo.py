def get_bmi(height_in_m, weight_in_kg):
    """根據身高體重計算BMI值 (這是 Documentation)

    :param height_in_m: 身高（單位 公尺）
    :param weight_in_kg: 體重（單位 公斤）
    :return: BMI值
    """
    return weight_in_kg / (height_in_m ** 2)  # 這是 comment


if __name__ == "__main__":
    print(get_bmi.__doc__)
