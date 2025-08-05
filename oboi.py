import ctypes

# Путь к изображению
image_path = "i.png"

# Установка обоев
ctypes.windll.user32.SystemParametersInfoW(1, 1, image_path, 0)