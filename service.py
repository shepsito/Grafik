from jnius import autoclass
from time import sleep
from datetime import datetime
from service_logic import generate_yearly_schedule

# ---------------------------------------------------------
# SAFE GET SERVICE INSTANCE
# ---------------------------------------------------------
def get_service():
    PythonService = autoclass('org.kivy.android.PythonService')
    service = PythonService.mService
    return service


# ---------------------------------------------------------
# FOREGROUND NOTIFICATION (SAFE)
# ---------------------------------------------------------
def start_foreground():
    service = get_service()
    if service is None:
        print("⚠ Service not ready yet")
        return

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
    print("🔥 Foreground service started")


# ---------------------------------------------------------
# SEND EVENT NOTIFICATION (SAFE)
# ---------------------------------------------------------
def send_notification(title, message):
    service = get_service()
    if service is None:
        print("⚠ Service not ready yet")
        return

    Context = autoclass('android.content.Context')
    NotificationManager = autoclass('android.app.NotificationManager')
    NotificationChannel = autoclass('android.app.NotificationChannel')
    NotificationBuilder = autoclass('android.app.Notification$Builder')

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
    print("🔔 Notification sent:", title)


# ---------------------------------------------------------
# WAIT UNTIL SERVICE IS READY
# ---------------------------------------------------------
print("⏳ Waiting for Android service to be ready...")
for _ in range(20):  # максимум ~10 секунди
    if get_service() is not None:
        break
    sleep(0.5)

if get_service() is None:
    print("❌ Service failed to initialize")
else:
    print("✅ Service ready")
    start_foreground()


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
last_check_hour = None

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
        print("❌ Error:", e)
        sleep(60)
