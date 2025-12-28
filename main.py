import os
import sys
import argparse
from analyzer import StegoAnalyzer
from dictionary_checker import DictionaryChecker

def main():
    print("=== StegoAnalyzer CLI v2.1 ===")

    # --- Обработка аргументов командной строки ---
    parser = argparse.ArgumentParser(description="Анализатор текстовой стеганографии")
    parser.add_argument("-in", "--input", dest="filename", default="input.txt",
                        help="Имя входного файла (по умолчанию input.txt)")
    
    args = parser.parse_args()
    input_file = args.filename

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

    print(f"Файл: '{input_file}' загружен ({len(text)} символов).")
    
    # --- 2. Инициализация ---
    analyzer = StegoAnalyzer()
    checker = DictionaryChecker("russian_words.txt")
    
    # --- 3. Анализ ---
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
        print("Совет: проверьте, есть ли искомые слова в russian_words.txt")
    else:
        print("Анализ завершен.")

if __name__ == "__main__":
    main()
