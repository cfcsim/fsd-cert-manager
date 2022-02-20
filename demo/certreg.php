<!DOCTYPE html>
<html>
<head>
        <meta charset="utf-8"> 
        <title>呼号注册</title>
        <link rel="preconnect" href="https://www.gstatic.com" crossorigin>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@5.15.4/css/all.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@5.15.4/js/all.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script src="https://ssl.captcha.qq.com/TCaptcha.js"></script>
</head>
<body style="background-repeat:no-repeat; background-size:100% 100%; background-attachment: fixed;" background="https://images.pexels.com/photos/326136/pexels-photo-326136.jpeg?fit=crop&fm=jpg&h=1080&w=1920">
<style>
        .modal-dialog {
        opacity: 0.75;
        position: absolute;
        top: 50%;
        width: 100%;
        left: 50%;
        z-index: 3;
        margin: auto; 
        -webkit-transform: translate(-50%, -50%) !important;
        -moz-transform: translate(-50%, -50%) !important;
        -ms-transform: translate(-50%, -50%) !important;
        -o-transform: translate(-50%, -50%) !important;
        transform: translate(-50%, -50%) !important;
    }
</style>
<script>
    window.onload = function() {
        $("#reg").modal({show:true, backdrop: 'static', keyboard: false}); 
        $("#reg").modal('show');
    }; 
    window.captexec = function (res) {
        if (res.ret === 0) {
            $("input[name='captTicket']").val(res.ticket);
            $("input[name='captStr']").val(res.randstr);
            $("#reg_form").submit();
        }
    }
    function gennum() {
        $("input[name='num']").val(parseInt(Math.random() * (9999 - 1000 + 1) + 1000));
        return false;
    }
</script>
<div id="reg" class="modal fade" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                <h5 class="modal-title">呼号注册</h5>
            </div>
                        <div class="modal-body">
                            <form class="form-horizontal" method="post" id="reg_form">
                    <div class="input-group form-group">
                        <input class="form-control required" type="text" placeholder="3位大写字母,例: CFC" name="acc" maxlength="3"/>
                        <input class="form-control required" type="text" placeholder="4位数字,例: 1000" name="num" maxlength="4"/>
                        <button class="btn btn-primary" onclick="return gennum()">自动生成呼号</button>
                    </div>
                    <div class="input-group form-group">
                        <input class="form-control required" type="password" placeholder="密码" name="password"/>
                    </div>
                    <input class="form-control" type="hidden" name="name"/>
                    <input class="form-control" type="hidden" name="captTicket"/>
                    <input class="form-control" type="hidden" name="captStr"/>
                </form>
                        </div>
            <div class="modal-footer">
		<div class="btn-group">
                    <!-- See Tencent captcha docs (data-appid) -->
                    <button id="TencentCaptcha" class="btn btn-secondary" data-appid="" data-cbfn="captexec" type="button">注册</button>
                </div>
            </div>
                </div>
        </div>
</div>
</body>
</html>

<?php
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        return;
    }
    function getresponse($url, $request, $type) {
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
        curl_setopt($ch, CURLOPT_POSTFIELDS, $request);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: ".$type));
        $data = curl_exec($ch);
        if($data === false){
            return curl_error($ch);
        }
        curl_close($ch);
        return $data;
    }
    $token = "parse token here";
    function alert($message) {
        echo "<script type='text/javascript'>";
        echo "alert('".$message."');";
        echo "</script>";
    }
    $post = $_POST;
    if (empty($post))
        return;
    if ($post['captTicket'] == null) {
        alert("请完成人机验证");
        return;
    } elseif ($post['captStr'] == null) {
        alert("请完成人机验证");
        return;
    }
    if ($post['num'] == null) {
        alert("必须填写呼号");
        return;
    }
    if ($post['acc'] == null) {
        alert("必须填写航司");
        return;
    }
    if ($post['password'] == null) {
        alert("必须填写密码");
        return;
    }
    $acc = $post['acc'];
    $acc_len = strlen($acc);
    $num = $post['num'];
    $num_len = strlen($num);
    if ($acc_len !== (int)"3") {
        alert("格式不正确");
        return;
    }
    if ($num_len !== (int)"4") {
        alert("格式不正确");
        return;
    }
    if (!is_numeric($num)) {
        alert("格式不正确");
        return;
    }
    if (!ctype_alpha($acc)) {
        alert("格式不正确");
        return;
    }
    if (mb_strtoupper($acc) !== $acc) {
        alert("格式不正确");
        return;
    }
    if (strstr($post['password'], ";")) {
        alert("密码不能包含分号");
        return;
    }
    if (strstr($post['password'], "'")) {
        alert("密码不能包含引号");
        return;
    }
    if (strstr($post['password'], '"')) {
        alert("密码不能包含引号");
        return;
    }
    if (strstr($acc, ";")) {
        alert("航司不能包含分号");
        return;
    }
    if (strstr($acc, "'")) {
        alert("航司不能包含引号");
        return;
    }
    if (strstr($acc, '"')) {
        alert("航司不能包含引号");
        return;
    }
    if (strstr($post['num'], ";")) {
        alert("呼号不能包含分号");
        return;
    }
    if (strstr($post['num'], "'")) {
        alert("呼号不能包含引号");
        return;
    }
    if (strstr($post['num'], '"')) {
        alert("呼号不能包含引号");
        return;
    }

    $query = $post;
    $query['token'] = $token;
    $query['name'] = $query['acc'].$query['num'];
    unset($query['acc']);
    unset($query['num']);
    $query = json_encode($query);
    # How to configure this please see Tencent captcha docs
    $captcha = Array('Action'=>'DescribeCaptchaResult', 'AppSecretKey'=>'', 'CaptchaAppId'=>'', 'CaptchaType'=>'9', 'Nonce'=>rand(), 'Randstr'=>$post['captStr'], 'SecretId'=>'', 'Ticket'=>$post['captTicket'], 'Timestamp'=>time(), 'UserIp'=>$_SERVER['REMOTE_ADDR'], 'Version'=>'2019-07-22');
    $signStr = "POSTcaptcha.tencentcloudapi.com/?";
    foreach ( $captcha as $key => $value ) {
        $signStr = $signStr . $key . "=" . $value . "&";
    }
    $signStr = substr($signStr, 0, -1);
    # See Tencent captcha, too
    $captcha['Signature'] = base64_encode(hash_hmac('sha1', $signStr, "", true));
    ksort($captcha);
    $captcha_result = json_decode(getresponse("https://captcha.tencentcloudapi.com/", http_build_query($captcha), "application/x-www-form-urlencoded"), true);
    if ($captcha_result['Response']['CaptchaCode'] != 1) {
        alert("请重新进行人机验证");
        return;
    }
    $responsee = getresponse("http://yourserver:29343/api/query", $query, "application/json");
    $query_result = json_decode($responsee, true);
    if ($query_result != null) {
        if ($query_result['exist']) {
            alert("呼号已存在");
            return;
        }
    } else {
        alert($responsee);
        return;
    }

    $create_result = json_decode(getresponse("http://youserver:29343/api/create", $query, "application/json"), true);
    if ($create_result != null) {
        if ($create_result['status'] = (int)"200") {
            alert("注册成功");
            return;
        }
    } else {
        alert("注册失败(2)");
        return;
    }
    alert("注册失败(3)");
    return;
?>
