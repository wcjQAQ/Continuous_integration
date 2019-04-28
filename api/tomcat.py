from flask_restful import Resource, reqparse
from flask import make_response, jsonify
from etc.configure import GetConfigure
from lib.deploytomcat import deploy
import time
class UpdateTomcat(Resource):
    def __init__(self):
        self.servername = 'tomcat'

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project', type=str, location=['form', 'json', 'values', 'args'], required=True)
        parser.add_argument('module', type=str, location=['form', 'json', 'values', 'args'], required=True)
        parser.add_argument('scale', type=str, location=['form', 'json', 'values', 'args'], required=True)
        parser.add_argument('tag', type=str, location=['form', 'json', 'values', 'args'], required=True)
        # strict = True 如果参数中出现解析器中未定义的参数抛出异常
        args = parser.parse_args(strict=True)
        project = args['project']
        module = args['module']
        scale = args['scale']
        tag = args['tag']
        serverlist = GetConfigure.get_serverlist()
        hps = serverlist[self.servername][project][module][scale]
        hostips = hps['hostips']
        ports = hps['ports']

         #添加删除机制, 删除旧节点
        __db = GetConfigure.get_mysql_client()
        sql = 'select hostip,port from server_list where project="%s" and module="%s" and scale="%s";' % (
            project, module, scale)
        print('查询当前运行节点sql: %s' % sql)
        try:
            results = __db.select(sql=sql)
            print(results)
            old_server_list = list(results)
            if old_server_list:
                print('当前运行环境 %s' % old_server_list)
            else:
                print('查询结果为空')
        except Exception as exc:
            raise exc

        for hostip in hostips:
            for port in ports:
                if old_server_list:
                    for i in old_server_list:
                        print(i)
                        old_port = i[1]
                        old_hostip = i[0]
                        if port == old_port and hostip == old_hostip:
                            print("从列表中删除%s:%s" % (hostip, port))
                            old_server_list.remove(i)
                image = GetConfigure.get_docker_image(module)
                container_name = '%s_%s_%s_%s_%s' % (self.servername, project, module, scale, port)
                print("image:%s, container:%s, Hport:'%s:%s'" % (image, container_name, hostip,port ))
                start_container = deploy(project, module, scale, hostip, port, container_name, image, tag)
                start_container.start()

                ###update server_list
                server_name = 'tomcat'
                sql='select id from `server_list` where hostip="%s" and port=%d and module="%s" and project="%s";' % (hostip, port, module, project)
                print('查询当前的节点是否在server_list表中:%s'%sql)
                if __db.existence(sql):
                    #sql = "update server_list set server_name='%s' where project='%s' and hostip='%s' and port='%s';" %(server_name,project,hostip,port)
                    #print(sql)
                    #__db.update(sql)
                    pass
                else:
                    sql = 'insert into server_list (project, module, scale, server_name, hostip, port) VALUES ("%s","%s","%s","%s","%s",%s);'  \
                       % (project, module, scale, server_name, hostip, port)
                    print(sql)
                    __db.insert(sql)

        ###更新或者插入tag_list表
        now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = 'select tag from `tag_list` where scale="%s" and project="%s" and module="%s";' % (scale, project, module)
        print("查看当前项目是否在tag_list表创建:%s" %sql)
        if __db.existence(sql):
            ##查询结果: list ---> tuple ---> str
            rollback_tag = __db.select(sql)[0][0]
            print('回滚tag为: %s' %rollback_tag)
            sql = 'update tag_list set tag="%s",rollback_tag="%s",update_time="%s" where scale="%s" and project="%s" and module="%s";' % (tag, rollback_tag, now_date, scale, project, module)
            print('更新当前项目的tag_list状态:%s' %sql)
            __db.update(sql)
        else:
            sql = 'insert into tag_list (project, module, scale, tag, rollback_tag, create_time, update_time) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s");' \
                       % (project, module, scale, tag, tag, now_date, now_date)
            print('将当前项目状态插入tag_list表:%s' %sql)
            __db.insert(sql)


        #删除不再serverlist.json的节点
        #if old_server_list:
        #    print("删除所有不用的节点")
        #    for i in old_server_list:
        #        print(i)
        #        port = i[1]
        #        hostip = i[0]
        #        container_name = '%s_%s_%s_%s_%s' % (self.servername, project, module, scale, old_port)
        #        rm_container = deploy(project, module, scale, hostip, port, container_name, image, tag)
        #        rm_container.remove()
        #        sql = 'delete from `server_list` where hostip="%s" and port=%d and module="%s" and project="%s";' % (
        #        hostip, port, module, project)
        #        print("删除server_list的节点:%s" %sql)
        #        __db.insert(sql)




        return make_response(jsonify({'request': args, 'status': 'yes'}), 200)


