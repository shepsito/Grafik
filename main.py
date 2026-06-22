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

from service_logic import generate_yearly_schedule, get_shift_hours

# Настройки на прозореца
Window.clearcolor = (0.08, 0.08, 0.12, 1)

class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10
        
        # Заглавие
        self.add_widget(Label(
            text="📋 ГРАФИК ПРОВЕРКИ",
            font_size='26sp',
            bold=True,
            color=(0.3, 0.9, 0.3, 1),
            size_hint_y=0.08
        ))
        
        # --- ПОСЛЕДНО МИНАЛО СЪБИТИЕ ---
        self.past_box = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=5,
            size_hint_y=None,
            height=100
        )
        with self.past_box.canvas.before:
            Color(0.15, 0.15, 0.2, 1)
            self.past_rect = Rectangle()
        self.past_box.bind(size=self._update_rect, pos=self._update_rect)
        
        self.past_label = Label(
            text="🕐 ПОСЛЕДНО МИНАЛО СЪБИТИЕ",
            bold=True,
            color=(0.7, 0.7, 0.7, 1),
            font_size='13sp',
            size_hint_y=0.3,
            halign='left'
        )
        self.past_box.add_widget(self.past_label)
        
        self.past_content = Label(
            text="Няма минали събития",
            color=(0.9, 0.9, 0.9, 1),
            font_size='15sp',
            size_hint_y=0.7,
            halign='left',
            text_size=(Window.width - 50, None)
        )
        self.past_box.add_widget(self.past_content)
        self.add_widget(self.past_box)
        
        # --- СЛЕДВАЩО СЪБИТИЕ ---
        self.next_box = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=5,
            size_hint_y=None,
            height=100
        )
        with self.next_box.canvas.before:
            Color(0.1, 0.2, 0.15, 1)
            self.next_rect = Rectangle()
        self.next_box.bind(size=self._update_rect2, pos=self._update_rect2)
        
        self.next_label = Label(
            text="⏰ СЛЕДВАЩО ПРЕДСТОЯЩО СЪБИТИЕ",
            bold=True,
            color=(0.7, 0.7, 0.7, 1),
            font_size='13sp',
            size_hint_y=0.3,
            halign='left'
        )
        self.next_box.add_widget(self.next_label)
        
        self.next_content = Label(
            text="Няма предстоящи събития",
            color=(0.4, 0.9, 0.4, 1),
            font_size='15sp',
            size_hint_y=0.7,
            halign='left',
            text_size=(Window.width - 50, None)
        )
        self.next_box.add_widget(self.next_content)
        self.add_widget(self.next_box)
        
        # --- ВСИЧКИ СЪБИТИЯ ДНЕС ---
        self.today_label = Label(
            text="📅 СЪБИТИЯ ДНЕС",
            bold=True,
            color=(0.8, 0.8, 0.2, 1),
            font_size='14sp',
            size_hint_y=0.05
        )
        self.add_widget(self.today_label)
        
        # Scroll за днешните събития
        self.today_scroll = ScrollView(size_hint=(1, 0.35))
        self.today_box = BoxLayout(
            orientation='vertical',
            spacing=8,
            size_hint_y=None
        )
        self.today_box.bind(minimum_height=self.today_box.setter('height'))
        self.today_scroll.add_widget(self.today_box)
        self.add_widget(self.today_scroll)
        
        # --- ДОЛЕН ПАНЕЛ ---
        bottom_box = BoxLayout(
            orientation='vertical',
            size_hint_y=0.08,
            spacing=2
        )
        
        self.status_label = Label(
            text="🟢 Приложението работи",
            color=(0.3, 0.8, 0.3, 1),
            font_size='12sp'
        )
        bottom_box.add_widget(self.status_label)
        
        btn_box = BoxLayout(size_hint_y=0.5)
        check_btn = Button(
            text="🔍 Провери сега",
            background_color=(0.2, 0.5, 0.8, 1),
            font_size='13sp'
        )
        check_btn.bind(on_press=self.check_now)
        btn_box.add_widget(check_btn)
        
        refresh_btn = Button(
            text="🔄 Обнови",
            background_color=(0.3, 0.3, 0.4, 1),
            font_size='13sp'
        )
        refresh_btn.bind(on_press=self.refresh_data)
        btn_box.add_widget(refresh_btn)
        
        bottom_box.add_widget(btn_box)
        self.add_widget(bottom_box)
        
        # --- ИНИЦИАЛИЗАЦИЯ ---
        self.yearly_events = []
        self.load_events()
        
        # Актуализация на всеки час
        Clock.schedule_interval(self.update_display, 3600)
        
        # Android настройки
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
                Permission.WAKE_LOCK
            ])
        except Exception as e:
            print(f"Грешка: {e}")
    
    def load_events(self):
        try:
            self.yearly_events = generate_yearly_schedule(datetime.now().year)
            self.update_display()
            self.status_label.text = f"✅ Заредени {len(self.yearly_events)} събития"
        except Exception as e:
            self.status_label.text = f"❌ Грешка: {e}"
    
    def refresh_data(self, *args):
        self.load_events()
    
    def update_display(self, *args):
        now = datetime.now()
        today = now.date()
        
        # Намираме събитията за днес
        today_events = [e for e in self.yearly_events if e[0].date() == today]
        
        # --- ПОСЛЕДНО МИНАЛО ---
        past_events = [e for e in self.yearly_events if e[0] < now]
        if past_events:
            last_event = past_events[-1]
            self.past_content.text = (
                f"{last_event[0].strftime('%d.%m.%Y %H:%M')}\n"
                f"{last_event[1]}\n"
                f"{last_event[2]} | {last_event[3]}"
            )
        else:
            self.past_content.text = "📭 Няма минали събития"
        
        # --- СЛЕДВАЩО СЪБИТИЕ ---
        future_events = [e for e in self.yearly_events if e[0] > now]
        if future_events:
            next_event = future_events[0]
            time_left = next_event[0] - now
            hours = int(time_left.total_seconds() / 3600)
            minutes = int((time_left.total_seconds() % 3600) / 60)
            
            self.next_content.text = (
                f"{next_event[0].strftime('%d.%m.%Y %H:%M')}\n"
                f"{next_event[1]}\n"
                f"{next_event[2]} | {next_event[3]}\n"
                f"⏳ След {hours}h {minutes}m"
            )
        else:
            self.next_content.text = "🎉 Няма предстоящи събития"
        
        # --- ДНЕШНИ СЪБИТИЯ ---
        self.today_box.clear_widgets()
        
        if today_events:
            # Групираме по час
            events_by_time = {}
            for e in today_events:
                time_key = e[0].strftime('%H:%M')
                if time_key not in events_by_time:
                    events_by_time[time_key] = []
                events_by_time[time_key].append(e)
            
            # Показваме групираните събития
            for time_key, event_list in sorted(events_by_time.items()):
                hour_label = Label(
                    text=f"🕐 {time_key} - {len(event_list)} събития",
                    bold=True,
                    color=(0.6, 0.8, 1, 1),
                    font_size='13sp',
                    size_hint_y=None,
                    height=25
                )
                self.today_box.add_widget(hour_label)
                
                for event in event_list:
                    status = "✅" if event[0] < now else "⏳"
                    event_text = (
                        f"{status} {event[1]}\n"
                        f"   {event[2]} | {event[3]}"
                    )
                    event_label = Label(
                        text=event_text,
                        color=(0.9, 0.9, 0.9, 1),
                        font_size='12sp',
                        size_hint_y=None,
                        height=40,
                        halign='left',
                        text_size=(Window.width - 60, None)
                    )
                    self.today_box.add_widget(event_label)
        else:
            self.today_box.add_widget(Label(
                text="📭 Няма събития за днес",
                color=(0.6, 0.6, 0.6, 1),
                font_size='14sp',
                size_hint_y=None,
                height=40
            ))
    
    def check_now(self, *args):
        """Ръчна проверка на събитията"""
        try:
            from service import check_and_notify
            result = check_and_notify()
            if result:
                self.status_label.text = "✅ Изпратени нотификации!"
            else:
                self.status_label.text = "ℹ️ Няма събития в момента"
            self.update_display()
        except Exception as e:
            self.status_label.text = f"❌ Грешка: {e}"

class NotificationApp(App):
    def build(self):
        return MainWidget()
    
    def on_start(self):
        print("✅ Приложението стартира")
    
    def on_stop(self):
        print("🛑 Приложението спира")

if __name__ == "__main__":
    NotificationApp().run()
