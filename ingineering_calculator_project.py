import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
import numpy as np

class History:
    def __init__(self):
        self._history = []
    
    def add(self, category, operation, result):
        self._history.append({"category": category, "operation": operation, "result": result})
    
    def clear(self):
        self._history.clear()


class TrigCalculator:
    def __init__(self, history, mode='deg'):
        self._history = history
        self.mode = mode
        self._to_rad = math.radians if mode == 'deg' else lambda x: x
        self._from_rad = math.degrees if mode == 'deg' else lambda x: x
    
    def _add_record(self, name, a, result):
        suffix = "°" if self.mode == 'deg' else ""
        self._history.add("Тригонометрия", f"{name}({a}{suffix}) = ", result)
    
    def sin(self, a):
        result = math.sin(self._to_rad(a))
        self._add_record("sin", a, result)
        return result
    
    def cos(self, a):
        result = math.cos(self._to_rad(a))
        self._add_record("cos", a, result)
        return result
    
    def tan(self, a):
        if (self.mode == 'deg' and a in (90, 270)) or (self.mode != 'deg' and a in (math.pi/2, 3*math.pi/2)):
            self._history.add("Тригонометрия", f"tan({a}) = ", "ОШИБКА!")
            return "Ошибка! tan не определен"
        result = math.tan(self._to_rad(a))
        self._add_record("tan", a, result)
        return result
    
    def asin(self, a):
        if not -1 <= a <= 1:
            self._history.add("Тригонометрия", f"asin({a}) = ", "ОШИБКА!")
            return "Ошибка! asin только от -1 до 1"
        result = self._from_rad(math.asin(a))
        self._add_record("asin", a, result)
        return result
    
    def acos(self, a):
        if not -1 <= a <= 1:
            self._history.add("Тригонометрия", f"acos({a}) = ", "ОШИБКА!")
            return "Ошибка! acos только от -1 до 1"
        result = self._from_rad(math.acos(a))
        self._add_record("acos", a, result)
        return result
    
    def atan(self, a):
        result = self._from_rad(math.atan(a))
        self._add_record("atan", a, result)
        return result


class BasedCalculator:
    def __init__(self, history):
        self._history = history
    
    def add(self, a, b):
        result = a + b
        self._history.add("Арифметика", f"{a}+{b} = ", result)
        return result
    
    def minus(self, a, b):
        result = a - b
        self._history.add("Арифметика", f"{a}-{b} = ", result)
        return result
    
    def mul(self, a, b):
        result = a * b
        self._history.add("Арифметика", f"{a}*{b} = ", result)
        return result
    
    def div(self, a, b):
        if b == 0:
            return "Ошибка! Деление на ноль!"
        result = a / b
        self._history.add("Арифметика", f"{a}/{b} = ", result)
        return result
    
    def pow(self, a, b):
        result = a ** b
        self._history.add("Арифметика", f"{a}^{b} = ", result)
        return result
    
    def root(self, a, b):
        if b == 0:
            return "Ошибка! Корень нулевой степени!"
        result = a ** (1/b)
        self._history.add("Арифметика", f"корень {b}-й степени из {a} = ", result)
        return result


class IntegrationCalculator:
    def __init__(self, history):
        self._history = history
        self.functions = {
            'square': lambda x: x**2,
            'sine': math.sin,
            'cosine': math.cos,
            'linear': lambda x: 3*x + 1,
            'cubic': lambda x: x**3,
            'exp': math.exp
        }
    
    def integrate(self, name, a, b, n=1000):
        if name not in self.functions:
            raise ValueError(f"Функция '{name}' не найдена!")
        func = self.functions[name]
        h = (b - a) / n
        total = 0.5 * (func(a) + func(b))
        for i in range(1, n):
            total += func(a + i * h)
        result = total * h
        self._history.add("Интегрирование", f"∫ от {a} до {b} для {name} (n={n}) = ", result)
        return result


