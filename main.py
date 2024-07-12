import Core.Application.ApplicationWidget as Application
import sys

app = Application.QApplication(sys.argv)
ex = Application.UMainApp()
sys.exit(app.exec_())