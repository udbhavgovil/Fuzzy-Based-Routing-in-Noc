import math
import numpy as np
import skfuzzy as fuzz
import random 
import time
"""
MESH TOPOLOGY
1 2 3 4
. . . . 4
. . . . 3
. . . . 2
. . . . 1
"""
def XY_routing (id_s , id_d):
        if id_s == id_d:
                return 0
        
        else:
                #print "->",
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



def FXY_routing (id_s , id_d ):

        if id_s == id_d:
                return 0
        
        else:
                #print "->",
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
                                return FXY_routing(id_s-num_of_col ,id_d) + 1 + float(router[id_s]['input_south']+router[id_s-num_of_col]['input_north'])/16 + float(router[id_s-num_of_col]['total'])/40
                               
                        else:
                                #print "North",
                                return FXY_routing (id_s + num_of_col,id_d) + 1 + float(router[id_s]['input_north']+router[id_s+num_of_col]['input_south'])/16 + float(router[id_s+num_of_col]['total'])/40

                                
                elif y_s == y_d:
                        if x_s > x_d:
                                #print "West",
                                return FXY_routing(id_s-1,id_d) + 1 + float(router[id_s]['input_west']+router[id_s-1]['input_east'])/16 + float(router[id_s-1]['total'])/40
                                
                        else:
                                #print "East",
                                return FXY_routing(id_s+1,id_d) + 1 + float(router[id_s]['input_east']+router[id_s+1]['input_west'])/16 + float(router[id_s+1]['total'])/40
                                
                else:
                        if x_s < x_d and y_s < y_d:                                  
                                cost_x = compute_cost (router[id_s+1]['input_west'],router[id_s+1]['total']) 
                                cost_y = compute_cost (router[id_s+num_of_col]['input_south'],router[id_s+num_of_col]['total'])
                                if cost_x <= cost_y:
                                        #print "East", 
                                        return FXY_routing(id_s+1,id_d) + 1 + float(router[id_s]['input_east']+router[id_s+1]['input_west'])/16 + float(router[id_s+1]['total'])/40
                                else:
                                        #print "North",
                                        return FXY_routing (id_s + num_of_col,id_d) + 1 + float(router[id_s]['input_north']+router[id_s+num_of_col]['input_south'])/16 + float(router[id_s+num_of_col]['total'])/40

                                        
                                
                        if x_s > x_d and y_s > y_d:
                                cost_x = compute_cost (router[id_s-1]['input_east'],router[id_s-1]['total']) #
                                cost_y = compute_cost (router[id_s-num_of_col]['input_north'],router[id_s-num_of_col]['total'])
                                if cost_x <= cost_y:
                                        #print "West",
                                        return FXY_routing (id_s -1 , id_d) + 1 + float(router[id_s]['input_west']+router[id_s-1]['input_east'])/16 + float(router[id_s-1]['total'])/40
                                         
                                else:
                                        #print "South",
                                        return FXY_routing (id_s - num_of_col, id_d) + 1 + float(router[id_s]['input_south']+router[id_s-num_of_col]['input_north'])/16 + float(router[id_s-num_of_col]['total'])/40
                                        
                        if x_s > x_d and y_s < y_d:
                                cost_x = compute_cost (router[id_s-1]['input_east'],router[id_s-1]['total']) #
                                cost_y = compute_cost (router[id_s+num_of_col]['input_south'],router[id_s+num_of_col]['total'])
                                if cost_x <= cost_y:
                                        #print "West",
                                        return FXY_routing (id_s -1 , id_d) + 1 + float(router[id_s]['input_west']+router[id_s-1]['input_east'])/16 + float(router[id_s-1]['total'])/40
                                         
                                else:
                                        #print "North",
                                        return FXY_routing (id_s + num_of_col,id_d) + 1 + float(router[id_s]['input_north']+router[id_s+num_of_col]['input_south'])/16 + float(router[id_s+num_of_col]['total'])/40

                                        
                        if x_s < x_d and y_s > y_d:
                                cost_x = compute_cost (router[id_s+1]['input_west'],router[id_s+1]['total']) #
                                cost_y = compute_cost (router[id_s-num_of_col]['input_north'],router[id_s-num_of_col]['total'])
                                if cost_x <= cost_y:
                                        #print "East",
                                        return FXY_routing(id_s+1,id_d) + 1 + float(router[id_s]['input_east']+router[id_s+1]['input_west'])/16 + float(router[id_s+1]['total'])/40
                                         
                                else:
                                        #print "South",
                                        return FXY_routing (id_s - num_of_col, id_d) + 1 + float(router[id_s]['input_south']+router[id_s-num_of_col]['input_north'])/16 + float(router[id_s-num_of_col]['total'])/40
                                        
                                
                                
                                 
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

	#global tobff_ #= [[],[],[],[],[]]
        tobff_[0] = fuzz.trimf(total_buffer_occup , [0, 0, 10] )
        tobff_[1] = fuzz.trimf(total_buffer_occup , [0, 10, 20] )
        tobff_[2]  = fuzz.trimf(total_buffer_occup , [10, 20, 30] )
        tobff_[3]  = fuzz.trimf(total_buffer_occup , [20, 30, 40] )
        tobff_[4]  = fuzz.trimf(total_buffer_occup , [30, 40, 40] )

	#global r_cost_ #= [[],[],[],[],[]]
        r_cost_[0]  = fuzz.trimf(router_cost , [0, 0, 10] )
        r_cost_[1] = fuzz.trimf(router_cost , [0, 10, 20] )
        r_cost_[2]  = fuzz.trimf(router_cost , [10, 20, 30] )
        r_cost_[3]  = fuzz.trimf(router_cost , [20, 30, 40] )
        r_cost_[4]  = fuzz.trimf(router_cost , [30, 40, 40] )

        global value 
        value = [0 ,10,20 ,30 ,40]
        # , tobff_  , inbff_ ,  input_buffer_occup, total_buffer_occup , value
        #return compute_cost(_input, _total )
        
