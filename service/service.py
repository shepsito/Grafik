from jnius import autoclass
from time import sleep
from datetime import datetime
from service_logic import generate_yearly_schedule

# ---------------------------------------------------------
# FOREGROUND NOTIFICATION
# ---------------------------------------------------------
def start_foreground():
    PythonService = autoclass('org.kivy.android.PythonService')
    service = PythonService.mService
    context = service.getApplicationContext()

    NotificationBuilder = autoclass('android.app.Notification$Builder')
    NotificationChannel = autoclass('android.app.NotificationChannel')
    NotificationManager = autoclass('android.app.NotificationManager')

    nm = context.getSystemService("notification")

    channel_id = "foreground_channel"
    channel = nm.getNotificationChannel(channel_id)

    if channel is None:
        channel = NotificationChannel(
            channel_id,
            "Foreground",
            NotificationManager.IMPORTANCE_LOW
        )
        nm.createNotificationChannel(channel)

    builder = NotificationBuilder(context, channel_id)
    builder.setContentTitle("Service running")
    builder.setContentText("Grafik service active")
    builder.setSmallIcon(autoclass('android.R$drawable').ic_dialog_info)

    notification = builder.build()
    service.startForeground(1, notification)


# ---------------------------------------------------------
# SEND EVENT NOTIFICATION
# ---------------------------------------------------------
def send_notification(title, message):
    Context = autoclass('android.content.Context')
    NotificationManager = autoclass('android.app.NotificationManager')
    NotificationChannel = autoclass('android.app.NotificationChannel')
    NotificationBuilder = autoclass('android.app.Notification$Builder')

    PythonService = autoclass('org.kivy.android.PythonService')
    service = PythonService.mService
    context = service.getApplicationContext()
    nm = context.getSystemService(Context.NOTIFICATION_SERVICE)

    channel_id = "grafik_channel"
    channel = nm.getNotificationChannel(channel_id)

    if channel is None:
        channel = NotificationChannel(
            channel_id,
            "Grafik Proverki",
            NotificationManager.IMPORTANCE_HIGH
        )
        nm.createNotificationChannel(channel)

    builder = NotificationBuilder(context, channel_id)
    builder.setContentTitle(title)
    builder.setContentText(message)
    builder.setSmallIcon(autoclass('android.R$drawable').ic_dialog_info)
    builder.setAutoCancel(True)

    nm.notify(int(datetime.now().timestamp()), builder.build())


# ---------------------------------------------------------
# SERVICE START
# ---------------------------------------------------------
start_foreground()
last_check_hour = None

# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
while True:
    try:
        now = datetime.now()
        hour = now.hour
        minute = now.minute

        # Проверка само в 07:00, 15:00, 23:00
        if hour in [7, 15, 23] and minute < 2:
            if last_check_hour != hour:
                events = generate_yearly_schedule(now.year)

                for ev in events:
                    ev_time = ev["datetime"]

                    if ev_time.year == now.year and \
                       ev_time.month == now.month and \
                       ev_time.day == now.day and \
                       ev_time.hour == hour:

                        send_notification(ev["title"], ev["description"])

                last_check_hour = hour

        if hour not in [7, 15, 23]:
            last_check_hour = None

        sleep(30)

    except Exception as e:
        print("Error:", e)
        sleep(60)
