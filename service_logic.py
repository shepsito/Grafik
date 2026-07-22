from datetime import datetime, timedelta
import calendar

def get_week_of_month(date):
    first_day = date.replace(day=1)
    first_weekday = first_day.weekday()
    if first_weekday == 0:
        first_monday = first_day
    else:
        first_monday = first_day + timedelta(days=(7 - first_weekday))
    if date < first_monday:
        return 0
    delta_days = (date - first_monday).days
    return (delta_days // 7) + 1

def is_last_monday_of_quarter(date):
    return date.weekday() == 0 and date.month in [3,6,9,12] and calendar.monthrange(date.year,date.month)[1] - date.day < 7

def is_last_tuesday_of_quarter(date):
    return date.weekday() == 1 and date.month in [3,6,9,12] and calendar.monthrange(date.year,date.month)[1] - date.day < 7

def is_last_wednesday_of_quarter(date):
    return date.weekday() == 2 and date.month in [3,6,9,12] and calendar.monthrange(date.year,date.month)[1] - date.day < 7

def is_last_thursday_of_quarter(date):
    return date.weekday() == 3 and date.month in [3,6,9,12] and calendar.monthrange(date.year,date.month)[1] - date.day < 7

def is_last_friday_of_quarter(date):
    return date.weekday() == 4 and date.month in [3,6,9,12] and calendar.monthrange(date.year,date.month)[1] - date.day < 7

def generate_yearly_schedule(year):
    events = []
    current = datetime(year,1,1)
    end = datetime(year,12,31)

    while current <= end:
        day = current.day
        month = current.month
        week = get_week_of_month(current)

        # Смяна 1 → ВАРИАНТ А → вчера 23:00
        def night_event(title, facility, description):
            return {
                'datetime': (current - timedelta(days=1)).replace(hour=23),
                'title': title,
                'facility': facility,
                'description': description,
                'shift': 'Смяна 1'
            }

        # Смяна 2 → 07:00
        def morning_event(title, facility, description):
            return {
                'datetime': current.replace(hour=7),
                'title': title,
                'facility': facility,
                'description': description,
                'shift': 'Смяна 2'
            }

        # Смяна 3 → 15:00
        def afternoon_event(title, facility, description):
            return {
                'datetime': current.replace(hour=15),
                'title': title,
                'facility': facility,
                'description': description,
                'shift': 'Смяна 3'
            }

        # --- ВСИЧКИ ТВОИ УСЛОВИЯ (НЕ СЪМ ПРОМЕНЯЛ НИЩО ДРУГО) ---

        if month in [2,9] and current.weekday()==0 and week==1:
            events.append(afternoon_event(' Проверка АВР','Аварийно осветление','Проверка АВР-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if day in [11,12]:
            events.append(afternoon_event(' ЕЕ ЦПС-1','ЕЕ ЦПС-1','Проверка аварийно осветление-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if month in [3,10] and current.weekday()==0 and week in [1,2]:
            events.append(morning_event(' Ф.И. Проверка','По процедура','Ф.И аварийно осветление-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if day == 15:
            events.append(afternoon_event(' МЗ и ЕЕ ЦПС-1','МЗ и ЕЕ ЦПС-1','Проверка евакуационно осветление-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_monday_of_quarter(current):
            events.append(afternoon_event(' Проверка АВР (Пон.)','МЗ,ЦПС-1','Проверка АВР-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_tuesday_of_quarter(current):
            events.append(afternoon_event(' Проверка АВР (Вт.)','МЗ','Проверка АВР-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_wednesday_of_quarter(current):
            events.append(afternoon_event(' Проверка АВР (Ср.)','МЗ','Проверка АВР-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_thursday_of_quarter(current):
            events.append(afternoon_event(' Проверка АВР (Четв.)','МЗ','Проверка АВР-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if is_last_friday_of_quarter(current):
            events.append(night_event(' Проверка АВР (Петък)','МЗ,ХВО и ЦПС-1','Проверка АВР-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if day == 8:
            events.append(night_event(' Секции 0,4кВ-ГК','Секции 0,4кВ-ГК','Проверка АВР-[color=ff0000]ДИС,ОЕОи СКУ[/color]'))

        if day == 18:
            events.append(afternoon_event(' Вентилни отводи','Вентилни отводи','Отчитане-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if day == 1:
            events.append(night_event(' Ел.двигатели 6кВ','Ел.двигатели 6кВ','Измерване-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))
            events.append(morning_event(' Отчитане електромери','Методика','Отчитане-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if month in [1,4,7,10] and current.weekday()==0 and week==1:
            events.append(morning_event(' Проверка ДГ-А','ДГ-А','Ф.И ≥60мин-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if month in [1,4,7,10] and current.weekday()==0 and week==2:
            events.append(morning_event(' Проверка ДГ-Б','ДГ-Б','Ф.И ≥60мин-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        if month in [1,4,7,10] and current.weekday()==2 and week==3:
            events.append(morning_event(' Проверка 2АДГ-ДСАПП-4','2АДГ-ДСАПП-4','Ф.И аварийно захранване-[color=ff0000]НСЕО,ЕнергетикПРАО[/color]'))

        if month in [1,4,7,10] and current.weekday()==3 and week==3:
            events.append(morning_event(' Проверка ДГ-КАС','ДГ-КАС','Ф.И аварийно захранване-[color=ff0000]НСЕО,ЕнергетикПРАО[/color]'))

        if month in [6,12] and current.weekday()==0 and week==3:
            events.append(morning_event(' Проверка ГРТ-ЦНРД','ГРТ-ЦНРД','Изпробване АВР-[color=ff0000]НСЕО,ЕнергетикПРАО,ДИС[/color]'))

        if current.weekday() == 5 and week == 3:
            events.append(morning_event(' Проверка ТП1,ТП3','ТП1,ТП3','Изпробване вентилатори-[color=ff0000]НСЕО[/color]'))

        if current.weekday() in [2,5] and week == 3:
            events.append(night_event(' Измерване стойности по фидери','Методика','Измерване-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))
            events.append(morning_event(' Измерване стойности по фидери','Методика','Измерване-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))
            events.append(afternoon_event(' Измерване стойности по фидери','Методика','Измерване-[color=ff0000]НСЕО,ОЕОи СКУ[/color]'))

        current += timedelta(days=1)

    return sorted(events, key=lambda x: x['datetime'])
