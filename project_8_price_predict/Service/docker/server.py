#!/usr/bin/env python
# coding: utf-8

# ### Сервис предсказания стоимости объектов недвижимости с использованием полученной модели

# In[41]:


from flask import Flask, request, jsonify
import json
app = Flask(__name__)


# In[42]:


# Контроль доступности сервиса
@app.route('/')
def index():
    return 'Test message. The server is running'


# In[43]:


import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import ast
#from Model.ms_func import Dumper
import pickle
from os import path
from datetime import datetime


# In[44]:


# Класс для чтения сохранённой модели и вспомогательных данных
class Dumper():  
    def __init__(self, model_dir="Model/"):  
        self.model_dir = model_dir  
          
    # сохраняет объект
    def dump(self, data, filename):  
        with open(self.get_file_name(filename), 'wb') as file:  
            pickle.dump(data, file)  
              
    # загружает объект
    def load(self, filename):  
        file_name = path.join(self.model_dir, filename + ".pkl")   
        with open(file_name, 'rb') as file:  
            sets = pickle.load(file)  
        return sets  
          
    # возвращает полное имя файла
    def get_file_name(self, filename):   
        return path.join(self.model_dir, filename + ".pkl")
    
app_geo = Nominatim(user_agent="tutorial")
    
def get_loc(street, city, zipcode):
    """Получаем географические координаты по адресу, городу, почтовому индексу

    Args:
        street (string): адрес
        city (string): город
        zipcode (string): почтовый индекс

    Returns:
        tuple (float lat, float lon): географические координаты.
    """
    answ = (np.nan, np.nan)
    if street == None:
        street = ''
    if city == None:
        city = ''
    if zipcode == None:
        zipcode = ''
    street = str(street).strip()
    city = str(city).strip()
    zipcode = str(zipcode).strip()
    haserror = False
    
    try:
        location = app_geo.geocode(street + ' ' + city).raw
        answ = (location['lat'], location['lon'])
    except Exception:
        haserror = True
        
    if haserror == True:
        try:
            location = app_geo.geocode(zipcode).raw
            answ = (location['lat'], location['lon'])
        except Exception:
            answ = (np.nan, np.nan)
    
    return answ

def GetFromHomeFactsList(AStr):
    """Получить информацию из записи в колонке homeFacts

    Args:
        string: строка из колокни homeFacts.

    Returns:
        list: значения свойств: 'Year built', 'Remodeled year', 'Heating', 'Cooling', 'Parking', 'lotsize', 'Price/sqft'
    """
    answ = [None, None, None, None, None, None, None]
    labs = ['Year built', 'Remodeled year', 'Heating', 'Cooling', 'Parking', 'lotsize', 'Price/sqft']
    try:
        lst = ast.literal_eval(AStr)['atAGlanceFacts']
        answ = []
        for l in labs:
            fnd = False
            try:
                for val in lst:
                    if val['factLabel'] == l:
                        answ.append(val['factValue'])
                        fnd = True
                        break
                if fnd == False:
                    answ.append(None)
            except Exception:
                answ.append(None)
    except Exception:
        return answ
    return answ

def GetFromSchoolList(AStr):
    """Получить информацию из записи в колонке schools

    Args:
        string: строка из колокни schools.

    Returns:
        list: значения свойств: 'rating', 'data'.'Distance', 'data'.'Grades', 'name'
    """
    answ = [[None], [None], [None], [None]]
    labs1lvl = ['rating', 'data', 'name']
    labs2lvl = ['Distance', 'Grades']
    try:
        lst = ast.literal_eval(AStr)[0]
        answ = []
        for l in labs1lvl:
            try:
                if l == 'data':
                    try:
                        answ.append(lst[l]['Distance'])    
                    except Exception:
                        answ.append([None])
                    try:
                        answ.append(lst[l]['Grades'])    
                    except Exception:
                        answ.append([None])
                else:
                    answ.append(lst[l])  
            except Exception:
                answ.append([None])
    except Exception:
        return answ
    return answ

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

def MaxMinMeanDistance(Alst):
    """Функция для определения минимального, максимального и среднего расстояния до учебного заведения

    Args:
        list: Alst - список из расстояний.

    Returns:
        list: минимальное, максимальное и среднее расстояние до учебного заведения
    """
    res = [np.nan, np.nan, np.nan]
    dcount = 0
    dsum = 0.0
    dMax = 0.0
    dMin = np.inf
    mask = '0123456789.'
    for elm in Alst:
        elm = strIntersection(elm, mask)
        if elm != '':
            fElm = float(elm)
            dsum += fElm
            if fElm < dMin:
                dMin = fElm
            if fElm > dMax:
                dMax = fElm
            dcount += 1
    if dcount > 0:
        res = [dMax, dMin, dsum/dcount]
    return res

