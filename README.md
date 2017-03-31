![](fig/Smartenit_Main_Color_Positive.png?raw=true)

Making your world smarter and greener
# World of Smartenit IoT Workshop

This repository is a **[Smartenit Inc.][smt-site]** workshop to get you involved in the world of the IoT company services. Please enjoy it!
*Copyright Compacta International, Ltd 2017. All rights reserved*

This workshop is part of a series of workshops which we want to introduce you to our robust ecosystem! [Smartenit Ecosystem Documentation](https://docs.smartenit.io/)

This workshop is focused in the part of the Zigbee network and the usage of the **Smartenit** Zigbee controllers using the [Serial API](docs/ZBPCID_API.pdf) (a.k.a Serapi). We will use a USB Zigbee Coordinator and a Zigbee device with OnOff Cluster support to control it and read its attributes.

1. This workshop is written in python language, please follow the instructions bellow based on your Operating System. Please install Python version **2.7**

    Windows or Mac OS:

    [Python for windows and Mac OS installer][py-installer]

    Ubuntu/Debian:

     `sudo apt-get install python python-pip`

    Other OS:
 
    [Visit Python Page][py-page-installer]

2. Once the Python interpreter has been installed, clone the workshop repository through a web page using these instructions [Cloning a GIT repository][git-cloning] or from a terminal using the command:

    `git clone https://github.com/Smartenit/iot-workshop-smartenit.git`
 
    Optionally, you can download the repository as a ZIP file at the  `Downloads` menu.
In case you are interested in making a contribution for this workshop, follow the instructions in [contributions guidelines](#contributions-guidelines)

3. Once you are done cloning or downloading the repository, change your current path to the workshop folder, there you will be able to install the repository requirements using the Python package installer `pip`. In case you need to install this tool please visit [Installing pip][pip-installing]:

    `pip install -r requirements.txt`

    Note: Debian-based OS would require to run this command with  `sudo` privilegies.

    Note: Windows installer may not add the pip to the PATH automatically, you would use it giving the full path `C:\Python27\Scripts\pip.exe`

4. We recommend to use [TkInter][tkinter-intro] to generate some simple plots complemented by `matplotlib`. In order to install TkInter follow these instructions based on your operative system.

    Windows:
    
    Python installer for windows includes TKInter, you are done if you use this Operating System
    
    Other OS:
    
    Follow this guide [How to install TKInter][tkinter-install]

5. Finally run our checker script which actually does not do anything but trying to import the dependencies and will let you know if all dependencies are met.

    `python check.py`

**Welcome to Smartenit IoT workshop!**
    
## Reading your Coordinator's MAC
Smartenit Coordinator allows you to turn any controller with a USB port such as a PC, media storage server, Raspberry Pi, or Beagle Bone board into a home automation powerhouse by enabling them with a ZigBee network interface. The device brings management of a ZigBee network to your controller to create a powerful gateway that allows your devices to communicate with each other and your phone, tablet, or web browser.

![](fig/radios.jpg?raw=true)

In this workshop we are assuming you are using your PC, but you can use whatever you want!

The coordinator is part of the Zigbee network, so our first challenge for you is to request the USB dongle MAC!

You don't even know where to start?
Identify the request you should use to read the coordinator MAC in our [Serapi document](docs/ZBPCID_API.pdf).

You got this? Ok, now identify how to execute that request using the python library to get the Zigbee MAC of the coordinator. [Use the Python SDK documentation](serapi/README.md)

## Reading the short address for the given device
Most of the requests to devices in the Zigbee network requires the short address identifier which identifies each device in the network with its MAC. You already have a basic Zigbee network, don't you? So let's get the short address of the device in your network!

*Tip:* Look at the device and get its MAC Address.

*Tip:* Unpowered devices are unreachable, getting their short address is not possible.

*Tip:* You do not have a Zigbee network yet? Let's try an open join request!

## Sending a Cluster Command to the given device
Once you know the short address of your device, let's implement a simple interface where you can send ON and OFF commands to the device!

 ![](fig/on_off_controls.png?raw=true)

This base user interface is available at [gui/base.py](gui/base.py)

Also, read the OnOff cluster information in the [Zigbee Cluster library specification.](docs/zcl-1.0-6.pdf)

## Reading an attribute from given device
There are some methods to configure the device to report an attribute after it has changed, but in this practice we will read the OnOff attribute manually. Finish the above application reading the attribute once the method has been sent.

Finally, read the current power consumption that the device is measuring right now! Easy? So let's plot the retrieved data in a widget!

Is [there](docs/zcl-1.0-6.pdf) a cluster to read that information?

 ![](fig/plot_example.png?raw=true)

This base plot widget is available at [gui/plot-example.py](gui/plot-example.py)

## Connecting to your gateway using OAuth 2.0
This section is still in progress, hopefully you will find the guidelines the next time you visit this workshop page!

## Contributions Guidelines
* Report issues using Github [issue menu](https://help.github.com/articles/creating-an-issue/)
* Upload your changes using Github [pull requests](https://help.github.com/articles/creating-a-pull-request/)

If you would like to test our products or design a solution based on them please [mail us][contact].

[contact]: http://smartenit.com/contact_us/
[smt-site]: http://smartenit.com/
[git-cloning]: https://help.github.com/articles/cloning-a-repository/
[py-installer]: https://www.python.org/downloads/release/python-2713/
[py-page-installer]: https://wiki.python.org/moin/Python2orPython3
[pip-installing]: https://pip.pypa.io/en/stable/installing/
[tkinter-intro]: https://docs.python.org/2/library/tkinter.html
[tkinter-install]: http://tkinter.unpythonic.net/wiki/How_to_install_Tkinter
