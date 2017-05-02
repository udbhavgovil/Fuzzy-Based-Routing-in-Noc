import math
import numpy as np
import skfuzzy as fuzz
import random 
import time
import matplotlib.pyplot as plt
import operator
import sys
"""
MESH TOPOLOGY (4x4)
12--13--14--15
|   |   |   |
8---9---10--11
|   |   |   |
4---5---6---7
|   |   |   |
0---1---2---3
"""
def XY_routing (id_s , id_d):
        if id_s == id_d:
                return 0
        
        else:
                #print  id_s , "->", 
                num_of_row = router[id_s]['nor']
                num_of_col = router[id_d]['noc']
                x_s = id_s % num_of_col
                x_d = id_d % num_of_col
                y_s = id_s / num_of_col
                y_d = id_d / num_of_col
		##print x_s , y_s
		##print id_s
		##print id_d
                x_hops = abs(x_s - x_d)
                y_hops = abs(y_s - y_d)
                if x_hops > 0:
                        if x_s > x_d:
                                #print "West",
                                return XY_routing( id_s - 1, id_d) + 1 + float(router[id_s]['input_west']+router[id_s-1]['input_east'])/16 + float(router[id_s-1]['total'])/40
                        else:
                                #print "East",
                                return XY_routing (id_s +1 , id_d) + 1 + float(router[id_s]['input_east']+router[id_s+1]['input_west'])/16 + float(router[id_s+1]['total'])/40
                elif y_hops > 0 :
                        if y_s > y_d:
                                #print "South",
                                return XY_routing (id_s - num_of_col ,id_d) + 1 + float(router[id_s]['input_south']+router[id_s-num_of_col]['input_north'])/16 + float(router[id_s-num_of_col]['total'])/40
                        else:
                                #print "North",
                                return XY_routing (id_s + num_of_col,id_d) + 1 + float(router[id_s]['input_north']+router[id_s+num_of_col]['input_south'])/16+ float(router[id_s+num_of_col]['total'])/40



