#!/usr/bin/env python3
"""
ESA Space Challenge
A self-contained Tkinter quiz for public outreach events.\n\nEach prize value can contain multiple questions; one is selected randomly\nfrom each value whenever a new game starts.

Run:
    python esa_space_quiz.py

Controls:
    F11     Toggle full screen
    Escape  Leave full screen
    R       Restart quiz

No external images or packages are required.
"""

import math
import random
import json
import io
import tkinter as tk
from tkinter import messagebox

#Localization
UI_LANGUAGES=['en','it','de','fr','es']
UI_TEXT={}
LOCALIZED_QUESTION_BANKS={}
for lang in UI_LANGUAGES:
    with io.open(f"ui_{lang}.json",mode="r",encoding="utf-8") as f:
        UI_TEXT[lang]=json.load(f)
    with io.open(f"questions_{lang}.json",mode="r",encoding="utf-8") as f:
        LOCALIZED_QUESTION_BANKS[lang]=json.load(f)

# The quiz still has one question per prize level, but the question for each
# level is selected randomly when a new game starts.
PRIZE_LADDER = list(LOCALIZED_QUESTION_BANKS['en'].keys())
LADDER_LENGHT = len(PRIZE_LADDER)
LETTERS = ("A", "B", "C", "D")

# Validate the question bank when the program starts.
for language in LOCALIZED_QUESTION_BANKS.keys():
    QUESTION_BANK=LOCALIZED_QUESTION_BANKS[language]
    for prize_value, questions in QUESTION_BANK.items():
        if not questions:
            raise ValueError(f"No questions configured for {prize_value}")
        for question in questions:
            if len(question["answers"]) != 4:
                raise ValueError(f"{prize_value}: every question must have exactly 4 answers")
            if not 0 <= question["correct"] < 4:
                raise ValueError(f"{prize_value}: correct answer must be 0, 1, 2 or 3")

