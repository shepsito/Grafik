from datetime import datetime, timedelta
import calendar
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

# --- Помощни логически функции за седмици и тримесечия ---

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
    return "Смяна 3"

def generate_yearly_schedule(year):
    events = []
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    current = start_date

    while current <= end_date:
        day = current.day
        shift = get_shift_by_hour(15)

        # 1. Фиксирани месечни дати
        if day in [11, 12]:
            events.append((current, "🚨 ЕЕ ЦПС-2", f"Изправност на аварийно осветление ({shift})"))
        if day == 15:
            events.append((current, "🚨 МЗ и ЕЕ ЦПС-1", "Изправност на евакуационно осветление"))
        if day == 8:
            events.append((current, "🚨 Секции 0,4кВ-ГК", "Проверка АВР на -ШУ и сигнализация"))
        if day == 18:
            events.append((current, "🚨 Вентилни отводи", "Вентилни отводи 1 и 3 ТП - Отчитане"))
        if day == 25:
            events.append((current, "🚨 КЛ 6кВ захранващи", "Проверка на КЛ 6кВ захранващи"))
        if day == 5:
            events.append((current, "🚨 ГРЩ и силови табла", "Проверка на термографски контроли"))
        if day == 20:
            events.append((current, "🚨 Маслени трансформатори", "Проверка за течове и ниво на маслото"))

        # 2. Седмични проверки
        monday_week = get_monday_week_number(current)
        wednesday_week = get_wednesday_week_number(current)
        thursday_week = get_thursday_week_number(current)
        saturday_week = get_saturday_week_number(current)

        if monday_week == 1:
            events.append((current, "📅 Понеделник (Седмица 1)", "ЕЕ ЦПС-1 - Проверка на акумулаторна батерия"))
        if monday_week == 2:
            events.append((current, "📅 Понеделник (Седмица 2)", "Проверка на заземителни уредби"))
        if wednesday_week == 1:
            events.append((current, "📅 Сряда (Седмица 1)", "ЕЕ ЦПС-2 - Проверка на оперативен ток"))
        if wednesday_week == 3:
            events.append((current, "📅 Сряда (Седмица 3)", "Почистване на изолатори в ТП"))
        if thursday_week == 2:
            events.append((current, "📅 Четвъртък (Седмица 2)", "Инспекция на пожароизвестителна система"))
        if thursday_week == 4:
            events.append((current, "📅 Четвъртък (Седмица 4)", "Тест на дизел генератор при товар"))
        if saturday_week == 1:
            events.append((current, "📅 Събота (Седмица 1)", "Проверка на осветление по периметъра"))

        # 3. Квартални проверки
        if is_last_monday_of_quarter(current):
            events.append((current, "⚠️ Квартален Понеделник", "Измерване на преходни съпротивления"))
        if is_last_tuesday_of_quarter(current):
            events.append((current, "⚠️ Квартален Вторник", "Преглед на лични предпазни средства и щанги"))
        if is_last_wednesday_of_quarter(current):
            events.append((current, "⚠️ Квартала Сряда", "Проверка на блокировките на КРУ 6кВ"))
        if is_last_thursday_of_quarter(current):
            events.append((current, "⚠️ Квартален Четвъртък", "Инспекция на маслонапълнени апарати"))
        if is_last_friday_of_quarter(current):
            events.append((current, "⚠️ Квартален Петък", "Контролно замерване на изолация на кабели"))

        current += timedelta(days=1)
    
    events.sort(key=lambda x: x[0])
    return events