def FXY_routing (id_s , id_d ,f):

        if id_s == id_d:
                return 0
        
        else:
                #print  id_s , "->",
                num_of_row = router[id_s]['nor']
                num_of_col = router[id_d]['noc']
                x_s = id_s % num_of_col
                x_d = id_d % num_of_col
                y_s = id_s / num_of_col
                y_d = id_d / num_of_col
                ##print x_s , y_s
                ##print x_d , y_d
                if x_s == x_d:
                        if y_s > y_d:
                                #print "South",
                                if f:
                                        return FXY_routing(id_s-num_of_col ,id_d,f) + 1 + float(router[id_s]['input_south']+router[id_s-num_of_col]['input_north'])/16 + float(router[id_s-num_of_col]['total'])/40
                                return FXY_routing(id_s-num_of_col ,id_d,f) + 1 + compute_cost(router[id_s]['input_south'],router[id_s-num_of_col]['input_north'])/40
                        else:
                                #print "North",
                                if f:
                                        return FXY_routing (id_s + num_of_col,id_d,f) + 1 + float(router[id_s]['input_north']+router[id_s+num_of_col]['input_south'])/16 + float(router[id_s+num_of_col]['total'])/40
                                return FXY_routing(id_s+num_of_col ,id_d,f) + 1 + compute_cost(router[id_s]['input_north'],router[id_s+num_of_col]['input_south'])/40
                                
                elif y_s == y_d:
                        if x_s > x_d:
                                #print "West",
                                if f:
                                        return FXY_routing(id_s-1,id_d,f) + 1 + float(router[id_s]['input_west']+router[id_s-1]['input_east'])/16 + float(router[id_s-1]['total'])/40
                                return FXY_routing(id_s-1 ,id_d,f) + 1 +  compute_cost(router[id_s]['input_west'],router[id_s-1]['input_east'])/40   
                        else:
                                #print "East",
                                if f:
                                        return FXY_routing(id_s+1,id_d,f) + 1 + float(router[id_s]['input_east']+router[id_s+1]['input_west'])/16 + float(router[id_s+1]['total'])/40
                                return FXY_routing(id_s+1,id_d,f) + 1 + compute_cost(router[id_s]['input_east'],router[id_s+1]['input_west'])/40   
                else:
                        if x_s < x_d and y_s < y_d:                                  
                                cost_x = compute_cost (router[id_s+1]['input_west'],router[id_s+1]['total']) 
                                cost_y = compute_cost (router[id_s+num_of_col]['input_south'],router[id_s+num_of_col]['total'])
                                if cost_x <= cost_y:
                                        #print "East", 
                                        if f:
                                                return FXY_routing(id_s+1,id_d,f) + 1 + float(router[id_s]['input_east']+router[id_s+1]['input_west'])/16 + float(router[id_s+1]['total'])/40
                                        return FXY_routing(id_s+1,id_d,f) + 1 +  cost_x /40

                                else:
                                        #print "North",
                                        if f:
                                                return FXY_routing (id_s + num_of_col,id_d,f) + 1 + float(router[id_s]['input_north']+router[id_s+num_of_col]['input_south'])/16 + float(router[id_s+num_of_col]['total'])/40
                                        return FXY_routing(id_s+num_of_col,id_d,f) + 1 + cost_y/40 
                                        
                                
                        if x_s > x_d and y_s > y_d:
                                cost_x = compute_cost (router[id_s-1]['input_east'],router[id_s-1]['total']) #
                                cost_y = compute_cost (router[id_s-num_of_col]['input_north'],router[id_s-num_of_col]['total'])
                                if cost_x <= cost_y:
                                        #print "West",
                                        if f:
                                                return FXY_routing (id_s -1 , id_d,f) + 1 + float(router[id_s]['input_west']+router[id_s-1]['input_east'])/16 + float(router[id_s-1]['total'])/40
                                        return FXY_routing(id_s-1,id_d,f) + 1 + cost_x/40  
                                else:
                                        #print "South",
                                        if f:
                                                return FXY_routing (id_s - num_of_col, id_d,f) + 1 + float(router[id_s]['input_south']+router[id_s-num_of_col]['input_north'])/16 + float(router[id_s-num_of_col]['total'])/40
                                        return FXY_routing(id_s-num_of_col,id_d,f) + 1 + cost_y/40 
                        if x_s > x_d and y_s < y_d:
                                cost_x = compute_cost (router[id_s-1]['input_east'],router[id_s-1]['total']) #
                                cost_y = compute_cost (router[id_s+num_of_col]['input_south'],router[id_s+num_of_col]['total'])
                                if cost_x <= cost_y:
                                        #print "West",
                                        if f:
                                                return FXY_routing (id_s -1 , id_d,f) + 1 + float(router[id_s]['input_west']+router[id_s-1]['input_east'])/16 + float(router[id_s-1]['total'])/40
                                        return FXY_routing(id_s-1,id_d,f) + 1 +  cost_x/40
                                else : 
                                        #print "North",
                                        if f:
                                                return FXY_routing (id_s + num_of_col,id_d,f) + 1 + float(router[id_s]['input_north']+router[id_s+num_of_col]['input_south'])/16 + float(router[id_s+num_of_col]['total'])/40
                                        return FXY_routing(id_s+num_of_col,id_d,f) + 1 +  cost_y/40
                                        
                        if x_s < x_d and y_s > y_d:
                                cost_x = compute_cost (router[id_s+1]['input_west'],router[id_s+1]['total']) #
                                cost_y = compute_cost (router[id_s-num_of_col]['input_north'],router[id_s-num_of_col]['total'])
                                if cost_x <= cost_y:
                                        #print "East",
                                        if f :
                                                return FXY_routing(id_s+1,id_d,f) + 1 + float(router[id_s]['input_east']+router[id_s+1]['input_west'])/16 + float(router[id_s+1]['total'])/40
                                        return FXY_routing(id_s+1,id_d,f) + 1 + cost_x/40
                                else:
                                        #print "South",
                                        if f:
                                                return FXY_routing (id_s - num_of_col, id_d,f) + 1 + float(router[id_s]['input_south']+router[id_s-num_of_col]['input_north'])/16 + float(router[id_s-num_of_col]['total'])/40
                                        return FXY_routing(id_s-num_of_col,id_d,f) + 1 + cost_y/40
                                
                                
                                 
