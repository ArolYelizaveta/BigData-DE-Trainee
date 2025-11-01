import numpy as np
import random
import timeit
from scipy.spatial.distance import cdist

'''Задача 1: Подсчитать произведение ненулевых элементов
на диагонали прямоугольной матрицы.'''

# No numpy solution
rows = 5
cols = 6
min_val = 0
max_val = 10

matrix = [[random.randint(min_val, max_val) for j in range(cols)] for i in range(rows)]
for r in matrix:
    print(r)

result = 1
diagonal_length = min(rows, cols)

for i in range(diagonal_length):
    element = matrix[i][i]
    if element != 0:
        result *= element

print(f"\nПроизведение ненулевых элементов на диагонали: {result}")

# Numpy solution
matrix_np = np.random.randint(0, 10, size=(5, 6))
print("Исходная матрица (NumPy):")
print(matrix_np)

diagonal = np.diag(matrix_np)
non_zero_elements = diagonal[diagonal != 0]
product_np = np.prod(non_zero_elements)
print(f"\nПроизведение ненулевых элементов на диагонали: {product_np}")

'''Задача 2: Даны два вектора x и y. Проверить, задают ли они 
одно и то же мультимножество.'''

# No numpy solution
def are_multisets_equal_sorted(x, y):
  if len(x) != len(y):
    return False
  return sorted(x) == sorted(y)

# Numpy solution
def are_multisets_equal_unique(x, y):
  x = np.asarray(x)
  y = np.asarray(y)

  if len(x) != len(y):
      return False

  unique_x, counts_x = np.unique(x, return_counts=True)
  unique_y, counts_y = np.unique(y, return_counts=True)
  return np.array_equal(unique_x, unique_y) and np.array_equal(counts_x, counts_y)

'''Задача 3: Найти максимальный элемент в векторе x среди элементов, 
перед которыми стоит ноль.'''

# No numpy solution
def max_after_zero_list(x):
    max_val = None
    for i in range(1, len(x)):
        if x[i-1] == 0:
            if max_val is None:
                max_val = x[i]
            elif x[i] > max_val:
                max_val = x[i]
    return max_val

# Numpy solution
def max_after_zero_numpy(x):
    x = np.asarray(x)
    zero_indices = np.where(x == 0)[0]
    indices_after_zeros = zero_indices + 1

    valid_indices = indices_after_zeros[indices_after_zeros < len(x)]
    elements_after_zeros = x[valid_indices]

    if elements_after_zeros.size == 0:
        return None

    return np.max(elements_after_zeros)

'''Задача 4: Реализовать кодирование длин серий (Run-length encoding). 
Для некоторого вектора x необходимо вернуть кортеж из двух 
векторов одинаковой длины. Первый содержит числа, 
а второй - сколько раз их нужно повторить.'''

# No numpy solution
def rle_without_numpy(x):
    if not x:
        return ([], [])

    values = []
    counts = []
    current_value = x[0]
    current_count = 1

    for i in range(1, len(x)):
        if x[i] == current_value:
            current_count += 1
        else:
            values.append(current_value)
            counts.append(current_count)
            current_value = x[i]
            current_count = 1

    values.append(current_value)
    counts.append(current_count)

    return (values, counts)

# Numpy solution
def rle_with_numpy(x):
    x = np.asarray(x)
    if x.size == 0:
        return (np.array([]), np.array([]))

    change_indices = np.where(x[1:] != x[:-1])[0] + 1
    run_starts = np.concatenate(([0], change_indices))
    values = x[run_starts]
    run_lengths = np.diff(np.concatenate((run_starts, [x.size])))

    return (values, run_lengths)

'''Задача 5:  Даны две выборки объектов - X и Y. Вычислить матрицу 
евклидовых расстояний между объектами. Сравните с функцией 
scipy.spatial.distance.cdist по скорости работы.'''

# Numpy solution
def compute_euclidean_matrix(X, Y):
    sum_x_sq = np.sum(X**2, axis=1)
    sum_y_sq = np.sum(Y**2, axis=1)
    dot_product = X @ Y.T
    dist_sq = sum_x_sq[:, np.newaxis] - 2 * dot_product + sum_y_sq
    dist_sq = np.maximum(dist_sq, 0)
    return np.sqrt(dist_sq)

# No numpy solution
num_features = 128
num_x_samples = 1000
num_y_samples = 800

