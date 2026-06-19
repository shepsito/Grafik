from datetime import datetime, timedelta
import calendar
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.scrollview import ScrollView

# --- Помощни логически функции за графика ---

def get_monday_week_number(date):
    if date.weekday() != 0: return 0
    return 1 if date.day <= 7 else 2 if date.day <= 14 else 3 if date.day <= 21 else 4

def get_wednesday_week_number(date):
    if date.weekday() != 2: return 0
    return 1 if date.day <= 7 else 2 if date.day <= 14 else 3 if date.day <= 21 else 4

def get_thursday_week_number(date):
    if date.weekday() != 3: return 0
    return 1 if date.day <= 7 else 2 if date.day <= 14 else 3 if date.day <= 21 else 4

def get_saturday_week_number(date):
    if date.weekday() != 5: return 0
    return 1 if date.day <= 7 else 2 if date.day <= 14 else 3 if date.day <= 21 else 4

def is_last_monday_of_quarter(date):
    if date.weekday() != 0: return False
    if date.month in [3, 6, 9, 12]:
        return calendar.monthrange(date.year, date.month)[1] - date.day < 7
    return False

def is_last_tuesday_of_quarter(date):
    if date.weekday() != 1: return False
    if date.month in [3, 6, 9, 12]:
        return calendar.monthrange(date.year, date.month)[1] - date.day < 7
    return False

def is_last_wednesday_of_quarter(date):
    if date.weekday() != 2: return False
    if date.month in [3, 6, 9, 12]:
        return calendar.monthrange(date.year, date.month)[1] - date.day < 7
    return False

def is_last_thursday_of_quarter(date):
    if date.weekday() != 3: return False
    if date.month in [3, 6, 9, 12]:
        return calendar.monthrange(date.year, date.month)[1] - date.day < 7
    return False

def is_last_friday_of_quarter(date):
    if date.weekday() != 4: return False
    if date.month in [3, 6, 9, 12]:
        return calendar.monthrange(date.year, date.month)[1] - date.day < 7
    return False

def get_shift_by_hour(hour):
    if hour == 15: return "Смяна 3"
    elif hour == 23: return "Смяна 1"
    elif hour == 7: return "Смяна 2"
    return None


# --- Основен интерфейс на приложението ---
class NotificationApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"

        layout = MDBoxLayout(orientation="vertical")

        toolbar = MDTopAppBar(title="Годишен График за Проверки")
        layout.add_widget(toolbar)

        content_layout = MDBoxLayout(orientation="vertical", padding=20, spacing=15)

        self.status_label = MDLabel(
            text="🔴 Графикът не е стартиран.",
            halign="center",
            theme_text_color="Hint",
            font_style="H6",
            size_hint_y=None,
            height=50
        )
        content_layout.add_widget(self.status_label)

        # Добавяме скролиращо се текстово поле, където ще се изписват известията без да пукат приложението
        scroll = ScrollView()
        self.log_label = MDLabel(
            text="Тук ще се показват активните проверки, когато стартирате графика...",
            halign="center",
            theme_text_color="Primary",
            font_style="Body1",
            size_hint_y=None
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        scroll.add_widget(self.log_label)
        content_layout.add_widget(scroll)

        self.action_button = MDRaisedButton(
            text="СТАРТИРАЙ ГРАФИКА",
            pos_hint={"center_x": 0.5},
            size_hint=(0.8, 0.1),
            on_release=self.toggle_schedule
        )
        content_layout.add_widget(self.action_button)

        layout.add_widget(content_layout)
        self.is_running = False
        return layout

    def toggle_schedule(self, instance):
        if not self.is_running:
            # Сменяме таймера на 5 секунди за тест, за да видиш веднага резултата на екрана!
            Clock.schedule_interval(self.check_schedule, 5)
            self.status_label.text = "🟢 Графикът работи и следи на заден план..."
            self.action_button.text = "СПРИ ГРАФИКА"
            self.action_button.md_bg_color = (0.8, 0.2, 0.2, 1)
            self.is_running = True
            self.send_alert("СИСТЕМНО ИЗВЕСТИЕ", "Графикът е активиран успешно!")
        else:
            Clock.unschedule(self.check_schedule)
            self.status_label.text = "🔴 Графикът е спрян."
            self.action_button.text = "СТАРТИРАЙ ГРАФИКА"
            self.action_button.md_bg_color = self.theme_cls.primary_color
            self.is_running = False

    def check_schedule(self, dt):
        now = datetime.now()
        current_month = now.month
        current_day = now.day
        current_hour = now.hour

        # ЗА ТЕСТА: Махаме временно ограничението за минута 00 и фиксираме изкуствено час 15,
        # за да видиш веднага как софтуерът изчислява и изкарва проверките за текущия ден!
        shift = "Смяна 3" 

        monday_week = get_monday_week_number(now)
        wednesday_week = get_wednesday_week_number(now)
        thursday_week = get_thursday_week_number(now)
        saturday_week = get_saturday_week_number(now)

        # Проверка по правилата
        if current_month in [2, 9] and monday_week == 1:
            self.send_alert("🚨 Проверка АВР", f"Съоръжение: Аварийно осветление\nСмяна: {shift}")
        
        if current_day in [11, 12]:
            self.send_alert("🚨 ЕЕ ЦПС-2", f"Съоръжение: ЕЕ ЦПС-2\nПроверка: Изправност на аварийно осветление\nСмяна: {shift}")

        if current_day == 15:
            self.send_alert("🚨 МЗ и ЕЕ ЦПС-1", f"Съоръжение: МЗ и ЕЕ ЦПС-1\nПроверка: Изправност на евакуационно осветление")

        if current_day == 8:
            self.send_alert("🚨 Секции 0,4кВ-ГК", f"Проверка: Проверка АВР на -ШУ и изправност на сигнализацията")

        if current_day == 18:
            self.send_alert("🚨 Вентилни отводи", f"Съоръжение: Вентилни отводи 1 и 3 ТП\nПроверка: Отчитане")

    def send_alert(self, title, message):
        # Новото безопасно "известие" – печата се директно на екрана на приложението!
        text_to_show = f"🔔 {title}\n{message}\n\n[Последно обновяване: {datetime.now().strftime('%H:%M:%S')}]"
        self.log_label.text = text_to_show

if __name__ == "__main__":
    NotificationApp().run()
