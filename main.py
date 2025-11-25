from manim import *
import numpy as np


class SemicircleProblem(Scene):
    def __init__(self):
        super().__init__()
        self.camera.frame_width = 14
        self.camera.frame_height = 8
    
    def construct(self):
        self.camera.background_color = BLACK
        
        # === ПРАВИЛЬНАЯ ГЕОМЕТРИЯ ===
        R_big = 3.0  # Радиус большой полуокружности
        
        # Большая полуокружность (вверх) - ТОЛЩЕ
        semicircle = Arc(
            radius=R_big,
            start_angle=0,
            angle=PI,
            color=RED,
            stroke_width=6
        )
        
        # Диаметр AB - ТОЛЩЕ
        A = LEFT * R_big
        B = RIGHT * R_big
        diameter = Line(A, B, color=WHITE, stroke_width=4)
        
        self.play(Create(semicircle), run_time=2)
        self.play(Create(diameter), run_time=1)
        
        # Точки A и B
        dot_A = Dot(A, color=WHITE, radius=0.1)
        dot_B = Dot(B, color=WHITE, radius=0.1)
        label_A = Text("A", font_size=32, color=WHITE).next_to(A, DOWN, buff=0.2)
        label_B = Text("B", font_size=32, color=WHITE).next_to(B, DOWN, buff=0.2)
        
        self.play(
            Create(dot_A), Write(label_A),
            Create(dot_B), Write(label_B),
            run_time=1
        )
        
        # === МАЛАЯ ОКРУЖНОСТЬ - ТОЧНО КАСАЕТСЯ ДУГИ AB И ДИАМЕТРА ===
        r = 1.3  # УВЕЛИЧЕННЫЙ радиус
        
        # Центр малой окружности должен быть на расстоянии R_big - r от центра большой
        # И на высоте r от диаметра (чтобы касаться диаметра)
        # Решаем: x^2 + r^2 = (R_big - r)^2
        x_small = np.sqrt((R_big - r)**2 - r**2)
        O_small = np.array([x_small, r, 0])  # Точно касается и диаметра и дуги
        
        small_circle = Circle(radius=r, color=BLUE, stroke_width=4)
        small_circle.move_to(O_small)
        
        self.play(Create(small_circle), run_time=1.5)
        
        # Центр малой окружности
        dot_O_small = Dot(O_small, color=WHITE, radius=0.08)
        self.play(Create(dot_O_small), run_time=0.5)
        
        # Радиус r - ТОЛЩЕ
        r_line = Line(O_small, O_small + RIGHT * r, color=GREEN, stroke_width=4)
        r_label = Text("r", font_size=28, color=GREEN).next_to(r_line, UP, buff=0.15)
        
        self.play(Create(r_line), Write(r_label), run_time=1)
        
        # Точка T - касание малой окружности с диаметром
        T = np.array([O_small[0], 0, 0])
        dot_T = Dot(T, color=WHITE, radius=0.1)
        label_T = Text("T", font_size=32, color=WHITE).next_to(T, DOWN, buff=0.2)
        
        self.play(
            Create(dot_T), Write(label_T),
            run_time=1
        )
        
        # Точка E - касание малой и большой окружности
        # Лежит на линии, соединяющей центры
        vec_centers = O_small - ORIGIN
        vec_centers_norm = vec_centers / np.linalg.norm(vec_centers)
        E = ORIGIN + vec_centers_norm * R_big
        
        dot_E = Dot(E, color=WHITE, radius=0.08)
        label_E = Text("E", font_size=28, color=WHITE).next_to(E, UP, buff=0.15)
        
        self.play(Create(dot_E), Write(label_E), run_time=1)
        
        # === КАСАТЕЛЬНАЯ ИЗ A К МАЛОЙ ОКРУЖНОСТИ ===
        
        def find_tangent_point_from_A(A, O, r):
            """Находит точку касания C из точки A к окружности с центром O и радиусом r"""
            # Вектор от A к O
            AO = O - A
            dist_AO = np.linalg.norm(AO)
            
            # Угол между AO и касательной
            angle = np.arcsin(r / dist_AO)
            
            # Нормализованный вектор AO
            AO_norm = AO / dist_AO
            
            # Перпендикулярный вектор
            perp = np.array([-AO_norm[1], AO_norm[0], 0])
            
            # Выбираем касательную, которая идет вверх и вправо
            C_dir = np.cos(angle) * AO_norm + np.sin(angle) * perp
            
            # Точка касания C
            C = O - r * (np.sin(angle) * AO_norm - np.cos(angle) * perp)
            
            return C
        
        # Находим точку касания C
        C = find_tangent_point_from_A(A, O_small, r)
        
        # Линия AC продолжаем до пересечения с большой полуокружностью в D
        line_dir = (C - A)
        line_dir = line_dir / np.linalg.norm(line_dir)
        
        # Находим пересечение линии A->C с большой окружностью
        O_big = ORIGIN
        OA = A - O_big
        a = np.dot(line_dir, line_dir)
        b = 2 * np.dot(OA, line_dir)
        c = np.dot(OA, OA) - R_big**2
        
        discriminant = b**2 - 4*a*c
        t1 = (-b + np.sqrt(discriminant)) / (2*a)
        t2 = (-b - np.sqrt(discriminant)) / (2*a)
        
        # Выбираем t > 0 (точка D дальше от A чем C)
        t_D = max(t1, t2)
        D = A + t_D * line_dir
        
        # Касательная AD - ТОЛЩЕ
        tangent_line = Line(A, D, color=WHITE, stroke_width=4)
        
        # Точки C и D
        dot_C = Dot(C, color=WHITE, radius=0.08)
        dot_D = Dot(D, color=WHITE, radius=0.08)
        label_C = Text("C", font_size=28, color=WHITE).next_to(C, LEFT + UP, buff=0.15)
        label_D = Text("D", font_size=28, color=WHITE).next_to(D, UP, buff=0.15)
        
        self.play(Create(tangent_line), run_time=1.5)
        self.play(
            Create(dot_C), Write(label_C),
            Create(dot_D), Write(label_D),
            run_time=1
        )
        
        # Отрезок CD (изначально белый)
        CD_line_white = Line(C, D, color=WHITE, stroke_width=4)
        CD_line_yellow = Line(C, D, color=YELLOW, stroke_width=4)
        
        # Отрезок TB (изначально белый)
        TB_line_white = Line(T, B, color=WHITE, stroke_width=4)
        TB_line_yellow = Line(T, B, color=YELLOW, stroke_width=4)
        
        # Создаем отрезки белыми
        self.play(Create(CD_line_white), Create(TB_line_white), run_time=1)
        
        # Подписи 6 и 15 - РОВНО ПО ЦЕНТРУ ОТРЕЗКОВ
        label_6 = Text("6", font_size=28, color=YELLOW, font = "Consolas")
        label_6.move_to((C + D) / 2)  # Точный центр отрезка CD
        label_6.shift(UP * 0.3)  # Немного выше отрезка
        
        label_15 = Text("15", font_size=28, color=YELLOW, font = "Consolas")
        label_15.move_to((T + B) / 2)  # Точный центр отрезка TB
        label_15.shift(DOWN * 0.3)  # Немного ниже отрезка
        
        # ПЛАВНОЕ ИЗМЕНЕНИЕ ЦВЕТА на желтый
        self.play(
            Transform(CD_line_white, CD_line_yellow),
            Transform(TB_line_white, TB_line_yellow),
            Write(label_6),
            Write(label_15),
            run_time=2
        )
        
        self.wait(5)

        # ОБРАТНОЕ ИЗМЕНЕНИЕ ЦВЕТА на белый
        CD_line_white_back = Line(C, D, color=WHITE, stroke_width=4)
        TB_line_white_back = Line(T, B, color=WHITE, stroke_width=4)
        
        self.play(
            Transform(CD_line_yellow, CD_line_white_back),
            Transform(TB_line_yellow, TB_line_white_back),
            FadeOut(label_6),
            FadeOut(label_15),
            run_time=1
        )
        
        # Новые подписи справа от полуокружности (ЕЩЕ ВЫШЕ)
        cd_text = Text("CD=6", font_size=24, color=YELLOW, font="Consolas")
        tb_text = Text("TB=15", font_size=24, color=YELLOW, font="Consolas")
        
        # Позиционируем ЕЩЕ ВЫШЕ и с маленьким margin
        text_position = RIGHT * (R_big + 1.5) + UP * 2.0  # Поднял выше
        cd_text.move_to(text_position)
        tb_text.move_to(text_position + DOWN * 0.4)  # Маленький отступ
        
        self.play(
            Write(cd_text),
            Write(tb_text),
            run_time=1
        )
        
        self.wait(5)
        
        # === ДОПОЛНИТЕЛЬНЫЕ ПОСТРОЕНИЯ ===
        
        # 1. Отрезок OE сразу красным цветом
        line_OE = Line(O_small, E, color=PURPLE, stroke_width=5)
        
        # Прямая через O_small и E до пересечения с AB
        line_dir = (E - O_small) / np.linalg.norm(E - O_small)
        
        # Находим пересечение с AB (y = 0)
        if abs(line_dir[1]) > 1e-6:
            t_intersect = -O_small[1] / line_dir[1]
            O_point = O_small + t_intersect * line_dir
        else:
            O_point = O_small + line_dir * 5
        
        # Проверяем что точка O лежит на отрезке AB
        if O_point[0] < A[0]:
            O_point = A
        elif O_point[0] > B[0]:
            O_point = B
        
        # Прямая O_small -> O (через E)
        line_O_small_O = Line(O_small, O_point, color=PURPLE, stroke_width=3)
        
        # Точка O на AB
        dot_O = Dot(O_point, color=WHITE, radius=0.08)
        label_O = Text("O", font_size=28, color=WHITE).next_to(O_point, DOWN, buff=0.15)
        
        self.play(
            Create(line_OE),
            Create(line_O_small_O),
            Create(dot_O), Write(label_O),
            run_time=1.5
        )
        
        # 2. Касательная к полуокружности в точке E (пунктиром)
        # Касательная перпендикулярна радиусу O_big->E
        radius_dir = (E - ORIGIN) / np.linalg.norm(E - ORIGIN)
        tangent_dir = np.array([-radius_dir[1], radius_dir[0], 0])
        
        tangent_length = 2.0
        tangent_start = E - tangent_dir * tangent_length
        tangent_end = E + tangent_dir * tangent_length
        tangent_dashed = DashedLine(tangent_start, tangent_end, color=WHITE, stroke_width=2, dash_length=0.1)
        
        self.play(Create(tangent_dashed), run_time=1.5)
        
        # 3. ПРАВИЛЬНЫЙ уголок - классическое обозначение прямого угла
        # Вектор направления OE
        OE_dir = (E - O_small) / np.linalg.norm(E - O_small)
        
        # Уголок в точке E - КЛАССИЧЕСКОЕ ОБОЗНАЧЕНИЕ (отзеркаленный квадратик)
        angle_length = 0.25
        
        # Создаем квадратик в угле
        # Первая линия - вдоль OE (от E в сторону O_small)
        angle_line1_start = E - OE_dir * angle_length
        angle_line1_end = angle_line1_start + tangent_dir * angle_length
        angle_line1 = Line(angle_line1_start, angle_line1_end, color=YELLOW, stroke_width=3)
        
        # Вторая линия - вдоль касательной (от E в нужную сторону)  
        angle_line2_start = E + tangent_dir * angle_length
        angle_line2_end = angle_line2_start - OE_dir * angle_length
        angle_line2 = Line(angle_line2_start, angle_line2_end, color=YELLOW, stroke_width=3)
        
        # Прямоугольный угол (квадратик в угле)
        angle_square = VGroup(angle_line1, angle_line2)
        
        self.play(Create(angle_square), run_time=1)
        
        self.wait(1)
        
        # 4. Убираем вспомогательные элементы (кроме OE)
        self.play(
            FadeOut(tangent_dashed),
            FadeOut(angle_square),
            run_time=1.5
        )
        
        # 5. Подпись R появляется ПОСЛЕ исчезновения касательной
        R_label = Text("R", font_size=28, color=PURPLE)
        R_position = (O_big + E)/2
        R_label.move_to(R_position)
        R_label.shift(LEFT * 0.2 + UP * 0.1)
        
        self.play(Write(R_label), run_time=1)
        
        # Финальная пауза
        self.wait(3)
               # === НОВЫЕ ПОСТРОЕНИЯ ===
        
        # 6. Выделение равенства отрезков AC и AT
        # Создаем оранжевые версии отрезков
        AC_line_colored = Line(A, C, color=ORANGE, stroke_width=5)
        AT_line_colored = Line(A, T, color=ORANGE, stroke_width=5)
        
        # Подписи 2R-15 для обоих отрезков
        AT_label = Text("2R-15", font_size=20, color=ORANGE, font = "Consolas")
        AT_label.next_to((A + T) / 2, DOWN)
        
        AC_label = Text("2R-15", font_size=20, color=ORANGE, font = "Consolas")
        AC_label.next_to((A + C) / 2, LEFT)
        
        # Одновременно окрашиваем оба отрезка
        self.play(
            Transform(Line(A, C, color=WHITE, stroke_width=4), AC_line_colored),
            Transform(Line(A, T, color=WHITE, stroke_width=4), AT_line_colored),
            Write(AT_label),
            Write(AC_label),
            run_time=1.5
        )
        
               # 7. Перпендикуляр из центра малой окружности на AB
        # Уже есть точка T - это основание перпендикуляра
        # Показываем перпендикулярность отрезком O_small -> T
        perpendicular_line = Line(O_small, T, color=GREEN, stroke_width=3)
        
        # ПРАВИЛЬНЫЙ прямой угол в точке T - стандартное обозначение
        angle_length = 0.25
        # Создаем квадратик в угле (стандартное обозначение)
        # Первая линия - вдоль AB (от T влево)
        angle_line1_start = T + LEFT * angle_length
        angle_line1_end = angle_line1_start + UP * angle_length
        angle_line1 = Line(angle_line1_start, angle_line1_end, color=YELLOW, stroke_width=3)
        
        # Вторая линия - вдоль перпендикуляра (от T вверх)
        angle_line2_start = T + UP * angle_length  
        angle_line2_end = angle_line2_start + LEFT * angle_length
        angle_line2 = Line(angle_line2_start, angle_line2_end, color=YELLOW, stroke_width=3)
        
        angle_indicator = VGroup(angle_line1, angle_line2)
        
        self.play(
            Create(perpendicular_line),
            Create(angle_indicator),
            run_time=1.5
        )
        
        # 8. Прямая из точки C через центр O_small до пересечения с AB
        line_dir_CQ = (O_small - C) / np.linalg.norm(O_small - C)
        
        # Находим пересечение с AB (y = 0)
        if abs(line_dir_CQ[1]) > 1e-6:
            t_intersect_Q = -C[1] / line_dir_CQ[1]
            Q_point = C + t_intersect_Q * line_dir_CQ
        else:
            Q_point = C + line_dir_CQ * 5
        
        # Проверяем что точка Q лежит на отрезке AB
        if Q_point[0] < A[0]:
            Q_point = A
        elif Q_point[0] > B[0]:
            Q_point = B
        
        # Прямая C -> Q (через O_small)
        line_CQ = Line(C, Q_point, color=PURPLE, stroke_width=3)
        
        # Точка Q на AB
        dot_Q = Dot(Q_point, color=WHITE, radius=0.08)
        label_Q = Text("Q", font_size=28, color=WHITE).next_to(Q_point, DOWN, buff=0.15)
        
        self.play(
            Create(line_CQ),
            Create(dot_Q),
            Write(label_Q),
            run_time=1.5
        )
        
        # 9. Отрезок TQ и подпись X + дополнительные подписи
        TQ_line = Line(T, Q_point, color=PINK, stroke_width=5)
        X_label = Text("X", font_size=28, color=PINK)
        X_label.move_to((T + Q_point) / 2)
        X_label.shift(DOWN * 0.2)
        
        # Новые подписи: O_small->O = R-r, O->T = R-15, Q->B = 15-x, O_small->T = r
        R_minus_r_label = Text("R-r", font_size=20, color=WHITE, font="Consolas")
        R_minus_r_label.move_to((O_small + O_point) / 2)
        R_minus_r_label.shift(LEFT * 0.3)
        
        R_minus_15_label = Text("R-15", font_size=20, color=WHITE, font="Consolas")
        R_minus_15_label.move_to((O_point + T) / 2)
        R_minus_15_label.shift(DOWN * 0.2)
        
        fifteen_minus_x_label = Text("15-x", font_size=20, color=WHITE, font="Consolas")
        fifteen_minus_x_label.move_to((Q_point + B) / 2)
        fifteen_minus_x_label.shift(DOWN * 0.2)
        
        # Подпись r на перпендикуляре O_small->T
        r_perpendicular_label = Text("r", font_size=20, color=GREEN, font="Consolas")
        r_perpendicular_label.move_to((O_small + T) / 2)
        r_perpendicular_label.shift(LEFT * 0.2)
        
        self.play(
            Create(TQ_line),
            Write(X_label),
            Write(R_minus_r_label),
            Write(R_minus_15_label),
            Write(fifteen_minus_x_label),
            Write(r_perpendicular_label),
            run_time=1.5
        )
        self.wait(3)
        # 10. Соединяем D и B + обозначаем перпендикулярность углов
        DB_line = Line(D, B, color=WHITE, stroke_width=3)
        
        # Обозначаем перпендикулярность углов ADB и ACQ
        # Угол ADB (в точке D между AD и DB)
        angle_ADB_length = 0.25
        AD_dir = (A - D) / np.linalg.norm(A - D)
        DB_dir = (B - D) / np.linalg.norm(B - D)
        
        # Квадратик для угла ADB
        angle_ADB_line1_start = D + AD_dir * angle_ADB_length
        angle_ADB_line1_end = angle_ADB_line1_start + DB_dir * angle_ADB_length
        angle_ADB_line1 = Line(angle_ADB_line1_start, angle_ADB_line1_end, color=YELLOW, stroke_width=3)
        
        angle_ADB_line2_start = D + DB_dir * angle_ADB_length
        angle_ADB_line2_end = angle_ADB_line2_start + AD_dir * angle_ADB_length
        angle_ADB_line2 = Line(angle_ADB_line2_start, angle_ADB_line2_end, color=YELLOW, stroke_width=3)
        
        angle_ADB_indicator = VGroup(angle_ADB_line1, angle_ADB_line2)
        
        # Угол ACQ (в точке C между AC и CQ)
        angle_ACQ_length = 0.25
        AC_dir = (A - C) / np.linalg.norm(A - C)
        CQ_dir = (Q_point - C) / np.linalg.norm(Q_point - C)
        
        # Квадратик для угла ACQ
        angle_ACQ_line1_start = C + AC_dir * angle_ACQ_length
        angle_ACQ_line1_end = angle_ACQ_line1_start + CQ_dir * angle_ACQ_length
        angle_ACQ_line1 = Line(angle_ACQ_line1_start, angle_ACQ_line1_end, color=YELLOW, stroke_width=3)
        
        angle_ACQ_line2_start = C + CQ_dir * angle_ACQ_length
        angle_ACQ_line2_end = angle_ACQ_line2_start + AC_dir * angle_ACQ_length
        angle_ACQ_line2 = Line(angle_ACQ_line2_start, angle_ACQ_line2_end, color=YELLOW, stroke_width=3)
        
        angle_ACQ_indicator = VGroup(angle_ACQ_line1, angle_ACQ_line2)
        
        self.play(
            Create(DB_line),
            Create(angle_ADB_indicator),
            Create(angle_ACQ_indicator),
            run_time=1.5
        )

        # 11. Перпендикуляр из Q на DB
        # Находим проекцию точки Q на прямую DB
        DB_vector = B - D
        QD_vector = Q_point - D
        projection_length = np.dot(QD_vector, DB_vector) / np.dot(DB_vector, DB_vector)
        H_point = D + projection_length * DB_vector
        
        # Проверяем что H лежит на отрезке DB
        if projection_length < 0:
            H_point = D
        elif projection_length > 1:
            H_point = B
        
        # Перпендикуляр QH
        QH_line = Line(Q_point, H_point, color=WHITE, stroke_width=3)
        
        # Точка H
        dot_H = Dot(H_point, color=WHITE, radius=0.06)
        label_H = Text("H", font_size=24, color=WHITE).next_to(H_point, UP, buff=0.1)
        
        # Прямой угол QHB (в точке H между QH и HB)
        angle_QHB_length = 0.2
        QH_dir = (Q_point - H_point) / np.linalg.norm(Q_point - H_point)
        HB_dir = (B - H_point) / np.linalg.norm(B - H_point)
        
        # Квадратик для угла QHB
        angle_QHB_line1_start = H_point + QH_dir * angle_QHB_length
        angle_QHB_line1_end = angle_QHB_line1_start + HB_dir * angle_QHB_length
        angle_QHB_line1 = Line(angle_QHB_line1_start, angle_QHB_line1_end, color=YELLOW, stroke_width=3)
        
        angle_QHB_line2_start = H_point + HB_dir * angle_QHB_length
        angle_QHB_line2_end = angle_QHB_line2_start + QH_dir * angle_QHB_length
        angle_QHB_line2 = Line(angle_QHB_line2_start, angle_QHB_line2_end, color=YELLOW, stroke_width=3)
        
        angle_QHB_indicator = VGroup(angle_QHB_line1, angle_QHB_line2)
        
        self.play(
            Create(QH_line),
            Create(dot_H), Write(label_H),
            Create(angle_QHB_indicator),
            run_time=1.5
        )
        
        
        # ДОБАВЛЯЕМ =qh к существующей подписи CD=6 (самое последнее действие)
        cd_text_with_qh = Text("CD=QH=6", font_size=24, color=YELLOW, font="Consolas")
        cd_text_with_qh.move_to(cd_text.get_center())
        
        self.play(
            Transform(cd_text, cd_text_with_qh),
            run_time=1
        )
        
        self.wait(2)
        
        # 12. Обозначаем равенство углов HQB, TO_smallQ и DAB синими рисками
        # Угол HQB (в точке Q между QH и QB) - стандартная одинарная риска
        QH_dir = (H_point - Q_point) / np.linalg.norm(H_point - Q_point)
        QB_dir = (B - Q_point) / np.linalg.norm(B - Q_point)
        
        # Нормализуем и находим биссектрису для угла HQB
        hqb_bisector = (QH_dir + QB_dir) / np.linalg.norm(QH_dir + QB_dir)
        hqb_risk = Arc(radius=0.35, start_angle=np.arctan2(hqb_bisector[1], hqb_bisector[0]) - PI/8, 
                      angle=PI/4, color=RED, stroke_width=4)
        hqb_risk.move_arc_center_to(Q_point)
        
        # Угол между векторами O_smallT и O_smallQ (в точке O_small)
        O_smallT_dir = (T - O_small) / np.linalg.norm(T - O_small)
        O_smallQ_dir = (Q_point - O_small) / np.linalg.norm(Q_point - O_small)
        
        o_small_angle_bisector = (O_smallT_dir + O_smallQ_dir) / np.linalg.norm(O_smallT_dir + O_smallQ_dir)
        o_small_risk = Arc(radius=0.35, start_angle=np.arctan2(o_small_angle_bisector[1], o_small_angle_bisector[0]) - PI/8,
                          angle=PI/4, color=RED, stroke_width=4)
        o_small_risk.move_arc_center_to(O_small)
        
        # Угол DAB (в точке A между AD и AB) - одинарная риска
        AD_dir = (D - A) / np.linalg.norm(D - A)
        AB_dir = (B - A) / np.linalg.norm(B - A)
        
        dab_bisector = (AD_dir + AB_dir) / np.linalg.norm(AD_dir + AB_dir)
        dab_risk = Arc(radius=0.35, start_angle=np.arctan2(dab_bisector[1], dab_bisector[0]) - PI/8,
                      angle=PI/4, color=RED, stroke_width=4)
        dab_risk.move_arc_center_to(A)
        
        # Показываем риски одновременно
        self.play(
            Create(hqb_risk),
            Create(o_small_risk),
            Create(dab_risk),
            run_time=1.5
        )
        
        self.wait(2)

          # 1. Полупрозрачная заливка треугольника OoT и первое уравнение
        triangle_OO_small_T = Polygon(O_point, O_small, T, color=BLUE, fill_opacity=0.3, stroke_width=2)
        equation1 = MathTex("(R-15)^2 + r^2 = (R-r)^2", font_size=36)
        equation1.move_to(DOWN)
        
        self.play(
            Create(triangle_OO_small_T),
            Write(equation1),
            run_time=2
        )
        self.wait(2)
        
        # 2. Fadeout только заливку
        self.play(
            FadeOut(triangle_OO_small_T),
            run_time=1
        )
        self.wait(1)
        
        # 3. Разными цветами заливаем треугольники ACQ, ADB и QHB
        triangle_ACQ = Polygon(A, C, Q_point, color=RED, fill_opacity=0.3, stroke_width=2)
        triangle_ADB = Polygon(A, D, B, color=GREEN, fill_opacity=0.3, stroke_width=2)
        triangle_QHB = Polygon(Q_point, H_point, B, color=ORANGE, fill_opacity=0.3, stroke_width=2)
        
        similarity_text = MathTex("ACQ \\sim ADB \\sim QHB", font_size=36)
        similarity_text.move_to(DOWN*2)
        
        self.play(
            Create(triangle_ACQ),
            Create(triangle_ADB),
            Create(triangle_QHB),
            Write(similarity_text),
            run_time=2
        )
        self.wait(3)
        
        # 4. Fadeout надпись и все заливки
        self.play(
            FadeOut(triangle_ACQ),
            FadeOut(triangle_ADB),
            FadeOut(triangle_QHB),
            FadeOut(similarity_text),
            run_time=1.5
        )
        self.wait(1)
        
        # 5. Вместо надписи пишем финальное уравнение
        equation2 = MathTex(r"\frac{2R - 15}{2R - 15 + x} = \frac{r}{\sqrt{r^2 + x^2}} = \frac{6}{15 - x}", font_size=36)
        equation2.move_to(DOWN * 2)
        
        self.play(
            Write(equation2),
            run_time=2
        )
        
        self.wait(3)

        self.wait(3)

        self.wait(3)

        # Финальная анимация - сдвиг уравнений влево и добавление ответа справа
        # Сдвигаем оба уравнения влево на том же уровне по Y
        equation1_target = equation1.copy().move_to(LEFT * 2 + equation1.get_center()[1] * UP)
        equation2_target = equation2.copy().move_to(LEFT * 2 + equation2.get_center()[1] * UP)
        
        # Добавляем ответ справа на том же уровне что первое уравнение
        answer_text = MathTex(r"\text{Answer: } r=10", font_size=42, color=WHITE)
        answer_text.move_to(RIGHT * 4 + equation1.get_center()[1]+DOWN*0.5)
        
        # Обводим ответ в прямоугольник
        answer_box = SurroundingRectangle(answer_text, color=WHITE, buff=0.3, stroke_width=3)
        
        self.play(
            Transform(equation1, equation1_target),
            Transform(equation2, equation2_target),
            Write(answer_text),
            Create(answer_box),
            run_time=2
        )
        
        self.wait(3)

#manim main.py SemiCircleScene -qh
