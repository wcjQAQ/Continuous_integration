from flask import jsonify, abort, make_response, render_template
from flask_restful import Resource, reqparse, fields
from etc.configure import GetConfigure
class showtag(Resource):
    def get(self, project, module):
        #parser = reqparse.RequestParser()
        #parser.add_argument('project', type=str, location=['form', 'json', 'values', 'args'], required=True)
        #parser.add_argument('module', type=str, location=['form', 'json', 'values', 'args'], required=True)
        # strict = True 如果参数中出现解析器中未定义的参数抛出异常
        #args = parser.parse_args(strict=True)
        #project = args['project']
        #module = args['module']
        sql = 'select * from tag_list where project="%s" and module="%s"' % (project, module)
        __db = GetConfigure.get_mysql_client()
        info = __db.select(sql)
        print(sql)
        tag_list = []
        for d in info:
            project = d[1]
            module = d[2]
            scale = d[3]
            tag = d[4]
            rollbak_tag = d[5]
            create_time = d[6]
            update_time = d[7]
            #tag_list.append({'project': '%s' %project, 'module': '%s' %module, 'scale': '%s' %scale, 'tag': '%s' %tag, 'rollback': '%s' %rollbak_tag, 'create_time': '%s' %create_time, 'update_time': '%s' %update_time})
            tag_list.append({'project': '%s_%s' % (project,module), 'scale': '%s' %scale, 'tag': '%s' %tag, 'rollback': '%s' %rollbak_tag, 'create_time': '%s' %create_time, 'update_time': '%s' %update_time})
        #return make_response(render_template('tag.html', tag_list=tag_list))
        return tag_list

    def post(self):
        pass


class showproject(Resource):
    def get(self):
        sql = 'select  distinct  project,module  from server_list;'
        __db = GetConfigure.get_mysql_client()
        info = __db.select(sql)
        server_list = []
        for server in info:
             server_list.append({"project":server[0],"module":server[1]})
        return server_list

    def post(self):
        pass
