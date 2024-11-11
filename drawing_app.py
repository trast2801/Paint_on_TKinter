import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        '''Метод инициализирует приложение для рисования'''
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.color_preview = tk.Label(root, width=20, height=2, bg='white', relief=tk.RAISED, borderwidth=1)
        self.color_preview.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)
        self.root.bind('<Control-s>', self.save_image)  # Добавление горячих клавиш для сохранения
        self.root.bind('<Control-c>', self.choose_color)  # Добавление горячих клавиш для выбора цвета

    def setup_ui(self):
        '''Метод отвечает за создание и расположение виджетов управления.'''
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        '''Создание выпадающего списка.Выбор размера кисти из списка'''
        brush_sizes = [1, 2, 5, 10]
        self.brush_size = tk.IntVar()
        self.brush_size.set(2)  # Установка начального значения
        brush_size_option = tk.OptionMenu(self.root, self.brush_size, *brush_sizes)
        brush_size_option.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

        erase_button = tk.Button(control_frame, text="Ластик", command=self.erase)
        erase_button.pack(side=tk.LEFT)

        resize_button = tk.Button(control_frame, text="Изменить размер холста", command=self.resize_canvas)
        resize_button.pack(side=tk.LEFT)


    def paint(self, event):
        '''Метод для рисования на холсте при движени мыши.'''
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        '''Метод сбрасывает последние координаты кисти.'''
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        '''Метод очищает холст.'''
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        '''Метод для выбора цвета кисти.'''
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.update_color_preview()

    def get_canvas_color(self):
        '''метод получает текущий фон '''
        color = self.canvas['bg']
        return color

    def erase(self):
        '''Метод отвечает за действие ластика.'''
        self.canvas.pack()
        self.pen_color = self.get_canvas_color()

        # self.pen_color = 'white'

    def pick_color(self, event):
        ''' Метод для выбора цвета пипеткой.'''
        x, y = event.x, event.y
        pixel_color = self.image.getpixel((x, y))
        self.pen_color = '#%02x%02x%02x' % pixel_color
        # self.pen_color = pixel_color
        print(f"Выбран цвет: {self.pen_color}")
        self.update_color_preview()

    def save_image(self, event=None):
        '''Метод сохраняет изображение.'''
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def update_color_preview(self):
        '''Метод для предварительного просмотра цвета кисти'''
        self.color_preview.config(bg=self.pen_color)


    def resize_canvas(self):
        '''Метод для изменения размеров холста'''
        width = simpledialog.askinteger("Введите ширину", "Введите новую ширину холста(пикселях):")
        height = simpledialog.askinteger("Введите высоту", "Введите новую высоту холста(пикселях):")

        if width is not None and height is not None:
            self.canvas.config(width=width, height=height)  # Изменяем размер холста
            self.image = Image.new("RGB", (width, height),
                                   "white")  # Создаем новый объект изображения с новыми размерами
            self.draw = ImageDraw.Draw(self.image)  # Обновляем self.draw
            self.clear_canvas()  # Очистка холста после изменения размера

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
