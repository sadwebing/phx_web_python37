$(function () {
    tableInit.Init();
    operate.operateInit();
});

//全局变量
window.modal_results = document.getElementById("Checkresults");
window.modal_footer = document.getElementById("progressFooter");
window.modal_head = document.getElementById("progress_head");

//初始化表格
var tableInit = {
    Init: function () {
        //this.dbclick();
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/monitor/project/Query',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            clickToSelect: false,
            height:780,
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset, 'act':'query_all' };
            },//传递参数（*）
            columns: [
                //{
                //    checkbox: true,
                //    width:'2%',
                //},
                {
                    field: 'id',
                    title: 'id',
                    sortable: true,
                    width:'3%',
                    //align: 'center'
                },{
                    field: 'envir',
                    title: '环境',
                    sortable: true,
                    width:'5%',
                    //align: 'center'
                },{
                    field: 'product',
                    title: '产品',
                    sortable: true,
                    width:'9%',
                    //align: 'center'
                },{
                    field: 'project',
                    title: '项目名',
                    sortable: true,
                    width:'9%',
                    //align: 'center'
                },{
                    field: 'minion_id',
                    title: 'Minion Id',
                    sortable: true,
                    //align: 'center',
                    width:'18%',
                },{
                    field: 'server_type',
                    title: '服务类型',
                    sortable: true,
                    width:'8%',
                    //align: 'center'
                },{
                    field: 'role',
                    title: '角色',
                    sortable: true,
                    width:'6%',
                    //align: 'center'
                }, {
                    field: 'domain',
                    title: '域名',
                    sortable: true,
                    width:'auto',
                    //align: 'center',
                    //events: this.cur_statusEvents,
                    formatter: this.cur_statusFormatter
                },{
                    field: 'uri',
                    title: '检测地址',
                    sortable: true,
                    //align: 'center',
                    width:'auto',
                },{
                    field: 'status_',
                    title: '状态',
                    sortable: true,
                    width:'5%',
                    events: operateStatusEvents,
                    formatter: this.operateStatusFormatter,
                    //align: 'center'
                },{
                    field: 'info',
                    title: '备注',
                    sortable: true,
                    width:'auto',
                    //align: 'center'
                },{
                    field: 'operations',
                    title: '操作项',
                    //align: 'center',
                    width:'6%',
                    checkbox: false,
                    events: operateEvents,
                    formatter: this.operateFormatter,
                    //width:300,
                },
            ]

        });
        ko.applyBindings(this.myViewModel, document.getElementById("tomcat_table"));
        //部分列进行隐藏
        //$('#tomcat_table').bootstrapTable('hideColumn', 'operations');
    },

    dbclick: function (){
        $('#tomcat_table').on('all.bs.table', function (e, name, args) {
            //console.log('Event:', name, ', data:', args);
        }).on('dbl-click-cell.bs.table', function (e, field, value, row, $element) {
            console.log(row)
            //return false;
            $("#myModal").modal().on("shown.bs.modal", function () {
                //将选中该行数据有数据Model通过Mapping组件转换为viewmodel
                ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(row));
                if (document.getElementById(operate.DepartmentModel.id()).checked){
                    operate.DepartmentModel.status_ = 'active';
                }else {
                    operate.DepartmentModel.status_ = 'inactive';
                }
                ko.applyBindings(operate.DepartmentModel, document.getElementById("myModal"));
                operate.operateSave('Update');
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("myModal"));
            });

        });
    },

    operateStatusFormatter: function (value,row,index){
        if (row.status_ == 'active'){
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id='+ row.id +' class="update_status" checked><span></span>',
                '</label>',
            '</div>'
            ].join('');
        }else if (row.status_ == 'inactive'){
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id='+ row.id +' class="update_status"><span></span>',
                '</label>',
            '</div>'
            ].join('');
        }else {
            content = ['<p>unknown</p>']
        }
        return content;
    },

    operateFormatter: function (value,row,index){
        content = [
        '<a class="check_server" href="javascript:void(0)" title="检测服务">',
        '<i class="text-primary"> 检测</i>',
        '</a>'
        ].join('');   
        return content;
    },
};

