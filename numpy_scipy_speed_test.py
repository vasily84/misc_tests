"""
различные тесты скорости функций из numpy и scipy.
свободная лицензия
В.Симонов, 2-фев-2021 vasily_simonov@mail.ru
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
import platform,time,scipy,os

def comp_info():
    """ выводит на экран информацию о системе на которой запущена"""
    print('os = '+str(platform.platform()))
    print('python implementation = '+str(platform.python_implementation()))
    print('python compiler = '+str(platform.python_compiler()))
    print('python ver = '+str(platform.python_version()))
    print('numpy ver = '+str(np.version.version))
    print('scipy version = '+str(scipy.version.version))
    print('')
    print('processor = '+str(platform.processor()))
    if platform.system()=='Windows':
        os.system('wmic cpu get L2CacheSize, L2CacheSpeed, L3CacheSize, L3CacheSpeed')
        print('KB')

def test_time_sort_int(Nsize,kind=None,dtype = np.int32):
    """ измерить время сортировки массива."""
    A = np.random.randint(-1000,1000,Nsize,dtype=dtype)    
    tstart = time.thread_time() # process_time()
    A.sort(kind=kind)
    time1 = time.thread_time()-tstart
    return time1

def test_sort(Nmax = 10_000_000):
    """
    сравнительный тест скорости сортировок массивов numpy разными алгоритмами.
    """  
    fig, ax = plt.subplots()
    sort_kinds = ('quicksort','heapsort','mergesort')
    for k in sort_kinds:
        Nmark = []
        speedMark = []
        N = 2
        while int(N)<Nmax:
            r = test_time_sort_int(int(N),kind=k,dtype=np.int32)
            print("{} N = {} time = {}".format(k,N,r))
            Nmark.append(int(N))
            speedMark.append(r)
            N = N*1.155

        ax.plot(Nmark,speedMark,label = k)
    ax.legend()
    plt.title('sort speed test')
    plt.xlabel('array len, [N]')
    plt.ylabel('time, [s]')
    plt.savefig('sort_speed_test.png')
    plt.show()
    

def test_time_rfft(Nsize,Nfft=None):
    """ измерить время быстрого преобразования Фурье."""
    if Nfft is None:
        Nfft = len(Nsize)

    A = np.random.random(Nsize)    
    tstart = time.thread_time() # process_time()
    B = fft.rfft(A,Nfft,overwrite_x=True)
    time1 = time.thread_time()-tstart
    return time1

def test_rfft(Nmax = 1_000_000):
    """ измерить скорость RFFT - БПФ для действительных чисел.
    сравнивает варианты с неизменной длиной входных данных и дополненных
    до оптимальной длины .next_fast_len() """

    fig, ax = plt.subplots()
    for k in ('len(N)','next_fast_len()'):
        Nmark = []
        speedMark = []
        N = 2
        while int(N)<Nmax:
            if k=='len(N)':
                L=int(N)
            else:
                L=fft.next_fast_len(int(N),False)
            
            r = test_time_rfft(int(N),L)
            print("{} N = {} time = {}".format(k,N,r))
            Nmark.append(int(N))
            speedMark.append(r)
            N = N*1.01
            

        ax.plot(Nmark,speedMark,label = k)

    ax.legend()
    plt.title('scipy rfft speed test')
    plt.xlabel('array len, [N]')
    plt.ylabel('time, [s]')
    plt.savefig('rfft_speed_test.png')
    plt.show()
    
def test_time_matmul(Ax,Bx,dtype=np.int32):
    """ измерить время умножения матриц """
    A = np.random.randint(-1000,1000,Ax*Bx,dtype=dtype).reshape(Ax,Bx)
    B = np.random.randint(-1000,1000,Ax*Bx,dtype=dtype).reshape(Bx,Ax)
    tstart = time.thread_time() # process_time()
    C = np.matmul(A,B)
    time1 = time.thread_time()-tstart
    return time1

def test_matmul(Nmax = 1_000):
    """ измерить скорость вычисления произведения матриц """  
    fig, ax = plt.subplots()
   
    Nmark = []
    speedMark = []
    N = 2
    while int(N)<Nmax:
        r = test_time_matmul(int(N),int(N))
        print("matmul N*N N = {} time = {}".format(N,r))
        Nmark.append(int(N)*int(N))
        speedMark.append(r)
        N += 10

    ax.plot(Nmark,speedMark)
    plt.title('numpy matmul speed test')
    plt.xlabel('matrix total len, [N*N]')
    plt.ylabel('time, [s]')
    plt.savefig('numpy_matmul_speed_test.png')
    plt.show()

def test_time_inv_matrix(Ax,Bx,dtype=np.int32):
    A = np.random.randint(-1000,1000,Ax*Bx,dtype=dtype).reshape(Ax,Bx)
    tstart = time.thread_time() # process_time()
    back_A = np.linalg.inv(A)
    time1 = time.thread_time()-tstart
    return time1


def test_inv_matrix(Nmax = 3_000):   
    fig, ax = plt.subplots()
   
    Nmark = []
    speedMark = []
    N = 2
    while int(N)<Nmax:
        r = test_time_inv_matrix(int(N),int(N))
        print("matrix inverse N*N N = {} time = {}".format(N,r))
        Nmark.append(int(N)*int(N))
        speedMark.append(r)
        N += 10

    ax.plot(Nmark,speedMark)
    plt.title('numpy matrix inverse speed test')
    plt.xlabel('matrix total len, [N*N]')
    plt.ylabel('time, [s]')
    plt.savefig('numpy_matrix_inverse_test.png')
    plt.show()

def main():
    comp_info() 
    test_sort()
    test_rfft()
    test_matmul()
    test_inv_matrix()

if __name__ =='__main__':
    main()