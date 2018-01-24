$(function () {
    tableInit.Init();
    operate.operateInit();
});

//全局变量
window.run = true;
window.myViewModel = {}
window.postUpgradeData = {
        svn_id:'',
        tag:'',
        project:'',
        ip_addr:[],
        act:'',
        step:0,
        envir:'',
        restart:'',
};

window.postEditConfig = {}
window.uat_ip_addr_list = new Array();
window.online_ip_addr_list = new Array();
window.html_uat = "";
window.html_online = "";
window.modal_results = document.getElementById("upgrade_results");
window.modal_head_content = document.getElementById("upgrade_modal_head_content");
window.modal_head_close = document.getElementById("upgrade_modal_head_close");
window.upgrade_progress_head = document.getElementById("upgrade_progress_head");
window.upgrade_progress_body = document.getElementById("upgrade_progress_body");
window.Displayadd = document.getElementById('btn_save_new_config');
window.Displaydelete = document.getElementById('btn_confirm_delete_config');
window.config_name = document.getElementById('config_name')
window.config_content = document.getElementById('config_content')
window.radio_config_list = document.getElementById('radio_config_list')
window.edit_config_head = document.getElementById("edit_config_head")

var tableInit = {
    Init: function () {
        this.operateFormatter;
        this.cur_statusFormatter;
        this.dbclick();
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/upgrade/query_svn',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset, 'act':'query_not_deleted' };
            },//传递参数（*）
            toolbarAlign: "left",
            columns: [
                //{ 
                //    checkbox: true 
                //},
                {
                    field: 'id',
                    title: 'id',
                    sortable: true,
                    width:'1%',
                    //align: 'center'
                },{
                    field: 'id_time',
                    title: '版本时间',
                    sortable: true,
                    //align: 'center',
                    width:'9%',
                },{
                    field: 'svn_id',
                    title: '版本',
                    sortable: true,
                    width:'6%',
                    //align: 'center'
                },{
                    field: 'tag',
                    title: '标签',
                    sortable: true,
                    width:'5%',
                    //align: 'center'
                },{
                    field: 'project',
                    title: '项目名',
                    sortable: true,
                    width:'18%',
                    //align: 'center'
                },{
                    field: 'envir_uat',
                    title: '测试环境',
                    sortable: true,
                    width:'6%',
                    //align: 'center',
                    //events: this.cur_statusEvents,
                    formatter: this.cur_statusFormatter
                },{
                    field: 'envir_online',
                    title: '运营环境',
                    sortable: true,
                    width:'6%',
                    //align: 'center',
                    //events: this.cur_statusEvents,
                    formatter: this.cur_statusFormatter
                },{
                    field: 'info',
                    title: '备注',
                    sortable: true,
                    //align: 'center',
                    width:'9%',
                },{
                    field: 'operations',
                    title: '操作项',
                    //align: 'center',
                    width:'9%',
                    events: operateEvents,
                    formatter: this.operateFormatter,
                    //width:300,
                },
            ]

        });
        ko.applyBindings(this.myViewModel, document.getElementById("upgrade_op_table"));
    },

    dbclick: function (){
        $('#upgrade_op_table').on('all.bs.table', function (e, name, args) {
            //console.log('Event:', name, ', data:', args);
        }).on('dbl-click-cell.bs.table', function (e, field, value, row, $element) {
            if (row.deleted == 1){
                alert(row.svn_id+': 是删除的状态，请先恢复！')
                return false;
            }

            $('#upgrade_modal').modal('show');
            upgrade_parms = {
                id_time:row.id_time,
                svn_id:row.svn_id,
                tag:row.tag,
                envir_uat,
                envir_online,
                project:row.project,
            }

            if (row.envir_online == 'done'){
                upgrade_parms.envir_online = ko.observable('已升级');
            }else if (row.envir_online == 'undone'){
                upgrade_parms.envir_online = ko.observable('未升级');
            }else if (row.envir_online == 'rollback'){
                upgrade_parms.envir_online = ko.observable('已回退');
            }
            if (row.envir_uat == 'done'){
                upgrade_parms.envir_uat = ko.observable('已升级');
            }else if (row.envir_uat == 'undone'){
                upgrade_parms.envir_uat = ko.observable('未升级');
            }else if (row.envir_uat == 'rollback'){
                upgrade_parms.envir_uat = ko.observable('已回退');
            }

            //初始化升级按钮
            operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip','upgrade_interrupt'], true);

            //初始化页面参数
            var obj_envir = document.getElementsByName('upgrade_envir');
            var obj_restart = document.getElementsByName('upgrade_restart');
            for(i=0;i<obj_envir.length;i++) { 
                if(obj_envir[i].checked) { 
                    obj_envir[i].checked = false; 
                } 
            }
            for(i=0;i<obj_restart.length;i++) { 
                if(obj_restart[i].checked) { 
                    obj_restart[i].checked = false; 
                } 
            }
            document.getElementById('upgrade_ip').innerHTML = "";
            $('.selectpicker').selectpicker('refresh');
            operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
            operate.disableButtons(['upgrade_envir_uat', 'upgrade_envir_online'], true);
            upgrade_progress_body.hidden = true;
            upgrade_progress_head.innerHTML= "";
            modal_head_content.innerHTML = "请选择升级参数";
            modal_head_close.innerHTML = "&times;";
            modal_results.innerHTML = "";
            $('#upgrade_results').append('<p>正在获取主机地址，请稍后...</p>');
            //modal_results.append('<p>正在获取主机地址，请稍后...</p>');
            operate.DisSelectedIp();
            ko.cleanNode(document.getElementById("upgrade_modal_body"));
            ko.applyBindings(upgrade_parms, document.getElementById("upgrade_modal_body"));
            operate.GetProjectServers(row.project);
        });
    },

    operateFormatter: function (value,row,index){
        content_m = [
            '<a class="edit_config_choose_envir text-info" href="javascript:void(0)" title="编辑配置文件" style="margin-right: 10px;">',
                '编辑配置',
            '</a>',
        ].join('');

        content_m = content_m + [
            '<a class="modify_upgrade_status text-info" href="javascript:void(0)" title="修改升级状态" style="margin-right: 10px;">',
                '修改状态',
            '</a>',
        ].join('');

        if (row.deleted == 0){
            content_n = [
                '<a class="delete text-info" href="javascript:void(0)" title="删除">',
                    '删除',
                '</a>',
            ].join('');
        }else if (row.deleted == 1){
            content_n = [
                '<a class="recover text-info" href="javascript:void(0)" title="恢复">',
                    '恢复',
                '</a>',
            ].join('');
            return content_n;
        }else {
            content_n = "";
        }
        return content_m+content_n;
    },

    cur_statusFormatter: function (value,row,index) {
        var status = value;
        var content = "";
        if (status == 'undone'){
            content = '<span style="background-color: #FF0000">未升级</span>';
            return content;
        }else if(status == 'done'){
            content = '<span style="background-color: #32CD32">已升级</span>';
            return content;
        }else if(status == 'rollback'){
            content = '<span style="background-color: #FFD700">已回退</span>';
            return content;
        }else {
            return "未定义";
        }

    },
};

