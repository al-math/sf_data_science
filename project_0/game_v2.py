import numpy as np

def random_predict(number:int=1) -> int:
    """Рандомно угадываем число

    Args:
        number (int, optional): Загаданное число. Defaults to 1.

    Returns:
        int: Число попыток
    """

    count = 0
    lbrd = 1 # левая граница интервала
    rbrd = 100 # правая граница интервала
    brd = 50 # середина интервала
    while True:
        count += 1
        if number == brd:
            break # выход из цикла, если угадали
        elif number < brd:
            rbrd = brd
        else:
            lbrd = brd
        # рассматриваем частный случай, когда деление интервала не даёт нового значения
        if brd == (lbrd + rbrd)//2:
            brd+=1
        else:
            brd = (lbrd + rbrd)//2
    return(count)

def score_game(random_predict) -> int:
    """_summary_

    Args:
        random_predict (_type_): _description_

    Returns:
        int: _description_
    """

    count_ls = [] # список для сохранения количества попыток
    np.random.seed(1) # фиксируем сид для воспроизводимости
    random_array = np.random.randint(1, 101, size=(1000)) # загадали список чисел

    for number in random_array:
        count_ls.append(random_predict(number))

    score = int(np.mean(count_ls)) # находим среднее количество попыток

    print(f'Ваш алгоритм угадывает число в среднем за: {score} попыток')
    return(score)

# RUN
if __name__ == '__main__':
    score_game(random_predict)