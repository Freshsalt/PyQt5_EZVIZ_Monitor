

# 前言

**这是作者的本科课程设计作业，时间只有一周，所以制作较为简陋。项目主要利用了PyQt5环境，借助学校老师提供的萤石摄像头（CS-XP1）从而实现远程（或局域网）监控系统。实现云台控制，视频流显示，电子缩放等功能。**

# 使用步骤

## 1.安装工具

前置环境：Pycharm、Anaconda/miniconda、PyQt5等。

在安装了Pycharm与Anaconda/miniconda后，下载PyQt5，在windows端中打开命令行，输入

```
pip install pyqt5

pip install pyqt5-tools
```

随后打开Pycharm，于**文件-设置-外部工具**中增加QtDesigner、QtDesigner-Edit、PyUIC、PyRcc四个工具。

第一个工具：QtDesigner

```
Name：QtDesigner （名称可以自定义，要方便分辨即可）

Group：Qt （默认是 External Tools，可自定义组名）

Program：..\Anaconda3\Lib\site-packages\qt5_applications\Qt\bin\designer.exe（conda默认将pip安装的包放在自己的文件夹内）

Arguments：（不填）

Working directory： $ProjectFileDir$
```

第二个工具：QtDesigner-Edit

```
Name：QtDesignerEdit （名称可以自定义，要方便分辨即可）

Group：Qt （默认是 External Tools，可自定义组名）

Program：同上

Arguments：$FileName$

Working directory：$FileDir$
```

第三个工具：PyUIC

```
Name：PyUIC （名称可以自定义，要方便分辨即可）

Group：Qt （默认是 External Tools，可自定义）

Program：E:\Python\Anaconda3\python.exe（选择的是要导出的Python版本，一般为Anaconda文件夹下的python.exe或者对应env中的python.exe）

Arguments： -m PyQt5.uic.pyuic $FileName$ -o $FileNameWithoutExtension$.py

Working directory： $FileDir$
```

第四个工具：PyRcc

```
Name：PyRcc （名称可以自定义，要方便分辨即可）

Group：Qt （默认是 External Tools，可自定义）

Program：..\Anaconda3\envs\ptyolo5\Scripts\pyrcc5.exe
（Program路径注意：选择的是要导出的Python版本所对应的虚拟环境，一般为Scripts文件夹下的pyrcc5.exe）

Arguments： $FileName$ -o $FileNameWithoutExtension$_rc.py

Working directory： $FileDir$
```

验证工具是否可以使用，选择**工具-Qt（自己定义的Group）-QtDesigner**。能够正常打开即可。

在页面编辑完成后，保存xxx.ui文件，在Pycharm中**右键**该文件夹,选择**Qt（自己定义的Group）-PyUIC**，会生成一个同名的xxx.py文件，我们之后将调用该文件。值得注意的是，如果在生成py文件过程中报错，请检查上述外部工具配置是否正确。

## 2.获取萤石API接口与RTSP链接

网页搜索**萤石开放平台**（https://open.ys7.com），登录后进入控制台，在设备管理一栏检查自己的摄像头是否已绑定个人账号。首先给摄像头上电并联网。进入**设备详情**，关闭**设备加密**，后在左侧栏选择**账号中心-应用中心**创建应用，获得应用密钥和Token等。注意，Token存在有效期，有效期过后，需要更新以获取新的Token，这个过程是免费的。

下载萤石工作室（https://service.ezviz.com/downloadInfoSite/document/69.html），下载后对设备进行高级配置。**我的设备-设置-账号内设备-高级设置**进入后选择**网络-常用**，右侧栏可以查看到局域网的IPv4地址和RTSP端口，将其放于代码中更改即可。

## 3.编写主程序

新建.py文件，调用刚刚生成的xxx.py文件，之后便可以在本程序中控制各类模组的信号与槽机制。请确保在**QtDesigner**内定义的模组名与主程序的模组名对应，否则无法将其关联。另外，如果要更改页面，可以**右键**xxx.ui文件，选择**QtDesigner-Edit**进行编辑。

# 效果

效果如图所示，成功调用萤石摄像头，并对其云台进行控制。

![image-20241206194541116](F:\work\Univesity\大四\大四上\课设\picture_01.png)

# 许可

该项目遵循MIT协议

# 联系我们

如有更好的方案或纠错，你可以尝试以下方式联系作者：

Email: [1248739523@qq.com](mailto:1248739523@qq.com)

# 参考文章

##### Pycharm配置QtDesigner：https://blog.csdn.net/Emins/article/details/124915601