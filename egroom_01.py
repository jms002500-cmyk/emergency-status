import requests
import json
import xmltodict

def save_emergency_data(city="경기도", district="화성시"):
    # 1. 인증키 및 URL 설정
    service_key = "a07b8307eabbea7ef46efa8a49999db3d89ee629d60f27d17357aba2f9ece4d7"
    url = "http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEmrrmRltmUsefulSckbdInfoInqire"

    params = {
        'serviceKey': service_key,
        'STAGE1': city,
        'STAGE2': district,
        'pageNo': '1',
        'numOfRows': '20'
    }

    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data_dict = xmltodict.parse(response.text)
            items = data_dict['response']['body']['items']
            
            if items is None:
                print(f"현재 {district} 지역에 데이터가 없습니다.")
                return

            hospital_list = items['item']
            if isinstance(hospital_list, dict):
                hospital_list = [hospital_list]

            # 2. 데이터 가공 (블로그용)
            results = []
            for hospital in hospital_list:
                hvec = hospital.get('hvec', '-')
                results.append({
                    "name": hospital.get('dutyName'),
                    "beds": hvec if hvec != '-1' else "Full",
                    "surgery": hospital.get('hvoc', '-'),
                    "time": hospital.get('hvidate', '-')
                })

            # 3. JSON 파일로 저장
            with open('emergency_data.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            
            print("✅ emergency_data.json 파일이 성공적으로 생성되었습니다!")
            
            # 터미널에도 확인용 출력
            for res in results:
                print(f"[{res['name']}] 가용병상: {res['beds']}")

        else:
            print(f"API 요청 실패: {response.status_code}")

    except Exception as e:
        print(f"오류 발생: {e}")

# 실행
if __name__ == "__main__":
    save_emergency_data("경기도", "화성시")

requests
xmltodict 