def compute_cost (_input , _total ):      
        _input_ = []
        _total_ = []
        for i in range(5):
                _input_.append(i)
                _total_ .append(i)
        rule = [[0,0,1,2,3],[0,1,1,2,3] ,[1,1,2,3,3],[2,2,3,4,4] , [3,3,4,4,4]]
	for i in range(5):
		 _input_[i] = fuzz.interp_membership(input_buffer_occup , inbff_[i],  _input)
		 _total_[i] = fuzz.interp_membership(total_buffer_occup , tobff_[i],  _total)
	"""		
        _input_[0] = fuzz.interp_membership(input_buffer_occup , inbff_[0],  _input)
        _input_[1] = fuzz.interp_membership(input_buffer_occup , inbff_[],  _input)
        _input_[2] = fuzz.interp_membership(input_buffer_occup , inbff_s,  _input)
        _input_[3] = fuzz.interp_membership(input_buffer_occup , inbff_m,  _input)
        _input_[4] = fuzz.interp_membership(input_buffer_occup , inbff_l,  _input)
        
        
        _total_[1]= fuzz.interp_membership(total_buffer_occup , tobff_vs,  _total)
        _total_[2] = fuzz.interp_membership(total_buffer_occup , tobff_s,  _total)
        _total_[3] = fuzz.interp_membership(total_buffer_occup , tobff_m,  _total)
        _total_[4] = fuzz.interp_membership(total_buffer_occup , tobff_l,  _total)
	"""
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



initialize ()

t = input ()
Pass = 0 
for i in range (2,8):
        Pass =0
        t1 = time.clock()
  	for j in range(t):
  	
		y = pow(2,i)
		x=y
		random.seed()
		source = random.randint(0,x*y-1)
		dest = random.randint (0,x*y-1)
		while source == dest:
		        dest = random.randint (0,x*y-1)
		router = [{'id':k,'input_north':random.randint(1,8),'input_west':random.randint(1,8),'input_south':random.randint(1,8),'input_east':random.randint(1,8),'noc':y , 'nor':x , 'total':0} for k in range(x*y+1)]
		for k in range(x*y):
		        router[k]['total'] = router[k]['input_north'] + router[k]['input_south'] + router[k]['input_west'] + router[k]['input_east']
		#for k in range(x*y):
		#       #print k , router[k]['input_east'] , router[k]['input_north'] , router[k]['input_south'] , router[k]['input_west'] , router[k]['total']
		##print "FXY"
		#print x ,source , dest
		fxy = FXY_routing(source,dest)
		##print 
		
		xy =  XY_routing(source,dest)
		##print fxy , xy , " next " 
		if ( float (fxy/xy) <=1 ):
		        Pass = Pass + 1;
		#else:
		#        print fxy , xy 
	t2 = time.clock() - t1
	
	print "Test Cycle = ", t
	print "Processing Time " , t2 ,"Sec"
	print "Topology 2-D Mesh (",x,"*",y,")"
	print "Accuracy = ", float (float(Pass*100) /t) , "%"
	print ""
