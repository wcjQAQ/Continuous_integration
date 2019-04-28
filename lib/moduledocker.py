import docker


class DockerAPI(object):
    def __init__(self, ip, port='10000'):
        self.__base_url = 'tcp://%s:%s' % (ip, port)
        self.conn = docker.APIClient(base_url=self.__base_url, timeout=30)

    def check_crontainer_exists(self, container_name):
        try:
            self.conn.inspect_container(container=container_name)
            return True
        except Exception as err:
            #log.error(err)
            return False

    def check_image_exist(self, image):
        try:
            self.conn.inspect_image(image=image)
            return True
        except Exception:
            return False

    def start_container(self, container_name):
        if not self.check_crontainer_exists(container_name):
            #log.error('container %s not exists' % container_name)
            raise IndentationError('container %s not exists' % container_name)
        try:
            self.conn.start(container=container_name)
        except Exception as exc:
            log.error(traceback.format_exc())
            raise exc
    def stop_container(self, container_name):
        if not self.check_crontainer_exists(container_name):
            print('container %s is not exists' % container_name)
            return
        try:
            self.conn.stop(container=container_name)
            print('ok')
        except Exception as exc:
            #log.error(traceback.format_exc())
            raise exc

    def remove_container(self, container_name):
        if not self.check_crontainer_exists(container_name):
            #log.warning('container %s is not exists' % container_name)
            return
        try:
            self.conn.remove_container(container=container_name)
        except Exception as exc:
            #log.error(traceback.format_exc())
            raise exc

    def restart_container(self, container_name):
        if not self.check_crontainer_exists(container_name):
            #log.warning('container %s is not exists' %s container_name)
            return
        try:
            self.conn.restart(container=container_name)
        except Exception as exc:
            log.error(traceback.format_exc())
            raise exc

    def kill_container(self, container_name):
        if not self.check_crontainer_exists(container_name):
            log.warning('container %s is not exists' % container_name)
            return
        try:
            self.conn.kill(container=container_name)
        except Exception as exc:
            log.error(traceback.format_exc())
            raise exc

    def inspect_image(self, image):
        self.conn.inspect_image(image=image)

    def inspect_container(self, container_name):
        self.conn.inspect_container(container=container_name)