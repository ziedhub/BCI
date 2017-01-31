'''
Created on 05.09.2016

@author: Stefan/Zied
'''
import pylsl
from emotiv_plugin.emotiv_w import *
from includes.abstract_experiment import ExperimentBase
from psychopy import visual, core, event, parallel #import some libraries from PsychoPy
import random
import math
import time
import csv
import numpy as np
#import sklearn

class ExperimentDefinition(ExperimentBase):
    experiment_info = {'name': 'pong_game',
                       'author:': 'Zied',
                       'version': '1.0',}
    def init(self):
        print "Creating stream " + self.lsl_stream_name
        info = pylsl.StreamInfo(self.lsl_stream_name, 'Markers', 1, pylsl.IRREGULAR_RATE, 'string', 'skynet')
        self.outlet = pylsl.StreamOutlet(info)
        time.sleep(1)
            
    def start(self):

        rate=128#samples
        window=1.5#sec
        marker='feature recorded'
        c=0    
        t=time.time()
        
        C1=np.zeros((1,1),dtype='float64')
        C3=np.zeros((1,1),dtype='float64')
        C5=np.zeros((1,1),dtype='float64')
        FC3=np.zeros((1,1),dtype='float64')
        CP3=np.zeros((1,1),dtype='float64')
        C2=np.zeros((1,1),dtype='float64')
        C4=np.zeros((1,1),dtype='float64')
        C6=np.zeros((1,1),dtype='float64')
        CP4=np.zeros((1,1),dtype='float64')
        FC4=np.zeros((1,1),dtype='float64')
        #features
        fC1=np.zeros((1,1),dtype='float64')
        fC3=np.zeros((1,1),dtype='float64')
        fC5=np.zeros((1,1),dtype='float64')
        fFC3=np.zeros((1,1),dtype='float64')
        fCP3=np.zeros((1,1),dtype='float64')
        fC2=np.zeros((1,1),dtype='float64')
        fC4=np.zeros((1,1),dtype='float64')
        fC6=np.zeros((1,1),dtype='float64')
        fCP4=np.zeros((1,1),dtype='float64')
        fFC4=np.zeros((1,1),dtype='float64')
        #delete the 0 from the features
        fC1=np.delete(fC1,0)
        fC3=np.delete(fC3,0)
        fC5=np.delete(fC5,0)
        fFC3=np.delete(fFC3,0)
        fCD3=np.delete(fCP3,0)
        fC2=np.delete(fC2,0)
        fC4=np.delete(fC4,0)
        fC6=np.delete(fC6,0)
        fCP4=np.delete(fCP4,0)
        fFC4=np.delete(fFC4,0)
        # Parameters
        screensize = [1000,1000]
        ballsize = 1.5
        paddlesize = 15 # as fraction of total screensize
        ballspeed = 0.26
        gameduration = 180
        showfeedback = True
        
        comment = 'training'
        
        bcicontrol = False # otherwise mouse control
        #//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        headset = Emotiv(2) # buffer in seconds
        headset.open()
        print("Headset info: " + str(headset.getDeviceInfo()))
        headset.start(check_connection=False)
        data = None
        #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        '''if bcicontrol:
            # labstreaminglayer
            from pylsl import StreamInlet, resolve_stream
        
            # first resolve an EEG stream on the lab network
            print("looking for an EEG stream...")
            streams = resolve_stream('type', 'EEG')
        
            # create a new inlet to read from the stream
            inlet = StreamInlet(streams[0])'''
        
        
        
        ########################################
        
        # create window
        mywin = visual.Window(screensize,monitor="testMonitor", screen=1, units="deg", rgb=[-1,-1,-1])
        
        message1 = visual.TextStim(win=mywin, pos=[0,0],text='Hit space when ready.',color=(1, 1, 1), colorSpace='rgb')
        message1.draw()
        mywin.flip()
        event.waitKeys('space')
        
        mouseinstance = event.Mouse(visible=False,newPos=False,win=mywin)
        
        nHits = visual.TextStim(win=mywin, pos=[-13,13],text=0,color=(0, 1, 0), height=2, colorSpace='rgb', bold=True)
        if showfeedback:
            nHits.setAutoDraw(True)
        
        nMiss = visual.TextStim(win=mywin, pos=[13,13],text=0,color=(1, 0, 0), height=2, colorSpace='rgb', bold=True)
        if showfeedback:
            nMiss.setAutoDraw(True)
        
        countdown = visual.TextStim(win=mywin, pos=[0,13],text=0,color=(1, 1, 1), height=1.5, colorSpace='rgb', bold=True)
        if showfeedback:
            countdown.setAutoDraw(True)
        
        # create ball
        ball = visual.Circle(win=mywin, size=ballsize, pos=[0,0],lineWidth=0,lineColor='white',fillColor='white')
        ball.setAutoDraw(True)
        
        # create paddle
        paddle = visual.Rect(win=mywin, width=paddlesize, height=1, pos=[0,-13],lineWidth=2,lineColor='blue',fillColor='white')
        paddle.setAutoDraw(True)
        
        # initialization
        #ch = [0.8,0.9,1,-0.8,-0.9,-1]
        ch = [0.7,0.8,0.9,1,-0.7,-0.8,-0.9,-1]
        
        while True:
        
            a = random.choice(ch)*ballspeed/2
            b = random.choice(ch)*math.sqrt(ballspeed*ballspeed-a*a)
            direction = [a, b]
            hitpoints = 0
            misspoints = 0
            ball.pos = [0,10]
            
            start=time.clock()
            current = 0
        
            while gameduration-current>0:
                if ball.pos[1]>-12 or ball.pos[1]<-13:
                    toggle = True
                mywin.flip()
                # generate random direction vector
            
                # update ball position
                ball.pos = ball.pos+direction
            
                # check ball position against boundaries
                # and reverse direction if it hits any boundary
                if ball.pos[0]>14 or ball.pos[0]<-14:
                    direction[0]=-direction[0]
                if ball.pos[1]>14:
                    direction[1]=-direction[1]
                
                # check ball position against paddle
                if toggle and ball.pos[1]<-12 and ball.pos[1]>-13 and ball.pos[0]<paddle.pos[0]+paddlesize/2 and ball.pos[0]>paddle.pos[0]-paddlesize/2:
                    direction[1]=-direction[1]
                    hitpoints = hitpoints+1
                    toggle = False
                
                if ball.pos[1]<-30:
                    misspoints = misspoints+1
                    a = random.choice(ch)*ballspeed/2
                    b = random.choice(ch)*math.sqrt(ballspeed*ballspeed-a*a)
                    direction = [a, b]
                    ball.pos = [0,10]
                    time.sleep(0)
                
                # move paddle according to the BCI  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                data = headset.read(np.array(EmotivChannels.ALL_DATA) ,with_offset=True)
                if data is None:
                    continue
                #insert the new data
                C1=np.insert(C1,0,(data[0])[0])
                C3=np.insert(C1,0,(data[0])[4])
                C5=np.insert(C1,0,(data[0])[6])
                FC3=np.insert(C1,0,(data[0])[5])
                CP3=np.insert(C1,0,(data[0])[1])
                C2=np.insert(C1,0,(data[0])[13])
                C4=np.insert(C1,0,(data[0])[9])
                C6=np.insert(C1,0,(data[0])[7])
                FC4=np.insert(C1,0,(data[0])[8])
                CP4=np.insert(C1,0,(data[0])[12])
                #delete the old data to maintain the window size
                while C1.size>window*rate:
                    C1=np.delete(C1,window*rate)
                    C3=np.delete(C3,window*rate)
                    C5=np.delete(C5,window*rate)
                    FC3=np.delete(FC3,window*rate)
                    CP3=np.delete(CP3,window*rate)
                    C2=np.delete(C2,window*rate)
                    C4=np.delete(C4,window*rate)
                    C6=np.delete(C6,window*rate)
                    FC4=np.delete(FC4,window*rate)
                    CP4=np.delete(CP4,window*rate)
                    
                #root-mean-square
                pC1=math.sqrt(np.mean(np.square(C1)))
                pC3=math.sqrt(np.mean(np.square(C3)))
                pC5=math.sqrt(np.mean(np.square(C5)))
                pFC3=math.sqrt(np.mean(np.square(FC3)))
                pCP3=math.sqrt(np.mean(np.square(CP3)))
                pC2=math.sqrt(np.mean(np.square(C2)))
                pC4=math.sqrt(np.mean(np.square(C4)))
                pC6=math.sqrt(np.mean(np.square(C6)))
                pFC4=math.sqrt(np.mean(np.square(FC4)))
                pCP4=math.sqrt(np.mean(np.square(CP4)))
        
                left=(pC1+pC3+pC5+pFC3+pCP3) 
                right=(pC2+pC4+pC6+pFC4+pCP4) 
                if ball.pos[1]<-12 and ball.pos[1]>-12.7 and time.time()-t>1 :
                    t=time.time()
                    fC1=np.insert(fC1,0,pC1)
                    fC3=np.insert(fC3,0,pC3)
                    fC5=np.insert(fC5,0,pC5)
                    fFC3=np.insert(fFC3,0,pFC3)
                    fCP3=np.insert(fCP3,0,pCP3)
                    fC2=np.insert(fC2,0,pC2)
                    fC4=np.insert(fC4,0,pC4)
                    fC6=np.insert(fC6,0,pC6)
                    fCP4=np.insert(fCP4,0,pFC4)
                    fFC4=np.insert(fFC4,0,pCP4)
                    print('feature saved ')
                    print(fC1)
                    self.outlet.push_sample([marker])
                if right>=left:
                    move=0.3
                else:
                    move=-0.3
                c=c+move
                paddle.pos=[c,-13]
                #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                 
                if paddle.pos[0] > 15-paddlesize/2:
                    paddle.pos[0]=15-paddlesize/2
                if paddle.pos[0]<-15+paddlesize/2:
                    paddle.pos[0]=-15+paddlesize/2    
            
                nHits.setText(hitpoints)
                nMiss.setText(misspoints)
                now = time.clock()
                current = int(now-start)
                countdown.setText(gameduration-current)
            
            message2 = visual.TextStim(win=mywin, pos=[0,1],text='End of Game',color=(1, 1, 1), colorSpace='rgb', bold=True)
            message2.draw()
            message3 = visual.TextStim(win=mywin, pos=[0,0],text='Continue (Space)',color=(1, 1, 1), colorSpace='rgb')
            message3.draw()
            message4 = visual.TextStim(win=mywin, pos=[0,-1],text='Terminate (Esc)',color=(1, 1, 1), colorSpace='rgb')
            message4.draw()
            mywin.flip()
            resp_key = event.waitKeys(keyList=['space','escape'])
            
            # write results to text file
            with open('stats.txt', 'a') as file:
                file.write(time.ctime()+'\t'+str(hitpoints)+'\t'+str(misspoints)+'\t'+comment+'\n')
            
            print resp_key
            if resp_key == ['space']:
                message5 = visual.TextStim(win=mywin, pos=[0,0],text='Continue ...',color=(1, 1, 1), colorSpace='rgb', bold=True)
                message5.draw()
                mywin.flip()
                time.sleep(2)
            if resp_key == ['escape']:
                break