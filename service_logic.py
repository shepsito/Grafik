from datetime import datetime, timedelta
import calendar

# --- НОВА ПРАВИЛНА ЛОГИКА ЗА СЕДМИЦИ ---
def get_week_of_month(date):
    """
    Връща седмица от месеца според ПЪЛНИ седмици.
    Седмица започва в понедеделник.
    """
    first_day = date.replace(day=1)
    first_weekday = first_day.weekday()  # 0 = Monday

    # намираме първия понеделник в месеца
    if first_weekday == 0:
        first_monday = first_day
    else:
        first_monday = first_day + timedelta(days=(7 - first_weekday))

    # ако датата е преди първия понеделник → седмица 0
    if date < first_monday:
        return 0

    # изчисляваме седмицата
    delta_days = (date - first_monday).days
    week_number = (delta_days // 7) + 1

    return week_number


# --- ПОМОЩНИ ФУНКЦИИ (остават същите) ---
def is_last_monday_of_quarter(date):
    return date.weekday() == 0 and date.month in [3, 6, 9, 12] and calendar.monthrange(date.year, date.month)[1] - date.day < 7

def is_last_tuesday_of_quarter(date):
    return date.weekday() == 1 and date.month in [3, 6, 9, 12] and calendar.monthrange(date.year, date.month)[1] - date.day < 7

def is_last_wednesday_of_quarter(date):
    return date.weekday() == 2 and date.month in [3, 6, 9, 12] and calendar.monthrange(date.year, date.month)[1] - date.day < 7

def is_last_thursday_of_quarter(date):
    return date.weekday() == 3 and date.month in [3, 6, 9, 12] and calendar.monthrange(date.year, date.month)[1] - date.day < 7

def is_last_friday_of_quarter(date):
    return date.weekday() == 4 and date.month in [3, 6, 9, 12] and calendar.monthrange(date.year, date.month)[1] - date.day < 7


# --- ГЕНЕРИРАНЕ НА ГРАФИК ---
def generate_yearly_schedule(year):
    events = []
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    current = start_date

    while current <= end_date:
        current_day = current.day
        current_month = current.month
        week = get_week_of_month(current)
        shift = "Смяна 3"

        # 1. Проверка АВР (месеци 2 и 9, първи понеделник)
        if current_month in [2, 9] and current.weekday() == 0 and week == 1:
            events.append({
                'datetime': current.replace(hour=15),
                'title': ' Проверка АВР',
                'facility': 'Аварийно осветление',
                'description': 'Проверка АВР на захранването-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': shift
            })

        # 2. ЕЕ ЦПС-1 (ден 11 и 12)
        if current_day in [11, 12]:
            events.append({
                'datetime': current.replace(hour=15),
                'title': ' ЕЕ ЦПС-1',
                'facility': 'ЕЕ ЦПС-1',
                'description': 'Проверка изправноста на аварийното осветление-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': shift
            })

        # 3. Ф.И. Проверка (месеци 3 и 10, седмица 1 или 2)
        if current_month in [3, 10] and current.weekday() == 0 and week in [1, 2]:
            events.append({
                'datetime': current.replace(hour=7),
                'title': ' Ф.И. Проверка',
                'facility': 'По процедура',
                'description': 'Ф.И. на аварийното осветление-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': 'Смяна 2'
            })

        # 4. МЗ и ЕЕ ЦПС-1 (ден 15)
        if current_day == 15:
            events.append({
                'datetime': current.replace(hour=15),
                'title': ' МЗ и ЕЕ ЦПС-1',
                'facility': 'МЗ и ЕЕ ЦПС-1',
                'description': 'Проверка изправността на евакуационното осветление-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': shift
            })

        # 5–9. Последни дни на тримесечие
        if is_last_monday_of_quarter(current):
            events.append({
                'datetime': current.replace(hour=15),
                'title': ' Проверка АВР (Пон.)',
                'facility': 'МЗ,ЦПС-1',
                'description': 'Проверка АВР сборки на 0,4кВ захранвани от 3 и 4 БН-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': shift
            })

        if is_last_tuesday_of_quarter(current):
            events.append({
                'datetime': current.replace(hour=15),
                'title': ' Проверка АВР (Вт.)',
                'facility': 'МЗ',
                'description': 'Проверка АВР сборки на 0,4кВ захранвани от 23 и 24 БН-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': shift
            })

        if is_last_wednesday_of_quarter(current):
            events.append({
                'datetime': current.replace(hour=15),
                'title': ' Проверка АВР (Ср.)',
                'facility': 'МЗ',
                'description': 'Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 3-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': shift
            })

        if is_last_thursday_of_quarter(current):
            events.append({
                'datetime': current.replace(hour=15),
                'title': ' Проверка АВР (Четв.)',
                'facility': 'МЗ',
                'description': 'Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 4-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': shift
            })

        if is_last_friday_of_quarter(current):
            events.append({
                'datetime': current.replace(hour=23),
                'title': ' Проверка АВР (Петък)',
                'facility': 'МЗ,ХВО и ЦПС-1',
                'description': 'Проверка АВР сборки на 0,4кВ с/без сборки захр.от 3,4,23,24БН,33БН I-III,43БН I-III-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': 'Смяна 1'
            })

        # 10. Секции 0,4кВ-ГК (ден 8)
        if current_day == 8:
            events.append({
                'datetime': current.replace(hour=23),
                'title': ' Секции 0,4кВ-ГК',
                'facility': 'Секции 0,4кВ-ГК 1-4 block',
                'description': 'Проверка АВР на -ШУ и сигнализацията-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': 'Смяна 1'
            })

        # 11. Вентилни отводи (ден 18)
        if current_day == 18:
            events.append({
                'datetime': current.replace(hour=15),
                'title': ' Вентилни отводи',
                'facility': 'Вентилни отводи 1 и 3 ТП',
                'description': 'Отчитане на -вентилни отводи-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': shift
            })

        # 12. Ел.двигатели 6кВ (ден 1)
        if current_day == 1:
            events.append({
                'datetime': current.replace(hour=23),
                'title': ' Ел.двигатели 6кВ',
                'facility': 'Ел.двигатели 6кВ',
                'description': 'Измерване isoлацията-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': 'Смяна 1'
            })

        # 13. Проверка ДГ-А (седмица 1)
        if current_month in [1, 4, 7, 10] and current.weekday() == 0 and week == 1:
            events.append({
                'datetime': current.replace(hour=7),
                'title': ' Проверка ДГ-А',
                'facility': 'ДГ-A',
                'description': 'Ф.И. ≥ 60мин-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': 'Смяна 2'
            })

        # 14. Проверка ДГ-Б (седмица 2)
        if current_month in [1, 4, 7, 10] and current.weekday() == 0 and week == 2:
            events.append({
                'datetime': current.replace(hour=7),
                'title': ' Проверка ДГ-Б',
                'facility': 'ДГ-Б',
                'description': 'Ф.И. ≥ 60мин-[color=ff0000]НСЕО ОЕОиСКУ[/color]',
                'shift': 'Смяна 2'
            })

        # 15. Проверка 2АДГ-ДСАПП-4 (сряда седмица 3)
        if current_month in [1, 4, 7, 10] and current.weekday() == 2 and week == 3:
            events.append({
                'datetime': current.replace(hour=7),
                'title': ' Проверка 2АДГ-ДСАПП-4',
                'facility': '2АДГ-ДСАПП-4',
                'description': 'Ф.И аварийно ел.захранване-[color=ff0000]НСЕО[/color]',
                'shift': 'Смяна 2'
            })

        # 16. Проверка ДГ-КАС (четвъртък седмица 3)
        if current_month in [1, 4, 7, 10] and current.weekday() == 3 and week == 3:
            events.append({
                'datetime': current.replace(hour=7),
                'title': ' Проверка ДГ-КАС',
                'facility': 'ДГ-КАС',
                'description': 'Ф.И аварийно ел.захранване-[color=ff0000]НСЕО[/color]',
                'shift': 'Смяна 2'
            })

        # 17. Проверка ГРТ-ЦНРД (месеци 6,12, понеделник седмица 3)
        if current_month in [6, 12] and current.weekday() == 0 and week == 3:
            events.append({
                'datetime': current.replace(hour=7),
                'title': ' Проверка ГРТ-ЦНРД',
                'facility': 'ГРТ-ЦНРД',
                'description': 'Изпробване АВР-[color=ff0000]НСЕО[/color]',
                'shift': 'Смяна 2'
            })

        # 18. Отчитане електромери (ден 1)
        if current_day == 1:
            events.append({
                'datetime': current.replace(hour=7),
                'title': ' Отчитане електромери',
                'facility': 'Методика ДП.ЕД.МТ.1153',
                'description': 'Отчитане електромери-[color=ff0000]НСЕО[/color]',
                'shift': 'Смяна 2'
            })

        # 19. Проверка ТП1, ТП3 (събота седмица 3)
        if current.weekday() == 5 and week == 3:
            events.append({
                'datetime': current.replace(hour=7),
                'title': ' Проверка ТП1, ТП3',
                'facility': 'ТП1,ТП3',
                'description': 'Изпробване вентилатори-[color=ff0000]НСЕО[/color]',
                'shift': 'Смяна 2'
            })

        # 20. Измерване стойности по фидери (сряда или събота седмица 3)
        if current.weekday() in [2, 5] and week == 3:
            events.append({
                'datetime': current.replace(hour=23),
                'title': ' Измерване стойности по фидери',
                'facility': 'Методика ДП.ЕД.МТ.1153',
                'description': 'Измерване стойности-[color=ff0000]НСЕО[/color]',
                'shift': 'Смяна 1'
            })
            events.append({
                'datetime': current.replace(hour=7),
                'title': ' Измерване стойности по фидери',
                'facility': 'Методика ДП.ЕД.МТ.1153',
                'description': 'Измерване стойности-[color=ff0000]НСЕО[/color]',
                'shift': 'Смяна 2'
            })
            events.append({
                'datetime': current.replace(hour=15),
                'title': ' Измерване стойности по фидери',
                'facility': 'Методика ДП.ЕД.МТ.1153',
                'description': 'Измерване стойности-[color=ff0000]НСЕО[/color]',
                'shift': 'Смяна 3'
            })

        current += timedelta(days=1)

    return sorted(events, key=lambda x: x['datetime'])


def get_shift_hours(shift):
    return {"Смяна 1": 23, "Смяна 2": 7, "Смяна 3": 15}.get(shift, 0)
