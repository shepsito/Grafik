from datetime import datetime, timedelta
import calendar
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.utils import platform

# Интегрираме функциите за логика
from service import generate_yearly_schedule

class NotificationApp(App):
    def build(self):
        if platform == 'android':
            try:
                from android.permissions import Permission, request_permissions
                request_permissions([Permission.POST_NOTIFICATIONS])
                self.start_android_clock_monitoring()
            except Exception as e:
                print(f"Грешка Android Инициализация: {e}")

        self.yearly_events = generate_yearly_schedule(datetime.now().year)
        main_layout = BoxLayout(orientation="vertical", padding=15, spacing=15)

        # 1. Заглавие
        title = Label(text="ГРАФИК ПРОВЕРКИ v6.0", font_size='22sp', bold=True, size_hint_y=0.08)
        main_layout.add_widget(title)

        # 2. КАРЕ: МИНАЛО СЪБИТИЕ
        self.past_box = BoxLayout(orientation="vertical", padding=15, spacing=10, size_hint_y=0.4)
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
        self.next_box = BoxLayout(orientation="vertical", padding=15, spacing=10, size_hint_y=0.4)
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

        # 4. Долно инфо поле
        self.status_label = Label(text="Автоматично фоново следене (AlarmManager) е активно.", font_size='13sp', size_hint_y=0.12, halign='center', color=(0.6, 0.8, 0.6, 1))
        main_layout.add_widget(self.status_label)

        # Автоматично зареждане на данните на екрана при отваряне
        self.update_events_display()
        return main_layout

    def _update_rect1(self, instance, value): self.rect1.pos = instance.pos; self.rect1.size = instance.size
    def _update_rect2(self, instance, value): self.rect2.pos = instance.pos; self.rect2.size = instance.size

    def start_android_clock_monitoring(self):
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            PendingIntent = autoclass('android.app.PendingIntent')
            AlarmManager = autoclass('android.app.AlarmManager')
            System = autoclass('java.lang.System')
            Context = autoclass('android.content.Context')

            activity = PythonActivity.mActivity
            context = activity.getApplicationContext()

            service_intent = Intent(context, autoclass('org.kivy.android.PythonService'))
            service_intent.putExtra('serviceEntrypoint', 'service.py')
            service_intent.putExtra('serviceName', 'MyNotificationService')

            pending_intent = PendingIntent.getService(context, 0, service_intent, 201326592)
            alarm_manager = activity.getSystemService(Context.ALARM_SERVICE)

            interval = 3600000 
            trigger_at = System.currentTimeMillis() + 5000 

            alarm_manager.setRepeating(AlarmManager.RTC_WAKEUP, trigger_at, interval, pending_intent)
        except Exception as e:
            print(f"Неуспешно инжектиране в AlarmManager: {e}")

    def update_events_display(self, *args):
        now = datetime.now()
        past_event = None
        next_event = None

        for event_date, title_text, facility_text, check_text, shift_text in self.yearly_events:
            if event_date.date() < now.date():
                past_event = (event_date, title_text, facility_text, check_text, shift_text)
            elif event_date.date() >= now.date() and next_event is None:
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

if __name__ == "__main__":
    NotificationApp().run()
