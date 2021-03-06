import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as plt
from collections import Counter
from sklearn import preprocessing

# 한글 폰트 안 깨지게하기위한 import
import matplotlib.font_manager as fm

# 가져올 폰트 지정
font_location='E:/글꼴/H2GTRE.TTF'
# 폰트 이름 지정 
font_name=fm.FontProperties(fname=font_location).get_name()
mpl.rc('font',family=font_name)

# 시즌을 count를 할 갯수
count = 10
# 시작 년도
syear = 8


def data_norm(table):
    col = table.columns
    
    # 데이터 정규화 과정
    x = table[col].values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x.astype(float))
    table = pd.DataFrame(x_scaled,
                         columns=col,
                         index=table.index)
    return table

def convert_negative(table,name):
    for loop  in range(0,len(table.columns)):
        if len(table.columns[loop])==2:
            if(table.columns[loop][-1]==name):
                table[table.columns[loop]] = table[table.columns[loop]]*-1

# =====================================================================7년치 시즌 데이터 ===================================================================

# 플레이오프 진출 요인들 담을 리스트
M_factor_list = [[] for i in range(count)]
F_factor_list = [[] for i in range(count)]
Mcount = []
Fcount = []

Mdata = []
Fdata = []

# 시즌 결과 데이터를 저장한다.
for year in range(syear,18):
    kovo_Mresult_table = pd.read_pickle('Kovo_Male_result_table(%s-%s)'%(str(year),str(year+1)))
    kovo_Fresult_table = pd.read_pickle('Kovo_Female_result_table(%s-%s)'%(str(year),str(year+1)))
    
    # 플레이오프와 관련없는 순위/팀/경기수/세트수에 대한 데이터 제거
    for i in range(7,72):
        if i ==7:   
            if kovo_Mresult_table.columns[i][1]=='순위':
               for index in range(i,i+3):
                   del kovo_Mresult_table[kovo_Mresult_table.columns[i]]
                   del kovo_Fresult_table[kovo_Fresult_table.columns[i]]
        else:
            if kovo_Mresult_table.columns[i][1]=='순위':
               for index in range(i,i+4):
                   del kovo_Mresult_table[kovo_Mresult_table.columns[i]]
                   del kovo_Fresult_table[kovo_Fresult_table.columns[i]]

    # 시즌 승패결과를 Season_data를 저장
    Season_male_data = pd.read_pickle('Male_Season(%s-%s)'%(str(year),str(year+1)))
    Season_female_data = pd.read_pickle('Female_Season(%s-%s)'%(str(year),str(year+1)))
    
    # 시즌의 순위를 남녀 Team_name에 저장한다.
    Male_team_name = kovo_Mresult_table.index
    Female_team_name = kovo_Fresult_table.index
    
    # 남년 최다연승 최다연패을 저장할 배열을 생성한다.
    Male_win_score = np.zeros(len(Male_team_name))
    Male_lose_score = np.zeros(len(Male_team_name))
    Female_win_score = np.zeros(len(Female_team_name))
    Female_lose_score = np.zeros(len(Female_team_name))
    win = 0
    lose = 0
        
    # 남자팀의 최다 연승 최다 연패를 계산하여 배열에 저장한다.
    for team in range(len(Male_team_name)):
        for index in range(len(Season_male_data)):
            if Season_male_data["홈"][index] == Male_team_name[team] and Season_male_data["승패"][index] == "승" or Season_male_data["상대팀"][index] == Male_team_name[team] and Season_male_data["승패"][index] == "패":
                win += 1
                lose = 0
                if Male_win_score[team] < win:
                    Male_win_score[team] = win
            elif Season_male_data["홈"][index] == Male_team_name[team] and Season_male_data["승패"][index] == "패" or Season_male_data["상대팀"][index] == Male_team_name[team] and Season_male_data["승패"][index] == "승":
                lose+=1
                win = 0
                if Male_lose_score[team] < lose:
                    Male_lose_score[team] = lose
    
    # 여자팀 최다 연승 최다 연패를 계산하여 저장한다.
    for team in range(len(Female_team_name)):
        for index in range(len(Season_female_data)):
            if Season_female_data["홈"][index] == Female_team_name[team] and Season_female_data["승패"][index] == "승" or Season_female_data["상대팀"][index] == Female_team_name[team] and Season_female_data["승패"][index] == "패":
                win += 1
                lose = 0
                if Female_win_score[team] < win:
                    Female_win_score[team] = win
            elif Season_female_data["홈"][index] == Female_team_name[team] and Season_female_data["승패"][index] == "패" or Season_female_data["상대팀"][index] == Female_team_name[team] and Season_female_data["승패"][index] == "승":
                lose+=1
                win = 0
                if Female_lose_score[team] < lose:
                    Female_lose_score[team] = lose
    
    Male_attack_efficiency =  ((kovo_Mresult_table[('공격', '성공')]-kovo_Mresult_table[('공격', '공격차단')]-kovo_Mresult_table[('공격', '범실')])/kovo_Mresult_table[('공격', '시도')])*100
    Female_attack_efficiency = ((kovo_Fresult_table[('공격', '성공')]-kovo_Fresult_table[('공격', '공격차단')]-kovo_Fresult_table[('공격', '범실')])/kovo_Fresult_table[('공격', '시도')])*100
    Male_open_attack_efficiency =  ((kovo_Mresult_table[('오픈공격', '성공')]-kovo_Mresult_table[('오픈공격', '공격차단')]-kovo_Mresult_table[('오픈공격', '범실')])/kovo_Mresult_table[('오픈공격', '시도')])*100
    Female_open_attack_efficiency =  ((kovo_Fresult_table[('오픈공격', '성공')]-kovo_Fresult_table[('오픈공격', '공격차단')]-kovo_Fresult_table[('오픈공격', '범실')])/kovo_Fresult_table[('오픈공격', '시도')])*100
    Male_time_attack_efficiency =  ((kovo_Mresult_table[('시간차공격', '성공')]-kovo_Mresult_table[('시간차공격', '공격차단')]-kovo_Mresult_table[('시간차공격', '범실')])/kovo_Mresult_table[('시간차공격', '시도')])*100
    Female_time_attack_efficiency = ((kovo_Fresult_table[('시간차공격', '성공')]-kovo_Fresult_table[('시간차공격', '공격차단')]-kovo_Fresult_table[('시간차공격', '범실')])/kovo_Fresult_table[('시간차공격', '시도')])*100
    Male_moving_attack_efficiency =  ((kovo_Mresult_table[('이동공격', '성공')]-kovo_Mresult_table[('이동공격', '공격차단')]-kovo_Mresult_table[('이동공격', '범실')])/kovo_Mresult_table[('이동공격', '시도')])*100
    Female_moving_attack_efficiency = ((kovo_Fresult_table[('이동공격', '성공')]-kovo_Fresult_table[('이동공격', '공격차단')]-kovo_Fresult_table[('이동공격', '범실')])/kovo_Fresult_table[('이동공격', '시도')])*100
    Male_back_attack_efficiency =  ((kovo_Mresult_table[('후위공격', '성공')]-kovo_Mresult_table[('후위공격', '공격차단')]-kovo_Mresult_table[('후위공격', '범실')])/kovo_Mresult_table[('후위공격', '시도')])*100
    Female_back_attack_efficiency = ((kovo_Fresult_table[('후위공격', '성공')]-kovo_Fresult_table[('후위공격', '공격차단')]-kovo_Fresult_table[('후위공격', '범실')])/kovo_Fresult_table[('후위공격', '시도')])*100
    Male_quick_attack_efficiency =  ((kovo_Mresult_table[('속공', '성공')]-kovo_Mresult_table[('속공', '공격차단')]-kovo_Mresult_table[('속공', '범실')])/kovo_Mresult_table[('속공', '시도')])*100
    Female_quick_attack_efficiency = ((kovo_Fresult_table[('속공', '성공')]-kovo_Fresult_table[('속공', '공격차단')]-kovo_Fresult_table[('속공', '범실')])/kovo_Fresult_table[('속공', '시도')])*100
    Male_quick_open_efficiency =  ((kovo_Mresult_table[('퀵오픈', '성공')]-kovo_Mresult_table[('퀵오픈', '공격차단')]-kovo_Mresult_table[('퀵오픈', '범실')])/kovo_Mresult_table[('퀵오픈', '시도')])*100
    Female_quick_open_efficiency = ((kovo_Fresult_table[('퀵오픈', '성공')]-kovo_Fresult_table[('퀵오픈', '공격차단')]-kovo_Fresult_table[('퀵오픈', '범실')])/kovo_Fresult_table[('퀵오픈', '시도')])*100
    Male_serve_efficiency =  ((kovo_Mresult_table[('서브', '성공')]-kovo_Mresult_table[('서브', '범실')])/kovo_Mresult_table[('서브', '시도')])*100
    Female_serve_efficiency = ((kovo_Fresult_table[('서브', '성공')]-kovo_Fresult_table[('서브', '범실')])/kovo_Fresult_table[('서브', '시도')])*100
    Male_blocking_efficiency =  ((kovo_Mresult_table[('블로킹', '성공')]+kovo_Mresult_table[('블로킹', '유효블락')]+kovo_Mresult_table[('블로킹', '어시스트')]-kovo_Mresult_table[('블로킹', '범실')]-kovo_Mresult_table[('블로킹', '실패')])/kovo_Mresult_table[('블로킹', '시도')])*100
    Female_blocking_efficiency = ((kovo_Fresult_table[('블로킹', '성공')]+kovo_Fresult_table[('블로킹', '유효블락')]+kovo_Fresult_table[('블로킹', '어시스트')]-kovo_Fresult_table[('블로킹', '범실')]-kovo_Fresult_table[('블로킹', '실패')])/kovo_Fresult_table[('블로킹', '시도')])*100
    Male_dig_efficiency =  ((kovo_Mresult_table[('디그', '성공')]-kovo_Mresult_table[('디그', '실패')]-kovo_Mresult_table[('디그', '범실')])/kovo_Mresult_table[('디그', '시도')])*100
    Female_dig_efficiency = ((kovo_Fresult_table[('디그', '성공')]-kovo_Fresult_table[('디그', '실패')]-kovo_Fresult_table[('디그', '범실')])/kovo_Fresult_table[('디그', '시도')])*100
    Male_set_efficiency =  ((kovo_Mresult_table[('세트', '성공')]-kovo_Mresult_table[('세트', '범실')])/kovo_Mresult_table[('세트', '시도')])*100
    Female_set_efficiency = ((kovo_Fresult_table[('세트', '성공')]-kovo_Fresult_table[('세트', '범실')])/kovo_Fresult_table[('세트', '시도')])*100
    Male_receive_efficiency =  ((kovo_Mresult_table[('리시브', '정확')]-kovo_Mresult_table[('리시브', '범실')])/kovo_Mresult_table[('리시브', '시도')])*100
    Female_receive_efficiency = ((kovo_Fresult_table[('리시브', '정확')]-kovo_Fresult_table[('리시브', '범실')])/kovo_Fresult_table[('리시브', '시도')])*100
    
    import Analysis_practice as As
    
    # 임시로 플레이오프 진출한 팀에 대한 내용을 추가했다.
    Male_play_off = []
    Female_play_off = []
    
    # 1은 진출했다는 의미 / 0은 진출하지 못하였다는 의미
    for index in range(len(kovo_Mresult_table)) :
        if index<3:
            Male_play_off.append(1)
        else:
            # 11년도 시즌 이후부터는 4등과 3등의 승점이 3점 이내일 경우 플레이오프에 진출하므로 조건을 추가해줘야 한다.
            if year>10 and index==3 and kovo_Mresult_table.iloc[2]["승점"]-kovo_Mresult_table.iloc[3]["승점"]<=3:
                Male_play_off.append(1)
            else:
                Male_play_off.append(0)
    
    for index in range(len(kovo_Fresult_table)) :
        if index<3:
            Female_play_off.append(1)
        else:
            Female_play_off.append(0)
        
    # 공격 효율이라는 항목을 추가하므로 공격파트에 추가를 해줘야 보기 편하기에 삽입하였다.
    kovo_Mresult_table.insert(loc=16,column="공격_효율",value=Male_attack_efficiency)
    kovo_Fresult_table.insert(loc=16,column="공격_효율",value=Female_attack_efficiency)
    kovo_Mresult_table.insert(loc=22,column="오픈공격_효율",value=Male_open_attack_efficiency)
    kovo_Fresult_table.insert(loc=22,column="오픈공격_효율",value=Female_open_attack_efficiency)
    kovo_Mresult_table.insert(loc=28,column="시간차공격_효율",value=Male_time_attack_efficiency)
    kovo_Fresult_table.insert(loc=28,column="시간차공격_효율",value=Female_time_attack_efficiency)
