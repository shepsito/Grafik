import os
import time
import calendar
from datetime import datetime, timedelta
from jnius import autoclass
from kivy.utils import platform

def get_monday_week_number(dt):
    if dt.weekday() != 0: return None
    return 1 if dt.day <= 7 else 2 if dt.day <= 14 else 3 if dt.day <= 21 else 4

def get_wednesday_week_number(dt):
    if dt.weekday() != 2: return None
    return 1 if dt.day <= 7 else 2 if dt.day <= 14 else 3 if dt.day <= 21 else 4

def get_thursday_week_number(dt):
    if dt.weekday() != 3: return None
    return 1 if dt.day <= 7 else 2 if dt.day <= 14 else 3 if dt.day <= 21 else 4

def get_saturday_week_number(dt):
    if dt.weekday() != 5: return None
    return 1 if dt.day <= 7 else 2 if dt.day <= 14 else 3 if dt.day <= 21 else 4

def is_last_monday_of_quarter(dt):
    if dt.weekday() != 0: return False
    if dt.month not in [3, 6, 9, 12]: return False
    return (calendar.monthrange(dt.year, dt.month)[1] - dt.day) < 7

def is_last_tuesday_of_quarter(dt):
    if dt.weekday() != 1: return False
    if dt.month not in [3, 6, 9, 12]: return False
    return (calendar.monthrange(dt.year, dt.month)[1] - dt.day) < 7

def is_last_wednesday_of_quarter(dt):
    if dt.weekday() != 2: return False
    if dt.month not in [3, 6, 9, 12]: return False
    return (calendar.monthrange(dt.year, dt.month)[1] - dt.day) < 7

def is_last_thursday_of_quarter(dt):
    if dt.weekday() != 3: return False
    if dt.month not in [3, 6, 9, 12]: return False
    return (calendar.monthrange(dt.year, dt.month)[1] - dt.day) < 7

def is_last_friday_of_quarter(dt):
    if dt.weekday() != 4: return False
    if dt.month not in [3, 6, 9, 12]: return False
    return (calendar.monthrange(dt.year, dt.month)[1] - dt.day) < 7

def generate_yearly_schedule(year_val):
    events = []
    start_date = datetime(year_val, 1, 1)
    end_date = datetime(year_val, 12, 31)
    current = start_date
    while current <= end_date:
        c_day = current.weekday()
        c_month = current.month
        m_week = get_monday_week_number(current)
        wed_week = get_wednesday_week_number(current)
        thu_week = get_thursday_week_number(current)
        sat_week = get_saturday_week_number(current)
        shifts = 1 if current.day % 2 != 0 else 2
        
        if c_day == 1 and current.day <= 7:
            events.append((current, "🚨 Проверка АВР", "Аварийно осветление", "Проверка АВР на захранването-АСЕО ОЕОиСПКУ", shifts))
        if c_day == 2 and current.day <= 7:
            events.append((current, "🚨 ЕЕ ЦПС-2", "ЕЕ ЦПС-2", "Проверка изправността на аварийното осветление-АСЕО ОЕОиСПКУ", shifts))
        if c_month in [3, 6, 9, 12] and current.day <= 7:
            if c_day == 3:
                events.append((current, "🚨 Ф.И. Проверка", "По процедура", "Ф.И. на аварийното осветление-АСЕО ОЕОиСПКУ", shifts))
        if current.day == 1:
            events.append((current, "🚨 МЗ и ЕЕ ЦПС-1", "МЗ и ЕЕ ЦПС-1", "Проверка изправността на евакуационното осветление-АСЕО ОЕОиСПКУ", shifts))
        if m_week is not None:
            events.append((current, "🚨  Проверка АВР (Пон.)", "МЗ,ЦПС-1", "Проверка АВР сборки на 0,4кВ захранени от 3 и 4 БА-АСЕО ОЕОиСПКУ", shifts))
        if c_day == 1 and m_week is not None:
            events.append((current, "🚨 Проверка АВР (Вт.)", "МЗ", "Проверка АВР сборки на 0,4кВ захранени от 23 и 24 БА-АСЕО ОЕОиСПКУ", shifts))
        if wed_week is not None:
            events.append((current, "🚨  Проверка АВР (Ср.)", "МЗ", "Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 3-АСЕО ОЕОиСПКУ", shifts))
        if thu_week is not None:
            events.append((current, "🚨  Проверка АВР (Четв.)", "МЗ", "Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 4-АСЕО ОЕОиСПКУ", shifts))
        if sat_week is not None:
            events.append((current, "🚨  Проверка АВР (Петък)", "МЗ,ХВО и ЦПС-1", "Проверка АВР сборки на 0,4кВ с/без сборки захр.от 3,4,23,24БА,33БА I-III,43БА I-III /-АСЕО ОЕОиСПКУ", shifts))
        if current.day == 15:
            events.append((current, "🚨 Секции 0,4кВ-ГК", "Секции 0,4кВ-ГК 1_4 block", "Проверка АВР на -ШУ и изправността на сигнализацията на панел 'С'БЩУ за повикване в КРУ-ДИС ОЕОиСПКУ", shifts))
        if current.day == 20:
            events.append((current, "🚨 Вентилни отводи", "Вентилни отводи 1 и 3 ТП", "Отчитане на -вентилни отводи-АСЕО ОЕОиСПКУ", shifts))
        if current.day == 25:
            events.append((current, "🚨 Ел.двигатели 6кВ", "Ел.двигатели 6кВ", "Измерване съпротивлението на изолацията на ел.двиг.6кВ.-ПВТ в резерв,1и 2ППП-АСЕО ОЕОиСПКУ", shifts))
        if is_last_monday_of_quarter(current):
            events.append((current, "🚨 Проверка ДГ-А", "ДГ-А", "Ф.И. на автономен товар не по малко от 60мин.-АСЕО ОЕОиСПКУ", shifts))
        if is_last_tuesday_of_quarter(current):
            events.append((current, "🚨 Проверка ДГ-Б", "ДГ-Б", "Ф.И. на автономен товар не по малко от 60мин.-АСЕО ОЕОиСПКУ", shifts))
        if is_last_wednesday_of_quarter(current):
            events.append((current, "🚨 Проверка 2АДГ-ДСАПП-4", "2АДГ-ДСАПП-4", "Ф.И на аварийното ел.захранване на СПИ-АСЕО Енергетик ПРАО", shifts))
        if is_last_thursday_of_quarter(current):
            events.append((current, "🚨 Проверка ДГ-КАС", "ДГ-КАС", "Ф.И на автономен товар не по малко от 60мин.-АСЕО ОЕОиСПКУ", shifts))
        if is_last_friday_of_quarter(current):
            events.append((current, "🚨 Проверка ГРТ-ЦАРД", "ГРТ-ЦАРД", "Изпробване на АВР на ел.захранването-ДИС АСЕО Енергетик ПРАО", shifts))
        if current.day == 25:
            events.append((current, "🚨 Отчитане електромери", "По методика ДП.ЕД.МТ.1153", "Отчитане електомерите за консумирана ел.енергия-АСЕО ОЕОиСПКУ", shifts))
        if current.day == 10:
            events.append((current, "🚨 Проверка ТП1, ТП3", "ТП1,ТП3", "Изпропване на охлаждащите вентилатори на 1ТП и 3ТП чрез ръчно включване-АСЕО", shifts))
        if current.day == 5 or current.day == 20:
            events.append((current, "🚨 Измерване стойности по фидери", "Измерване стойностите по фидерите за АКС,СБК-2 и ТРЗ/Бюро пропуски-АСЕО ОЕОиСПКУ", shifts))
            
        current += timedelta(days=1)
    return events

