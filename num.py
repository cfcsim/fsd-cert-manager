import fsdcert

cert = fsdcert.cert()


def check(string: str, mode=None):
    for word in ["'", '"', ";"]:
        if word in string:
            return False
    if mode == "callsign":
        if not len(string) == 7:
            return False
        if (
            not string[0:3].isalpha()
            or not string[0:3].isupper()
            or not string[3:7].isdigit()
        ):
            return False
    elif mode == "level":
        try:
            intstr = int(string)
        except ValueError:
            return False
        if intstr < 0 or intstr > 12:
            return False
    return True


while True:
    oper = input("请选择操作(C新建呼号 M更改信息 D删除呼号 I查询信息): ")
    if not oper in ["C", "M", "D", "I"]:
        print("错误的选择!")
        continue
    break
if oper == "C":
    while True:
        callsign = input("呼号: ")
        if not check(callsign, mode="callsign"):
            print("输入不正确!")
            continue
        if input(f"呼号是: {callsign} 要重新输入吗(Y确认呼号, 任意按键重新输入)? ") == "Y":
            break
    if callsign in cert:
        print("呼号已存在!")
        raise SystemExit
    while True:
        password = input("密码: ")
        if not check(password):
            print("输入不正确!")
            continue
        if input(f"密码是: {password} 要重新输入吗(Y确认密码, 任意按键重新输入)? ") == "Y":
            break
    cert[callsign] = {"password": password, "level": 1}
elif oper == "M":
    while True:
        callsign = input("呼号: ")
        if not check(callsign, mode="callsign"):
            print("输入不正确!")
            continue
        if input(f"呼号是: {callsign} 要重新输入吗(Y确认呼号, 任意按键重新输入)? ") == "Y":
            break
    if not callsign in cert:
        print("呼号不存在!")
        raise SystemExit
    while True:
        oper = input("更改密码或权限(P密码, L权限)? ")
        if not oper in ["P", "L"]:
            print("错误的选择!")
            continue
        break
    if oper == "P":
        while True:
            password = input("密码: ")
            if not check(password):
                print("输入不正确!")
                continue
            if input(f"密码是: {password} 要重新输入吗(Y确认密码, 任意按键重新输入)? ") == "Y":
                break
        cert[callsign] = {"password": password}
    elif oper == "L":
        while True:
            level = input("权限: ")
            if not check(level, mode="level"):
                print("输入不正确!")
                continue
            if input(f"权限是: {level} 要重新输入吗(Y确认密码, 任意按键重新输入)? ") == "Y":
                break
        cert[callsign] = {"level": int(level)}
elif oper == "D":
    while True:
        callsign = input("呼号: ")
        if not check(callsign, mode="callsign"):
            print("输入不正确!")
            continue
        if input(f"呼号是: {callsign} 要重新输入吗(Y确认呼号, 任意按键重新输入)? ") == "Y":
            break
    del cert[callsign]
elif oper == "I":
    while True:
        callsign = input("呼号: ")
        if not check(callsign, mode="callsign"):
            print("输入不正确!")
            continue
        if input(f"呼号是: {callsign} 要重新输入吗(Y确认呼号, 任意按键重新输入)? ") == "Y":
            break
    if not callsign in cert:
        print("呼号不存在!")
        raise SystemExit
    info = cert[callsign]
    print(f"等级: {info['level']}, 密码: {info['password']}")