#    NaN값이 많아서 추가하지 않았다.
#    kovo_Mresult_table.insert(loc=34,column="이동공격_효율",value=Male_moving_attack_efficiency)
#    kovo_Fresult_table.insert(loc=34,column="이동공격_효율",value=Female_moving_attack_efficiency)
    kovo_Mresult_table.insert(loc=39,column="후위공격_효율",value=Male_back_attack_efficiency)
    kovo_Fresult_table.insert(loc=39,column="후위공격_효율",value=Female_back_attack_efficiency)
    kovo_Mresult_table.insert(loc=45,column="속공_효율",value=Male_quick_attack_efficiency)
    kovo_Fresult_table.insert(loc=45,column="속공_효율",value=Female_quick_attack_efficiency)
    kovo_Mresult_table.insert(loc=51,column="퀵오픈_효율",value=Male_quick_open_efficiency)
    kovo_Fresult_table.insert(loc=51,column="퀵오픈_효율",value=Female_quick_open_efficiency)
    kovo_Mresult_table.insert(loc=56,column="서브_효율",value=Male_serve_efficiency)
    kovo_Fresult_table.insert(loc=56,column="서브_효율",value=Female_serve_efficiency)
    kovo_Mresult_table.insert(loc=64,column="블로킹_효율",value=Male_blocking_efficiency)
    kovo_Fresult_table.insert(loc=64,column="블로킹_효율",value=Female_blocking_efficiency)
    kovo_Mresult_table.insert(loc=70,column="디그_효율",value=Male_dig_efficiency)
    kovo_Fresult_table.insert(loc=70,column="디그_효율",value=Female_dig_efficiency)
    kovo_Mresult_table.insert(loc=75,column="세트_효율",value=Male_set_efficiency)
    kovo_Fresult_table.insert(loc=75,column="세트_효율",value=Female_set_efficiency)
    kovo_Mresult_table.insert(loc=80,column="리시브_효율",value=Male_receive_efficiency)
    kovo_Fresult_table.insert(loc=80,column="리시브_효율",value=Female_receive_efficiency)
    
    kovo_Mresult_table["최다연승"] = Male_win_score
    kovo_Mresult_table["최다연패"] = Male_lose_score   
    kovo_Fresult_table["최다연승"] = Female_win_score
    kovo_Fresult_table["최다연패"] = Female_lose_score
    kovo_Mresult_table["플레이오프진출"] = Male_play_off
    kovo_Fresult_table["플레이오프진출"] = Female_play_off
    
    if year<=10:
        del kovo_Mresult_table["승률"]
        del kovo_Fresult_table["승률"]
    else:
        del kovo_Mresult_table["승점"]
        del kovo_Fresult_table["승점"]
    
    # 해당 데이터에서 낮으면 긍정적인 값들을 음수값으로 변경해준다.
    convert_negative(kovo_Mresult_table,'공격차단')
    convert_negative(kovo_Fresult_table,'공격차단')
    convert_negative(kovo_Mresult_table,'범실')
    convert_negative(kovo_Fresult_table,'범실')
    convert_negative(kovo_Mresult_table,'실패')
    convert_negative(kovo_Fresult_table,'실패')
    convert_negative(kovo_Mresult_table,'최다연패')
    convert_negative(kovo_Fresult_table,'최다연패')
    
    Mdata.append(kovo_Mresult_table)
    Fdata.append(kovo_Fresult_table)
    
