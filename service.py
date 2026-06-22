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
        channel_name = "График Проверки"
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
        
        # Създаваме нотификация
        builder = NotificationBuilder(context, channel_id)
        builder.setContentTitle(title)
        builder.setContentText(message)
        builder.setSmallIcon(autoclass('android.R$drawable').ic_dialog_alert)
        builder.setAutoCancel(True)
        builder.setSound(default_sound)
        builder.setPriority(Notification.PRIORITY_HIGH)
        builder.setVibrate([0, 500, 300, 500])
        
        # Уникален ID за всяка нотификация
        if notification_id is None:
            notification_id = int(time.time() * 1000) % 100000
        
        notification_manager.notify(notification_id, builder.build())
        print(f"✅ Нотификация: {title}")
        return True
    except Exception as e:
        print(f"❌ Грешка в нотификация: {e}")
        return False

def check_and_notify():
    """Проверява за събития и изпраща нотификации за ВСИЧКИ"""
    now = datetime.now()
    events = generate_yearly_schedule(now.year)
    
    # Намираме всички събития за днес
    today_events = [e for e in events if e[0].date() == now.date()]
    
    if not today_events:
        return False
    
    # Групираме по час
    events_by_hour = {}
    for event in today_events:
        hour = event[0].hour
        if hour not in events_by_hour:
            events_by_hour[hour] = []
        events_by_hour[hour].append(event)
    
    # Проверяваме текущия час
    current_hour = now.hour
    if current_hour in events_by_hour:
        notifications_sent = 0
        for event in events_by_hour[current_hour]:
            title = f"🔔 {event[1]}"
            message = f"📍 {event[2]}\n📋 {event[3]}\n⏰ {event[4]}"
            
            # Уникален ID за всяко събитие
            event_id = int(f"{event[0].timestamp()}"[-6:])
            send_notification(title, message, event_id)
            notifications_sent += 1
        
        print(f"✅ Изпратени {notifications_sent} нотификации за час {current_hour}:00")
        return True
    
    return False

class MyNotificationService(AndroidService):
    def on_start(self):
        print("🚀 MyNotificationService стартира!")
        self.running = True
        self.last_date = None
        self.last_hour = None
        
        self.thread = threading.Thread(target=self.background_loop)
        self.thread.daemon = True
        self.thread.start()
    
    def background_loop(self):
        print("🔄 Започва фонова проверка...")
        
        while self.running:
            try:
                now = datetime.now()
                current_hour = now.hour
                
                # Проверка всеки час
                if self.last_hour != current_hour:
                    print(f"⏰ Часова проверка в {now.strftime('%H:%M')}")
                    check_and_notify()
                    self.last_hour = current_hour
                
                # Проверка при смяна на деня
                if self.last_date != now.date():
                    print(f"📅 Нова дата: {now.strftime('%d.%m.%Y')}")
                    self.last_date = now.date()
                
                time.sleep(30)
                
            except Exception as e:
                print(f"❌ Грешка в услугата: {e}")
                time.sleep(60)
    
    def on_destroy(self):
        print("🛑 MyNotificationService спира...")
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("✅ MyNotificationService спря")

if __name__ == "__main__":
    print("Тест на услугата...")
    check_and_notify()
