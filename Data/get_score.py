import csv
import requests
from bs4 import BeautifulSoup

sv_valid = []
vf_data = []
score_data = []
file_path = 'list_score.txt'
base_url = "https://vaddict.b35.jp/user.php?player_id={}&dv=63&dl=262144&dd=511&dt=1&so=0"
# Variables

with open(file_path, 'r') as file:
    sv_codes = file.readlines()
# Read file

for id, sv_code in enumerate(sv_codes):
    if id % 50 == 0:
        print(f"Processed {id} data.")
    # Progress

    sv_code = sv_code.strip()
    full_url = base_url.format(sv_code)
    response = requests.get(full_url)
    if response.status_code != 200:
        continue
    # Check connection

    soup = BeautifulSoup(response.text, 'html.parser')
    user_info = soup.find('div', id='user_info')
    # Get html

    score_loop3 = user_info.find('div', id='score_loop3')
    scores = score_loop3.find_all('div', class_='score')
    if len(scores) < 100:
        continue
    # Get scores

    user_info = user_info.find('div', class_='text')
    user_info = user_info.find_all('td', class_='value')
    vf = user_info[4]
    vf = vf.find('a')
    vf = vf.get_text()
    # Get volforce

    score_num = [int(score.get_text()) for score in scores]
    score_num.reverse()
    data = [score if score >= 9000000 else 0 for score in score_num[:100]]

    sv_valid.append(sv_code)
    score_data.append(data)
    vf_data.append(vf)
# Get data

merged_data = [[sv, v] + d for sv, v, d in zip(sv_valid, vf_data, score_data)]

with open('data_score.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(merged_data)

print("Data extraction and CSV creation complete.")
# Write file