# Male_data와 Female_data로 합친다.
Male_data = pd.concat([Mdata[0],Mdata[1],Mdata[2],Mdata[3],Mdata[4],Mdata[5],Mdata[6],Mdata[7],Mdata[8],Mdata[9]])
Female_data = pd.concat([Fdata[0],Fdata[1],Fdata[2],Fdata[3],Fdata[4],Fdata[5],Fdata[6],Fdata[7],Fdata[8],Fdata[9]])

# 10년치의 데이터를 합친(공격효율,최다연승,최다연패,플레이오프진출)
Male_data.to_pickle("Total_M_Data")
Female_data.to_pickle("Total_F_Data")

# 플레이오프와 관계없는 데이터를 제거한다

def delete_feature(table,name):
    del table[name]
    
delete_feature(Male_data,'경기수')
delete_feature(Female_data,'경기수')
delete_feature(Male_data,'순위')
delete_feature(Female_data,'순위')
delete_feature(Male_data,'승')
delete_feature(Female_data,'승')
delete_feature(Male_data,'패')
delete_feature(Female_data,'패')
delete_feature(Male_data,'세트득실률')
delete_feature(Female_data,'세트득실률')
delete_feature(Male_data,'점수득실률')
delete_feature(Female_data,'점수득실률')

def change_name(table):
    for loop in range(0,len(table.columns)):
        # 튜플로 된 이름들은 길이가 2이므로
        if len(table.columns[loop])==2:
            # 득점,벌칙,범실은 2개가 겹치므로 하나만 넣어준다.
            if (table.columns[loop][-1]=='득점' and table.columns[loop][-2]=='득점') or (table.columns[loop][-1]=='벌칙' and table.columns[loop][-2]=='벌칙') or (table.columns[loop][-1]=='범실' and table.columns[loop][-2]=='범실'):
                table.rename(columns={table.columns[loop]:table.columns[loop][-2]},inplace='True')
            else:
                table.rename(columns={table.columns[loop]:table.columns[loop][-2]+'_'+table.columns[loop][-1]},inplace='True')


