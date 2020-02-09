#! /usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import ifilter
import logging
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

UNIDADES = (
    '',
    'UN ',
    'DOS ',
    'TRES ',
    'CUATRO ',
    'CINCO ',
    'SEIS ',
    'SIETE ',
    'OCHO ',
    'NUEVE ',
    'DIEZ ',
    'ONCE ',
    'DOCE ',
    'TRECE ',
    'CATORCE ',
    'QUINCE ',
    'DIECISEIS ',
    'DIECISIETE ',
    'DIECIOCHO ',
    'DIECINUEVE ',
    'VEINTE '
)
DECENAS = (
    'VENTI',
    'TREINTA ',
    'CUARENTA ',
    'CINCUENTA ',
    'SESENTA ',
    'SETENTA ',
    'OCHENTA ',
    'NOVENTA ',
    'CIEN '
)
CENTENAS = (
    'CIENTO ',
    'DOSCIENTOS ',
    'TRESCIENTOS ',
    'CUATROCIENTOS ',
    'QUINIENTOS ',
    'SEISCIENTOS ',
    'SETECIENTOS ',
    'OCHOCIENTOS ',
    'NOVECIENTOS '
)
MONEDAS = (
    {'country': 'Colombia', 'currency': 'COP', 'singular': 'PESO COLOMBIANO', 'plural': 'PESOS COLOMBIANOS', 'symbol': '$'},
    {'country': 'Estados Unidos', 'currency': 'USD', 'singular': 'DOLAR', 'plural': 'DOLARES', 'symbol': 'US$'},
    {'country': 'El Salvador', 'currency': 'USD', 'singular': 'DOLAR', 'plural': 'DOLARES', 'symbol': 'US$'},
    {'country': 'Europa', 'currency': 'EUR', 'singular': 'EURO', 'plural': 'EUROS', 'symbol': '?'},
    {'country': 'M?xico', 'currency': 'MXN', 'singular': 'PESO MEXICANO', 'plural': 'PESOS MEXICANOS', 'symbol': '$'},
    {'country': 'Per?', 'currency': 'PEN', 'singular': 'NUEVO SOL', 'plural': 'NUEVOS SOLES', 'symbol': 'S/.'},
    {'country': 'Reino Unido', 'currency': 'GBP', 'singular': 'LIBRA', 'plural': 'LIBRAS', 'symbol': '?'}
)
# Para definir la moneda me estoy basando en los c?digo que establece el ISO 4217
# Decid? poner las variables en ingl?s, porque es m?s sencillo de ubicarlas sin importar el pa?s
# Si, ya s? que Europa no es un pa?s, pero no se me ocurri? un nombre mejor para la clave.
#Esto se usa primero el numero luego la moneda pj. amount_to_text(400245.3,"USD")
def amount_to_text(number,currency=None):
    currency="USD"
    if currency != None:
        try:
            moneda = ifilter(lambda x: x['currency'] == currency, MONEDAS).next()
            if number < 2:
                moneda = moneda['singular']
            else:
                moneda = moneda['plural']
        except:
            return "Tipo de moneda inv?lida"
    else:
        moneda = ""
    """Converts a number into string representation"""
    converted = ''
    number = float(number)
    decimal_part = ("%0.2f" % number)[-2:]
    number = int(number)
    
    if not (0 < number < 999999999):
        if number != 0:
            return 'No es posible convertir el numero a letras'
        else:
            converted = 'Cero '+moneda+' con 00/100 Centavos'
            return converted.title()
    
    number_str = str(number).zfill(9)
    millones = number_str[:3]
    miles = number_str[3:6]
    cientos = number_str[6:]
    if(millones):
        if(millones == '001'):
            converted += 'UN MILLON '
        elif(int(millones) > 0):
            converted += '%sMILLONES ' % __convert_group(millones)
    if(miles):
        if(miles == '001'):
            converted += 'MIL '
        elif(int(miles) > 0):
            converted += '%sMIL ' % __convert_group(miles)
    if(cientos):
        if(cientos == '001'):
            converted += 'UN '
        elif(int(cientos) > 0):
            converted += '%s ' % __convert_group(cientos)
    converted += moneda+" con "+decimal_part+"/100 Centavos"
    return converted.title()
def __convert_group(n):
    """Turn each group of numbers into letters"""
    output = ''
    if(n == '100'):
        output = "CIEN "
    elif(n[0] != '0'):
        output = CENTENAS[int(n[0]) - 1]
    k = int(n[1:])
    if(k <= 20):
        output += UNIDADES[k]
    else:
        if((k > 30) & (n[2] != '0')):
            output += '%sY %s' % (DECENAS[int(n[1]) - 2], UNIDADES[int(n[2])])
        else:
            output += '%s%s' % (DECENAS[int(n[1]) - 2], UNIDADES[int(n[2])])
    return output
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:  