def MaxMinMeanRating(Alst):
    """Функция для определения минимального, максимального и среднего рейтинга учебного заведения

    Args:
        list: Alst - список рейтингов.

    Returns:
        list: минимальное, максимальное и среднее значение рейтинга учебного заведения
    """
    res = [np.nan, np.nan, np.nan]
    dcount = 0
    dsum = 0.0
    dMax = 0.0
    dMin = np.inf
    mask = '0123456789/'
    for elm in Alst:
        elm = strIntersection(elm, mask)
        elm = elm.replace('/10', '')
        if elm != '':
            fElm = float(elm)
            dsum += fElm
            if fElm < dMin:
                dMin = fElm
            if fElm > dMax:
                dMax = fElm
            dcount += 1
    if dcount > 0:
        res = [dMax/10, dMin/10, dsum/dcount/10]
    return res

def str_to_float(aStr):
    """Функция для преобразования строки в действительное число

    Args:
        string: aStr - возможное число в строковом представлении

    Returns:
        float: действительное число или nan, если не удалось совершить преобразование
    """
    if aStr == None:
        return np.nan
    aStr = strIntersection(str(aStr), '-0123456789.')
    if aStr == '':
        return np.nan
    aStr = aStr.replace('..', '.')
    aStr = aStr.replace('--', '-')
    if aStr == '.':
        return np.nan
    if aStr[len(aStr) - 1] == '.':
        aStr = aStr[0:len(aStr)-1]
    try:
        return float(aStr)
    except Exception:
        return np.nan

def str_float_to_int(aStr):
    """Функция для преобразования строки в целое число

    Args:
        string: aStr - возможное число в строковом представлении

    Returns:
        float: целое число или nan, если не удалось совершить преобразование
    """
    aFlt = str_to_float(aStr)
    try:
        return int(round(aFlt))
    except Exception:
        return np.nan
    
def ColToLow(df, colname):
    """Функция для приведения текстового признака к нижнему регистру и только базовым символам

    Args:
        dataframe: df - исходный датафрейм
        string: colname - признак

    Returns:
        преобразует признак в исходном датафрейме
    """
    mask = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    df[colname] = df[colname].str.lower()
    df[colname] = df[colname].apply(lambda x: strIntersection(str(x), mask))


# In[45]:


dumper = Dumper()


# In[46]:


# модель
model = dumper.load('model')
# граничный коэффициент ванн на квадратный фут
bath_sqft_border_coef = dumper.load('bath_sqft_border_coef')
# среднее количество ванн на квадратный фут
bath_sqft_coef = dumper.load('bath_sqft_coef')
# географический прямоугольник, ограничивающий координаты объектов в США
geo_borders = dumper.load('geo_borders')
# медианные значения ключевых признаков в Калифонии (CA)
median_CA = dumper.load('median_CA')
# медианные значения ключевых признаков в остальных штатах
median_other = dumper.load('median_other')
# преобразователь масштаба
scaler = dumper.load('scaler')
# преобразователь QuantileTransformer
sqft_q_trans = dumper.load('sqft_q_trans')
# список колонок (и их порядок), которые участвуют в финальных признаках
df_columns = dumper.load('df_columns')
# порядок сокращённого набора признаков
idx10_features = dumper.load('idx10_features')


# In[47]:


