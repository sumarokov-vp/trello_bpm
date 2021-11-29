def parse_hours(s: str):

    def has_intersections (a, b):
        return len(list(set(a) & set(b)))>0

    def typical_format(s):
        index = s.find(':')
        if index == -1 or index+1 == len(s):
            return False, 0, 0
        else:
            string_before = s[:index]
            string_after = s[index+1:]

            if not(string_before.isdigit()) or not(string_after.isdigit()):
                return False, 0, 0
            else:
                return True, int(string_before), int(string_after)

    def check_pair(a, b):
        if b in hour_set:
            check, hours, minutes = is_hours_digit(a)
            if check:
                return True, hours, minutes

        elif b in minute_set and a.isdigit():
            return True, 0, int(a)

        else:
            return False, 0, 0
    
    def is_hours_digit(string):
        string = string.replace(',', '.')
        try:
            x = float(string)
            if x == int(x):
                return True, int(x), 0
            else:
                h = int(x)
                m = int((x-int(x))*60)
                return True, h, m

        except ValueError:
            return False, 0, 0

    hour_set = ['ч','час','h','hr','hrs','hours', 'часа', 'часов']
    minute_set = ['min', 'minute', 'minutes', 'мин', 'минута', 'минут']
    total_set = ['total', 'всего', 'итого']
    s = s.lower()

    check, h, m = typical_format(s)
    if check:
        return True, h, m

    words = s.split()
    for total in total_set:
        for i in range(len(words)):
            if words[i] == total:
                if i+1 < len(words):
                    check, h, m = typical_format(words[i+1])
                    if check:
                        return check, h, m

                if i+2 < len(words):
                    check, h, m = check_pair(words[i+1], words[i+2])
                    if check:
                        return check, h, m

    for i in range(len(words)):
        word = words[i].rstrip(' ,.:;')
        if i>0:
            previous_word = words[i-1].lower()
        else:
            previous_word = ''

        check, h, m = check_pair(previous_word, word)
        if check:
            return check, h, m

        for item in hour_set:
            i = word.find(item)
            if i>0:
                part_0 = word[:i]

                check, hours, minutes = is_hours_digit(part_0)
                if check:
                    return True, hours, minutes

    
    return False, 0, 0

    
