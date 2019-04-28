#!/bin/bash
Date="$(date +'%Y-%m-%d_%H-%M-%S')"
if [ ! -n "$Tag" ]; then
    Tag="TAG-${Date}"
fi
# 解析命令行参数
eval $@
####### 显式引用变量  ########
# jenkins 变量,
branch="$branch"
user_name="$BUILD_USER"
build_id="$BUILD_NUMBER"
# 命令行参数
program_name="$program_name"
#
project_url="$project_url" # git 地址
project="$project" # 项目名称
module="$module" # 模块名称 web admin h5 or master security or server
scale="$scale" # 服务级别
package_home="/var/jenkins_home/package/${project}/${module}"

# 如果必须的变量为空,则退出
if [ "$branch" == "" ] || [ "$user_name" == "" ] || [ "$build_id" == "" ]
then
    echo "$(Time) jenkins variable [ branch|user_name|build_id ]can't null;"
    echo "$(Time) \$branch is $branch"
    echo "$(Time) \$user_name is $user_name"
    echo "$(Time) \$build_id is $build_id"
    exit 1
fi

#

##根据program_name判断package_name的命名##
if [ "${program_name}" == "java" ]
then
  package_name=${Tag}.${module}.war
elif [ "${program_name}" == "js" ] || [ "${program_name}" == "python" ]
then
  package_name=${TAG}.${module}.tar
else
  echo "Please set program_name"
  exit 1
fi

##java的打包##
java_make_packed() {
    if [ ${project} == "test" ]
    then
        if [ ${module} == "master" ]
        then
            git checkout ${branch}
            git pull
            echo ${Tag} > $WORKSPACE/src/main/webapp/tag.txt
            echo  ${branch}-${Tag} > $WORKSPACE/src/main/webapp/version.txt
            #/var/jenkins_home/bin/maven/bin/mvn clean install
            mvn clean install
            war_name=$(ls -t target/*.war | tail -1)
            [ ! -d ${package_home} ] && mkdir -p ${package_home}
            cp -frp $war_name $package_home/${package_name}
        else
            echo "ok"
        fi
     fi

     ###git生成TAG###
     cd ${WORKSPACE}
     git config --global user.email "${user_name}@wcj.com"
     git config --global user.name "${user_name}"
     git tag -a $Tag -m "add tag $Tag"
     git push --tags


}
tomcat_deploy() {
    args="project=$project&module=$module&scale=$scale&tag=$Tag"
    #echo "run command:  curl -si  -X POST -d \"$args\" http://192.168.31.100:5000/api/update/tomcat"
    #echo "=================================================================================="
    #echo -e "                         【 正在部署,请稍等... 】"
    #echo "=================================================================================="
    curl -si  -X POST -d "$args" http://192.168.31.100:5000/api/update/tomcat

}

if [ "$program_name" == "java" ]
then
    java_make_packed
    tomcat_deploy
elif [ "$program_name" == "js" ]
then
    js_make_packed
    html_deploy
else
    echo "请输入 项目名称"
    exit 1
fi
