from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.metrics import dp, sp

from service_logic import generate_yearly_schedule

# Настройки за Android
Window.clearcolor = (0.05, 0.05, 0.08, 1)

class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(15), dp(10), dp(15), dp(10)]
        self.spacing = dp(8)
        
        # --- ЗАГЛАВИЕ ---
        self.add_widget(Label(
            text="[b]ГРАФИК ПРОВЕРКИ[/b]",
            font_size=sp(36),
            bold=True,
            color=(0.3, 0.9, 0.3, 1),
            size_hint_y=0.06,
            halign='center',
            markup=True
        ))
        
        self.add_widget(Widget(size_hint_y=0.01))
        
        # --- ПОСЛЕДНО МИНАЛО ---
        self.past_box = BoxLayout(
            orientation='vertical',
            padding=[dp(15), dp(10), dp(15), dp(10)],
            spacing=dp(3),
            size_hint_y=0.24
        )
        with self.past_box.canvas.before:
            Color(0.15, 0.12, 0.18, 1)
            self.past_rect = Rectangle()
        self.past_box.bind(size=self._update_rect, pos=self._update_rect)
        
        self.past_label = Label(
            text="[b]<< МИНАЛО СЪБИТИЕ[/b]",
            bold=True,
            color=(0.8, 0.7, 0.7, 1),
            font_size=sp(16),
            size_hint_y=0.18,
            halign='left',
            markup=True
        )
        self.past_box.add_widget(self.past_label)
        
        self.past_content = Label(
            text="Няма минали събития",
            color=(0.9, 0.8, 0.8, 1),
            font_size=sp(18),
            size_hint_y=0.82,
            halign='left',
            text_size=(Window.width - dp(60), None),
            markup=True
        )
        self.past_box.add_widget(self.past_content)
        self.add_widget(self.past_box)
        
        self.add_widget(Widget(size_hint_y=0.01))
        
        # --- СЛЕДВАЩО ---
        self.next_box = BoxLayout(
            orientation='vertical',
            padding=[dp(15), dp(10), dp(15), dp(10)],
            spacing=dp(3),
            size_hint_y=0.24
        )
        with self.next_box.canvas.before:
            Color(0.08, 0.18, 0.12, 1)
            self.next_rect = Rectangle()
        self.next_box.bind(size=self._update_rect2, pos=self._update_rect2)
        
        self.next_label = Label(
            text="[b]>> СЛЕДВАЩО СЪБИТИЕ[/b]",
            bold=True,
            color=(0.7, 0.8, 0.7, 1),
            font_size=sp(16),
            size_hint_y=0.18,
            halign='left',
            markup=True
        )
        self.next_box.add_widget(self.next_label)
        
        self.next_content = Label(
            text="Няма предстоящи събития",
            color=(0.4, 0.9, 0.4, 1),
            font_size=sp(18),
            size_hint_y=0.82,
            halign='left',
            text_size=(Window.width - dp(60), None),
            markup=True
        )
        self.next_box.add_widget(self.next_content)
        self.add_widget(self.next_box)
        
        self.add_widget(Widget(size_hint_y=0.01))
        
        # --- ДНЕС ---
        self.today_label = Label(
            text="[b]ДНЕС[/b]",
            bold=True,
            color=(0.9, 0.8, 0.2, 1),
            font_size=sp(17),
            size_hint_y=0.04,
            halign='center',
            markup=True
        )
        self.add_widget(self.today_label)
        
        self.today_scroll = ScrollView(size_hint=(1, 0.26))
        self.today_box = BoxLayout(
            orientation='vertical',
            spacing=dp(6),
            size_hint_y=None,
            padding=[dp(5), dp(5), dp(5), dp(5)]
        )
        self.today_box.bind(minimum_height=self.today_box.setter('height'))
        self.today_scroll.add_widget(self.today_box)
        self.add_widget(self.today_scroll)
        
        self.add_widget(Widget(size_hint_y=0.01))
        
        # --- ДОЛЕН ПАНЕЛ ---
        bottom_box = BoxLayout(
            orientation='vertical',
            size_hint_y=0.10,
            spacing=dp(3)
        )
        
        self.status_label = Label(
            text="[color=33cc33]АКТИВНО[/color]",
            color=(0.3, 0.8, 0.3, 1),
            font_size=sp(14),
            markup=True
        )
        bottom_box.add_widget(self.status_label)
        
        btn_box = BoxLayout(size_hint_y=0.55, spacing=dp(10))
        
        check_btn = Button(
            text="🔔 ТЕСТ",
            background_color=(0.8, 0.2, 0.2, 1),
            font_size=sp(16),
            bold=True
        )
        check_btn.bind(on_press=self.test_fullscreen_notification)
        btn_box.add_widget(check_btn)
        
        refresh_btn = Button(
            text="ОБНОВИ",
            background_color=(0.25, 0.25, 0.35, 1),
            font_size=sp(16),
            bold=True
        )
        refresh_btn.bind(on_press=self.refresh_data)
        btn_box.add_widget(refresh_btn)
        
        btn_box.add_widget(Widget())  # Разширител
        
        bottom_box.add_widget(btn_box)
        self.add_widget(bottom_box)
        
        # --- ИНИЦИАЛИЗАЦИЯ ---
        self.yearly_events = []
        self.load_events()
        Clock.schedule_interval(self.update_display, 3600)
        
        if platform == 'android':
            self.setup_android()
    
    def _update_rect(self, instance, value):
        self.past_rect.pos = instance.pos
        self.past_rect.size = instance.size
    
    def _update_rect2(self, instance, value):
        self.next_rect.pos = instance.pos
        self.next_rect.size = instance.size
    
    def setup_android(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.POST_NOTIFICATIONS,
                Permission.VIBRATE,
                Permission.WAKE_LOCK,
                Permission.SYSTEM_ALERT_WINDOW  # За плаващи прозорци
            ])
            print("✅ Разрешенията са дадени")
        except Exception as e:
            print(f"❌ Грешка: {e}")
    
    def load_events(self):
        try:
            self.yearly_events = generate_yearly_schedule(datetime.now().year)
            self.update_display()
            self.status_label.text = f"[color=33cc33]ЗАРЕДЕНИ {len(self.yearly_events)}[/color]"
        except Exception as e:
            self.status_label.text = f"[color=ff3333]ГРЕШКА: {e}[/color]"
    
    def refresh_data(self, *args):
        self.load_events()
    
    def update_display(self, *args):
        now = datetime.now()
        today = now.date()
        
        # --- МИНАЛО ---
        past_events = [e for e in self.yearly_events if e['datetime'] < now]
        if past_events:
            last = past_events[-1]
            dt = last['datetime'].strftime('%d.%m.%Y %H:%M')
            title = last['title'].replace('🚨', '').strip()
            self.past_content.text = (
                f"[b]{dt}[/b]\n{title}\n"
                f"Локация: {last['facility']}  |  {last['shift']}\n"
                f"[color=888888]{last['description']}[/color]"
            )
        else:
            self.past_content.text = "[i]Няма минали събития[/i]"
        
        # --- СЛЕДВАЩО ---
        future_events = [e for e in self.yearly_events if e['datetime'] > now]
        if future_events:
            next_ev = future_events[0]
            dt = next_ev['datetime'].strftime('%d.%m.%Y %H:%M')
            time_left = next_ev['datetime'] - now
            hours = int(time_left.total_seconds() / 3600)
            minutes = int((time_left.total_seconds() % 3600) / 60)
            title = next_ev['title'].replace('🚨', '').strip()
            self.next_content.text = (
                f"[b]{dt}[/b]\n{title}\n"
                f"Локация: {next_ev['facility']}  |  {next_ev['shift']}\n"
                f"[color=888888]{next_ev['description']}[/color]\n"
                f"[color=33cc33]СЛЕД {hours}h {minutes}m[/color]"
            )
        else:
            self.next_content.text = "[i]Няма предстоящи събития[/i]"
        
        # --- ДНЕС ---
        self.today_box.clear_widgets()
        today_events = [e for e in self.yearly_events if e['datetime'].date() == today]
        
        if today_events:
            events_by_time = {}
            for e in today_events:
                time_key = e['datetime'].strftime('%H:%M')
                if time_key not in events_by_time:
                    events_by_time[time_key] = []
                events_by_time[time_key].append(e)
            
            for time_key, event_list in sorted(events_by_time.items()):
                hour_label = Label(
                    text=f"[b]{time_key}  ({len(event_list)} бр.)[/b]",
                    bold=True,
                    color=(0.5, 0.8, 1, 1),
                    font_size=sp(17),
                    size_hint_y=None,
                    height=dp(32),
                    halign='left',
                    markup=True
                )
                self.today_box.add_widget(hour_label)
                
                for ev in event_list:
                    status = "[OK]" if ev['datetime'] < now else "[  ]"
                    title = ev['title'].replace('🚨', '').strip()
                    ev_text = (
                        f"{status}  {title}\n"
                        f"     {ev['facility']}  |  {ev['shift']}"
                    )
                    ev_label = Label(
                        text=ev_text,
                        color=(0.9, 0.9, 0.9, 1),
                        font_size=sp(15),
                        size_hint_y=None,
                        height=dp(36),
                        halign='left',
                        text_size=(Window.width - dp(60), None),
                        markup=True
                    )
                    self.today_box.add_widget(ev_label)
                
                self.today_box.add_widget(Widget(size_hint_y=None, height=dp(4)))
        else:
            self.today_box.add_widget(Label(
                text="[i]Няма събития за днес[/i]",
                color=(0.5, 0.5, 0.5, 1),
                font_size=sp(16),
                size_hint_y=None,
                height=dp(35),
                halign='center',
                markup=True
            ))
    
    def test_fullscreen_notification(self, *args):
        """Тества плаващо известие"""
        try:
            from service import send_fullscreen_notification
            print("🔔 Изпращам ТЕСТОВО ПЛАВАЩО ИЗВЕСТИЕ...")
            
            result = send_fullscreen_notification(
                "🧪 ТЕСТОВА АЛАРМА",
                "Това е плаващо известие",
                "Ако виждате това - всичко работи!"
            )
            
            if result:
                self.status_label.text = "[color=33cc33]✅ ТЕСТОВОТО ИЗВЕСТИЕ Е ИЗПРАТЕНО![/color]"
                print("✅ Тестовото известие е изпратено!")
            else:
                self.status_label.text = "[color=ff3333]❌ ГРЕШКА ПРИ ТЕСТА[/color]"
                print("❌ Грешка при изпращане")
                
        except Exception as e:
            self.status_label.text = f"[color=ff3333]❌ ГРЕШКА: {str(e)[:30]}[/color]"
            print(f"❌ Грешка: {e}")

class NotificationApp(App):
    def build(self):
        return MainWidget()
    
    def on_start(self):
        print("🚀 Приложението стартира")
    
    def on_stop(self):
        print("🛑 Приложението спира")

if __name__ == "__main__":
    NotificationApp().run()
