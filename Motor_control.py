import RPi.GPIO as GPIO
import time
from Bipolar_Stepper_Motor_Class import Bipolar_Stepper_Motor
from numpy import abs,sqrt


def GCD(a,b):#greatest common diviser
    while b:
       a, b = b, a%b;
    return a;

def LCM(a,b):#least common multipler
    return a*b/GCD(a,b);

def sign(a): #return the sign of number a
    if a>0:
        return 1;
    elif a<0:
        return -1;
    else:
        return 0;
    
def Motor_Step(stepper1, step1, stepper2, step2, stepper3, step3, stepper4,step4, speed):
#   control stepper motor 1 and 2 simultaneously
#   stepper1 and stepper2 are objects of Bipolar_Stepper_Motor class
#   direction is reflected in the polarity of [step1] or [step2]

    dir1=sign(step1);  #get dirction from the polarity of argument [step]
    dir2=sign(step2);
    dir3=sign(step3);
    dir4=sign(step4);

    step1=abs(step1);
    step2=abs(step2);
    step3=abs(step3);
    step4=abs(step4);

# [total_micro_step] total number of micro steps
# stepper motor 1 will move one step every [micro_step1] steps
# stepper motor 2 will move one step every [micro_step2] steps
# So [total_mirco_step]=[micro_step1]*[step1] if step1<>0;  [total_micro_step]=[micro_step2]*[step2] if step2<>0 
    total_micro_step = 1
    
    #TODO reduce here, with gcd and reducs
    if step1!=0:
        total_micro_step=total_micro_step * step1
    if step2!=0:
        total_micro_step=total_micro_step * step2
    if step3!=0:
        total_micro_step=total_micro_step * step3
    if step4!=0:
        total_micro_step=total_micro_step * step4

    if step1!=0:
    	micro_step1=total_micro_step/step1
    else:
    	micro_step1=total_micro_step+100#make it never happen
    if step2!=0:
        micro_step2=total_micro_step/step2
    else:
        micro_step2=total_micro_step+100#make it never happen
    if step3!=0:
        micro_step3=total_micro_step/step3
    else:
        micro_step3=total_micro_step+100#make it never happen
    if step4!=0:
        micro_step4=total_micro_step/step4
    else:
        micro_step4=total_micro_step+100#make it never happen

##dit voorgaand stuk is om het aantal micro steps te bepalen ( minimale resolutie van de beweging om het rechtste pad te kunnen uitstippelen)
##ik moet dus de total micro steps berekenen van de steps die niet 0 zijn, en diegene die - zijn de microstap groter dan de total micro steps (zodat het nooit wordt uitgevoerd

#idee
### totaal micro steps = (voor alle niet 0 waarden) de vermenigvuldiging van alle steps
### de micro step is voor alle niet 0 waarden de totaal micro steps gedeeld door het steps van de motor
### voor de 0 waarde is de microstep NULL (en dan programatisch oplosse) of total_micro steps +1

    T=sqrt(sqrt(sqrt(step1**2+step2**2)**2+step3**2)**2+step4**2)/speed;      #total time #for all 4
    print(T); 
    dt=T/total_micro_step;                #time delay every micro_step
    print(total_micro_step)
    time.sleep(T);
    
    ###cnt_microstep for each stepper, 1 x microstep
    
    cnt=0
    while cnt<total_micro_step:
        #for each
        if cnt == cnt_micro_step4:
            do movement
            en cnt_micro_step4 + micro_step4

        lowest cnt_micro_step #of all
        calculate time to sleep for all before next and rest this, only di if not total-micro-step
        cnt = lowest cnt

    
    
    """
    for i in range(1,total_micro_step+1):    #i is the iterator for the micro_step. i cannot start from 0
        
        #this is all crazy expensive, idea is to write small gcode in 1 time as an array of commands,
        print(i)
        time_laps=0;
        if ((i % micro_step1)==0):#motor 1 need to turn one step
            stepper1.move(dir1,1,dt/4.0);
            time_laps+=dt/4.0;
            
        if ((i % micro_step2)==0):#motor 2 need to turn one step
            stepper2.move(dir2,1,dt/4.0);
            time_laps+=dt/4.0;

        if ((i % micro_step3)==0):#motor 3 need to turn one step
            stepper3.move(dir3,1,dt/4.0);
            time_laps+=dt/4.0;

        if ((i % micro_step4)==0):#motor 4 need to turn one step
            stepper4.move(dir4,1,dt/4.0);
            time_laps+=dt/4.0;
        
        time.sleep(dt-time_laps);
        """
    return 0;