def get_x_y(adf):
    """Преобразовать входной dataframe в набор, котрый можно подать на вход модели
       Преобразователь преобразует тип, заполняет, кодирует, масштабирует признаки аналогично тому, как это происходило при подготовке датасета модели

    Args:
        dataframe: датафрейм для прогнозирования.

    Returns:
        ndarray X: признаки, подготовленные к передаче в модель
        series y: целевой признак (для проверки); если использование "боевое", то передать в исходном dataframe 0
    """
    vdf = adf.copy()    
      
    vdf['SC_List'] = vdf['schools'].apply(lambda x: GetFromSchoolList(x))

    vdf['SC_Distance'] = vdf['SC_List'].apply(lambda x: x[1])
    vdf['SC_Distance_Lst'] = vdf['SC_Distance'].apply(lambda x: MaxMinMeanDistance(x))
    vdf['SC_Distance_Max'] = vdf['SC_Distance_Lst'].apply(lambda x: x[0])
    
    vdf['SC_Rating'] = vdf['SC_List'].apply(lambda x: x[0])    
    vdf['SC_Rating_Lst'] = vdf['SC_Rating'].apply(lambda x: MaxMinMeanRating(x))
    vdf['SC_Rating_Mean'] = vdf['SC_Rating_Lst'].apply(lambda x: x[2])
    
    vdf['lat'], vdf['lng'] = zip(*vdf.apply(lambda x: get_loc(x['street'], x['city'], x['zipcode']), axis = 1))
    vdf['lat'] = vdf['lat'].apply(lambda x: str_to_float(x))
    vdf['lng'] = vdf['lng'].apply(lambda x: str_to_float(x))
    
    vdf['sqft'] = vdf['sqft'].apply(lambda x: str_float_to_int(x))
    vdf['baths'] = vdf['baths'].apply(lambda x: str_float_to_int(x))
    
    vdf['HF_List'] = vdf['homeFacts'].apply(lambda x: GetFromHomeFactsList(x))
    vdf['HF_YearBuilt'] = vdf['HF_List'].apply(lambda x: x[0])
    vdf['HF_Lotsize'] = vdf['HF_List'].apply(lambda x: x[5])
    vdf['HF_YearBuilt'] = vdf['HF_YearBuilt'].apply(lambda x: str_float_to_int(x))
    vdf['HF_Lotsize'] = vdf['HF_Lotsize'].apply(lambda x: str_float_to_int(x))
    vdf['target'] = vdf['target'].apply(lambda x: str_float_to_int(x))
    
    ColToLow(vdf, 'propertyType')
    vdf['propertyType_condo'] = vdf['propertyType'].apply(lambda x: 1 if x == 'condo' else 0)
    
    vdf['state_CA'] = vdf['state'].apply(lambda x: 1 if x == 'CA' else 0)
    
    vdf['SC_Distance_Max'] = vdf.apply(lambda x: median_other['SC_Distance_Max'] if (np.isnan(x['SC_Distance_Max']) or (x['SC_Distance_Max'] == 0)) and (x['state_CA'] == 0)        
        else x['SC_Distance_Max'], axis = 1)
    vdf['SC_Distance_Max'] = vdf.apply(lambda x: median_CA['SC_Distance_Max'] if (np.isnan(x['SC_Distance_Max']) or (x['SC_Distance_Max'] == 0)) and (x['state_CA'] == 1)
        else x['SC_Distance_Max'], axis = 1)
    
    vdf['SC_Rating_Mean'] = vdf.apply(lambda x: median_other['SC_Rating_Mean'] if (np.isnan(x['SC_Rating_Mean']) or (x['SC_Rating_Mean'] == 0)) and (x['state_CA'] == 0)        
        else x['SC_Rating_Mean'], axis = 1)
    vdf['SC_Rating_Mean'] = vdf.apply(lambda x: median_CA['SC_Rating_Mean'] if (np.isnan(x['SC_Rating_Mean']) or (x['SC_Rating_Mean'] == 0)) and (x['state_CA'] == 1)
        else x['SC_Rating_Mean'], axis = 1)
    
    vdf['lat'] = vdf.apply(lambda x: median_other['lat'] if (np.isnan(x['lat']) or (x['lat'] < geo_borders['minlat']) or (x['lat'] > geo_borders['maxlat'])) and (x['state_CA'] == 0)
        else x['lat'], axis = 1)
    vdf['lat'] = vdf.apply(lambda x: median_CA['lat'] if (np.isnan(x['lat']) or (x['lat'] < geo_borders['minlat']) or (x['lat'] > geo_borders['maxlat'])) and (x['state_CA'] == 1)
        else x['lat'], axis = 1)
    
    
    vdf['lng'] = vdf.apply(lambda x: median_other['lng'] if (np.isnan(x['lng']) or (x['lng'] < geo_borders['minlng']) or (x['lng'] > geo_borders['maxlng'])) and (x['state_CA'] == 0)
        else x['lng'], axis = 1)
    vdf['lng'] = vdf.apply(lambda x: median_CA['lng'] if (np.isnan(x['lng']) or (x['lng'] < geo_borders['minlng']) or (x['lng'] > geo_borders['maxlng'])) and (x['state_CA'] == 1)
        else x['lng'], axis = 1)
    
    vdf['HF_Lotsize'] = vdf.apply(lambda x: median_other['HF_Lotsize'] if (np.isnan(x['HF_Lotsize']) or (x['HF_Lotsize'] == 0)) and (x['state_CA'] == 0)        
        else x['HF_Lotsize'], axis = 1)
    vdf['HF_Lotsize'] = vdf.apply(lambda x: median_CA['HF_Lotsize'] if (np.isnan(x['HF_Lotsize']) or (x['HF_Lotsize'] == 0)) and (x['state_CA'] == 1)
        else x['HF_Lotsize'], axis = 1)
    
    vdf['HF_YearBuilt'] = vdf.apply(lambda x: median_other['HF_YearBuilt'] 
                                    if (np.isnan(x['HF_YearBuilt']) or (x['HF_YearBuilt'] <= 1900) or (x['HF_YearBuilt'] > datetime.now().year + 10)) and (x['state_CA'] == 0)
        else x['HF_YearBuilt'], axis = 1)
    vdf['HF_YearBuilt'] = vdf.apply(lambda x: median_CA['HF_YearBuilt'] 
                                    if (np.isnan(x['HF_YearBuilt']) or (x['HF_YearBuilt'] <= 1900) or (x['HF_YearBuilt'] > datetime.now().year + 10)) and (x['state_CA'] == 1)
        else x['HF_YearBuilt'], axis = 1)
    
    vdf['baths'] = vdf.apply(lambda x: x['sqft']*bath_sqft_coef if np.isnan(x['baths']) or (x['baths'] > x['sqft']*bath_sqft_border_coef[0]) else x['baths'], axis = 1)
    
    data_for_transform = vdf['sqft'].values.reshape((len(vdf), 1))
    vdf['sqft'] = pd.DataFrame(sqft_q_trans.transform(data_for_transform), columns = ['sqft'], index=vdf.index)
    
    tvdf = vdf.copy()
    tvdf = tvdf[['sqft', 'baths', 'lng', 'lat', 'SC_Rating_Mean', 'SC_Distance_Max', 'HF_YearBuilt', 'HF_Lotsize', 'propertyType_condo', 'state_CA', 'target']]
    
    #for col in tvdf.columns:
    #    if col not in df_columns:
    #        tvdf.drop(col, axis=1, inplace=True)
    
    for col in df_columns:
        if col in tvdf.columns:
            tvdf.drop(col, axis=1, inplace=True)
            tvdf[col] = vdf[col]
        else:
            tvdf[col] = 0
            
    vdf = tvdf
    
    if 'target' in vdf.columns:
        X = vdf.drop('target', axis=1)
        y = vdf['target']
    else:
        X = vdf
        y = 0
    
    X = scaler.transform(X)
    
    X = X[:, idx10_features]
    #X = X[:, [0, 4, 10, 3, 9, 5, 8, 19, 23, 6]]

    return X, y


