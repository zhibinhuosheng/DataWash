from datetime import datetime
from log import tc
class Test_XXX:
    """
    @TestCaseNumber:
    @TestCaseName:
    @PreCondition:
        1、XXX设置为XXXX
    @TestStep:
        1.进行XXX
        2.进行XXXX
    @ExpectedResult:
        1.进行XXXXX
        2.执行XXXXXXXX
    @Return:
    @ModifyRecord:
    """

    def Precondition(self):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tc.logInfo(f"前置条件：XXX{time}设置为XXXX")
        # XXX设置为XXXX的具体实现代码
        print("前置条件：XXX设置为XXXX")

    def test_Procedure(self):
        tc.logInfo("测试步骤：进行XXX")
        # 进行XXX的具体实现代码
        tmp = 123
        if tmp > 100:
            tc.logInfo("测试步骤：进行XXX")
            # 进入True的代码
        else:
            tc.logInfo("测试步骤：进行XXX")
            # 进入False的代码
        print("测试步骤：进行XXX")
        tmp = 123
        if tmp > 100:
            tc.logInfo("测试步骤：进行XXX")
            # 进入True的代码
        elif tmp == 100:
            tc.logInfo("测试步骤：进行XXX")
            # 进入False的代码
        else:
            tc.logInfo("测试步骤：进行XXX")
            # 进入else的代码
        print("测试步骤：进行XXX")
        tc.logInfo("查询XXX")
        # 查询XXX的具体实现代码
        print("查询XXX")

    def Postcondition(self):
        tc.logInfo("后置条件：XXX设置为XXXX")
        # XXX设置为XXXX的具体实现代码
        print("后置条件：XXX设置为XXXX")
        print("后置条件：XXX设置为XXXX")
        print("后置条件：XXX设置为XXXX")
