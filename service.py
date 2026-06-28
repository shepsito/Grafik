import sys
import os
from time import sleep
from datetime import datetime
from jnius import autoclass

# ---------------------------------------------------------
# FIX: Ensure service_logic.py can be imported inside APK
# ---------------------------------------------------------
service_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(service_dir)

try:
    from service_logic import generate_yearly_schedule
except Exception as e:
    print("❌ Cannot import service_logic:", e)
    generate_yearly_schedule = None


# ---------------------------------------------------------
# SAFE SERVICE ACCESS
# ---------------------------------------------------------
def get_service():
    PythonService = autoclass('org.kivy.android.PythonService')
    return PythonService.mService


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