window.operateEvents = {
    'click .upgrade': function (e, value, row, index) {
        var tmp = document.getElementById("OperateUpgraderesults");
        var tmpfooter = document.getElementById("progressFooter");
        tmp.innerHTML = "";
        tmpfooter.innerHTML = "";
        var socket = new WebSocket("ws://" + window.location.host + "/upgrade/operate_upgrade");
        socket.onopen = function () {
            console.log('WebSocket open');//成功连接上Websocket
            //socket.send($('#message').val());//发送数据到服务端
        };
        socket.onerror = function (){
            alert('连接服务器失败，请重试！');
            return false;
        };
        socket.onmessage = function (e) {
            data = eval('('+ e.data +')')
            //console.log('message: ' + data.message);//打印服务端返回的数据
            $('#OperateUpgraderesults').append('<p>' + data.message + '</p>');
            var a = document.getElementById("progress_head");
            a.innerHTML = "操作进行中，请勿刷新页面......";
            $("#progress_bar").css("width", "30%");
            p = 0;  
            stop = 0; 
            $('#runprogress').modal('show');  
            run(data.count); 
            if (data.count == 5){
                //$('#runprogress').modal('hide'); 
                console.log('websocket已关闭');
                tmpfooter.innerHTML = '<button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span>关闭</button>'
            }
        }; 
        return false;
    },

    'click .edit_config_choose_envir': function (e, value, row, index) {
        content = [
            '<form id="envir_form" class="form-inline" role="form" style="text-align: center; margin-bottom: 50px;">',
                '<div class="col-xs-12 col-sm-12 col-md-12">',
                    '项目：<span id="choose_envir_project" value='+row.project+' style="font-weight:bold;">'+row.project+'</span>',
                '</div>',
                '<div class="col-xs-12 col-sm-12 col-md-12">',
                    'svn_id：<span id="choose_envir_svn_id" value='+row.svn_id+' style="font-weight:bold;">'+row.svn_id+'</span>',
                '</div>',
            '</form>',
            '<form id="envir_form" class="form-inline" role="form" style="text-align: center;">',
                '<button name="edit_config" id="edit_config_uat" onclick="operate.editConfig(this)" type="button" class="btn btn-default" style="margin-right: 50px;" value="UAT">测试环境</button>',
                '<button name="edit_config" id="edit_config_online" onclick="operate.editConfig(this)" type="button" class="btn btn-default" value="ONLINE">运营环境</button>',
            '</form>',
        ].join('')

        document.getElementById("choose_envir_body").innerHTML = content;

        $('#choose_envir_modal').modal('show');
        return false;
    },

    'click .modify_upgrade_status': function (e, value, row, index) {
        operate.disableButtons(['btn_close_update_upgrade_status_modal', 'btn_update_upgrade_status_submit'], false);

        document.getElementById('uat_upgrade_done').checked = false;
        document.getElementById('uat_upgrade_rollback').checked = false;
        document.getElementById('online_upgrade_done').checked = false;
        document.getElementById('online_upgrade_rollback').checked = false;
        document.getElementById('upgrade_status_id').value = row.id;

        if (row.envir_uat == 'done'){
            document.getElementById('uat_upgrade_done').checked = true;
        }else if (row.envir_uat == 'rollback'){
            document.getElementById('uat_upgrade_rollback').checked = true;
        }

        if (row.envir_online == 'done'){
            document.getElementById('online_upgrade_done').checked = true;
        }else if (row.envir_online == 'rollback'){
            document.getElementById('online_upgrade_rollback').checked = true;
        }

        $('#update_upgrade_status_modal').modal('show');

        return false;
    },

    'click .delete': function (e, value, row, index) {
        var postData = {};
        postData['deleted'] = 1
        postData['id'] = row.id
        postData['svn_id'] = row.svn_id
        postData['act'] = 'update_deleted'

        $.ajax({
            url: "/upgrade/update_svn",
            type: "post",
            data: JSON.stringify(postData),
            success: function (datas, status) {
                $('#upgrade_op_table').bootstrapTable('remove', {
                    field: 'id',
                    values: [row.id]
                });
                if (datas == 'failure'){
                    alert("failure");
                }else {
                    toastr.warning('删除成功！', row.project+": "+row.svn_id)
                }
            },
            error:function(XMLHttpRequest, textStatus, errorThrown){
                if (XMLHttpRequest.status == 0){
                    toastr.error('后端服务不响应', '错误')
                }else {
                    toastr.error(XMLHttpRequest.responseText, XMLHttpRequest.status)
                }
            }
        });
        return false;
    },
    'click .recover': function (e, value, row, index) {
        var postData = {};
        postData['deleted'] = 0
        postData['id'] = row.id
        postData['svn_id'] = row.svn_id
        postData['act'] = 'update_deleted'

        $.ajax({
            url: "/upgrade/update_svn",
            type: "post",
            data: JSON.stringify(postData),
            success: function (datas, status) {
                if (datas == 'failure'){
                    alert("failure");
                }else {
                    toastr.warning('恢复成功！', row.project+": "+row.svn_id)
                    $('#upgrade_op_table').bootstrapTable('refresh');
                }
            },
            error:function(XMLHttpRequest, textStatus, errorThrown){
                if (XMLHttpRequest.status == 0){
                    toastr.error('后端服务不响应', '错误')
                }else {
                    toastr.error(XMLHttpRequest.responseText, XMLHttpRequest.status)
                }
            }
        });
        
        return false;
    }
};  

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.operateUpgradeSelect();
        this.upgradeButtons();
        this.Buttons();
        //this.updateConfig();
        //this.editConfig();
        //this.setHandleUser();
        //this.selectpicker();
    },

    getpostData: function (act) {
        var obj_envir = document.getElementsByName('upgrade_envir');
        var obj_restart = document.getElementsByName('upgrade_restart');
        for(i=0;i<obj_envir.length;i++) { 
            if(obj_envir[i].checked) { 
                postUpgradeData.envir = obj_envir[i].value; 
            } 
        }
        postUpgradeData.restart = '';
        for(i=0;i<obj_restart.length;i++) { 
            if(obj_restart[i].checked) { 
                postUpgradeData.restart = obj_restart[i].value; 
            } 
        }
        postUpgradeData.svn_id = upgrade_parms.svn_id;
        postUpgradeData.tag = upgrade_parms.tag;
        postUpgradeData.project = upgrade_parms.project;
        postUpgradeData.act = act;
        var selectedValue = []; 
        var objSelect = document.getElementById('upgrade_ip');
        for(var i = 0; i < objSelect.options.length; i++) { 
            if (objSelect.options[i].selected == true) 
            selectedValue.push(objSelect.options[i].value);
        }
        if (selectedValue.length == 0 && postUpgradeData.envir == 'UAT'){
            postUpgradeData.ip_addr = uat_ip_addr_list;
        }else if (selectedValue.length == 0 && postUpgradeData.envir == 'ONLINE') {
            postUpgradeData.ip_addr = online_ip_addr_list;
        }else {
            postUpgradeData.ip_addr = selectedValue;
        }
        return postUpgradeData;
    },

    disableButtons: function (buttonList, fun) {
        for (var i = 0; i < buttonList.length; i++){
            if (fun){
                document.getElementById(buttonList[i]).disabled = true;
            }else {
                document.getElementById(buttonList[i]).disabled = false;
            }
        }
    },

    upgradeButtons: function(){
        $('#upgrade_deploy').on("click", function () {
            var args = {};

            args['act'] = 'deploy';
            args['content1'] = '升级中';
            args['content2'] = '升级完成';
            //console.log(args.act)
            operate.socketConn(args);

        });

        $('#upgrade_diff').on("click", function () {
            var args = {};

            args['act'] = 'diff';
            args['content1'] = '对比中';
            args['content2'] = '对比完成';
            //console.log(args.act)

            operate.socketConn(args);

        });

        $('#upgrade_rollback').on("click", function () {
            var args = {};

            args['act'] = 'rollback';
            args['content1'] = '回退中';
            args['content2'] = '回退完成';
            //console.log(args.act)
            operate.socketConn(args);
        });



        $('#upgrade_interrupt').on("click", function () {
            //alert('终止')
            //cur_status.innerHTML = '中断';
            modal_head_content.innerHTML = "中断";
            run = false;
            operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
            operate.disableButtons(['upgrade_interrupt'], true);
        });
    },

    GetCheckedEnvir: function (){
        var obj_envir = document.getElementsByName('upgrade_envir');
        for(i=0;i<obj_envir.length;i++) { 
            if(obj_envir[i].checked) { 
                return obj_envir[i].value;
            } 
        }
        return false;
    },

    socketConn: function (args){
        //获取需要post的所有数据
        var postData = operate.getpostData(args.act);
        if (postData.ip_addr.length == 0){
            alert('所选IP为空，请检查！');
            return false;
        }
        if ((postData.act == 'deploy' || postData.act == 'rollback') && postData.restart == ''){
            alert('请选择是否重启服务！');
            return false;
        }

        postData.envir = operate.GetCheckedEnvir()
        postData.step = 0;
        run = true;

        //更改页面展示的状态
        modal_head_content.innerHTML = args.content1+"，请勿刷新页面......";
        //cur_status = document.getElementById('cur_status');
        //cur_status.innerHTML = args.content1;
        modal_head_close.innerHTML = "";
        upgrade_progress_body.hidden = false;
        $("#upgrade_progress_bar").css("width", "0%");

        //按钮禁用
        operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], true);

        //插入结果
        upgrade_progress_head.innerHTML="总共：<strong>"+postData.ip_addr.length+"</strong>台    "+"成功：<strong>"+postData.step+"</strong>台";
        
        if (postData.step == postData.ip_addr.length - 1){
            operate.disableButtons(['upgrade_interrupt'], true);
        }else {
            operate.disableButtons(['upgrade_interrupt'], false);
        }
        //建立socket连接
        var socket = new WebSocket("ws://" + window.location.host + "/upgrade/op_upgrade/deploy");
        socket.onopen = function () {
            //第一次发送数据
            socket.send(JSON.stringify(postData));
            $('#upgrade_results').append('<p>执行动作:&thinsp;<strong>'+ postData.act +'</strong></p>');
            $('#upgrade_results').append('<p>返回结果:</p>');
        };
        socket.onerror = function (){
            modal_head_content.innerHTML = '与服务器连接失败...';
            upgrade_progress_head.innerHTML = '与服务器连接失败...';
            modal_head_close.innerHTML = "&times;";
            operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
            operate.disableButtons(['upgrade_interrupt'], true);
        };
        socket.onmessage = function (e) {
            //return false;
            data = eval('('+ e.data +')')

            if (data.op_status == -1){
                modal_head_close.innerHTML = "&times;"
                operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
                operate.disableButtons(['upgrade_interrupt'], true);
                $('#upgrade_results').append('<p>传入参数错误，请检查服务！</p>');
                return false;
            }else if (data.op_status == 0){
                modal_head_close.innerHTML = "&times;"
                operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
                operate.disableButtons(['upgrade_interrupt'], true);
                $('#upgrade_results').append('<p>错误：'+ data.result +'</p>');
                return false;
            }

            if (data.act == 'getfile'){
                if (data.result == 'ReadTimeout' || data.result == 'UnknownError' || data.result == 'ConnectionError' || data.result == 'InsertRecordError'){
                    modal_head_close.innerHTML = "&times;"
                    $('#upgrade_results').append('<p>获取svn版本文件: '+ data.result +'</p>');
                    operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
                    return false;
                }else {
                    $('#upgrade_results').append('<p>获取svn版本文件: 成功</p>');
                    postData.step = postData.step + 1;
                    socket.send(JSON.stringify(postData));
                    return false;
                }
            }

            var button = ""
            var button_html = "";
            //console.log('ip_addr: ' + data.ip_addr);//打印服务端返回的数据
            var timestamp = operate.getNowFormatDate('timestamp')
            var width = 100*(data.step+1)/postData.ip_addr.length + "%"
            postData.step = postData.step + 1;
            if (postData.step == postData.ip_addr.length - 1){
                operate.disableButtons(['upgrade_interrupt'], true);
            }
            $("#upgrade_progress_bar").css("width", width);
            $('#upgrade_results').append('<p><strong>'+data.ip_addr+'</strong></p>');
            //console.log(typeof(data.result))
            $('#upgrade_results').append('<pre class="pre-scrollable"><xmp>'+data.info+'</xmp></pre>',)
            upgrade_progress_head.innerHTML="总共：<strong>"+postData.ip_addr.length+"</strong>台    "+"成功：<strong>"+(postData.step)+"</strong>台";
            //console.log(data.step+" : "+postData.ip_addr.length)
            if (run){
                if (data.step < postData.ip_addr.length - 1){
                    //console.log(postData);
                    socket.send(JSON.stringify(postData));
                }else {
                    //cur_status.innerHTML = args.content2;
                    modal_head_close.innerHTML = "&times;"
                    modal_head_content.innerHTML = args.content2;
                    operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
                    operate.disableButtons(['upgrade_interrupt'], true);
                    //socket.close();
                }
            }else {
                modal_head_close.innerHTML = "&times;"
                operate.disableButtons(['upgrade_deploy', 'upgrade_diff', 'upgrade_rollback', 'upgrade_ip'], false);
                operate.disableButtons(['upgrade_interrupt'], true);
                //socket.close();
            }
            
        }; 
        return false;
    },

    getNowFormatDate: function (type) {
        var seperator1 = "-";
        var seperator2 = ":";
        var dtCur = new Date();
        var yearCur = dtCur.getFullYear();
        var monCur = dtCur.getMonth() + 1;
        var dayCur = dtCur.getDate();
        var hCur = dtCur.getHours();
        var mCur = dtCur.getMinutes();
        var sCur = dtCur.getSeconds();
        var currentdate = yearCur + seperator1 + (monCur < 10 ? "0" + monCur : monCur) + seperator1 + (dayCur < 10 ? "0" + dayCur : dayCur) + " " + (hCur < 10 ? "0" + hCur : hCur) + seperator2 + (mCur < 10 ? "0" + mCur : mCur) + seperator2 + (sCur < 10 ? "0" + sCur : sCur);
        var timestamp = yearCur + (monCur < 10 ? "0" + monCur : monCur) + (dayCur < 10 ? "0" + dayCur : dayCur) + (hCur < 10 ? "0" + hCur : hCur) + (mCur < 10 ? "0" + mCur : mCur) + (sCur < 10 ? "0" + sCur : sCur);
        if (type == 'normal'){
            return currentdate;
        }else if (type = 'timestamp'){
            return timestamp;
        }   
    },

    DisSelectedIp: function (){
        var obj = operate.GetCheckedEnvir()
        var selectedValue = []; 
        var objSelect = document.getElementById('upgrade_ip'); 
        for(var i = 0; i < objSelect.options.length; i++) { 
            if (objSelect.options[i].selected == true) 
            selectedValue.push(" "+objSelect.options[i].value);
        }
        var selected_ip = selectedValue;
        if (obj == 'UAT'){
            if (selected_ip.length == 0 && uat_ip_addr_list.length != 0){
                selected_ip = 'All';
            }else if (selected_ip.length == 0 && uat_ip_addr_list.length == 0){
                selected_ip = 'Null';
            }
        }else if (obj == 'ONLINE'){
            if (selected_ip.length == 0 && online_ip_addr_list.length != 0){
                selected_ip = 'All';
            }else if (selected_ip.length == 0 && online_ip_addr_list.length == 0){
                selected_ip = 'Null';
            }
        }else {
            selected_ip = 'Null';
        }
        if (selected_ip.length > 6){
                selected_ip = selected_ip.splice(0, 6);
                selected_ip = selected_ip + ' ...';
        }

        ko.cleanNode(document.getElementById("selected_ip"));
        ko.applyBindings(selected_ip, document.getElementById("selected_ip"));
    },

    GetProjectServers: function(project){
        uat_ip_addr_list.length = 0;
        online_ip_addr_list.length = 0;
        html_uat = "";
        html_online = "";
        var projectlist = [];
        projectlist.push(project);
        //console.log(projectlist);
        var postData = {};
        postData['project'] = projectlist;
        postData['act'] = 'gethosts';
        $.ajax({
            url: "/upgrade/get_hosts",
            type: "post",
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(postData),
            success: function (datas, status) {
                //alert(datas);
                var data = eval(datas);
                //var html = "<option value=''></option>";
                if (data.op_status == 0){
                    $('#upgrade_results').append('<p>接口返回：'+data.result+'</p>');
                    $('#upgrade_results').append('获取主机地址失败...');
                }else {
                    var html_uat_tmp = "";
                    var html_online_tmp = "";
                    try {
                        var ip_dict = eval('('+ data.result +')')
                    }catch (e){
                        $('#upgrade_results').append('<p>接口返回：'+data.result+'</p>');
                        $('#upgrade_results').append('获取主机地址失败...');
                        return false;
                    }
                    //console.log(ip_dict)
                    try {
                        if (typeof(ip_dict.ONLINE) == 'object'){
                            var ip_online = ip_dict.ONLINE;
                        }else {
                            var ip_online = eval('('+ ip_dict.ONLINE +')');
                        }
                        if (ip_online.length == 1 && ip_online[0] == ""){
                            $('#upgrade_results').append('获取运营环境主机地址为空...');
                        }else {
                            $('#upgrade_results').append('<p>获取运营环境主机地址成功...</p>');
                            operate.disableButtons(['upgrade_envir_online'], false)
                        }
                    }catch (e){
                        $('#upgrade_results').append('<p>接口返回：'+ip_dict.ONLINE+'</p>');
                        $('#upgrade_results').append('获取运营环境主机地址失败...');
                        return false;
                    }
                    try {
                        if (typeof(ip_dict.UAT) == 'object'){
                            var ip_uat = ip_dict.UAT;
                        }else {
                            var ip_uat = eval('('+ ip_dict.UAT +')');
                        }
                        if (ip_uat.length == 1 && ip_uat[0] == ""){
                            $('#upgrade_results').append('获取测试环境主机地址为空...');
                        }else {
                            $('#upgrade_results').append('<p>获取测试环境主机地址成功...</p>');
                            operate.disableButtons(['upgrade_envir_uat'], false)
                        }
                    }catch (e){
                        $('#upgrade_results').append('<p>接口返回：'+ip_dict.UAT+'</p>');
                        $('#upgrade_results').append('获取测试环境主机地址失败...');
                        return false;
                    }
                    $.each(ip_online, function (index, item) { 
                        //循环获取数据 
                        var ip = ip_online[index];
                        html_name = "<option value='"+ip+"'>"+ip+"</option>";
                        html_online_tmp = html_online_tmp + html_name;
                        online_ip_addr_list.push(ip);
                    });
                    $.each(ip_uat, function (index, item) { 
                        //循环获取数据 
                        var ip = ip_uat[index];
                        html_name = "<option value='"+ip+"'>"+ip+"</option>";
                        html_uat_tmp = html_uat_tmp + html_name;
                        uat_ip_addr_list.push(ip);
                    }); 
                    //html_tmp = "<optgroup label='"+ project +"'>" + html_tmp + "</optgroup>";
                    html_uat = html_uat + html_uat_tmp;
                    html_online = html_online + html_online_tmp;
                    //operate.disableButtons(['upgrade_envir_uat', 'upgrade_envir_online'], false)
                    
                }
                return false;
            },
            error:function(XMLHttpRequest, textStatus, errorThrown){
                if (XMLHttpRequest.status == 0){
                    toastr.error('后端服务不响应，获取主机地址失败...', '错误');
                    $('#upgrade_results').append('后端服务不响应，获取主机地址失败...');
                }else {
                    toastr.error(XMLHttpRequest.responseText, XMLHttpRequest.status);
                    $('#upgrade_results').append('<p>'+XMLHttpRequest.responseText+'</p>');
                }
            },
        });
        return false;
    },

    setupIp: function (obj){
        if (obj.value == 'UAT'){
            document.getElementById('upgrade_ip').innerHTML=html_uat;
        }else if(obj.value == 'ONLINE'){
            document.getElementById('upgrade_ip').innerHTML=html_online;
        }
        $('.selectpicker').selectpicker('refresh');
        operate.DisSelectedIp();
    },

    operateUpgradeSelect: function(){
        $('#btn_op_search').on("click", function () {
            var postData = {
                project:"all",
                cur_status_sel:"all",
                deleted:"all",
            };
            if (! document.getElementById("project_active").value == ""){
                var projectlist = [];
                var objSelectproject = document.upgradeform.project_active; 
                for(var i = 0; i < objSelectproject.options.length; i++) { 
                    if (objSelectproject.options[i].selected == true) 
                    projectlist.push(objSelectproject.options[i].value);
                }
                postData['project'] = projectlist;
            }
            if (document.getElementById("cur_status_sel").value != ""){
                var statuslist = [];
                var objSelectstatus = document.upgradeform.cur_status_sel; 
                for(var i = 0; i < objSelectstatus.options.length; i++) { 
                    if (objSelectstatus.options[i].selected == true) 
                    statuslist.push(objSelectstatus.options[i].value);
                }
                postData['cur_status_sel'] = statuslist;
            }
            if (document.getElementById("deleted").value != ""){
                var deletedlist = [];
                var objSelectstatus = document.upgradeform.deleted; 
                for(var i = 0; i < objSelectstatus.options.length; i++) { 
                    if (objSelectstatus.options[i].selected == true) 
                    deletedlist.push(objSelectstatus.options[i].value);
                }
                postData['deleted'] = deletedlist;
            }
            //if (postData['cur_status'] != 'undone'){
            //    if (! document.getElementById("handle_user").value == ""){
            //        var userlist = [];
            //        var objSelectuser = document.upgradeform.handle_user; 
            //        for(var i = 0; i < objSelectuser.options.length; i++) { 
            //            if (objSelectuser.options[i].selected == true) {
            //                userlist.push(objSelectuser.options[i].value);
            //            }
            //        }
            //        postData['handle_user'] = userlist;
            //    }
            //}
            //console.log(postData)
            
            var act = '';
            if (postData['deleted'] == 'all' || postData['deleted'].length == 2){
                act = 'query_all';
            } else if (postData['deleted'].length == 1){
                if (postData['deleted'][0] == 0){
                    act = 'query_not_deleted';
                }else if (postData['deleted'][0] == 1){
                    act = 'query_deleted';
                }else {
                    act = 'null';
                }
            }

            var params = {
                url: '/upgrade/query_svn',
                method: 'post',
                singleSelect: false,
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 'postData': postData, 'act': act };
                },
            }
            $('#upgrade_op_table').bootstrapTable('refresh', params);
            return false;

        });
    },

    editConfig: function (obj){
            //var postData = {};
            document.getElementById('edit_config_uat').disabled = true;
            document.getElementById('edit_config_online').disabled = true;
            postEditConfig['project'] = document.getElementById('choose_envir_project').innerText;
            postEditConfig['svn_id'] = document.getElementById('choose_envir_svn_id').innerText;
            postEditConfig['envir'] = obj.value;
            postEditConfig['act'] = 'getfiles'
            $.ajax({
                url: "/upgrade/edit_config",
                type: "post",
                data: JSON.stringify(postEditConfig),
                success: function (datas, status) {
                    data = eval('('+datas+')');
                    //toastr.success('操作成功！', data['response']);
                    $('#choose_envir_modal').modal('hide');
                    $('#edit_config_modal').modal('show');
                    ko.cleanNode(document.getElementById('radio_config_list'));
                    config_name.value = "";
                    config_content.value = "";
                    Displayadd.style.display = 'inline';
                    myViewModel = {}
                    if (data.files == {}){
                        document.getElementById("edit_config_head").innerHTML = '请新增配置文件';
                    }else {
                        document.getElementById("radio_config_list").innerHTML = '';
                        document.getElementById("edit_config_head").innerHTML = '请选择要编辑的文件';
                        //console.log(data)
                        for (var file in data.files){
                            target = file.split('.')[0].replace(/-|_/g, '');
                            //console.log(target)
                            myViewModel[target] = ko.observable(file); 
                            var content = data.files[file].join('');
                            var html = [
                                '<label class="label_e">',
                                    '<input type="radio"  name="config_name" onclick="operate.DisplayFileContent(this)" style="margin-left: 10px;" id="radio_'+target+'" data-bind="text: '+target+'"> <span data-bind="text: '+target+'"></span>',
                                '</label>',
                                '<textarea id="textarea_'+target+'" style="display:none">'+content+'</textarea>',
                            ].join('');
                            $("#radio_config_list").append(html);
                        }
                    }
                    ko.applyBindings(myViewModel, document.getElementById('radio_config_list'));

                    //console.log(data.files);
                },
                error: function(XMLHttpRequest, textStatus, errorThrown){
                    if (XMLHttpRequest.status == 0){
                        toastr.error('后端服务不响应', '错误');
                    }else {
                        toastr.error(XMLHttpRequest.responseText, XMLHttpRequest.status)
                    }
                    document.getElementById('edit_config_uat').disabled = false;
                    document.getElementById('edit_config_online').disabled = false;
                }
            });
    },

    DisplayFileContent: function (obj){
        //console.log(content)
        //获取到目标
        target = obj.id.split("_")[1]
        //隐藏新增
        Displayadd.style.display = 'none';
        Displaydelete.style.display = 'none';
        //修改临时文本的name值
        $("#config_content").attr("name", obj.value)
        //填充数据框的值
        config_name.value = myViewModel[target]();
        //填充文本框的值
        config_content.value = document.getElementById("textarea_"+target).value;
    },

    updateConfig: function (obj){
        //判断是不是要新增文件
        if (Displayadd.style.display == 'inline'){
            return false;
        }

        //判断是否选中了文件
        var file = $("input[name='config_name']:checked"); 
        var item = file.val()
        if (file.val() == undefined){
            return false;
        }
        //获取到目标
        target = file.attr("id").split("_")[1]

        //判断是要更新文件名还是文件内容
        if (obj.type == 'text'){
            myViewModel[target](obj.value);
        }else if(obj.type == 'textarea'){
            document.getElementById("textarea_"+target).value = obj.value;
        }

    },

    Buttons: function () {
        $('#btn_add_config').on("click", function () {
            Displayadd.style.display = 'inline';
            Displaydelete.style.display = 'none';
            var file = $("input[name='config_name']:checked"); 
            if (file.val() == undefined){
                return false;
            }else {
                config_name.value = "";
                config_content.value = "";
                $("input:radio").prop("checked",false);
            }
        });

        $('#btn_delete_config').on("click", function () {
            Displayadd.style.display = 'none';
            Displaydelete.style.display = 'inline';
        });

        $('#btn_save_new_config').on("click", function () {
            if (config_name.value == ""){
                toastr.warning('请先输入文件名')
                return false;
            }
            try {
                if (/([a-z]+|[0-9]+)\.[a-z]+/.test(config_name.value)){
                    target = config_name.value.split('.')[0];
                }else {
                    toastr.warning('请输入正确的文件名')
                    return false;
                }
                for (var key in myViewModel){
                    if (config_name.value == myViewModel[key]()){
                        toastr.warning('文件名已存在')
                        return false;
                    }
                    if (target == key){
                        target = target+"A"
                    }
                }
            }catch (e){
                toastr.warning('请输入正确的文件名')
                return false;
            }
            myViewModel[target] = ko.observable(config_name.value);
            //console.log(myViewModel)
            //重新绑定
            ko.cleanNode(document.getElementById('radio_config_list'));
            content = config_content.value;
            var html = [
                '<label class="label_e">',
                    '<input type="radio"  name="config_name" onclick="operate.DisplayFileContent(this)" style="margin-left: 10px;" id="radio_'+target+'" data-bind="text: '+target+'"> <span data-bind="text: '+target+'"></span>',
                '</label>',
                '<textarea id="textarea_'+target+'" style="display:none">'+content+'</textarea>',
            ].join('')
            $("#radio_config_list").append(html);
            ko.applyBindings(myViewModel, document.getElementById('radio_config_list'));
            Displayadd.style.display = 'none';
            document.getElementById("radio_"+target).checked = true;
            toastr.success('文件新建成功！', config_name.value);
        });

        $('#btn_confirm_delete_config').on("click", function () {
            var file = $("input[name='config_name']:checked"); 
            if (file.val() == undefined){
                toastr.warning('没有删除任何文件')
                return false;
            }

            //获取到目标
            target = file.attr("id").split("_")[1];
            delete myViewModel[target];
            inputh = document.getElementById("radio_"+target);
            texth = document.getElementById("textarea_"+target);
            texth.parentNode.removeChild(texth);
            inputh.parentNode.parentNode.removeChild(inputh.parentNode);

            toastr.success('文件删除成功！', config_name.value);
            config_name.value = "";
            config_content.value = "";

            Displaydelete.style.display = 'none';
            
        });

        $('#btn_submit').on("click", function () {
            postEditConfig['act'] = 'commitfiles';
            postEditConfig['files'] = {};
            for (var key in myViewModel){
                file = myViewModel[key]();
                postEditConfig['files'][file] = document.getElementById("textarea_"+key).value;
            }
            //console.log(postEditConfig);
            edit_config_head.innerHTML = '正在保存配置文件，请稍后...'
            $.ajax({
                url: "/upgrade/edit_config",
                type: "post",
                data: JSON.stringify(postEditConfig),
                success: function (datas, status) {
                    edit_config_head.innerHTML = '保存配置文件成功...'
                },
                error: function(XMLHttpRequest, textStatus, errorThrown){
                    if (XMLHttpRequest.status == 0){
                        toastr.error('后端服务不响应', '错误')
                    }else {
                        toastr.error(XMLHttpRequest.responseText, XMLHttpRequest.status)
                    }
                    edit_config_head.innerHTML = '保存配置文件失败，请重试...'
                }
            });
        });

        $('#btn_update_upgrade_status_submit').on("click", function () {
            operate.disableButtons(['btn_close_update_upgrade_status_modal', 'btn_update_upgrade_status_submit'], true);

            var postData = {
                id: document.getElementById('upgrade_status_id').value,
            }
            if (document.getElementById('uat_upgrade_done').checked == true){
                postData['envir_uat'] = 'done';
            }else if (document.getElementById('uat_upgrade_rollback').checked == true){
                postData['envir_uat'] = 'rollback';
            }else {
                postData['envir_uat'] = 'undone';
            }

            if (document.getElementById('online_upgrade_done').checked == true){
                postData['envir_online'] = 'done';
            }else if (document.getElementById('online_upgrade_rollback').checked == true){
                postData['envir_online'] = 'rollback';
            }else {
                postData['envir_online'] = 'undone';
            }

            postData['act'] = 'update_upgrade_status';

            $.ajax({
                url: "/upgrade/update_svn",
                type: "post",
                data: JSON.stringify(postData),
                success: function (datas, status) {
                    toastr.success('修改成功');
                    $('#upgrade_op_table').bootstrapTable('refresh');
                    $('#update_upgrade_status_modal').modal('hide');
                },
                error: function(XMLHttpRequest, textStatus, errorThrown){
                    operate.disableButtons(['btn_close_update_upgrade_status_modal', 'btn_update_upgrade_status_submit'], false);
                    if (XMLHttpRequest.status == 0){
                        toastr.error('后端服务不响应', '错误');
                    }else {
                        toastr.error(XMLHttpRequest.responseText, XMLHttpRequest.status)
                    }
                }
            });
        });

    },

    setHandleUser: function(){
        var objSelectstatus = document.upgradeform.cur_status_sel;
        var count = 0;
        for(var i = 0; i < objSelectstatus.options.length; i++) { 
            if (objSelectstatus.options[i].selected == true) 
            count = count + 1;
        }
        if (document.getElementById("cur_status_sel").value == "undone" && count == 1){
            $('#handle_user').prop('disabled', true);
            $('#handle_user').selectpicker('refresh');
            //$("#handle_user").selectpicker('setStyle', 'btn-warning');
        }else {
            $('#handle_user').prop('disabled', false);
            $('#handle_user').selectpicker('refresh');
            //$("#handle_user").removeAttr("disabled");
            //$("#handle_user").selectpicker('setStyle', 'btn-warning', 'remove');
            //$("#handle_user").selectpicker('setStyle', 'btn-default');
        }
    },

    selectpicker: function() {
        $('.selectpicker').selectpicker({
            style: 'btn-default',
            //width: "auto",
            size: 10,
            showSubtext:true,
        });
    },

    //数据校验
    operateCheck:function(arr){
        if (arr.length <= 0) {
            alert("请至少选择一行数据");
            return false;
        }
        if (arr.length > 1) {
            alert("只能编辑一行数据");
            return false;
        }
        return true;
    }
}