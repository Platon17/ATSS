import os

class DictionaryChecker:
    def __init__(self, dictionary_path="russian_words.txt"):
        self.words = set()
        self.load_dictionary(dictionary_path)

    def load_dictionary(self, path):
        """Загружает словарь. Если файла нет, создает базовый набор для теста."""
        if not os.path.exists(path):
            print(f"[WARN] Файл словаря '{path}' не найден.") 
            print("       Используется встроенный тестовый набор слов.")
            # Базовый набор слов, чтобы пример пользователя сработал
            self.words = {
                "лит", "хабаровск", "стеганография", 
                "привет", "код", "анализ", "тест"
            }
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().lower()
                    if len(word) > 1: # Игнорируем однобуквенные, кроме контекста
                        self.words.add(word)
        except Exception as e:
            print(f"[ERROR] Ошибка чтения словаря: {e}")

    def calculate_score_and_segment(self, text):
        """
        Жадный алгоритм поиска слов.
        Возвращает кортеж: (score, readable_text)
        Score - число от 0.0 до 1.0
        """
        if not text:
            return 0.0, ""

        clean_text = text.lower()
        n = len(clean_text)
        if n == 0:
            return 0.0, ""

        recognized_chars = 0
        result_segments = []
        i = 0
        
        while i < n:
            found_word = None
            # Ищем максимально длинное слово, начинающееся с текущей позиции
            # Ограничим длину поиска (например, до 25 символов)
            max_len = min(25, n - i)
            
            for length in range(max_len, 1, -1):
                sub = clean_text[i : i + length]
                if sub in self.words:
                    found_word = sub
                    break
            
            if found_word:
                result_segments.append(found_word.upper()) # Найденное слово капсом
                recognized_chars += len(found_word)
                i += len(found_word)
            else:
                # Если слово не найдено, оставляем символ как есть (lower)
                result_segments.append(clean_text[i])
                i += 1

        score = recognized_chars / n
        readable_text = " ".join(result_segments)
        return score, readable_text