change_name(Male_data)
change_name(Female_data)

delete_feature(Male_data,'벌칙')
delete_feature(Female_data,'벌칙')

# 임시로 엑셀파일을 만들어 둔다
#Male_data.to_excel('male.xlsx')
#Female_data.to_excel('female.xlsx')

Mplayoff = Male_data['플레이오프진출']
del Male_data['플레이오프진출']
Fplayoff = Female_data['플레이오프진출']
del Female_data['플레이오프진출']

# 전체 데이터를 정규화 한다.(전체 데이터를 다 받고 정규화)
Male_data_norm = data_norm(Male_data)
Female_data_norm = data_norm(Female_data)

# 주요요인 추출
# 전체경기요인
#Extract_M_Data = Male_data_norm[['득점_공격', '득점_블로킹', '득점_서브', '득점', '공격_시도', '공격_성공', '공격_공격차단', '공격_범실',
#       '공격_성공률','공격_효율','오픈공격_시도', '오픈공격_성공', '오픈공격_공격차단', '오픈공격_범실',
#       '오픈공격_성공률','오픈공격_효율','시간차공격_시도', '시간차공격_성공', '시간차공격_공격차단', '시간차공격_범실',
#       '시간차공격_성공률','시간차공격_효율','이동공격_시도', '이동공격_성공', '이동공격_공격차단', '이동공격_범실', '이동공격_성공률',
#       '후위공격_시도', '후위공격_성공', '후위공격_공격차단', '후위공격_범실', '후위공격_성공률','후위공격_효율', '속공_시도',
#       '속공_성공', '속공_공격차단', '속공_범실', '속공_성공률','속공_효율', '퀵오픈_시도', '퀵오픈_성공', '퀵오픈_공격차단',
#       '퀵오픈_범실', '퀵오픈_성공률','퀵오픈_효율', '서브_시도', '서브_성공', '서브_범실', '서브_세트당평균','서브_효율', '블로킹_시도',
#       '블로킹_성공', '블로킹_유효블락', '블로킹_실패', '블로킹_범실', '블로킹_어시스트', '블로킹_세트당평균','블로킹_효율',
#       '디그_시도', '디그_성공', '디그_실패', '디그_범실', '디그_세트당평균','디그_효율', '세트_시도', '세트_성공',
#       '세트_범실', '세트_세트당평균','세트_효율', '리시브_시도', '리시브_정확', '리시브_범실', '리시브_세트당평균','리시브_효율', '범실']]
#Extract_F_Data = Female_data_norm[['득점_공격', '득점_블로킹', '득점_서브', '득점', '공격_시도', '공격_성공', '공격_공격차단', '공격_범실',
#       '공격_성공률','공격_효율','오픈공격_시도', '오픈공격_성공', '오픈공격_공격차단', '오픈공격_범실',
#       '오픈공격_성공률','오픈공격_효율','시간차공격_시도', '시간차공격_성공', '시간차공격_공격차단', '시간차공격_범실',
#       '시간차공격_성공률','시간차공격_효율','이동공격_시도', '이동공격_성공', '이동공격_공격차단', '이동공격_범실', '이동공격_성공률',
#       '후위공격_시도', '후위공격_성공', '후위공격_공격차단', '후위공격_범실', '후위공격_성공률','후위공격_효율', '속공_시도',
#       '속공_성공', '속공_공격차단', '속공_범실', '속공_성공률','속공_효율', '퀵오픈_시도', '퀵오픈_성공', '퀵오픈_공격차단',
#       '퀵오픈_범실', '퀵오픈_성공률','퀵오픈_효율', '서브_시도', '서브_성공', '서브_범실', '서브_세트당평균','서브_효율', '블로킹_시도',
#       '블로킹_성공', '블로킹_유효블락', '블로킹_실패', '블로킹_범실', '블로킹_어시스트', '블로킹_세트당평균','블로킹_효율',
#       '디그_시도', '디그_성공', '디그_실패', '디그_범실', '디그_세트당평균','디그_효율', '세트_시도', '세트_성공',
#       '세트_범실', '세트_세트당평균','세트_효율', '리시브_시도', '리시브_정확', '리시브_범실', '리시브_세트당평균','리시브_효율', '범실']]
# 공격파트
#Extract_M_Data = Male_data_norm[['공격_시도', '공격_성공', '공격_공격차단', '공격_범실','공격_성공률','공격_효율']]
#Extract_F_Data = Female_data_norm[['공격_시도', '공격_성공', '공격_공격차단', '공격_범실','공격_성공률','공격_효율']]
# 오픈공격파트
#Extract_M_Data = Male_data_norm[['오픈공격_시도', '오픈공격_성공', '오픈공격_공격차단', '오픈공격_범실','오픈공격_성공률', '오픈공격_효율']]
#Extract_F_Data = Female_data_norm[['오픈공격_시도', '오픈공격_성공', '오픈공격_공격차단', '오픈공격_범실','오픈공격_성공률','오픈공격_효율']]
# 시간차공격
#Extract_M_Data = Male_data_norm[['시간차공격_시도', '시간차공격_성공', '시간차공격_공격차단', '시간차공격_범실','시간차공격_성공률','시간차공격_효율']]
#Extract_F_Data = Female_data_norm[['시간차공격_시도', '시간차공격_성공', '시간차공격_공격차단', '시간차공격_범실','시간차공격_성공률','시간차공격_효율']]
# 이동공격
#Extract_M_Data = Male_data_norm[['이동공격_시도', '이동공격_성공', '이동공격_공격차단', '이동공격_범실']]
#Extract_F_Data = Female_data_norm[['이동공격_시도', '이동공격_성공', '이동공격_공격차단', '이동공격_범실']]
# 후위공격
#Extract_M_Data = Male_data_norm[['후위공격_시도', '후위공격_성공', '후위공격_공격차단', '후위공격_범실','후위공격_성공률','후위공격_효율']]
#Extract_F_Data = Female_data_norm[['후위공격_시도', '후위공격_성공', '후위공격_공격차단', '후위공격_범실','후위공격_성공률','후위공격_효율']]
# 속공
#Extract_M_Data = Male_data_norm[['속공_시도','속공_성공', '속공_공격차단', '속공_범실','속공_성공률','속공_효율']]
#Extract_F_Data = Female_data_norm[['속공_시도','속공_성공', '속공_공격차단', '속공_범실','속공_성공률','속공_효율']]
# 퀵오픈
#Extract_M_Data = Male_data_norm[['퀵오픈_시도', '퀵오픈_성공', '퀵오픈_공격차단','퀵오픈_범실','퀵오픈_성공률','퀵오픈_효율']]
#Extract_F_Data = Female_data_norm[['퀵오픈_시도', '퀵오픈_성공', '퀵오픈_공격차단','퀵오픈_범실','퀵오픈_성공률','퀵오픈_효율']]
# 서브
#Extract_M_Data = Male_data_norm[['서브_시도', '서브_성공', '서브_범실','서브_효율']]
#Extract_F_Data = Female_data_norm[['서브_시도', '서브_성공', '서브_범실','서브_효율']]
# 블로킹
#Extract_M_Data = Male_data_norm[['블로킹_시도','블로킹_성공', '블로킹_유효블락', '블로킹_실패', '블로킹_범실', '블로킹_어시스트','블로킹_효율']]
#Extract_F_Data = Female_data_norm[['블로킹_시도','블로킹_성공', '블로킹_유효블락', '블로킹_실패', '블로킹_범실', '블로킹_어시스트','블로킹_효율']]
# 디그
#Extract_M_Data = Male_data_norm[['디그_시도', '디그_성공', '디그_실패', '디그_범실','디그_효율']]
#Extract_F_Data = Female_data_norm[['디그_시도', '디그_성공', '디그_실패', '디그_범실','디그_효율']]
# 세트
#Extract_M_Data = Male_data_norm[['세트_시도', '세트_성공','세트_범실','세트_효율']]
#Extract_F_Data = Female_data_norm[['세트_시도', '세트_성공','세트_범실','세트_효율']]
# 리시브
#Extract_M_Data = Male_data_norm[['리시브_시도', '리시브_정확', '리시브_범실','리시브_효율']]
#Extract_F_Data = Female_data_norm[['리시브_시도', '리시브_정확', '리시브_범실','리시브_효율']]

