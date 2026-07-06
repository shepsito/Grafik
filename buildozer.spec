[app]
title = GrafikProverki
package.name = grafikapp
package.domain = org.twoman
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3==3.10.10, hostpython3==3.10.10, kivy==2.2.1

orientation = portrait
fullscreen = 1

android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25c
android.sdk = 33

android.permissions = 

[buildozer]
log_level = 2

