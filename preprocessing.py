#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob

def od_in(date: int, end_time: str, dest: int, from_seoul: bool):
    # 해당 날짜 csv 파일 읽어오기
    csv_dir = glob.glob(f"data/**/od_{date}*.csv", recursive = True)
    df = pd.read_csv(csv_dir[0])    # 하루치 데이터를 읽을 때에만 성립
    
    # 행정동 코드 문자열로 바꾸기 (시각화 때 merged_df 생성 위해)
    df["dest_hdong_cd"] = df["dest_hdong_cd"].astype(str)
    df["origin_hdong_cd"] = df["origin_hdong_cd"].astype(str)
    
    # origin_hdong_cd 서울시 한정
    if from_seoul == True:
        df = df[df["origin_hdong_cd"].str.startswith("11")]
    
    # dest_hdong_cd 필터링 & end_time 필터링
    df.loc[:, 'end_time'] = pd.to_datetime(df['end_time'], format='%H:%M').dt.hour 
    df = df[(df["dest_hdong_cd"] == str(dest)) & (df["end_time"].astype("str") == end_time)]
    
    # 해당되는 모든 데이터의 이동인원 summation
    df = df.groupby("origin_hdong_cd")["od_cnts"].sum().sort_values(ascending=False).reset_index()
    
    return df


def od_out(date: int, start_time: str, origin: int, to_seoul: bool):
    # 해당 날짜 csv 파일 읽어오기
    csv_dir = glob.glob(f"data/**/od_{date}*.csv", recursive = True)
    df = pd.read_csv(csv_dir[0])    # 하루치 데이터를 읽을 때에만 성립
    
    # 행정동 코드 문자열로 바꾸기 (시각화 때 merged_df 생성 위해)
    df["dest_hdong_cd"] = df["dest_hdong_cd"].astype(str)
    df["origin_hdong_cd"] = df["origin_hdong_cd"].astype(str)
    
    # dest_hdong_cd 서울시 한정
    if to_seoul == True:
        df = df[df["dest_hdong_cd"].str.startswith("11")]
        
    # origin_hdong_cd 필터링 & start_time 필터링
    df.loc[:, 'start_time'] = pd.to_datetime(df['start_time'], format='%H:%M').dt.hour 
    df = df[(df["origin_hdong_cd"] == str(origin)) & (df["start_time"].astype("str") == start_time)]
    
    # 해당되는 모든 데이터의 이동인원 summation
    df = df.groupby("dest_hdong_cd")["od_cnts"].sum().sort_values(ascending=False).reset_index()

    return df

def stay(day, time):
    csv_dir = glob.glob(f"data/**/stay_{day}_1.csv", recursive = True)
    data = pd.read_csv(csv_dir[0])
    
    # 서울시에 해당하는 행만 필터링
    data = data[(data['hdong_cd'] >= 1100000000) & (data['hdong_cd'] <= 1174070000)] 
    
    # 시간 형식을 변환 (예: 13:00 -> 13)
    data.loc[:, 'time'] = pd.to_datetime(data['time'], format='%H:%M').dt.hour 
    
    # input 시간에 해당하는 데이터만 필터링
    data = data[data['time'].astype("str") == time]
    
    # 행정동 코드와 시간을 기준으로 그룹화하고, 체류인원 합산
    data_grouped = data.groupby(['hdong_cd', 'time'], as_index=False).agg({'stay_cnts': 'sum'})
    
    # 결과를 행정동 코드와 시간으로 정렬
    data_grouped = data_grouped.sort_values(by=['hdong_cd'])
    data_grouped = data_grouped.drop(columns=['time'])
    return data_grouped