# 공격 + 블로킹 + 서브 + 세트  +리시브 + 최다연승 + 최다연패
#Extract_M_Data = Male_data_norm[['공격_시도','공격_범실','공격_공격차단','공격_성공','공격_효율','블로킹_시도','블로킹_성공','블로킹_실패','블로킹_범실','서브_시도','서브_범실','서브_성공','세트_시도','세트_범실','세트_성공','리시브_시도','리시브_범실','리시브_정확','최다연패','최다연승']]
#Extract_F_Data = Female_data_norm[['공격_시도','공격_범실','공격_공격차단','공격_성공','공격_효율','블로킹_시도','블로킹_성공','블로킹_실패','블로킹_범실','서브_시도','서브_범실','서브_성공','세트_시도','세트_범실','세트_성공','리시브_시도','리시브_범실','리시브_정확','최다연패','최다연승']]

# 상위 3개 요인 남자(후위공격/공격/오픈공격 : 12개) 여자(오픈공격/공격/리시브 : 11개)
#Extract_M_Data = Male_data_norm[['공격_시도', '공격_성공', '공격_공격차단', '공격_범실','오픈공격_시도', '오픈공격_성공', '오픈공격_공격차단', '오픈공격_범실','후위공격_시도', '후위공격_성공', '후위공격_공격차단', '후위공격_범실']]
#Extract_F_Data = Female_data_norm[['공격_시도', '공격_성공', '공격_공격차단', '공격_범실','오픈공격_시도', '오픈공격_성공', '오픈공격_공격차단', '오픈공격_범실','리시브_시도', '리시브_정확', '리시브_범실']]

