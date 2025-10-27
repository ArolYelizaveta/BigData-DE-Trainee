import numpy as np

arr = np.random.randint(0, 20, 10)
print(f"Исходный массив: {arr}")

'''1. Дан случайный массив, поменять знак у элементов, 
значения которых между 3 и 8'''

mask = (arr > 3) & (arr < 8)
arr[mask] *= -1
print(f"Измененный массив: {arr}")

'''2. Заменить максимальный элемент случайного массива на 0'''

arr[arr.argmax()] = 0
print(f"Массив с замененным максимумом: {arr}")

'''3. Построить прямое произведение массивов (все комбинации 
с каждым элементом). На вход подается двумерный массив'''

arr1 = np.array([[1, 'A'],
                [2, 'B'],
                [3, 'C']])
print("Исходный массив:")
print(arr1)

grids = np.meshgrid(*arr1.T)
cartesian_product = np.stack(grids, axis=-1).reshape(-1, arr1.shape[1])
print("\nПрямое (декартово) произведение:")
print(cartesian_product)

'''4. Даны 2 массива A (8x3) и B (2x2). Найти строки в A, 
которые содержат элементы из каждой строки в B, 
независимо от порядка элементов в B'''

arr_A = np.random.randint(0, 10, size=(8, 3))
arr_B = np.random.randint(0, 10, size=(2, 2))
print("Массив A:\n", arr_A)
print("\nМассив B:\n", arr_B)

mask1 = np.any(np.isin(arr_A, arr_B[0]), axis=1)
mask2 = np.any(np.isin(arr_A, arr_B[1]), axis=1)
combined_mask = mask1 & mask2

result = arr_A[combined_mask]
print("\nСтроки в A, содержащие элементы из каждой строки в B:")
print(result)

'''5. Дана 10x3 матрица, найти строки из неравных значений 
(например строка [2,2,3] остается, строка [3,3,3] удаляется)'''

arr2 = np.random.randint(0, 5, size=(10, 3))
print("Исходная матрица:\n", arr2)
unequal_rows = arr2[(arr2 != arr2[:, [0]]).any(axis=1)]

print("\nСтроки, где не все значения равны:\n", unequal_rows)

'''6. Дан двумерный массив. Удалить те строки, которые повторяются'''

arr3 = np.array([[0, 1, 2],
                [3, 4, 5],
                [0, 1, 2],
                [6, 7, 8],
                [3, 4, 5],
                [9, 0, 1]])
print("Исходный массив:\n", arr3)
unique_rows = np.unique(arr3, axis=0)
print("\nМассив без повторяющихся строк:\n", unique_rows)
