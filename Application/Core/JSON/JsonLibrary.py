# Функция для замены всех переменных с заданным именем в JSON
def replace_variables_by_name(data, variable_name, new_value, index =-1):
    if index>=0:
        k = -1
        for key, value in data.items():
            if key == variable_name:
                k = k + 1
                if k == index:
                    data[key] = new_value
                    return
            if isinstance(value, dict):
                replace_variables_by_name(value, variable_name, new_value)
    else:
        for key, value in data.items():
            if key == variable_name:
                data[key] = new_value
            if isinstance(value, dict):
                replace_variables_by_name(value, variable_name, new_value)


# Функция для поиска всех переменных по имени в JSON
def find_variables_by_name(data, variable_name):
    found_variables = []
    k = -1
    for key, value in data.items():
        if key == variable_name:
            found_variables.append(value)

        if isinstance(value, dict):
            found_variables.extend(find_variables_by_name(value, variable_name))
    return found_variables
