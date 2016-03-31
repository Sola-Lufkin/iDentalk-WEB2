iDentalk
==============================

It's a SNS website for dentist and patient.

> Master为主分支，部署在AWS上。
> Dev为开发分支，未完成，不可部署。分支上`static/phonegap-try`有Phonegap测试版本，未完成，不可用。

## Env
---------------------------------

* Ubuntu 12.04

* Python 2.7.3

* Django 1.2.7

* Mysql

* Apache

## Usage
---------------------------------

### Back-end
网站后台方面，功能的实现都主要集中在了根目录下apps文件夹里。根据网站不同身份，功能不同的特征，将所有的app分成了以下几个大块，而每个块中再有不同单一功能模块的小块。


* dentist_apps 用于实现医生所有专属功能的app集合包
* patient_apps 用于实现病人所有专属功能的app集合包
* public_apps  用于实现医生和病人共同功能的app集合包
* extra_apps   存放了包括registration在内的第三方app集合包

以下是关于这是个app集合包的具体说明


####dentist_apps
	den_manage 用于实现医生的病人列表，返回与医生存在关系的病人的基本信息，并在页面上显示
	den_profile 用于向数据库读取与写入当前医生的个人信息，包括姓名，专业，诊所等，并在页面渲染显示
	dentist 同样用于向数据库读取当前医生的个人信息，不过该app是在病人访问医生时调用。 另外app还包括了QA功能模块的实现
	gallery 用于实现医生的病例相册的实现，并在页面渲染显示
	stream  用于实现医生的主页timeline信息流功能

####patient_apps 
	pat_manage 用于实现病人的医生列表，返回与当前病人存在关系的医生的基本信息，并在页面渲染显示
	pat_profile 用于向数据库读取与写入当前病人的个人信息，包括姓名，问卷，地理位置等，并在页面渲染显示
	patient  用于实现病人主页的渲染。另外app还包括了病人calendar功能模块的实现

####public_apps
	accounts  用于实现用户帐户操作的一些功能，包括登陆，密码修改等基本操作
	iDenMail  用于实现用户之间的iDenMail的通信操作
	imgupload 用于实现左右图片的上传功能。   值得注意的是，这里的图片都是上传到S3服务器上，而非本地。在操作S3的api时调用了第三方app boto
	notification 用于实现用户之间站内通信和操作时的通知提醒
	profile  该app主要定义了用户基本信息的数据modle，并在数据库创建了相应的表
	public  该app主要包括了一些基本的通用函数
	relationship 用于实现用户之间的关系操作
	search 用于实现用户的搜索操作

####extra_apps
	annoying  该app为第三方app，包装了一些方便使用的修饰器，用于减少重复代码。值得注意的是，为了符合网站功能，在修饰器中有少许代码有过修改
	captcha   该app为第三方app，用于实现验证码功能
	registration  该app为第三方app，用于实现登陆，注册，验证邮件等核心的帐户功能。值得注意的是，为了符合网站功能，在修饰器中有少许代码有过修改


####关于后台其他文件

####根目录下config文件夹
	由于测试和部署需要，将原本的配置文件config改写成了两个版本，并在根目录下settings.py文件里通过切换from local import * 来变换调用不同的配置文件，实现本地和服务器两个不同环境下的自动识别
####根目录下templates文件夹
    按照app的功能分类，相应的存放了渲染页面所需要的Html模版文件
####根目录下decorators.py文件
	由于功能的需要编写的修饰器，用于在函数执行前对函数进行身份要求的修饰，如果不满足身份要求，将跳转到ErrorPage




### Front-end

静态文件包括图片、js、css都存放于`static`目录下

CSS使用了`Bootstrap`, `FontAwsome`

JS使用`requirejs`模块化代码，并用`r.js`合并压缩文件存放在`js-bulid`文件下。`r.js`的配置文件为`static/js/bulid.js`

页面脚本在`scripts`下，模块存放在`modules`下，`tmpl`存放DOM模板，`utils`存放jquery插件。

#### Module

* common

	* avatar.js 头像上传

	* contact.js 发送message

	* global.js 页面全局设置

	* mail.js iDentalk页面发送消息

	* message.js 轮询后端查询最新message

* dentist

	* baseinfo.js 医生主页基本信息

	* gallery.js 医生主页gallery

	* profile.js 医生主页profile

	* qa.js 医生主页qa

	* stream.js 医生主页信息流

* patient

	* baseinfo.js 病人个人信息

	* follow_action.js 病人关注医生操作

	* stream.js 病人主页信息流

#### scripts
	
* common

	* calendar.js 日历页面

	* index.js iDentalk主页

	* info_step.js 注册信息填写页面

	* notification.js 提醒页面

	* setting.js 用户个人设置页面

* dentist

	* den_homepage.js 医生个人主页

	* den_mail.js 医生mail页面

	* den_public.js 公共视角医生主页

	* gallery_edit.js 医生gallery操作

	* manage_pat.js 医生对病人操作

	* unique_post.js 单独post页面

	* worklocation.js 医生worklocation操作

* patient

	* pat_edit.js 病人个人基本休息操作

	* pat_homepage.js 病人个人主页

	* pat_mail.js 病人mail页面

	* search.js 搜索医生


### Mobile app

`static/mobile-app`,基于jquery-mobile.


### AWS部署
本地代码向服务器端同步，通过git来完成


在本地段存有pem密钥文件后，通过命令`ssh -i identalkwebkey.pem ubuntu@ec2-23-21-234-99.compute-1.amazonaws.com`进入云端服务器
切换至云端目录`/var/www/iDentalk`进入到项目文件夹，通过命令`git pull`同步github上的代码。
值得注意的是在服务器段尽量只做pull操作，避免直接修改云端代码，或者push代码。


####AWS RDB信息：
	master user name:  dbadmin
	master Pasword:  5$perDBinst
	identalkdb.co6kezkdcruj.us-east-1.rds.amazonaws.com

####服务器端phpmyadmin远程访问地址
    http://23.21.234.99:8080/phpmyadmin/index.php?db=iDentalk&server=2&token=9821d772287fa84e481e129a0bc74167
    用户名: dbadmin
    密码: 5$perDBinst


## Bugs

### Front-end

* 大部分js文件中，对元素先unbind再bind的绑定方式错误的，用on来代替。


## Todos

