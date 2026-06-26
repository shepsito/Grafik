from android import AndroidService
from datetime import datetime
import time
import threading
import os

from service_logic import generate_yearly_schedule

# --- ФУНКЦИЯ ЗА ЗАПИС ВЪВ ФАЙЛ (ВЪВ ВЪТРЕШНА ПАМЕТ) ---
def log_to_file(message):
    """Записва съобщение във файл на телефона - ДОСТЪПЕН ОТ ВСЯКЪДЕ"""
    try:
        # Записваме в главната директория на телефона (вътрешна памет)
        log_path = '/sdcard/grafik_log.txt'
        
        # Алтернатива: /storage/emulated/0/grafik_log.txt
        # log_path = '/storage/emulated/0/grafik_log.txt'
        
        # Създаваме директорията ако не съществува
        log_dir = os.path.dirname(log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        with open(log_path, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")
            f.flush()  # Принудително записваме веднага
            
        print(f"📝 LOG: {message}")
        
    except Exception as e:
        # Ако не може да запише на /sdcard, опитваме в папката на приложението
        try:
            fallback_path = '/data/data/org.twoman.grafikapp/files/log.txt'
            with open(fallback_path, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}] {message}\n")
                f.flush()
        except:
            print(f"❌ Грешка при запис на лог: {e}")

# --- НОТИФИКАЦИЯ ---
def send_notification(title, message, notification_id=None):
    """Изпраща нотификация"""
    log_to_file(f"🔔 Опит за нотификация: {title}")
    
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
            log_to_file("✅ Каналът е създаден")
        
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
        
        log_to_file(f"✅ НОТИФИКАЦИЯ ИЗПРАТЕНА: {clean_title}")
        return True
        
    except Exception as e:
        error_msg = f"❌ ГРЕШКА: {str(e)}"
        log_to_file(error_msg)
        print(error_msg)
        import traceback
        traceback.print_exc()
        return False

# --- ПРОВЕРКА ЗА СЪБИТИЯ ---
def check_and_notify():
    """Проверява за събития"""
    log_to_file("="*50)
    log_to_file("🚀 НАЧАЛО НА ПРОВЕРКА")
    
    try:
        now = datetime.now()
        current_hour = now.hour
        current_date = now.date()
        
        log_to_file(f"📱 Текущ час: {current_hour}:00")
        log_to_file(f"📅 Текуща дата: {current_date}")
        
        # Проверяваме само в трите часа
        if current_hour not in [7, 15, 23]:
            log_to_file(f"⏰ Пропускам - {current_hour}:00 не е час за събитие")
            return False
        
        log_to_file(f"🔍 Търся събития за {current_hour}:00...")
        events = generate_yearly_schedule(now.year)
        
        # Намираме събитията за днес в този час
        today_events = []
        for event in events:
            if event['datetime'].date() == current_date and event['datetime'].hour == current_hour:
                today_events.append(event)
                log_to_file(f"📌 Намерено: {event['title']} - {event['facility']}")
        
        if not today_events:
            log_to_file(f"📭 Няма събития в {current_hour}:00")
            return False
        
        # Изпращаме нотификации
        count = 0
        for event in today_events:
            title = event['title'].replace('🚨', '').strip()
            message = f"{event['facility']} | {event['shift']}"
            
            log_to_file(f"📤 Изпращам: {title}")
            send_notification(title, message, event['description'])
            count += 1
            time.sleep(0.5)
        
        log_to_file(f"✅ ИЗПРАТЕНИ {count} НОТИФИКАЦИИ")
        log_to_file("="*50)
        return True
        
    except Exception as e:
        log_to_file(f"❌ ГРЕШКА В check_and_notify: {e}")
        import traceback
        log_to_file(traceback.format_exc())
        return False

# --- УСЛУГА ---
class MyNotificationService(AndroidService):
    def on_start(self):
        log_to_file("="*50)
        log_to_file("🚀 SERVICE START")
        log_to_file("="*50)
        self.running = True
        self.last_date = None
        self.last_check_hour = None
        
        self.thread = threading.Thread(target=self.background_loop)
        self.thread.daemon = True
        self.thread.start()
    
    def background_loop(self):
        log_to_file("🔄 Фонов режим стартира")
        log_to_file("⏰ Ще проверява в 07:00, 15:00 и 23:00")
        
        while self.running:
            try:
                now = datetime.now()
                current_hour = now.hour
                current_minute = now.minute
                
                # Проверка в точните часове
                if current_minute < 2 and current_hour in [7, 15, 23]:
                    if self.last_check_hour != current_hour:
                        log_to_file(f"⏰ ЧАСОВА ПРОВЕРКА в {current_hour}:00")
                        check_and_notify()
                        self.last_check_hour = current_hour
                else:
                    if current_hour not in [7, 15, 23]:
                        self.last_check_hour = None
                
                # Смяна на деня
                if self.last_date != now.date():
                    log_to_file(f"📅 Нова дата: {now.strftime('%d.%m.%Y')}")
                    self.last_date = now.date()
                    self.last_check_hour = None
                
                time.sleep(30)
                
            except Exception as e:
                log_to_file(f"❌ ГРЕШКА В ЦИКЪЛА: {e}")
                time.sleep(60)
    
    def on_destroy(self):
        log_to_file("🛑 SERVICE STOP")
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        log_to_file("✅ SERVICE STOPPED")
        log_to_file("="*50)

if __name__ == "__main__":
    log_to_file("=== ТЕСТОВО СТАРТИРАНЕ ===")
    check_and_notify()
