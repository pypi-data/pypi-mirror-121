'''
Integer In Words Lister
This module returns numbers to a list of words

Author: Amin Morakabi Sabet
'''

import humanize


class NumericLister:
    def __init__(self, number):
        if type(number) != int or number < 0:
            raise TypeError("Only positive integers are allowed")

        self.number = number
        self.part_digits = humanize.intcomma(self.number).split(',')

        self.and_text = 'and'

    def __tens_text(self, number):
        switcher = {
            11: '11',
            12: '12',
            13: '13',
            14: '14',
            15: '15',
            16: '16',
            17: '17',
            18: '18',
            19: '19',
            1: '10',
            2: '20',
            3: '30',
            4: '40',
            5: '50',
            6: '60',
            7: '70',
            8: '80',
            9: '90',
        }

        return switcher.get(int(number), 'wrong')

    def __hundreds_text(self, number):
        switcher = {
            1: '100',
            2: '200',
            3: '300',
            4: '400',
            5: '500',
            6: '600',
            7: '700',
            8: '800',
            9: '900',
        }

        return switcher.get(int(number), 'wrong')

    def __digits_2_3(self, part):
        list_text = []
        int_part = int(part)
        if int_part > 10 and int_part < 20:
            list_text.append(self.__tens_text(part))
        if int_part > 19 and part[1] != '0':
            list_text.append(self.__tens_text(part[0]))
            list_text.append(self.and_text)
            list_text.append(part[1])
        if part[1] == '0':
            list_text.append(self.__tens_text(part[0]))

        return list_text
    
    def calculate(self):
        part_name = {
            2: 'thousand',
            3: 'million',
            4: 'milliard'
        }

        list_text = []
        part_name_index = len(self.part_digits)
        for part in self.part_digits:
            part = str(int(part))

            if len(part) == 1 and int(part) > 0:
                list_text.append(part)

            if len(part) == 2:
                list_text.extend(self.__digits_2_3(part))

            if len(part) == 3:
                list_text.append(self.__hundreds_text(part[0]))
                part_1_2 = int('{}{}'.format(part[1], part[2]))
                if part_1_2 > 0 and part_1_2 < 10:
                    list_text.append(self.and_text)
                    list_text.extend(str(part_1_2))
                elif part_1_2 > 9:
                    list_text.append(self.and_text)
                    list_text.extend(self.__digits_2_3(str(part_1_2)))

            if part_name_index > 1 and int(part) > 0:
                list_text.append(part_name[part_name_index])
                list_text.append(self.and_text)

            part_name_index = part_name_index - 1

        
        if list_text[len(list_text) - 1] == self.and_text:
            list_text.pop()
        return list_text