# 공격 + 블로킹 + 서브 + 세트 + 리시브
#Extract_M_Data = Male_data_norm[['공격_시도','공격_범실','공격_공격차단','공격_성공','블로킹_시도','블로킹_성공','블로킹_실패','블로킹_범실','서브_시도','서브_범실','서브_성공','세트_시도','세트_범실','세트_성공','리시브_시도','리시브_범실','리시브_정확']]
#Extract_F_Data = Female_data_norm[['공격_시도','공격_범실','공격_공격차단','공격_성공','블로킹_시도','블로킹_성공','블로킹_실패','블로킹_범실','서브_시도','서브_범실','서브_성공','세트_시도','세트_범실','세트_성공','리시브_시도','리시브_범실','리시브_정확']]

# 상위 5개 요인 남자(세트/오픈공격/후위공격/서브/속공) 여자(오픈공격/퀵오픈/후위공격/리시브/세트)
#Extract_M_Data = Male_data_norm[['오픈공격_시도', '오픈공격_성공', '오픈공격_공격차단', '오픈공격_범실','오픈공격_성공률', '오픈공격_효율',
#                                 '후위공격_시도', '후위공격_성공', '후위공격_공격차단', '후위공격_범실','후위공격_성공률','후위공격_효율',
#                                 '속공_시도','속공_성공', '속공_공격차단', '속공_범실','속공_성공률','속공_효율',
#                                 '서브_시도', '서브_성공', '서브_범실','서브_효율',
#                                 '세트_시도','세트_성공','세트_범실','세트_효율']]
#Extract_F_Data = Female_data_norm[['오픈공격_시도', '오픈공격_성공', '오픈공격_공격차단', '오픈공격_범실','오픈공격_성공률', '오픈공격_효율',
#                                   '후위공격_시도', '후위공격_성공', '후위공격_공격차단', '후위공격_범실','후위공격_성공률','후위공격_효율',
#                                   '퀵오픈_시도', '퀵오픈_성공', '퀵오픈_공격차단','퀵오픈_범실','퀵오픈_성공률','퀵오픈_효율',
#                                   '세트_시도', '세트_성공','세트_범실','세트_효율',
#                                   '리시브_시도', '리시브_정확', '리시브_범실','리시브_효율']]

