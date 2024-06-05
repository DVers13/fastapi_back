def time_to_deadline(lab):
    deadline = lab.deadline
    loading_time = lab.loading_time
    return (deadline - loading_time).total_seconds()

def loading_hour(lab):
    loading_time = lab.loading_time
    return loading_time.hour

def sort_labs(student_labs):
    sort_labs = student_labs.copy()
    sort_labs.sort(key=lambda lab: (
    -time_to_deadline(lab),  # Сначала сортируем по времени до дедлайна (чем больше, тем лучше)
    lab.count_try,  # Затем сортируем по количеству попыток (чем меньше, тем лучше)
    loading_hour(lab),  # Затем сортируем по часу загрузки (чем раньше, тем лучше)
    lab.laboratory_name  # Наконец, сортируем по названию лабораторной работы для группировки одинаковых работ
    ))

    return sort_labs