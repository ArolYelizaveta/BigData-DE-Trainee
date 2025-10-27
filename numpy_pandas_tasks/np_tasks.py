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

