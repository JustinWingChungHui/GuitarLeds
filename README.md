WLED Guitar strap and Amplifier
===============================
![demo](docs/demo.gif)

Synced LED guitar strap and amplifier with changes triggered by pressing a guitar FX pedal.


LED Strip
---------

The main requirement here was for everything to be **AS OBNOXIOUSLY BRIGHT AS POSSIBLE!!! 🤘🤘🤘🤘** 

In guitar world it is universally known that

**Loud = Gooder** so by that logic **Brighter = Gooder**

As such the specs for the LED strip are:
 - SK6812
 - 12v
 - RGBNW
 - 144 LEDs per metre
 - IP67

There many types of LEDs.  SK6812 work with WLED, are individually addressable and have a separate white LED.  The white LEDs really pop, so its important to get an LED strip with a separate white channel.  

You get the option of: 
 - RGBCW (RGB Cool white)
 - RGBWW (RGB Warm White)
 - RGBNW (RGB Neutral White)

What you see in the picture is neutral white.  I would avoid warm white as  this is normally for home lighting which needs to have more subtle tones. 

There are 5v, 12v and 24v variations.  I found 12v is bright and its fairly easy to get portable 12v battery packs.

144 LEDs per metre is currently the most number of LEDs that was available.  The strips are available in 30 and 60 LEDs per metre, and they look very disappointing compared to 144.

IP67 is a standard for water resistance.  In reality, you will not be submerging your guitar and amp in water.  But the IP67 light strip came in a transparent sleeve which made it easy to sow onto the guitar strap with fishing line, and so I would recommend getting this.

WLED Controller
---------------

[WLED](https://github.com/wled/WLED) is an open source firmware for ESP32 microcontrollers to control addressable LEDs.  Open source means no vendor tie in.  There are a lot of LED controllers on the market that have apps to control the lighting.  Unfortunately as a lot of them are not open source, it menas that if a vendor pulls their app or goes out of business, you have an LED which you can't control.

I went for a Gledopto ESP32 controller with built in microphone and 12v barrel jack input
![Gledopto](docs/gledopto.png)

But the beauty of open source, is that any WLED compatible 12v controller will work.

Note I found that loud **rock🤘** music was generally too loud & noisy for the built in microphone to do anything useful with the lights.  So I mostly used sequences that weren't sound activated.  So you might decide to go for a controller without a microphone.

Battery
-------

