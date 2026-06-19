from datetime import datetime, timedelta
import calendar
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

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


# --- Основен интерфейс (Чист Kivy) ---
class NotificationApp(App):
    def build(self):
        # Основен контейнер с вертикално подреждане
        layout = BoxLayout(orientation="vertical", padding=30, spacing=20)

        # Заглавие
        title_label = Label(
            text="ГОДИШЕН ГРАФИК ЗА ПРОВЕРКИ",
            font_size='22sp',
            bold=True,
            size_hint_y=None,
            height=60
        )
        layout.add_widget(title_label)

        # Статус
        self.status_label = Label(
            text="Статус: Графикът е спрян",
            font_size='16sp',
            color=(1, 0.3, 0.3, 1), # Червен цвят
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.status_label)

        # Скролиращ се панел за логовете
        scroll = ScrollView()
        self.log_label = Label(
            text="Натиснете бутона по-долу, за да стартирате симулацията на проверките...",
            font_size='15sp',
            halign="center",
            valign="middle",
            size_hint_y=None
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        scroll.add_widget(self.log_label)
        layout.add_widget(scroll)

        # Бутон за управление
        self.action_button = Button(
            text="СТАРТИРАЙ ГРАФИКА",
            font_size='18sp',
            bold=True,
            background_color=(0, 0.6, 0.6, 1), # Teal цвят
            size_hint_y=None,
            height=70
        )
        self.action_button.bind(on_release=self.toggle_schedule)
        layout.add_widget(self.action_button)

        self.is_running = False
        return layout

    def toggle_schedule(self, instance):
        if not self.is_running:
            # За теста проверяваме на всеки 3 секунди
            Clock.schedule_interval(self.check_schedule, 3)
            self.status_label.text = "Статус: Графикът работи на заден план"
            self.status_label.color = (0.3, 1, 0.3, 1) # Зелен цвят
            self.action_button.text = "СПРИ ГРАФИКА"
            self.action_button.background_color = (0.8, 0.2, 0.2, 1) # Червен бутон
            self.is_running = True
            self.send_alert("СИСТЕМНО ИЗВЕСТИЕ", "Графикът е активиран успешно!")
        else:
            Clock.unschedule(self.check_schedule)
            self.status_label.text = "Статус: Графикът е спрян"
            self.status_label.color = (1, 0.3, 0.3, 1)
            self.action_button.text = "СТАРТИРАЙ ГРАФИКА"
            self.action_button.background_color = (0, 0.6, 0.6, 1)
            self.is_running = False

    def check_schedule(self, dt):
        now = datetime.now()
        current_month = now.month
        current_day = now.day

        # Слагаме тестова смяна за визуализация веднага
        shift = "Смяна 3" 

        monday_week = get_monday_week_number(now)
        wednesday_week = get_wednesday_week_number(now)
        thursday_week = get_thursday_week_number(now)
        saturday_week = get_saturday_week_number(now)

        # Примерна бърза проверка за визуализация според твоите правила
        if current_day in [11, 12]:
            self.send_alert("🚨 ЕЕ ЦПС-2", f"Съоръжение: ЕЕ ЦПС-2\nПроверка: Изправност на аварийно осветление\nСмяна: {shift}")
        elif current_day == 15:
            self.send_alert("🚨 МЗ и ЕЕ ЦПС-1", f"Съоръжение: МЗ и ЕЕ ЦПС-1\nПроверка: Изправност на евакуационно осветление")
        elif current_day == 8:
            self.send_alert("🚨 Секции 0,4кВ-ГК", f"Проверка: Проверка АВР на -ШУ и изправност на сигнализацията")
        elif current_day == 18:
            self.send_alert("🚨 Вентилни отводи", f"Съоръжение: Вентилни отводи 1 и 3 ТП\nПроверка: Отчитане")
        else:
            # Ако днес няма събитие по график, генерираме тестово съобщение, за да видиш, че софтуерът работи
            self.send_alert("📅 Текущ анализ", f"Днес е {current_day}-то число, месец {current_month}.\nНяма активни големи проверки за днешната дата.\nСистемата следи непрекъснато.")

    def send_alert(self, title, message):
        self.log_label.text = f"🔔 {title}\n\n{message}\n\n[Последно сканиране: {datetime.now().strftime('%H:%M:%S')}]"

if __name__ == "__main__":
    NotificationApp().run()
