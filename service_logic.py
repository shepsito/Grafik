from datetime import datetime, timedelta
import calendar

# --- Помощни функции ---
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

def generate_yearly_schedule(year):
    """Генерира годишен график с всички събития - ПОДРЕДЕНИ ПО ДАТА"""
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
        
        # --- СЪБИТИЯТА ПОДРЕДЕНИ ПО ДАТА И ЧАС ---
        
        # 1. Ел.двигатели 6кВ (ден 1) - 23:00
        if current_day == 1:
            events.append({
                'datetime': current.replace(hour=23, minute=0),
                'title': '🚨 Ел.двигатели 6кВ',
                'facility': 'Ел.двигатели 6кВ',
                'description': 'Измерване съпротивлението на изолацията на ел.двиг.6кВ-ПВТ в резерв,1и 2ППП-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 1',
                'priority': 1
            })
        
        # 2. Отчитане електромери (ден 1) - 07:00
        if current_day == 1:
            events.append({
                'datetime': current.replace(hour=7, minute=0),
                'title': '🚨 Отчитане електромери',
                'facility': 'По методика ДП.ЕД.МТ.1153',
                'description': 'Отчитане електомерите за консумирана ел.енергия-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 2',
                'priority': 2
            })
        
        # 3. Секции 0,4кВ-ГК (ден 8) - 23:00
        if current_day == 8:
            events.append({
                'datetime': current.replace(hour=23, minute=0),
                'title': '🚨 Секции 0,4кВ-ГК',
                'facility': 'Секции 0,4кВ-ГК 1_4 block',
                'description': 'Проверка АВР на ШУ и изправността на сигнализацията на панел "С"БЩУ за повикване в КРУ-ДИС ОЕОиСКУ',
                'shift': 'Смяна 1',
                'priority': 1
            })
        
        # 4. ЕЕ ЦПС-2 (ден 11) - 15:00
        if current_day == 11:
            events.append({
                'datetime': current.replace(hour=15, minute=0),
                'title': '🚨 ЕЕ ЦПС-2',
                'facility': 'ЕЕ ЦПС-2',
                'description': 'Проверка изправноста на аварийното осветление-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 3',
                'priority': 1
            })
        
        # 5. ЕЕ ЦПС-2 (ден 12) - 15:00
        if current_day == 12:
            events.append({
                'datetime': current.replace(hour=15, minute=0),
                'title': '🚨 ЕЕ ЦПС-2',
                'facility': 'ЕЕ ЦПС-2',
                'description': 'Проверка изправноста на аварийното осветление-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 3',
                'priority': 1
            })
        
        # 6. МЗ и ЕЕ ЦПС-1 (ден 15) - 15:00
        if current_day == 15:
            events.append({
                'datetime': current.replace(hour=15, minute=0),
                'title': '🚨 МЗ и ЕЕ ЦПС-1',
                'facility': 'МЗ и ЕЕ ЦПС-1',
                'description': 'Проверка изправността на евакуационното осветление-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 3',
                'priority': 1
            })
        
        # 7. Вентилни отводи (ден 18) - 15:00
        if current_day == 18:
            events.append({
                'datetime': current.replace(hour=15, minute=0),
                'title': '🚨 Вентилни отводи',
                'facility': 'Вентилни отводи 1 и 3 ТП',
                'description': 'Отчитане на вентилни отводи-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 3',
                'priority': 1
            })
        
        # 8. Проверка АВР (месеци 2 и 9, първи понеделник) - 07:00
        if current_month in [2, 9] and monday_week == 1:
            events.append({
                'datetime': current.replace(hour=7, minute=0),
                'title': '🚨 Проверка АВР',
                'facility': 'Аварийно осветление',
                'description': 'Проверка АВР на захранването-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 2',
                'priority': 1
            })
        
        # 9. Ф.И. Проверка (месеци 3 и 10, седмица 1 или 2) - 15:00
        if current_month in [3, 10] and monday_week in [1, 2]:
            events.append({
                'datetime': current.replace(hour=15, minute=0),
                'title': '🚨 Ф.И. Проверка',
                'facility': 'По процедура',
                'description': 'Ф.И. на аварийното осветление-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 3',
                'priority': 1
            })
        
        # 10. Проверка ДГ-А (месеци 1,4,7,10, седмица 1) - 07:00
        if current_month in [1, 4, 7, 10] and monday_week == 1:
            events.append({
                'datetime': current.replace(hour=7, minute=0),
                'title': '🚨 Проверка ДГ-А',
                'facility': 'ДГ-A',
                'description': 'Ф.И. на автономен товар не по малко от 60мин-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 2',
                'priority': 2
            })
        
        # 11. Проверка ДГ-Б (месеци 1,4,7,10, седмица 2) - 07:00
        if current_month in [1, 4, 7, 10] and monday_week == 2:
            events.append({
                'datetime': current.replace(hour=7, minute=0),
                'title': '🚨 Проверка ДГ-Б',
                'facility': 'ДГ-Б',
                'description': 'Ф.И. на автономен товар не по малко от 60мин-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 2',
                'priority': 2
            })
        
        # 12. Проверка 2АДГ-ДСАПП-4 (месеци 1,4,7,10, сряда седмица 3) - 07:00
        if current_month in [1, 4, 7, 10] and wednesday_week == 3:
            events.append({
                'datetime': current.replace(hour=7, minute=0),
                'title': '🚨 Проверка 2АДГ-ДСАПП-4',
                'facility': '2АДГ-ДСАПП-4',
                'description': 'Ф.И на аварийното ел.захранване на СПИ-НСЕО Енергетик ПРАО',
                'shift': 'Смяна 2',
                'priority': 2
            })
        
        # 13. Проверка ДГ-КАС (месеци 1,4,7,10, четвъртък седмица 3) - 07:00
        if current_month in [1, 4, 7, 10] and thursday_week == 3:
            events.append({
                'datetime': current.replace(hour=7, minute=0),
                'title': '🚨 Проверка ДГ-КАС',
                'facility': 'ДГ-КАС',
                'description': 'Ф.И на аварийното ел.захранване на СПИ-НСЕО Енергетик ПРАО',
                'shift': 'Смяна 2',
                'priority': 2
            })
        
        # 14. Проверка ГРТ-ЦНРД (месеци 6,12, понеделник седмица 3) - 07:00
        if current_month in [6, 12] and monday_week == 3:
            events.append({
                'datetime': current.replace(hour=7, minute=0),
                'title': '🚨 Проверка ГРТ-ЦНРД',
                'facility': 'ГРТ-ЦНРД',
                'description': 'Изпробване на АВР на ел.захранването-ДИС НСЕО Енергетик ПРАО',
                'shift': 'Смяна 2',
                'priority': 2
            })
        
        # 15. Проверка ТП1, ТП3 (събота седмица 3) - 07:00
        if saturday_week == 3:
            events.append({
                'datetime': current.replace(hour=7, minute=0),
                'title': '🚨 Проверка ТП1, ТП3',
                'facility': 'ТП1,ТП3',
                'description': 'Изпробване на охлаждащите вентилатори на 1ТП и 3ТП чрез ръчно включване-НСЕО',
                'shift': 'Смяна 2',
                'priority': 2
            })
        
        # 16. Проверка АВР (последен понеделник на тримесечие) - 15:00
        if is_last_monday_of_quarter(current):
            events.append({
                'datetime': current.replace(hour=15, minute=0),
                'title': '🚨 Проверка АВР (Пон.)',
                'facility': 'МЗ,ЦПС-1',
                'description': 'Проверка АВР сборки на 0,4кВ захранвани от 3 и 4 БН-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 3',
                'priority': 1
            })
        
        # 17. Проверка АВР (последен вторник на тримесечие) - 15:00
        if is_last_tuesday_of_quarter(current):
            events.append({
                'datetime': current.replace(hour=15, minute=0),
                'title': '🚨 Проверка АВР (Вт.)',
                'facility': 'МЗ',
                'description': 'Проверка АВР сборки на 0,4кВ захранвани от 23 и 24 БН-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 3',
                'priority': 1
            })
        
        # 18. Проверка АВР (последна сряда на тримесечие) - 15:00
        if is_last_wednesday_of_quarter(current):
            events.append({
                'datetime': current.replace(hour=15, minute=0),
                'title': '🚨 Проверка АВР (Ср.)',
                'facility': 'МЗ',
                'description': 'Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 3-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 3',
                'priority': 1
            })
        
        # 19. Проверка АВР (последен четвъртък на тримесечие) - 15:00
        if is_last_thursday_of_quarter(current):
            events.append({
                'datetime': current.replace(hour=15, minute=0),
                'title': '🚨 Проверка АВР (Четв.)',
                'facility': 'МЗ',
                'description': 'Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 4-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 3',
                'priority': 1
            })
        
        # 20. Проверка АВР (последен петък на тримесечие) - 23:00
        if is_last_friday_of_quarter(current):
            events.append({
                'datetime': current.replace(hour=23, minute=0),
                'title': '🚨 Проверка АВР (Петък)',
                'facility': 'МЗ,ХВО и ЦПС-1',
                'description': 'Проверка АВР сборки на 0,4кВ с/без сборки захр.от 3,4,23,24БН,33БН I-III,43БН I-III -НСЕО ОЕОиСКУ',
                'shift': 'Смяна 1',
                'priority': 1
            })
        
        # 21. Измерване стойности по фидери (сряда или събота седмица 3)
        if wednesday_week == 3 or saturday_week == 3:
            # Смяна 1 - 23:00
            events.append({
                'datetime': current.replace(hour=23, minute=0),
                'title': '🚨 Измерване стойности по фидери',
                'facility': 'По методика ДП.ЕД.МТ.1153',
                'description': 'Измерване стойностите по фидерите за АКС,СБК-2 и ТРЗ/Бюро пропуски-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 1',
                'priority': 1
            })
            # Смяна 2 - 07:00
            events.append({
                'datetime': current.replace(hour=7, minute=0),
                'title': '🚨 Измерване стойности по фидери',
                'facility': 'По методика ДП.ЕД.МТ.1153',
                'description': 'Измерване стойностите по фидерите за АКС,СБК-2 и ТРЗ/Бюро пропуски-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 2',
                'priority': 2
            })
            # Смяна 3 - 15:00
            events.append({
                'datetime': current.replace(hour=15, minute=0),
                'title': '🚨 Измерване стойности по фидери',
                'facility': 'По методика ДП.ЕД.МТ.1153',
                'description': 'Измерване стойностите по фидерите за АКС,СБК-2 и ТРЗ/Бюро пропуски-НСЕО ОЕОиСКУ',
                'shift': 'Смяна 3',
                'priority': 3
            })

        current += timedelta(days=1)
    
    # Сортираме по дата и час
    return sorted(events, key=lambda x: x['datetime'])

def get_shift_hours(shift):
    """Връща часа за дадена смяна"""
    shift_map = {
        "Смяна 1": 23,
        "Смяна 2": 7,
        "Смяна 3": 15
    }
    return shift_map.get(shift, 0)
