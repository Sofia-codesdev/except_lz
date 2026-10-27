from data_processor import DataProcessor

def main():
    # Имя файла с данными
    filename = "var1.csv" 
    
    # Создаем экземпляр класса
    processor = DataProcessor(filename)
    
    # Запускаем обработку
    df = processor.process()
    
if __name__ == "__main__":
    main()