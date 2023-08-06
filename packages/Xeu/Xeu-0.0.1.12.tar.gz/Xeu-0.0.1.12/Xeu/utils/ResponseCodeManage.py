# _*_ coding:utf-8 _*_


class ResponseCode:

    InfoGothOK = ["base.InfoGoOK", "信息获取成功"]
    OrganAuthOK = ["auth.OrganAuthOK", "机构验证正确"]
    PhoneAvailableOK = ["base.PhoneAvailableOK", "手机号可用"]
    PhoneChangeOK = ["0", "变更成功"]
    RespOK = ["0", "响应成功"]
    RegisterOK = ["base.RegisterOK", "注册成功"]
    RegisterDuplication = ["base.RegisterDuplication", "重复注册"]
    AccountPasswordAuthOk = ["0", "账号密码正确"]
    UserInfoAuthOk = ["0", "用户信息校验成功"]
    ParamsError = ["base.ParamsError", "参数不正确"]
    RequiredParameterMissingError = ["1", "参数缺失"]
    NonExistent = ["2", "信息不存在或已失效"]
    PhoneAvailableNo = ["base.PhoneAvailableNo", "手机号已占用"]
    IllegalMobile = ["base.IllegalMobile", "手机号不合法"]
    PhoneNonExistent = ["5", "手机号不存在"]
    VerCodeSendSuccess = ["base.VerCodeSendSuccess", "验证码发送成功"]
    VerCodeSendFail = ["base.VerCodeSendFail", "验证码发送失败"]
    PhoneChangeFail = ["6", "变更失败"]
    AccountPasswordAuthFail = ["7", "账号密码验证不通过"]
    RegisterFail = ["7", "注册失败"]
    UserNameError = ["8", "姓名不匹配"]
    PlatformAuthFail = ["8", "平台校验不通过"]
    ServicesError = ["sys.ServicesError.", "服务异常,请稍后重试"]