window.operateStatusEvents = {
    'click .update_status': function (e, value, row, index) {
        var postData = {
            id:row.id,
            status,
        };
        if (document.getElementById(row.id).checked){
            postData.status = 1;
            //console.log(postData);
        }else {
            postData.status = 0;
            //console.log(postData);
        }
        $.ajax({
            url: "/monitor/project/UpdateStatus",
            type: "post",
            data: JSON.stringify(postData),
            success: function (data, status) {
                if (postData.status == 1){
                    toastr.success(row.product+"_"+row.project+": "+row.domain, '监控项已启用');
                }else {
                    toastr.warning(row.product+"_"+row.project+": "+row.domain, '监控项已禁用');
                }
                
                //ko.cleanNode(document.getElementById("tomcat_table"));
                row.status_ = postData.status;
                //alert(data);
                //tableInit.myViewModel.refresh();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                if (postData.status == 1){
                    document.getElementById(row.id).checked = false;
                }else {
                    document.getElementById(row.id).checked = true;
                }
                if (XMLHttpRequest.status == 0){
                    toastr.error('后端服务不响应', '错误')
                }else {
                    toastr.error(XMLHttpRequest.responseText, XMLHttpRequest.status)
                }
                //console.info(XMLHttpRequest)
                //alert(XMLHttpRequest.status+': '+XMLHttpRequest.responseText);
                //tableInit.myViewModel.refresh();
            }
        });
        return false;
    },
};

window.operateEvents = {
    'click .check_server': function (e, value, row, index) {
        var postData = {
            minion_id:row.minion_id,
            server_type:row.server_type,
            domain:row.domain,
            uri:row.uri,
        };
        modal_results.innerHTML = "";
        modal_footer.innerHTML = "";
        document.getElementById('progress_bar_div').hidden = false;
        $("#progress_bar").css("width", "30%");
        modal_head.style.color = 'blue';
        modal_head.innerHTML = "操作进行中，请勿刷新页面......";
        var socket = new WebSocket("ws://" + window.location.host + "/monitor/project/CheckServer");
        socket.onopen = function () {
            //console.log('WebSocket open');//成功连接上Websocket
            socket.send(JSON.stringify(postData));
        };
        $('#runprogress').modal('show');
        socket.onerror = function (){
            modal_head.innerHTML = "与服务器连接失败...";
            $('#Checkresults').append('<p>连接失败......</p>' );
            setTimeout(function(){$('#runprogress').modal('hide');}, 1000);
        };
        socket.onmessage = function (e) {
            data = eval('('+ e.data +')')
            //console.log('message: ' + data);//打印服务端返回的数据
            if (data.step == 'one'){
                $("#progress_bar").css("width", "50%");
                $('#Checkresults').append('<p> 产品名:&thinsp;<strong>' + row.product + '</strong></p>' );
                $('#Checkresults').append('<p> 项目名:&thinsp;<strong>' + row.project + '</strong></p>' );
                $('#Checkresults').append('<p> 服务器地址:&thinsp;<strong>' + row.minion_id + '</strong></p>' );
                $('#Checkresults').append('<p> 服务类型:&thinsp;<strong>' + row.server_type + '</strong></p>' );
                $('#Checkresults').append('<p> 角色:&thinsp;<strong>' + row.role + '</strong></p>' );
                $('#Checkresults').append('<p> 域名:&thinsp;<strong>' + row.domain + '</strong></p>' );
                $('#Checkresults').append('<p> 检测地址:&thinsp;<strong>' + row.uri + '</strong></p>' );
                $('#Checkresults').append('<hr>' );
            }else if (data.step == 'final'){
                $("#progress_bar").css("width", "100%");
                modal_head.innerHTML = "检测完成！";
                $('#Checkresults').append('<p> 检测时间:&thinsp;<strong>' + data.access_time + '</strong></p>' );
                $('#Checkresults').append('<p> 检测状态:&thinsp;<strong>' + data.code + '</strong></p>' );
                //$('#Checkresults').append('<p> 备注:&thinsp;<strong>' + data.info + '</strong></p>' );
                //setTimeout("document.getElementById('progress_bar_div').hidden = true;", 1000)
                //console.log('websocket已关闭');
                modal_footer.innerHTML = '<button id="close_modal" type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span>关闭</button>'
                socket.close();
            }
        };
        return false;
    },
}; 

