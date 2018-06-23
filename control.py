#!/usr/bin/python
# -*- coding: iso-8859-9 -*-
import sys
import os
import glob
import RPi.GPIO as GPIO
import time
import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

GPIO.setmode (GPIO.BCM)

#Kullanilacak Anahtar icin Pin Numaralari

pinListesi = [17, 27, 22, 18]

#Uyarilari Gosterme

GPIO.setwarnings(False)

#Anahtarlari Sifirla
#if pinListesi == (GPIO.HIGH):
#    GPIO.output(pinListesi, GPIO.LOW)
#else:
#    pinListesi ==(GPIO.LOW)

# Sensorun tanimlanmasi

sensorler = glob.glob("/sys/bus/w1/devices/28*/w1_slave")

for Termometre in sensorler:
  tfile = open(Termometre)
  text = tfile.read()
  tfile.close()
  secondline = text.split("\n")[1]
  temperaturedata = secondline.split(" ")[9]
  sicaklik = float(temperaturedata[2:])/1000

#Bekleme saniye cinsinden

bekle = 2

#pinler

for i in pinListesi: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)
    
#Basliyoruz
MinDeger = input("En düşük sıcaklığı belirleyiniz:")
MaxDeger = input("En yüksek sıcaklığı belirleyiniz:")

MinOrtamSicakligi = MinDeger
MaxOrtamSicakligi = MaxDeger

if sicaklik < MinOrtamSicakligi:
	GPIO.output(17, GPIO.LOW)
	GPIO.output(27, GPIO.LOW)
	print 'Rezistans ve motor çalıştırıldı.', 'Sıcaklık', sicaklik, 'C derece.'
else:
	GPIO.output(17, GPIO.HIGH)
	GPIO.output(27, GPIO.HIGH)
	print 'Rezistans ve motor durduruldu', 'Sıcaklık', sicaklik, 'C derece.'
if sicaklik >= MaxOrtamSicakligi:
	GPIO.output(22, GPIO.LOW)
	GPIO.output(18, GPIO.LOW)
	print "Soğutucu ve motor çalıştırıldı", "Sıcaklık", sicaklik, "C derece."
else:
	GPIO.output(22, GPIO.HIGH)
	GPIO.output(18, GPIO.HIGH)
	print "Soğutucu ve motor durduruldu", "Sıcaklık", sicaklik, "C derece."

#Sonuc Ekrani
while True:
	time.sleep(bekle)
