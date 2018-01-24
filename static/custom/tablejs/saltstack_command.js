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
        this.SubmitRestart();
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

    GetRestartProjectServers: function(){
        var projectlist = []
        //var project = document.getElementById("project_active").value;
        var objSelectproject = document.restart_projectreform.restart_project_active; 
        for(var i = 0; i < objSelectproject.options.length; i++) { 
            if (objSelectproject.options[i].selected == true) 
            projectlist.push(objSelectproject.options[i].value);
        }
        //console.log(projectlist);
        var postData = {};
        postData['project'] = projectlist;
        $.ajax({
            url: "/saltstack/restart/get_project_servers",
            type: "post",
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(postData),
            success: function (datas, status) {
                //alert(datas);
                var data = eval(datas);
                //var html = "<option value=''></option>";
                var html = "";
                for (var project in data){
                    html_tmp = "";
                    $.each(data[project], function (index, item) { 
                        //循环获取数据 
                        var name = data[project][index];
                        //html_name = "<option>"+name+"</option>";
                        //console.log(name.role)
                        if (name.status === 'inactive') {
                            html_name = "<option value='"+name.minion_id+"' data-subtext='"+name.info+" "+name.role+"' disabled>"+name. minion_id+"</option>";
                        }else {
                            html_name = "<option value='"+name.minion_id+"' data-subtext='"+name.info+" "+name.role+"'>"+name.minion_id+"</ option>";
                        }
                        html_tmp = html_tmp + html_name
                    }); 
                    html_tmp = "<optgroup label='"+ project +"'>" + html_tmp + "</optgroup>";
                    html = html + html_tmp;
                }
                document.getElementById('restart_minion_id').innerHTML=html;
                //$('.selectpicker').selectpicker({title:"请选择服务器地址"});
                $('.selectpicker').selectpicker('refresh');
                return false;
            },
            error:function(msg){
                alert("获取项目服务器地址失败！");
                return false;
            }
        });
    },

    GetProjectServers: function(){
        var projectlist = []
        //var project = document.getElementById("project_active").value;
        var objSelectproject = document.projectreform.project_active; 
        for(var i = 0; i < objSelectproject.options.length; i++) { 
            if (objSelectproject.options[i].selected == true) 
            projectlist.push(objSelectproject.options[i].value);
        }
        //console.log(projectlist);
        var postData = {};
        postData['project'] = projectlist;
        $.ajax({
            url: "/saltstack/restart/get_project_servers",
            type: "post",
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(postData),
            success: function (datas, status) {
                //alert(datas);
                var data = eval(datas);
                //var html = "<option value=''></option>";
                var html = "";
                for (var project in data){
                    html_tmp = "";
                    $.each(data[project], function (index, item) { 
                        //循环获取数据 
                        var name = data[project][index];
                        //html_name = "<option>"+name+"</option>";
                        //console.log(name.role)
                        html_name = "<option value='"+name.minion_id+"' data-subtext='"+name.info+" "+name.role+"'>"+name.minion_id+"</ option>";
                        html_tmp = html_tmp + html_name
                    }); 
                    html_tmp = "<optgroup label='"+ project +"'>" + html_tmp + "</optgroup>";
                    html = html + html_tmp;
                }
                document.getElementById('minions_id').innerHTML=html;
                //$('.selectpicker').selectpicker({title:"请选择服务器地址"});
                $('.selectpicker').selectpicker('refresh');
                return false;
            },
            error:function(msg){
                alert("获取项目服务器地址失败！");
                return false;
            }
        });
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

    SubmitRestart: function(){
        $("#btn_submit_restart").bind('click',function () {
            //var postData=operate.Getform();
            var postData = {
                project:document.getElementById("restart_project_active").value,
                minion_id:document.getElementById("restart_minion_id").value,
            };
            if (postData['project'].length == 0){
                alert("请至少选择一个服务进行重启！")
                return false;
            }
            if (postData['minion_id'].length == 0){
                alert("请至少选择一个服务器进行重启！")
                return false;
            }
            //alert("获取到的表单数据为:"+JSON.stringify(postData));
            modal_results.innerHTML = "";
            modal_footer.innerHTML = "";
            $("#progress_bar").css("width", "30%");
            modal_head.style.color = 'blue';
            modal_head.innerHTML = "操作进行中，请勿刷新页面......";
            var socket = new WebSocket("ws://" + window.location.host + "/saltstack/command/restart");
            socket.onopen = function () {
                //console.log('WebSocket open');//成功连接上Websocket
                //socket.send($('#message').val());//发送数据到服务端
                socket.send(JSON.stringify(postData))
            };
            $('#runprogress').modal('show');
            socket.onerror = function (){
                modal_head.innerHTML = "与服务器连接失败...";
                $('#OperateRestartresults').append('<p>连接失败......</p>' );
                setTimeout(function(){$('#runprogress').modal('hide');}, 1000);
            };
            socket.onmessage = function (e) {
                //return false;
                data = eval('('+ e.data +')')
                //console.log('message: ' + data);//打印服务端返回的数据
                if (data.step == 'one'){
                    $("#progress_bar").css("width", "50%");
                    $('#OperateRestartresults').append('<p>' + data['project'] + ':&thinsp;<strong>' + data['minion_id'] + '</strong></p>' );
                }else if (data.step == 'final'){
                    $("#progress_bar").css("width", "100%");
                    if (data['result'] == 'not return'){
                        modal_head.innerHTML = "服务重启失败！";
                        modal_head.style.color = 'red';

                    }else {
                        modal_head.innerHTML = "服务重启完成...";
                    }
                    $('#OperateRestartresults').append('<pre>' + data['result'] + '</pre>');
                    //console.log('websocket已关闭');
                    modal_footer.innerHTML = '<button id="close_modal" type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span>关闭</button>'
                }
            }; 

            return false;
        });
    },

    Getcommandform: function getEntity(commandform) {
        var formdata = {
            expr_form:document.getElementById("expr_form").value,
            target:document.getElementById("target").value,
            function:document.getElementById("function").value,
            arguments:document.getElementById("arguments").value,
        };
        var target = document.getElementById("target").value;
        if (formdata['expr_form'] == 'list'){
            formdata['target'] = target.replace(/[\s*]/g, '').split(',');
        }
        return formdata;
    },

    Getcommandform2: function getEntity(projectreform) {
        var formdata = {
            expr_form,
            target,
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
        modal_results.innerHTML = "";
        modal_footer.innerHTML = "";
        $("#progress_bar").css("width", "30%");
        modal_head.innerHTML = "操作进行中，请勿刷新页面......";
        $('#OperateRestartresults').append('<p>连接中......</p>' );
        var socket = new WebSocket("ws://" + window.location.host + "/saltstack/command/execute");

        socket.onerror = function (){
            modal_head.innerHTML = "与服务器连接失败...";
            $('#OperateRestartresults').append('<p>连接失败......</p>' );
            setTimeout(function(){$('#runprogress').modal('hide');}, 1000);
        };

        socket.onopen = function () {
            //console.log('WebSocket open');//成功连接上Websocket
            //socket.send($('#message').val());//发送数据到服务端
            socket.send(JSON.stringify(postData))
        };

        $('#runprogress').modal('show');
        socket.onmessage = function (e) {
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
                return false;
            }
        }; 
        return false;
    },

    Exe: function(){
        $("#btn_exe").bind('click',function () {
            //var postData=operate.Getform();
            var postData = {
                expr_form,
                target,
                function:document.getElementById("function2").value,
                arguments:document.getElementById("arguments2").value,
            };
            //console.log(postData)
            postData['target'] = operate.showSelectedValue();
            if (document.getElementById("project_active").value.length == 0){
                alert("请至少选择一个服务！")
                return false;
            }
            if (postData['target'].length == 0){
                alert("请至少选择一个服务器！")
                return false;
            }
            postData['expr_form'] = 'list';
            console.log(postData)
            //alert("获取到的表单数据为:"+JSON.stringify(postData));
            $.ajax({
                url: "/saltstack/command/execute",
                type: "post",
                contentType: 'application/json',
                dataType: "json",
                data: JSON.stringify(postData),
                success: function (data, status) {
                    var html = "";
                    var button = "";
                    for (var tgt in data){
                        button = button + [
                            '<div class="btn-group">',
                                '<button data-toggle="modal" data-target="#'+tgt+'" id="#'+tgt+'" type="button" class="btn btn-primary">'+tgt+'',
                                '</button>',
                            '</div>',
                            '<div class="modal fade" id="'+tgt+'" tabindex="-1" role="dialog" dialaria-labelledby="'+tgt+'" aria-hidden="true">',
                                '<div class="modal-dialog" style="width:1000px;">',
                                    '<div class="modal-content" >',
                                        '<div class="modal-body">',
                                            '<xmp>'+data[tgt]+'</xmp>',
                                        '</div>',
                                    '</div>',
                                '</div>',
                            '</div>',].join("");
                        html = html + "<p><strong>"+tgt+"</strong></p><pre class='pre-scrollable'><xmp>"+data[tgt]+"</xmp></pre>";
                    }
                    button = "<div class='btn-toolbar' role='toolbar'>" + button +"</div>" + "<hr>"
                    $("#commandresults").html(button+html);
                    for (var tgt in data){
                        $("#"+tgt).click(function(){
                            $(this).modal({keyboard: true});
                        });
                    }
                    return false;
                },
                error:function(msg){
                    alert("参数输入错误！");
                    return false;
                }
            });
            return false;
        });
    },

};