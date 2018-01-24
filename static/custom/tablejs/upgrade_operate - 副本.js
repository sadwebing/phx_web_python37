$(function () {
    tableInit.Init();
    operate.operateInit();
});



var tableInit = {
    Init: function () {
        this.Events;
        this.operateFormatter;
        this.cur_statusFormatter;
        //this.cur_statusEvents;
        $('#upgrade_op_table').bootstrapTable({
            url: '/upgrade/query_svn',   //请求后台的URL（*） 
            method: 'post',      //请求方式（*） 
            toolbar: '#toolbar',    //工具按钮用哪个容器 
            striped: false,      //是否显示行间隔色 
            cache: false,      //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*） 
            pagination: true,     //是否显示分页（*） 
            //sortable: false,      //是否启用排序 
            sortOrder: "asc",     //排序方式 
            queryParams: function (params) {
                return { limit: params.limit, offset: params.offset, 'act':'query_all' };
            },//传递参数（*） 
            sidePagination: "server",   //分页方式：client客户端分页，server服务端分页（*） 
            pageNumber:1,      //初始化加载第一页，默认第一页 
            pageSize: 10,      //每页的记录行数（*） 
            pageList: [5, 10, 25, 50, 100, 'ALL'],  //可供选择的每页的行数（*） 
            search: true,      //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大 
            strictSearch: false, 
            showColumns: true,     //是否显示所有的列 
            showRefresh: true,     //是否显示刷新按钮 
            //showPaginationSwitch: true,
            //showFooter:true,
            minimumCountColumns: 2,    //最少允许的列数 
            clickToSelect: true,    //是否启用点击选中行 
            //height: 500,      //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度 
            uniqueId: "id",      //每一行的唯一标识，一般为主键列 
            showToggle:true,     //是否显示详细视图和列表视图的切换按钮 
            //cardView: true,     //是否显示详细视图 
            detailView: false,     //是否显示父子表 
            //height: getHeight(),
            toolbarAlign: "left",
            columns: [
                //{ 
                //    checkbox: true 
                //},
                {
                    field: 'id',
                    title: 'id',
                    sortable: true,
                    width:'3%',
                    //align: 'center'
                },{
                    field: 'svn_id',
                    title: '版本',
                    sortable: true,
                    width:'6%',
                    //align: 'center'
                }, {
                    field: 'id_time',
                    title: '版本时间',
                    sortable: true,
                    //align: 'center',
                    width:'9%',
                }, {
                    field: 'project',
                    title: '项目名',
                    sortable: true,
                    width:'18%',
                    //align: 'center'
                },{
                    field: 'cur_svn_id',
                    title: '当前版本',
                    sortable: true,
                    width:'6%',
                    //align: 'center'
                }, {
                    field: 'cur_status',
                    title: '状态',
                    sortable: true,
                    width:'6%',
                    //align: 'center',
                    //events: this.cur_statusEvents,
                    formatter: this.cur_statusFormatter
                },{
                    field: 'op_time',
                    title: '操作时间',
                    sortable: true,
                    //align: 'center',
                    width:'9%',
                },{
                    field: 'handle_user',
                    title: '操作人',
                    sortable: true,
                    width:'6%',
                    //align: 'center'
                },{
                    field: 'id',
                    title: '操作项',
                    //align: 'center',
                    width:'18%',
                    events: operateEvents,
                    formatter: this.operateFormatter,
                    //width:300,
                },
            ]
        });
    },

    operateFormatter: function (value,row,index){
        return [
            '<a class="upgrade" href="javascript:void(0)" title="升级">',
            '<i class="glyphicon glyphicon-hand-up"> &ensp; </i>',
            '</a> ',
            '<a class="diff" href="javascript:void(0)" title="比对代码">',
            '<i class="glyphicon glyphicon-align-center"> &ensp; </i>',
            '</a>',
        ].join('');
        //if (row.cur_status == 'rollback'){
        //    content = content + [
        //    '<a class="rollback" href="javascript:void(0)" title="回退[禁用]" disabled="disabled">',
        //    '<i class="glyphicon glyphicon-hand-down"></i>',
        //    '</a>'
        //    ].join('');
        //}else {
        //    content = content + [
        //    '<a class="rollback" href="javascript:void(0)" title="回退">',
        //    '<i class="glyphicon glyphicon-hand-down"></i>',
        //    '</a>'
        //    ].join('');   
        //}

        //return content;
    },

    cur_statusFormatter: function (value,row,index) {
        var status = row.cur_status;
        if (status == 'undone'){
            content = '<span style="background-color: grey">未升级</span>';
            return content;
        }else if(status == 'done'){
            return "已升级";
        }else if(status == 'rollback'){
            content = '<span style="background-color: #FF6347">已回滚</span>';
            return content;
        }else {
            return "未定义";
        }
    },
};