def initialize ():
        global input_buffer_occup , total_buffer_occup , inbff_ , tobff_ , r_cost_ 
        input_buffer_occup = np.arange(0,9,1)
        total_buffer_occup = np.arange(0,41,1)
        router_cost = np.arange(0,41,1)
        
        inbff_ = [[] for j in range(5)]
        tobff_ = [[] for j in range(5)]
        r_cost_ = [[] for j in range(5)]
	#global inbff_ = [[],[],[],[],[]]
	
        inbff_[0]  = fuzz.trimf(input_buffer_occup , [0, 0, 2] )
        inbff_[1] = fuzz.trimf(input_buffer_occup , [0, 2, 4] )
        inbff_[2]  = fuzz.trimf(input_buffer_occup , [2, 4, 6] )
        inbff_[3] = fuzz.trimf(input_buffer_occup , [4, 6, 8] )
        inbff_[4]  = fuzz.trimf(input_buffer_occup , [6, 8, 8] )
        fig,ax = plt.subplots()
        mf = ['Zero', 'Very Small' , 'Small','Medium' ,'Large']
        for i in range(5):
        	ax.plot(input_buffer_occup,inbff_[i], label=mf[i])
        	
        ax.legend(loc='upper right', shadow=True)
        plt.title("Membership Function For Input Buffer Occupied")	
        plt.xlabel("Number of Input Buffer Occupied")
        plt.ylabel("Membership Value")
        
        tobff_[0] = fuzz.trimf(total_buffer_occup , [0, 0, 10] )
        tobff_[1] = fuzz.trimf(total_buffer_occup , [0, 10, 20] )
        tobff_[2]  = fuzz.trimf(total_buffer_occup , [10, 20, 30] )
        tobff_[3]  = fuzz.trimf(total_buffer_occup , [20, 30, 40] )
        tobff_[4]  = fuzz.trimf(total_buffer_occup , [30, 40, 40] )
        fig, ax = plt.subplots()
        for i in range(5):
        	ax.plot(total_buffer_occup,tobff_[i], label=mf[i])
        	
        ax.legend(loc='upper right', shadow=True)
        plt.title("Membership Function For Total Buffer Occupied")
        plt.xlabel("Number of Total Buffer Occupied")
        plt.ylabel("Membership Value")
        
        r_cost_[0]  = fuzz.trimf(router_cost , [0, 0, 10] )
        r_cost_[1] = fuzz.trimf(router_cost , [0, 10, 20] )
        r_cost_[2]  = fuzz.trimf(router_cost , [10, 20, 30] )
        r_cost_[3]  = fuzz.trimf(router_cost , [20, 30, 40] )
        r_cost_[4]  = fuzz.trimf(router_cost , [30, 40, 40] )

        global value 
        value = [0 ,10,20 ,30 ,40]
        plt.show()
        # , tobff_  , inbff_ ,  input_buffer_occup, total_buffer_occup , value
        #return compute_cost(_input, _total )
        
def compute_cost (_input , _total ):      
        _input_ = []
        _total_ = []
        for i in xrange(5):
                _input_.append(i)
                _total_ .append(i)

                
        rule = [[0,0,1,2,3],[0,1,1,2,3] ,[1,1,2,3,3],[2,2,3,4,4] , [3,3,4,4,4]]
        for i in xrange(5):
                
                _input_[i] = fuzz.interp_membership(input_buffer_occup , inbff_[i],  _input)
                _total_[i] = fuzz.interp_membership(total_buffer_occup , tobff_[i],  _total)
        n=0
        m=0	
        cost=0
        mvalue=0
        for i in _input_:
                m=0
                for j in _total_:
                        if i>=0 and j>=0:
                                cost = cost + min(i,j)*value[rule[n][m]]
                                mvalue = mvalue + min(i,j)
                                m=m+1
                n=n+1

        ##print cost/mvalue
        ##print cost
        ##print mvalue 
        return (cost/mvalue)

