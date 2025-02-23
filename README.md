# AFEDIUM (Advanced Fursuit of Electrical Device and Information Universal Manager)

## TODO: 
+ ### 模块化框架: 
+ [x] 通用插件加载
+ [x] 通用数据传输存储协议
+ [x] 通用配置文件存储模块
+ [x] Events/指令系统
+ [x] 日志系统
+ [ ] ~~↑ 自动汇报开发者~~
+ [ ] ahpc总线通讯协议
+ [ ] 高可用自动恢复

+ ### 动眼模块: 
+ [x] 动态加载
+ [x] gif支持
+ [ ] ~~加载优化~~
+ [x] 双屏支持
+ [x] 使用tag格式存储图层
+ [x] 覆盖图层（异瞳支持）
+ [ ] 骨骼动画支持
+ [ ] 动态缩放支持


## 部署说明:

建议python版本3.10。

你需要安装`tkinter pillow`

正常情况下无需配置开箱即用。（使用默认瞳孔，单显示器）

替换`eyeball.png`即可更换瞳孔，

在`display.json`中`addon`添加
`‘文件名’: [1, [0](显示器ID，视情况决定), 'eyeball']`即可使用异瞳
<br>*注：文件名可忽略后缀*

| 配置文件             | 所属插件 | 功能               |
|------------------|------|------------------|
| main.json        | 核心   | 禁用其他插件，调整debug模式 |
| display.json     | 显示模块 | 调整显示器数量，显示图层     |
| display_pos.json | 控制模块 | 调整显示动作逻辑         |


+ ### 高级部署
*WIP*
