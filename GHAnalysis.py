import json
import os
import argparse
import multiprocessing
import shutil
import time
import mmap
import sqlite3
UsefulName = ("login", "type", "name", "actor", "repo")
UsefulInfo = ("PushEvent", "IssueCommentEvent", "IssuesEvent",
              "PullRequestEvent")


class Data:
    def __init__(self, dict_address: int = None, reload: int = 0):
        localtime = time.asctime(time.localtime(time.time()))
        print(localtime)
        if reload == 1:
            try:
                os.makedirs('json_123')
            except:
                shutil.rmtree('json_123')
                os.makedirs('json_123')
            self.__init(dict_address)
        if dict_address is None and not os.path.exists('test.db'):
            raise RuntimeError('error: init failed')
        # x = open('1.json', 'r', encoding='utf-8').read()
        # self.__4Events4PerP = json.loads(x)
        # x = open('2.json', 'r', encoding='utf-8').read()
        # self.__4Events4PerR = json.loads(x)
        # x = open('3.json', 'r', encoding='utf-8').read()
        # self.__4Events4PerPPerR = json.loads(x)

    def __init(self, dict_address: str):
        self.__4Events4PerP = {}
        self.__4Events4PerR = {}
        self.__4Events4PerPPerR = {}

        for root, dic, files in os.walk(dict_address):
            pool = multiprocessing.Pool(processes=8)
            for f in files:
                self.dataProcessing
                pool.apply_async(self.dataProcessing, args=(f, dict_address))
            pool.close()
            pool.join()
        for root, dic, files in os.walk(dict_address):
            for f in files:
                if f[-5:] == '.json':
                    x = open('json_123\\' + f, 'r', encoding='utf-8').read()
                    x = json.loads(x)
                    self.count(x)
        print(time.asctime(time.localtime(time.time())))
        conn = sqlite3.connect('test.db', isolation_level='DEFERRED')
        c = conn.cursor()
        c.execute('''PRAGMA synchronous = OFF''')
        c.execute('''CREATE TABLE EventPerP
                (ID INT PRIMARY KEY,
                PersonName TEXT,
                PushEvent INT,
                IssueCommentEvent INT,
                IssuesEvent INT,
                PullRequestEvent INT) ''')
        c.execute('''CREATE TABLE EventPerR
                (ID INT PRIMARY KEY,
                RepoName TEXT,
                PushEvent INT,
                IssueCommentEvent INT,
                IssuesEvent INT,
                PullRequestEvent INT) ''')
        c.execute('''CREATE TABLE EventPerPPerR
                (ID INT PRIMARY KEY,
                PersonName TEXT,
                RepoName TEXT,
                PushEvent INT,
                IssueCommentEvent INT,
                IssuesEvent INT,
                PullRequestEvent INT) ''')

        number = 0
        for People in self.__4Events4PerP:
            number += 1
            sql = "insert into EventPerP(ID,PersonName,PushEvent,IssueCommentEvent,IssuesEvent,PullRequestEvent) values(%d,'%s',%d,%d,%d,%d)" % (
                number, People, self.__4Events4PerP.get(People).get(
                    'PushEvent', 0), self.__4Events4PerP.get(People).get(
                        'IssueCommentEvent', 0),
                self.__4Events4PerP.get(People).get('IssuesEvent', 0),
                self.__4Events4PerP.get(People).get('PullRequestEvent', 0))
            conn.execute(sql)
        number = 0
        for Repo in self.__4Events4PerR:
            number += 1
            sql = "insert into EventPerR(ID,RepoName,PushEvent,IssueCommentEvent,IssuesEvent,PullRequestEvent) values(%d,'%s',%d,%d,%d,%d)" % (
                number, Repo, self.__4Events4PerR.get(Repo).get(
                    'PushEvent', 0), self.__4Events4PerR.get(Repo).get(
                        'IssueCommentEvent', 0),
                self.__4Events4PerR.get(Repo).get('IssuesEvent', 0),
                self.__4Events4PerR.get(Repo).get('PullRequestEvent', 0))
            conn.execute(sql)
        number = 0
        for People in self.__4Events4PerPPerR:
            for Repo in self.__4Events4PerPPerR.get(People):
                number += 1
                sql = "insert into EventPerPPerR(ID,PersonName,RepoName,PushEvent,IssueCommentEvent,IssuesEvent,PullRequestEvent) values(%d,'%s','%s',%d,%d,%d,%d)" % (
                    number, People, Repo,
                    self.__4Events4PerPPerR.get(People).get(Repo).get(
                        'PushEvent',
                        0), self.__4Events4PerPPerR.get(People).get(Repo).get(
                            'IssueCommentEvent', 0),
                    self.__4Events4PerPPerR.get(People).get(Repo).get(
                        'IssuesEvent',
                        0), self.__4Events4PerPPerR.get(People).get(Repo).get(
                            'PullRequestEvent', 0))
                conn.execute(sql)
        conn.execute(
            '''CREATE INDEX EventPerP_index ON EventPerP (PersonName)''')
        conn.execute(
            '''CREATE INDEX EventPerR_index ON EventPerR (RepoName)''')
        conn.execute(
            '''CREATE INDEX EventPerPPerR_index ON EventPerPPerR (PersonName,RepoName)'''
        )
        conn.commit()
        print(time.asctime(time.localtime(time.time())))

    def count(self, records):
        for i in records:
            if not self.__4Events4PerP.get(i['actor__login'], 0):
                self.__4Events4PerP.update({i['actor__login']: {}})
                self.__4Events4PerPPerR.update({i['actor__login']: {}})
            self.__4Events4PerP[i['actor__login']][
                i['type']] = self.__4Events4PerP[i['actor__login']].get(
                    i['type'], 0) + 1
            if not self.__4Events4PerR.get(i['repo__name'], 0):
                self.__4Events4PerR.update({i['repo__name']: {}})
            self.__4Events4PerR[i['repo__name']][
                i['type']] = self.__4Events4PerR[i['repo__name']].get(
                    i['type'], 0) + 1
            if not self.__4Events4PerPPerR[i['actor__login']].get(
                    i['repo__name'], 0):
                self.__4Events4PerPPerR[i['actor__login']].update(
                    {i['repo__name']: {}})
            self.__4Events4PerPPerR[i['actor__login']][i['repo__name']][
                i['type']] = self.__4Events4PerPPerR[i['actor__login']][
                    i['repo__name']].get(i['type'], 0) + 1

    def dataProcessing(self, f, dict_address):
        json_list = []
        if f[-5:] == '.json':
            json_path = f
            x = open(dict_address + '\\' + json_path, 'r', encoding='utf-8')
            with mmap.mmap(x.fileno(), 0, access=mmap.ACCESS_READ) as m:
                m.seek(0, 0)
                obj = m.read()
                obj = str(obj, encoding="utf-8")
                str_list = [_x for _x in obj.split('\n') if len(_x) > 0]
                for i, _str in enumerate(str_list):
                    try:
                        json_list.append(json.loads(_str))
                    except:
                        pass
            self.save(json_list, f)

    def save(self, json_list, f1):
        record = self.__listOfNestedDict2ListOfDict(json_list)
        k = []
        for i in record:
            k.append({
                'actor__login': i['actor__login'],
                'type': i['type'],
                'repo__name': i['repo__name']
            })
        with open('json_123\\' + f1, 'w', encoding='utf-8') as f:
            json.dump(k, f)

    def __checkMatches(self, k: str):
        for name in UsefulName:
            if k == name:
                return 0
        return 1

    def __cheakInfo(self, k: str):
        for name in UsefulInfo:
            if k == name:
                return 0
        return 1

    def __parseDict(self, d: dict, prefix: str):
        _d = {}
        for k in d.keys():
            if str(type(d[k]))[-6:-2] == 'dict':
                cheak = self.__parseDict(d[k], k)
                # if cheak is False:
                #     return False
                _d.update(cheak)
                # _d.update(self.__parseDict(d[k], k))
            else:
                # if (k == "type" and self.__cheakInfo(d[k])):
                #     return False
                if self.__checkMatches(k):
                    continue
                _k = f'{prefix}__{k}' if prefix != '' else k
                _d[_k] = d[k]
        return _d

    def __listOfNestedDict2ListOfDict(self, a: list):
        records = []
        for d in a:
            _d = self.__parseDict(d, '')
            if _d is False:
                continue
            records.append(_d)
        return records

    def getEventDB(self, EventName):
        row = 1
        for events in UsefulInfo:
            row += 1
            if events == EventName:
                break
        return row

    def getEventsUsers(self, username: str, event: str) -> int:
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        sql = "SELECT * From EventPerP WHERE PersonName ='%s'" % (username)
        data = c.execute(sql)
        res = data.fetchone()
        return res[self.getEventDB(event)]

        # if not self.__4Events4PerP.get(username, 0):
        #     return 0
        # else:
        #     return self.__4Events4PerP[username].get(event, 0)

    def getEventsRepos(self, reponame: str, event: str) -> int:
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        sql = "SELECT * From EventPerR WHERE RepoName ='%s'" % (reponame)
        data = c.execute(sql)
        res = data.fetchone()
        return res[self.getEventDB(event)]
        # if not self.__4Events4PerR.get(reponame, 0):
        #     return 0
        # else:
        #     return self.__4Events4PerR[reponame].get(event, 0)

    def getEventsUsersAndRepos(self, username: str, reponame: str,
                               event: str) -> int:
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        sql = "SELECT * From EventPerPPerR WHERE PersonName ='%s' AND RepoName = '%s'" % (
            username, reponame)
        data = c.execute(sql)
        res = data.fetchone()
        return res[self.getEventDB(event) + 1]
        # return res[self.getEventDB(event)]
        # if not self.__4Events4PerP.get(username, 0):
        #     return 0
        # elif not self.__4Events4PerPPerR[username].get(reponame, 0):
        #     return 0
        # else:
        #     return self.__4Events4PerPPerR[username][reponame].get(event, 0)