def dsdv(i,x,i_cost):
        MAX = sys.maxsize
        forward_table = [{'cost':MAX,'node':0} for j in xrange(x*x) ]
        cal = []
        for j in xrange(x*x):
                cal.append(False)
        node = {}
        forward = {}
        flag = True
        counter =0
        f=1
        forward[i]= -1
        cal[i]=True
        while len(node)!=0 or flag==True:
                flag =False
                
                if not i%x == x-1 and cal[i+1]==False:
                        cost = FXY_routing(i,i+1,f)
                        if i+1 in node:
                                if cost+i_cost < node[i+1]:
                                        node[i+1]=cost+i_cost
                                        forward[i+1]=forward[i]
                                        
                        else:
                                node[i+1]=cost+i_cost
                                if forward[i] == -1 :
                                        forward[i+1] = i+1
                                else:
                                        forward[i+1] = forward[i]
                                
                                
                if not i%x==0 and cal[i-1]==False:
                        cost = FXY_routing(i,i-1,f)
                        if i-1 in node:
                                if cost+i_cost < node[i-1]:
                                        node[i-1]=cost+i_cost
                                        forward[i-1]=forward[i]
                        else:
                                node[i-1]=cost+i_cost
                                if forward[i] == -1 :
                                        forward[i-1] = i-1
                                else:
                                        forward[i-1] = forward[i]
                if i>=x and cal[i-x]==False:
                        cost = FXY_routing(i,i-x,f)
                        if i-x in node:
                                if cost+i_cost < node[i-x]:
                                        node[i-x]=cost+i_cost
                                        forward[i-x]=forward[i]
                        else:
                                node[i-x]=cost+i_cost
                                if forward[i] == -1 :
                                        forward[i-x] = i-x
                                else:
                                        forward[i-x] = forward[i]
                if i<x*(x-1) and cal[i+x]==False:
                        cost = FXY_routing(i,i+x,f)
                        if i+x in node:
                                if cost+i_cost < node[i+x]:
                                        node[i+x]=cost+i_cost
                                        forward[i+x]=forward[i]
                        else:
                                node[i+x]=cost+i_cost
                                if forward[i] == -1 :
                                        forward[i+x] = i+x
                                else:
                                        forward[i+x] = forward[i]
                                

               
                        
                #print "node" , node
                sorted_node = sorted(node.items(),key=operator.itemgetter(1))
                next_node = sorted_node[0][0]
                #print "next node " , next_node
                del node[next_node]
                forward_table[next_node]['cost']=sorted_node[0][1]
                forward_table[next_node]['node']=forward[next_node]
                cal[next_node]=True
                i_cost = sorted_node[0][1]
                i = next_node        
                #print forward 
                
                #for t in forward_table:
                        
                #        print t['node'],
                
        return forward_table
        
        
def dsdv_compute(id_s,id_d,routing_table):
        if id_s == id_d :
                return 0
        next_s = routing_table[id_s][id_d]['node']
        num_of_col = router[id_s]['noc']
        if next_s == id_s:
                #print id_s , "->" , id_d
                if id_s - 1 == next_s:
                        return  1 + float(router[id_s]['input_west']+router[id_s-1]['input_east'])/16 + float(router[id_s-1]['total'])/40
                elif id_s + 1 == next_s:
                        return  1 + float(router[id_s]['input_east']+router[id_s+1]['input_west'])/16 + float(router[id_s+1]['total'])/40

                elif id_s + router[id_s]['noc'] == next_s:
                        return 1 + float(router[id_s]['input_north']+router[id_s+num_of_col]['input_south'])/16+ float(router[id_s+num_of_col]['total'])/40
                else:
                        return  + float(router[id_s]['input_south']+router[id_s-num_of_col]['input_north'])/16+ float(router[id_s-num_of_col]['total'])/40

        #print id_s ,"->", next_s
                
        if id_s - 1 == next_s:
                return dsdv_compute(next_s,id_d,routing_table) + 1 + float(router[id_s]['input_west']+router[id_s-1]['input_east'])/16 + float(router[id_s-1]['total'])/40
        elif id_s + 1 == next_s:
                return dsdv_compute(next_s,id_d,routing_table) + 1 + float(router[id_s]['input_east']+router[id_s+1]['input_west'])/16 + float(router[id_s+1]['total'])/40

        elif id_s + router[id_s]['noc'] == next_s:
                return dsdv_compute(next_s,id_d,routing_table) + 1 + float(router[id_s]['input_north']+router[id_s+num_of_col]['input_south'])/16+ float(router[id_s+num_of_col]['total'])/40
        else:
                return dsdv_compute(next_s,id_d,routing_table) + 1 + float(router[id_s]['input_south']+router[id_s-num_of_col]['input_north'])/16+ float(router[id_s-num_of_col]['total'])/40
                        
