from datetime import datetime, timedelta
import calendar
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

# --- Прецизни помощни логически функции за седмици и тримесечия ---

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


# --- Генериране на годишния календар ---
def generate_yearly_schedule(year):
    events = []
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    current = start_date

    while current <= end_date:
        current_day = current.day
        current_month = current.month
        
        monday_week = get_monday_week_number(current)
        wednesday_week = get_wednesday_week_number(current)
        thursday_week = get_thursday_week_number(current)
        saturday_week = get_saturday_week_number(current)

        shift = "Смяна 3" 

        # 1
        if current_month in [2, 9] and monday_week == 1:
            events.append((current, "🚨 Проверка АВР", f"Съоръжение: Аварийно осветление\nПроверка: Проверка АВР на захранването\nСмяна: {shift}"))
        # 2
        if current_day in [11, 12]:
            events.append((current, "🚨 ЕЕ ЦПС-2", f"Съоръжение: ЕЕ ЦПС-2\nПроверка: Проверка изправноста на аварийното осветление\nСмяна: {shift}"))
        # 3
        if current_month in [3, 10] and monday_week in [1, 2]:
            events.append((current, "🚨 Ф.И. Проверка", f"Съоръжение: По procedure\nПроверка: Ф.И. на аварийното осветление\nСмяна: {shift}"))
        # 4
        if current_day == 15:
            events.append((current, "🚨 МЗ и ЕЕ ЦПС-1", f"Съоръжение: МЗ и ЕЕ ЦПС-1\nПроверка: Проверка изправността на евакуационното осветление\nСмяна: {shift}"))
        # 5
        if is_last_monday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Пон.)", f"Съоръжение: МЗ,ЦПС-1\nПроверка: Проверка АВР сборки на 0,4кВ  захранвани от 3 и 4 БН\nСмяна: {shift}"))
        # 6
        if is_last_tuesday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Вт.)", f"Съоръжение: МЗ\nПроверка: Проверка АВР сборки на 0,4кВ захранвани от 23 и 24 БН\nСмяна: {shift}"))
        # 7
        if is_last_wednesday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Ср.)", f"Съоръжение: МЗ\nПроверка: Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 3\nСмяна: {shift}"))
        # 8
        if is_last_thursday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Четв.)", f"Съоръжение: МЗ\nПроверка: Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 4\nСмяна: {shift}"))
        # 9
        if is_last_friday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Петък)", f"Съоръжение: МЗ,ХВО и ЦПС-1\nПроверка: Проверка АВР сборки на 0,4кВ с/без сборки захр.от 3,4,23,24БН,33БН I-III,43БН I-III /\nСмяна: {shift}"))
        # 10
        if current_day == 8:
            events.append((current, "🚨 Секции 0,4кВ-ГК", f"Съоръжение: Секции 0,4кВ-ГК 1_4 блок\nПроверка: Проверка АВР на -ШУ и изправността на сигнализацията на панел 'С'БЩУ за повикване в КРу\nСмяна: {shift}"))
        # 11
        if current_day == 18:
            events.append((current, "🚨 Вентилни отводи", f"Съоръжение: Вентилни отводи 1 и 3 ТП\nПроверка:  Отчитане на -вентилни отводи\nСмяна: {shift}"))
        # 12
        if current_day == 1:
            events.append((current, "🚨 Ел.двигатели 6кВ", f"Съоръжение: Ел.двигатели 6кВ\nПроверка: Измерване съпротивлението на изолацията на ел.двиг.6кВ.-ПВТ в резерв,1и 2ППП\nСмяна: Смяна 1"))
        # 13
        if current_month in [1, 4, 7, 10] and monday_week == 1:
            events.append((current, "🚨 Проверка ДГ-А", f"Съоръжение: ДГ-A\nПроверка: Ф.И. на автономен товар не по малко от 60мин.\nСмяна: {shift}"))
        # 14
        if current_month in [1, 4, 7, 10] and monday_week == 2:
            events.append((current, "🚨 Проверка ДГ-Б", f"Съоръжение: ДГ-Б\nПроверка: Ф.И. на автономен товар не по малко от 60мин.\nСмяна: {shift}"))
        # 15
        if current_month in [1, 4, 7, 10] and wednesday_week == 3:
            events.append((current, "🚨 Проверка 2АДГ-ДСАПП-4", f"Съоръжение: 2АДГ-ДСАПП-4\nПроверка: Ф.И на аварийното ел.захранване на СПИ\nСмяна: {shift}"))
        # 16
        if current_month in [1, 4, 7, 10] and thursday_week == 3:
            events.append((current, "🚨 Проверка ДГ-КАС", f"Съоръжение: ДГ-КАС\nПроверка: Ф.И на аварийното ел.захранване на СПИ\nСмяна: {shift}"))
        # 17
        if current_month in [6, 12] and monday_week == 3:
            events.append((current, "🚨 Проверка ГРТ-ЦНРД", f"Съоръжение: ГРТ-ЦНРД\nПроверка: Изпробване на АВР на ел.захранването\nСмяна: {shift}"))
        # 18
        if current_day == 1:
            events.append((current, "🚨 Отчитане електромери", f"Съоръжение: По методика ДП.ЕД.МТ.1153\nПроверка: Отчитане електомерите за консумирана ел.енергия\nСмяна: Смяна 2"))
        # 19
        if saturday_week == 3:
            events.append((current, "🚨 Проверка ТП1, ТП3", f"Съоръжение: ТП1,ТП3\nПроверка: Изпропване на охлаждащите вентилатори на 1ТП и 3ТП чрез ръчно включване\nСмяна: {shift}"))
        # 20
        if wednesday_week == 3 or saturday_week == 3:
            events.append((current, "🚨 Измерване стойности по фидери", f"Съоръжение: По методика ДП.ЕД.МТ.1153\nПроверка: Измерване стойностите по фидерите за АКС,СБК-2 и ТРЗ/Бюро пропуски\nСмяна: {shift}"))

        current += timedelta(days=1)
    
    events.sort(key=lambda x: x[0])
    return events


