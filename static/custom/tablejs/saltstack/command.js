$(function () {
    operate.operateInit();
});

//全局变量
window.modal_results = document.getElementById("OperateRestartresults");
window.modal_footer = document.getElementById("progressFooter");
window.modal_head = document.getElementById("progress_head");

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.DisplayPanel();
        //this.Getform();
        //this.Submit();
        this.Results();
        this.selectpicker();
        //this.showSelectedValue();
        //this.Exe();
    },

    ChangeArgumentsStyle: function (fun, arg){
        if (document.getElementById(fun).value == 'test.ping'){
            document.getElementById(arg).disabled = true;
        }else {
            document.getElementById(arg).disabled = false;
        }
    },

    DisplayPanel: function (){
        $("#command_panel").bind('click',function () {
            that = document.getElementById("command_form")
            if (that.style.display == "none"){
                that.style.display = "inline";
                document.getElementById('command_panel').innerHTML = "-";
                document.getElementById('command_panel').title = "隐藏";
            }else {
                that.style.display = "none";
                document.getElementById('command_panel').innerHTML = "+";
                document.getElementById('command_panel').title = "展开";
            }
        });

        $("#command2_panel").bind('click',function () {
            that = document.getElementById("command2_form")
            if (that.style.display == "none"){
                that.style.display = "inline";
                document.getElementById('command2_panel').innerHTML = "-";
                document.getElementById('command2_panel').title = "隐藏";
            }else {
                that.style.display = "none";
                document.getElementById('command2_panel').innerHTML = "+";
                document.getElementById('command2_panel').title = "展开";
            }
        });

        $("#restart_panel").bind('click',function () {
            that = document.getElementById("restart_form")
            if (that.style.display == "none"){
                that.style.display = "inline";
                document.getElementById('restart_panel').innerHTML = "-";
                document.getElementById('restart_panel').title = "隐藏";
            }else {
                that.style.display = "none";
                document.getElementById('restart_panel').innerHTML = "+";
                document.getElementById('restart_panel').title = "展开";
            }
        });
    },
    
    Reset: function (){
        $("#btn_reset").bind('click',function () {
            document.getElementById("commandform").reset();
            return false;
        });
    },

    Results: function(){
        $("#show_results").modal({
            keyboard: true
        })
    },

    selectpicker: function() {
        $('.selectpicker').selectpicker({
            style: 'btn-default',
            //width: "auto",
            size: 13,
            showSubtext:true,
        });
    },

    showSelectedValue: function (){
        var selectedValue = []; 
        var objSelect = document.projectreform.minions_id; 
        for(var i = 0; i < objSelect.options.length; i++) { 
            if (objSelect.options[i].selected == true) 
            selectedValue.push(objSelect.options[i].value);
        }
        return selectedValue;
    },

    Getcommandform: function getEntity(commandform) {
        var formdata = {
            expr_form:document.getElementById("expr_form").value,
            target:document.getElementById("target").value.replace(/[\s*]/g, ''),
            function:document.getElementById("function").value,
            arguments:document.getElementById("arguments").value,
        };
        var target = formdata['target'];
        if (formdata['expr_form'] == 'list'){
            formdata['target'] = target.split(',');
        }
        return formdata;
    },

    Getcommandform2: function getEntity(projectreform) {
        var formdata = {
            expr_form:"",
            target:[],
            function:document.getElementById("function2").value,
            arguments:document.getElementById("arguments2").value,
        };
        return formdata;
    },

    GetExeUser: function (radio_name){
        var obj = document.getElementsByName(radio_name);
        for(i=0;i<obj.length;i++) { 
            if(obj[i].checked) { 
                return obj[i].value; 
            } 
        }   
        return "undefined";
    },

    Submit: function(submit){
        if (submit == 'btn_submit_command') {
            //console.log("btn_submit_command")
            var postData=operate.Getcommandform();
            postData['exe_user'] = operate.GetExeUser('commandform_user');
            //console.log(postData['exe_user']);
            if (postData['target'] == ''){
                alert("Minion ID 不能为空！");
                return false;
            }
            if (postData['function'] != 'test.ping' &  postData['arguments'] == ''){
                alert("执行参数 不能为空！");
                return false;
            }
        }else if (submit == 'btn_submit_command2') {
            //console.log("btn_submit_command2")
            var postData=operate.Getcommandform2();
            postData['exe_user'] = operate.GetExeUser('commandform2_user');
            //console.log(postData['exe_user']);
            postData['target'] = operate.showSelectedValue();
            if (document.getElementById("project_active").value.length == 0){
                alert("请至少选择一个服务！")
                return false;
            }
            if (postData['target'].length == 0){
                alert("请至少选择一个服务器！")
                return false;
            }
            if (postData['function'] != 'test.ping' &  postData['arguments'] == ''){
                alert("执行参数 不能为空！");
                return false;
            }
            postData['expr_form'] = 'list';
        }else {
            alert("获取执行参数失败，请检查服务！");
            return false;
        }
        //alert("获取到的表单数据为:"+JSON.stringify(postData));
        $('#runprogress').modal('show');
        modal_results.innerHTML = "";
        modal_footer.innerHTML = "";
        $("#progress_bar").css("width", "30%");
        modal_head.innerHTML = "操作进行中，请勿刷新页面......";
        $('#OperateRestartresults').append('<p>连接中......</p>' );

        public.socketConn("/saltstack/command/execute", [])

        window.s.onopen = function (e) {
            window.s.send(JSON.stringify(postData));
        };
        
        window.s.onerror = function (){
            modal_head.innerHTML = "与服务器连接失败...";
            $('#OperateRestartresults').append('<p>连接失败......</p>' );
            setTimeout(function(){$('#runprogress').modal('hide');}, 1000);
        };

        window.s.onclose = function () {
            setTimeout(function(){$('#runprogress').modal('hide');}, 1000);
        };

        window.s.onmessage = function (e) {
            if (e.data == 'userNone'){
                toastr.error('未获取用户名，请重新登陆！', '错误');
                public.disableButtons(window.buttons, false);
                window.s.close();
                return false;
            }

            //return false;
            data = eval('('+ e.data +')')
            //console.log('message: ' + data['target']);//打印服务端返回的数据
            if (data.step == 'one'){
                $("#progress_bar").css("width", "50%");
                $('#OperateRestartresults').append('<p>连接成功......</p>' );
                modal_head.innerHTML = "命令执行中...";
            }else if (data.step == 'final'){
                modal_head.innerHTML = "命令执行完成...";
                $("#progress_bar").css("width", "100%");
                //$('#OperateRestartresults').append('<pre>' + data['result'] + '</pre>');
                $('#OperateRestartresults').append('<p>执行完成......</p>' );
                //console.log('websocket已关闭');
                setTimeout(function(){$('#runprogress').modal('hide');}, 1000);
                var html = "";
                var button = ""
                var button_html = "";
                for (var tgt in data.results){
                    //alert(tgt+data[tgt])
                    if (data['results'][tgt] == 'not return'){
                        button = [                        
                        '<div class="btn-group" style="width:18%; margin-bottom:5px;">',
                            '<button data-toggle="modal" data-target="#'+tgt+'" id="#'+tgt+'" type="button" class="btn btn-danger" style="width:100%;">'+tgt+'',
                            '</button>',
                        '</div>',].join("");
                    }else {
                        button = [                        
                        '<div class="btn-group" style="width:18%; margin-bottom:5px;">',
                            '<button data-toggle="modal" data-target="#'+tgt+'" id="#'+tgt+'" type="button" class="btn btn-info" style="width:100%;">'+tgt+'',
                            '</button>',
                        '</div>',].join("");
                    }

                    button_html = button_html + button + [
                        '<div class="modal fade" id="'+tgt+'" tabindex="-1" role="dialog" dialaria-labelledby="'+tgt+'" aria-hidden="true">',
                            '<div class="modal-dialog" style="width:1000px;">',
                                '<div class="modal-content" >',
                                    '<div class="modal-body">',
                                        '<xmp>'+data['results'][tgt]+'</xmp>',
                                    '</div>',
                                '</div>',
                            '</div>',
                        '</div>',].join("");
                    //$("#" + tgt).modal({keyboard: true});
                    //button = button + "<button class='btn btn-primary' data-toggle='modal' data-target='#show_results'>"+tgt+"</button>"
                    html = html + "<p><strong>"+tgt+"</strong></p><pre class='pre-scrollable'><xmp>"+data['results'][tgt]+"</xmp></pre>";
                }
                button_html = "<div class='btn-toolbar' role='toolbar'>" + button_html +"</div>" + "<hr>"
                $("#commandresults").html(button_html + html);
                for (var tgt in data.results){
                    $("#"+tgt).click(function(){
                        $(this).modal({keyboard: true});
                    });
                }
                window.s.close();
                return false;
            }
        }; 
        return false;
    },

};