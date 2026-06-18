from datetime import datetime, timedelta
import calendar
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from plyer import notification

# --- Помощни логически функции за графика ---

def get_monday_week_number(date):
    """Връща поредността на понеделника в месеца (1 за първи, 2 за втори и т.н.)."""
    if date.weekday() != 0: # 0 е Понеделник
        return 0
    if date.day <= 7:
        return 1
    elif date.day <= 14:
        return 2
    elif date.day <= 21:
        return 3
    else:
        return 4

def get_wednesday_week_number(date):
    """Връща поредността на срядата в месеца (1 за първа, 2 за втора, 3 за трета и т.н.)."""
    if date.weekday() != 2: # 2 е Сряда
        return 0
    if date.day <= 7:
        return 1
    elif date.day <= 14:
        return 2
    elif date.day <= 21:
        return 3
    else:
        return 4

def get_thursday_week_number(date):
    """Връща поредността на четвъртъка в месеца (1 за първи, 2 за втори, 3 за трети и т.н.)."""
    if date.weekday() != 3: # 3 е Четвъртък
        return 0
    if date.day <= 7:
        return 1
    elif date.day <= 14:
        return 2
    elif date.day <= 21:
        return 3
    else:
        return 4

def get_saturday_week_number(date):
    """Връща поредността на съботата в месеца (1 за първа, 2 за втора, 3 за трета и т.н.)."""
    if date.weekday() != 5: # 5 е Събота
        return 0
    if date.day <= 7:
        return 1
    elif date.day <= 14:
        return 2
    elif date.day <= 21:
        return 3
    else:
        return 4

def is_last_monday_of_quarter(date):
    """Проверява дали дадена дата е ПОСЛЕДНИЯТ понеделник на тримесечието."""
    if date.weekday() != 0: 
        return False
    if date.month in [3, 6, 9, 12]:
        last_day_of_month = calendar.monthrange(date.year, date.month)[1]
        if last_day_of_month - date.day < 7:
            return True
    return False

def is_last_tuesday_of_quarter(date):
    """Проверява дали дадена дата е ПОСЛЕДНИЯТ вторник на тримесечието."""
    if date.weekday() != 1: # 1 е Вторник
        return False
    if date.month in [3, 6, 9, 12]:
        last_day_of_month = calendar.monthrange(date.year, date.month)[1]
        if last_day_of_month - date.day < 7:
            return True
    return False

def is_last_wednesday_of_quarter(date):
    """Проверява дали дадена дата е ПОСЛЕДНАТА сряда на тримесечието."""
    if date.weekday() != 2: # 2 е Сряда
        return False
    if date.month in [3, 6, 9, 12]:
        last_day_of_month = calendar.monthrange(date.year, date.month)[1]
        if last_day_of_month - date.day < 7:
            return True
    return False

def is_last_thursday_of_quarter(date):
    """Проверява дали дадена дата е ПОСЛЕДНИЯТ четвъртък на тримесечието."""
    if date.weekday() != 3: # 3 е Четвъртък
        return False
    if date.month in [3, 6, 9, 12]:
        last_day_of_month = calendar.monthrange(date.year, date.month)[1]
        if last_day_of_month - date.day < 7:
            return True
    return False

def is_last_friday_of_quarter(date):
    """Проверява дали дадена дата е ПОСЛЕДНИЯТ петък на тримесечието."""
    if date.weekday() != 4: # 4 е Петък
        return False
    if date.month in [3, 6, 9, 12]:
        last_day_of_month = calendar.monthrange(date.year, date.month)[1]
        if last_day_of_month - date.day < 7:
            return True
    return False

def get_shift_by_hour(hour):
    """Връща името на смяната спрямо текущия час."""
    if hour == 15:
        return "Смяна 3"
    elif hour == 23:
        return "Смяна 1"
    elif hour == 7:
        return "Смяна 2"
    return None


