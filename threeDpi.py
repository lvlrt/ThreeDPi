#!/usr/bin/env python

##TODO
#ME en E-pos en de maken ?? treat e as another axis?? extruder 
#engraver 

##TODO END

import argparse

parser = argparse.ArgumentParser(description="RPi Controlled 3Dprinter")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-f", "--filepath", help="Path to GCode file")
group.add_argument("-m", "--manual", action="store_true", help="Manually control printer")
parser.add_argument("-d", "--dryrun", type=float, help="Level of dry run")
args = parser.parse_args()

if args.dryrun != None:
        dry_run = args.dryrun
else:
        dry_run = 0

if dry_run<1:
    import RPi.GPIO as GPIO

if dry_run<1:
    import Motor_control
    from Bipolar_Stepper_Motor_Class import Bipolar_Stepper_Motor
import time
from numpy import pi, sin, cos, sqrt, arccos, arcsin

################################################################################################
################################################################################################
#################                            ###################################################
#################    Parameters set up       ###################################################
#################                            ###################################################
################################################################################################
################################################################################################

if dry_run<1:
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup();
    GPIO.setmode(GPIO.BCM)

if dry_run<1:
    MX=Bipolar_Stepper_Motor(5,25,24,23);     #pin number for a1,a2,b1,b2.  a1 and a2 form coil A; b1 and b2 form coil B

    MY=Bipolar_Stepper_Motor(19,13,12,6);

    MZ=Bipolar_Stepper_Motor(21,20,26,16);

    ME=Bipolar_Stepper_Motor(22,27,18,17);

#resolution of motors?? make it an external CONF FILE??
dx=0.075; #resolution in x direction. Unit: mm
dy=0.075; #resolution in y direction. Unit: mm
dz=0.075; #resolution in z direction. Unit: mm
de=0.075; #resolution in e direction. Unit: mm

################################################################################################
#################    G code reading Functions    ###############################################
################################################################################################

def XYZEFposition(lines):
    #given a movement command line, return the X Y Z E position
    if lines.find('X') != -1:
        xchar_loc=lines.index('X');
        i=xchar_loc+1;
        while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
            i+=1;
        x_pos=float(lines[xchar_loc+1:i]);    
    else:
        x_pos=0
    
    if lines.find('Y') != -1:
        ychar_loc=lines.index('Y');
        i=ychar_loc+1;
        while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
            i+=1;
        y_pos=float(lines[ychar_loc+1:i]);    
    else:
        y_pos=0

    if lines.find('Z') != -1:
        zchar_loc=lines.index('Z');
        i=zchar_loc+1;
        while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
            i+=1;
        z_pos=float(lines[zchar_loc+1:i]);    
    else:
    	z_pos=0

    if lines.find('E') != -1:
        echar_loc=lines.index('E');
        i=echar_loc+1;
        while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
            i+=1;
        e_pos=float(lines[echar_loc+1:i]);    
    else:
    	e_pos=0

    if lines.find('F') != -1:
        fchar_loc=lines.index('F');
        i=fchar_loc+1;
        while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
            i+=1;
        feedrate=float(lines[fchar_loc+1:i]);    
    else:
    	feedrate=0

    return x_pos,y_pos,z_pos,e_pos, feedrate;

def IJposition(lines):
    #given a G02 or G03 movement command line, return the I J position
    ichar_loc=lines.index('I');
    i=ichar_loc+1;
    while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
        i+=1;
    i_pos=float(lines[ichar_loc+1:i]);    
    
    jchar_loc=lines.index('J');
    i=jchar_loc+1;
    while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
        i+=1;
    j_pos=float(lines[jchar_loc+1:i]);    

    return i_pos,j_pos;

def moveto(MX,x_pos,dx,MY,y_pos,dy,MZ,z_pos,dz,ME,e_pos,de,speed):
#Move to (x_pos,y_pos) (in real unit)
    stepx=int(round(x_pos/dx))-MX.position;
    stepy=int(round(y_pos/dy))-MY.position;
    stepz=int(round(z_pos/dz))-MZ.position;
    stepe=int(round(e_pos/de))-ME.position;

    Total_step=sqrt((sqrt((sqrt((stepx**2+stepy**2))**2+stepz**2))**2+stepe**2));
            
    if Total_step>0:
        print('Movement: Dx=', stepx, '  Dy=', stepy, '  Dz=', stepz, '  De=', stepe);
        if dry_run<1:
            Motor_control.Motor_Step(MX,stepx,MY,stepy,MZ,stepz,ME,stepe,speed);
    return 0;
    
###########################################################################################
#################    Main program           ###############################################
###########################################################################################

