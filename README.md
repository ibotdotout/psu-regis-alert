[Psu-Regis-Alert](http://alert.im-bot.com) - [Facebook Fanpage](http://fb.me/psuregisalert)
------------

[![Build
Status](https://travis-ci.org/ibotdotout/psu-regis-alert.svg?branch=master)](https://travis-ci.org/ibotdotout/psu-regis-alert)
[![Code
Health](https://landscape.io/github/ibotdotout/psu-regis-alert/master/landscape.svg?style=flat)](https://landscape.io/github/ibotdotout/psu-regis-alert/master)
[![Codacy
Badge](https://www.codacy.com/project/badge/2618f4ead25849a0b23b0b6350ee9b3c)](https://www.codacy.com/app/tkroputa/psu-regis-alert)

Web service helps student  who want enroll course which full by send email when someone withdraw.
Monitoring by scraping web and using Regex to extract seats available,
written in Python, MongoDB that contain in Docker Container.


เผื่อใครลงทะเบียนไม่ทัน   
แล้วต้องมาคอยเช็คดูว่ามีคนถอนออกไปบ้างไหม  
ลองใช้เว็บนี้ดูนะ  
http://al-bot.com  
ระบบจะคอยเช็คให้ทุกๆ 5 นาที  
ถ้ามียังมีพื้นที่ว่างให้สามารถลงทะเบียนได้  
จะมี Mail/Line แจ้งไปให้ลงทะเบียน  

เงื่อนไข:  
1. ถ้าส่งแจ้งไปแล้ว ข้อมูลจะถูกลบออกนะครับ  
ต้องมา add ข้อมูลใหม่ ถ้าลงไม่ทัน  
2. ใครมีคำแนะนำไร โพสไว้ได้เลย  
