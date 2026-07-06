[app]
title = GrafikProverki
package.name = grafikapp
package.domain = org.twoman
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3==3.11.0, hostpython3==3.11.0, kivy==2.3.0

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25c
android.sdk = 33

# САМО ОСНОВНИ РАЗРЕШЕНИЯ - БЕЗ УСЛУГИ
android.permissions = 

[buildozer]
log_level = 2
