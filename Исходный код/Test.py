from Image_Threshold import*
from MainWindow import*
# Загрузка изображения
app = qt.QApplication([])
Win = Window()
Win.show()
Win.setWindowTitle('Обработка изображений')
sys.exit(app.exec())