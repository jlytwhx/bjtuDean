import re
import time
import datetime
from bs4 import BeautifulSoup
from dean import Dean


class FreeClassroom:
    session = Dean().dean_session
    week = (int(time.time()) - 1551024000) // (7 * 24 * 3600) + 1 or 1
    building_dict = {
        "1": "思源楼",
        "2": "思源西楼",
        "3": "思源东楼",
        "4": "第九教学楼",
        "5": "第八教学楼",
        "6": "第五教学楼",
        "7": "第二教学楼",
        "8": "东区一教",
        "9": "东区二教",
        "10": "东教三楼",
        "11": "逸夫教学楼",
        "12": "机械楼",
        "13": "第十七号教学楼",
        "90": "科技大厦",
        "91": "天佑会堂",
        "92": "工程素质",
        "93": "综合实验楼",
        "94": "机械实验馆",
        "100": "学生活动服务中心"

    }
    status_dict = {
        '#fff': '空闲',
        '#394ed6': '考试占用',
        '#e46868': '排课占用',
        '#77bf6d': '预约',
        '#d8cc56': '个人占用'
    }

    def _get_building_room_info(self, building_no, page=1):
        url = 'https://dean.bjtu.edu.cn/classroom/timeholdresult/room_stat/'
        queries = {
            'zxjxjhh': '2018-2019-2-2',
            'zc': self.week,
            'jxlh': building_no,
            'jash': '',
            'submit': '查询+',
            'has_advance_query': '',
            'page': page
        }
        building = self.building_dict[str(building_no)]
        content = self.session.get(url, params=queries).content.decode()
        table = BeautifulSoup(content, 'html5lib').find('table', {'class': 'table table-bordered'})
        weekday = datetime.datetime.now().weekday() or 7
        classroom_list = table.find_all('tr')[2:]
        for classroom in classroom_list:
            course_list = classroom.find_all('td', {'title': re.compile(r'星期{}'.format(weekday))})
            classroom_name = classroom.td.text.split()[0]
            for course in course_list:
                no = int(course.get('title')[-2])
                color = course.get('style').replace('background-color: ', '')
                status = self.status_dict[color]
                print(building, classroom_name, '第{}节课'.format(no), status)

    def update(self):
        for building_no in self.building_dict.keys():
            self._get_building_room_info(building_no=building_no)


if __name__ == '__main__':
    FreeClassroom().update()