class NotificationApp(App):
    def build(self):
        self.yearly_events = generate_yearly_schedule(datetime.now().year)

        main_layout = BoxLayout(orientation="vertical", padding=15, spacing=15)

        # 1. Основно заглавие на приложението
        title = Label(text="ГРАФИК ПРОВЕРКИ v2.7", font_size='24sp', bold=True, size_hint_y=None, height=45)
        main_layout.add_widget(title)

        # 2. Каре: ПОСЛЕДНО МИНАЛО СЪБИТИЕ (Изцяло нов стабилен Layout)
        self.past_box = BoxLayout(orientation="vertical", padding=12, spacing=4, size_hint_y=None, height=210)
        with self.past_box.canvas.before:
            Color(0.18, 0.18, 0.24, 1) 
            self.rect1 = Rectangle(size=self.past_box.size, pos=self.past_box.pos)
        self.past_box.bind(size=self._update_rect1, pos=self._update_rect1)
        
        past_title_lbl = Label(text="ПОСЛЕДНО МИНАЛО СЪБИТИЕ:", bold=True, color=(0.7, 0.7, 0.7, 1), font_size='14sp', size_hint_y=None, height=20, halign='left')
        past_title_lbl.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        
        # Разделени етикети за Име и Описание за стабилност
        self.past_header = Label(text="Няма данни", font_size='16sp', bold=True, color=(1, 0.5, 0.5, 1), size_hint_y=None, height=25, halign='left')
        self.past_header.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        
        self.past_desc = Label(text="Натиснете бутона за старт или ръчен тест.", font_size='15sp', color=(0.9, 0.9, 0.9, 1), halign='left', valign='top')
        self.past_desc.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        
        self.past_box.add_widget(past_title_lbl)
        self.past_box.add_widget(self.past_header)
        self.past_box.add_widget(self.past_desc)
        main_layout.add_widget(self.past_box)

        # 3. Каре: СЛЕДВАЩО ПРЕДСТОЯЩО СЪБИТИЕ
        self.next_box = BoxLayout(orientation="vertical", padding=12, spacing=4, size_hint_y=None, height=210)
        with self.next_box.canvas.before:
            Color(0.12, 0.22, 0.18, 1) 
            self.rect2 = Rectangle(size=self.next_box.size, pos=self.next_box.pos)
        self.next_box.bind(size=self._update_rect2, pos=self._update_rect2)

        next_title_lbl = Label(text="СЛЕДВАЩО ПРЕДСТОЯЩО СЪБИТИЕ:", bold=True, color=(0.7, 0.7, 0.7, 1), font_size='14sp', size_hint_y=None, height=20, halign='left')
        next_title_lbl.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        
        self.next_header = Label(text="Няма данни", font_size='16sp', bold=True, color=(0.4, 1, 0.4, 1), size_hint_y=None, height=25, halign='left')
        self.next_header.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        
        self.next_desc = Label(text="Натиснете бутона за старт или ръчен тест.", font_size='15sp', color=(0.9, 0.9, 0.9, 1), halign='left', valign='top')
        self.next_desc.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        
        self.next_box.add_widget(next_title_lbl)
        self.next_box.add_widget(self.next_header)
        self.next_box.add_widget(self.next_desc)
        main_layout.add_widget(self.next_box)

        # 4. Долно поле за статус
        scroll = ScrollView()
        self.status_label = Label(text="Системата е готова.", font_size='15sp', size_hint_y=None, halign='center', color=(0.8, 0.8, 0.8, 1))
        self.status_label.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        self.status_label.bind(texture_size=self.status_label.setter('size'))
        scroll.add_widget(self.status_label)
        main_layout.add_widget(scroll)

        # 5. Бутон за ръчен тест (Оранжев)
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

    def trigger_manual_test(self, instance):
        self.update_events_display()
        now = datetime.now()
        self.status_label.text = f"Ръчно сканиране... УСПЕШНО!\nЧас: {now.strftime('%H:%M:%S')}"

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

        for event_date, title_text, full_msg in self.yearly_events:
            if event_date.date() <= now.date():
                past_event = (event_date, title_text, full_msg)
            elif event_date.date() > now.date() and next_event is None:
                next_event = (event_date, title_text, full_msg)

        # Безопасно разпределяне на данните без застъпване
        if past_event:
            date_str = past_event[0].strftime('%d.%m.%Y')
            self.past_header.text = f"Дата: {date_str}  |  {past_event[1]}"
            self.past_desc.text = past_event[2]
        else:
            self.past_header.text = "Няма събития"
            self.past_desc.text = ""

        if next_event:
            date_str = next_event[0].strftime('%d.%m.%Y')
            self.next_header.text = f"Дата: {date_str}  |  {next_event[1]}"
            self.next_desc.text = next_event[2]
        else:
            self.next_header.text = "Няма предстоящи събития"
            self.next_desc.text = ""

        if self.is_running:
            self.status_label.text = f"Последна автоматична проверка:\n{now.strftime('%H:%M:%S')}"

if __name__ == "__main__":
    NotificationApp().run()
