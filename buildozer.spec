[app]
title = GrafikProverki
package.name = grafikapp
package.domain = org.twoman
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3, kivy, pyjnius, plyer, pillow
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33
android.permissions = POST_NOTIFICATIONS, VIBRATE, WAKE_LOCK, FOREGROUND_SERVICE
services = mynotificationservice:service.py
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1

[buildozer]
log_level = 2
warn_on_root = 1