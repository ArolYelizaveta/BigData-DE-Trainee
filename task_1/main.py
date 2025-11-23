import argparse # легко принимает аргументы из терминала при запуске
import json
import psycopg2 # связь Python & PostgreSQL
import psycopg2.extras # Важно для словарей и быстрой вставки
import sys # работа с интерпретатором
import xml.etree.ElementTree as ET
from typing import List, Dict, Any # type hinting
from config import DB_CONFIG

class DataLoader:
    """Класс для загрузки данных из JSON файлов в базу данных."""
    def __init__(self, conn):
        self.conn = conn

    def load_data(self, file_path: str, table_name: str):
        """Загружает данные из JSON файла в указанную таблицу."""
        print(f"Загрузка данных из {file_path} в таблицу {table_name}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not data:
                print(f"Предупреждение: Файл {file_path} пуст.")
                return

            with self.conn.cursor() as cursor:
                if table_name == 'rooms':
                    query = "INSERT INTO rooms (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;"
                    records = [(item['id'], item['name']) for item in data]
                elif table_name == 'students':
                    query = "INSERT INTO students (id, name, sex, birthday, room_id) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;"
                    records = [(item['id'], item['name'], item['sex'], item['birthday'], item['room']) for item in data]
                else:
                    raise ValueError(f"Неизвестное имя таблицы: {table_name}")

                # Используем execute_batch для быстрой массовой вставки
                psycopg2.extras.execute_batch(cursor, query, records)
                self.conn.commit()
                print(f"Успешно загружено {len(records)} записей в таблицу {table_name}.")

        except (Exception, psycopg2.Error) as error:
            print(f"Ошибка при загрузке данных в {table_name}: {error}")
            self.conn.rollback() # Откатываем изменения в случае ошибки

class QueryRunner:
    """Класс для выполнения аналитических SQL-запросов."""
    def __init__(self, conn):
        self.conn = conn

    def _execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Вспомогательный метод для выполнения запроса и возврата результата в виде списка словарей."""
        results = []
        try:
            # Используем DictCursor, чтобы получать строки как словари (ключ: значение)
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(query)
                results = [dict(row) for row in cursor.fetchall()]
        except (Exception, psycopg2.Error) as error:
            print(f"Ошибка выполнения запроса: {error}")
        return results

    def get_rooms_with_student_count(self):
        """Возвращает список комнат и количество студентов в каждой."""
        query = """
            SELECT r.name AS room_name, COUNT(s.id) AS students_count
            FROM rooms r
            LEFT JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            ORDER BY r.name;
        """
        return self._execute_query(query)

    def get_top5_rooms_smallest_avg_age(self):
        """Возвращает 5 комнат с самым маленьким средним возрастом студентов."""
        query = """
            SELECT
                r.name AS room_name,
                AVG(EXTRACT(YEAR FROM AGE(s.birthday))) AS avg_age
            FROM rooms r
            JOIN students s ON r.id = s.room_id
            GROUP BY r.id
            HAVING COUNT(s.id) > 0
            ORDER BY avg_age
            LIMIT 5;
        """
        return self._execute_query(query)

    def get_top5_rooms_largest_age_diff(self):
        """Возвращает 5 комнат с самой большой разницей в возрасте студентов."""
        query = """
            SELECT
                r.name AS room_name,
                (MAX(EXTRACT(YEAR FROM AGE(s.birthday))) - MIN(EXTRACT(YEAR FROM AGE(s.birthday)))) AS age_difference
            FROM rooms r
            JOIN students s ON r.id = s.room_id
            GROUP BY r.id
            HAVING COUNT(s.id) > 1 -- Разница имеет смысл только если студентов больше одного
            ORDER BY age_difference DESC
            LIMIT 5;
        """
        return self._execute_query(query)

    def get_rooms_with_mixed_sexes(self):
        """Возвращает список комнат, где живут студенты разного пола."""
        query = """
            SELECT r.name AS room_name
            FROM rooms r
            JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            HAVING COUNT(DISTINCT s.sex) > 1
            ORDER BY r.name;
        """
        return self._execute_query(query)

class DataExporter:
    """Класс для экспорта данных в разные форматы."""
    @staticmethod
    def to_json(data: Dict[str, Any]) -> str:
        """Конвертирует словарь с результатами запросов в JSON строку."""
        # default=str нужен для корректной обработки дат и других типов данных
        return json.dumps(data, indent=4, default=str, ensure_ascii=False)

    @staticmethod
    def to_xml(data: Dict[str, Any]) -> str:
        """Конвертирует словарь с результатами запросов в XML строку."""
        root = ET.Element("results")
        for query_name, records in data.items():
            query_element = ET.SubElement(root, query_name)
            for record in records:
                record_element = ET.SubElement(query_element, "record")
                for key, val in record.items():
                    field = ET.SubElement(record_element, str(key))
                    field.text = str(val)
        # 'unicode' для поддержки кириллицы
        return ET.tostring(root, encoding='unicode', short_empty_elements=False)

def main():
    """Главная функция для запуска всего процесса."""
    parser = argparse.ArgumentParser(description="Загрузка данных и выполнение запросов к БД студентов.")
    parser.add_argument('students', type=str, help='Путь к JSON файлу со студентами')
    parser.add_argument('rooms', type=str, help='Путь к JSON файлу с комнатами')
    parser.add_argument('format', type=str, choices=['json', 'xml'], help='Формат вывода (json или xml)')
    args = parser.parse_args()

    conn = None
    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(**DB_CONFIG)
        print("Соединение с базой данных установлено.")

        # 1. Загрузка данных
        loader = DataLoader(conn)
        loader.load_data(args.rooms, 'rooms')
        loader.load_data(args.students, 'students')

        # 2. Выполнение запросов
        runner = QueryRunner(conn)
        results = {
            "rooms_with_student_count": runner.get_rooms_with_student_count(),
            "top5_rooms_smallest_avg_age": runner.get_top5_rooms_smallest_avg_age(),
            "top5_rooms_largest_age_diff": runner.get_top5_rooms_largest_age_diff(),
            "rooms_with_mixed_sexes": runner.get_rooms_with_mixed_sexes()
        }

        # 3. Экспорт результатов
        if args.format == 'json':
            output = DataExporter.to_json(results)
        else: # xml
            output = DataExporter.to_xml(results)

        print("\n--- Результаты запросов ---")
        print(output)

    except psycopg2.OperationalError as e:
        print(f"ОШИБКА ПОДКЛЮЧЕНИЯ: Не удалось подключиться к базе. Проверьте DB_CONFIG. Детали: {e}", file=sys.stderr)
    except FileNotFoundError as e:
        print(f"ОШИБКА ФАЙЛА: {e}. Проверьте правильность путей к файлам.", file=sys.stderr)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}", file=sys.stderr)
    finally:
        if conn is not None:
            conn.close()
            print("\nСоединение с базой данных закрыто.")

if __name__ == "__main__":
    main()
