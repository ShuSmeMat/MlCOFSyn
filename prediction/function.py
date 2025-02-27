# function.py
"""
该文件包含若干生成序列的函数，包括：
1. constant_sequence         （常数序列）
2. arithmetic_progression    （等差数列）
3. geometric_progression     （等比数列）
"""
from webbrowser import open_new


def constant_sequence(initial_value: float, list_numbers: int):
    """
    生成常数序列。
    参数：
    - initial_value : 初始值（每个元素都相同）
    - list_numbers  : 序列长度
    返回：所有元素相同的列表
    """
    return [initial_value] * list_numbers


def arithmetic_progression(initial_value: float, common_difference: float, list_numbers: int):
    """
    生成等差数列。
    参数：
    - initial_value     : 首项
    - common_difference : 公差
    - list_numbers      : 序列长度
    返回：等差数列列表
    """
    seq = []
    current = initial_value
    for _ in range(list_numbers):
        seq.append(current)
        current += common_difference
    return seq


def geometric_progression(initial_value: float, common_ratio: float, list_numbers: int):
    """
    生成等比数列。
    参数：
    - initial_value : 首项
    - common_ratio  : 公比
    - list_numbers  : 序列长度
    返回：等比数列列表
    """
    seq = []
    current = initial_value
    for _ in range(list_numbers):
        seq.append(current)
        current *= common_ratio
    return seq

####################################################################################################
"""
生成addition.txt以及parameter.txt，用于生成任务
"""
def generate_parameter_file(initial_volume, time_interval, nuclei_concentration,nuclei_diameter,nuclei_height,C_hhtp_add):
    try:
        with open('../negen1o/parameter.txt', 'w') as file:
            file.write(f'V_initial = {initial_volume}\n')
            file.write(f'addition_interval = {time_interval}\n')
            file.write(f'con_initial = {nuclei_concentration}\n')
            file.write(f'dia_initial = {nuclei_diameter}\n')
            file.write(f'hei_initial = {nuclei_height}\n')
            file.write(f'C_hhtp_add = {C_hhtp_add}\n')
        # print("parameter.txt generated！")
    except Exception as e:
        print(f"error: {e}")

def generate_addition_file(sequence):
    sequence_list = sequence.split(',')
    total_count = len(sequence_list)
    formatted_sequence = f'1_0_{total_count} : {sequence}'

    try:
        with open('../negen1o/addition_squeue.txt', 'w') as file:
            file.write(formatted_sequence + '\n')
        # print("addition.txt generated！")
    except Exception as e:
        print(f"错误: {e}")