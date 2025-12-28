import re

class StegoAnalyzer:
    def __init__(self):
        self.strategies = [
            ("Первые буквы строк (Стих)", self.get_first_letters),
            ("Последние буквы строк (Стих)", self.get_last_letters),
            ("Первые буквы предложений (Проза)", self.get_first_letters_sentences_strict),
            ("Вторые буквы строк", self.get_second_letters_clean),
            ("Первые буквы ВТОРОГО слова", self.get_first_letters_second_word),
            ("Края строк (1-я + Последняя)", self.get_first_and_last_combined),
        ]

    def prepare_lines(self, text):
        """Базовая разбивка на строки для стратегий стихов."""
        if not text:
            return []
        return [line.strip() for line in text.split('\n') if line.strip()]

    def analyze(self, text):
        # Для стихов используем lines
        lines = self.prepare_lines(text)
        results = {}
        
        if not text:
            return results

        for name, strategy_func in self.strategies:
            try:
                # Если стратегия требует сырой текст (для строгого парсинга предложений)
                if strategy_func == self.get_first_letters_sentences_strict:
                    candidate = strategy_func(text)
                else:
                    candidate = strategy_func(lines)
                
                # Чистка результата
                candidate_clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', candidate)
                if len(candidate_clean) > 2:
                    results[name] = candidate_clean
            except Exception:
                continue
        
        return results

    # --- Стратегии ---

    def get_first_letters_sentences_strict(self, text):
        """
        Превращает текст в одну строку и ищет предложения по знакам . ! ?
        Берет первую букву каждого предложения.
        """
        # Заменяем переносы на пробелы, чтобы объединить абзацы
        one_line = text.replace('\n', ' ')
        # Разбиваем по знакам препинания
        sentences = re.split(r'(?<=[.!?])\s+', one_line)
        
        res = []
        for s in sentences:
            clean = s.strip()
            # Берем первую букву, если она есть
            match = re.search(r'[а-яА-Яa-zA-Z]', clean)
            if match:
                res.append(match.group(0))
        return "".join(res)

    def get_first_letters(self, lines):
        return "".join([line[0] for line in lines if len(line) > 0])

    def get_last_letters(self, lines):
        res = []
        for line in lines:
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            if clean:
                res.append(clean[-1])
        return "".join(res)

    def get_first_and_last_combined(self, lines):
        res = []
        for line in lines:
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            if len(clean) >= 2:
                res.append(clean[0] + clean[-1])
            elif len(clean) == 1:
                res.append(clean[0])
        return "".join(res)

    def get_second_letters_clean(self, lines):
        res = []
        for line in lines:
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            if len(clean) >= 2:
                res.append(clean[1])
        return "".join(res)

    def get_first_letters_second_word(self, lines):
        res = []
        for line in lines:
            words = line.split()
            if len(words) >= 2:
                word = re.sub(r'[^а-яА-Яa-zA-Z]', '', words[1])
                if word:
                    res.append(word[0])
        return "".join(res)