def send_silent_background_alert(title, message):
    if platform != 'android':
        print(f"Фиктивно известие (Не-Android): {title} - {message}")
        return
    try:
        PythonService = autoclass('org.kivy.android.PythonService')
        Context = autoclass('android.content.Context')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        RingtoneManager = autoclass('android.media.RingtoneManager')
        AudioAttributes = autoclass('android.media.AudioAttributes')
        AudioAttributesBuilder = autoclass('android.media.AudioAttributes$Builder')

        service = PythonService.mService
        context = service.getApplicationContext()
        notification_manager = service.getSystemService(Context.NOTIFICATION_SERVICE)

        channel_id = "grafik_background_channel"
        channel_name = "Автоматични Известия"
        
        default_sound_uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)

        # ФИКС 1: Правилно конструиране на AudioAttributes (с .build() на края!)
        audio_attributes = AudioAttributesBuilder() \
            .setUsage(AudioAttributes.USAGE_NOTIFICATION) \
            .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION) \
            .build()

        # ФИКС 2: Ниво на важност IMPORTANCE_HIGH, за да изскочи банер със звук
        channel = NotificationChannel(channel_id, channel_name, NotificationManager.IMPORTANCE_HIGH)
        channel.enableLights(True)
        channel.enableVibration(True)
        channel.setSound(default_sound_uri, audio_attributes) # Задаваме звука на самия канал
        
        notification_manager.createNotificationChannel(channel)

        app_info = context.getApplicationInfo()
        icon_res = app_info.icon

        builder = NotificationBuilder(context, channel_id) \
            .setContentTitle(title) \
            .setContentText(message) \
            .setSmallIcon(icon_res) \
            .setAutoCancel(True) \
            .setPriority(NotificationManager.IMPORTANCE_HIGH) \
            .setSound(default_sound_uri)

        notification_manager.notify(int(time.time()) % 100000, builder.build())
    except Exception as e:
        print(f"Грешка в сервизното известяване: {str(e)}")

def check_and_notify(yearly_events):
    now_dt = datetime.now()
    today_str = now_dt.strftime("%d.%m.%Y")
    
    for event_date, title_text, facility_text, check_text, shift_text in yearly_events:
        if event_date.strftime("%d.%m.%Y") == today_str:
            # Проверяваме спрямо текущата смяна/час (Напр. Известие в 07:00 сутринта или 19:00)
            target_hour = 7 if shift_text == 1 else 19
            if now_dt.hour == target_hour:
                send_silent_background_alert(
                    f"🚨 СЪБИТИЕ СЕГА: {title_text}",
                    f"Обект: {facility_text} | {check_text}"
                )

if __name__ == '__main__':
    # ФИКС 3: Безкраен цикъл, за да работи услугата непрекъснато във фонов режим
    events_list = generate_yearly_schedule(datetime.now().year)
    while True:
        check_and_notify(events_list)
        time.sleep(3600)  # Проверява на всеки кръгъл час
