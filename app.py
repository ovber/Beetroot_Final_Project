from flask import Flask, render_template, request, flash, url_for
from make_pdf import MakePDF as serialPDF
from make_pdf_individual import MakePDF as individualPDF
from select_serial import SelectSerial
from flask_caching import Cache


config_cache = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 1
}
cache = Cache(config=config_cache)
app = Flask(__name__)
app.config["SECRET_KEY"] = b"sdlajkfhlsadhf;"
cache.init_app(app)

menu = [{"name": "Головна", "url": "/"},
        {"name": "Підбір серійних перемичок", "url": "/calculation"},
        {"name": "Розрахунок індівидуальної балки", "url": "/individual"},
        {"name": "Контакти", "url": "/about"}
        ]


class MakeRequestDict:

    def __init__(self):
        self.requests_dict = dict()
        self.number_mark = 1
        self.position_mark = "ПР"

    def add(
        self,
        type_of_wall,
        type_of_construction_wall,
        height_of_bricks,
        width_of_opening,
        width_of_wall
    ):
        self.requests_dict[f"{self.position_mark}-{self.number_mark}"] = [
            type_of_wall,
            type_of_construction_wall,
            height_of_bricks,
            width_of_opening,
            width_of_wall
        ]
        self.number_mark += 1

    def get(self):
        return self.requests_dict

    def clear(self):
        self.number_mark = 1
        self.requests_dict.clear()

class MakeRequestDictIndividual:

    def __init__(self):
        self.requests_dict = dict()
        self.position_mark = "Б"

    def add(
        self,
        type_of_wall,
        type_of_construction_wall,
        width_of_opening,
        height_of_beam,
        width_of_wall
    ):
        self.requests_dict[f"{self.position_mark}-1"] = [
            type_of_wall,
            type_of_construction_wall,
            width_of_opening,
            height_of_beam,
            width_of_wall
        ]

    def get(self):
        return self.requests_dict

    def clear(self):
        self.requests_dict.clear()


requests_dict = MakeRequestDict()
file_number = 0
file_name = ""


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", title="Головна сторінка", menu=menu, count=len(requests_dict.get()))


@app.route("/clear", methods=["GET", "POST"])
def clear():
    if request.method == "POST":
        if request.form["clear"] == "clear":
            requests_dict.clear()
    return render_template(
        "calculation.html",
        title="Розрахунки", menu=menu,
        data=requests_dict.get(),
        count=len(requests_dict.get())
    )


@app.route("/calculation", methods=["GET", "POST"])
def calculation():
    if request.method == "POST":
        if len(requests_dict.get()) < 10:
            try:
                requests_dict.add(
                    request.form["type_of_wall"],
                    request.form["type_of_construction_wall"],
                    request.form["height_of_bricks"],
                    request.form["width_of_opening"],
                    request.form["width_of_wall"]
                )
                flash("Параметри успішно додано до списку", "flash_ok")
            except:
                flash("Помилка додавання параметрів до списку", "flash_error")
        else:
            flash("Додано максимальну кількість", "flash_error")
    return render_template("calculation.html", title="Розрахунки", menu=menu, data=requests_dict.get(), count=len(requests_dict.get()))


@app.route("/individual", methods=["GET", "POST"])
def individual():
    return render_template("individual.html", title="Розрахунки", menu=menu, data=requests_dict.get(), count=len(requests_dict.get()))


@app.route("/result_page", methods=["GET", "POST"])
def result_page():
    global file_number
    if request.method == "POST":
        if request.form["clear"] == "clear":
            requests_dict.clear()
    return render_template("result_page.html", title="Результат", menu=menu, data=requests_dict.get(), count=len(requests_dict.get()))

@app.route("/result_individual", methods=["GET", "POST"])
def result_individual():
    requests_dict_individual = MakeRequestDictIndividual()
    file_name = f"files/result_individual.pdf"
    if request.method == "POST":
        requests_dict_individual.add(
            request.form["type_of_wall"],
            request.form["type_of_construction_wall"],
            request.form["width_of_opening"],
            request.form["height_of_beam"],
            request.form["width_of_wall"]
        )
        try:
            individualPDF(requests_dict_individual.get(), file_name)
        except:
            flash("Помилка! З даними параметрами неможливо виконати розрахунок. Змініть параметри перерізу.", "flash_error2")
            return render_template("individual.html", title="Розрахунки", menu=menu, data=requests_dict.get(), count=len(requests_dict.get()))
    return render_template("result_individual.html", title="Результат", menu=menu, file=file_name)

@app.route("/about")
def about():
    return render_template("about.html", title="Про нас", menu=menu, count=len(requests_dict.get()))


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.route("/result", methods=["GET", "POST"])
def result():
    cache.clear()
    dict_for_pdf = dict()
    global file_number
    global file_name
    if request.method == "POST":
        file_name = f"files/result_{file_number}.pdf"
        for mark, parameters in requests_dict.get().items():
            package = SelectSerial(parameters)
            if len(package.get_result()) > 0:
                dict_for_pdf[mark] = package.get_result()
            else:
                continue
    serialPDF(dict_for_pdf, file_name)
    return render_template("result.html", title="Результат", file=file_name, count=len(requests_dict.get()))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page404.html", title="Сторінка не знайдена", menu=menu, count=len(requests_dict.get()))


@app.route("/test", methods=["POST", "GET"])
def test():
    return render_template('test.html')


if __name__ == "__main__":
    app.run(debug=True)
