from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp, sp
from kivy.clock import Clock

from service_logic import generate_yearly_schedule

Window.clearcolor = (0.05, 0.05, 0.08, 1)


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(15), dp(10), dp(15), dp(10)]
        self.spacing = dp(10)

        # ------------------ МИНАЛО СЪБИТИЕ ------------------
        self.past_box = self._create_panel("<< МИНАЛО СЪБИТИЕ", (0.15, 0.12, 0.18, 1))
        self.past_content = self._create_content_label()
        self.past_box.add_widget(self.past_content)
        self.add_widget(self.past_box)

        # ------------------ ДНЕС (тъмно зеленикав фон + SCROLL) ------------------
        self.today_box = self._create_panel("ДНЕС", (0.08, 0.20, 0.12, 1))

        self.today_scroll = ScrollView(size_hint_y=0.82)
        self.today_content = Label(
            text="Зареждане...",
            color=(0.9, 0.9, 0.9, 1),
            font_size=sp(17),
            halign='left',
            valign='top',
            text_size=(Window.width - dp(60), None),
            markup=True,
            size_hint_y=None
        )
        self.today_content.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))

        self.today_scroll.add_widget(self.today_content)
        self.today_box.add_widget(self.today_scroll)
        self.add_widget(self.today_box)

        # ------------------ СЛЕДВАЩО СЪБИТИЕ (тъмно синкав фон) ------------------
        self.next_box = self._create_panel(">> СЛЕДВАЩО СЪБИТИЕ", (0.10, 0.14, 0.25, 1))
        self.next_content = self._create_content_label()
        self.next_box.add_widget(self.next_content)
        self.add_widget(self.next_box)

        # ------------------ ДОЛЕН ПАНЕЛ ------------------
        bottom_box = BoxLayout(orientation='vertical', size_hint_y=0.08)
        self.info_label = Label(
            text=f"[color=888888]Актуализирано: {datetime.now().strftime('%H:%M')}[/color]",
            markup=True,
            font_size=sp(12)
        )
        bottom_box.add_widget(self.info_label)

        refresh_btn = Button(
            text="ОБНОВИ",
            background_color=(0.2, 0.5, 0.8, 1),
            font_size=sp(16),
            bold=True,
            size_hint_y=0.6
        )
        refresh_btn.bind(on_press=self.refresh_data)
        bottom_box.add_widget(refresh_btn)

        self.add_widget(bottom_box)

        # ------------------ ЗАРЕЖДАНЕ ------------------
        self.yearly_events = []
        self.load_events()

        Clock.schedule_interval(self.update_display, 3600)

    # ---------------------------------------------------------
    # ПАНЕЛИ
    # ---------------------------------------------------------
    def _create_panel(self, title, bg_color):
        box = BoxLayout(
            orientation='vertical',
            padding=[dp(15), dp(10), dp(15), dp(10)],
            spacing=dp(3),
            size_hint_y=0.25
        )
        with box.canvas.before:
            Color(*bg_color)
            rect = Rectangle()
        box.bind(size=lambda inst, val: self._update_rect(rect, inst),
                 pos=lambda inst, val: self._update_rect(rect, inst))

        label = Label(
            text=f"[b]{title}[/b]",
            font_size=sp(16),
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=0.18,
            halign='left',
            markup=True
        )
        box.add_widget(label)
        return box

    def _create_content_label(self):
        return Label(
            text="Зареждане...",
            color=(0.9, 0.9, 0.9, 1),
            font_size=sp(17),
            halign='left',
            text_size=(Window.width - dp(60), None),
            markup=True
        )

    def _update_rect(self, rect, instance):
        rect.pos = instance.pos
        rect.size = instance.size

    # ---------------------------------------------------------
    # ЛОГИКА
    # ---------------------------------------------------------
    def load_events(self):
        try:
            self.yearly_events = generate_yearly_schedule(datetime.now().year)
            self.update_display()
            self.info_label.text = f"[color=33cc33]Заредени {len(self.yearly_events)} събития[/color]"
        except Exception as e:
            self.info_label.text = f"[color=ff3333]Грешка: {e}[/color]"

    def refresh_data(self, *args):
        self.load_events()
        self.info_label.text = f"[color=ffcc00]Обновено в {datetime.now().strftime('%H:%M')}[/color]"

    def update_display(self, *args):
        now = datetime.now()
        today = now.date()

        # -------- МИНАЛО (без описание) --------
        past_events = [e for e in self.yearly_events if e['datetime'] < now]
        if past_events:
            last = past_events[-1]
            self.past_content.text = (
                f"[b]{last['datetime'].strftime('%d.%m.%Y %H:%M')}[/b]\n"
                f"{last['title']}\n"
                f"Място: {last['facility']} | {last['shift']}"
            )
        else:
            self.past_content.text = "[i]Няма минали събития[/i]"

        # -------- ДНЕС (с описание + SCROLL) --------
        today_events = [e for e in self.yearly_events if e['datetime'].date() == today]
if today_events:
    lines = []
    for ev in today_events:
        status = "ИЗПЪЛНЕНО" if ev['datetime'] < now else "ПРЕДСТОЯЩО"
        lines.append(
            f"[b]{ev['datetime'].strftime('%H:%M')}[/b]  {status}\n"
            f"[b]{ev['title']}[/b]\n"   
            f"Място: {ev['facility']} | {ev['shift']}\n"
            f"[color=888888]{ev['description']}[/color]\n"
        )
    self.today_content.text = "\n".join(lines)
else:
    self.today_content.text = "[i]Няма събития за днес[/i]"


        # -------- СЛЕДВАЩО (без описание, НЕ взима днешни) --------
        future_events = [
            e for e in self.yearly_events
            if e['datetime'] > now and e['datetime'].date() != today
        ]

        if future_events:
            next_ev = future_events[0]
            time_left = next_ev['datetime'] - now
            hours = int(time_left.total_seconds() // 3600)
            minutes = int((time_left.total_seconds() % 3600) // 60)

            self.next_content.text = (
                f"[b]{next_ev['datetime'].strftime('%d.%m.%Y %H:%M')}[/b]\n"
                f"{next_ev['title']}\n"
                f"Място: {next_ev['facility']} | {next_ev['shift']}\n"
                f"[color=33cc33]След {hours}h {minutes}m[/color]"
            )
        else:
            self.next_content.text = "[i]Няма предстоящи събития[/i]"


class NotificationApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    NotificationApp().run()
