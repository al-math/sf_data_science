# Проект. Классификация

## Оглавление  
[1. Описание проекта](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/README.md#Описание-проекта)  
[2. Какой кейс решаем?](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/README.md#Какой-кейс-решаем)  
[3. Краткая информация о данных](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/README.md#Краткая-информация-о-данных)  
[4. Этапы работы над проектом](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/README.md#Этапы-работы-над-проектом)  
[5. Результаты](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/README.md#Результаты)    
[6. Выводы](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/README.md#Выводы) 

### Описание проекта    
Обкатать на практике задачу класификации: от и до. Включая ансаблиевые модели и подбор гиперпараметров.

Требования к версиям модулей [здесь](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/requirements.txt)

:arrow_up:[к оглавлению](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/README.md#Оглавление)


### Какой кейс решаем?    
Прогнозирование открытия депозита клиентом банка.

### Краткая информация о данных
####Описание данных:
Данные о клиентах банка:
* age (возраст);
* job (сфера занятости);
* marital (семейное положение);
* education (уровень образования);
* default (имеется ли просроченный кредит);
* housing (имеется ли кредит на жильё);
* loan (имеется ли кредит на личные нужды);
* balance (баланс).

Данные, связанные с последним контактом в контексте текущей маркетинговой кампании:
* contact (тип контакта с клиентом);
* month (месяц, в котором был последний контакт);
* day (день, в который был последний контакт);
* duration (продолжительность контакта в секундах).

Прочие признаки:
* campaign (количество контактов с этим клиентом в течение текущей кампании);
* pdays (количество пропущенных дней с момента последней маркетинговой кампании до контакта в текущей кампании);
* previous (количество контактов до текущей кампании)
* poutcome (результат прошлой маркетинговой кампании).

И, разумеется, наша целевая переменная deposit, которая определяет, согласится ли клиент открыть депозит в банке. Именно её мы будем пытаться предсказать в данном кейсе.
  
:arrow_up:[к оглавлению](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/README.md#Оглавление)

### Этапы работы над проектом  
1. Первичная обработка данных
2. Разведывательный анализ данных (EDA)
3. Отбор и преобразование признаков
4. Решение задачи классификации: логистическая регрессия и решающие деревья; подбор гиперапараметров
5. Решение задачи классификации: ансамбли моделей и построение прогноза; подбор гиперапараметров

:arrow_up:[к оглавлению](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/README.md#Оглавление)

### Результаты:  
[Jupyter Notebook](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/Project_4_ML.ipynb)

:arrow_up:[к оглавлению](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/README.md#Оглавление)


### Выводы:  
Обкатать на практике задача класификации: от и до с использованием различных подходов и подбором гиперапараметров.

:arrow_up:[к оглавлению](https://github.com/al-math/sf_data_science/tree/main/Project_4_ML/README.md#Оглавление)