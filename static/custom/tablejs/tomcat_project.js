$(function () {
    tableInit.Init();
    operate.operateInit();
});
//初始化表格
var tableInit = {
    Init: function () {
        this.dbclick();
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/tomcat/tomcat_project/Query',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset, 'act':'query_all'};
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
                    width:'1%',
                    //align: 'center'
                },{
                    field: 'product',
                    title: '产品',
                    sortable: true,
                    width:'6%',
                    //align: 'center'
                }, {
                    field: 'project',
                    title: '项目名',
                    sortable: true,
                    //align: 'center',
                    width:'18%',
                },{
                    field: 'server_type',
                    title: '服务类型',
                    sortable: true,
                    //align: 'center',
                    width:'5%',
                }, {
                    field: 'code_dir',
                    title: '代码目录',
                    sortable: true,
                    width:'8%',
                    //align: 'center'
                },{
                    field: 'tomcat',
                    title: 'tomcat',
                    sortable: true,
                    width:'20%',
                    //align: 'center',
                    //events: this.cur_statusEvents,
                    formatter: this.cur_statusFormatter
                },{
                    field: 'tomcat_version',
                    title: 'T版本',
                    sortable: true,
                    //align: 'center',
                    width:'3%',
                },{
                    field: 'main_port',
                    title: '服务端口',
                    sortable: true,
                    width:'5%',
                    //align: 'center'
                },{
                    field: 'jdk',
                    title: 'jdk',
                    sortable: true,
                    width:'5%',
                    //align: 'center'
                },{
                    field: 'script',
                    title: '重启脚本',
                    sortable: true,
                    //align: 'center',
                    width:'15%',
                    checkbox: false,
                },{
                    field: 'status_',
                    title: '状态',
                    sortable: true,
                    width:'5%',
                    events: operateEvents,
                    formatter: this.operateFormatter,
                    //align: 'center'
                },
            ]
        });
        ko.applyBindings(this.myViewModel, document.getElementById("project_table"));
    },

    dbclick: function (){
        $('#project_table').on('all.bs.table', function (e, name, args) {
            //console.log('Event:', name, ', data:', args);
        }).on('dbl-click-cell.bs.table', function (e, field, value, row, $element) {
            //console.log(row)
            //return false;
            $("#mytomcatproductModal").modal().on("shown.bs.modal", function () {
                //将选中该行数据有数据Model通过Mapping组件转换为viewmodel
                ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(row));
                ko.applyBindings(operate.DepartmentModel, document.getElementById("mytomcatproductModal"));
                operate.operateSave('Update');
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("mytomcatproductModal"));
            });

        });
    },

    operateFormatter: function (value,row,index){
        if (row.status_ == 'active'){
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id='+ row.id +' class="update_status" checked><span></span>',
                '</label>',
            '</div>'
            ].join('');
        }else {
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id='+ row.id +' class="update_status"><span></span>',
                '</label>',
            '</div>'
            ].join('');
        }
        return content;
    },
};

