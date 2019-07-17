from flask import jsonify, abort, make_response, render_template
from flask_restful import Resource, reqparse, fields
from etc.configure import GetConfigure
import re
import operator
class showtag(Resource):
    def get(self, project, module):
        sql = "select project,module,scale,tag,rollback_tag from tag_list where project = '%s' and module = '%s'" % (project, module)
        __db = GetConfigure.get_mysql_client()
        info = __db.select(sql)
        list_online = []
        list_test = []
        list_dev = []
        list_all = []
        for i in info:
            Project = i[0]
            Module = i[1]
            Scale = i[2]
            Tag = i[3]
            Rollback = i[4]
            if re.match(r'(online)', Scale):
                list_online.append({'name': '%s_%s' %(Project,Module),'scale':'%s' %(Scale), 'tag':'%s' %(Tag), 'rollback_tag':'%s' %(Rollback)})
            elif re.match(r'(dev)', Scale):
                list_dev.append({'name': '%s_%s' %(Project,Module),'scale':'%s' %(Scale), 'tag':'%s' %(Tag), 'rollback_tag':'%s' %(Rollback)})
            elif re.match(r'(test)', Scale):
                list_test.append({'name': '%s_%s' %(Project,Module),'scale':'%s' %(Scale), 'tag':'%s' %(Tag), 'rollback_tag':'%s' %(Rollback)})
            else:
                pass
        list_all.append(sorted(list_online,key=operator.itemgetter('scale')))
        list_all.append(sorted(list_test,key=operator.itemgetter('scale')))
        list_all.append(sorted(list_dev,key=operator.itemgetter('scale')))
        return list_all

class showproject(Resource):
    def get(self, project):
        sql = "select module from module_list where project = '%s' " % (project)
        __db = GetConfigure.get_mysql_client()
        info = __db.select(sql)
        list_module = []
        for i in info:
            Module = i[0]
            list_module.append(Module)
        return list_module
    def post(self):
        pass