# 배구 5개 요인 남자(오픈공격/블로킹/서브/리시브/세트) 여자(오픈공격/블로킹/서브/리시브.세트)
#Extract_M_Data = Male_data_norm[['공격_시도', '공격_성공', '공격_공격차단', '공격_범실','공격_성공률', '공격_효율',
#                                 '블로킹_시도','블로킹_성공', '블로킹_유효블락', '블로킹_실패', '블로킹_범실', '블로킹_어시스트','블로킹_효율',
#                                 '서브_시도', '서브_성공', '서브_범실','서브_효율',
#                                 '세트_시도','세트_성공','세트_범실','세트_효율',
#                                 '리시브_시도', '리시브_정확', '리시브_범실','리시브_효율','최다연승','최다연패']]
#Extract_F_Data = Female_data_norm[['공격_시도', '공격_성공', '공격_공격차단', '공격_범실','공격_성공률', '공격_효율',
#                                 '블로킹_시도','블로킹_성공', '블로킹_유효블락', '블로킹_실패', '블로킹_범실', '블로킹_어시스트','블로킹_효율',
#                                 '서브_시도', '서브_성공', '서브_범실','서브_효율',
#                                 '세트_시도','세트_성공','세트_범실','세트_효율',
#                                 '리시브_시도', '리시브_정확', '리시브_범실','리시브_효율','최다연승','최다연패']]

# 남녀부문 파트별 중요 3요인 남:오픈공격/서브/세트/최다연승/최다연패 여:오픈공격/세트/리시브/최다연승/최다연패
Extract_M_Data = Male_data_norm[['오픈공격_시도', '오픈공격_성공', '오픈공격_공격차단', '오픈공격_범실','오픈공격_성공률', '오픈공격_효율',
#                                '공격_시도', '공격_성공', '공격_공격차단', '공격_범실','공격_성공률', '공격_효율',
                                 '서브_시도', '서브_성공', '서브_범실','서브_효율',
                                 '세트_시도','세트_성공','세트_범실','세트_효율',
                                 '최다연승','최다연패']]
Extract_F_Data = Female_data_norm[[#'공격_시도', '공격_성공', '공격_공격차단', '공격_범실','공격_성공률', '공격_효율',
#                                 '오픈공격_시도', '오픈공격_성공', '오픈공격_공격차단', '오픈공격_범실','오픈공격_성공률', '오픈공격_효율',
                                 '후위공격_시도', '후위공격_성공', '후위공격_공격차단', '후위공격_범실','후위공격_성공률', '후위공격_효율',
                                 #'퀵오픈_시도', '퀵오픈_성공', '퀵오픈_공격차단','퀵오픈_범실','퀵오픈_성공률','퀵오픈_효율',
                                 '세트_시도','세트_성공','세트_범실','세트_효율',
                                 '리시브_시도', '리시브_정확', '리시브_범실','리시브_효율',
                                 '최다연승','최다연패']]


# 하위 4개 요인 제거
#Extract_M_Data = Male_data_norm[['득점', '공격_시도', '공격_성공', '공격_공격차단', '공격_범실',
#       '공격_성공률','오픈공격_시도', '오픈공격_성공', '오픈공격_공격차단', '오픈공격_범실',
#       '오픈공격_성공률', '후위공격_시도', '후위공격_성공', '후위공격_공격차단', '후위공격_범실', '후위공격_성공률', '속공_시도',
#       '속공_성공', '속공_공격차단', '속공_범실', '속공_성공률', '퀵오픈_시도', '퀵오픈_성공', '퀵오픈_공격차단',
#       '퀵오픈_범실', '퀵오픈_성공률', '서브_시도', '서브_성공', '서브_범실', '서브_세트당평균', '블로킹_시도',
#       '블로킹_성공', '블로킹_유효블락', '블로킹_실패', '블로킹_범실', '블로킹_어시스트', '블로킹_세트당평균',
#       '세트_시도', '세트_성공','세트_범실', '세트_세트당평균',]]
#Extract_F_Data = Female_data_norm[['득점', '공격_시도', '공격_성공', '공격_공격차단', '공격_범실',
#       '공격_성공률','오픈공격_시도', '오픈공격_성공', '오픈공격_공격차단', '오픈공격_범실',
#       '오픈공격_성공률', '시간차공격_시도', '시간차공격_성공', '시간차공격_공격차단', '시간차공격_범실',
#       '시간차공격_성공률','후위공격_시도', '후위공격_성공', '후위공격_공격차단', '후위공격_범실', '후위공격_성공률', '속공_시도',
#       '퀵오픈_시도', '퀵오픈_성공', '퀵오픈_공격차단','퀵오픈_범실', '퀵오픈_성공률', '블로킹_시도',
#       '블로킹_성공', '블로킹_유효블락', '블로킹_실패', '블로킹_범실', '블로킹_어시스트', '블로킹_세트당평균',
#       '세트_시도', '세트_성공','세트_범실', '세트_세트당평균', '리시브_시도', '리시브_정확', '리시브_범실', '리시브_세트당평균', '범실']]

