from manim import *
import numpy as np

config.frame_rate = 60

class GeometryProblem(Scene):
    def __init__(self):
        super().__init__()
        self.camera.frame_width = 14
        self.camera.frame_height = 8

    def construct(self):
        self.camera.background_color = BLACK
        
        # Создаем квадрат ABCD
        side_length = 5.0
        A = np.array([-side_length/2, side_length/2, 0])
        B = np.array([side_length/2, side_length/2, 0])
        C = np.array([side_length/2, -side_length/2, 0])
        D = np.array([-side_length/2, -side_length/2, 0])
        
        # Создаем квадрат
        square = Polygon(A, B, C, D, color=BLUE, stroke_width=4)
        
        # Добавляем точки F на DC и E на BC
        F_pos = D + 0.6 * (C - D)  # F находится на 60% от D к C
        E_pos = B + 0.4 * (C - B)  # E находится на 40% от B к C
        
        # Создаем отрезки из A в E и A в F
        AE = Line(A, E_pos, color=WHITE, stroke_width=4)
        AF = Line(A, F_pos, color=WHITE, stroke_width=4)
        
        # Создаем отрезок EF
        EF = Line(E_pos, F_pos, color=GREEN, stroke_width=4)
        
        # Создаем треугольник AEF
        triangle_AEF = Polygon(A, E_pos, F_pos, color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.3)
        
        # Создаем точки
        dot_A = Dot(A, color=WHITE, radius=0.08)
        dot_B = Dot(B, color=WHITE, radius=0.08)
        dot_C = Dot(C, color=WHITE, radius=0.08)
        dot_D = Dot(D, color=WHITE, radius=0.08)
        dot_E = Dot(E_pos, color=WHITE, radius=0.08)
        dot_F = Dot(F_pos, color=WHITE, radius=0.08)
        
        # Подписи точек
        label_A = Text("A", font_size=24, color=WHITE).next_to(A, UP + LEFT, buff=0.15)
        label_B = Text("B", font_size=24, color=WHITE).next_to(B, UP + RIGHT, buff=0.15)
        label_C = Text("C", font_size=24, color=WHITE).next_to(C, DOWN + RIGHT, buff=0.15)
        label_D = Text("D", font_size=24, color=WHITE).next_to(D, DOWN + LEFT, buff=0.15)
        label_E = Text("E", font_size=24, color=WHITE).next_to(E_pos, RIGHT, buff=0.15)
        label_F = Text("F", font_size=24, color=WHITE).next_to(F_pos, DOWN, buff=0.15)
        
        # === ПОСТРОЕНИЕ ГЕОМЕТРИИ ===
        self.play(Create(square), run_time=1.5)
        self.play(
            Create(dot_A), Write(label_A),
            Create(dot_B), Write(label_B),
            Create(dot_C), Write(label_C),
            Create(dot_D), Write(label_D),
            run_time=1
        )
        self.wait(1)
        
        # Показываем точки E и F
        self.play(
            Create(dot_E), Write(label_E),
            Create(dot_F), Write(label_F),
            run_time=1
        )
        self.wait(1)
        
        # Показываем отрезки из A в E и A в F одновременно
        self.play(
            Create(AE),
            Create(AF),
            Create(EF),
            run_time=1.5
        )
        self.wait(1)
        
        # Показываем угол EAF = 45° - ПРАВИЛЬНАЯ ДУГА
        angle_radius = 0.8
        # Вычисляем углы для лучей AE и AF
        vector_AE = E_pos - A
        vector_AF = F_pos - A
        angle_AE = np.arctan2(vector_AE[1], vector_AE[0])
        angle_AF = np.arctan2(vector_AF[1], vector_AF[0])
        
        # Создаем правильную дугу угла
        angle_EAF = Arc(
            radius=angle_radius,
            start_angle=angle_AE,
            angle=angle_AF - angle_AE,
            color=YELLOW,
            stroke_width=4
        ).move_arc_center_to(A)
        
        self.play(Create(angle_EAF), run_time=1)
        self.wait(1)
        

        
        # === ЧИСЛЕННЫЕ ЗНАЧЕНИЯ ===
        
        # Длина EF = 17 (зеленый)
        EF_label = MathTex("17", font_size=24, color=GREEN)
        EF_label.next_to(EF.get_center(), DOWN+RIGHT)
        
        # Угол 45° (желтый)
        angle_label = MathTex("45^\\circ", font_size=24, color=YELLOW)
        # Размещаем метку угла на дуге
        mid_angle = (angle_AE + angle_AF) / 2
        angle_label.move_to(A + (angle_radius + 0.3) * np.array([np.cos(mid_angle), np.sin(mid_angle), 0]))
        
        # Площадь треугольника AEF = 170 (красный)
        area_label = MathTex("170", font_size=32, color=WHITE)
        area_label.move_to(triangle_AEF.get_center(), UP+LEFT)
        
        # Показываем все численные значения одновременно
        self.play(
            Write(EF_label),
            Write(angle_label),
            Write(area_label),
            run_time=1.5
        )
        
        self.wait(3)



#manim -pql main.py GeometryProblem
