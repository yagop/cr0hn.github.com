import timeit
import aiohttp
import asyncio
import urllib.error
import urllib.request as req

from time import sleep
from multiprocessing import Pool
from threading import Thread, Semaphore
from random import randint


"""
Measure performance when download a lof of web pages
"""

CONCURRENCE = 0
URLS = 0


# --------------------------------------------------------------------------
# Download for threads
# --------------------------------------------------------------------------
# @profile
def download_threads(url, sem_threads):
    try:
        print(".")
        response = req.urlopen(url)
        data = response.read()
    except urllib.error.URLError:
        print("Thread error in URL: ", url)
    sem_threads.release()


# --------------------------------------------------------------------------
# Threads
# --------------------------------------------------------------------------
# @profile
def test_threads():

    sem_threads = Semaphore(CONCURRENCE)

    th = []
    th_append = th.append
    for page in URLS:
        sem_threads.acquire()
        t = Thread(target=download_threads, args=(page, sem_threads))
        t.start()
        th_append(t)

    # Wait for threads ends
    for x in th:
        x.join()


# --------------------------------------------------------------------------
# Processes
# --------------------------------------------------------------------------
# @profile
def download_processes(url):
    try:
        response = req.urlopen(url, )
        data = response.read()
    except urllib.error.URLError:
        print("Process Error in URL: ", url)


# ----------------------------------------------------------------------
# @profile
def test_processes():
    mp = Pool(CONCURRENCE)
    mp.map(download_processes, URLS)


# --------------------------------------------------------------------------
# Python 3 Coroutines
# --------------------------------------------------------------------------
@asyncio.coroutine
# @profile
def download_coroutine(url, sem_coroutines):
    # conn = aiohttp.ProxyConnector(proxy=PROXY)
    with (yield from sem_coroutines):
        # response = yield from aiohttp.request('GET', url, connector=conn)
        response = yield from aiohttp.request('GET', url)
        data = (yield from response.read())
        # asyncio.sleep(0.01)
    # response = yield from aiohttp.request('GET', url, compress=True)
    # data = (yield from response.read())

    # response = yield from aiohttp.request('GET', url)
    # data = (yield from response.read())

@asyncio.coroutine
# ----------------------------------------------------------------------
def hh():
    """Comment"""
    print("sss")
    return 1


# ----------------------------------------------------------------------
# @profile
def test_coroutines():
    # f = asyncio.wait([download_coroutine(page, sem_coroutines) for page in URLS])

    # sem_coroutines = asyncio.Semaphore(CONCURRENCE)
    # loop = asyncio.get_event_loop()
    # print(dir(loop))
    # for x in dir(loop):
    #     if "task" in x:
    #         print(x)
    # print(vars(loop))

    loop = asyncio.get_event_loop()
    for x in dir(asyncio):
        print(x)
    return
    tasks = [
        loop.create_task(hh()),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    # tasks = [loop.create_task(download_coroutine(page, sem_coroutines)) for page in URLS]
    # loop.run_until_complete(asyncio.wait(tasks))

# import urllib.request as req
# PROXY = "http://172.31.219.30:8080"
# hc = req.HTTPCookieProcessor()
# proxy = req.ProxyHandler({'http': PROXY})
# opener = req.build_opener(hc, proxy)
# req.install_opener(opener)

# --------------------------------------------------------------------------
# Time it!
# --------------------------------------------------------------------------
if __name__ == '__main__':
    BASE_URL = [
        # "http://www.bing.com/search?q=%s&go=&qs=n&form=QBLH&filt=all&pq=hello&sc=8-1&sp=-1&sk=&cvid=3c6b1fd5cbe0456b8c2370b57dc7ad38",
        # "https://www.google.es/webhp?tab=ww&ei=AtXPU_ivMuyR1AWivIGIDg&ved=0CBAQ1S4#q=%s",
        # "http://buscador.terra.es/Default.aspx?source=Search&ca=l&query=%s",
        # "https://es.search.yahoo.com/search;_ylt=AnJ6euGJruAwoFqdrV3z9Npdoq5_?p=%s&toggle=1&cop=mss&ei=UTF-8&fr=yfp-t-907&fp=1"
        # "http://www.navajanegra.com/%s"
        # "http://golismero.com/%s",
        "https://www.youtube.com/results?search_query=%s"
        # "http://127.0.0.1:8000/index.html"
    ]
    # BASE_URL_LEN = len(BASE_URL)


    testing_cases = {
        "Python 3 coroutines": "test_coroutines",
        # "Threads": "test_threads",
        # "Processes": "test_processes",
    }

    print("[*] Starting test")
    # for requests in [50, 100, 200]:
    for requests in [50]:
        print(" " * 3, "- Requesting %s URLs:" % requests)

        # for i, concurrence in enumerate([5, 10, 15]):
        for i, concurrence in enumerate([5, 15]):
            print(" " * 5, "+ concurrence %s:" % concurrence)

            # URLS = [BASE_URL[randint(0, BASE_URL_LEN - 1)] % w for w in range(requests)]
            URLS = [BASE_URL[0] for w in range(requests)]

            CONCURRENCE = concurrence
            # URLS = ["http://upload.wikimedia.org/wikipedia/commons/3/37/African_Bush_Elephant.jpg"
            #         for w in range(requests)]

            for case_name, case_function in testing_cases.items():
                # print(case_name, globals()[case_function]())
                print(" " * 8, "> ", case_name,  "time: ",
                      timeit.timeit("%s()" % case_function, setup="from __main__ import %s" % case_function, number=1),
                      "seconds")
                # sleep(1)

    print("[*] Tests end")