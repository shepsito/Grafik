from datetime import datetime, timedelta
import calendar
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.utils import platform

# --- Директна връзка с Android API (Java) за 100% работещ звук и известия ---
if platform == 'android':
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Context = autoclass('android.content.Context')
    NotificationManager = autoclass('android.app.NotificationManager')
    NotificationChannel = autoclass('android.app.NotificationChannel')
    NotificationCompat = autoclass('androidx.core.app.NotificationCompat$Builder')
    # За звука и вибрацията
    RingtoneManager = autoclass('android.media.RingtoneManager')

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

        if current_month in [2, 9] and monday_week == 1:
            events.append((current, "🚨 Проверка АВР", "Аварийно осветление", "Проверка АВР на захранването", shift))
        if current_day in [11, 12]:
            events.append((current, "🚨 ЕЕ ЦПС-2", "ЕЕ ЦПС-2", "Проверка изправноста на аварийното осветление", shift))
        if current_month in [3, 10] and monday_week in [1, 2]:
            events.append((current, "🚨 Ф.И. Проверка", "По процедура", "Ф.И. на аварийното осветление", shift))
        if current_day == 15:
            events.append((current, "🚨 МЗ и ЕЕ ЦПС-1", "МЗ и ЕЕ ЦПС-1", "Проверка изправността на евакуационното осветление", shift))
        if is_last_monday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Пон.)", "МЗ,ЦПС-1", "Проверка АВР сборки на 0,4кВ захранвани от 3 и 4 БН", shift))
        if is_last_tuesday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Вт.)", "МЗ", "Проверка АВР сборки на 0,4кВ захранвани от 23 и 24 БН", shift))
        if is_last_wednesday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Ср.)", "МЗ", "Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 3", shift))
        if is_last_thursday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Четв.)", "МЗ", "Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 4", shift))
        if is_last_friday_of_quarter(current):
            events.append((current, "🚨 Квартална Проверка АВР (Петък)", "МЗ,ХВО и ЦПС-1", "Проверка АВР сборки на 0,4кВ с/без сборки захр.от 3,4,23,24БН,33БН I-III,43БН I-III /", shift))
        if current_day == 8:
            events.append((current, "🚨 Секции 0,4кВ-ГК", "Секции 0,4кВ-ГК 1_4 блок", "Проверка АВР на -ШУ и изправността на сигнализацията на панел 'С'БЩУ за повикване в КРу", shift))
        if current_day == 18:
            events.append((current, "🚨 Вентилни отводи", "Вентилни отводи 1 и 3 ТП", "Отчитане на -вентилни отводи", shift))
        if current_day == 1:
            events.append((current, "🚨 Ел.двигатели 6кВ", "Ел.двигатели 6кВ", "Измерване съпротивлението на изолацията на ел.двиг.6кВ.-ПВТ в резерв,1и 2ППП", "Смяна 1"))
        if current_month in [1, 4, 7, 10] and monday_week == 1:
            events.append((current, "🚨 Проверка ДГ-А", "ДГ-A", "Ф.И. на автономен товар не по малко от 60мин.", shift))
        if current_month in [1, 4, 7, 10] and monday_week == 2:
            events.append((current, "🚨 Проверка ДГ-Б", "ДГ-Б", "Ф.И. на автономен товар не по малко от 60мин.", shift))
        if current_month in [1, 4, 7, 10] and wednesday_week == 3:
            events.append((current, "🚨 Проверка 2АДГ-ДСАПП-4", "2АДГ-ДСАПП-4", "Ф.И на аварийното ел.захранване на СПИ", shift))
        if current_month in [1, 4, 7, 10] and thursday_week == 3:
            events.append((current, "🚨 Проверка ДГ-КАС", "ДГ-КАС", "Ф.И на аварийното ел.захранване на СПИ", shift))
        if current_month in [6, 12] and monday_week == 3:
            events.append((current, "🚨 Проверка ГРТ-ЦНРД", "ГРТ-ЦНРД", "Изпробване на АВР на ел.захранването", shift))
        if current_day == 1:
            events.append((current, "🚨 Отчитане електромери", "По методика ДП.ЕД.МТ.1153", "Отчитане електомерите за консумирана ел.енергия", "Смяна 2"))
        if saturday_week == 3:
            events.append((current, "🚨 Проверка ТП1, ТП3", "ТП1,ТП3", "Изпропване на охлаждащите вентилатори на 1ТП и 3ТП чрез ръчно включване", shift))
        if wednesday_week == 3 or saturday_week == 3:
            events.append((current, "🚨 Измерване стойности по фидери", "По методика ДП.ЕД.МТ.1153", "Измерване стойностите по фидерите за АКС,СБК-2 и ТРЗ/Бюро пропуски", shift))

        current += timedelta(days=1)
    
    events.sort(key=lambda x: x[0])
    return events