window.operateMailEvents = {
    'click .update_mail_status': function (e, value, row, index) {
        var check_id = event.target.id
        var program = check_id.replace(/[0-9]+_/g, "");
        var postData = {
            id:row.id,
            program:program,
        };
        postData[program] = 0;
        //console.log(row[postData.program])
        //console.log(event.target.id.replace(/[0-9]+_/g, ""))
        if (document.getElementById(event.target.id).checked){
            postData[program] = 1;
            //console.log(postData);
        }else {
            postData[program] = 0;
            //console.log(postData);
        }
        $.ajax({
            url: "/tomcat/mail/UpdateMailStatus",
            type: "post",
            data: JSON.stringify(postData),
            success: function (data, status) {
                if (postData[program] == 1){
                    toastr.success(postData.program+": "+row.mail_address, '报警邮箱已启用');
                }else {
                    toastr.warning(postData.program+": "+row.mail_address, '报警邮箱已禁用');
                }
                
                row[program] = postData[program];
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                if (postData[program] == 1){
                    document.getElementById(check_id).checked = false;
                }else {
                    document.getElementById(check_id).checked = true;
                }
                if (XMLHttpRequest.status == 0){
                    toastr.error('后端服务不响应', '错误')
                }else {
                    toastr.error(XMLHttpRequest.responseText, XMLHttpRequest.status)
                }
                //tableInit.myViewModel.refresh();
            }
        });
        return false;
    },
};

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        //this.operateCheckStatus();
        //this.operateEditMail();
        this.selectpicker();
        this.operateAdd();
        this.operateUpdate();
        this.operateconfirmDelete();
        this.operateMonitorPorjectSelect();
        //this.operateDelete();
        this.DepartmentModel = {
            id: ko.observable(),
            envir: ko.observable(),
            project: ko.observable(),
            minion_id: ko.observable(),
            ip_addr: ko.observable(),
            server_type: ko.observable(),
            role: ko.observable(),
            domain: ko.observable(),
            url: ko.observable(),
            status_: ko.observable(),
            info: ko.observable(),
        };
    },

    selectpicker: function docombjs() {
        $('.selectpicker').selectpicker({
            style: 'btn-default',
            //width: "auto",
            size: 15,
            showSubtext:true,
        });
    },

    //新增
    operateAdd: function(){
        $('#btn_add').on("click", function () {
            $("#myModal").modal().on("shown.bs.modal", function () {
                var oEmptyModel = {
                    envir: ko.observable(),
                    project: ko.observable(),
                    minion_id: ko.observable(),
                    ip_addr: ko.observable(),
                    server_type: ko.observable(),
                    role: ko.observable(),
                    domain: ko.observable(),
                    url: ko.observable(),
                    status_: ko.observable(),
                    info: ko.observable(),
                };
                ko.utils.extend(operate.DepartmentModel, oEmptyModel);
                ko.applyBindings(operate.DepartmentModel, document.getElementById("myModal"));
                operate.operateSave('Add');
            }).on('hidden.bs.modal', function () {
                ko.cleanNode(document.getElementById("myModal"));
            });
        });
    },

    //编辑
    operateUpdate: function () {
        $('#btn_edit').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (!operate.operateCheck(arrselectedData)) { return; }
            $("#myModal").modal().on("shown.bs.modal", function () {
                operate.operateSave('Update');
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("myModal"));
            });
        });
    },

    //保存数据
    operateSave: function (funcName) {
        $('#btn_submit').on("click", function () {
            //取到当前的viewmodel
            var oViewModel = operate.DepartmentModel;
            console.log(oViewModel.project())
            if (! oViewModel.project()){
                alert('项目名 不能为空！')
                return false;
            }
            if (! oViewModel.minion_id()){
                alert('Minion Id 不能为空！')
                return false;
            }
            if (! oViewModel.ip_addr()){
                alert('Ip地址 不能为空！')
                return false;
            }
            if (! oViewModel.domain()){
                oViewModel.domain = 'null';
            }
            if (! oViewModel.info()){
                oViewModel.info = '';
            }
            if (! oViewModel.url()){
                oViewModel.url = 'null';
            }
            //将Viewmodel转换为数据model
            var oDataModel = ko.toJS(oViewModel);
            //var funcName = oDataModel.id?"Update":"Add";
            $.ajax({
                url: "/tomcat/project/"+funcName,
                type: "post",
                data: oDataModel,
                success: function (data, status) {
                    toastr.success(data);
                    tableInit.myViewModel.refresh();
                },
                error:function(XMLHttpRequest, textStatus, errorThrown){
                    if (XMLHttpRequest.status == 0){
                        toastr.error('后端服务不响应', '错误')
                    }else {
                        toastr.error(XMLHttpRequest.responseText, XMLHttpRequest.status)
                    }
                    //alert("失败，请检查日志！");
                    //tableInit.myViewModel.refresh();
                }
            });
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