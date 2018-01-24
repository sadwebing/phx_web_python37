$(function () {
    tableInit.Init();
    operate.operateInit();
});

//初始化表格
var tableInit = {
    Init: function () {
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/tomcat/project_servers/act',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',        //工具按钮用哪个容器     
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset, 'act': 'query'};
            },//传递参数（*）
        });
        ko.applyBindings(this.myViewModel, document.getElementById("project_servers"));
    }
};

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.operateAdd();
        this.operateUpdate();
        this.operateconfirmDelete();
        //this.operateDelete();
        this.DepartmentModel = {
            id: ko.observable(),
            project: ko.observable(),
            domain: ko.observable(),
            url: ko.observable(),
            status_: ko.observable(),
        };
    },
    //新增
    operateAdd: function(){
        $('#btn_add').on("click", function () {
            $("#myModal").modal().on("shown.bs.modal", function () {
                var oEmptyModel = {
                    id: ko.observable(),
                    project: ko.observable(),
                    domain: ko.observable(),
                    url: ko.observable(),
                    status_: ko.observable(),
                };
                ko.utils.extend(operate.DepartmentModel, oEmptyModel);
                ko.applyBindings(operate.DepartmentModel, document.getElementById("myModal"));
                operate.operateSave();
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
                operate.operateSave();
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
                    html_name = "<tr><td>"+name.id()+"</td><td>"+name.project()+"</td><td>"+name.domain()+"</td><td>"+name.url()+"</td><td>"+name.status_()+"</td></tr>";
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
    operateSave: function () {
        $('#btn_submit').on("click", function () {
            //取到当前的viewmodel
            var oViewModel = operate.DepartmentModel;
            //将Viewmodel转换为数据model
            var oDataModel = ko.toJS(oViewModel);var funcName = oDataModel.id?"Update":"Add";
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