# --- Основен интерфейс на приложението ---
class NotificationApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"

        layout = MDBoxLayout(orientation="vertical")

        toolbar = MDTopAppBar(title="Годишен График за Проверки")
        layout.add_widget(toolbar)

        self.status_label = MDLabel(
            text="Графикът не е стартиран.\nНатиснете бутона по-долу.",
            halign="center",
            theme_text_color="Secondary",
            font_style="H6"
        )
        layout.add_widget(self.status_label)

        self.action_button = MDRaisedButton(
            text="СТАРТИРАЙ ГРАФИКА",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, 0.1),
            on_release=self.toggle_schedule
        )
        layout.add_widget(self.action_button)
        layout.add_widget(MDBoxLayout(size_hint_y=0.2))

        self.is_running = False
        return layout

    def toggle_schedule(self, instance):
        if not self.is_running:
            Clock.schedule_interval(self.check_schedule, 60)
            self.status_label.text = "🟢 Графикът работи на заден план.\nСледи се за събития..."
            self.action_button.text = "СПРИ ГРАФИКА"
            self.action_button.md_bg_color = (0.8, 0.2, 0.2, 1)
            self.is_running = True
            self.send_alert("Графикът е активен", "Успешно стартиране!")
        else:
            Clock.unschedule(self.check_schedule)
            self.status_label.text = "🔴 Графикът е спрян.\nНяма да получавате известия."
            self.action_button.text = "СТАРТИРАЙ ГРАФИКА"
            self.action_button.md_bg_color = self.theme_cls.primary_color
            self.is_running = False

    def check_schedule(self, dt):
        now = datetime.now()

        # Проверяваме само на кръгъл час (минута 00)
        if now.minute != 0:
            return

        current_month = now.month
        current_day = now.day
        current_hour = now.hour

        shift = get_shift_by_hour(current_hour)
        if not shift:
            return

        monday_week = get_monday_week_number(now)
        wednesday_week = get_wednesday_week_number(now)
        thursday_week = get_thursday_week_number(now)
        saturday_week = get_saturday_week_number(now)

        # --- ПРАВИЛО 1: Февруари и Септември (Първи Понеделник) ---
        if current_month in [2, 9] and monday_week == 1:
            msg = f"Съоръжение: Аварийно осветление\nПроверка: Проверка АВР на захранването\nСмяна: {shift}"
            self.send_alert("🚨 График: Проверка АВР", msg)

        # --- ПРАВИЛО 2: Всеки месец на 11-то и 12-то число ---
        if current_day in [11, 12]:
            msg = f"Съоръжение: ЕЕ ЦПС-2\nПроверка: Проверка изправноста на аварийното осветление\nСмяна: {shift}"
            self.send_alert("🚨 График: ЕЕ ЦПС-2", msg)

        # --- ПРАВИЛО 3: Март и Октомври (Първи и Втори Понеделник) ---
        if current_month in [3, 10] and monday_week in [1, 2]:
            msg = f"Съоръжение: По процедура\nПроверка: Ф.И. на аварийното осветление\nСмяна: {shift}"
            self.send_alert("🚨 График: Ф.И. Проверка", msg)

        # --- ПРАВИЛО 4: Всеки месец на 15-то число ---
        if current_day == 15:
            msg = f"Съоръжение: МЗ и ЕЕ ЦПС-1\nПроверка: Проверка изправността на евакуационното осветление\nСмяна: {shift}"
            self.send_alert("🚨 График: МЗ и ЕЕ ЦПС-1", msg)

        # --- ПРАВИЛО 5: Последен понеделник на всяко тримесечие ---
        if is_last_monday_of_quarter(now):
            msg = f"Съоръжение: МЗ,ЦПС-1\nПроверка: Проверка АВР сборки на 0,4кВ захранвани от 3 и 4 БН\nСмяна: {shift}"
            self.send_alert("🚨 График: Квартална Проверка АВР (Пон.)", msg)

        # --- ПРАВИЛО 6: Последен вторник на всяко тримесечие ---
        if is_last_tuesday_of_quarter(now):
            msg = f"Съоръжение: МЗ\nПроверка: Проверка АВР сборки на 0,4кВ захранвани от 23 и 24 БН\nСмяна: {shift}"
            self.send_alert("🚨 График: Квартална Проверка АВР (Вт.)", msg)

        # --- ПРАВИЛО 7: Последна сряда на всяко тримесечие ---
        if is_last_wednesday_of_quarter(now):
            msg = f"Съоръжение: МЗ\nПроверка: Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 3\nСмяна: {shift}"
            self.send_alert("🚨 График: Квартална Проверка АВР (Ср.)", msg)

        # --- ПРАВИЛО 8: Последен четвъртък на всяко тримесечие ---
        if is_last_thursday_of_quarter(now):
            msg = f"Съоръжение: МЗ\nПроверка: Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 4\nСмяна: {shift}"
            self.send_alert("🚨 График: Квартална Проверка АВР (Четв.)", msg)

        # --- ПРАВИЛО 9: Последен петък на всяко тримесечие ---
        if is_last_friday_of_quarter(now):
            msg = f"Съоръжение: МЗ,ХВО и ЦПС-1\nПроверка: Проверка АВР сборки на 0,4кВ с/без сборки захр.от 3,4,23,24БН,33БН I-III,43БН I-III /\nСмяна: {shift}"
            self.send_alert("🚨 График: Квартална Проверка АВР (Петък)", msg)

        # --- ПРАВИЛО 10: Всеки месец на 8-мо число ---
        if current_day == 8:
            msg = f"Съоръжение: Секции 0,4кВ-ГК 1_4 блок\nПроверка: Проверка АВР на -ШУ и изправността на сигнализацията на панел 'С'БЩУ за повикване в КРу\nСмяна: {shift}"
            self.send_alert("🚨 График: Секции 0,4кВ-ГК", msg)

        # --- ПРАВИЛО 11: Всеки месец на 18-то число ---
        if current_day == 18:
            msg = f"Съоръжение: Вентилни отводи 1 и 3 ТП\nПроверка: Отчитане на -вентилни отводи\nСмяна: {shift}"
            self.send_alert("🚨 График: Вентилни отводи", msg)

        # --- ПРАВИЛО 12: Всеки месец на 1-во число (Смяна 1) ---
        if current_day == 1 and shift == "Смяна 1":
            msg = f"Съоръжение: Ел.двигатели 6кВ\nПроверка: Измерване съпротивлението на изолацията на ел.двиг.6кВ.-ПВТ в резерв,1и 2ППП\nСмяна: {shift}"
            self.send_alert("🚨 График: Ел.двигатели 6кВ", msg)

        # --- ПРАВИЛО 13: Януари, Април, Юли, Октомври (Първи Понеделник) ---
        if current_month in [1, 4, 7, 10] and monday_week == 1:
            msg = f"Съоръжение: ДГ-A\nПроверка: Ф.И. на автономен товар не по малко от 60мин.\nСмяна: {shift}"
            self.send_alert("🚨 График: Проверка ДГ-А", msg)

        # --- ПРАВИЛО 14: Януари, Април, Юли, Октомври (Втори Понеделник) ---
        if current_month in [1, 4, 7, 10] and monday_week == 2:
            msg = f"Съоръжение: ДГ-Б\nПроверка: Ф.И. на автономен товар не по малко от 60мин.\nСмяна: {shift}"
            self.send_alert("🚨 График: Проверка ДГ-Б", msg)

        # --- ПРАВИЛО 15: Януари, Април, Юли, Октомври (Трета Сряда) ---
        if current_month in [1, 4, 7, 10] and wednesday_week == 3:
            msg = f"Съоръжение: 2АДГ-ДСАПП-4\nПроверка: Ф.И на аварийното ел.захранване на СПИ\nСмяна: {shift}"
            self.send_alert("🚨 График: Проверка 2АДГ-ДСАПП-4", msg)

        # --- ПРАВИЛО 16: Януари, Април, Юли, Октомври (Tрети Четвъртък) ---
        if current_month in [1, 4, 7, 10] and thursday_week == 3:
            msg = f"Съоръжение: ДГ-КАС\nПроверка: Ф.И на аварийното ел.захранване на СПИ\nСмяна: {shift}"
            self.send_alert("🚨 График: Проверка ДГ-КАС", msg)

        # --- ПРАВИЛО 17: Юни, Декември (Трети Понеделник) ---
        if current_month in [6, 12] and monday_week == 3:
            msg = f"Съоръжение: ГРТ-ЦНРД\nПроверка: Изпробване на АВР на ел.захранването\nСмяна: {shift}"
            self.send_alert("🚨 График: Проверка ГРТ-ЦНРД", msg)

        # --- ПРАВИЛО 18: Всеки месец на 1-во число (Смяна 2) ---
        if current_day == 1 and shift == "Смяна 2":
            msg = f"Съоръжение: По методика ДП.ЕД.МТ.1153\nПроверка: Отчитане електомерите за консумирана ел.енергия\nСмяна: {shift}"
            self.send_alert("🚨 График: Отчитане електромери", msg)

        # --- ПРАВИЛО 19: Всеки месец, Трета Събота ---
        if saturday_week == 3:
            msg = f"Съоръжение: ТП1,ТП3\nПроверка: Изпропване на охлаждащите вентилатори на 1ТП и 3ТП чрез ръчно включване\nСмяна: {shift}"
            self.send_alert("🚨 График: Проверка ТП1, ТП3", msg)

        # --- ПРАВИЛО 20: Всеки месец, Трета Сряда ИЛИ Трета Събота (За всички смени) ---
        if wednesday_week == 3 or saturday_week == 3:
            msg = f"Съоръжение: По методика ДП.ЕД.МТ.1153\nПроверка: Измерване стойностите по фидерите за АКС,СБК-2 и ТРЗ/Бюро пропуски\nСмяна: {shift}"
            self.send_alert("🚨 График: Измерване стойности по фидери", msg)

    def send_alert(self, title, message):
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Работен График",
                timeout=15
            )
        except Exception as e:
            print(f"Грешка при известие: {e}")

if __name__ == "__main__":
    NotificationApp().run()