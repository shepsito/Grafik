[app]
title = GrafikProverki
package.name = grafikapp
package.domain = org.twoman
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3==3.11.0, hostpython3==3.11.0, kivy==2.3.0, pyjnius, plyer

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25c
android.sdk = 33

android.permissions = POST_NOTIFICATIONS, VIBRATE, WAKE_LOCK, RECEIVE_BOOT_COMPLETED, FOREGROUND_SERVICE, SYSTEM_ALERT_WINDOW, USE_FULL_SCREEN_INTENT
services = MyNotificationService:service.py
android.gradle_dependencies = androidx.core:core:1.9.0, androidx.appcompat:appcompat:1.6.1
android.add_src = True
android.enable_androidx = True
android.foreground_service = True
android.foreground_service_type = dataSync

[buildozer]
log_level = 2
