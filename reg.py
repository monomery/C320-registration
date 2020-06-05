#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pexpect
import textfsm
import time
from datetime import date

user = ''
passwd = ''
switch_ip = sys.argv[1]
port = 22
fsm_unc = 'unc.fsm'
fsm_rlo = 'rlo.fsm'
type_onu = 'ONU_1G'
interface = sys.argv[2]
time_string = time.ctime()

def rlo_ont_def():
    p.sendline('show gpon olt config ' + interface +'\n')
    p.expect('gpon')
    p.expect('#')
    rlo = p.before
    f = open(fsm_rlo)
    re_table = textfsm.TextFSM(f)
    ont_count_t = re_table.ParseText(rlo)
    ont = str(ont_count_t[0][0])
    ont = str(int(ont) + 1)
    print(time_string + ' ONU Serial: ' + serial)
    print(time_string + ' Next ONU on Interface '+ interface + ': ' + ont)
    return ont
def reg_def():
    p.sendline('config t')
    p.expect('#')
    p.sendline('interface ' + interface)
    p.expect('#')
    p.sendline('onu ' + ont + ' type ' + type_onu + ' sn ' + serial)
    p.expect('#')
    p.sendline('onu ' + ont + ' profile line 1 remote ' + remote_profile)
    p.expect('#')
    p.sendline('exit')
    p.expect('#')
    p.sendline('exit')
    p.expect('#')
    p.sendline('write')
    p.expect('#')
p = pexpect.spawn('telnet %s' % switch_ip, timeout=2)
output = ''
p.expect(['Username'])
p.sendline(user)
p.expect(['Password:'])
p.sendline(passwd)
p.expect('#')
p.sendline('show gpon onu unc\n')
unc_status = p.expect(['OnuIndex','%Code 32310-GPONSRV : No related information to show.'])

if unc_status == 1:
    print(time_string + ' No unconfigured ONTs')
if unc_status == 0:
    p.expect('#')
    print(time_string + ' Unconfigured ONTs avaliable')
    unc_onts = p.before
    f = open(fsm_unc)
    re_table = textfsm.TextFSM(f)
    unc_onts_table = re_table.ParseText(unc_onts)
    interface_onu = unc_onts_table[0][0]
    interface = interface_onu.replace('onu', 'olt')
    serial = unc_onts_table[0][1]
    ont = rlo_ont_def()
    remote_profile = str(int(ont) + 100)
    reg_def()
p.sendline('logout')
p.close()

