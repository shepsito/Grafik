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


# --- Генериране на годишния календар с ПРАЗНИ РЕДОВЕ между детайлите ---
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

        # Правило 1
        if current_month in [2, 9] and monday_week == 1:
            events.append((current, "🚨 Проверка АВР", f"Съоръжение: Аварийно осветление\n\nПроверка: Проверка АВР на захранването\n\nСмяна: {shift}"))
        # Правило 2
        if current_day in [11, 12]:
            events.append((current, "🚨 ЕЕ ЦПС-2", f"Съоръжение: ЕЕ ЦПС-2\n\nПроверка: Проверка изправноста на аварийното осветление\n\nСмяна: {shift}"))
        # Правило 3
        if current_month in [3, 10] and monday_week in [1, 2]:
            events.append((current, "🚨 Ф.И. Проверка", f"Съоръжение: По процедура\n\nПроверка: Ф.И. на аварийното осветление\n\nСмяна: {shift}"))
        # Правило 4
        if current_day == 15:
            events.append((current, "🚨 МЗ и ЕЕ ЦПС-1", f"Съоръжение: МЗ и ЕЕ ЦПС-1\n\nПроверка: Проверка изправността на евакуационното осветление\n\nСмяна: {shift}"))
        # Правило 5
        if is_last_monday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Пон.)", f"Съоръжение: МЗ,ЦПС-1\n\nПроверка: Проверка АВР сборки на 0,4кВ захранвани от 3 и 4 БН\n\nСмяна: {shift}"))
        # Правило 6
        if is_last_tuesday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Вт.)", f"Съоръжение: МЗ\n\nПроверка: Проверка АВР сборки на 0,4кВ захранвани от 23 и 24 БН\n\nСмяна: {shift}"))
        # Правило 7
        if is_last_wednesday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Ср.)", f"Съоръжение: МЗ\n\nПроверка: Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 3\n\nСмяна: {shift}"))
        # Правило 8
        if is_last_thursday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Четв.)", f"Съоръжение: МЗ\n\nПроверка: Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 4\n\nСмяна: {shift}"))
        # Правило 9
        if is_last_friday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Петък)", f"Съоръжение: МЗ,ХВО и ЦПС-1\n\nПроверка: Проверка АВР сборки на 0,4кВ с/без сборки захр.от 3,4,23,24БН,33БН I-III,43БН I-III /\n\nСмяна: {shift}"))
        # Правило 10
        if current_day == 8:
            events.append((current, "🚨 Секции 0,4кВ-ГК", f"Съоръжение: Секции 0,4кВ-ГК 1_4 block\n\nПроверка: Проверка АВР на -ШУ и изправността на сигнализацията на панел 'С'БЩУ за повикване в КРу\n\nСмяна: {shift}"))
        # Правило 11
        if current_day == 18:
            events.append((current, "🚨 Вентилни отводи", f"Съоръжение: Вентилни отводи 1 и 3 ТП\n\nПроверка: Отчитане на -вентилни отводи\n\nСмяна: {shift}"))
        # Правило 12
        if current_day == 1:
            events.append((current, "🚨 Ел.двигатели 6кВ", f"Съоръжение: Ел.двигатели 6кВ\n\nПроверка: Измерване съпротивлението на изолацията на ел.двиг.6кВ.-ПВТ в резерв,1и 2ППП\n\nСмяна: Смяна 1"))
        # Правило 13
        if current_month in [1, 4, 7, 10] and monday_week == 1:
            events.append((current, "🚨 Проверка ДГ-А", f"Съоръжение: ДГ-A\n\nПроверка: Ф.И. на автономен товар не по малко от 60мин.\n\nСмяна: {shift}"))
        # Правило 14
        if current_month in [1, 4, 7, 10] and monday_week == 2:
            events.append((current, "🚨 Проверка ДГ-Б", f"Съоръжение: ДГ-Б\n\nПроверка: Ф.И. на автономен товар не по малко от 60мин.\n\nСмяна: {shift}"))
        # Правило 15
        if current_month in [1, 4, 7, 10] and wednesday_week == 3:
            events.append((current, "🚨 Проверка 2АДГ-ДСАПП-4", f"Съоръжение: 2АДГ-ДСАПП-4\n\nПроверка: Ф.И на аварийното ел.захранване на СПИ\n\nСмяна: {shift}"))
        # Правило 16
        if current_month in [1, 4, 7, 10] and thursday_week == 3:
            events.append((current, "🚨 Проверка ДГ-КАС", f"Съоръжение: ДГ-КАС\n\nПроверка: Ф.И на аварийното ел.захранване на СПИ\n\nСмяна: {shift}"))
        # Правило 17
        if current_month in [6, 12] and monday_week == 3:
            events.append((current, "🚨 Проверка ГРТ-ЦНРД", f"Съоръжение: ГРТ-ЦНРД\n\nПроверка: Изпробване на АВР на ел.захранването\n\nСмяна: {shift}"))
        # Правило 18
        if current_day == 1:
            events.append((current, "🚨 Отчитане електромери", f"Съоръжение: По методика ДП.ЕД.МТ.1153\n\nПроверка: Отчитане електомерите за консумирана ел.енергия\n\nСмяна: Смяна 2"))
        # Правило 19
        if saturday_week == 3:
            events.append((current, "🚨 Проверка ТП1, ТП3", f"Съоръжение: ТП1,ТП3\n\nПроверка: Изпропване на охлаждащите вентилатори на 1ТП и 3ТП чрез ръчно включване\n\nСмяна: {shift}"))
        # Правило 20
        if wednesday_week == 3 or saturday_week == 3:
            events.append((current, "🚨 Измерване стойности по фидери", f"Съоръжение: По методика ДП.ЕД.МТ.1153\n\nПроверка: Измерване стойностите по фидерите за АКС,СБК-2 и ТРЗ/Бюро пропуски\n\nСмяна: {shift}"))

        current += timedelta(days=1)
    
    events.sort(key=lambda x: x[0])
    return events


