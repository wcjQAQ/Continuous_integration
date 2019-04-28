import requests
from lib.moduledocker import DockerAPI
from os import path
import traceback
from time import sleep
def check_url_status(url):
    try:
        response = requests.get(url=url, timeout=10)
        status = response.status_code
        res = str(response.text.strip())
        # noinspection PyUnreachableCode
        if status == 200:
            return res
        else:
            print('file %s not exists! http status is %s' % (url, status))
            raise BaseException
    except Exception as exc:
        raise exc


class deploy():
    def __init__(self, project, module, scale, hostip, port, container_name, image, tag):
        self.project = project
        self.module = module
        self.scale = scale
        self.hostip = hostip
        self.port = port
        self.container_name = container_name
        self.image = image
        self.tag = tag
        self.__docker_api = DockerAPI(ip=hostip)

    def start(self):
        if self.__docker_api.check_image_exist(self.image) == False:
            print('Pull image %s' % (self.image))
            try:
                #dockerauth = {'username' : 'admin', 'password' : 'Hzwbg@2016'}
                #self.__docker_api.conn.pull(self.__image, auth_config=dockerauth)
                self.__docker_api.conn.pull(self.image)
            except Exception as exc:
                print('Pull images %s 失败' % (self.image))
                raise exc


        ### 设置变量
        package_name = '%s.%s.war' % (self.tag, self.module)
        domain_name = 'http://package.wcj.com'
        PACKAGE_REGISTRY_URL = path.join(domain_name, self.project, self.module)
        env = { }
        env['PACKAGE_REGISTRY_URL'] = '%s/%s' % (PACKAGE_REGISTRY_URL,package_name)
        env['TAG'] = self.tag
        env['HOST'] = self.hostip
        env['PORT'] = self.port
        env['PROJECT'] = self.project
        env['MODULE'] = self.module
        env['SCALE'] = self.scale

        ### 设置端口绑定
        expose_port = 8080
        port_bindings = {expose_port: (str(self.hostip), self.port)}

        ### 设置hosts
        extra_hosts = {
                        'package.wcj.com': '172.17.0.1',
                        'jenkins.wcj.com': '172.17.0.1'
                      }

        ### 设置日至挂载
        apphome = '/home/docker/app'
        loghome = path.join(apphome, 'tomcat', self.project, self.module, self.scale, str(self.port))
        binds = {loghome: {'bind': '/opt/apache-tomcat-8.5.37/logs', 'mode': 'rw'}}


        ### 启动docker
        if self.__docker_api.check_crontainer_exists(container_name=self.container_name):
            print('stopping container %s' %self.container_name)
            self.__docker_api.stop_container(container_name=self.container_name)
            self.__docker_api.remove_container(container_name=self.container_name)
            print('%s 删除成功' % self.container_name)

        host_config = self.__docker_api.conn.create_host_config(binds=binds, port_bindings=port_bindings,extra_hosts=extra_hosts,restart_policy={'Name': 'always'},network_mode='bridge')

        container_id = self.__docker_api.conn.create_container(image=self.image,environment=env,host_config=host_config,name=self.container_name)['Id']
        self.__docker_api.start_container(self.container_name)
        print('create container %s success' % (self.container_name))


        count = 60
        while count:
            try:
                url = 'http://' + self.hostip + ':' + str(self.port) + '/tag.txt'
                res_tag = check_url_status(url=url)
                #print(res_tag)
                #print(self.tag)
                if '%s' %res_tag == '%s' %self.tag:
                    print('update %s:%s success' % (self.hostip, self.port))
                else:
                    #print('updtae faild, %s request tag is %s and The correct tag shuuld be %s' % (url, res_tag, self.tag))
                    print('access tag.txt error,count:%s' %count)
                    raise Exception('request timeout or update faild')
                break
            except Exception as exc:
                print(exc)
                count -= 1
                sleep(1)
                continue

        return container_id

    def remove(self):
        if self.__docker_api.check_crontainer_exists(container_name=self.container_name):
            print('stopping container %s' %self.container_name)
            self.__docker_api.stop_container(container_name=self.container_name)
            self.__docker_api.remove_container(container_name=self.container_name)
            print('%s 删除成功' % self.container_name)