window.operateEvents = {
    'click .upgrade': function (e, value, row, index) {
        console.log('click upgrade.')
        alert(row.project);
        return false;
    },
    'click .diff': function (e, value, row, index) {
        console.log('click diff.')
        alert(row.project);
        return false;
    },
    'click .rollback': function (e, value, row, index) {
        console.log('click rollback.')
        alert(row.project);
        return false;
    }
};  

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.operateAdd();
        this.operateUpdate();
        this.selectpicker();
        this.operateconfirmDelete();
        this.operateTomcatUrlSelect();
        this.GetProject();
        //this.operateDelete();
        this.DepartmentModel = {
            id: ko.observable(),
            project: ko.observable(),
            server_ip: ko.observable(),
            server_type: ko.observable(),
            role: ko.observable(),
            domain: ko.observable(),
            url: ko.observable(),
            status_: ko.observable(),
            info: ko.observable(),
        };
    },

    operateTomcatUrlSelect: function(){
        $('#tomcat_url_active').on("click", function () {
            document.getElementById('tomcat_url_active').disabled = true;
            document.getElementById('tomcat_url_inactive').disabled = false;
            document.getElementById('tomcat_url_all').disabled = false;
            var params = {
                url: '/tomcat/tomcat_url/Query',
                method: 'post',
                singleSelect: false,
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 'act':'query_active' };
                },
            }
            tableInit.myViewModel.refresh(params);
        });
        $('#tomcat_url_inactive').on("click", function () {
            document.getElementById('tomcat_url_active').disabled = false;
            document.getElementById('tomcat_url_inactive').disabled = true;
            document.getElementById('tomcat_url_all').disabled = false;
            var params = {
                url: '/tomcat/tomcat_url/Query',
                method: 'post',
                singleSelect: false,                                                
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 'act':'query_inactive' };
                },
            }
            tableInit.myViewModel.refresh(params);
        });
        $('#tomcat_url_all').on("click", function () {
            document.getElementById('tomcat_url_active').disabled = false;
            document.getElementById('tomcat_url_inactive').disabled = false;
            document.getElementById('tomcat_url_all').disabled = true;
            var params = {
                url: '/tomcat/tomcat_url/Query',
                method: 'post',
                singleSelect: false,
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 'act':'query_all' };
                },
            }
            tableInit.myViewModel.refresh(params);
        });
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
                var html_B79 = "";
                var html_P02 = "";
                var html_E02 = "";
                var html_NWF = "";
                var html_PUBLIC = "";
                $.each(data, function (index, item) { 
                    //循环获取数据 
                    var name = data[index];
                    //console.log(data)
                    //html_name = "<option>"+name+"</option>";
                    if (name.product === 'B79') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_B79 = html_B79 + html_name
                    }else if (name.product === 'P02') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_P02 = html_P02 + html_name
                    }else if (name.product === 'E02') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_E02 = html_E02 + html_name
                    }else if (name.product === 'NWF') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_NWF = html_NWF + html_name
                    }else if (name.product === 'PUBLIC') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_PUBLIC = html_PUBLIC + html_name
                    }
                }); 
                //$("#project").html(html);
                //$("#project_active").html(html);
                var html = "<optgroup label='B79'>" + html_B79 + "</optgroup>" + "<optgroup label='P02'>" + html_P02 + "</optgroup>" + "<optgroup label='E02'>" + html_E02 + "</optgroup>" + "<optgroup label='NWF'>" + html_NWF + "</optgroup>" + "<optgroup label='PUBLIC'>" + html_PUBLIC + "</optgroup>"
                document.getElementById('project_active').innerHTML=html;
                $('.selectpicker').selectpicker('refresh');
                return false;
            },
            error:function(msg){
                alert("获取项目失败！");
                return false;
            }
        });
    },

    //新增
    operateAdd: function(){
        $('#btn_add').on("click", function () {
            $("#myModal").modal().on("shown.bs.modal", function () {
                var oEmptyModel = {
                    project: ko.observable(),
                    server_ip: ko.observable(),
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
                var arrselectedData = tableInit.myViewModel.getSelections();
                if (!operate.operateCheck(arrselectedData)) { return; }
                //将选中该行数据有数据Model通过Mapping组件转换为viewmodel
                ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[0]));
                ko.applyBindings(operate.DepartmentModel, document.getElementById("myModal"));
                operate.operateSave('Update');
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("myModal"));
            });
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
                    html_name = "<tr><td>"+name.id()+"</td><td>"+name.project()+"</td><td>"+name.server_ip()+"</td><td>"+name.server_type()+"</td><td>"+name.role()+"</td><td>"+name.domain()+"</td><td>"+name.url()+"</td><td>"+name.status_()+"</td><td>"+name.info()+"</td></tr>";
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
                url: "/tomcat/tomcat_url/Delete",
                type: "post",
                contentType: 'application/json',
                data: JSON.stringify(arrselectedData),
                success: function (data, status) {
                    alert(data);
                    tableInit.myViewModel.refresh();
                },
                error:function(msg){
                    alert("失败，请检查日志！");
                    tableInit.myViewModel.refresh();
                }
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
            if (! oViewModel.server_ip()){
                alert('服务器地址 不能为空！')
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
                url: "/tomcat/tomcat_url/"+funcName,
                type: "post",
                data: oDataModel,
                success: function (data, status) {
                    alert(data);
                    tableInit.myViewModel.refresh();
                },
                error:function(msg){
                    alert("失败，请检查日志！");
                    tableInit.myViewModel.refresh();
                }
            });
        });
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