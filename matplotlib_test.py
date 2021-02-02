"""
разные тесты для ускорения отображения графики в matplotlib.pyplot
варианты ускорения test_out1()..test_out4() позаимствованы у Bastian Bechtold
https://bastibe.de/2013-05-30-speeding-up-matplotlib.html

В.Симонов, vasily_simonov@mail.ru
"""

import matplotlib.pyplot as plt
import numpy as np
import time
import os

NPOINTS = 100 
TEST_TIME = 2

def test_out1():
    _, ax = plt.subplots()
    tstart = time.thread_time()
    num_plots = 0
    while time.thread_time()-tstart < TEST_TIME:
        ax.clear()
        ax.plot(np.random.randn(NPOINTS))
        ax.plot(np.random.randn(NPOINTS))
        plt.pause(1e-5)
        num_plots += 1  
    plt.close('all')
    print("test1 = {} frames per second".format(num_plots/TEST_TIME))

def test_out2():
    _, ax = plt.subplots()
    line, = ax.plot(np.random.randn(NPOINTS))
    line2, = ax.plot(np.random.randn(NPOINTS))

    tstart = time.thread_time()
    num_plots = 0
    while time.thread_time()-tstart < TEST_TIME:
        line.set_ydata(np.random.randn(NPOINTS))
        line2.set_ydata(np.random.randn(NPOINTS))
        plt.pause(1e-5)
        num_plots += 1
    plt.close('all')
    print("test2 = {} frames per second".format(num_plots/TEST_TIME))

def test_out3():
    fig, ax = plt.subplots()
    line, = ax.plot(range(NPOINTS),np.random.randn(NPOINTS))
    line2, = ax.plot(range(NPOINTS),np.random.randn(NPOINTS))
    plt.show(block=False)
    tstart = time.thread_time()
    num_plots = 0
    while time.thread_time()-tstart < TEST_TIME:
        line2.set_ydata(np.random.randn(NPOINTS))
        line.set_data(range(NPOINTS),np.random.randn(NPOINTS))
        fig.canvas.draw()
        fig.canvas.flush_events()
        num_plots += 1
    plt.close('all')
    print("test3 = {} frames per second".format(num_plots/TEST_TIME))

def test_out4():
    fig, ax = plt.subplots()
    line, = ax.plot(np.random.randn(NPOINTS))
    line2, = ax.plot(np.random.randn(NPOINTS))
    plt.show(block=False)
    fig.canvas.draw()
    tstart = time.thread_time()
    num_plots = 0
    while time.thread_time()-tstart < TEST_TIME:
        line.set_ydata(np.random.randn(NPOINTS))
        line2.set_ydata(np.random.randn(NPOINTS))
        ax.draw_artist(ax.patch)
        ax.draw_artist(line)
        ax.draw_artist(line2)
        fig.canvas.blit(ax.bbox)
        fig.canvas.flush_events()
        num_plots += 1
    plt.close('all')
    print("test4 = {} frames per second".format(num_plots/TEST_TIME))

def test_save1():
    """ простой savefig в формате png"""
    fig, ax = plt.subplots()
    line, = ax.plot(range(NPOINTS),np.random.randn(NPOINTS))
    line2, = ax.plot(range(NPOINTS),np.random.randn(NPOINTS))
    plt.show(block=False)
    tstart = time.thread_time()
    num_plots = 0
    total_time = 0
    while total_time < TEST_TIME:
        line2.set_ydata(np.random.randn(NPOINTS))
        line.set_data(range(NPOINTS),np.random.randn(NPOINTS))
        fig.canvas.draw()
        fig.canvas.flush_events()
        tstart = time.thread_time()
        fig.savefig("1.png")
        total_time += (time.thread_time()-tstart)
        num_plots += 1
    os.remove("1.png")
    plt.close('all')
    print("test_save1/png/ = {} saves per second ".format(num_plots/TEST_TIME))

def test_save2():
    """ imsave через захват образа с canvas. Не деградирует с числом точек"""
    fig, ax = plt.subplots()
    line, = ax.plot(range(NPOINTS),np.random.randn(NPOINTS))
    line2, = ax.plot(range(NPOINTS),np.random.randn(NPOINTS))
    plt.show(block=False)
    tstart = time.thread_time()
    num_plots = 0
    total_time = 0
    while total_time < TEST_TIME:
        line2.set_ydata(np.random.randn(NPOINTS))
        line.set_data(range(NPOINTS),np.random.randn(NPOINTS))
        fig.canvas.draw()
        fig.canvas.flush_events()
        tstart = time.thread_time()
        # speed optimization plt.savefig() hack 
        buf = fig.canvas.tostring_rgb()
        ncols, nrows = fig.canvas.get_width_height()
        rgb_image = np.frombuffer(buf, dtype=np.uint8).reshape(nrows, ncols, 3)
        plt.imsave("1.png",rgb_image)
        total_time += (time.thread_time()-tstart)
        num_plots += 1
    os.remove("1.png")
    plt.close('all')
    print("test_save2/binary png/ = {} saves per second ".format(num_plots/TEST_TIME))

def test_save3():
    """ savefig в формате jpeg. На некоторых системах работает быстрее png"""
    fig, ax = plt.subplots()
    line, = ax.plot(range(NPOINTS),np.random.randn(NPOINTS))
    line2, = ax.plot(range(NPOINTS),np.random.randn(NPOINTS))
    plt.show(block=False)
    tstart = time.thread_time()
    num_plots = 0
    total_time = 0
    while total_time < TEST_TIME:
        line2.set_ydata(np.random.randn(NPOINTS))
        line.set_data(range(NPOINTS),np.random.randn(NPOINTS))
        fig.canvas.draw()
        fig.canvas.flush_events()
        tstart = time.thread_time()
        fig.savefig("1.jpg")
        total_time += (time.thread_time()-tstart)
        num_plots += 1
    os.remove("1.jpg")
    plt.close('all')
    print("test_save3/jpg/ = {} saves per second ".format(num_plots/TEST_TIME))

def create_html_plotter():
    """ создать и запустить временную веб страницу для отображения картинки 1.png
    концепция позаимствована у Scott W Harden
    https://swharden.com/blog/2016-07-19-realtime-audio-visualization-in-python/"""
    with open("1.html","w") as f:
        print('<html>',file=f)
        print('<script language="javascript">',file=f)
        print('function RefreshImage(){',file=f)
        print('document.pic0.src="1.png?a=" + String(Math.random()*99999999);',file=f)
        print("setTimeout('RefreshImage()',50);",file=f)
        print('}',file=f)
        print('</script>',file=f)
        print('<body onload="RefreshImage()">',file=f)
        print('<img name="pic0" src="1.png">',file=f)
        print('</body>',file=f)
        print('</html>',file=f)
    os.system('1.html')

def main():
    global NPOINTS
    create_html_plotter()
    for p in [10,1000,100_0000]:
        NPOINTS = p
        print("\nNPOINTS = "+str(NPOINTS))
        test_out1()
        test_out2()
        test_out3()
        test_out4()
        test_save1()
        test_save2()
        test_save3()
    os.remove("1.html") # remove html plotter
    print('matplotlib.pyplot testing completed ')

if __name__=='__main__':
    main()