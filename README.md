# Домашняя работа №3 - Преобразование конфигурационного файла
### Постановка задачи

Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.

Входной текст на языке yaml принимается из стандартного ввода. Выходной
текст на учебном конфигурационном языке попадает в файл, путь к которому
задан ключом командной строки.
Однострочные комментарии:
```
:: Это однострочный комментарий
```
Массивы:
```
{ значение, значение, значение, ... }
```
Имена:
```
[A-Z]+
```
Значения:
- Числа.
- Строки.
- Массивы.
- Строки:
```
q(Это строка)
```
Объявление константы на этапе трансляции:
```
имя = значение;
```
Вычисление константы на этапе трансляции:
```
|имя|
```
Результатом вычисления константного выражения является значение.

Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 3
примера описания конфигураций из разных предметных областей.

### Запуск программы
```bash
python main.py <yaml_file> -o output.txt 
```

### Запуск тестов
```bash
pip install pytest
pytest test
```

### Результат тестирования
![Tests](https://github.com/Balex7777/Configuration_HW3/blob/main/images/tests.png)

### Результат работы программы
Исходный файл config.yaml

![yaml](https://github.com/Balex7777/Configuration_HW3/blob/main/yaml.png)

Результат работы программы

![output](https://github.com/Balex7777/Configuration_HW3/blob/main/output.png)
