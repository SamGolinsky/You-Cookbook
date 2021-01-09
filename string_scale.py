from fractions import Fraction

valid_frac = ['1/4', '3/4', '1/3', '2/3', '1/2']


def __scale_fraction(fraction, multiplier):
    split_frac = fraction.split('/')
    numerator = int(split_frac[0])
    denominator = int(split_frac[1])

    scaled_decimal_frac = (numerator / denominator) * multiplier
    integer = str(int(scaled_decimal_frac))
    fraction = str(Fraction(scaled_decimal_frac % 1))
    return integer, fraction


def __scale_compound(cnum, multiplier):
    split_comp = cnum.split()
    integer = int(split_comp[0])
    fraction = split_comp[1]

    scaled_frac_int, scaled_frac_frac = __scale_fraction(fraction, multiplier)

    if (integer * multiplier) % 1 == 0:
        integer = integer * multiplier + int(scaled_frac_int)
        remainder = 0
    else:
        temp_int = integer * multiplier
        integer = int(temp_int) + int(scaled_frac_int)
        remainder = temp_int % 1

    if scaled_frac_frac != '0':
        split_scaled_frac_frac = scaled_frac_frac.split('/')
        numerator, denominator = int(split_scaled_frac_frac[0]), int(split_scaled_frac_frac[1])
        decimal_frac = numerator / denominator + remainder
    else:
        decimal_frac = 0
    integer = integer + int(decimal_frac)
    fraction = str(Fraction(decimal_frac % 1))

    return str(int(integer)), fraction


def __appropriate_frac(integer, fraction, unit):
    if (unit == 'cups' or unit == 'cup') and Fraction(fraction) < 0.25 and fraction != '0' and integer == '0':
        decimal_frac = Fraction(fraction)
        tablespoon_amount = 16 * decimal_frac
        integer = str(int(tablespoon_amount))
        fraction = str(Fraction(tablespoon_amount % 1))
        unit = 'tablespoon'
    elif (unit == 'tablespoons' or unit == 'tablespoon' or unit == 'tbs' or unit == 'tbsp') \
            and Fraction(fraction) < 1 and fraction != '0' and integer == '0':
        decimal_frac = Fraction(fraction)
        teaspoon_amount = 3 * decimal_frac
        integer = str(int(teaspoon_amount))
        fraction = str(Fraction(teaspoon_amount % 1))
        unit = 'teaspoon'

    if fraction not in valid_frac and fraction != '0':
        numerator, denominator = int(fraction.split('/')[0]), int(fraction.split('/')[1])
        if denominator % 2 == 0:
            divider = denominator / 4
            numerator = int(round(numerator / divider))
            denominator = int(denominator / divider)
            if numerator == 0:
                numerator = 1
        elif denominator % 2 == 1:
            divider = denominator / 9
            numerator = int(round(numerator / divider))
            denominator = int(denominator / divider)
            if numerator == 0:
                numerator = 1

        if numerator / denominator == 1:
            integer = str(int(integer) + 1)
            fraction = '0'
        else:
            fraction = f'{numerator}/{denominator}'
            if fraction == '2/4':
                fraction = '1/2'

    return integer, fraction, unit


def fam_scale(fam_data):
    list_scales = []
    i = 1
    while fam_data[i] != '|\n':
        list_scales.append(int(fam_data[i].split(';')[1]))
        i += 1
    fam_portion_avg = 0
    for i in list_scales:
        if i == 1:
            fam_portion_avg += 0.5
        elif i == 2:
            fam_portion_avg += 1
        elif i == 3:
            fam_portion_avg += 1.5
        elif i == 4:
            fam_portion_avg += 3
    multiplier = fam_portion_avg/len(list_scales)

    if abs(multiplier - round(multiplier * 4) / 4) < abs(multiplier - round(multiplier * 3) / 3):
        return round(multiplier*4)/4
    else:
        return round(multiplier*3)/3


def scale(num, multiplier, unit):
    if num == '':
        return '', ''
    if unit == '':
        if round(int(num) * multiplier) == 0:
            return 1, unit
        else:
            return str(int(round(int(num) * multiplier))), unit

    if unit in ['ml', 'l', 'dl', 'mg', 'g', 'kg', 'mm', 'cm', 'm', 'fluid ounce',
                'fluid ounces', 'fl oz', 'ounce', 'ounces',
                'oz']:
        return str(float(num) * multiplier), unit

    is_fraction = False
    is_compound = False
    for char in num:
        if ord(char) == 32:
            is_compound = True
        elif ord(char) == 47:
            is_fraction = True

    if is_compound:
        integer, fraction = __scale_compound(num, multiplier)
        integer, fraction, unit = __appropriate_frac(integer, fraction, unit)
        if integer != '0' and fraction != '0':
            return integer + ' ' + fraction, unit
        elif integer != '0' and fraction == '0':
            return integer, unit
        elif integer == '0' and fraction != '0':
            return fraction, unit
        else:
            return ' ', unit
    if is_fraction:
        integer, fraction = __scale_fraction(num, multiplier)
        integer, fraction, unit = __appropriate_frac(integer, fraction, unit)
        if integer != '0' and fraction != '0':
            return integer + ' ' + fraction, unit
        elif integer != '0' and fraction == '0':
            return integer, unit
        elif integer == '0' and fraction != '0':
            return fraction, unit
        else:
            return ' ', unit

    scaled_num_integer = str(int(int(num) * multiplier))
    scaled_num_fraction = str(Fraction((int(num) * multiplier) % 1))
    scaled_num_integer, scaled_num_fraction, unit = __appropriate_frac(scaled_num_integer, scaled_num_fraction, unit)

    if scaled_num_integer != '0' and scaled_num_fraction != '0':
        return scaled_num_integer + ' ' + scaled_num_fraction, unit
    elif scaled_num_integer != '0' and scaled_num_fraction == '0':
        return scaled_num_integer, unit
    elif scaled_num_integer == '0' and scaled_num_fraction != '0':
        return scaled_num_fraction, unit
    else:
        return ' ', unit
