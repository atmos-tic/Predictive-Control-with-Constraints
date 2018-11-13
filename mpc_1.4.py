#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def StateFunc(y, u):
    y_ = [1.2, 0.7] * y  -  u
    return y_

fig = plt.figure()
ims = []
ims_t = []
ims_y = []
ims_s = []
ims_u = []

setpoint = 1.0
Hp = 8
Tref = 6
Ts = 0.6
ramda = np.exp(-Ts/Tref)

umpast = 0.0
ympast = 0.0
ym2past = 0.0
t = 0
rptraj = 0.0
ymnow = StateFunc(ympast, ym2past, umpast)
ymfree = 0.0
ymfree_past = 0.0
ymfree_2past = 0.0
step_responce = 0.0
step_responce_past = 0.0
step_responce_2past = 0.0
uptraj = 0.0

while(t<25):
    t += 1
    rptraj = setpoint - (setpoint - ymnow) * (ramda**Hp)
    ymfree_2past = ym2past
    ymfree_past = ympast
    step_responce_past = 0
    step_responce_2past = 0
    for predict_step in range(Hp):
        ymfree =  StateFunc(ymfree_past, ymfree_2past, umpast)
        ymfree_past = ymfree
        ymfree_2past = ymfree_past
        step_responce = StateFunc(step_responce_past, step_responce_2past, 1)
        step_responce_past = step_responce
        step_responce_2past = step_responce_past
    duptraj = (rptraj - ymfree) / step_responce
    uptraj = umpast + duptraj
    ymnow = StateFunc(ympast, ym2past, uptraj)
    ympast = ymnow
    ym2past = ympast
    umpast = uptraj

    ims_t.append(t)
    ims_y.append(ymnow)
    ims_s.append(setpoint)
    ims_u.append(uptraj)
    #print(setpoint)
    #plt.plot(t, ymnow, '.',c="black")
    ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=100)

plt.plot(ims_t, ims_s, c="red", label="set_point")
plt.plot(ims_t, ims_y, c="black", label="output")
plt.plot(ims_t, ims_u,'+', c="blue", label="input")
ani.save('anim.gif', writer="imagemagick")
plt.legend()
plt.show()