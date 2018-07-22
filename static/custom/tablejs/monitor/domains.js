//全局变量
window.modal_results = document.getElementById("Checkresults");
window.modal_footer  = document.getElementById("progressFooter");
window.modal_head    = document.getElementById("progress_head");
window.data_all      = {}

$(function () {
    tableInit.Init();
    operate.operateInit();
});

//初始化表格
var tableInit = {
    Init: function () {
        //this.dbclick();
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            //url: '/monitor/domains/Query',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            clickToSelect: true,
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset, 'status': 2, 'num': 30 };
            },//传递参数（*）
            columns: [
                {
                    checkbox: true,
                    width:'2%',
                },
                {
                    field: 'id',
                    title: 'id',
                    sortable: true,
                    width:'3%',
                    //align: 'center'
                },{
                    field: 'name',
                    title: '域名',
                    sortable: true,
                    //width:'5%',
                    //align: 'center'
                },{
                    field: 'product',
                    title: '产品',
                    sortable: true,
                    //width:'9%',
                    //align: 'center'
                }
                ,{
                    field: 'group',
                    title: '所属组',
                    sortable: true,
                    //width:'9%',
                    //align: 'center'
                }
                ,{
                    field: 'status',
                    title: '状态',
                    sortable: true,
                    //width:'5%',
                    events: operateStatusEvents,
                    formatter: this.operateStatusFormatter,
                    //align: 'center'
                },{
                    field: 'content',
                    title: '备注',
                    sortable: true,
                    //width:'auto',
                    //align: 'center'
                },
                //{
                //    field: 'operations',
                //    title: '操作项',
                //    //align: 'center',
                //    width:'6%',
                //    checkbox: false,
                //    events: operateEvents,
                //    formatter: this.operateFormatter,
                //    //width:300,
                //},
            ]

        });
        ko.applyBindings(this.myViewModel, document.getElementById("tomcat_table"));
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
        if (row.status == 1){
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id='+ row.id +' class="update_status" checked><span></span>',
                '</label>',
            '</div>'
            ].join('');
        }else if (row.status == 0){
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
            url: "/monitor/domains/UpdateStatus",
            type: "post",
            data: JSON.stringify(postData),
            success: function (data, status) {
                if (postData.status == 1){
                    toastr.success(row.product+": "+row.name, '监控项已启用');
                }else {
                    toastr.warning(row.product+": "+row.name, '监控项已禁用');
                }
                
                //ko.cleanNode(document.getElementById("tomcat_table"));
                row.status = postData.status;
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
        this.getGroups();
        this.operateAdd();
        this.operateUpdate();
        this.operateconfirmDelete();
        this.operateMonitorPorjectSelect();
        //this.operateDelete();
        this.DepartmentModel = {
            id: ko.observable(),
            name: ko.observable(),
            product: ko.observable(),
            group: ko.observable(),
            content: ko.observable(),
            status: ko.observable(),
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

    getGroups: function () {
        $.ajax({
            url: "/monitor/domains/getGroups",
            type: "get",
            success: function (datas, status) {
                //var data = eval(datas);
                var data = eval('(' + datas + ')');;
                //console.log(data);
                //var selects = "<option selected value>all</option>";
                var selects = {}
                selects['data']    = data
                selects['group']   = "";
                selects['product'] = "";
                $.each(data['group_l'], function (index, item) { 
                    selects['group'] = selects['group'] + "<option value="+item.id+" data-subtext='"+item.client+" | "+item.method+" | "+item.ssl+" | "+item.retry+"'>"+item.group+"</option>"
                }); 
                $.each(data['product_l'], function (index, item) { 
                    selects['product'] = selects['product'] + "<option value="+item[0]+">"+item[1]+"</option>"
                }); 
                document.getElementById("txt_group").innerHTML=selects['group'];
                document.getElementById("txt_product").innerHTML=selects['product'];
                document.getElementById("txt_add_group").innerHTML=selects['group'];
                document.getElementById("txt_add_product").innerHTML=selects['product'];
                $('.selectpicker').selectpicker('refresh');
                data_all = selects;
                return true;
            },
            error: function(msg){
                alert("获取组信息失败，请检查日志！");
                //tableInit.myViewModel.refresh();
                return ""
            }
        });
    },

    
    
    operateMonitorPorjectSelect: function(){
        $('#btn_query').on("click", function () {
            var group_l   = [];
            var product_l = [];
            var objSelectproject = document.selectmalform.txt_group
            for(var i = 0; i < objSelectproject.options.length; i++) { 
                if (objSelectproject.options[i].selected == true) 
                group_l.push(objSelectproject.options[i].value);
            }
            if (group_l.length == 0) {
                for(var i = 0; i < objSelectproject.options.length; i++) {
                    group_l.push(objSelectproject.options[i].value);
                }
            }
            objSelectproject = document.selectmalform.txt_product
            for(var i = 0; i < objSelectproject.options.length; i++) { 
                if (objSelectproject.options[i].selected == true) 
                product_l.push(objSelectproject.options[i].value);
            }
            if (product_l.length == 0) {
                for(var i = 0; i < objSelectproject.options.length; i++) {
                    product_l.push(objSelectproject.options[i].value);
                }
            }
            
            var params = {
                url: '/monitor/domains/Query',
                method: 'post',
                singleSelect: false,
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 
                        'status':document.getElementById("txt_status").value, 
                        'num': document.getElementById("txt_num").value, 
                        'group': group_l,
                        'product': product_l,
                        };
                },
            }
            tableInit.myViewModel.refresh(params);
        });

        $('#domains_active').on("click", function () {
            //document.getElementById('project_active').disabled = true;
            //document.getElementById('project_inactive').disabled = false;
            //document.getElementById('project_all').disabled = false;
            var params = {
                url: '/monitor/domains/Query',
                method: 'post',
                singleSelect: false,
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 
                        'status':1, 
                        'num': document.getElementById("txt_num").value, 
                        'group': document.getElementById("txt_group").value,
                        };
                },
            }
            tableInit.myViewModel.refresh(params);
        });
        $('#domains_inactive').on("click", function () {
            //document.getElementById('project_active').disabled = false;
            //document.getElementById('project_inactive').disabled = true;
            //document.getElementById('project_all').disabled = false;
            var params = {
                url: '/monitor/domains/Query',
                method: 'post',
                singleSelect: false,                                                
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 
                        'status': 0, 
                        'num': document.getElementById("txt_num").value, 
                        'group': document.getElementById("txt_group").value,
                        };
                },
            }
            tableInit.myViewModel.refresh(params);
        });
        $('#domains_all').on("click", function () {
            //document.getElementById('project_active').disabled = false;
            //document.getElementById('project_inactive').disabled = false;
            //document.getElementById('project_all').disabled = true;
            var params = {
                url: '/monitor/domains/Query',
                method: 'post',
                singleSelect: false,
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 
                        'status': 2, 
                        'num': document.getElementById("txt_num").value, 
                        'group': document.getElementById("txt_group").value,
                        };
                },
            }
            tableInit.myViewModel.refresh(params);
        });
    },

    operateCheckStatus: function () {
        $.ajax({
            url: "/monitor/UpdateCheckStatus",
            type: "get",
            success: function (datas, status) {
                var data = eval(datas);
                $.each(data, function (index, item) { 
                    if (document.getElementById(data[index]['program'])){
                        if (data[index]['status'] == 1){
                            document.getElementById(data[index]['program']).checked = true; 
                        }else {
                            document.getElementById(data[index]['program']).checked = false;
                        }
                    }
                }); 
            },
            error: function(msg){
                alert("查询监控项状态失败，请检查日志！");
                //tableInit.myViewModel.refresh();
            }
        });
        var postData = {
            program:'',
            status:1,
        };
        $('#check_services').on("click", function () {
            postData.program = 'check_services';
            if (document.getElementById('check_services').checked){
                postData.status = 1;
                //var status = '已启用监控！'
                //toastr.success("check_services"+": "+status, '状态已更新');
            }else {
                postData.status = 0;
                //var status = '已禁用监控！'
                //toastr.warning("check_services"+": "+status, '状态已更新');
            }
            updateCheckStatus(postData);
        });

        $('#check_salt_minion').on("click", function () {
            postData.program = 'check_salt_minion';
            if (document.getElementById('check_salt_minion').checked){
                postData.status = 1;
                //var status = '已启用监控！'
                //toastr.success("check_salt_minion"+": "+status, '状态已更新');
            }else {
                postData.status = 0;
                //var status = '已禁用监控！'
                //toastr.warning("check_salt_minion"+": "+status, '状态已更新');
            }
            updateCheckStatus(postData);
        });

        function updateCheckStatus (postData){
            //console.log(postData)
            var apostData = postData;
            $.ajax({
                url: "/tomcat/UpdateCheckStatus",
                type: "post",
                data: JSON.stringify(apostData),
                success: function (data, status) {
                    if (postData['status'] == 1){
                        var status = '已启用监控！'
                        toastr.success(postData.program+": "+status, '状态已更新');
                    }else {
                        var status = '已禁用监控！'
                        toastr.warning(postData.program+": "+status, '状态已更新');
                    }
                },
                error: function(XMLHttpRequest, textStatus, errorThrown){
                    if (apostData['status'] == 1){
                        document.getElementById(apostData['program']).checked = false;
                    }else {
                        document.getElementById(apostData['program']).checked = true;
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
        };

    },

    operateEditMail: function (){
        this.mailViewModel = new ko.bootstrapTableViewModel({
            url: '/tomcat/mail/Query',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            //toolbar: '#toolbar',                //工具按钮用哪个容器
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset, 'act':'query_all' };
            },//传递参数（*）
            columns: [
                {
                    field: 'id',
                    title: 'id',
                    sortable: true,
                    width:'3%',
                    //align: 'center'
                },{
                    field: 'name',
                    title: '姓名',
                    sortable: true,
                    width:'5%',
                    //align: 'center'
                },{
                    field: 'mail_address',
                    title: '邮箱',
                    sortable: true,
                    width:'18%',
                    //align: 'center'
                },{
                    field: 'role',
                    title: '角色',
                    sortable: true,
                    //align: 'center',
                    width:'9%',
                },{
                    field: 'check_services',
                    title: '假死监控',
                    sortable: true,
                    //align: 'center',
                    width:'5%',
                    events: operateMailEvents,
                    formatter: operate.checkServicesFormatter,
                },{
                    field: 'check_salt_minion',
                    title: 'minion监控',
                    sortable: true,
                    width:'5%',
                    //align: 'center'
                    events: operateMailEvents,
                    formatter: operate.checkSaltMinionFormatter,
                },
            ]
        });
        ko.applyBindings(this.mailViewModel, document.getElementById("mail_table"));
        //部分列进行隐藏
        $('#mail_table').bootstrapTable('hideColumn', 'id');
        $('#mail_table').bootstrapTable('hideColumn', 'name');
        $('#mail_table').bootstrapTable('hideColumn', 'role');
        $('#edit_mail').on("click", function () {
            //console.log(this.mailViewModel)
            $("#modifyMail").modal('show');
        });
    },

    checkServicesFormatter: function (value,row,index){
        //console.log(row)
        if (value == 1){
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id="'+ row.id+'_check_services" class="update_mail_status" checked><span></span>',
                '</label>',
            '</div>'
            ].join('');
        }else {
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id="'+ row.id+'_check_services" class="update_mail_status"><span></span>',
                '</label>',
            '</div>'
            ].join('');
        }
        return content;
    },

    checkSaltMinionFormatter: function (value,row,index){
        if (value == 1){
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id="'+ row.id+'_check_salt_minion" class="update_mail_status" checked><span></span>',
                '</label>',
            '</div>'
            ].join('');
        }else {
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id="'+ row.id+'_check_salt_minion" class="update_mail_status"><span></span>',
                '</label>',
            '</div>'
            ].join('');
        }
        return content;
    },

    isDomain: function (value) {
        var regexp = /^(http:\/\/|https:\/\/).*[a-zA-Z0-9]+.*\.[a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*.*$/;
        //var regexp_tw = /^(tw|.*\.tw)\..*$/;

        var valid = regexp.test(value);
        if(!valid){
            return false;
        }
        return true
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
                document.getElementById("txt_add_group").innerHTML=data_all['group'];
                document.getElementById("txt_add_product").innerHTML=data_all['product'];
                $('.selectpicker').selectpicker('refresh');
                operate.operateAddCommit();
                //operate.operateSave('Add');
            }).on('hidden.bs.modal', function () {
                ko.cleanNode(document.getElementById("myModal"));
            });
        });
        

    },

    operateAddCommit: function () {
        $('#btn_add_submit').on("click", function () {
            //取到当前的viewmodel
            var postData = {
                'status'  : document.getElementById('txt_add_status').value,
                'group'   : document.getElementById('txt_add_group').value,
                'product' : document.getElementById('txt_add_product').value,
                'domains' : document.getElementById('textarea_add_domain').value,
                'content' : document.getElementById('textarea_add_content').value,
            }

            if (! postData['group']){
                alert('前选择所属组！')
                return false;
            }
            if (! postData['product']){
                alert('前选择所属产品！')
                return false;
            }
            if (! postData['domains']){
                alert('域名不能为空！')
                return false;
            }else {
                postData['domain_l'] = postData['domains'].split('\n')
                for(var i = 0; i < postData['domain_l'].length; i++) { 
                    if(postData['domain_l'][i].replace(/ /g, '') === ''){
                        postData['domain_l'].splice(i, 1);
                    }else if (! operate.isDomain(postData['domain_l'][i])) {
                        alert(postData['domain_l'][i] + "格式不正确！");
                        return false;
                    }
                }
            }

            //var oDataModel = ko.toJS(postData);
            //var funcName = oDataModel.id?"Update":"Add";
            toastr.info("请求发送中，请耐心等待返回...");
            $.ajax({
                url: "/monitor/domains/Add",
                type: "post",
                data: JSON.stringify(postData),
                contentType: 'application/json',
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
    
    //编辑
    operateUpdate: function () {
        $('#btn_edit').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (!operate.operateCheck(arrselectedData)) { return; }
            //operate.operateSave('Update');
            if (arrselectedData.length == 1) {
                $("#editSingleModal").modal().on("shown.bs.modal", function () {
                    //operate.selectpicker();
                    //将选中该行数据有数据Model通过Mapping组件转换为viewmodel
                    ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[0]));
                    var data = ko.toJS(operate.DepartmentModel)
                    
                    for(var i = 0; i < data_all['data']['group_l'].length; i++) { 
                        if (data['group'] == data_all['data']['group_l'][i]['group']){
                            data['group'] = data_all['data']['group_l'][i]['id'];
                        }
                    }
                    for(var i = 0; i < data_all['data']['product_l'].length; i++) { 
                        if (data['product'] == data_all['data']['product_l'][i][1]){
                            data['product'] = data_all['data']['product_l'][i][0];
                        }
                    }
                    
                    if (document.getElementById(operate.DepartmentModel.id()).checked){
                        data['status'] = 1;
                    }else {
                        data['status'] = 0;
                    }
                    
                    document.getElementById("txt_edit_group").innerHTML=data_all['group'];
                    document.getElementById("txt_edit_product").innerHTML=data_all['product'];
                    ko.utils.extend(operate.DepartmentModel, data);
                    ko.applyBindings(operate.DepartmentModel, document.getElementById("editSingleModal"));
                    $('#btn_update_submit').on("click", function () {
                        operate.operateSave('Update');
                    });
                }).on('hidden.bs.modal', function () {
                    //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                    ko.cleanNode(document.getElementById("editSingleModal"));
                });
            }else {
                $("#editMultiModal").modal().on("shown.bs.modal", function () {
                    //ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData));
                    var data = {
                        id: "",
                        name: "",
                        product: "",
                        group: "",
                        content: "",
                        status: "",
                    };
                    var html = "";
                    $.each(arrselectedData, function (index, item) { 
                        //循环获取数据
                        var name = arrselectedData[index];
                        //alert(name)
                        html_name = "<tr><td>"+name.id+"</td><td>"+name.name+"</td><td>"+name.product+"</td><td>"+name.group+"</td><td>"+name.status+"</td><td>"+name.content+"</td></tr>";
                        html = html + html_name
                        data['name'] = data['name'] + name.name + "\n";
                    }); 
                    $("#UpdateDatas").html(html);
                    //console.log(data)

                    document.getElementById("txt_edit2_group").innerHTML="<option value selected>所属组[默认不修改]</option>" + data_all['group'];
                    document.getElementById("txt_edit2_product").innerHTML="<option value selected>所属产品[默认不修改]</option>" + data_all['product'];
                    ko.utils.extend(operate.DepartmentModel, data);
                    ko.applyBindings(operate.DepartmentModel, document.getElementById("editMultiModal"));
                    
                    $('#btn_update2_submit').on("click", function () {
                        operate.operateSave('Update');
                    });
                }).on('hidden.bs.modal', function () {
                    //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                    ko.cleanNode(document.getElementById("editMultiModal"));
                });
            }
        });
    },

    ViewModel: function() {
                var self = this;
                self.datas = ko.observableArray();
    },

    operateconfirmDelete: function () {
        $('#btn_confirm_delete').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (arrselectedData.length <= 0){
                alert("请至少选择一行数据");
                return false;
            }
            var vm = new operate.ViewModel();
            for (var i=0;i<arrselectedData.length;i++){
                //ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[i]));
                //vm.datas.push(operate.DepartmentModel);
                vm.datas.push(ko.mapping.fromJS(arrselectedData[i]));
            }
            $("#confirmDeleteModal").modal().on("shown.bs.modal", function () {
                //ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData));
                //ko.applyBindings(operate.DepartmentModel, document.getElementById("confirmDeleteModal"));
                ko.applyBindings(vm, document.getElementById("confirmDeleteModal"));
                //datas = ko.mapping.fromJS(arrselectedData)
                var html = "";
                $.each(vm.datas(), function (index, item) { 
                    //循环获取数据
                    var name = vm.datas()[index];
                    //alert(name)
                    html_name = "<tr><td>"+name.id()+"</td><td>"+name.name()+"</td><td>"+name.product()+"</td><td>"+name.group()+"</td><td>"+name.status()+"</td><td>"+name.content()+"</td></tr>";
                    html = html + html_name
                }); 
                $("#DeleteDatas").html(html);
                operate.operateDelete();
                //vm.datas.valueHasMutated();
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("confirmDeleteModal"));
            });
        });
    },

    //删除
    operateDelete: function () {
        $('#btn_delete').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            $.ajax({
                url: "/monitor/domains/Delete",
                type: "post",
                contentType: 'application/json',
                data: JSON.stringify(arrselectedData),
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
    //保存数据
    operateSave: function (funcName) {
        //toastr.info("Welcome World!1");
        //将Viewmodel转换为数据model
        var data = ko.toJS(operate.DepartmentModel);
        data['name'] = data['name'].split('\n');
        for(var i = 0; i < data['name'].length; i++) { 
            if(data['name'][i].replace(/ /g, '') === ''){
                data['name'].splice(i, 1);
            }else if (! operate.isDomain(data['name'][i])) {
                alert(data['name'][i] + "格式不正确！");
                return false;
            }
        }
        data['all'] = tableInit.myViewModel.getSelections();
        if (data['name'].length !== data['all'].length){
            alert("需要修改的域名数量不正确，请检查！");
            return false;
        }

        toastr.info("请求发送中，请耐心等待返回...");
        //var funcName = oDataModel.id?"Update":"Add";
        $.ajax({
            url: "/monitor/domains/"+funcName,
            type: "post",
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function (data, status) {
                toastr.success(data);
                tableInit.myViewModel.refresh();
                return true;
            },
            error:function(XMLHttpRequest, textStatus, errorThrown){
                if (XMLHttpRequest.status == 0){
                    toastr.error('后端服务不响应', '错误')
                    return false;
                }else {
                    toastr.error(XMLHttpRequest.responseText, XMLHttpRequest.status)
                    return false;
                }
                //alert("失败，请检查日志！");
                //tableInit.myViewModel.refresh();
            }
        });
    },
    //数据校验
    operateCheck:function(arr){
        if (arr.length <= 0) {
            alert("请至少选择一行数据");
            return false;
        }
        //if (arr.length > 1) {
        //    alert("只能编辑一行数据");
        //    return false;
        //}
        return true;
    }
}