# In[48]:


def predict(ax):
    """Получить предсказанеи модели

    Args:
        ndarray ax: признаки

    Returns:
        ndarray: предсказания
    """
    return model.predict(ax)


# In[49]:


def get_deviation(atrue, apred):
    """Получить отклонение предсказанного значения от истинного

    Args:
        float atrue: истинное значение
        float apred: предсказанное значение
    """
    if atrue > apred:
        return "{:02n} %".format(round((1 - apred/atrue)*100)*(-1))
    else:
        return "{:02n} %".format(round((1 - atrue/apred)*100))

def print_result(sd, y_pred, y_true):
    t = PrettyTable(['State', 'City', 'Address', 'Sqft', 'Predicted', 'Real price (test)', 'Deviation'])
    for idx, y in enumerate(y_pred):
        y = np.exp(y)+1
        yt = str_float_to_int(y_true.iloc[idx])
        if (yt != np.nan) and (not np.isnan(yt)) and (yt > 0):
            t.add_row([sd['state'].iloc[idx], sd['city'].iloc[idx], sd['street'].iloc[idx], sd['sqft'].iloc[idx], '${:0,.0f}'.format(y), '${:0,.0f}'.format(yt), get_deviation(yt, y)])
        else:
            t.add_row([sd['state'].iloc[idx], sd['city'].iloc[idx], sd['street'].iloc[idx], sd['sqft'].iloc[idx], '${:0,.0f}'.format(y), '-', '-'])
    print(t)


# In[50]:


# Метод прогноза
@app.route('/predict', methods=['POST'])
def model_predict():
    features = request.json
    jdata = json.loads(features)
    dfr = pd.DataFrame(jdata)
    df = dfr.T

    X, y = get_x_y(df)
    yp = np.exp(predict(X)) + 1

    return {'prediction': yp.tolist()}


# In[ ]:


# Старт сервиса
if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=5000)

