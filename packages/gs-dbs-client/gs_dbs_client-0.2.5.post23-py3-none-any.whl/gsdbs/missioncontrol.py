import http.client as httplib
import random
from datetime import datetime
import websocket
import string
from threading import Thread
import json
import requests
import asyncio
from twisted.internet import task, reactor
from multiprocessing.dummy import Pool

""" SockJS Client class  """


class MissionControl(Thread):

    def __init__(self, cnode, prefix, gsdbs, userInfoURL, execute, heartbeat, heartbeatintervall=10, host="localhost",
                 port=8081):
        self._mandantname = ""
        self.counter = 0
        self._host = host
        self._port = port
        self.cnode = cnode
        self._gsdbs = gsdbs
        self._prefix = prefix
        self.execute = execute
        self.heartbeat = heartbeat
        self.userInfoURL = userInfoURL
        self.heartbeatintervall = heartbeatintervall * 1000
        self.loop = self.getEventLoop()
        self._pool = Pool(1)
        Thread.__init__(self)
        self.connect()

    def connect(self):
        self.get_socket_info()
        self.start()

    def disconnect(self):
        pass

    def run(self):

        self._r1 = str(random.randint(0, 1000))
        self._conn_id = self.random_str(8)
        websocket.enableTrace(False)

        self._ws = websocket.WebSocketApp(
            ("ws://" if "localhost" in self._host else "wss://")
            + self._host + ":" + str(self._port) +
            self._prefix +
            "/" +
            self._r1 +
            "/" +
            self._conn_id +
            "/websocket?access_token=" +
            self._gsdbs.getAccessToken(),
            # on_cont_message=self.on_message,
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close)

        self._ws.run_forever()

    def get_socket_info(self):
        conn = 0
        try:
            if self._port == 8081:
                conn = httplib.HTTPConnection(self._host, self._port)
            else:
                conn = httplib.HTTPSConnection(self._host, self._port)

            print(" Getting info from ", self._host)
            conn.request('GET', self._prefix + '/info',
                         headers={"Authorization": "Bearer " + self._gsdbs.getAccessToken()
                                  # , "Origin": "https://glass-sphere-ai.de"
                                  }
                         )
            response = conn.getresponse()
            print("INFO", response.status, response.reason, response.read())

        except  Exception as e:
            print(e)
        finally:
            if not conn: conn.close()

    def on_message(self, ws, message):
        self.processMessage(message)

        # self._pool.apply_async(self.processMessage, args=[message], callback=self.on_success,
        #                        error_callback=self.on_errorPost)

    def on_success(self, r):
        print('message succeed')

    def on_errorPost(self, error):
        print('message failed :' + error)

    def getEventLoop(self):
        if asyncio.get_event_loop().is_closed():
            asyncio.set_event_loop(asyncio.new_event_loop())
        return asyncio.get_event_loop()

    def processMessage(self, message):
        # sleep(0.05)
        if message == 'a["\\n"]':
            print("beat:" + datetime.now().strftime("%H:%M:%S"))
            self._ws.send('["\\n"]')
            self.counter = self.counter + 1
            # if self.counter % self.heartbeatintervall == 0:
            self.ETHome()
            # self.counter = 0

        if message == "o":
            pass
        if message.startswith("a"):
            if "{" in message:
                try:
                    print("Received")
                    mssgbdy = json.loads(
                        message[message.find("{"):message.find("\\u0000")].replace("\\\"", "\"").replace("\\n",
                                                                                                         " ").replace(
                            "\\r", " ").replace("\\t", " "))
                    self.execute(self._gsdbs, mssgbdy, self.onNext)
                    if self.str2bool(mssgbdy["isComputingStep"]) and mssgbdy["computingstep"] != '':
                        self.markJobAsDone(mssgbdy["jobid"], mssgbdy["groupid"], mssgbdy["computingstep"])
                except Exception as e:
                    print("JobFailed")
                    self.markJobAsFailed(mssgbdy["jobid"])
                    print(e)
        else:
            pass

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

    def call_api(self, transactionid, send):
        x = 16388
        res = [send[y - x:y] for y in range(x, len(send) + x, x)]
        for x in res:
            self._ws.send("[\"" + x + "\"]")

    def on_success(self, r):
        print('Post succeed')

    def on_errorPost(self, error):
        print('Post requests failed')

    def onNext(self, pool, target, json1, data):
        try:
            data["mandantname"] = self._mandantname

            url = "http://" + self._host + ":" + str(self._port) + "/missioncontrol/onnext"
            json2 = {"jobid": json1["jobid"], "groupid": json1["groupid"],
                     "accesstoken": self._gsdbs.getAccessToken(),
                     "computingstep": json1["computingstep"],
                     "target": target,
                     "cnode": self.cnode,
                     "data": data}
            headers = {"Content-Type": "application/json",
                       "Authorization": "Bearer " + self._gsdbs.getAccessToken()}

            datastring = json.dumps(json2).replace("\"", "\'")

            transactionid = 'tx-' + self.random_str(8)
            send = 'SEND\\n' \
                   'destination:/queue/onnext\\n' \
                   'durable:false\\n' \
                   'exclusive:false\\n' \
                   'auto-delete:false\\n\\n' \
                   + datastring + '\\u0000'
            self.call_api(transactionid, send)

        except Exception as e:
            return e

    def utf8len(self, s):

        encoded_string = s.encode('utf-8')
        byte_array = bytearray(s)

        return len(s.encode('utf-8'))

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed: Code->" + close_status_code + "Message:" + close_msg + ":" + datetime.now().strftime(
            "%H:%M:%S") + "###")

    def on_open(self, ws):
        connect = '\"CONNECT\\naccept-version:1.2,1.0\\nheart-beat:' + str(self.heartbeatintervall) + ',' + str(
            self.heartbeatintervall) + '\\nauto-delete:true\\nexclusive:true\\n\\n\\u0000\"'
        self._ws.send("[" + connect + "]")
        sub = f'\"SUBSCRIBE\\nid:{self.random_str(4)}\\ndestination:/queue/{self.getQueue()}\\n\\n\\u0000\"'
        # sub = f'\"SUBSCRIBE\\nid:{self.random_str(4)}\\ndestination:/queue/detector\\n\\n\\u0000\"'
        self._ws.send("[" + sub + "]")
        self.ETHome()
        print("open:" + datetime.now().strftime("%H:%M:%S"))

    def ETHome(self):
        headers = {'Authorization': 'Bearer ' + self._gsdbs.getAccessToken()}

        protokoll = "https://"
        if "localhost" in self._host:
            protokoll = "http://"
        resp = requests.get(protokoll + self._host + ":" + str(self._port) + "/missioncontrol/register",
                            headers=headers)
        resp.raise_for_status()
        self.heartbeat(self._gsdbs, self.cnode)

    def getQueue(self):
        headers = {'Authorization': 'Bearer ' + self._gsdbs.getAccessToken()}
        try:
            resp = requests.get(self.userInfoURL, headers=headers)
            resp.raise_for_status()
            userinfo = resp.json()
            self._mandantname = userinfo["mandant"]["mandantName"]
            return userinfo["mandant"]["mandantName"] + "-" + self.cnode  # + "-" + self._conn_id
        except:
            return ""

    def random_str(self, length):
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for c in range(length))

    def markJobAsDone(self, jobid, groupid, computingstep):

        json2 = {"jobid": jobid, "groupid": groupid, "accesstoken": self._gsdbs.getAccessToken(),
                 "computingstep": computingstep, "cnode": self.cnode}
        datastring = json.dumps(json2).replace("\"", "\\\"")

        transactionid = 'tx-' + self.random_str(8)
        send = 'SEND\\ndestination:/queue/onnotify\\ndurable:false\\nexclusive:false\\nauto-delete:false\\n\\n' + datastring + '\\u0000'
        self.call_api(transactionid, send)

        print("job done")

    def markJobAsFailed(self, jobid):
        self._gsdbs.executeStatement(f"""
                mutation{{
                        updateDTable(
                  dtablename:"gsasyncjob",
                   where: [
                      {{connective: BLANK, column: gsasyncjob_jobid, operator: EQUAL, value: "{jobid}"}}
                        {{connective: AND, column: gsasyncjob_cnode, operator: EQUAL, value: "{self.cnode}"}}
                  ],
                  updatelist:[
                    {{datalink:gsasyncjob_jobstatus,value:"failed"}}
                  ]
                )
                }}
            """)


class MissionControlClient:

    def __init__(self, cnode, execute, heartBeat, gsdbs, host="glass-sphere-ai.de", port=443):
        self.cnode = cnode
        self.execute = execute
        self.gsdbs = gsdbs
        self.host = host
        self.port = port
        self.client = None
        self.heartBeat = heartBeat
        self.init()

    def createClient(self):
        self.client = MissionControl(self.cnode,
                                     '/gs-guide-websocket',
                                     self.gsdbs,
                                     "https://ens-fiti.de/user/info",
                                     self.execute,
                                     self.heartBeat,
                                     60,
                                     host=self.host,
                                     port=self.port
                                     )
        # , "glass-sphere-ai.de", 443)

    def checkThreadRunning(self):
        if self.client is None or not self.client.is_alive():
            self.gsdbs.refreshToken()
            reactor.callFromThread(self.createClient)

    def init(self):
        l = task.LoopingCall(self.checkThreadRunning)
        l.start(1.0)
        reactor.run()
