import random


class Words:
	def __init__(self, input_file="1000sluw.txt"):
		# wczytaj plik ze słowami
		self.wordPosition = 0
		self.deletedPos = 1
		with open(input_file, "r", encoding="utf-8") as f:
			self.pool = [line.strip() for line in f if line.strip()]
		if not self.pool:
			raise RuntimeError("Words file is empty")
		self.shuffle_words()

	def shuffle_words(self):
		random.shuffle(self.pool)

	def get_word(self) -> str:
		self.wordCopy = list(self.pool[self.wordPosition])
		self.wordCopy[self.deletedPos] = "_"
		self.wordCopy = "".join(self.wordCopy)

		return self.wordCopy

	def next_word(self) -> None:
		self.wordPosition += 1
		if self.wordPosition >= len(self.pool):
			self.wordPosition = 0
			self.shuffle_words()
		self.deletedPos = random.randrange(0, len(self.wordCopy))

	def check_answer(self, answer: str):
		word_lower = list(self.wordCopy)
		word_upper = list(self.wordCopy) # not = Lword because lists are shared as pointers
		word_lower[self.deletedPos] = answer.lower()
		word_upper[self.deletedPos] = answer.upper()
		word_lower = "".join(word_lower)
		word_upper = "".join(word_upper)
		
		if word_upper in self.pool:
			return True, word_upper, self.pool[self.wordPosition]
		elif word_lower in self.pool:
			return True, word_lower, self.pool[self.wordPosition]
		else:
			return False, word_lower, self.pool[self.wordPosition]