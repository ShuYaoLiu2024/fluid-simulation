import time

def func_pipe1(conn, p_id):
	time.sleep(1)
	while 1:
		time.sleep(2)
		conn.send(time.time())
    

    

    


def func_pipe2(conn, p_id):
	
	for i in range(2):
		rec = conn.recv()
		print(p_id, 'recv', rec)


def run__pipe():
    from multiprocessing import Process, Pipe

    conn1, conn2 = Pipe()
    
    process = [Process(target=func_pipe1, args=(conn1, 'I1')),]

    [p.start() for p in process]
    
    while 1:
    	rec = conn2.recv()
    	print('recv', rec)
    #process[1].terminate()
    
    #[p.join() for p in process]

if __name__ =='__main__':
    run__pipe()