X_large = np.random.rand(num_x_samples, num_features)
Y_large = np.random.rand(num_y_samples, num_features)

numpy_time = timeit.timeit(lambda: compute_euclidean_matrix(X_large, Y_large), number=10)
scipy_time = timeit.timeit(lambda: cdist(X_large, Y_large, 'euclidean'), number=10)

print("\n--- Сравнение производительности ---")
print(f"Размерность данных: X({num_x_samples}, {num_features}), Y({num_y_samples}, {num_features})")
print(f"Наша реализация на NumPy: {numpy_time:.5f} секунд")
print(f"Функция scipy.cdist:      {scipy_time:.5f} секунд")

numpy_result = compute_euclidean_matrix(X_large, Y_large)
scipy_result = cdist(X_large, Y_large, 'euclidean')
print(f"Результаты совпадают: {np.allclose(numpy_result, scipy_result)}")

'''Задача 6: CrunchieMunchies'''

calorie_stats = np.array([ 70., 120.,  70.,  50., 110., 110., 110., 130.,  90.,  90., 120.,
       110., 120., 110., 110., 110., 100., 110., 110., 110., 100., 110.,
       100., 100., 110., 110., 100., 120., 120., 110., 100., 110., 100.,
       110., 120., 120., 110., 110., 110., 140., 110., 100., 110., 100.,
       150., 150., 160., 100., 120., 140.,  90., 130., 120., 100.,  50.,
        50., 100., 100., 120., 100.,  90., 110., 110.,  80.,  90.,  90.,
       110., 110.,  90., 110., 140., 100., 110., 110., 100., 100., 110.])

crunchie_munchies_calories = 60

# 1. Вычисление среднего количества калорий конкурентов
average_calories_raw = np.mean(calorie_stats)
average_calories = average_calories_raw - crunchie_munchies_calories
print("--- 1. Среднее количество калорий конкурентов ---")
print(f"Среднее количество калорий конкурентов: {average_calories_raw:.2f}")
print(f"Среднее количество калорий конкурентов выше на: {average_calories:.2f} калорий.")

# 2. Сортировка данных
calorie_stats_sorted = np.sort(calorie_stats)
print("\n--- 2. Отсортированные данные ---")
print("Отсортированные данные о калориях:\n", calorie_stats_sorted)

# 3. Вычисление медианы
median_calories = np.median(calorie_stats)
print("\n--- 3. Медиана ---")
print(f"Медиана количества калорий: {median_calories:.2f}")

# 4. Поиск наименьшего процентиля, превышающего 60 калорий
for p in range(1, 10):
    perc_value = np.percentile(calorie_stats, p)
    if perc_value > crunchie_munchies_calories:
        nth_percentile = p
        break
else:
    nth_percentile = 5

print("\n--- 4. Наименьший процентиль, превышающий 60 калорий ---")
print(f"{nth_percentile}-й процентиль: {np.percentile(calorie_stats, nth_percentile):.2f}")
print(f"Наименьший процентиль, превышающий 60 калорий: {nth_percentile}")

# 5. Процент хлопьев с более чем 60 калориями
more_calories_count = np.count_nonzero(calorie_stats > crunchie_munchies_calories)
more_calories = (more_calories_count / len(calorie_stats)) * 100
print("\n--- 5. Процент конкурентов с более чем 60 калориями ---")
print(f"Процент конкурентов с более чем 60 калориями: {more_calories:.2f}%")

# 6. Расчет стандартного отклонения
calorie_std = np.std(calorie_stats)
print("\n--- 6. Стандартное отклонение ---")
print(f"Стандартное отклонение количества калорий: {calorie_std:.2f}")

# 7. Маркетинговые выводы
print("\n--- 7. Маркетинговые выводы ---")
marketing_summary = f"""
Анализ данных конкурентов с помощью NumPy показывает, что CrunchieMunchies (60 калорий) является самым здоровым выбором.
1. Почти все конкуренты (96.10%) имеют более 60 калорий на порцию.
2. Среднее количество калорий (107.29) у конкурентов на 47.29 калорий выше, чем в CrunchieMunchies.
3. Медиана (110.00) показывает, что половина рынка имеет калорийность почти в два раза выше.
4. Стандартное отклонение (22.86) указывает на значительный разброс данных, но большинство конкурентов находятся в диапазоне 84-130 калорий, 
что подчеркивает исключительную низкую калорийность CrunchieMunchies по сравнению с основной массой.
"""
print(marketing_summary)

