from datetime import datetime, timedelta
import calendar
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

# --- Прецизни помощни логически функции за седмици и тримесечия ---

def get_monday_week_number(date):
    if date.weekday() != 0: return 0
    return 1 if date.day <= 7 else 2 if date.day <= 14 else 3 if date.day <= 21 else 4

def get_wednesday_week_number(date):
    if date.weekday() != 2: return 0
    return 1 if date.day <= 7 else 2 if date.day <= 14 else 3 if date.day <= 21 else 4

def get_thursday_week_number(date):
    if date.weekday() != 3: return 0
    return 1 if date.day <= 7 else 2 if date.day <= 14 else 3 if date.day <= 21 else 4

def get_saturday_week_number(date):
    if date.weekday() != 5: return 0
    return 1 if date.day <= 7 else 2 if date.day <= 14 else 3 if date.day <= 21 else 4

def is_last_monday_of_quarter(date):
    if date.weekday() != 0: return False
    if date.month in [3, 6, 9, 12]:
        return calendar.monthrange(date.year, date.month)[1] - date.day < 7
    return False

def is_last_tuesday_of_quarter(date):
    if date.weekday() != 1: return False
    if date.month in [3, 6, 9, 12]:
        return calendar.monthrange(date.year, date.month)[1] - date.day < 7
    return False

def is_last_wednesday_of_quarter(date):
    if date.weekday() != 2: return False
    if date.month in [3, 6, 9, 12]:
        return calendar.monthrange(date.year, date.month)[1] - date.day < 7
    return False

def is_last_thursday_of_quarter(date):
    if date.weekday() != 3: return False
    if date.month in [3, 6, 9, 12]:
        return calendar.monthrange(date.year, date.month)[1] - date.day < 7
    return False

def is_last_friday_of_quarter(date):
    if date.weekday() != 4: return False
    if date.month in [3, 6, 9, 12]:
        return calendar.monthrange(date.year, date.month)[1] - date.day < 7
    return False


# --- Генериране на годишния календар ---
def generate_yearly_schedule(year):
    events = []
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    current = start_date

    while current <= end_date:
        current_day = current.day
        current_month = current.month
        
        monday_week = get_monday_week_number(current)
        wednesday_week = get_wednesday_week_number(current)
        thursday_week = get_thursday_week_number(current)
        saturday_week = get_saturday_week_number(current)

        shift = "Смяна 3" 

        # --- ПРАВИЛО 1: Февруари и Септември (Първи Понеделник) ---
        if current_month in [2, 9] and monday_week == 1:
            events.append((current, "🚨 График: Проверка АВР", f"Съоръжение: Аварийно осветление\nПроверка: Проверка АВР на захранването\nСмяна: {shift}"))

        # --- ПРАВИЛО 2: Всеки месец на 11-то и 12-то число ---
        if current_day in [11, 12]:
            events.append((current, "🚨 График: ЕЕ ЦПС-2", f"Съоръжение: ЕЕ ЦПС-2\nПроверка: Проверка изправноста на аварийното осветление\nСмяна: {shift}"))

        # --- ПРАВИЛО 3: Март и Октомври (Първи и Втори Понеделник) ---
        if current_month in [3, 10] and monday_week in [1, 2]:
            events.append((current, "🚨 График: Ф.И. Проверка", f"Съоръжение: По процедура\nПроверка: Ф.И. на аварийното осветление\nСмяна: {shift}"))

        # --- ПРАВИЛО 4: Всеки месец на 15-то число ---
        if current_day == 15:
            events.append((current, "🚨 График: МЗ и ЕЕ ЦПС-1", f"Съоръжение: МЗ и ЕЕ ЦПС-1\nПроверка: Проверка изправността на евакуационното осветление\nСмяна: {shift}"))

        # --- ПРАВИЛО 5