# 데이터 가중치 확인하기

def Confirm_feature_weight(table,result):
    # 데이터 전처리 과정
    from sklearn.model_selection import train_test_split
    
    X,y = table.values,result.values
    
    # 테스트셋을 원래 데이터의 20%만 허용한다.
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0)
    
    # 1. D차원의 데이터간의 연관성을 찾기 위해 데이터를 먼저 표준화 시킨다. (위에서 표준화를 하였으므로 생략한다.)
    
    from sklearn.preprocessing import StandardScaler
    
    sc = StandardScaler()
    X_train_std = sc.fit_transform(X_train)
    X_test_std = sc.transform(X_test)
    
    X_train=X_train_std
    X_test=X_test_std
#    X_cen = X_train - X_train.mean(axis=0)
#    cov_mat = np.dot(X_cen.T,X_cen)/len(X_cen)
    
    # 2. 특징들 상호간의 각각의 공분산을 구하기 위해 공분산 행렬을 만든다.
    cov_mat = np.cov(X_train.T) # 공분산 행렬을 생성해주는 함수
    
    # 3. 공분산 행렬을 Eigen value와 Eigen vector로 분해한다.
    # 이것을 Eigendecomposition이라고 한다.
    
    Eval,Evec = np.linalg.eig(cov_mat)
    print(Eval)
    
    # eigen value의 값이 큰 순서를 E_val_des_order에 저장한다. np.argsort(음수*데이터값)을 넣으면 크기가 큰 숫자부터 1~N까지 나온다.
    E_val_des_order = np.argsort(-abs(Eval))
    print(E_val_des_order)
    
    # 4. 공분산행렬을 통해 그 두가지(Eigen value,Eigen vector)를 유도하는 것이 가능
    tot = sum(Eval)
    
    var_exp = [(i/tot) for i in sorted(Eval,reverse=True)]
    
    # Eigen value / Eigen value의 합을 각각 구한다. 나온 각각의 값은 Eigen value의 설명 분산 비율이다.
    # 즉, 어떤 Eigen value가 가장 설명력이 높은지를 비율로 나타내기 위한 것이다.
    
    cum_var_exp = np.cumsum(var_exp)    # 누적 합을 계산해주는 함수 -> 누적 백분위로 표현
    
#    plt.figure(figsize=(18,8))
#    plt.bar(table.columns[E_val_des_order],var_exp,alpha = 0.5,align='center',
#            label = 'individual explained variance')
#    plt.step(range(0,len(cum_var_exp)),cum_var_exp,where='mid',
#              label='cumulative explained variance')
#    plt.xticks(rotation=90)
#    plt.ylabel('explained variance ratio')
#    plt.xlabel('principal components')
#    plt.legend(loc='best')
#    plt.tight_layout()
#    plt.show()
#    # 각각의 항목에 대한 weight값을 텍스트로 나타내는것
#    weight_order = table.columns[E_val_des_order]
#    for loop in range(0,len(table.columns)):
#        print("변수:{}\tweight:{}".format(weight_order[loop],cum_var_exp[loop]))

#print("============================남자경기요인============================")
#Confirm_feature_weight(Male_data_norm,Mplayoff)
#Confirm_feature_weight(Male_data,Mplayoff)
#Confirm_feature_weight(Extract_M_Data,Mplayoff)        
#print("============================여자경기요인============================")
#Confirm_feature_weight(Female_data_norm,Fplayoff)
#Confirm_feature_weight(Female_data,Fplayoff)
#Confirm_feature_weight(Extract_M_Data,Mplayoff)        

Male_data['플레이오프진출'] = Mplayoff
Female_data['플레이오프진출'] = Fplayoff
Extract_M_Data['플레이오프진출'] = Mplayoff
Extract_F_Data['플레이오프진출'] = Fplayoff

##print(Extract_M_Data.columns)
##print(Extract_F_Data.columns)


## pickle로 변환한다.
#Male_data.to_pickle("Male_data")
#Female_data.to_pickle("Female_data")
Extract_M_Data.to_pickle("Extract_M_Data")
Extract_F_Data.to_pickle("Extract_F_Data")
#Extract_M_Data.to_pickle("original_M_Data")
#Extract_F_Data.to_pickle("original_F_Data")