import os
from decouple import config
from flask_sqlalchemy import SQLAlchemy
import json
from sanic import Sanic
from sanic.response import json


class Persistence():

    myBase = "POSTGRES"
    myCulture = "es-EC"
    myDecimalSeparator = ","
    myGroupSeparator = "."
    myDateSeparator = "/"
    myShortDate = "dd/mm/YY"
    myLongDate = "dd/mm/YYYY"
    myDecimalDigits = 2
    myVariables = None
    mySession = None
    myDb = None
    myApp = None

    def __init__(self, session):
        self.myApp = Sanic(__name__)
        self.myDb = SQLAlchemy(self.myApp)
        self.myApp.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        self.LoadVariables()
        self.SetRegion()
        self.SetSession(session)

    async def _sql(self, rawSql, sqlVars={}):
        "Execute raw sql, optionally with prepared query"
        assert type(rawSql) == str
        assert type(sqlVars) == dict
        res = self.myDb.session.execute(rawSql, sqlVars)
        self.myDb.session.commit()
        return res

    async def _sqltran(self, rawSql, sqlVars={}):
        "Execute raw sql, optionally with prepared query"
        assert type(rawSql) == str
        assert type(sqlVars) == dict
        res = self.myDb.session.execute(rawSql, sqlVars)
        return dict(res, ctx=self.myDb.session)

    async def SetSession(self, session):
        self.mySession = session

    async def PaginatedQuery(self, stm, table, field, since, top):
        self.GetDbCnx(table)
        condition = (lambda x: "AND"
                     if (str(x).upper().contains("WHERE")) else "WHERE")(stm)
        self._sql(stm+" "+condition+" "+field+" > "+since + " LIMIT "+top)

    async def Query(self, stm, table):
        self.GetDbCnx(table)
        self._sql(stm)

    async def Write(self, stm, table, logtable="LOGTABLE"):
        session = self.mySession
        self.GetDbCnx(table)
        self._sql(stm)
        self.WriteLog(stm, table, logtable, session)

    async def WriteLog(self, stm, table, logtable, session):
        self.GetDbCnx(logtable)
        currenttable = self.GetTableName(logtable)
        insert = "INSERT INTO " + currenttable + """
            (stm,table,session,created) VALUES (""" + \
            stm+", "+table+", "+session+", NOW())"
        return self._sql(insert)

    async def WriteImg(self, table, meta,  img):
        self.GetDbCnx(table)
        insert = "INSERT INTO " + table + \
            "(meta,img,created) VALUES (" + \
            meta+", "+img+" , NOW())"
        return self._sql(insert)

    async def SpExec(self, sp, args):
        stm = "CALL "+sp+"("+args+")"
        return self._sql(stm)

    async def SetProp(self, table, key, value, condition):
        if condition:
            stm = "UPDATE "+table+" SET props = jsonb_set(props, "+key+", '"+value+"' ,false) \
                FROM "+table+" \
                WHERE "+condition+""
            return self._sql(stm)

    async def GetProp(self, key, table, condition="1=1"):
        stm = "SELECT props from "+table+" Where "+condition
        res = self._sql(stm)
        if key is None:
            return json.load(res)
        return json.load(res)[key]

    async def Transac(self, stm, table):
        self.GetDbCnx(table)
        return self._sqltran(stm)

    async def NextVal(self, field, table):
        self.GetDbCnx(table)
        stm = "SELECT MAX("+field+") FROM "+table+""
        return self._sql(stm)

    async def FindUserPerm(self, user, screen, table='permission'):
        self.GetDbCnx(table)
        stm = """ SELECT * FROM """+table + """ prm 
                JOIN screen scr 
                ON scr.screen_id=prm.screen_id_fk 
                JOIN user usr 
                ON usr.group_id_fk = prm.group_id_fk     
                WHERE screen_id_fk = """+screen+""" 
                AND usr.user_id = """ + user
        return self._sql(stm)

    async def FindParam(self, key, session, table='param'):
        self.GetDbCnx(table)
        stm = """SELECT * FROM
               """+table + """ prm 
                JOIN instance inst 
                ON inst.instance_id=prm.instance_id_fk   
                WHERE instance_id_fk = """+session[0]+""" 
                AND prm.param_key='"""+key+"'"
        return self._sql(stm)

    async def GetParams(self, table, session, key, condition):
        self.GetDbCnx(table)
        stm = "SELECT "+(lambda x: "*" if (x is None) else x)(key) + " \
            from "+table+" where " + condition + " \
            AND enterprise_id='"+session[0]+"'"
        res = self._sql(stm)
        if key is None:
            return json.load(res)
        return json.load(res)[key]

    async def GetTableName(self, table):
        tableAtDomain = self.GetVariable(table)
        domain = str(tableAtDomain).split("@")[1]
        tbl = self.GetVariable(domain)
        return tbl

    async def GetDbCnx(self, table):
        tableAtDomain = self.GetVariable(table)
        domain = str(tableAtDomain).split("@")[1]
        cnx = self.GetVariable(domain)
        self.SetDbCnx(cnx)

    async def SetDbCnx(self, cnx):
        self.myApp.config['SQLALCHEMY_DATABASE_URI'] = cnx

    async def SetRegion(self):
        self.myCulture = self.GetVariable("myCulture")
        self.myDecimalSeparator = self.GetVariable("myDecimalSeparator")
        self.myGroupSeparator = self.GetVariable("myGroupSeparator")
        self.myDateSeparator = self.GetVariable("myDateSeparator")
        self.myShortDate = self.GetVariable("myShortDate")
        self.myLongDate = self.GetVariable("myLongDate")
        self.myDecimalDigits = self.GetVariable("myDecimalDigits")

    async def GetVariable(self, key):
        if (os.getenv(str(key).upper()) is None):
            self.LoadVariables()
        return self.myVariables[str(key).upper()]

    async def GetAllVariables(self):
        return self.myVariables

    async def LoadVariables(self):
        os.environ = os.environ + config
        self.myVariables = os.environ.copy()
        for item in os.environ:
            self.myApp.config[item.Key] = item.Value
