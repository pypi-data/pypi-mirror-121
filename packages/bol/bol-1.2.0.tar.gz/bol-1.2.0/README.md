Bol.com api connector in python

## install

```bash
pip install bol
```

## Login to the api from your project

```python
import bol
BolShop = bol.Client(client_id='d75*****779', client_secret='AK6****quP')
```

## Example

```python
Python 3.7.4 (default, Oct  4 2019, 06:57:26) 
[GCC 9.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import bol
>>> BolShop = bol.Client(client_id='d75*****779', client_secret='AK6****quP')
logging in
>>> BolShop.
BolShop.client_id      BolShop.client_secret  BolShop.session        BolShop.token          
>>> BolShop._
BolShop._get(     BolShop._login(   BolShop._orders(  BolShop._post(    
>>> BolShop._orders()
{'orders': [{'orderId': '26000000', 'dateTimeOrderPlaced': '2019-11-23T18:59:46+01:00', 'orderItems': [{'orderItemId': '2300004', 'ean': '5000000', 'cancelRequest': False, 'quantity': 1}]}]}
>>> 
>>>
```

## Stability?

It's pretty stable it has been running production for about a year on version `0.1.4`

![Google Analytics](https://www.google-analytics.com/collect?v=1&tid=UA-48206675-1&cid=555&aip=1&t=event&ec=repo&ea=view&dp=gitlab%2Fbol%2FREADME.md&dt=bol)