class NotificationApp(App):
    def build(self):
        self.yearly_events = generate_yearly_schedule(datetime.now().year)

        main_layout = BoxLayout(orientation="vertical", padding=12, spacing=12)

        # 1. Основно заглавие
        title = Label(text="ГРАФИК ПРОВЕРКИ v2.8", font_size='22sp', bold=True, size_hint_y=None, height=40)
        main_layout.add_widget(title)

        # 2. Каре: ПОСЛЕДНО МИНАЛО СЪБИТИЕ (Височина 260 за раздалечените редове)
        self.past_box = BoxLayout(orientation="vertical", padding=12, spacing=4, size_hint_y=None, height=260)
        with self.past_box.canvas.before:
            Color(0.18, 0.18, 0.24, 1) 
            self.rect1 = Rectangle(size=self.past_box.size, pos=self.past_box.pos)
        self.past_box.bind(size=self._update_rect1, pos=self._update_rect1)
        
        past_title_lbl = Label(text="ПОСЛЕДНО МИНАЛО СЪБИТИЕ:", bold=True, color=(0.7, 0.7, 0.7, 1), font_size='13sp', size_hint_y=None, height=18, halign='left')
        past_title_lbl.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        self.past_box.add_widget(past_title_lbl)

        self.past_header = Label(text="Няма данни", font_size='15sp', bold=True, color=(1, 0.5, 0.5, 1), size_hint_y=None, height=22, halign='left')
        self.past_header.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        self.past_box.add_widget(self.past_header)

        # Скрол зона за самото дълго описание на миналата задача
        past_scroll = ScrollView()
        self.past_desc = Label(text="Натиснете бутона за старт или ръчен тест.", font_size='15sp', color=(0.9, 0.9, 0.9, 1), size_hint_y=None, halign='left', valign='top')
        self.past_desc.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        self.past_desc.bind(texture_size=self.past_desc.setter('size'))
        past_scroll.add_widget(self.past_desc)
        self.past_box.add_widget(past_scroll)
        
        main_layout.add_widget(self.past_box)

        # 3. Каре: СЛЕДВАЩО ПРЕДСТОЯЩО СЪБИТИЕ (Височина 260)
        self.next_box = BoxLayout(orientation="vertical", padding=12, spacing=4, size_hint_y=None, height=260)
        with self.next_box.canvas.before:
            Color(0.12, 0.22, 0.18, 1) 
            self.rect2 = Rectangle(size=self.next_box.size, pos=self.next_box.pos)
        self.next_box.bind(size=self._update_rect2, pos=self._update_rect2)

        next_title_lbl = Label(text="СЛЕДВАЩО ПРЕДСТОЯЩО СЪБИТИЕ:", bold=True, color=(0.7, 0.7, 0.7, 1), font_size='13sp', size_hint_y=None, height=18, halign='left')
        next_title_lbl.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        self.next_box.add_widget(next_title_lbl)
        
        self.next_header = Label(text="Няма данни", font_size='15sp', bold=True, color=(0.4, 1, 0.4, 1), size_hint_y=None, height=22, halign='left')
        self.next_header.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        self.next_box.add_widget(self.next_header)
        
        # Скрол зона за описанието на следващата задача
        next_scroll = ScrollView()
        self.next_desc = Label(text="Натиснете бутона за старт или ръчен тест.", font_size='15sp', color=(0.9, 0.9, 0.9, 1), size_hint_y=None, halign='left', valign='top')
        self.next_desc.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        self.next_desc.bind(texture_size=self.next_desc.setter('size'))
        next_scroll.add_widget(self.next_desc)
        self.next_box.add_widget(next_scroll)

        main_layout.add_widget(self.next_box)

        # 4. Долно малко поле за статус на системата
        scroll_status = ScrollView(size_hint_y=None, height=40)
        self.status_label = Label(text="Системата е готова.", font_size='14sp', size_hint_y=None, halign='center', color=(0.8, 0.8, 0.8, 1))
        self.status_label.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
        self.status_label.bind(texture_size=self.status_label.setter('size'))
        scroll_status.add_widget(self.status_label)
        main_layout.add_widget(scroll_status)

        # 5. Бутон за ръчен тест (Оранжев)
        self.test_btn = Button(text="ТЕСТВАЙ ИЗВЕСТИЯТА (РЪЧНО)", font_size='16sp', bold=True, background_color=(0.9, 0.5, 0.1, 1), size_hint_y=None, height=50)
        self.test_btn.bind(on_release=self.trigger_manual_test)
        main_layout.add_widget(self.test_btn)

        # 6. Основен Бутон: МОНИТОРИНГ
        self.btn = Button(text="СТАРТИРАЙ МОНИТОРИНГ", font_size='16sp', bold=True, background_color=(0, 0.6, 0.6, 1), size_hint_y=None, height=50)
        self.btn.bind(on_release=self.toggle_system)
        main_layout.add_widget(self.btn)

        self.is_running = False
        return main_layout

    def _update_rect1(self, instance, value): self.rect1.pos = instance.pos; self.rect1.size = instance.size
    def _update_rect2(self, instance, value): self.rect2.pos = instance.pos; self.rect2.size = instance.size

    def trigger_manual_test(self, instance):
        self.update_events_display()
        now = datetime.now()
        self.status_label.text = f"Ръчно сканиране... УСПЕШНО! в {now.strftime('%H:%M:%S')}"

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

        # Прехвърляне на новите структурирани събития с празен ред
        if past_event:
            date_str = past_event[0].strftime('%d.%m.%Y')
            self.past_header.text = f"Дата: {date_str}  |  {past_event[1]}\n"
            self.past_desc.text = past_event[2]
        else:
            self.past_header.text = "Няма събития"
            self.past_desc.text = ""

        if next_event:
            date_str = next_event[0].strftime('%d.%m.%Y')
            self.next_header.text = f"Дата: {date_str}  |  {next_event[1]}\n"
            self.next_desc.text = next_event[2]
        else:
            self.next_header.text = "Няма предстоящи събития"
            self.next_desc.text = ""

        if self.is_running:
            self.status_label.text = f"Последна автоматична проверка: {now.strftime('%H:%M:%S')}"

if __name__ == "__main__":
    NotificationApp().run()
