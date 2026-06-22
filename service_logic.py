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
    """Генерира годишен график с всички събития"""
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
        
        # --- ВСИЧКИ СЪБИТИЯ ОТ ВАШИЯ КОД ---
        
        # 1. Проверка АВР (месеци 2 и 9, първи понеделник)
        if current_month in [2, 9] and monday_week == 1:
            events.append((current, "🚨 Проверка АВР", "Аварийно осветление", "Проверка АВР на захранването-НСЕО ОЕОиСКУ", "Смяна 2"))
        
        # 2. ЕЕ ЦПС-2 (ден 11 и 12)
        if current_day in [11, 12]:
            events.append((current, "🚨 ЕЕ ЦПС-2", "ЕЕ ЦПС-2", "Проверка изправноста на аварийното осветление-НСЕО ОЕОиСКУ", "Смяна 3"))
        
        # 3. Ф.И. Проверка (месеци 3 и 10, седмица 1 или 2)
        if current_month in [3, 10] and monday_week in [1, 2]:
            events.append((current, "🚨 Ф.И. Проверка", "По процедура", "Ф.И. на аварийното осветление-НСЕО ОЕОиСКУ", "Смяна 3"))
        
        # 4. МЗ и ЕЕ ЦПС-1 (ден 15)
        if current_day == 15:
            events.append((current, "🚨 МЗ и ЕЕ ЦПС-1", "МЗ и ЕЕ ЦПС-1", "Проверка изправността на евакуационното осветление-НСЕО ОЕОиСКУ", "Смяна 3"))
        
        # 5. Проверка АВР (последен понеделник на тримесечие)
        if is_last_monday_of_quarter(current):
            events.append((current, "🚨 Проверка АВР (Пон.)", "МЗ,ЦПС-1", "Проверка АВР сборки на 0,4кВ захранвани от 3 и 4 БН-НСЕО ОЕОиСКУ", "Смяна 3"))
        
        # 6. Проверка АВР (последен вторник на тримесечие)
        if is_last_tuesday_of_quarter(current):
            events.append((current, "🚨 Проверка АВР (Вт.)", "МЗ", "Проверка АВР сборки на 0,4кВ захранвани от 23 и 24 БН-НСЕО ОЕОиСКУ", "Смяна 3"))
        
        # 7. Проверка АВР (последна сряда на тримесечие)
        if is_last_wednesday_of_quarter(current):
            events.append((current, "🚨 Проверка АВР (Ср.)", "МЗ", "Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 3-НСЕО ОЕОиСКУ", "Смяна 3"))
        
        # 8. Проверка АВР (последен четвъртък на тримесечие)
        if is_last_thursday_of_quarter(current):
            events.append((current, "🚨 Проверка АВР (Четв.)", "МЗ", "Проверка АВР сборки на 0,4кВ съответната с-ма-I (II,III)-блок 4-НСЕО ОЕОиСКУ", "Смяна 3"))
        
        # 9. Проверка АВР (последен петък на тримесечие)
        if is_last_friday_of_quarter(current):
            events.append((current, "🚨 Проверка АВР (Петък)", "МЗ,ХВО и ЦПС-1", "Проверка АВР сборки на 0,4кВ с/без сборки захр.от 3,4,23,24БН,33БН I-III,43БН I-III /-НСЕО ОЕОиСКУ", "Смяна 1"))
        
        # 10. Секции 0,4кВ-ГК (ден 8)
        if current_day == 8:
            events.append((current, "🚨 Секции 0,4кВ-ГК", "Секции 0,4кВ-ГК 1_4 block", "Проверка АВР на -ШУ и изправността на сигнализацията на панел 'С'БЩУ за повикване в КРУ-ДИС ОЕОиСКУ", "Смяна 1"))
        
        # 11. Вентилни отводи (ден 18)
        if current_day == 18:
            events.append((current, "🚨 Вентилни отводи", "Вентилни отводи 1 и 3 ТП", "Отчитане на -вентилни отводи-НСЕО ОЕОиСКУ", "Смяна 3"))
        
        # 12. Ел.двигатели 6кВ (ден 1)
        if current_day == 1:
            events.append((current, "🚨 Ел.двигатели 6кВ", "Ел.двигатели 6кВ", "Измерване съпротивлението на isoлацията на ел.двиг.6кВ.-ПВТ в резерв,1и 2ППП-НСЕО ОЕОиСКУ", "Смяна 1"))
        
        # 13. Проверка ДГ-А (месеци 1,4,7,10, седмица 1)
        if current_month in [1, 4, 7, 10] and monday_week == 1:
            events.append((current, "🚨 Проверка ДГ-А", "ДГ-A", "Ф.И. на автономен товар не по малко от 60мин.-НСЕО ОЕОиСКУ", "Смяна 2"))
        
        # 14. Проверка ДГ-Б (месеци 1,4,7,10, седмица 2)
        if current_month in [1, 4, 7, 10] and monday_week == 2:
            events.append((current, "🚨 Проверка ДГ-Б", "ДГ-Б", "Ф.И. на автономен товар не по малко от 60мин.-НСЕО ОЕОиСКУ", "Смяна 2"))
        
        # 15. Проверка 2АДГ-ДСАПП-4 (месеци 1,4,7,10, сряда седмица 3)
        if current_month in [1, 4, 7, 10] and wednesday_week == 3:
            events.append((current, "🚨 Проверка 2АДГ-ДСАПП-4", "2АДГ-ДСАПП-4", "Ф.И на аварийното ел.захранване на СПИ-НСЕО Енергетик ПРАО", "Смяна 2"))
        
        # 16. Проверка ДГ-КАС (месеци 1,4,7,10, четвъртък седмица 3)
        if current_month in [1, 4, 7, 10] and thursday_week == 3:
            events.append((current, "🚨 Проверка ДГ-КАС", "ДГ-КАС", "Ф.И на аварийното ел.захранване на СПИ-НСЕО Енергетик ПРАО", "Смяна 2"))
        
        # 17. Проверка ГРТ-ЦНРД (месеци 6,12, понеделник седмица 3)
        if current_month in [6, 12] and monday_week == 3:
            events.append((current, "🚨 Проверка ГРТ-ЦНРД", "ГРТ-ЦНРД", "Изпробване на АВР на ел.захранването-ДИС НСЕО Енергетик ПРАО", "Смяна 2"))
        
        # 18. Отчитане електромери (ден 1)
        if current_day == 1:
            events.append((current, "🚨 Отчитане електромери", "По методика ДП.ЕД.МТ.1153", "Отчитане електомерите за консумирана ел.енергия-НСЕО ОЕОиСКУ", "Смяна 2"))
        
        # 19. Проверка ТП1, ТП3 (събота седмица 3)
        if saturday_week == 3:
            events.append((current, "🚨 Проверка ТП1, ТП3", "ТП1,ТП3", "Изпробване на охлаждащите вентилатори на 1ТП и 3ТП чрез ръчно включване-НСЕО", "Смяна 2"))
        
        # 20. Измерване стойности по фидери (сряда или събота седмица 3)
        if wednesday_week == 3 or saturday_week == 3:
            events.append((current, "🚨 Измерване стойности по фидери", "По методика ДП.ЕД.МТ.1153", "Измерване стойностите по фидерите за АКС,СБК-2 и ТРЗ/Бюро пропуски-НСЕО ОЕОиСКУ", "Смяна 1"))
            events.append((current, "🚨 Измерване стойности по фидери", "По методика ДП.ЕД.МТ.1153", "Измерване стойностите по фидерите за АКС,СБК-2 и ТРЗ/Бюро пропуски-НСЕО ОЕОиСКУ", "Смяна 2"))
            events.append((current, "🚨 Измерване стойности по фидери", "По методика ДП.ЕД.МТ.1153", "Измерване стойностите по фидерите за АКС,СБК-2 и ТРЗ/Бюро пропуски-НСЕО ОЕОиСКУ", "Смяна 3"))

        current += timedelta(days=1)
    
    return sorted(events, key=lambda x: x[0])

def get_shift_hours(shift):
    """Връща часа за дадена смяна"""
    shift_map = {
        "Смяна 1": 23,
        "Смяна 2": 7,
        "Смяна 3": 15
    }
    return shift_map.get(shift, 0)