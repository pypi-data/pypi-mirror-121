# Iranian Bills Validation
#### This module checks and validates your bills and returns the required information

## Dependencies
#### To use this module you need to install [jdatetime](https://pypi.org/project/jdatetime/) and [python](https://www.python.org/)

## Install

    pip install iranian-bills-validation

## Usage
```python
from IranianBillsValidation.Bill import Receipt

receipt = Receipt('9985235404124', '0000880000568')
if receipt.billing_isvalid():
    print(receipt.billing_info())

if receipt.payment_isvalid():
    print(receipt.payment_info())

print(receipt.result())
```
## Output
```json
{"billing_service": "Electricity", "billing_companycode": "041", "billing_filecode": "99852354"}

{"payment_periodcode": "05", "payment_yearcode": "1400", "payment_amount": "8800000"}

{"billing": {"is_valid": true, "billing_service": "Electricity", "billing_companycode": "041", "billing_filecode": "99852354"}, "payment": {"is_valid": true, "payment_periodcode": "05", "payment_yearcode": "1400", "payment_amount": "8800000"}}
```

## اعتبارسنجی قبوض ایرانی
##### این ماژول قبض های شما را بررسی و اعتبارسنجی می کند و اطلاعات مورد نیاز را برمی گرداند
