from fpdf import FPDF


temp_list_req = [{'1ПБ16-1': {'length, m': 1.55,
                              'width, m': 0.12,
                              'height, m': 0.065,
                              'maximum loads, kN/m': 1.47,
                              'minimum support, m': 0.1,
                              'volume, m3': 0.012,
                              'weight, kN': 0.294
                              }
                  },
                 {'3ПБ16-37': {'length, m': 1.55,
                               'width, m': 0.12,
                               'height, m': 0.22,
                               'maximum loads, kN/m': 37.3,
                               'minimum support, m': 0.17,
                               'volume, m3': 0.041,
                               'weight, kN': 1.004
                               }
                  },
                 {'5ПБ27-37': {'length, m': 2.72,
                               'width, m': 0.25,
                               'height, m': 0.22,
                               'maximum loads, kN/m': 37.3,
                               'minimum support, m': 0.23,
                               'volume, m3': 0.15,
                               'weight, kN': 3.675
                               }
                  }
                 ]

temp_result_dict = {'ПР-1': ['Перегородка', 'Одна', '65', '', ''],
                    'ПР-2': ['Перегородка', 'Одна', '65', '', '']
                    }


class MakePDF(FPDF):

    def __init__(self, result_dict: dict, filename: str):
        super().__init__()
        count_of_lines = len(result_dict)
        if count_of_lines > 10:
            count_of_lines = 10
        self.form3 = FPDF(orientation='L', unit='mm', format='A3')
        self._draw_form_3()
        self._draw_specification(count_of_lines, 20, 30,
                                'Специфікація пакетів перемичок')
        self._draw_specification(count_of_lines, 20, 30 + 15 + count_of_lines * 8 + 20,
                                'Специфікація елементів перемичок')
        self._draw_statement(count_of_lines, 230, 30)
        annotation = \
        ''' Даний підбір виконано автоматично. Для підтвердження підбору зверніться у проектну організацію'''
        self._annotation(text=annotation)
        self.make_package_of_serial_beam(temp_list_req, 3)
        self.form3.output(f'static/{filename}')

    def make_package_of_serial_beam(self, package: list, n=6):
        scale = 20
        i = 0
        while i < n:
            if i < 5:
                x0 = 265
                y0 = 70 + 4 * 8 * i
                for nested_dict in package:
                    self._draw_serial_beam(list(nested_dict.keys())[0], x0, y0)
                    x0 += nested_dict[list(nested_dict.keys())[0]]['width, m'] * 1000 / scale + 10 / scale
            else:
                x0 = 355
                y0 = 70 + 4 * 8 * (i - 5)
                for nested_dict in package:
                    self._draw_serial_beam(list(nested_dict.keys())[0], x0, y0)
                    x0 += nested_dict[list(nested_dict.keys())[0]]['width, m'] * 1000 / scale + 10 / scale
            i += 1

    def _draw_serial_beam(self, mark: str, x=260, y=70, position: str = '00'):
        x0 = x
        y0 = y
        scale = 20
        if mark[0] == '1':
            b = 120/scale
            h = 65/scale
        elif mark[0] == '2':
            b = 120/scale
            h = 140/scale
        elif mark[0] == '3':
            b = 120/scale
            h = 220/scale
        elif mark[0] == '4':
            b = 120/scale
            h = 290/scale
        elif mark[0] == '5':
            b = 250/scale
            h = 220/scale
        else:
            return f'Помилка перерізу балки'
        self.form3.set_line_width(0.5)
        self.form3.rect(x0, y0, b, -h)
        self.form3.set_line_width(0.05)
        self.form3.line(x0, y0, x0 + b, y0 - h)
        self.form3.line(x0 + b, y0, x0, y0 - h)
        self.form3.line(x0 + b / 2, y0 - h + 1.25, x0 + b / 4, y0 - h - 5)
        self.form3.line(x0 + b / 4, y0 - h - 5, x0 + b / 4 + 4, y0 - h - 5)
        self.form3.ellipse(x0 + b / 2 - 0.5, y0 - h + 0.75, 1, 1, 'F')
        self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
        self.form3.set_font('iso', '', 11)
        self.form3.text(x0 + b / 4 + 0.5, y0 - h - 5.5, position)

    def _draw_form_3(self):
        self.form3.add_page()
        self.form3.set_line_width(0.5)
        self.form3.rect(20, 10, 390, 277)
        self.form3.rect(230, 232, 180, 55)
        self.form3.line(240, 232, 240, 257)
        self.form3.line(250, 232, 250, 287)
        self.form3.line(260, 232, 260, 257)
        self.form3.line(270, 232, 270, 287)
        self.form3.line(285, 232, 285, 287)
        self.form3.line(295, 232, 295, 287)
        self.form3.line(365, 257, 365, 287)
        self.form3.line(380, 257, 380, 272)
        self.form3.line(395, 257, 395, 272)
        self.form3.line(295, 242, 410, 242)
        self.form3.line(230, 252, 295, 252)
        self.form3.line(230, 257, 410, 257)
        self.form3.line(365, 262, 410, 262)
        self.form3.line(295, 272, 410, 272)
        self.form3.set_line_width(0.05)
        self.form3.line(230, 237, 295, 237)
        self.form3.line(230, 242, 295, 242)
        self.form3.line(230, 247, 295, 247)
        self.form3.line(230, 262, 295, 262)
        self.form3.line(230, 267, 295, 267)
        self.form3.line(230, 272, 295, 272)
        self.form3.line(230, 277, 295, 277)
        self.form3.line(230, 282, 295, 282)
        self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
        self.form3.set_font('iso', '', 11)
        self.form3.text(233, 255.75, 'Зм.')
        self.form3.text(240.75, 255.75, 'Кільк.')
        self.form3.text(252, 255.75, 'Арк.')
        self.form3.text(260.5, 255.75, '№док.')
        self.form3.text(273, 255.75, 'Підпис')
        self.form3.text(286, 255.75, 'Дата')
        self.form3.text(367, 260.75, 'Стадія')
        self.form3.text(382.5, 260.75, 'Аркуш')
        self.form3.text(396.25, 260.75, 'Аркушів')
        self.form3.image('static/images/logo_dark.png', 366.25, 273.25, 42.5, 12.5)
        
    def _draw_specification(self, count_of_lines: int, x=230, y=30, title: str = 'Специфікація'):
        x0 = x
        y0 = y
        self.form3.set_line_width(0.5)
        self.form3.line(x0 + 0, y0 + 0, x0 + 180, y0 + 0)
        self.form3.line(x0 + 0, y0 + 15, x0 + 180, y0 + 15)
        self.form3.line(x0 + 0, y0 + 0, x0 + 0, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 15, y0 + 0, x0 + 15, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 75, y0 + 0, x0 + 75, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 135, y0 + 0, x0 + 135, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 145, y0 + 0, x0 + 145, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 160, y0 + 0, x0 + 160, y0 + 15 + count_of_lines * 8)
        self.form3.line(x0 + 180, y0 + 0, x0 + 180, y0 + 15 + count_of_lines * 8)
        y = y0 + 23
        i = 0
        self.form3.set_line_width(0.05)
        while i < count_of_lines:
            self.form3.line(x0 + 0, y, x0 + 180, y)
            i += 1
            y += 8
        self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
        self.form3.set_font('iso', '', 14)
        self.form3.text(x0 + 65, y0 - 5, title)
        self.form3.set_font('iso', '', 11)
        self.form3.text(x0 + 5, y0 + 9.25, 'Поз.')
        self.form3.text(x0 + 35, y0 + 9.25, 'Позначення')
        self.form3.text(x0 + 94, y0 + 9.25, 'Найменування')
        self.form3.text(x0 + 135.5, y0 + 9.25, 'Кільк.')
        self.form3.text(x0 + 145.3, y0 + 7.25, 'Маса од.,')
        self.form3.text(x0 + 151, y0 + 11, 'кг')
        self.form3.text(x0 + 163, y0 + 9.25, 'Примітка')

    def _draw_statement(self, count_of_lines: int, x=230, y=30, title: str = 'Відомість перемичок'):
        x0 = x
        y0 = y
        self.form3.set_line_width(0.5)
        self.form3.line(x0 + 0, y0 + 0, x0 + 90, y0 + 0)
        self.form3.line(x0 + 0, y0 + 15, x0 + 90, y0 + 15)
        self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
        if count_of_lines <= 5:
            self.form3.set_font('iso', '', 14)
            self.form3.text(x0 + 25, y0 - 5, title)
            self.form3.set_font('iso', '', 11)
            self.form3.text(x0 + 5, y0 + 9.25, 'Марка')
            self.form3.text(x0 + 42, y0 + 9.25, 'Схема перерізу')
            self.form3.line(x0 + 0, y0 + 0, x0 + 0, y0 + 15 + count_of_lines * 8 * 4)
            self.form3.line(x0 + 20, y0 + 0, x0 + 20, y0 + 15 + count_of_lines * 8 * 4)
            self.form3.line(x0 + 90, y0 + 0, x0 + 90, y0 + 15 + count_of_lines * 8 * 4)
        elif 5 < count_of_lines <= 10:
            self.form3.set_font('iso', '', 14)
            self.form3.text(x0 + 70, y0 - 5, title)
            self.form3.set_font('iso', '', 11)
            self.form3.text(x0 + 5, y0 + 9.25, 'Марка')
            self.form3.text(x0 + 42, y0 + 9.25, 'Схема перерізу')
            self.form3.text(x0 + 95, y0 + 9.25, 'Марка')
            self.form3.text(x0 + 132, y0 + 9.25, 'Схема перерізу')
            self.form3.line(x0 + 0, y0 + 0, x0 + 0, y0 + 15 + 5 * 8 * 4)
            self.form3.line(x0 + 20, y0 + 0, x0 + 20, y0 + 15 + 5 * 8 * 4)
            self.form3.line(x0 + 90, y0 + 0, x0 + 90, y0 + 15 + 5 * 8 * 4)
            self.form3.line(x0 + 90, y0 + 0, x0 + 180, y0 + 0)
            self.form3.line(x0 + 90, y0 + 15, x0 + 180, y0 + 15)
            self.form3.line(x0 + 110, y0 + 0, x0 + 110, y0 + 15 + (count_of_lines - 5) * 8 * 4)
            self.form3.line(x0 + 180, y0 + 0, x0 + 180, y0 + 15 + (count_of_lines - 5) * 8 * 4)
        else:
            self.form3.set_font('iso', '', 14)
            self.form3.text(x0 + 70, y0 - 5, title)
            self.form3.set_font('iso', '', 11)
            self.form3.text(x0 + 5, y0 + 9.25, 'Марка')
            self.form3.text(x0 + 42, y0 + 9.25, 'Схема перерізу')
            self.form3.text(x0 + 95, y0 + 9.25, 'Марка')
            self.form3.text(x0 + 132, y0 + 9.25, 'Схема перерізу')
            self.form3.line(x0 + 0, y0 + 0, x0 + 0, y0 + 15 + 5 * 8 * 4)
            self.form3.line(x0 + 20, y0 + 0, x0 + 20, y0 + 15 + 5 * 8 * 4)
            self.form3.line(x0 + 90, y0 + 0, x0 + 90, y0 + 15 + 5 * 8 * 4)
            self.form3.line(x0 + 90, y0 + 0, x0 + 180, y0 + 0)
            self.form3.line(x0 + 90, y0 + 15, x0 + 180, y0 + 15)
            self.form3.line(x0 + 110, y0 + 0, x0 + 110, y0 + 15 + 5 * 8 * 4)
            self.form3.line(x0 + 180, y0 + 0, x0 + 180, y0 + 15 + 5 * 8 * 4)
        self.form3.set_line_width(0.05)
        y = y0 + 47
        i = 0
        while i < count_of_lines and i < 5:
            self.form3.line(x0 + 0, y, x0 + 90, y)
            i += 1
            y += 8 * 4
        y = y0 + 47
        while count_of_lines > i >= 5 and i < 10:
            self.form3.line(x0 + 90, y, x0 + 180, y)
            i += 1
            y += 8 * 4

    def _annotation(self, text: str = 'Примітка', x=30, y=257):
        self.form3.add_font('iso', '', 'static/ISOCPEUR/ISOCPEUR.ttf', uni=True)
        self.form3.set_font('iso', '', 11)
        self.form3.set_xy(x, y)
        self.form3.write(5, text)


# MakePDF(temp_result_dict, 'files/result_test.pdf')
