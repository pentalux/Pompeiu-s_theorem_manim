from manim import *
import numpy as np

class PompeiuTheorem(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # Создаем равносторонний треугольник
        side_length = 3.0
        triangle = Triangle(side_length=side_length, color=BLUE, stroke_width=4)
        triangle.move_to(ORIGIN)
        
        # Описываем окружность вокруг треугольника
        circumradius = side_length / np.sqrt(3)
        circle = Circle(radius=circumradius, color=WHITE, stroke_width=3)
        circle.move_to(ORIGIN)
        
        # Вершины треугольника
        A, B, C = triangle.get_vertices()
        
        # Начальная точка P на окружности
        angle = 30 * DEGREES  # начальный угол
        P = circle.point_at_angle(angle)
        
        # Создаем отрезки от P к вершинам
        PA = Line(P, A, color=RED, stroke_width=4)
        PB = Line(P, B, color=GREEN, stroke_width=4)  
        PC = Line(P, C, color=YELLOW, stroke_width=4)
        
        # Точки и подписи
        dot_A = Dot(A, color=WHITE, radius=0.08)
        dot_B = Dot(B, color=WHITE, radius=0.08)
        dot_C = Dot(C, color=WHITE, radius=0.08)
        dot_P = Dot(P, color=WHITE, radius=0.1)
        
        label_A = Text("A", font_size=24, color=WHITE).next_to(A, UP, buff=0.15)
        label_B = Text("B", font_size=24, color=WHITE).next_to(B, DOWN + LEFT, buff=0.15)
        label_C = Text("C", font_size=24, color=WHITE).next_to(C, DOWN + RIGHT, buff=0.15)
        label_P = Text("P", font_size=24, color=WHITE).next_to(P, UP + RIGHT, buff=0.15)
        
        # Анимация построения
        self.play(Create(circle), run_time=1.5)
        self.play(Create(triangle), run_time=1.5)
        self.play(
            Create(dot_A), Write(label_A),
            Create(dot_B), Write(label_B), 
            Create(dot_C), Write(label_C),
            run_time=1
        )
        self.wait(1)
        
        # Добавляем точку P и отрезки
        self.play(Create(dot_P), Write(label_P), run_time=1)
        self.play(
            Create(PA),
            Create(PB),
            Create(PC),
            run_time=2
        )
        self.wait(2)
        
        # Подписи отрезков a, b, c (определяем самый длинный)
        lengths = [np.linalg.norm(P - A), np.linalg.norm(P - B), np.linalg.norm(P - C)]
        max_index = np.argmax(lengths)
        
        # Подписи для отрезков
        if max_index == 0:  # PA самый длинный
            c_label = MathTex("c", font_size=28, color=RED).move_to(PA.get_center()).shift(UP * 0.3)
            a_label = MathTex("a", font_size=28, color=GREEN).move_to(PB.get_center()).shift(DOWN * 0.3)
            b_label = MathTex("b", font_size=28, color=YELLOW).move_to(PC.get_center()).shift(DOWN * 0.3)
            segments = [(PA, "c", RED), (PB, "a", GREEN), (PC, "b", YELLOW)]
        elif max_index == 1:  # PB самый длинный
            c_label = MathTex("c", font_size=28, color=GREEN).move_to(PB.get_center()).shift(UP * 0.3)
            a_label = MathTex("a", font_size=28, color=RED).move_to(PA.get_center()).shift(DOWN * 0.3)
            b_label = MathTex("b", font_size=28, color=YELLOW).move_to(PC.get_center()).shift(DOWN * 0.3)
            segments = [(PB, "c", GREEN), (PA, "a", RED), (PC, "b", YELLOW)]
        else:  # PC самый длинный
            c_label = MathTex("c", font_size=28, color=YELLOW).move_to(PC.get_center()).shift(UP * 0.3)
            a_label = MathTex("a", font_size=28, color=RED).move_to(PA.get_center()).shift(DOWN * 0.3)
            b_label = MathTex("b", font_size=28, color=GREEN).move_to(PB.get_center()).shift(DOWN * 0.3)
            segments = [(PC, "c", YELLOW), (PA, "a", RED), (PB, "b", GREEN)]
        
        # Показываем подписи
        self.play(
            Write(c_label),
            Write(a_label),
            Write(b_label),
            run_time=1.5
        )
        self.wait(2)
        
        # Показываем теорему
        theorem_text = MathTex("c = a + b", font_size=36, color=WHITE)
        theorem_text.to_edge(UP)
        
        self.play(Write(theorem_text), run_time=1.5)
        self.wait(2)
        
        # Двигаем точку P по окружности для демонстрации
        for new_angle in [120 * DEGREES, 240 * DEGREES, 300 * DEGREES, 60 * DEGREES]:
            new_P = circle.point_at_angle(new_angle)
            
            # Обновляем отрезки
            new_PA = Line(new_P, A, color=RED, stroke_width=4)
            new_PB = Line(new_P, B, color=GREEN, stroke_width=4)
            new_PC = Line(new_P, C, color=YELLOW, stroke_width=4)
            
            # Обновляем точку P и ее подпись
            new_label_P = Text("P", font_size=24, color=WHITE).next_to(new_P, UP + RIGHT, buff=0.15)
            
            # Определяем самый длинный отрезок для новой позиции
            new_lengths = [np.linalg.norm(new_P - A), np.linalg.norm(new_P - B), np.linalg.norm(new_P - C)]
            new_max_index = np.argmax(new_lengths)
            
            # Обновляем подписи отрезков
            if new_max_index == 0:  # PA самый длинный
                new_c_label = MathTex("c", font_size=28, color=RED).move_to(new_PA.get_center()).shift(UP * 0.3)
                new_a_label = MathTex("a", font_size=28, color=GREEN).move_to(new_PB.get_center()).shift(DOWN * 0.3)
                new_b_label = MathTex("b", font_size=28, color=YELLOW).move_to(new_PC.get_center()).shift(DOWN * 0.3)
            elif new_max_index == 1:  # PB самый длинный
                new_c_label = MathTex("c", font_size=28, color=GREEN).move_to(new_PB.get_center()).shift(UP * 0.3)
                new_a_label = MathTex("a", font_size=28, color=RED).move_to(new_PA.get_center()).shift(DOWN * 0.3)
                new_b_label = MathTex("b", font_size=28, color=YELLOW).move_to(new_PC.get_center()).shift(DOWN * 0.3)
            else:  # PC самый длинный
                new_c_label = MathTex("c", font_size=28, color=YELLOW).move_to(new_PC.get_center()).shift(UP * 0.3)
                new_a_label = MathTex("a", font_size=28, color=RED).move_to(new_PA.get_center()).shift(DOWN * 0.3)
                new_b_label = MathTex("b", font_size=28, color=GREEN).move_to(new_PB.get_center()).shift(DOWN * 0.3)
            
            # Анимация движения
            self.play(
                Transform(PA, new_PA),
                Transform(PB, new_PB),
                Transform(PC, new_PC),
                Transform(dot_P, Dot(new_P, color=WHITE, radius=0.1)),
                Transform(label_P, new_label_P),
                Transform(c_label, new_c_label),
                Transform(a_label, new_a_label),
                Transform(b_label, new_b_label),
                run_time=3
            )
            self.wait(2)
        
        # Финальная пауза
        self.wait(3)