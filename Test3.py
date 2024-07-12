import cherrypy


class Calculator:
    def __init__(self):
        self.number = 1
    @cherrypy.expose
    def index(self):
        return '''
            <html>
            <head></head>
            <body>
                <h2>Форма</h2>
                <form method="post" action="calculate">
                    Введите цифры: <input type="text" name="numbers"><br>
                    <button type="submit">Посчитать</button>
                </form>
            </body>
            </html>
        '''

    @cherrypy.expose
    def calculate(self, numbers):
        print(numbers)
        self.number = int(numbers)
        html = "<html><head></head><body>"
        html += "<h2>Введите числа:</h2>"
        html += "<form method='post' action='submit_numbers'>"

        for i in range(int(numbers)):
            html += f"<input type='text' name='number_{i}'><br>"

        html += "<button type='submit'>Отправить</button>"
        html += "</form></body></html>"

        return html

    @cherrypy.expose
    def submit_numbers(self, **params):
        numbers = [params[f"number_{i}"] for i in range(self.number)]
        print("Введенные числа:", numbers)

if __name__ == '__main__':
    cherrypy.quickstart(Calculator())