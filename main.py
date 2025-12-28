import os
import sys
import argparse
from analyzer import StegoAnalyzer
from dictionary_checker import DictionaryChecker

def analyze_file(input_file, text, analyzer, checker):
    print(f"\n--- Анализ файла: '{input_file}' ---")
    print(f"Файл: '{input_file}' загружен ({len(text)} символов).")
    
    print("--- Запуск анализа... ---")
    candidates = analyzer.analyze(text)
    
    found_any = False
    
    # Форматирование таблицы
    print(f"\n{'МЕТОД':<40} | {'SCORE':<8} | {'РЕЗУЛЬТАТ'}")
    print("-" * 100)

    for method, raw_string in candidates.items():
        score, segmented_text = checker.calculate_score_and_segment(raw_string)
        
        # Порог 0.3 (30%)
        if score > 0.3:
            found_any = True
            score_display = f"{score*100:.1f}%"
            # Обрезаем слишком длинный вывод для красоты
            if len(segmented_text) > 80:
                segmented_text = segmented_text[:77] + "..."
            print(f"{method:<40} | {score_display:<8} | {segmented_text}")
    
    print("-" * 100)
    
    if not found_any:
        print("Скрытых сообщений не найдено (Score < 30%).")
    else:
        print("Анализ завершен.")
    return found_any

def main():
    print("=== AcroText Steganography Solver CLI v1.0 ===")

    # --- Обработка аргументов командной строки ---
    parser = argparse.ArgumentParser(description="Анализатор текстовой стеганографии")
    parser.add_argument("-in", "--input", dest="filename", default=None,
                        help="Имя входного файла (по умолчанию input.txt)")
    parser.add_argument("-d", "--input-dir", dest="input_dir", default=None,
                        help="Папка с файлами для анализа (анализирует все .txt файлы в папке)")
    
    args = parser.parse_args()
    input_file = args.filename
    input_dir = args.input_dir

    # --- 2. Инициализация ---
    analyzer = StegoAnalyzer()
    checker = DictionaryChecker("russian_words.txt")

    # Если не задано ничего — используем input.txt по умолчанию
    if not input_file and not input_dir:
        input_file = "input.txt"

    # Если задана папка — обрабатываем все .txt файлы в ней
    if input_dir:
        if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
            print(f"[ОШИБКА] Папка '{input_dir}' не найдена или не является директорией.")
            return
        files = sorted(os.listdir(input_dir))
        txt_files = [f for f in files if os.path.isfile(os.path.join(input_dir, f)) and f.lower().endswith(".txt")]
        if not txt_files:
            print(f"[ОШИБКА] В папке '{input_dir}' не найдено .txt файлов.")
            return

        total = 0
        found_count = 0
        for fname in txt_files:
            total += 1
            path = os.path.join(input_dir, fname)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                print(f"[ОШИБКА] Не удалось прочитать файл '{path}': {e}")
                continue

            if not text.strip():
                print(f"[ПРЕДУПРЕЖДЕНИЕ] Файл '{path}' пуст — пропуск.")
                continue

            if analyze_file(path, text, analyzer, checker):
                found_count += 1

        print(f"\nГотово. Проанализировано файлов: {total}. Найдено потенциальных сообщений: {found_count}.")
        return

    # --- 1. Чтение файла ---
    if not os.path.exists(input_file):
        print(f"[ОШИБКА] Файл '{input_file}' не найден.")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"[ОШИБКА] Не удалось прочитать файл: {e}")
        return

    if not text.strip():
        print("[ОШИБКА] Файл пуст.")
        return

    analyze_file(input_file, text, analyzer, checker)

if __name__ == "__main__":
    main()