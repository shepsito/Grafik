from android import AndroidService
from datetime import datetime
import time
import threading

from service_logic import generate_yearly_schedule, get_shift_hours

def send_notification(title, message, notification_id=None):
    """Изпраща нотификация със звук и вибрация"""
    try:
        from jnius import autoclass
        
        Context = autoclass('android.content.Context')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        RingtoneManager = autoclass('android.media.RingtoneManager')
        AudioAttributesBuilder = autoclass('android.media.AudioAttributes$Builder')
        Notification = autoclass('android.app.Notification')
        
        PythonService = autoclass('org.kivy.android.PythonService')
        service = PythonService.mService
        context = service.getApplicationContext()
        notification_manager = service.getSystemService(Context.NOTIFICATION_SERVICE)
        
        # Канал за нотификации
        channel_id = "grafik_channel"
        channel_name = "Grafik Proverki"
        default_sound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
        
        channel = notification_manager.getNotificationChannel(channel_id)
        if channel is None:
            channel = NotificationChannel(
                channel_id, 
                channel_name, 
                NotificationManager.IMPORTANCE_HIGH
            )
            channel.enableLights(True)
            channel.enableVibration(True)
            channel.setLockscreenVisibility(Notification.VISIBILITY_PUBLIC)
            
            audio_attributes = AudioAttributesBuilder() \
                .setUsage(AudioAttributesBuilder().USAGE_NOTIFICATION) \
                .setContentType(AudioAttributesBuilder().CONTENT_TYPE_SONIFICATION) \
                .build()
            channel.setSound(default_sound, audio_attributes)
            notification_manager.createNotificationChannel(channel)
        
        # Премахваме иконите
        clean_title = title.replace('🚨', '').strip()
        clean_message = message.replace('📍', '').replace('📋', '').strip()
        
        builder = NotificationBuilder(context, channel_id)
        builder.setContentTitle(clean_title)
        builder.setContentText(clean_message)
        builder.setSmallIcon(autoclass('android.R$drawable').ic_dialog_alert)
        builder.setAutoCancel(True)
        builder.setSound(default_sound)
        builder.setPriority(Notification.PRIORITY_HIGH)
        builder.setVibrate([0, 500, 300, 500])
        
        if notification_id is None:
            notification_id = int(time.time() * 1000) % 100000
        
        notification_manager.notify(notification_id, builder.build())
        print(f"✅ Нотификация: {clean_title}")
        return True
    except Exception as e:
        print(f"❌ Грешка в нотификация: {e}")
        return False

def check_and_notify():
    """Проверява за събития само в 07:00, 15:00 и 23:00"""
    now = datetime.now()
    current_hour = now.hour
    
    # Проверяваме само в трите часа
    if current_hour not in [7, 15, 23]:
        print(f"⏰ Пропускам проверка в {current_hour}:00 - не е час за събитие")
        return False
    
    print(f"🔍 Проверка за събития в {current_hour}:00...")
    events = generate_yearly_schedule(now.year)
    
    # Намираме събитията за днес в този час
    today_events = []
    for event in events:
        if event['datetime'].date() == now.date() and event['datetime'].hour == current_hour:
            today_events.append(event)
    
    if not today_events:
        print(f"📭 Няма събития в {current_hour}:00")
        return False
    
    # Изпращаме нотификации за всяко събитие
    notifications_sent = 0
    for event in today_events:
        title = event['title'].replace('🚨', '').strip()
        message = f"{event['facility']} | {event['shift']}\n{event['description']}"
        
        event_id = int(f"{event['datetime'].timestamp()}"[-6:])
        send_notification(title, message, event_id)
        notifications_sent += 1
    
    print(f"✅ Изпратени {notifications_sent} нотификации за {current_hour}:00")
    return True

class MyNotificationService(AndroidService):
    def on_start(self):
        print("🚀 Service START - оптимизиран режим")
        self.running = True
        self.last_date = None
        self.last_check_hour = None
        
        self.thread = threading.Thread(target=self.background_loop)
        self.thread.daemon = True
        self.thread.start()
    
    def background_loop(self):
        """Проверява само в 07:00, 15:00 и 23:00"""
        print("🔄 Фонов режим - проверка само в 07:00, 15:00 и 23:00")
        
        while self.running:
            try:
                now = datetime.now()
                current_hour = now.hour
                current_minute = now.minute
                
                # Проверяваме само в точните часове (в първата минута)
                if current_minute < 2 and current_hour in [7, 15, 23]:
                    if self.last_check_hour != current_hour:
                        print(f"⏰ Часова проверка в {current_hour}:00")
                        check_and_notify()
                        self.last_check_hour = current_hour
                else:
                    # Нулираме часовника, за да може да проверява отново
                    if current_hour not in [7, 15, 23]:
                        self.last_check_hour = None
                
                # Проверка при смяна на деня
                if self.last_date != now.date():
                    print(f"📅 Нова дата: {now.strftime('%d.%m.%Y')}")
                    self.last_date = now.date()
                    self.last_check_hour = None  # Нулираме за новия ден
                
                # Спим 30 секунди, за да не натоварваме процесора
                time.sleep(30)
                
            except Exception as e:
                print(f"❌ Грешка в услугата: {e}")
                time.sleep(60)
    
    def on_destroy(self):
        print("🛑 Service STOP")
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("✅ Service STOPPED")

if __name__ == "__main__":
    print("Тест...")
    check_and_notify()