window.operateEvents = {
    'click .update_status': function (e, value, row, index) {
        var postData = {
            id:row.id,
            status,
        };
        if (document.getElementById(row.id).checked){
            postData.status = 'active';
            //console.log(postData);
        }else {
            postData.status = 'inactive';
            //console.log(postData);
        }
        $.ajax({
            url: "/tomcat/tomcat_project/UpdateStatus",
            type: "post",
            data: JSON.stringify(postData),
            success: function (data, status) {
                toastr.success('状态更新成功！', row.product+": "+row.project)
                //alert(data);
                //tableInit.myViewModel.refresh();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                if (postData.status == 'active'){
                    document.getElementById(row.id).checked = false;
                }else {
                    document.getElementById(row.id).checked = true;
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
        this.operateAdd();
        this.operateUpdate();
        this.operateconfirmDelete();
        this.operateTomcatProjectSelect();
        //this.operateDelete();
        this.DepartmentModel = {
            id: ko.observable(),
            product: ko.observable(),
            project: ko.observable(),
            server_type: ko.observable(),
            code_dir: ko.observable(),
            tomcat: ko.observable(),
            tomcat_version: ko.observable(),
            main_port: ko.observable(),
            jdk: ko.observable(),
            script: ko.observable(),
            status_: ko.observable(),
        };
    },

    operateTomcatProjectSelect: function(){
        $('#tomcat_project_active').on("click", function () {
            document.getElementById('tomcat_project_active').disabled = true;
            document.getElementById('tomcat_project_inactive').disabled = false;
            document.getElementById('tomcat_project_all').disabled = false;
            var params = {
                url: '/tomcat/tomcat_project/Query',
                method: 'post',
                singleSelect: false,
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 'act':'query_active' };
                },
            }
            tableInit.myViewModel.refresh(params);
        });
        $('#tomcat_project_inactive').on("click", function () {
            document.getElementById('tomcat_project_active').disabled = false;
            document.getElementById('tomcat_project_inactive').disabled = true;
            document.getElementById('tomcat_project_all').disabled = false;
            var params = {
                url: '/tomcat/tomcat_project/Query',
                method: 'post',
                singleSelect: false,                                                
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 'act':'query_inactive' };
                },
            }
            tableInit.myViewModel.refresh(params);
        });
        $('#tomcat_project_all').on("click", function () {
            document.getElementById('tomcat_project_active').disabled = false;
            document.getElementById('tomcat_project_inactive').disabled = false;
            document.getElementById('tomcat_project_all').disabled = true;
            var params = {
                url: '/tomcat/tomcat_project/Query',
                method: 'post',
                singleSelect: false,
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 'act':'query_all' };
                },
            }
            tableInit.myViewModel.refresh(params);
        });
    },


    //新增
    operateAdd: function(){
        $('#btn_add').on("click", function () {
            $("#mytomcatproductModal").modal().on("shown.bs.modal", function () {
                var oEmptyModel = {
                   id: ko.observable(),
                   product: ko.observable(),
                   project: ko.observable(),
                   server_type: ko.observable(),
                   code_dir: ko.observable(),
                   tomcat: ko.observable(),
                   tomcat_version: ko.observable(),
                   main_port: ko.observable(),
                   jdk: ko.observable(),
                   script: ko.observable(),
                   status_: ko.observable(),
                };
                ko.utils.extend(operate.DepartmentModel, oEmptyModel);
                ko.applyBindings(operate.DepartmentModel, document.getElementById("mytomcatproductModal"));
                operate.operateSave('Add');
            }).on('hidden.bs.modal', function () {
                ko.cleanNode(document.getElementById("mytomcatproductModal"));
            });
        });
    },
    //编辑
    operateUpdate: function () {
        $('#btn_edit').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (!operate.operateCheck(arrselectedData)) { return; }
            $("#mytomcatproductModal").modal().on("shown.bs.modal", function () {
                //将选中该行数据有数据Model通过Mapping组件转换为viewmodel
                ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[0]));
                ko.applyBindings(operate.DepartmentModel, document.getElementById("mytomcatproductModal"));
                operate.operateSave('Update');
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("mytomcatproductModal"));
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
                //ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[0]));
                ko.applyBindings(vm, document.getElementById("confirmDeleteModal"));
                var html = "";
                $.each(vm.datas(), function (index, item) { 
                    //循环获取数据 
                    var name = vm.datas()[index];
                    html_name = "<tr><td>"+name.id()+"</td><td>"+name.product()+"</td><td>"+name.project()+"</td><td>"+name.server_type()+"</td><td>"+name.code_dir()+"</td><td>"+name.tomcat()+"</td><td>"+name.tomcat_version()+"</td><td>"+name.main_port()+"</td><td>"+name.jdk()+"</td><td>"+name.script()+"</td><td>"+name.status_()+"</td></tr>";
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
                url: "/tomcat/tomcat_project/Delete",
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
                    //tableInit.myViewModel.refresh();
                }
            });
        });
    },


    //保存数据
    operateSave: function (funcName) {
        $('#btn_submit').on("click", function () {
            //取到当前的viewmodel
            var oViewModel = operate.DepartmentModel;
            //var jdkarray = ko.observableArray(['jdk1.6', 'jdk1.7', 'jdk1.8']);
            var jdkarray = new Array('jdk1.6', 'jdk1.7', 'jdk1.8');
            if (!oViewModel.product()){
                alert("产品 不能为空!");
                return false;
            }
            if (!oViewModel.project()){
                alert("项目名 不能为空!");
                return false;
            }
            if (!oViewModel.code_dir()){
                alert("代码目录 不能为空!");
                return false;
            }
            //if (!oViewModel.cur_svn_id()){
            //    alert("当前版本 不能为空!");
            //    return false;
            //}
            if (!oViewModel.tomcat()){
                oViewModel.tomcat('')
            }
            if (!oViewModel.main_port()){
                oViewModel.main_port('')
            }
            if (!oViewModel.jdk()){
                oViewModel.jdk('')
            }
            else if(!operate.contains(oViewModel.jdk(), jdkarray)){
                alert("jdk 版本不正确!");
                return false;
            }
            if (!oViewModel.script()){
                oViewModel.script('')
            }
            if (!oViewModel.status_()){
                oViewModel.status_('')
            }
            //将Viewmodel转换为数据model
            var oDataModel = ko.toJS(oViewModel);
            //var funcName = oDataModel.id?"Update":"Add";
            $.ajax({
                url: "/tomcat/tomcat_project/"+funcName,
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
                    //tableInit.myViewModel.refresh();
                }
            });
        });
    },
    contains:function(obj, arr) {
        var i = arr.length;
        while (i--) {
            if (arr[i] === obj) {
            return true;
            }
        }
        return false;
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