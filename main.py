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

# Импорт на функцията за генериране на график
from service_logic import generate_yearly_schedule

class NotificationApp(App):
    def build(self):
        if platform == 'android':
            try:
                from android.permissions import Permission, request_permissions
                request_permissions([
                    Permission.POST_NOTIFICATIONS,
                    Permission.VIBRATE,
                    Permission.WAKE_LOCK
                ])
                # Създаваме канал за нотификации
                self.create_notification_channel()
                # Стартираме AlarmManager
                self.start_android_clock_monitoring()
            except Exception as e:
                print(f"Грешка Android Инициализация: {e}")

        self.yearly_events = generate_yearly_schedule(datetime.now().year)
        main_layout = BoxLayout(orientation="vertical", padding=15, spacing=15)

        # ... (останалата част от UI кода остава същата) ...

        # Автоматично зареждане на данните на екрана при отваряне
        self.update_events_display()
        return main_layout

    def create_notification_channel(self):
        """Създава канал за нотификации за Android 8+"""
        try:
            from jnius import autoclass
            Context = autoclass('android.content.Context')
            NotificationManager = autoclass('android.app.NotificationManager')
            NotificationChannel = autoclass('android.app.NotificationChannel')
            NotificationImportance = autoclass('android.app.NotificationManager').IMPORTANCE_HIGH
            
            context = autoclass('org.kivy.android.PythonActivity').mActivity
            notification_manager = context.getSystemService(Context.NOTIFICATION_SERVICE)
            
            channel_id = "grafik_channel"
            channel_name = "Grafik Proverki"
            channel = NotificationChannel(channel_id, channel_name, NotificationImportance)
            channel.enableVibration(True)
            
            notification_manager.createNotificationChannel(channel)
            print("✅ Канал за нотификации създаден")
        except Exception as e:
            print(f"❌ Грешка при създаване на канал: {e}")

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

            # Правилният път към услугата
            ServiceClass = autoclass('org.kivy.android.PythonService')
            
            service_intent = Intent(context, ServiceClass)
            service_intent.putExtra('serviceEntrypoint', 'service.py')
            service_intent.putExtra('serviceName', 'MyNotificationService')

            flags = PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
            pending_intent = PendingIntent.getService(context, 0, service_intent, flags)
            alarm_manager = activity.getSystemService(Context.ALARM_SERVICE)

            interval = 60000  # 1 минута за тестване (вместо 1 час)
            trigger_at = System.currentTimeMillis() + 5000  # след 5 секунди

            alarm_manager.setRepeating(AlarmManager.RTC_WAKEUP, trigger_at, interval, pending_intent)
            print("✅ AlarmManager стартиран успешно")
            
        except Exception as e:
            print(f"❌ Неуспешно инжектиране в AlarmManager: {e}")

    def send_notification(self, title, message):
        """Изпраща нотификация"""
        if platform != 'android':
            print(f"📱 Нотификация (десктоп): {title} - {message}")
            return
            
        try:
            from jnius import autoclass
            
            Context = autoclass('android.content.Context')
            Intent = autoclass('android.content.Intent')
            PendingIntent = autoclass('android.app.PendingIntent')
            NotificationManager = autoclass('android.app.NotificationManager')
            NotificationBuilder = autoclass('android.app.Notification$Builder')
            
            context = autoclass('org.kivy.android.PythonActivity').mActivity
            
            # Intent за отваряне на приложението
            intent = Intent(context, autoclass('org.kivy.android.PythonActivity').getClass())
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK)
            pending_intent = PendingIntent.getActivity(context, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT)
            
            # Създаване на нотификацията
            channel_id = "grafik_channel"
            builder = NotificationBuilder(context, channel_id)
            builder.setContentTitle(title)
            builder.setContentText(message)
            builder.setSmallIcon(context.getApplicationInfo().icon)
            builder.setAutoCancel(True)
            builder.setContentIntent(pending_intent)
            builder.setVibrate([0, 500, 200, 500])  # Вибрация
            
            # Изпращане
            notification_manager = context.getSystemService(Context.NOTIFICATION_SERVICE)
            notification_manager.notify(1, builder.build())
            print(f"✅ Нотификация изпратена: {title}")
        except Exception as e:
            print(f"❌ Грешка при нотификация: {e}")

    def check_events_for_notification(self):
        """Проверява за предстоящи събития и изпраща нотификация"""
        now = datetime.now()
        today = now.date()
        current_hour = now.hour
        
        # Проверка за събития днес
        today_events = [ev for ev in self.yearly_events if ev[0].date() == today]
        
        if today_events:
            # Проверяваме дали има събитие в следващите 2 часа
            for event in today_events:
                event_time = event[0].time()
                event_hour = event_time.hour
                event_minute = event_time.minute
                
                # Изчисляваме време до събитието
                time_diff = (event_time.hour - current_hour) * 60 + (event_time.minute - now.minute)
                
                # Ако събитието е след 0-60 минути, изпращаме нотификация
                if 0 <= time_diff <= 60:
                    title = f"🔔 {event[1]}"
                    message = f"Днес {event_time.strftime('%H:%M')} - {event[2]}"
                    self.send_notification(title, message)
                    break

    def on_start(self):
        """Стартира периодична проверка за събития"""
        Clock.schedule_interval(self.check_events_for_notification, 60)  # Всяка минута

    # ... (останалите методи _update_rect1, _update_rect2, update_events_display остават същите) ...

if __name__ == "__main__":
    NotificationApp().run()
