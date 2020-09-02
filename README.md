# yaml_to_markdown
将yaml文件转化MARKDOWN,随后准备生成gitbook  

npm install gitbook-cli -g  

run_gitbook.sh是用来运行gitbook内容的脚本  
module中存放这cases转化yaml成MarkDown的Python脚本和gitbook的配置文件  

recording_service文件夹中是yaml生成用的服务内容  

yaml文件都存放在cases文件夹中，利用文件夹表示层级关系。文件夹同层级需要一个和文件夹相同名字的yml文件来作为根内容。
yaml用例事例
````yaml
#【必填】Desc: 测试用例详细描述
Desc: 直播轻互动和互动热度
#【可选】PreCondition 前置条件
PreCondition:
  - 使用6.0.80及以上版本
#【必填】TestPlan：编写测试用例
TestPlan:
  #【必填】CheckPoint 表示“测试点”
  -
    CheckPoint:
      #【必填】desc：测试点描述
      desc: 互动资源下发错误
      cases:
        #【必填】cases：放置具体测试用例
        -
          case:
            action: 没有下发动效资源btn_like_resource，或者下发的不合法
            assert: 不展示飘心动画，不展示热度，也不去轮询拉取热度接口
            iOSAutoTest: testInvalidResource
            androidAutoTest: testInvalidResource
  -
    CheckPoint:
      desc: 互动资源下发正确
      level: P1
      cases:
        -
          case:
            action: 展示动画
            assert: UI符合预期
        -
          case:
            action: 拉取热度值
            assert: 拉回来N条，按照每秒N/5去递增的展示
        -
          case:
            action: 查看热度值展示
            assert: 位置：在心的上方，数字规则：按照通用的来，大于9999显示万
        -
          case:
            action: 点击心
            assert: 本地假写，热度值+1，同时调用点赞计数增加的接口
#【必填】版本变更记录，版本号+负责人，中间按空格分开，版本号必须是3段格式，包含4个数字，如6.0.90
ChangeLog:
  -
    version: 6.0.80 (authorname）
    message: 这次修改了什么
  -
    version: 6.0.81 (authorname）
    message: 这次又修改了什么
#【可选】Story: 需求链接（多个需求使用数组格式）
Story:
  -
    name: 需求
    link: http://tapd.oa.com/10045201/prong/stories/view/1010045201857627509
#【可选】RelatedModule：额外关联模块，如果此用例同时影响其他模块，则在此处填写
RelatedModule:
  - Video/直播底层/普通直播
#【可选】IncludeTestCase：引入测试用例，填写后会自动将关联的测试用例包含进来
IncludeTestCase:
  - 日夜间适配
  - 网络适配
````
在运行转换用例以后生成的md文件会存放在md_cases,所有的结构都会和cases一模一样。在运行的时候会删除之前生成的用例内容。