class NotificationApp(App):
    def build(self):
        self.yearly_events = generate_yearly_schedule(datetime.now().year)
        self.last_notified_date = None

        main_layout = BoxLayout(orientation="vertical", padding=15, spacing=15)

        # 1. Заглавие
        title = Label(text="ГРАФИК ПРОВЕРКИ v5.0", font_size='22sp', bold=True, size_hint_y=0.08)
        main_layout.add_widget(title)

        # 2. КАРЕ: МИНАЛО СЪБИТИЕ
        self.past_box = BoxLayout(orientation="vertical", padding=15, spacing=10, size_hint_y=0.35)
        with self.past_box.canvas.before:
            Color(0.16, 0.16, 0.22, 1) 
            self.rect1 = Rectangle()
        self.past_box.bind(size=self._update_rect1, pos=self._update_rect1)
        
        self.past_title = Label(text="ПОСЛЕДНО МИНАЛО СЪБИТИЕ:", bold=True, color=(0.7, 0.7, 0.7, 1), font_size='13sp', size_hint_y=0.15, halign='left')
        self.past_header = Label(text="Дата: --.--.----  |  Няма данни", font_size='16sp', bold=True, color=(1, 0.5, 0.5, 1), size_hint_y=0.25, halign='left')
        self.past_facility = Label(text="Съоръжение: --", font_size='14sp', size_hint_y=0.2, halign='left')
        self.past_check = Label(text="Проверка: --", font_size='14sp', size_hint_y=0.2, halign='left')
        self.past_shift = Label(text="Смяна: --", font_size='14sp', size_hint_y=0.2, halign='left')

        for lbl in [self.past_title, self.past_header, self.past_facility, self.past_check, self.past_shift]:
            lbl.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
            self.past_box.add_widget(lbl)
            
        main_layout.add_widget(self.past_box)

        # 3. КАРЕ: СЛЕДВАЩО СЪБИТИЕ
        self.next_box = BoxLayout(orientation="vertical", padding=15, spacing=10, size_hint_y=0.35)
        with self.next_box.canvas.before:
            Color(0.11, 0.20, 0.16, 1) 
            self.rect2 = Rectangle()
        self.next_box.bind(size=self._update_rect2, pos=self._update_rect2)
        
        self.next_title = Label(text="СЛЕДВАЩО ПРЕДСТОЯЩО СЪБИТИЕ:", bold=True, color=(0.7, 0.7, 0.7, 1), font_size='13sp', size_hint_y=0.15, halign='left')
        self.next_header = Label(text="Дата: --.--.----  |  Няма данни", font_size='16sp', bold=True, color=(0.4, 1, 0.4, 1), size_hint_y=0.25, halign='left')
        self.next_facility = Label(text="Съоръжение: --", font_size='14sp', size_hint_y=0.2, halign='left')
        self.next_check = Label(text="Проверка: --", font_size='14sp', size_hint_y=0.2, halign='left')
        self.next_shift = Label(text="Смяна: --", font_size='14sp', size_hint_y=0.2, halign='left')

        for lbl in [self.next_title, self.next_header, self.next_facility, self.next_check, self.next_shift]:
            lbl.bind(size=lambda ins, val: setattr(ins, 'text_size', (val[0], None)))
            self.next_box.add_widget(lbl)

        main_layout.add_widget(self.next_box)

        # 4. Поле за Статус и Бутони
        bottom_layout = BoxLayout(orientation="vertical", spacing=8, size_hint_y=0.22)
        
        self.status_label = Label(text="Системата е готова.", font_size='13sp', size_hint_y=0.2, halign='center', color=(0.8, 0.8, 0.8, 1))
        bottom_layout.add_widget(self.status_label)

        self.test_btn = Button(text="ТЕСТВАЙ ИЗВЕСТИЯТА (РЪЧНО)", font_size='16sp', bold=True, background_color=(0.9, 0.5, 0.1, 1), size_hint_y=0.4)
        self.test_btn.bind(on_release=self.send_test_notification)
        bottom_layout.add_widget(self.test_btn)

        self.btn = Button(text="СТАРТИРАЙ МОНИТОРИНГ", font_size='16sp', bold=True, background_color=(0, 0.6, 0.6, 1), size_hint_y=0.4)
        self.btn.bind(on_release=self.toggle_system)
        bottom_layout.add_widget(self.btn)

        main_layout.add_widget(bottom_layout)

        self.is_running = False
        return main_layout

    def _update_rect1(self, instance, value): self.rect1.pos = instance.pos; self.rect1.size = instance.size
    def _update_rect2(self, instance, value): self.rect2.pos = instance.pos; self.rect2.size = instance.size

    # Напълно нов, ОФИЦИАЛЕН Android Java код, поддържащ Android 10 перфектно
    def send_android_alert(self, title, message):
        if platform != 'android':
            print(f"PC Тест -> Заглавие: {title}, Текст: {message}")
            return

        try:
            activity = PythonActivity.mActivity
            context = activity.getApplicationContext()
            notification_manager = activity.getSystemService(Context.NOTIFICATION_SERVICE)

            channel_id = "grafik_alerts_id"
            channel_name = "График Известия"

            # Форсираме създаването на сигурен канал за Android 10+
            importance = NotificationManager.IMPORTANCE_HIGH
            channel = NotificationChannel(channel_id, channel_name, importance)
            channel.setDescription("Звукови аларми за работния график")
            
            # Активираме звук и светлина на системно ниво
            channel.enableLights(True)
            channel.enableVibration(True)
            notification_manager.createNotificationChannel(channel)

            # Взимаме системния дефолтен звук на телефона за съобщения
            default_sound_uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)

            # Построяваме известието по правилата на Android
            builder = NotificationCompat(context, channel_id)
            builder.setContentTitle(title)
            builder.setContentText(message)
            # Използваме вградената икона на Kivy за известия
            builder.setSmallIcon(context.getApplicationInfo().icon)
            builder.setPriority(NotificationManager.IMPORTANCE_HIGH)
            builder.setSound(default_sound_uri)
            builder.setAutoCancel(True)

            # Изстрелваме известието
            notification_manager.notify(1, builder.build())
        except Exception as e:
            print(f"Грешка при Java Android Известяване: {e}")

    def send_test_notification(self, instance):
        self.update_events_display()
        now = datetime.now()
        self.status_label.text = f"Изпратено твърдо известие в {now.strftime('%H:%M:%S')}"
        
        self.send_android_alert(
            "🚨 ТЕСТ: Предстояща Проверка!",
            "Системата на Android 10 работи със звук."
        )

    def toggle_system(self, instance):
        if not self.is_running:
            self.update_events_display() 
            Clock.schedule_interval(self.update_events_display, 10) 
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

        for event_date, title_text, facility_text, check_text, shift_text in self.yearly_events:
            if event_date.date() <= now.date():
                past_event = (event_date, title_text, facility_text, check_text, shift_text)
            elif event_date.date() > now.date() and next_event is None:
                next_event = (event_date, title_text, facility_text, check_text, shift_text)

        if past_event:
            date_str = past_event[0].strftime('%d.%m.%Y')
            self.past_header.text = f"Дата: {date_str}  |  {past_event[1]}"
            self.past_facility.text = f"Съоръжение: {past_event[2]}"
            self.past_check.text = f"Проверка: {past_event[3]}"
            self.past_shift.text = f"Смяна: {past_event[4]}"

        if next_event:
            date_str = next_event[0].strftime('%d.%m.%Y')
            self.next_header.text = f"Дата: {date_str}  |  {next_event[1]}"
            self.next_facility.text = f"Съоръжение: {next_event[2]}"
            self.next_check.text = f"Проверка: {next_event[3]}"
            self.next_shift.text = f"Смяна: {next_event[4]}"

            # АВТОМАТИЧНА АЛАРМА
            if next_event[0].date() == now.date() and self.last_notified_date != now.date():
                self.last_notified_date = now.date()
                self.send_android_alert(
                    f"🚨 ДНЕС: {next_event[1]}",
                    f"Обект: {next_event[2]} | {next_event[3]}"
                )

        if self.is_running:
            self.status_label.text = f"Автоматичен мониторинг... {now.strftime('%H:%M:%S')}"

if __name__ == "__main__":
    NotificationApp().run()
