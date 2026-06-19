import time
from datetime import datetime
import calendar
from jnius import autoclass
from kivy.utils import platform

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
    from datetime import datetime, timedelta
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
            events.append((current, "🚨  Проверка АВР (Пон.)", "МЗ,ЦПС-1", "Проверка АВР сборки на 0,4кВ захранвани от 3 и 4 БН", shift))
        if is_last_tuesday_of_quarter(current):
            events.append((current, "🚨 Проверка АВР (Вт.)", "МЗ", "Проверка АВР сборки на 0,4кВ захранвани от 23 и 24 БН", shift))
        if is_last_wednesday_of_quarter(current):
            events.append((current, "🚨  Проверка АВР (Ср.)", "МЗ", "Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 3", shift))
        if is_last_thursday_of_quarter(current):
            events.append((current, "🚨  Проверка АВР (Четв.)", "МЗ", "Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 4", shift))
        if is_last_friday_of_quarter(current):
            events.append((current, "🚨  Проверка АВР (Петък)", "МЗ,ХВО и ЦПС-1", "Проверка АВР сборки на 0,4кВ с/без сборки захр.от 3,4,23,24БН,33БН I-III,43БН I-III /", shift))
        if current_day == 8:
            events.append((current, "🚨 Секции 0,4кВ-ГК", "Секции 0,4кВ-ГК 1_4 block", "Проверка АВР на -ШУ и изправността на сигнализацията на панел 'С'БЩУ за повикване в КРу", shift))
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
    return events

def send_silent_background_alert(title, message):
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        RingtoneManager = autoclass('android.media.RingtoneManager')
        AudioAttributesBuilder = autoclass('android.media.AudioAttributes$Builder')

        service = PythonService.mService
        context = service.getApplicationContext()
        notification_manager = service.getSystemService(Context.NOTIFICATION_SERVICE)

        channel_id = "grafik_background_channel"
        channel_name = "Автоматични Известия"
        default_sound_uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)

        channel = notification_manager.getNotificationChannel(channel_id)
        if channel is None:
            channel = NotificationChannel(channel_id, channel_name, NotificationManager.IMPORTANCE_HIGH)
            channel.enableLights(True)
            channel.enableVibration(True)
            
            audio_attributes = AudioAttributesBuilder() \
                .setUsage(AudioAttributesBuilder.USAGE_NOTIFICATION) \
                .setContentType(AudioAttributesBuilder.CONTENT_TYPE_SONIFICATION) \
                .build()
            channel.setSound(default_sound_uri, audio_attributes)
            notification_manager.createNotificationChannel(channel)

        builder = NotificationBuilder(context, channel_id)
        builder.setContentTitle(title)
        builder.setContentText(message)
        builder.setSmallIcon(context.getApplicationInfo().icon)
        builder.setAutoCancel(True)
        builder.setSound(default_sound_uri)
        builder.setPriority(NotificationManager.IMPORTANCE_HIGH)

        notification_manager.notify(int(time.time()) % 100000, builder.build())
    except Exception as e:
        print(f"Грешка в селфис известяването: {e}")

def check_and_notify():
    now = datetime.now()
    yearly_events = generate_yearly_schedule(now.year)
    
    for event_date, title, facility, check_text, shift in yearly_events:
        if event_date.date() == now.date():
            target_hour = 23 if shift == "Смяна 1" else 7 if shift == "Смяна 2" else 15 if shift == "Смяна 3" else None
            
            # Тъй като се сервизът се вика на всеки час, проверяваме дали съвпада точния час
            if target_hour is not None and now.hour == target_hour:
                send_silent_background_alert(
                    f"🚨 СЪБИТИЕ СЕГА: {title}",
                    f"Обект: {facility} | {check_text} ({shift})"
                )

if __name__ == '__main__':
    # Сервизът се изпълнява веднъж при събуждане от Android, проверява графика и приключва
    check_and_notify()