try:#read and execute G code
    if (args.manual == False):
        filename=args.filepath; #file name of the G code commands
        for lines in open(filename,'r'):
            print(lines);
            if lines==[]:
                1; #blank lines
            elif lines[0:3]=='G90':
                print('start');
            elif lines[0:6]=='G92 E0':
                print('reset extruder');
                if dry_run<1:
                    ME.position = 0

            elif lines[0:3]=='G20':# working in inch;
                dx/=25.4;
                dy/=25.4;
                print('Working in inch');
                  
            elif lines[0:3]=='G21':# working in mm;
                print('Working in mm');  
                
            elif lines[0:3]=='M05':
                print('Laser turned off');
                
            elif lines[0:3]=='M03':
                print('Laser turned on');

            elif lines[0:3]=='M02':
                print('finished. shuting down');
                break;
            elif (lines[0:3]=='G1F')|(lines[0:4]=='G1 F'):
                1;#do nothing
            elif (lines[0:3]=='G00')|(lines[0:3]=='G1 ')|(lines[0:3]=='G01'):#|(lines[0:3]=='G02')|(lines[0:3]=='G03'):
                if (lines.find('X') != -1 or lines.find('Y') != -1 or lines.find('Z') != -1 ): #Ignore lines not dealing with XY plane
		    #linear engraving movement
                    if (lines[0:3]=='G00'):#this is an empty move (stop extruding)
                        print('rapid move')
                    else:
                        print('not a rapid move')
                    
                    [x_pos,y_pos,z_pos, e_pos, feedrate]=XYZEFposition(lines);
                    if feedrate != 0:
                        speed = feedrate/60
                    print(x_pos,y_pos,z_pos, e_pos, speed);
                    if dry_run<1:
                        moveto(MX,x_pos,dx,MY,y_pos,dy,MZ,z_pos,dz,ME,e_pos,de,speed);
                
            elif (lines[0:3]=='G02')|(lines[0:3]=='G03'): #circular interpolation
                if (lines.find('X') != -1 and lines.find('Y') != -1 and lines.find('I') != -1 and lines.find('J') != -1):
                    laseron()
                    old_x_pos=x_pos;
                    old_y_pos=y_pos;

                    [x_pos,y_pos,z_pos, e_pos,feedrate]=XYZEFposition(lines);
                    
                    if feedrate != 0:
                        speed = feedrate/60
		    
                    [i_pos,j_pos]=IJposition(lines);

                    xcenter=old_x_pos+i_pos;   #center of the circle for interpolation
                    ycenter=old_y_pos+j_pos;
                
                
                    Dx=x_pos-xcenter;
                    Dy=y_pos-ycenter;      #vector [Dx,Dy] points from the circle center to the new position
                
                    r=sqrt(i_pos**2+j_pos**2);   # radius of the circle
                
                    e1=[-i_pos,-j_pos]; #pointing from center to current position
                    if (lines[0:3]=='G02'): #clockwise
                        e2=[e1[1],-e1[0]];      #perpendicular to e1. e2 and e1 forms x-y system (clockwise)
                    else:                   #counterclockwise
                        e2=[-e1[1],e1[0]];      #perpendicular to e1. e1 and e2 forms x-y system (counterclockwise)

                    #[Dx,Dy]=e1*cos(theta)+e2*sin(theta), theta is the open angle

                    costheta=(Dx*e1[0]+Dy*e1[1])/r**2;
                    sintheta=(Dx*e2[0]+Dy*e2[1])/r**2;        #theta is the angule spanned by the circular interpolation curve
                        
                    if costheta>1:  # there will always be some numerical errors! Make sure abs(costheta)<=1
                        costheta=1;
                    elif costheta<-1:
                        costheta=-1;

                    theta=arccos(costheta);
                    if sintheta<0:
                        theta=2.0*pi-theta;

                    no_step=int(round(r*theta/dx/5.0));   # number of point for the circular interpolation
                    
                    for i in range(1,no_step+1):
                        tmp_theta=i*theta/no_step;
                        tmp_x_pos=xcenter+e1[0]*cos(tmp_theta)+e2[0]*sin(tmp_theta);
                        tmp_y_pos=ycenter+e1[1]*cos(tmp_theta)+e2[1]*sin(tmp_theta);
                        moveto(MX,tmp_x_pos,dx,MY, tmp_y_pos,dy,speed);
    else: #Manual Control Mode
        while True:
            xsteps = int(input("X Stepper Steps: "))
            ysteps = int(input("Y Stepper Steps: "))
            zsteps = int(input("Z Stepper Steps: "))
            esteps = int(input("E Stepper Steps: ")) 

            if (xsteps > 0):
                MX.move(1,abs(xsteps),0.01)
            else:
                MX.move(-1,abs(xsteps),0.01)
            if (ysteps > 0):
                MY.move(1,abs(ysteps),0.01)
            else:
                MY.move(-1,abs(ysteps),0.01)
            if (zsteps > 0):
                MZ.move(1,abs(zsteps),0.01)
            else:
                MZ.move(-1,abs(zsteps),0.01)
            if (ysteps > 0):
                ME.move(1,abs(esteps),0.01)
            else:
                ME.move(-1,abs(esteps),0.01)

except KeyboardInterrupt:
    pass

moveto(MX,0,dx,MY,0,dy,50);  # move back to Origin #dont do Z here or E

MX.unhold();
MY.unhold();
MZ.unhold();

if dry_run<1:
    GPIO.cleanup();
