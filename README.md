# CyberPhys_lab2
Вариант на 3

## Установка
1) Установить ollama из офицаильного источника
```
curl -fsSL https://ollama.com/install.sh | sh
```
2) Загрузить модель Qwen2.5:0.5B
```
ollama pull qwen2.5:0.5b
```
3) Проверить работу сервера
```
curl http://localhost:11434/api/tags
```
4) Установить зависимости python1
```
python3 -m pip3 install -r requirements.txt
```
5) Запустить скрипт
```
python3 inference.py
```

## Результат
CSV-file с результатами инференса.
