from android import AndroidService
from datetime import datetime
import time
import threading

from service_logic import generate_yearly_schedule

def send_fullscreen_notification(title, message, description):
    """
    Изпраща ПЛАВАЩО ИЗВЕСТИЕ (Full Screen Intent)
    - Показва се на заключен екран
    - Със звук като аларма
    - Пробива през всичко
    """
    try:
        from jnius import autoclass
        
        Context = autoclass('android.content.Context')
        Intent = autoclass('android.content.Intent')
        PendingIntent = autoclass('android.app.PendingIntent')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        RingtoneManager = autoclass('android.media.RingtoneManager')
        AudioAttributesBuilder = autoclass('android.media.AudioAttributes$Builder')
        Notification = autoclass('android.app.Notification')
        
        # Вземаме контекст
        PythonService = autoclass('org.kivy.android.PythonService')
        service = PythonService.mService
        context = service.getApplicationContext()
        notification_manager = service.getSystemService(Context.NOTIFICATION_SERVICE)
        
        # --- 1. СЪЗДАВАМЕ КАНАЛ С ВИСОК ПРИОРИТЕТ ---
        channel_id = "grafik_alarm_channel"
        channel_name = "Аларми График"
        default_sound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)
        
        channel = notification_manager.getNotificationChannel(channel_id)
        if channel is None:
            # IMPORTANCE_MAX за най-висок приоритет
            channel = NotificationChannel(
                channel_id, 
                channel_name, 
                NotificationManager.IMPORTANCE_MAX  # Максимален приоритет
            )
            channel.enableLights(True)
            channel.enableVibration(True)
            channel.setLockscreenVisibility(Notification.VISIBILITY_PUBLIC)  # Вижда се на заключен екран
            
            # Настройка на звук за АЛАРМА
            audio_attributes = AudioAttributesBuilder() \
                .setUsage(AudioAttributesBuilder().USAGE_ALARM) \
                .setContentType(AudioAttributesBuilder().CONTENT_TYPE_SONIFICATION) \
                .build()
            channel.setSound(default_sound, audio_attributes)
            channel.setBypassDnd(True)  # Пробива през "Не безпокойте"
            notification_manager.createNotificationChannel(channel)
        
        # --- 2. СЪЗДАВАМЕ INTENT ЗА ОТВАРЯНЕ НА ПРИЛОЖЕНИЕТО ---
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        
        intent = Intent(context, PythonActivity)
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK)
        pending_intent = PendingIntent.getActivity(
            context, 
            0, 
            intent, 
            PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        )
        
        # --- 3. СЪЗДАВАМЕ FULL SCREEN INTENT (за заключен екран) ---
        full_screen_intent = Intent(context, PythonActivity)
        full_screen_intent.setFlags(
            Intent.FLAG_ACTIVITY_NEW_TASK | 
            Intent.FLAG_ACTIVITY_CLEAR_TASK |
            Intent.FLAG_ACTIVITY_SINGLE_TOP
        )
        full_screen_pending = PendingIntent.getActivity(
            context, 
            1, 
            full_screen_intent, 
            PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        )
        
        # --- 4. СЪЗДАВАМЕ НОТИФИКАЦИЯТА ---
        # Премахваме иконите
        clean_title = title.replace('🚨', '').strip()
        
        builder = NotificationBuilder(context, channel_id)
        builder.setContentTitle(clean_title)
        builder.setContentText(f"{message}\n{description}")
        builder.setSmallIcon(autoclass('android.R$drawable').ic_dialog_alert)
        builder.setLargeIcon(autoclass('android.R$drawable').ic_dialog_alert)  # Голяма икона
        
        # КРИТИЧНО: Настройки за FULL SCREEN
        builder.setPriority(Notification.PRIORITY_MAX)  # Максимален приоритет
        builder.setFullScreenIntent(full_screen_pending, True)  # ⚡ КЛЮЧОВО - плаващо известие
        builder.setAutoCancel(True)
        builder.setSound(default_sound)
        builder.setVibrate([0, 1000, 500, 1000, 500, 1000])  # Дълга вибрация
        builder.setCategory(Notification.CATEGORY_ALARM)  # Категория АЛАРМА
        builder.setContentIntent(pending_intent)
        
        # Индикатор за заключен екран
        builder.setVisibility(Notification.VISIBILITY_PUBLIC)
        
        # --- 5. ИЗПРАЩАМЕ ---
        notification_id = int(time.time() * 1000) % 100000
        notification_manager.notify(notification_id, builder.build())
        
        print(f"🔔 ПЛАВАЩО ИЗВЕСТИЕ: {clean_title}")
        return True
        
    except Exception as e:
        print(f"❌ ГРЕШКА ПРИ ИЗВЕСТИЕ: {e}")
        return False

def check_and_notify():
    """Проверява за събития и изпраща ПЛАВАЩИ ИЗВЕСТИЯ"""
    now = datetime.now()
    current_hour = now.hour
    current_date = now.date()
    
    print(f"🔍 [DEBUG] Проверка в {current_hour}:00")
    
    # Проверяваме само в 07:00, 15:00, 23:00
    if current_hour not in [7, 15, 23]:
        return False
    
    events = generate_yearly_schedule(now.year)
    
    # Намираме събитията за днес в този час
    today_events = []
    for event in events:
        if event['datetime'].date() == current_date and event['datetime'].hour == current_hour:
            today_events.append(event)
            print(f"  📌 Намерено: {event['title']}")
    
    if not today_events:
        print(f"📭 Няма събития в {current_hour}:00")
        return False
    
    # Изпращаме FULL SCREEN нотификации
    for event in today_events:
        title = event['title'].replace('🚨', '').strip()
        message = f"📍 {event['facility']} | {event['shift']}"
        description = event['description']
        
        send_fullscreen_notification(title, message, description)
        time.sleep(0.5)  # Малка пауза между нотификациите
    
    print(f"✅ Изпратени {len(today_events)} плаващи известия")
    return True

class MyNotificationService(AndroidService):
    def on_start(self):
        print("🚀 SERVICE START - Full Screen Notifications")
        self.running = True
        self.last_date = None
        self.last_check_hour = None
        
        self.thread = threading.Thread(target=self.background_loop)
        self.thread.daemon = True
        self.thread.start()
    
    def background_loop(self):
        print("🔄 Фонов режим - FULL SCREEN известия")
        
        while self.running:
            try:
                now = datetime.now()
                current_hour = now.hour
                current_minute = now.minute
                
                # Проверка в точните часове
                if current_minute < 2 and current_hour in [7, 15, 23]:
                    if self.last_check_hour != current_hour:
                        print(f"⏰ ЧАСОВА ПРОВЕРКА в {current_hour}:00")
                        check_and_notify()
                        self.last_check_hour = current_hour
                else:
                    if current_hour not in [7, 15, 23]:
                        self.last_check_hour = None
                
                # Смяна на деня
                if self.last_date != now.date():
                    print(f"📅 Нова дата: {now.strftime('%d.%m.%Y')}")
                    self.last_date = now.date()
                    self.last_check_hour = None
                
                time.sleep(30)
                
            except Exception as e:
                print(f"❌ ГРЕШКА: {e}")
                time.sleep(60)
    
    def on_destroy(self):
        print("🛑 SERVICE STOP")
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("✅ SERVICE STOPPED")

if __name__ == "__main__":
    check_and_notify()
