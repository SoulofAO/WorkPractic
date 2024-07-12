import cherrypy

Number = 5  # Глобальная переменная

class NumberInput:
    @cherrypy.expose
    def index(self):
        html = "<html><head></head><body>"
        html += "<h2>Введите числа:</h2>"
        html += "<form method='post' action='submit_numbers'>"

        for i in range(Number):
            html += f"<input type='text' name='number_{i}'><br>"

        html += "<button type='submit'>Отправить</button>"
        html += "</form></body></html>"

        return html

    @cherrypy.expose
    def submit_numbers(self, **params):
        numbers = [params[f"number_{i}"] for i in range(Number)]
        print("Введенные числа:", numbers)

if __name__ == '__main__':
    cherrypy.quickstart(NumberInput())