class Run:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.data = None
        self.argInit()
        print(self.analyse())

    def argInit(self):
        self.parser.add_argument('-i', '--init')
        self.parser.add_argument('-u', '--user')
        self.parser.add_argument('-r', '--repo')
        self.parser.add_argument('-e', '--event')

    def analyse(self):
        if self.parser.parse_args().init:
            self.data = Data(self.parser.parse_args().init, 1)
            return 0
        else:
            if self.data is None:
                self.data = Data()
            if self.parser.parse_args().event:
                if self.parser.parse_args().user:
                    if self.parser.parse_args().repo:
                        res = self.data.getEventsUsersAndRepos(
                            self.parser.parse_args().user,
                            self.parser.parse_args().repo,
                            self.parser.parse_args().event)
                    else:
                        res = self.data.getEventsUsers(
                            self.parser.parse_args().user,
                            self.parser.parse_args().event)
                elif self.parser.parse_args().repo:
                    res = self.data.getEventsRepos(
                        self.parser.parse_args().repo,
                        self.parser.parse_args().event)
                else:
                    raise RuntimeError('error: argument -l or -c are required')
            else:
                raise RuntimeError('error: argument -e is required')
        return res


if __name__ == '__main__':
    s = time.time()
    a = Run()
    e = time.time()
    print(e - s)
