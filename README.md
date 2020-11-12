# parental-control-linux
Scripts and programs for screen time and internet access for kids, based on 
https://aananth-linux-notes.blogspot.com/2018/11/parental-controls-in-ubuntu-18.html


## Pre-requisite
sudo permission
iptables
sudo apt install acct  
sudo apt install python3


## Installation
Please run ./install-parental-control.sh script



## Configuration
Edit the /etc/parental-control/parental-control.cfg file as below

```
USER      ACCESS      MO  TU  WE  TH  FR  SA  SU
username  http        0   0   0   0   0   30  30
username  login       30  30  30  60  30  60  60
```
