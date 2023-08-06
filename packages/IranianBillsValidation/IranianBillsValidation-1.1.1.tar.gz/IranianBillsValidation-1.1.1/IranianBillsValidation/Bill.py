'''
Iranian Bills Validation
This module checks and validates your bills and returns the required information

Author: Amin Morakabi Sabet
'''

import json
import jdatetime


class Receipt:
    def __init__(self, billing_id, payment_code):
        self.billing_id = billing_id
        self.payment_code = str(int(payment_code))

        self.__set_params()

    def __set_params(self):
        self.billing_length = len(self.billing_id)
        self.payment_length = len(self.payment_code)

    def __billing_controldigit(self):
        x_num = 2
        plus_numbers = 0
        for i in range(self.billing_length-2, -1, -1):
            x_num_x = 0
            if x_num > 7:
                x_num = 2

            x_num_x = int(self.billing_id[i]) * x_num
            plus_numbers = plus_numbers + x_num_x

            x_num = x_num + 1

        module_result = plus_numbers % 11
        if module_result == 0 or module_result == 1:
            return 0

        control_digit = 11 - (module_result % 11)
        return control_digit

    def __billing_service(self):
        service_code = int(self.billing_id[self.billing_length-2])
        check_service = {
            1: 'Water',
            2: 'Electricity',
            3: 'Gas',
            4: 'Telephone',
            5: 'Mobile',
            6: 'Municipality',
            7: 'Tax',
            8: 'Driving offenses',
            9: 'Driving offenses',
        }

        return check_service.get(service_code, '')

    def __billing_companycode(self):
        company_code = self.billing_id[
            self.billing_length-5:self.billing_length-2]

        return company_code

    def __billing_filecode(self):
        file_code = self.billing_id[:self.billing_length-5]

        return file_code

    def billing_isvalid(self):
        if int(self.billing_id[self.billing_length - 1]) == self.__billing_controldigit():
            return True

        return False

    def billing_info(self):
        information = {
            'billing_service': self.__billing_service(),
            'billing_companycode': self.__billing_companycode(),
            'billing_filecode': self.__billing_filecode(),
        }

        return json.dumps(information)

    def __payment_controldigit1(self):
        x_num = 2
        plus_numbers = 0
        for i in range(self.payment_length-3, -1, -1):
            if x_num > 7:
                x_num = 2

            x_num_x = int(self.payment_code[i]) * x_num
            plus_numbers = plus_numbers + x_num_x

            x_num = x_num + 1

        module_result = plus_numbers % 11
        if module_result == 0 or module_result == 1:
            return 0

        control_digit = 11 - (module_result % 11)
        return control_digit

    def __payment_controldigit2(self):
        billing_id = self.billing_id[:self.billing_length]
        if billing_id[0] == 0:
            billing_id = billing_id[1:self.billing_length]

        payment_code = self.payment_code[:self.payment_length-1]
        if payment_code[0] == 0:
            payment_code = payment_code[1:self.payment_length]

        final_code = '{0}{1}'.format(billing_id, payment_code)
        final_code_length = len(final_code)

        x_num = 2
        plus_numbers = 0
        for i in range(final_code_length-1, -1, -1):
            x_num_x = 0
            if x_num > 7:
                x_num = 2

            x_num_x = int(final_code[i]) * x_num
            plus_numbers = plus_numbers + x_num_x

            x_num = x_num + 1

        module_result = plus_numbers % 11
        if module_result == 0 or module_result == 1:
            return 0

        control_digit = 11 - (module_result % 11)
        return control_digit

    def __payment_periodcode(self):
        period_code = self.payment_code[
            self.payment_length-4:self.payment_length-2]

        return period_code

    def __payment_yearcode(self):
        year_code = self.payment_code[
            self.payment_length-5:self.payment_length-4]

        return str(int(year_code) + jdatetime.date.today().year)

    def __payment_amount(self):
        amount = int('{}000'.format(self.payment_code[:self.payment_length-5]))

        return str(amount)

    def payment_isvalid(self):
        if int(self.payment_code[self.payment_length - 2]) == self.__payment_controldigit1() and int(self.payment_code[self.payment_length - 1]) == self.__payment_controldigit2():
            return True

        return False

    def payment_info(self):
        information = {
            'payment_periodcode': self.__payment_periodcode(),
            'payment_yearcode': self.__payment_yearcode(),
            'payment_amount': self.__payment_amount(),
        }

        return json.dumps(information)

    def result(self):
        billing_info = {'is_valid': False}
        if self.billing_isvalid():
            billing_info = {'is_valid': True}
            billing_info.update(json.loads(self.billing_info()))

        payment_info = {'is_valid': False}
        if self.payment_isvalid():
            payment_info = {'is_valid': True}
            payment_info.update(json.loads(self.payment_info()))

        return json.dumps({'billing': billing_info, 'payment': payment_info})
