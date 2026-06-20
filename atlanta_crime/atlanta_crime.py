import requests
import pandas as pd

def fetch_atlanta_crime(limit=100):
    url = "https://services3.arcgis.com/Et5Qfajgiyosiw4d/ArcGIS/rest/services/OpenDataWebsite_Crime_view/FeatureServer/0/query"
    
    params = {
        "where": "1=1",
        "outFields": "IncidentNumber,ReportDate,Day_of_the_week,NIBRS_Offense,NIBRS_Bucket,FireArmInvolved,Zone,NhoodName,StreetAddress",
        "resultRecordCount": limit,
        "orderByFields": "ReportDate DESC",  # 최신순
        "f": "json"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"API 에러: {response.status_code}")
            return None
        
        data = response.json()
        
        if "error" in data:
            print(f"응답 에러: {data['error']}")
            return None
        
        # ArcGIS는 data['features'] 안에 데이터가 있어요
        features = data["features"]
        records = [f["attributes"] for f in features]
        
        return pd.DataFrame(records)
    
    except requests.exceptions.ConnectionError:
        print("네트워크 연결 실패")
        return None
    except requests.exceptions.Timeout:
        print("요청 시간 초과")
        return None

# 1. 데이터 가져오기
df = fetch_atlanta_crime(limit=100)

if df is not None:
    print(f"총 {len(df)}개 가져옴")
    print(df.head())
    print()
    
    # 2. 범죄 유형별 건수 (GROUP BY)
    print("=== 범죄 유형별 건수 ===")
    print(df.groupby("NIBRS_Bucket")["IncidentNumber"].count().sort_values(ascending=False))
    print()
    
    # 3. 구역별 건수
    print("=== Zone별 건수 ===")
    print(df.groupby("Zone")["IncidentNumber"].count().sort_values(ascending=False))
    print()
    
    # 4. 총기 관련 범죄만 필터
    gun_crimes = df[df["FireArmInvolved"] == "yes"]
    print(f"=== 총기 관련 범죄: {len(gun_crimes)}건 ===")
    print(gun_crimes[["IncidentNumber", "NIBRS_Offense", "NhoodName"]])
    print()
    
    # 5. CSV 저장
    df.to_csv("atlanta_crime.csv", index=False)
    print("atlanta_crime.csv 저장 완료!")