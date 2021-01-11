import arrow, requests, webbrowser
from tkinter import Tk, Label, Menu

start = arrow.now().floor('day')
end = arrow.now().ceil('day')

# insert your authoritization @ stormglass.io
authoritization_stormglass = "insert your api key here!!"

# insert your authoritization @ ipstack.com
authoritization_ipstack = "insert your api key here!!"

def fetch_info():
    ip = requests.get('http://checkip.dyndns.com/').text
    ip = [digit for digit in ip if digit.isdigit() or digit == '.']

    v1 = requests.get(
        f'http://api.ipstack.com/{"".join(ip)}?access_key={authoritization_ipstack}').json()

    info = [
        v1["latitude"],
        v1["longitude"],
    ]

    headers = {
        'Authorization': authoritization_stormglass
    }

    params = {
        'lat': info[0],
        'lng': info[1],
        'params': 'airTemperature,snowDepth,pressure',
        'start': start.to('UTC').timestamp,
        'end': end.to('UTC').timestamp
    }

    response = requests.get('https://api.stormglass.io/v2/weather/point',
                            params=params,
                            headers=headers
                            ).json()

    return {
        "airtemp": [
            response["hours"][0]["airTemperature"]["dwd"],
            response["hours"][0]["airTemperature"]["noaa"],
            response["hours"][0]["airTemperature"]["sg"]
        ],
        "location": [
            v1["country_name"],
            v1["city"]
        ],
        "snowdepth": [
            response["hours"][0]["snowDepth"]["noaa"],
            response["hours"][0]["snowDepth"]["sg"]
        ],
        "iopressure": [
            response["hours"][0]["pressure"]["noaa"],
            response["hours"][0]["pressure"]["sg"],
            response["hours"][0]["pressure"]["dwd"]
        ]
    }


def avg(arg):
    return round(sum(arg) / len(arg), 2)

def github_repo():
    webbrowser.open('https://github.com/Ammar-sys/weather_gui')

local_info = fetch_info()

root = Tk()
v1menu = Menu(root)
root.config(menu=v1menu)
root.geometry('500x150')
root.title(f'Weather | {local_info["location"][0]} | {local_info["location"][1]}')

v1menu.add_command(label='Github Repo', command=github_repo)

v1lab = Label(root, text=f'AirTemperature', font='Helvetica 10 bold')
v2lab = Label(root, text=f'\nAVG temperature: {avg(local_info["airtemp"])}℃'
                         f'\nDWD Station: {local_info["airtemp"][0]}℃'
                         f'\nNOAA Station: {local_info["airtemp"][1]}℃'
                         f'\nSG Station: {local_info["airtemp"][2]}℃'
              )
v3lab = Label(root, text='___________________________________________________________'
                         '_______________________________________')
v4lab = Label(root, text=f'SnowDepth', font='Helvetica 10 bold')
v5lab = Label(root, text=f'\nAVG depth: {avg(local_info["snowdepth"])}cm'
                         f'\nNOAA Station: {local_info["snowdepth"][0]}cm'
                         f'\nSG Station: {local_info["snowdepth"][1]}cm'
              )
v6lab = Label(root, text=f'AirPressure', font='Helvetica 10 bold')
v7lab = Label(root, text=f'\nAVG pressure: {avg(local_info["iopressure"])}hPa'
                         f'\nNOAA Station: {local_info["iopressure"][0]}hPa'
                         f'\nSG Station: {local_info["iopressure"][1]}hPa'
                         f'\nDWD Station: {local_info["iopressure"][2]}hPa'
              )

v1lab.place(x=10, y=20)
v2lab.place(x=10, y=50)
v3lab.place(x=0, y=0)
v4lab.place(x=180, y=20)
v5lab.place(x=180, y=50)
v6lab.place(x=350, y=20)
v7lab.place(x=350, y=50)

root.mainloop()
