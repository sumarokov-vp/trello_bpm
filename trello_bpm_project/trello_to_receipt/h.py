def test(s, t: str):

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
            else:
                return is_divided_format(a)

        elif b in minute_set and a.isdigit():
            return True, 0, int(a)

        else:
            return False, 0, 0
    
    def is_divided_format(s: str):
        d_position = s.find(':')
        part_1 = s[:d_position]
        part_2 = s[d_position+1:]
        check, h, x = is_hours_digit(part_1)
        if check:
            check, x, m = is_minutes_digit(part_2)
            if check: return True, h, m
            else: return False, 0, 0
        else: return False, 0, 0


    
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

    def is_minutes_digit(string):
        string = string.replace(',', '.')
        try:
            x = int(string)
            return True, 0, int(x)

        except ValueError:
            return False, 0, 0

    hour_set = ['ч','час','h','hr','hrs','hours', 'часа', 'часов']
    minute_set = ['min', 'minute', 'minutes', 'мин', 'минута', 'минут']
    total_set = ['total', 'всего', 'итого']
    s = s.lower()

    check, h, m = typical_format(s)
    return check_pair(s, t)

    
if __name__ == '__main__':
    print(test('0:45','h'))