class NotificationApp(App):
    def build(self):
        self.yearly_events = generate_yearly_schedule(datetime.now().year)

        main_layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # 1. Заглавие
        title = Label(text="ГРАФИК ПРОВЕРКИ v2.3", font_size='24sp', bold=True, size_hint_y=None, height=45)
        main_layout.add_widget(title)

        # 2. Каре: ПОСЛЕДНО ИЗТЕКЛО СЪБИТИЕ
        self.past_box = BoxLayout(orientation="vertical", padding=15, spacing=8, size_hint_y=None, height=160)
        with self.past_box.canvas.before:
            Color(0.18, 0.18, 0.24, 1) 
            self.rect1 = Rectangle(size=self.past_box.size, pos=self.past_box.pos)
        self.past_box.bind(size=self._update_rect1, pos=self._update_rect1)
        
        self.past_title = Label(text="ПОСЛЕДНО МИНАЛО СЪБИТИЕ:", bold=True, color=(0.7, 0.7, 0.7, 1), font_size='14sp', size_hint_y=None, height=22, halign='left')
        self.past_title.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))
        
        self.past_text = Label(text="Няма данни. Натиснете Старт или Тест.", font_size='16sp', bold=True, color=(1, 0.6, 0.6, 1), halign='left', valign='top')
        self.past_text.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))
        
        self.past_box.add_widget(self.past_title)
        self.past_box.add_widget(self.past_text)
        main_layout.add_widget(self.past_box)

        # 3. Каре: СЛЕДВАЩО ПРЕДСТОЯЩО СЪБИТИЕ
        self.next_box = BoxLayout(orientation="vertical", padding=15, spacing=8, size_hint_y=None, height=160)
        with self.next_box.canvas.before:
            Color(0.12, 0.22, 0.18, 1) 
            self.rect2 = Rectangle(size=self.next_box.size, pos=self.next_box.pos)
        self.next_box.bind(size=self._update_rect2, pos=self._update_rect2)

        self.next_title = Label(text="СЛЕДВАЩО ПРЕДСТОЯЩО СЪБИТИЕ:", bold=True, color=(0.7, 0.7, 0.7, 1), font_size='14sp', size_hint_y=None, height=22, halign='left')
        self.next_title.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))
        
        self.next_text = Label(text="Няма данни. Натиснете Старт или Тест.", font_size='16sp', bold=True, color=(0.5, 1, 0.5, 1), halign='left', valign='top')
        self.next_text.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))
        
        self.next_box.add_widget(self.next_title)
        self.next_box.add_widget(self.next_text)
        main_layout.add_widget(self.next_box)

        # 4. Поле за статус
        scroll = ScrollView()
        self.status_label = Label(text="Системата е в готовност...", font_size='16sp', size_hint_y=None, halign='center', color=(0.8, 0.8, 0.8, 1))
        self.status_label.bind(texture_size=self.status_label.setter('size'))
        scroll.add_widget(self.status_label)
        main_layout.add_widget(scroll)

        # 5. НОВ БУТОН: ЗА РЪЧЕН ТЕСТ (Оранжев)
        self.test_btn = Button(text="ТЕСТВАЙ ИЗВЕСТИЯТА (РЪЧНО)", font_size='18sp', bold=True, background_color=(0.9, 0.5, 0.1, 1), size_hint_y=None, height=55)
        self.test_btn.bind(on_release=self.trigger_manual_test)
        main_layout.add_widget(self.test_btn)

        # 6. Основен Бутон: МОНИТОРИНГ
        self.btn = Button(text="СТАРТИРАЙ МОНИТОРИНГ", font_size='18sp', bold=True, background_color=(0, 0.6, 0.6, 1), size_hint_y=None, height=55)
        self.btn.bind(on_release=self.toggle_system)
        main_layout.add_widget(self.btn)

        self.is_running = False
        return main_layout

    def _update_rect1(self, instance, value): self.rect1.pos = instance.pos; self.rect1.size = instance.size
    def _update_rect2(self, instance, value): self.rect2.pos = instance.pos; self.rect2.size = instance.size

    # Функция за ръчния тест
    def trigger_manual_test(self, instance):
        self.update_events_display()
        now = datetime.now()
        self.status_label.text = f"Ръчно сканиране на събитията... УСПЕШНО!\nЧас на теста: {now.strftime('%H:%M:%S')}"

    def toggle_system(self, instance):
        if not self.is_running:
            self.update_events_display() 
            Clock.schedule_interval(self.update_events_display, 4) 
            self.btn.text = "СПРИ МОНИТОРИНГ"
            self.btn.background_color = (0.8, 0.2, 0.2, 1)
            self.is_running = True
        else:
            Clock.unschedule(self.update_events_display)
            self.btn.text = "СТАРТИРАЙ МОНИТОРИНГ"
            self.btn.background_color = (0, 0.6, 0.6, 1)
            self.is_running = False

    def update_events_display(self, *args):
        now = datetime.now()
        
        past_event = None
        next_event = None

        for event_date, facility, info in self.yearly_events:
            if event_date.date() <= now.date():
                past_event = (event_date, facility, info)
            elif event_date.date() > now.date() and next_event is None:
                next_event = (event_date, facility, info)

        if past_event:
            date_str = past_event[0].strftime('%d.%m.%Y')
            self.past_text.text = f"Дата: {date_str}\nОбект: {past_event[1]}\nДейност: {past_event[2]}"
        else:
            self.past_text.text = "Няма минали събития"

        if next_event:
            date_str = next_event[0].strftime('%d.%m.%Y')
            self.next_text.text = f"Дата: {date_str}\nОбект: {next_event[1]}\nДейност: {next_event[2]}"
        else:
            self.next_text.text = "Няма предстоящи събития"

        # Ако мониторингът работи автоматично, опресняваме и долния надпис
        if self.is_running:
            self.status_label.text = f"Последна автоматична проверка:\n{now.strftime('%H:%M:%S')}\nВсичко е наред."

if __name__ == "__main__":
    NotificationApp().run()
