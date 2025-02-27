def generate_parameter_file(initial_volume, time_interval, nuclei_concentration,nuclei_diameter,nuclei_height,C_hhtp_add):
    try:
        with open('./negen1o/parameter.txt', 'w') as file:
            file.write(f'V_initial = {initial_volume}\n')
            file.write(f'addition_interval = {time_interval}\n')
            file.write(f'con_initial = {nuclei_concentration}\n')
            file.write(f'dia_initial = {nuclei_diameter}\n')
            file.write(f'hei_initial = {nuclei_height}\n')
            file.write(f'C_hhtp_add = {C_hhtp_add}\n')
        # print("parameter.txt generated！")
    except Exception as e:
        print(f"error: {e}")