class MatrixCalculator:
    def __init__(self, history):
        self._history = history
    
    def _validate(self, m, name="Матрица"):
        if not all(isinstance(row, list) for row in m):
            raise ValueError(f"{name} должна быть списком списков.")
        if not m or not m[0]:
            raise ValueError(f"{name} не может быть пустой.")
        cols = len(m[0])
        for i, row in enumerate(m):
            if len(row) != cols:
                raise ValueError(f"{name}: строка {i} имеет длину {len(row)} вместо {cols}.")
    
    def _det(self, m):
        n = len(m)
        if n == 1: return m[0][0]
        if n == 2: return m[0][0]*m[1][1] - m[0][1]*m[1][0]
        return sum((-1)**j * m[0][j] * self._det([row[:j] + row[j+1:] for row in m[1:]]) for j in range(n))
    
    def add(self, A, B):
        self._validate(A); self._validate(B)
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Матрицы должны быть одного размера!")
        result = [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
        self._history.add("Матрицы", f"Сложение\n{A}\n+\n{B} = ", result)
        return result
    
    def subtract(self, A, B):
        self._validate(A); self._validate(B)
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Матрицы должны быть одного размера!")
        result = [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
        self._history.add("Матрицы", f"Вычитание\n{A}\n-\n{B} = ", result)
        return result
    
    def multiply(self, A, B):
        self._validate(A); self._validate(B)
        if len(A[0]) != len(B):
            raise ValueError("Число столбцов A должно равняться числу строк B!")
        result = [[sum(A[i][k] * B[k][j] for k in range(len(A[0]))) for j in range(len(B[0]))] for i in range(len(A))]
        self._history.add("Матрицы", f"Умножение\n{A}\n@\n{B} = ", result)
        return result
    
    def transpose(self, M):
        self._validate(M)
        result = [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
        self._history.add("Матрицы", f"Транспонирование\n{M} = ", result)
        return result
    
    def determinant(self, M):
        self._validate(M)
        if len(M) != len(M[0]):
            raise ValueError("Определитель только для квадратных матриц!")
        result = self._det(M)
        self._history.add("Матрицы", f"Определитель\n{M} = ", result)
        return result
    
    def inverse(self, M):
        self._validate(M)
        n = len(M)
        if n != len(M[0]):
            raise ValueError("Обратная только для квадратных матриц!")
        det = self.determinant(M)
        if det == 0:
            raise ValueError("Матрица вырождена!")
        
        def _det_no_history(m):
            if len(m) == 1: return m[0][0]
            if len(m) == 2: return m[0][0]*m[1][1] - m[0][1]*m[1][0]
            return sum((-1)**j * m[0][j] * _det_no_history([row[:j] + row[j+1:] for row in m[1:]]) for j in range(len(m)))
        
        cofactors = [[((-1)**(i+j)) * _det_no_history([row[:j] + row[j+1:] for row in (M[:i] + M[i+1:])]) for j in range(n)] for i in range(n)]
        adjugate = [[cofactors[j][i] for j in range(n)] for i in range(n)]
        inv = [[adjugate[i][j] / det for j in range(n)] for i in range(n)]
        self._history.add("Матрицы", f"Обратная к\n{M} = ", inv)
        return inv


class GraphCalculator:
    def __init__(self, history):
        self._history = history
        self.x = np.linspace(-10, 10, 500)
    
    def plot(self, *functions):
        if not functions:
            print("Нет функций для построения!")
            return
        
        fig, ax = plt.subplots(figsize=(11, 6))
        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
        
        for i, expr in enumerate(functions):
            try:
                y = eval(expr, {"np": np, "x": self.x, "__builtins__": {}})
                y = np.array(y)
                mask = np.isfinite(y)
                if np.any(mask):
                    ax.plot(self.x[mask], y[mask], linewidth=2, 
                           label=f"y={expr}", color=colors[i % len(colors)])
                    self._history.add("Графики", f"Построение y={expr}", "Успешно")
                else:
                    print(f"Функция {expr} не имеет допустимых значений")
            except Exception as e:
                print(f"Ошибка в {expr}: {e}")
                self._history.add("Графики", f"Построение y={expr}", f"Ошибка: {type(e).__name__}")
        
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xlabel("X"); ax.set_ylabel("Y")
        ax.set_xlim(-10, 10)
        fig.tight_layout()
        plt.show()


class EngineeringCalc:
    def __init__(self, mode='deg'):
        self._history = History()
        self.arithmetic = BasedCalculator(self._history)
        self.trig = TrigCalculator(self._history, mode)
        self.integration = IntegrationCalculator(self._history)
        self.matrix = MatrixCalculator(self._history)
        self.graph = GraphCalculator(self._history)
        self.mode = mode


class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Инженерный калькулятор")
        self.root.geometry("750x600")
        self.root.resizable(False, False)

        self.calculator = EngineeringCalc('deg')

        self.create_widgets()
        self.update_history()

    def create_widgets(self):
        self.tabs = ttk.Notebook(self.root)

        self.arithmetic_tab = ttk.Frame(self.tabs)
        self.trigonometry_tab = ttk.Frame(self.tabs)
        self.integration_tab = ttk.Frame(self.tabs)
        self.matrix_tab = ttk.Frame(self.tabs)
        self.graph_tab = ttk.Frame(self.tabs)
        self.history_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.arithmetic_tab, text="Арифметика")
        self.tabs.add(self.trigonometry_tab, text="Тригонометрия")
        self.tabs.add(self.integration_tab, text="Интегралы")
        self.tabs.add(self.matrix_tab, text="Матрицы")
        self.tabs.add(self.graph_tab, text="Графики")
        self.tabs.add(self.history_tab, text="История")

        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.create_arithmetic_tab()
        self.create_trigonometry_tab()
        self.create_integration_tab()
        self.create_matrix_tab()
        self.create_graph_tab()
        self.create_history_tab()

    # ---------- АРИФМЕТИКА ----------

    def create_arithmetic_tab(self):
        title = ttk.Label(
            self.arithmetic_tab,
            text="Арифметика",
            font=("Arial", 16)
        )
        title.pack(pady=10)

        input_frame = ttk.Frame(self.arithmetic_tab)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Первое число:").grid(row=0, column=0, padx=5, pady=5)
        self.first_number_entry = ttk.Entry(input_frame, width=25)
        self.first_number_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Второе число:").grid(row=1, column=0, padx=5, pady=5)
        self.second_number_entry = ttk.Entry(input_frame, width=25)
        self.second_number_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Операция:").grid(row=2, column=0, padx=5, pady=5)

        self.arithmetic_operation = ttk.Combobox(
            input_frame,
            values=[
                "Сложение (+)",
                "Вычитание (-)",
                "Умножение (*)",
                "Деление (/)",
                "Степень (**)",
                "Корень"
            ],
            state="readonly",
            width=22
        )
        self.arithmetic_operation.grid(row=2, column=1, padx=5, pady=5)
        self.arithmetic_operation.current(0)

        calculate_button = ttk.Button(
            self.arithmetic_tab,
            text="Вычислить",
            command=self.calculate_arithmetic
        )
        calculate_button.pack(pady=15)

        self.arithmetic_result_label = ttk.Label(
            self.arithmetic_tab,
            text="Результат: ",
            font=("Arial", 13)
        )
        self.arithmetic_result_label.pack(pady=10)

    def calculate_arithmetic(self):
        try:
            a = self.get_float_from_entry(self.first_number_entry, "первое число")
            b = self.get_float_from_entry(self.second_number_entry, "второе число")

            operation = self.arithmetic_operation.get()

            if operation == "Сложение (+)":
                result = self.calculator.arithmetic.add(a, b)
            elif operation == "Вычитание (-)":
                result = self.calculator.arithmetic.minus(a, b)
            elif operation == "Умножение (*)":
                result = self.calculator.arithmetic.mul(a, b)
            elif operation == "Деление (/)":
                result = self.calculator.arithmetic.div(a, b)
            elif operation == "Степень (**)":
                result = self.calculator.arithmetic.pow(a, b)
            elif operation == "Корень":
                result = self.calculator.arithmetic.root(a, b)
            else:
                raise ValueError("Неизвестная операция")

            self.arithmetic_result_label.config(text=f"Результат: {result}")
            self.update_history()

        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    # ---------- ТРИГОНОМЕТРИЯ ----------

    def create_trigonometry_tab(self):
        title = ttk.Label(
            self.trigonometry_tab,
            text="Тригонометрия",
            font=("Arial", 16)
        )
        title.pack(pady=10)

        input_frame = ttk.Frame(self.trigonometry_tab)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Значение:").grid(row=0, column=0, padx=5, pady=5)
        self.angle_entry = ttk.Entry(input_frame, width=25)
        self.angle_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Режим:").grid(row=1, column=0, padx=5, pady=5)

        self.angle_mode = ttk.Combobox(
            input_frame,
            values=["deg (градусы)", "rad (радианы)"],
            state="readonly",
            width=22
        )
        self.angle_mode.grid(row=1, column=1, padx=5, pady=5)
        self.angle_mode.current(0)

        ttk.Label(input_frame, text="Функция:").grid(row=2, column=0, padx=5, pady=5)

        self.trigonometry_operation = ttk.Combobox(
            input_frame,
            values=[
                "sin",
                "cos",
                "tan",
                "asin",
                "acos",
                "atan"
            ],
            state="readonly",
            width=22
        )
        self.trigonometry_operation.grid(row=2, column=1, padx=5, pady=5)
        self.trigonometry_operation.current(0)

        calculate_button = ttk.Button(
            self.trigonometry_tab,
            text="Вычислить",
            command=self.calculate_trigonometry
        )
        calculate_button.pack(pady=15)

        self.trigonometry_result_label = ttk.Label(
            self.trigonometry_tab,
            text="Результат: ",
            font=("Arial", 13)
        )
        self.trigonometry_result_label.pack(pady=10)

    def calculate_trigonometry(self):
        try:
            value = self.get_float_from_entry(self.angle_entry, "значение")
            operation = self.trigonometry_operation.get()
            mode = self.angle_mode.get()
            
            if "градусы" in mode:
                self.calculator.trig.mode = 'deg'
            else:
                self.calculator.trig.mode = 'rad'

            if operation == "sin":
                result = self.calculator.trig.sin(value)
            elif operation == "cos":
                result = self.calculator.trig.cos(value)
            elif operation == "tan":
                result = self.calculator.trig.tan(value)
            elif operation == "asin":
                result = self.calculator.trig.asin(value)
            elif operation == "acos":
                result = self.calculator.trig.acos(value)
            elif operation == "atan":
                result = self.calculator.trig.atan(value)
            else:
                raise ValueError("Неизвестная функция")

            self.trigonometry_result_label.config(text=f"Результат: {result}")
            self.update_history()

        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    # ---------- ИНТЕГРАЛЫ ----------

    def create_integration_tab(self):
        title = ttk.Label(
            self.integration_tab,
            text="Интегрирование",
            font=("Arial", 16)
        )
        title.pack(pady=10)

        input_frame = ttk.Frame(self.integration_tab)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Имя функции:").grid(row=0, column=0, padx=5, pady=5)
        self.func_name_entry = ttk.Entry(input_frame, width=25)
        self.func_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.func_name_entry.insert(0, "square")

        ttk.Label(input_frame, text="Нижняя граница:").grid(row=1, column=0, padx=5, pady=5)
        self.lower_limit_entry = ttk.Entry(input_frame, width=25)
        self.lower_limit_entry.grid(row=1, column=1, padx=5, pady=5)
        self.lower_limit_entry.insert(0, "0")

        ttk.Label(input_frame, text="Верхняя граница:").grid(row=2, column=0, padx=5, pady=5)
        self.upper_limit_entry = ttk.Entry(input_frame, width=25)
        self.upper_limit_entry.grid(row=2, column=1, padx=5, pady=5)
        self.upper_limit_entry.insert(0, "2")

        ttk.Label(input_frame, text="Шагов (n):").grid(row=3, column=0, padx=5, pady=5)
        self.steps_entry = ttk.Entry(input_frame, width=25)
        self.steps_entry.grid(row=3, column=1, padx=5, pady=5)
        self.steps_entry.insert(0, "1000")

        calculate_button = ttk.Button(
            self.integration_tab,
            text="Вычислить интеграл",
            command=self.calculate_integral
        )
        calculate_button.pack(pady=15)

        funcs_frame = ttk.Frame(self.integration_tab)
        funcs_frame.pack(pady=10)
        
        ttk.Label(funcs_frame, text="Доступные функции:").pack()
        self.funcs_list = tk.Text(funcs_frame, width=50, height=6, state="disabled")
        self.funcs_list.pack()
        self.update_funcs_list()

        self.integral_result_label = ttk.Label(
            self.integration_tab,
            text="Результат: ",
            font=("Arial", 13)
        )
        self.integral_result_label.pack(pady=10)

    def update_funcs_list(self):
        self.funcs_list.config(state="normal")
        self.funcs_list.delete("1.0", tk.END)
        for name in self.calculator.integration.functions:
            self.funcs_list.insert(tk.END, f"  • {name}\n")
        self.funcs_list.config(state="disabled")

    def calculate_integral(self):
        try:
            func_name = self.func_name_entry.get().strip()
            a = self.get_float_from_entry(self.lower_limit_entry, "нижняя граница")
            b = self.get_float_from_entry(self.upper_limit_entry, "верхняя граница")
            n = int(self.steps_entry.get().strip()) if self.steps_entry.get().strip() else 1000

            result = self.calculator.integration.integrate(func_name, a, b, n)
            self.integral_result_label.config(text=f"Результат: {result}")
            self.update_history()

        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    # ---------- МАТРИЦЫ ----------

    def create_matrix_tab(self):
        title = ttk.Label(
            self.matrix_tab,
            text="Матрицы",
            font=("Arial", 16)
        )
        title.pack(pady=10)

        input_frame = ttk.Frame(self.matrix_tab)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Матрица A:").grid(row=0, column=0, padx=5, pady=5)
        self.matrix_a_entry = ttk.Entry(input_frame, width=45)
        self.matrix_a_entry.grid(row=0, column=1, padx=5, pady=5)
        self.matrix_a_entry.insert(0, "[[1,2],[3,4]]")

        ttk.Label(input_frame, text="Матрица B:").grid(row=1, column=0, padx=5, pady=5)
        self.matrix_b_entry = ttk.Entry(input_frame, width=45)
        self.matrix_b_entry.grid(row=1, column=1, padx=5, pady=5)
        self.matrix_b_entry.insert(0, "[[5,6],[7,8]]")

        ttk.Label(input_frame, text="Операция:").grid(row=2, column=0, padx=5, pady=5)

        self.matrix_operation = ttk.Combobox(
            input_frame,
            values=[
                "Сложение",
                "Вычитание",
                "Умножение",
                "Транспонирование (A)",
                "Определитель (A)",
                "Обратная (A)"
            ],
            state="readonly",
            width=30
        )
        self.matrix_operation.grid(row=2, column=1, padx=5, pady=5)
        self.matrix_operation.current(0)

        calculate_button = ttk.Button(
            self.matrix_tab,
            text="Вычислить",
            command=self.calculate_matrix
        )
        calculate_button.pack(pady=15)

        self.matrix_result_label = ttk.Label(
            self.matrix_tab,
            text="Результат: ",
            font=("Arial", 11)
        )
        self.matrix_result_label.pack(pady=10)

    def calculate_matrix(self):
        try:
            operation = self.matrix_operation.get()
            
            if operation in ["Транспонирование (A)", "Определитель (A)", "Обратная (A)"]:
                A = eval(self.matrix_a_entry.get().strip())
                
                if operation == "Транспонирование (A)":
                    result = self.calculator.matrix.transpose(A)
                elif operation == "Определитель (A)":
                    result = self.calculator.matrix.determinant(A)
                elif operation == "Обратная (A)":
                    result = self.calculator.matrix.inverse(A)
            else:
                A = eval(self.matrix_a_entry.get().strip())
                B = eval(self.matrix_b_entry.get().strip())
                
                if operation == "Сложение":
                    result = self.calculator.matrix.add(A, B)
                elif operation == "Вычитание":
                    result = self.calculator.matrix.subtract(A, B)
                elif operation == "Умножение":
                    result = self.calculator.matrix.multiply(A, B)

            self.matrix_result_label.config(text=f"Результат:\n{result}")
            self.update_history()

        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    # ---------- ГРАФИКИ ----------

    def create_graph_tab(self):
        title = ttk.Label(
            self.graph_tab,
            text="Построение графиков",
            font=("Arial", 16)
        )
        title.pack(pady=10)

        input_frame = ttk.Frame(self.graph_tab)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Функции (через запятую):").grid(row=0, column=0, padx=5, pady=5)
        self.graph_func_entry = ttk.Entry(input_frame, width=45)
        self.graph_func_entry.grid(row=0, column=1, padx=5, pady=5)
        self.graph_func_entry.insert(0, "np.sin(x), np.cos(x)")

        ttk.Label(input_frame, text="Примеры: np.sin(x), np.cos(x), x**2, np.exp(x)").grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        plot_button = ttk.Button(
            self.graph_tab,
            text="Построить график",
            command=self.plot_graph
        )
        plot_button.pack(pady=15)

        self.graph_result_label = ttk.Label(
            self.graph_tab,
            text="График откроется в новом окне",
            font=("Arial", 11)
        )
        self.graph_result_label.pack(pady=10)

    def plot_graph(self):
        try:
            funcs_str = self.graph_func_entry.get().strip()
            if not funcs_str:
                messagebox.showerror("Ошибка", "Введите хотя бы одну функцию!")
                return
            
            functions = [f.strip() for f in funcs_str.split(',') if f.strip()]
            
            if functions:
                self.calculator.graph.plot(*functions)
                self.update_history()
            else:
                messagebox.showerror("Ошибка", "Нет корректных функций!")
                
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    # ---------- ИСТОРИЯ ----------

    def create_history_tab(self):
        title = ttk.Label(
            self.history_tab,
            text="История вычислений",
            font=("Arial", 16)
        )
        title.pack(pady=10)

        self.history_text = tk.Text(
            self.history_tab,
            width=80,
            height=20,
            state="disabled",
            wrap=tk.WORD
        )
        self.history_text.pack(pady=10)

        button_frame = ttk.Frame(self.history_tab)
        button_frame.pack(pady=5)

        update_button = ttk.Button(
            button_frame,
            text="Обновить",
            command=self.update_history
        )
        update_button.grid(row=0, column=0, padx=5)

        clear_button = ttk.Button(
            button_frame,
            text="Очистить историю",
            command=self.clear_history
        )
        clear_button.grid(row=0, column=1, padx=5)

    def update_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)

        records = self.calculator._history._history

        if not records:
            self.history_text.insert(tk.END, "📭 История пуста.")
        else:
            for index, record in enumerate(records, start=1):
                category = record.get("category", "Неизвестно")
                operation = record.get("operation", "")
                result = record.get("result", "")
                
                line = f"{index}. [{category}] {operation}{result}\n"
                self.history_text.insert(tk.END, line)

        self.history_text.config(state="disabled")

    def clear_history(self):
        self.calculator._history.clear()
        self.update_history()
        messagebox.showinfo("История", "🗑️ История очищена.")

    # ---------- ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ----------

    def get_float_from_entry(self, entry, field_name):
        value = entry.get().strip().replace(",", ".")

        if value == "":
            raise ValueError(f"Поле '{field_name}' не должно быть пустым")

        try:
            return float(value)
        except ValueError:
            raise ValueError(f"В поле '{field_name}' должно быть число")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()