class ESASpaceQuiz(tk.Tk):
    BG = "#030515"
    PANEL = "#090d2c"
    BLUE = "#163c8c"
    BRIGHT_BLUE = "#2474ff"
    CYAN = "#49d9ff"
    GOLD = "#ffc94a"
    ORANGE = "#ff8b27"
    WHITE = "#f7fbff"
    MUTED = "#9eb4d6"
    GREEN = "#1fbd72"
    RED = "#d9445e"

    def __init__(self):
        super().__init__()
        self.title("ESA Space Challenge")
        self.geometry("1280x800")
        self.minsize(960, 650)
        self.configure(bg=self.BG)
        self.fullscreen = False
        self.language = "en"
        self.last_answer_correct = False
        self.current = 0
        self.selected_questions = []
        self.score = 0
        self.correct_count = 0
        self.locked = False
        self.after_id = None

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.leave_fullscreen)
        self.bind("<Key-r>", lambda _e: self.restart())
        self.bind("<Key-R>", lambda _e: self.restart())
        self.bind("<Configure>", self.on_resize)

        self.canvas = tk.Canvas(self, bg=self.BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.draw_background()
        self.show_start_screen()

    def t(self, key, **kwargs):
        text = UI_TEXT[self.language].get(key, UI_TEXT["en"][key])
        return text.format(**kwargs) if kwargs else text

    def set_language(self, language):
        self.language = language
        self.title("ESA Space Challenge")
        self.show_start_screen()

    def toggle_fullscreen(self, _event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def leave_fullscreen(self, _event=None):
        self.fullscreen = False
        self.attributes("-fullscreen", False)

    def on_resize(self, event):
        if event.widget is self:
            if self.after_id:
                self.after_cancel(self.after_id)
            self.after_id = self.after(80, self.redraw_current_screen)

    def clear(self):
        self.canvas.delete("all")

    def draw_background(self):
        w = max(self.winfo_width(), 960)
        h = max(self.winfo_height(), 650)
        self.canvas.create_rectangle(0, 0, w, h, fill=self.BG, outline="")

        # Game-show inspired radial rings and light beams, drawn without external assets.
        cx, cy = int(w * 0.39), int(h * 0.43)
        for radius, colour, width in [
            (int(h * 0.48), "#08164a", 3),
            (int(h * 0.38), "#0d2870", 2),
            (int(h * 0.29), "#1450a4", 2),
            (int(h * 0.21), "#2474ff", 2),
        ]:
            self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius,
                                    outline=colour, width=width)

        for angle in range(0, 360, 20):
            r1, r2 = int(h * 0.10), int(h * 0.50)
            x1 = cx + math.cos(math.radians(angle)) * r1
            y1 = cy + math.sin(math.radians(angle)) * r1
            x2 = cx + math.cos(math.radians(angle)) * r2
            y2 = cy + math.sin(math.radians(angle)) * r2
            self.canvas.create_line(x1, y1, x2, y2, fill="#0a245f", width=1)

        # Stars
        star_points = [
            (.05,.10),(.12,.28),(.20,.08),(.28,.20),(.35,.06),(.45,.13),
            (.53,.05),(.61,.18),(.70,.09),(.78,.23),(.88,.11),(.95,.30),
            (.08,.72),(.18,.88),(.31,.76),(.47,.91),(.58,.74),(.69,.88),
            (.81,.69),(.91,.86),(.97,.62),(.55,.31),(.24,.55),(.42,.67)
        ]
        for i, (sx, sy) in enumerate(star_points):
            r = 1 + (i % 3 == 0)
            self.canvas.create_oval(w*sx-r, h*sy-r, w*sx+r, h*sy+r,
                                    fill=self.WHITE, outline="")

    def rounded_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1+radius,y1, x2-radius,y1, x2,y1, x2,y1+radius,
            x2,y2-radius, x2,y2, x2-radius,y2, x1+radius,y2,
            x1,y2, x1,y2-radius, x1,y1+radius, x1,y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def text_button(self, x1, y1, x2, y2, text, command,
                    fill=None, outline=None, font_size=18, tag=None):
        tag = tag or f"button_{x1}_{y1}"
        fill = fill or self.BLUE
        outline = outline or self.CYAN
        self.rounded_rect(x1, y1, x2, y2, radius=18, fill=fill,
                          outline=outline, width=2, tags=(tag,))
        self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=text,
                                fill=self.WHITE, font=("Arial", font_size, "bold"),
                                width=max(100, x2-x1-30), justify="center", tags=(tag,))
        self.canvas.tag_bind(tag, "<Button-1>", lambda _e: command())
        self.canvas.tag_bind(tag, "<Enter>", lambda _e: self.set_button_colour(tag, self.BRIGHT_BLUE))
        self.canvas.tag_bind(tag, "<Leave>", lambda _e: self.set_button_colour(tag, fill))
        return tag

    def set_button_colour(self, tag, colour):
        items = self.canvas.find_withtag(tag)
        if items:
            self.canvas.itemconfigure(items[0], fill=colour)

    def show_start_screen(self):
        self.screen = "start"
        self.clear()
        self.draw_background()
        w, h = self.winfo_width(), self.winfo_height()
        cx = w * 0.42

        self.canvas.create_text(cx, h*0.16, text="ESA", fill=self.CYAN,
                                font=("Arial", max(24, int(h*.055)), "bold"))
        self.canvas.create_text(cx, h*0.24, text="SPACE CHALLENGE", fill=self.WHITE,
                                font=("Arial", max(28, int(h*.065)), "bold"))
        self.canvas.create_text(cx, h*0.33,
                                text=self.t("subtitle"),
                                fill=self.MUTED, font=("Arial", max(14, int(h*.026))),
                                width=w*.66, justify="center")

        r = min(w, h) * .15
        self.canvas.create_oval(cx-r, h*.49-r, cx+r, h*.49+r,
                                fill="#07113a", outline=self.CYAN, width=4)
        self.canvas.create_oval(cx-r*.76, h*.49-r*.76, cx+r*.76, h*.49+r*.76,
                                outline=self.GOLD, width=3)
        self.canvas.create_text(cx, h*.465, text=str(LADDER_LENGHT), fill=self.WHITE,
                                font=("Arial", max(30, int(h*.075)), "bold"))
        self.canvas.create_text(cx, h*.545, text=f"{LADDER_LENGHT} {self.t('questions')}", fill=self.GOLD,
                                font=("Arial", max(14, int(h*.025)), "bold"))

        self.text_button(cx-w*.13, h*.72, cx+w*.13, h*.81,
                         self.t("start"), self.start_quiz,
                         fill="#123d8b", outline=self.GOLD,
                         font_size=max(15, int(h*.026)), tag="start")
        self.canvas.create_text(cx, h*.89,
                                text=self.t("controls"),
                                fill=self.MUTED, font=("Arial", max(10, int(h*.017))))
        # Language selector. Changing language redraws this screen immediately.
        self.canvas.create_text(cx, h*.065, text=self.t("choose"), fill=self.MUTED,
                                font=("Arial", max(10, int(h*.017)), "bold"))
        labels = [("en", "EN"), ("it", "IT"), ("de", "DE"), ("fr", "FR"), ("es", "ES")]
        bw, gap = w*.052, w*.008
        total_w = len(labels)*bw + (len(labels)-1)*gap
        lx = cx-total_w/2
        for i, (code, label) in enumerate(labels):
            x1 = lx+i*(bw+gap)
            self.text_button(x1, h*.085, x1+bw, h*.13, label,
                             lambda c=code: self.set_language(c),
                             fill=self.BRIGHT_BLUE if code == self.language else "#101c45",
                             outline=self.GOLD if code == self.language else self.CYAN,
                             font_size=max(9, int(h*.015)), tag=f"lang_{code}")
        self.draw_ladder(w, h, active=None)

    def randomize_answers(self, question):
        indexed_answers = list(enumerate(question["answers"]))
        random.shuffle(indexed_answers)
        original_correct = question["correct"]
        question["answers"] = [answer for _, answer in indexed_answers]
        question["correct"] = next(
            i for i, (orig_idx, _) in enumerate(indexed_answers)
            if orig_idx == original_correct
        )
        return question

    def start_quiz(self):
        self.current = 0
        self.score = 0
        self.correct_count = 0
        self.locked = False

        # Pick exactly one question at random for each prize level.
        # Shift the answers so it is not always the same correct answer placement.
        # The selected questions remain fixed for the whole game.
        self.selected_questions = [
            self.randomize_answers(__import__("copy").deepcopy(random.choice(LOCALIZED_QUESTION_BANKS[self.language][value])))
            for value in PRIZE_LADDER
        ]

        self.show_question()

    def draw_ladder(self, w, h, active=None):
        x1, x2 = w*.80, w*.97
        y1, y2 = h*.10, h*.90
        self.rounded_rect(x1, y1, x2, y2, 22, fill="#060a22",
                          outline="#2359bd", width=2)
        self.canvas.create_text((x1+x2)/2, y1+h*.045, text=self.t("ladder"),
                                fill=self.CYAN, font=("Arial", max(11, int(h*.019)), "bold"))
        usable = y2-y1-h*.10
        step = usable/LADDER_LENGHT
        for display_i, value in enumerate(reversed(PRIZE_LADDER)):
            question_i = LADDER_LENGHT-1-display_i
            y = y1+h*.085 + display_i*step + step/2
            is_active = active == question_i
            is_passed = active is not None and question_i < active
            if is_active:
                self.rounded_rect(x1+8, y-step*.39, x2-8, y+step*.39, 10,
                                  fill=self.ORANGE, outline=self.GOLD, width=2)
                colour = self.WHITE
            elif is_passed:
                colour = self.GOLD
            else:
                colour = self.MUTED
            self.canvas.create_text(x1+18, y, text=str(question_i+1), anchor="w",
                                    fill=colour, font=("Arial", max(9, int(h*.016)), "bold"))
            self.canvas.create_text(x2-16, y, text=value, anchor="e",
                                    fill=colour, font=("Arial", max(9, int(h*.016)), "bold"))

    def show_question(self):
        self.screen = "question"
        self.locked = False
        self.clear()
        self.draw_background()
        w, h = self.winfo_width(), self.winfo_height()
        q = self.selected_questions[self.current]
        main_right = w*.76

        self.canvas.create_text(w*.03, h*.045, anchor="w",
                                text="ESA SPACE CHALLENGE", fill=self.CYAN,
                                font=("Arial", max(14, int(h*.025)), "bold"))
        self.canvas.create_text(main_right-w*.02, h*.045, anchor="e",
                                text=self.t("question", n=self.current+1, total=LADDER_LENGHT, prize=PRIZE_LADDER[self.current]),
                                fill=self.GOLD, font=("Arial", max(12, int(h*.021)), "bold"))

        # Progress bar
        px1, px2, py = w*.04, main_right-w*.03, h*.09
        self.canvas.create_rectangle(px1, py, px2, py+8, fill="#101c45", outline="")
        self.canvas.create_rectangle(px1, py, px1+(px2-px1)*(self.current+1)/LADDER_LENGHT,
                                     py+8, fill=self.CYAN, outline="")

        self.rounded_rect(w*.04, h*.15, main_right-w*.03, h*.38, 26,
                          fill="#07113a", outline=self.CYAN, width=3)
        self.canvas.create_text((w*.04+main_right-w*.03)/2, h*.265,
                                text=q["question"], fill=self.WHITE,
                                font=("Arial", max(18, int(h*.036)), "bold"),
                                width=main_right-w*.13, justify="center")

        coords = [
            (w*.04, h*.44, w*.38, h*.59),
            (w*.405, h*.44, main_right-w*.03, h*.59),
            (w*.04, h*.63, w*.38, h*.78),
            (w*.405, h*.63, main_right-w*.03, h*.78),
        ]
        for idx, ((x1,y1,x2,y2), answer) in enumerate(zip(coords, q["answers"])):
            tag = f"answer_{idx}"
            self.rounded_rect(x1,y1,x2,y2,20, fill=self.PANEL,
                              outline=self.BRIGHT_BLUE, width=2, tags=(tag,))
            self.canvas.create_text(x1+28, (y1+y2)/2, text=LETTERS[idx]+":",
                                    anchor="w", fill=self.GOLD,
                                    font=("Arial", max(15, int(h*.027)), "bold"), tags=(tag,))
            self.canvas.create_text(x1+70, (y1+y2)/2, text=answer,
                                    anchor="w", fill=self.WHITE,
                                    font=("Arial", max(12, int(h*.021)), "bold"),
                                    width=x2-x1-90, justify="left", tags=(tag,))
            self.canvas.tag_bind(tag, "<Button-1>", lambda _e, i=idx: self.choose_answer(i))
            self.canvas.tag_bind(tag, "<Enter>", lambda _e, t=tag: self.set_answer_colour(t, self.BLUE))
            self.canvas.tag_bind(tag, "<Leave>", lambda _e, t=tag: self.set_answer_colour(t, self.PANEL))

        self.canvas.create_text(w*.04, h*.87, anchor="w",
                                text=self.t("correct_answers", correct=self.correct_count, score=self.print_score()),
                                fill=self.MUTED, font=("Arial", max(11, int(h*.019)), "bold"))
        self.draw_ladder(w, h, active=self.current)

    def set_answer_colour(self, tag, colour):
        if self.locked:
            return
        items = self.canvas.find_withtag(tag)
        if items:
            self.canvas.itemconfigure(items[0], fill=colour)

    def choose_answer(self, selected):
        if self.locked:
            return
        self.locked = True
        q = self.selected_questions[self.current]
        correct = q["correct"]
        is_correct = selected == correct

        for i in range(4):
            items = self.canvas.find_withtag(f"answer_{i}")
            if not items:
                continue
            if i == correct:
                self.canvas.itemconfigure(items[0], fill=self.GREEN, outline="#86ffc1", width=3)
            elif i == selected:
                self.canvas.itemconfigure(items[0], fill=self.RED, outline="#ff9aaa", width=3)
            else:
                self.canvas.itemconfigure(items[0], fill="#0b1029", outline="#263157")

        if is_correct:
            self.correct_count += 1
            self.score = self.score + int(PRIZE_LADDER[self.current][1:].replace(',',''))

        self.last_answer_correct = is_correct
        self.after(850, lambda: self.show_fact(is_correct))

    def show_fact(self, is_correct):
        self.screen = "fact"
        self.clear()
        self.draw_background()
        w, h = self.winfo_width(), self.winfo_height()
        q = self.selected_questions[self.current]
        main_right = w*.76
        colour = self.GREEN if is_correct else self.RED
        headline = self.t("correct") if is_correct else self.t("wrong")

        self.canvas.create_text((main_right)/2, h*.15, text=headline,
                                fill=colour, font=("Arial", max(30, int(h*.065)), "bold"))
        self.canvas.create_text(main_right/2, h*.25,
                                text=self.t("answer_is", letter=LETTERS[q['correct']], answer=q['answers'][q['correct']]),
                                fill=self.WHITE, font=("Arial", max(16, int(h*.031)), "bold"),
                                width=main_right-w*.12, justify="center")

        self.rounded_rect(w*.07, h*.36, main_right-w*.05, h*.66, 28,
                          fill="#08133b", outline=self.GOLD, width=3)
        self.canvas.create_text(w*.11, h*.42, anchor="w", text=self.t("fun_fact"),
                                fill=self.GOLD, font=("Arial", max(14, int(h*.025)), "bold"))
        self.canvas.create_text((w*.07+main_right-w*.05)/2, h*.525,
                                text=q["fact"], fill=self.WHITE,
                                font=("Arial", max(14, int(h*.026))),
                                width=main_right-w*.20, justify="center")

        button_text = self.t("final") if self.current == LADDER_LENGHT-1 else self.t("next")
        self.text_button(main_right/2-w*.12, h*.73, main_right/2+w*.12, h*.82,
                         button_text, self.next_question,
                         fill="#123d8b", outline=self.GOLD,
                         font_size=max(14, int(h*.023)), tag="next")
        self.draw_ladder(w, h, active=self.current)

    def next_question(self):
        if self.current < LADDER_LENGHT-1:
            self.current += 1
            self.show_question()
        else:
            self.show_results()

    def result_title(self):
        titles = {
            "en": [("ESA MISSION DIRECTOR", "A perfect flight through the quiz!"), ("COSMIC EXPERT", "The universe clearly has your attention."), ("ASTRONAUT IN TRAINING", "A strong result and a great launchpad for more discovery."), ("SPACE EXPLORER", "You are well on your way across the Solar System."), ("EARTH OBSERVER", "Every space journey begins by looking up and asking questions.")],
            "it": [("DIRETTORE DI MISSIONE ESA", "Un volo perfetto attraverso il quiz!"), ("ESPERTO COSMICO", "L’universo ha chiaramente la tua attenzione."), ("ASTRONAUTA IN ADDESTRAMENTO", "Un ottimo risultato e una splendida base per nuove scoperte."), ("ESPLORATORE SPAZIALE", "Sei sulla buona strada attraverso il Sistema Solare."), ("OSSERVATORE DELLA TERRA", "Ogni viaggio spaziale inizia guardando in alto e ponendo domande.")],
            "de": [("ESA-MISSIONSDIREKTOR", "Ein perfekter Flug durch das Quiz!"), ("KOSMISCHER EXPERTE", "Das Universum hat eindeutig deine Aufmerksamkeit."), ("ASTRONAUT IM TRAINING", "Ein starkes Ergebnis und eine gute Startrampe für weitere Entdeckungen."), ("WELTRAUMFORSCHER", "Du bist auf einem guten Weg durch das Sonnensystem."), ("ERDBEOBACHTER", "Jede Raumfahrt beginnt mit einem Blick nach oben und mit Fragen.")],
            "fr": [("DIRECTEUR DE MISSION ESA", "Un parcours parfait dans le quiz !"), ("EXPERT COSMIQUE", "L’Univers a clairement toute votre attention."), ("ASTRONAUTE EN FORMATION", "Un excellent résultat et une belle rampe de lancement vers de nouvelles découvertes."), ("EXPLORATEUR SPATIAL", "Vous êtes en bonne voie à travers le Système solaire."), ("OBSERVATEUR DE LA TERRE", "Tout voyage spatial commence en levant les yeux et en posant des questions.")],
            "es": [("DIRECTOR DE MISIÓN DE LA ESA", "¡Un vuelo perfecto a través del concurso!"), ("EXPERTO CÓSMICO", "Está claro que el universo tiene toda tu atención."), ("ASTRONAUTA EN FORMACIÓN", "Un gran resultado y una excelente plataforma para nuevos descubrimientos."), ("EXPLORADOR ESPACIAL", "Vas por buen camino a través del Sistema Solar."), ("OBSERVADOR DE LA TIERRA", "Todo viaje espacial comienza mirando hacia arriba y haciendo preguntas.")]
        }
        if self.correct_count == LADDER_LENGHT: idx = 0
        elif self.correct_count >= 8: idx = 1
        elif self.correct_count >= 6: idx = 2
        elif self.correct_count >= 4: idx = 3
        else: idx = 4
        return titles[self.language][idx]

    def print_score(self):
        return f'€{self.score:,}'
        
    def show_results(self):
        self.screen = "results"
        self.clear()
        self.draw_background()
        w, h = self.winfo_width(), self.winfo_height()
        title, subtitle = self.result_title()
        earned = self.print_score()
        cx = w*.50

        self.canvas.create_text(cx, h*.12, text=self.t("complete"),
                                fill=self.CYAN, font=("Arial", max(22, int(h*.045)), "bold"))
        self.canvas.create_text(cx, h*.22, text=title,
                                fill=self.GOLD, font=("Arial", max(26, int(h*.058)), "bold"))
        self.canvas.create_text(cx, h*.29, text=subtitle,
                                fill=self.MUTED, font=("Arial", max(13, int(h*.024))),
                                width=w*.75, justify="center")

        self.rounded_rect(w*.20, h*.36, w*.80, h*.64, 30,
                          fill="#07113a", outline=self.CYAN, width=3)
        self.canvas.create_text(w*.35, h*.46, text=f"{self.correct_count}/{LADDER_LENGHT}",
                                fill=self.WHITE, font=("Arial", max(32, int(h*.075)), "bold"))
        self.canvas.create_text(w*.35, h*.56, text=self.t("correct_label"),
                                fill=self.MUTED, font=("Arial", max(12, int(h*.021)), "bold"))
        self.canvas.create_line(w*.50, h*.40, w*.50, h*.60, fill="#2850a0", width=2)
        self.canvas.create_text(w*.65, h*.46, text=earned,
                                fill=self.GOLD, font=("Arial", max(32, int(h*.075)), "bold"))
        self.canvas.create_text(w*.65, h*.56, text=self.t("score_label"),
                                fill=self.MUTED, font=("Arial", max(12, int(h*.021)), "bold"))

        self.text_button(w*.31, h*.71, w*.49, h*.81, self.t("again"), self.restart,
                         fill="#123d8b", outline=self.GOLD,
                         font_size=max(14, int(h*.024)), tag="again")
        self.text_button(w*.52, h*.71, w*.70, h*.81, self.t("exit"), self.destroy,
                         fill="#24144d", outline=self.CYAN,
                         font_size=max(14, int(h*.024)), tag="exit")
        self.canvas.create_text(cx, h*.89,
                                text=self.t("thanks"),
                                fill=self.WHITE, font=("Arial", max(12, int(h*.022)), "bold"))

    def restart(self):
        self.current = 0
        self.selected_questions = []
        self.score = 0
        self.correct_count = 0
        self.locked = False
        self.show_start_screen()

    def redraw_current_screen(self):
        self.after_id = None
        screen = getattr(self, "screen", "start")
        if screen == "start":
            self.show_start_screen()
        elif screen == "question":
            self.show_question()
        elif screen == "fact":
            # Preserve the most recent answer state approximately when resizing.
            self.show_fact(self.last_answer_correct)
        elif screen == "results":
            self.show_results()


if __name__ == "__main__":
    app = ESASpaceQuiz()
    app.mainloop()
