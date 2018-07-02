$(function () {
    gp.operateInit();
});

window.project_minion_list = {}

//操作
var gp = {
    //初始化按钮事件
    operateInit: function () {
        this.GetProject();
        this.SubmitDeploy();
    },

    GetProject: function(){
        $.ajax({
            url: "/saltstack/restart/get_project",
            type: "post",
            contentType: 'application/json',
            //data: JSON.stringify(postData),
            success: function (datas, status) {
                //alert(datas);
                var data = eval(datas);
                //var html = "<option value=''></option>";
                var html_dict = {};
                $.each(data, function (index, item) { 
                    //循环获取数据 
                    var name = data[index];
                    //console.log(name)
                    if (typeof(html_dict[name.product]) == undefined){
                        html_dict[name.product] == ''
                    }
                    //console.log(data)
                    //html_name = "<option>"+name+"</option>";
                    html_name = "<option value='"+name.product+"_"+name.project+"' data-subtext='"+name.server_type+" "+name.envir+"'>"+name.project+"</option>";
                    html_dict[name.product] = html_dict[name.product] + html_name
                    project_minion_list[name.product+'_'+name.project] = name
                }); 
                //$("#project").html(html);
                //$("#project_active").html(html);
                var html_project_active = ['<optgroup label="凤凰">',
                                                html_dict['fenghuang'],
                                            '</optgroup>',
                                            '<optgroup label="勇士">',
                                                html_dict['yongshi'],
                                            '</optgroup>',
                                            '<optgroup label="JAVA">',
                                                html_dict['java'],
                                            '</optgroup>',
                                            '<optgroup label="公共">',
                                                html_dict['pub'],
                                            '</optgroup>',
                                            ].join("")
                var html_restart_project_active = ['<optgroup label="凤凰">',
                                                        html_dict['fenghuang'],
                                                    '</optgroup>',
                                                    '<optgroup label="勇士">',
                                                        html_dict['yongshi'],
                                                    '</optgroup>',
                                                        '<optgroup label="JAVA">',
                                                    html_dict['java'],
                                            '</optgroup>',
                                                    ].join("")
                if (document.getElementById('project_active')){
                    document.getElementById('project_active').innerHTML=html_project_active;
                }
                if (document.getElementById('restart_project_active')){
                    document.getElementById('restart_project_active').innerHTML=html_restart_project_active;
                }
                $('.selectpicker').selectpicker('refresh');
                return false;
            },
            error:function(msg){
                alert("获取项目失败！");
                return false;
            }
        });
    },

    GetProjectServers: function(form, value){
        var projectlist = []
        //var project = document.getElementById("project_active").value;
        if (form === 1){
            var objSelectproject = document.projectreform.project_active; 
        }else if(form === 2){
            var objSelectproject = document.restart_projectreform.restart_project_active; 
        }
        
        for(var i = 0; i < objSelectproject.options.length; i++) { 
            if (objSelectproject.options[i].selected == true) 
            projectlist.push(objSelectproject.options[i].value);
        }
        var html = "";
        //console.log(project_minion_list)
        //console.log(projectlist)
        for (var num in projectlist){
            project = projectlist[num]
            html_tmp = "";
            project_info = project_minion_list[project]
            $.each(project_info['minion_id'], function (index, item) { 
                //循环获取数据 
                var name = item;
                //console.log(name)
                //html_name = "<option>"+name+"</option>";
                //console.log(name.role)
                html_name = "<option value='"+name+"' data-subtext='"+project_info.server_type+" "+project_info.envir+"'>"+name+"</ option>";
                html_tmp = html_tmp + html_name
            }); 
            html_tmp = "<optgroup label='"+ project +"'>" + html_tmp + "</optgroup>";
            html = html + html_tmp;
        }
        document.getElementById(value).innerHTML=html;
        //$('.selectpicker').selectpicker({title:"请选择服务器地址"});
        $('.selectpicker').selectpicker('refresh');
        return false;
    },

    SubmitDeploy: function(){
        $("#btn_submit_deploy").bind('click',function () {
            //var postData=operate.Getform();
            var postData = {
                project:document.getElementById("restart_project_active").value,
                minion_id: []
                //minion_id:document.getElementById("restart_minion_id").value,
            };
            if (postData['project'].length == 0){
                alert("请至少选择一个项目进行推送！")
                return false;
            }

            var objSelect = document.restart_projectreform.restart_minion_id; 

            if (document.getElementById("restart_minion_id").value.length == 0){
                for(var i = 0; i < objSelect.options.length; i++) { 
                    postData['minion_id'].push(objSelect.options[i].value);
                }
            }else {
                for(var i = 0; i < objSelect.options.length; i++) { 
                    if (objSelect.options[i].selected == true)
                    postData['minion_id'].push(objSelect.options[i].value);
                }
            }

            //console.log(postData['minion_id'])
            //return false

            modal_results.innerHTML = "";
            modal_footer.innerHTML = "";
            $("#progress_bar").css("width", "30%");
            modal_head.style.color = 'blue';
            modal_head.innerHTML = "操作进行中，请勿刷新页面......";
            var socket = new WebSocket("ws://" + window.location.host + "/saltstack/command/deploy");
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
            
            socket.onclose = function () {
                setTimeout(function(){$('#runprogress').modal('hide');}, 1000);
            };
            
            socket.onmessage = function (e) {
                //return false;
                data = eval('('+ e.data +')')
                //console.log('message: ' + data);//打印服务端返回的数据
                if (data.step == 'one'){
                    $("#progress_bar").css("width", "50%");
                    $('#OperateRestartresults').append('<p>连接成功......</p>' );
                    modal_head.innerHTML = "命令执行中...";
                }else if (data.step == 'final'){
                    $("#progress_bar").css("width", "100%");
                    $("#progress_bar").css("width", "100%");
                    $('#OperateRestartresults').append('<p>执行完成......</p>' );

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
                    socket.close();
                }
            }; 

            return false;
        });
    },

};