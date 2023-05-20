#!/usr/bin/env python
# coding: utf-8

# ## Проверка модели в продакшен-режиме
# Данный модуль является техническим и служит для проверки выгруженной модели и вспомогательных данных на работоспособность и корректность прогнозов в режиме сервиса

# #### Примечание 1:
# Для тестирования в модель подаётся dataframe из 10 ключевых признаков и target-признака, преобразованный в json-формат.</br>
# Если в данных target-признак равен 0, то считается, что его нет (боевое использование) и в этом случае модель выдаёт только прогноз без оценки его точности.

# #### Примечание 2:
# Можно было бы все функции и класс, использованные при обработке данных и подборе модели, выгрузить в отдельный модуль-библиотеку и не копировать код, но в этом случае снизится читабельность и понимание блока с подбором модели.

# #### Примечание 3:
# Благодаря тому, что подаваемые данные содержат существенно меньше объектов для оценки, мы можем позволить себе определять географические координаты с использованием адреса объекта.

# In[1]:


import pandas as pd
import numpy as np
from prettytable import PrettyTable
import random


# In[2]:


data = pd.read_csv('./Data/data.csv')


# In[3]:


def strIntersection(s1, s2):
    """Служебная функция для того, чтобы оставлять в строке только те символы, которые соответствуют маске

    Args:
        string: s1 исходная строка.
        string: s2 маска.

    Returns:
        string: исходная строка после применения маски
    """
    out = ""
    for c in s1:
        if c in s2:
            out += c
    return out

def get_deviation(atrue, apred):
    """Получить отклонение предсказанного значения от истинного

    Args:
        float atrue: истинное значение
        float apred: предсказанное значение

    Returns:
        string: строковое представление отклоения
    """
    if atrue > apred:
        return "{:02n} %".format(round((1 - apred/atrue)*100)*(-1))
    else:
        return "{:02n} %".format(round((1 - atrue/apred)*100))

def print_result(sd, y_pred, y_true):
    """Печать результата в красивой табличной форме

    Args:
        dataframe sd: dataframe из признаков
        float y_pred: истинное значение
        float y_true: предсказанное значение

    Returns:
        list: значения свойств: 'Year built', 'Remodeled year', 'Heating', 'Cooling', 'Parking', 'lotsize', 'Price/sqft'
    """
    t = PrettyTable(['State', 'City', 'Address', 'Sqft', 'Predicted', 'Real price (test)', 'Deviation'])
    for idx, y in enumerate(y_pred):
        y = round(np.float64(y))
        try:
            yt = round(np.float64(strIntersection(y_true[idx], '.1234567890')))
        except Exception:
            yt = 0
        if (yt != np.nan) and (not np.isnan(yt)) and (yt > 0):
            t.add_row([sd['state'].iloc[idx], sd['city'].iloc[idx], sd['street'].iloc[idx], sd['sqft'].iloc[idx], '${:0,.0f}'.format(y), '${:0,.0f}'.format(yt), get_deviation(yt, y)])
        else:
            t.add_row([sd['state'].iloc[idx], sd['city'].iloc[idx], sd['street'].iloc[idx], sd['sqft'].iloc[idx], '${:0,.0f}'.format(y), '-', '-'])
    print(t)


# In[4]:


import requests

if __name__ == '__main__':
    # Выберем случайную строку отсчёта
    ridx = random.randint(0, data.shape[0] - 10)
    # Выберем 10 строк признаков, начиная с выбранной строки
    df = data[ridx:ridx + 10]
    # Исключим строки с некорректной площадью объекта
    df = df[((df['sqft'].isna() != True) & (df['sqft'] != '0'))]
    jdata = df.to_json(orient="index")
    # выполняем POST-запрос на сервер по эндпоинту add с параметром json
    r = requests.post('http://localhost:5000/predict', json=jdata)
    # выводим статус запроса
    print('Status code: {}'.format(r.status_code))
    # реализуем обработку результата
    if r.status_code == 200:
        # если запрос выполнен успешно (код обработки=200),
        # выводим результат на экран
        print_result(df, r.json()['prediction'], df['target'].values)
    else:
        # если запрос завершён с кодом, отличным от 200
        # выводим содержимое ответа
        print(r.text)

