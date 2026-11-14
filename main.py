from typing import final
from cv2.typing import MatLike
from keras.models import load_model
import cv2
import numpy as np
from rich import print
from rich.markup import escape
from words import Words
from window import Window
import time
import argparse


@final
class Camera:
	def __init__(self, camera_idx: int = 0):
		# camera idx can be 0 or 1 based on default camera of your computer
		self.camera = cv2.VideoCapture(camera_idx)
		if not self.camera.isOpened():
			self.camera.release()
			raise RuntimeError(f"Could not open camera {camera_idx} (is another app using it?)")

	def quit(self):
		self.camera.release()

	def get_image(self) -> MatLike | None:
		ret, image = self.camera.read()
		if not ret:
			return None
		image = cv2.flip(image, 1)  # 1 = horizontal mirror
		image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
		return image


@final
class Model:
	def __init__(self, model_filename: str, labels_filename: str):
		self.model = load_model(model_filename, compile=False)
		if self.model is None:
			raise RuntimeError("Cannot load model")
		self.class_names = open(labels_filename, encoding="utf-8").readlines()
		self.letter_names = [c.split(" ", 1)[-1].strip() for c in self.class_names]

	def predict(self, image: MatLike) -> dict[str, float]:
		if self.model is None:
			return
		image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
		image = (image / 127.5) - 1
		prediction: list[list[float]] = self.model.predict(image, verbose=0)  # type: ignore[arg-type]

		letter_predictions: dict[str, float] = {}
		for index, percent in enumerate(prediction[0]):  # type: ignore[arg-type] # keras doesn't provide type hints
			letter_predictions[self.letter_names[index]] = float(percent)

		return letter_predictions


def print_scores(scores: dict[str, float], decimals: int = 2):
	thresholds = [
		(0.95, "#90ee90"),  # light green
		(0.90, "#00b300"),  # green
		(0.50, "#ffd700"),  # yellow
		(0.25, "#ff8c00"),  # orange
	]

	def color_for(score: float) -> str:
		for minimum, color in thresholds:
			if score > minimum:
				return color
		return "#ff3b3b"  # red

	width = max(len(name) for name in scores)
	parts: list[str] = []
	for name, score in scores.items():
		score = round(score, decimals)
		parts.append(
			f"[#00ffff]{escape(name.ljust(width))}[/] [{color_for(score)}]{score:.{decimals}f}[/]"
		)
	print(" [#808080]|[/] ".join(parts))


def show_camera_for(camera: Camera, window: Window, duration: float):
	end_time = time.time() + duration
	while time.time() < end_time:
		image = camera.get_image()
		if image is None:
			continue
		window.set_frame(image)
		window.update()


def main(
	model_filename: str,
	words_filename: str,
	letter_threshold_target: float,
	best_letter_streak_target: int,
	wrong_attempts_threshold: int,
):
	try:
		camera = Camera(0)
		model = Model(model_filename, "./model_data/labels.txt")
		words = Words(input_file=words_filename)
		window = Window("Rozpoczynanie", "blue")
		window.update_text(words.get_word())

		best_letter_streak: int = 0
		last_best_letter: str = "-"
		wrong_attempts: int = 0
		while True:
			image = camera.get_image()
			if image is None:
				continue

			window.set_frame(image)
			window.update()

			window.update()

			scores = model.predict(image)
			print_scores(scores)

			best_letter = max(scores, key=scores.__getitem__)

			if scores[best_letter] > letter_threshold_target and last_best_letter == best_letter:
				best_letter_streak += 1
			else:
				best_letter_streak = 0

			if best_letter != "-":
				if best_letter_streak > best_letter_streak_target:
					# there may be more than one correct word but this is the one we got from the shuffle
					correct, created_word, correct_word = words.check_answer(best_letter)
					if correct:
						window.update_text(created_word, "green")
						words.next_word()
						wrong_attempts = 0
					else:
						window.update_text(created_word, "red")
						wrong_attempts += 1

					show_camera_for(camera, window, 3)

					if wrong_attempts > wrong_attempts_threshold:
						window.update_text(correct_word, "blue")
						show_camera_for(camera, window, 5)
						wrong_attempts = 0
						words.next_word()

					best_letter_streak = 0
					window.update_text(words.get_word())

			last_best_letter = best_letter

	except KeyboardInterrupt:
		pass
	finally:
		cv2.destroyAllWindows()
		try:
			camera.quit()
		except:
			pass


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--model",
		dest="model_filename",
		default="./model_data/keras_model_40e.h5",
		help="model filename",
	)
	parser.add_argument(
		"--words",
		dest="words_filename",
		default="./word_data/200slow.txt",
		help="word file filename",
	)
	parser.add_argument(
		"--letter-threshold",
		dest="letter_threshold_target",
		type=float,
		default=0.8,
		help="minimum score for the best letter",
	)
	parser.add_argument(
		"--streak-target",
		dest="best_letter_streak_target",
		type=int,
		default=10,
		help="frames the best letter must hold",
	)
	parser.add_argument(
		"--wrong-attempts",
		dest="wrong_attempts_threshold",
		type=int,
		default=3,
		help="wrong attempts before showing the answer",
	)
	args = parser.parse_args()
	main(**vars(args))