def router_initialize(x,y):
        initialize()
        global router
        router = [{'id':k,'input_north':random.randint(1,8),'input_west':random.randint(1,8),'input_south':random.randint(1,8),'input_east':random.randint(1,8),'noc':y , 'nor':x , 'total':0} for k in range(x*y+1)]
        for k in range(x*y):
                router[k]['total'] = router[k]['input_north'] + router[k]['input_south'] + router[k]['input_west'] + router[k]['input_east']
                

if __name__ == "__main__":
	initialize ()
	t = input ()
	for i in xrange (2,6):
		plt.figure(1)
		g = 220 + i -1 
		plt.subplot(g)
		
		
                t1 = time.clock()
                y = pow(2,i)
                plt.title("2-D Mesh "+str(y)+"x"+str(y))
                x=y
                router = [{'id':k,'input_north':random.randint(1,8),'input_west':random.randint(1,8),'input_south':random.randint(1,8),'input_east':random.randint(1,8),'noc':y , 'nor':x , 'total':0} for k in range(x*y+1)]
                for k in xrange(x*y):
                        router[k]['total'] = router[k]['input_north'] + router[k]['input_south'] + router[k]['input_west'] + router[k]['input_east']
                routing_table = []
                for it in xrange(x*y):
                        routing_table.append([])
                        routing_table[it] = dsdv(it,x,0)
                        
##                print "\n\n | "
##                
##                
##                for it in xrange(x*x):
##                        print it,
##                        for jt in xrange(x*x):
##                               print routing_table[it][jt]['node'] , " | " ,
##                        print "\n"
##                print "\n\n\n"
##                for it in xrange(x*x):
##                        print it , " | ",
##                print "\n"
##                for it in xrange(x*x):
##                        print it, " *",
##                        for jt in xrange(x*x):
##                               print (  "%.2f"%routing_table[it][jt]['cost'] ), 
##                        print "\n"
                F = []
                D = []
                X = []
                
		
                        
                Pass_xy =0
                Pass_dsdv=0
                Pass_fxy=0
                
                for j in xrange(t):
                        random.seed()
                        M = sys.maxsize
                        source = random.randint(0,x*y-1)
                        dest = random.randint (0,x*y-1)
                        count = 0
                        while source == dest:
                                dest = random.randint (0,x*y-1)
                        #print "source = " , source , "dest" , dest 
                        #print "FXY"
                        fxy = FXY_routing(source,dest,1)
                        #print "DSDV" 
                        dsdv_xy = dsdv_compute(source,dest,routing_table)
                        #print routing_table[source]
                        #print "XY"
                        xy =  XY_routing(source,dest)
                        M = min(M,min(fxy,min(xy,dsdv_xy)))
                        F.append(fxy)
                        D.append(dsdv_xy)
                        X.append(xy)
                        #print "fxy " , fxy , "xy", xy , " dsdv " , dsdv_xy 
                        if fxy == M:
                                Pass_fxy = Pass_fxy + 1
                        if dsdv_xy == M:
                                Pass_dsdv = Pass_dsdv + 1
                        if xy == M:
                                Pass_xy = Pass_xy + 1

                        
                
                t2 = time.clock() - t1
                #print Pass_xy , Pass_fxy , Pass_dsdv
                
                print "Test Cycle = " , t
                print "Processing Time " , t2 ,"Sec"
                print 'Topology 2-D Mesh (',x,'*',y,')'
                print "Non - Fuzzy Accuracy = ",  (float(Pass_xy*100) /t) , "%"
                print "Fuzzy Accuracy = ",  (float(Pass_fxy*100) /t) , "%"
                print "Fuzzy-DSDV Accuracy = ",  (float(Pass_dsdv*100) /t) , "%"
                print ""
                x_axis = np.arange(1,t+1,1)
                
                #fig,ax = plt.subplots()
                plt.plot(x_axis,X,'g--',label='Non-Fuzzy')
                plt.plot(x_axis,F,'r--',label='Fuzzy-XY')
                plt.plot(x_axis,D,'b--',label='Fuzzy-DSDV')
                plt.xlabel("Test Run Number")
                plt.ylabel("Cost")
                plt.legend(loc='upper right', shadow=True)
                plt.subplots_adjust(top=0.92,bottom=0.08,left=0.10,right=0.95,hspace=0.25,wspace=0.35)
plt.show()
                        
