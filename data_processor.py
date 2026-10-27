import pandas as pd
import os

class DataProcessor:
    """
    Класс для обработки датасета.
    Проверяет наличие файла, его читаемость, структуру и типы данных.
    """
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.expected_structure = {
            'Участники гражданского оборота': str,
            'Тип операции': str,
            'Сумма операции': float,
            'Вид расчета': str,
            'Место оплаты': str,
            'Терминал оплаты': str,
            'Дата оплаты': str,
            'Время оплаты': str,
            'Результат операции': str,
            'Cash-back': str,
            'Сумма cash-back': float
        }

    def process(self):
        try:
            self._check_file_exists()
            df = self._read_file()
            self._check_empty(df)
            self._check_structure(df)
            print("Чтение датафрейма завершено успешно.")
            return df
            
        except FileNotFoundError as e:
            print(f"Возникла следующая ошибка: {e}")
        except pd.errors.EmptyDataError:
            print("Возникла следующая ошибка: Датафрейм пуст")
        except ValueError as e:
            print(f"Структура датафрейма НЕ соответствует ожидаемой:\n{e}")
        except Exception as e:
            print(f"Возникла непредвиденная ошибка: {e}")

    def _check_file_exists(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{self.filepath}'")

    def _read_file(self):
        return pd.read_csv(self.filepath, encoding='utf-8-sig')

    def _check_empty(self, df: pd.DataFrame):
        if df.empty:
            raise pd.errors.EmptyDataError

    def _check_structure(self, df: pd.DataFrame):
        errors = []
        
        # 1. Проверка названий столбцов
        expected_cols = list(self.expected_structure.keys())
        actual_cols = list(df.columns)
        
        if expected_cols != actual_cols:
            errors.append(f"  - Названия столбцов не совпадают.")
            errors.append(f"    Ожидаемые: {expected_cols}")
            errors.append(f"    Фактические: {actual_cols}")
            # Если столбцы не совпадают, дальше проверять типы нет смысла
            if errors:
                raise ValueError("\n".join(errors))

        # 2. Проверка типов данных
        type_mapping = {
            str: ['object'],
            float: ['float64', 'int64']
        }

        for col, expected_type in self.expected_structure.items():
            actual_type = str(df[col].dtype)
            
            if expected_type == str:
                if actual_type not in type_mapping[str]:
                    errors.append(f"  - В столбце '{col}' тип данных не соответствует ожидаемому.")
                    errors.append(f"    Ожидается: str, Фактически: {actual_type}")
            elif expected_type == float:
                if actual_type not in type_mapping[float]:
                    errors.append(f"  - В столбце '{col}' тип данных не соответствует ожидаемому.")
                    errors.append(f"    Ожидается: float, Фактически: {actual_type}")

        if errors:
            raise ValueError("\n".join(errors))