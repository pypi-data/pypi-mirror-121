import os, sys, time
sys.path.append('/afs/ipp/aug/ads-diags/common/python/lib')
import numpy as np
import sfread

import dd_20200525 as ddw

sf = ddw.shotfile()

diag = 'EQH'
sig = 'PFM'
nshot = 37485

t1 = time.time()    
eqh = sfread.SFREAD(nshot, diag, ed=1)
pfm1 = eqh.getobject(sig)
ssq = eqh.getobject('SSQnam')

t2 = time.time()

if sf.Open(diag, nshot, edition=1):
    pfm2 = sf.GetSignal(sig)
    sf.Close()

t3 = time.time()

print(t3 - t2, t2 - t1)
print(pfm2[:, 0, -1])
print(pfm1[:, 0, -1])
print(eqh.get_rel_names(sig))
finfo = eqh.getobject('INFOFILE')
#print(b''.join(finfo))

cez = sfread.SFREAD(nshot, 'CEZ', ed=1)
tim = cez.gettimebase('Ti')
ti_cez = cez.getobject('Ti')
area1 = cez.getareabase('Ti')
area2 = cez.getareabase('z_time')
print(tim)
ti2 = 3*ti_cez
print(ti2.phys_unit)

tth = sfread.SFREAD(nshot, 'TTH', ed=0)
laws = tth.getparset('scal_par')
g_gw = tth.getparset('G_gw_par')
print(laws['descript'])
print(g_gw['G_H_exp'])

ssqnames = []
for jssq in range(ssq.shape[1]):
    tmp = b''.join(ssq[:, jssq]).strip()
    lbl = tmp.decode('utf8')
    if lbl.strip() != '':
        if lbl not in ssqnames: # avoid double names
            ssqnames.append(lbl)
print(ssqnames)

tra = sfread.SFREAD(37712, 'TRA', exp='git')
ti = tra.getobject('TI')
print(ti[0, :])

# see ../dd/dd_bpd.py
diag = 'BPD'
sig = 'TPradtot'
nshot = 28053
bpd = sfread.SFREAD(nshot, diag)
timb = bpd.gettimebase(sig)
print(timb)

# see ../dd/dd_dcn.py

diag = 'DCN'
nshot = 34954
tb = 'T-ADC-FA'
sig = 'H-0'
dcn = sfread.SFREAD(nshot, diag)
tdcn = dcn.gettimebase(tb)
h1 = dcn.getobject(sig)
cal = dcn.getparset('C000H-1')
print( cal['MULTIA00'], cal['MULTIA01'])
h1cal = dcn.getobject(sig, cal=True) 
print(h1[:100])
print(h1cal[0:100])
print(h1cal.phys_unit)

diag = 'RMC'
tb = 'TIME-AD0'
rmc = sfread.SFREAD(nshot, diag, ed=1)
dev = rmc.getdevice('TDC-Sio0')
trmc = rmc.gettimebase(tb)
print(trmc[:10], trmc[-10:])

ts06 = sfread.get_ts06(nshot)
print(dev['TS06'] - ts06)

nshot = sfread.getlastshot()
print('Last Shot', nshot)

import matplotlib.pylab as plt
gc_r, gc_z = sfread.get_gc()
#for key in gc_r.keys():
#    plt.plot(gc_r[key], gc_z[key], 'b-')
#plt.show()
print('IDA')
ida = sfread.SFREAD(29761, 'IDA')
rhop = ida.getobject('rhop')
print(rhop.shape)
print(rhop[:, 0])
print(rhop.phys_unit)
print(area1.phys_unit)
print(area1.T[0, :])
print(rhop.size_x, rhop.size_y, rhop.size_z)
print(area1.size_x, area1.size_y, area1.size_z)

cez2 = sfread.SFREAD(99761, 'CEZ')
print('Hey')

tot = sfread.SFREAD(28053, 'TOT', ed=0)
print(tot.getlist())

jou = sfread.SFREAD(38384, 'JOU')
ps_nbi = jou.getparset('ICRH')
print(ps_nbi)

end = sfread.SFREAD(28550, 'END')
tb = end.getobject('T-LM_END') # Type PPG_prog
print('END timebase, type PPG_prog, shot:', end.shot)
print(tb[:10])
print(tb[-10:])

end = sfread.SFREAD(38384, 'END')
tb = end.getobject('T-LM_END')
print('END timebase, type PPG_prog, shot:', end.shot)
print(tb[:10])
print(tb[-10:])
print('DCN timebase, type ADC_intern, shot:', dcn.shot)
print(tdcn[:10])
print(tdcn[-10:])

brd = sfread.SFREAD(39790, 'BRD')
sig = 'BRT1'
tbrd = brd.gettimebase(sig)
brt1 = brd.getobject(sig)
brt1cal = brd.getobject(sig, cal=True)

print(brt1cal[:10])

tra1 = sfread.SFREAD(37114, 'TRA', exp='git', ed=1)
tra2 = sfread.SFREAD(37114, 'TRA', exp='git')

neut1 = tra1.getobject('NEUTT')
neut2 = tra2.getobject('NEUTT')

print(neut1[100:110])
print(neut2[100:110])
print(tra1.ed)
print(tra2.ed)
