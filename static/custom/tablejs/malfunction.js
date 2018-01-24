$(function () {
    operate.operateInit();
});

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.operateAdd();
        this.operateconfirmDelete();
        this.csoperateUpdate();
        this.saoperateUpdate();
        this.form_datetime();
        //this.set_time_all();
        //this.operateSave();
        this.DepartmentModel = {
            id: ko.observable(),
            record_time: ko.observable(),
            mal_details: ko.observable(),
            record_user: ko.observable(),
            mal_reasons: ko.observable(),
            mal_status: ko.observable(),
            recovery_time: ko.observable(),
            time_all: ko.observable(),
            handle_user: ko.observable(),
        };
    },
    //新增
    operateAdd: function(){
        $('#btn_add').on("click", function () {
            $("#csAddModal").modal().on("shown.bs.modal", function () {
                var oEmptyModel = {
                    id: ko.observable(),
                    record_time: ko.observable(),
                    mal_details: ko.observable(),
                    record_user: ko.observable(),
                };
                ko.utils.extend(operate.DepartmentModel, oEmptyModel);
                ko.applyBindings(operate.DepartmentModel, document.getElementById("csAddModal"));
                operate.form_datetime();
                operate.operatecsadd();
            }).on('hidden.bs.modal', function () {
                ko.cleanNode(document.getElementById("csAddModal"));
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
                    html_name = "<tr><td>"+name.id()+"</td><td>"+name.record_time()+"</td><td>"+name.mal_details()+"</td><td>"+name.record_user()+"</td><td>"+name.mal_reasons()+"</td><td>"+name.mal_status()+"</td><td>"+name.recovery_time()+"</td><td>"+name.time_all()+"</td></td><td>"+name.handle_user()+"</td></tr>";
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
                url: "/malfunction/Delete",
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

    //编辑
    csoperateUpdate: function () {
        $('#btn_cs_edit').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (!operate.operateCheck(arrselectedData)) { return; }
            $("#csEditModal").modal().on("shown.bs.modal", function () {
                var arrselectedData = tableInit.myViewModel.getSelections();
                if (!operate.operateCheck(arrselectedData)) { return; }
                //将选中该行数据有数据Model通过Mapping组件转换为viewmodel
                ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[0]));
                ko.applyBindings(operate.DepartmentModel, document.getElementById("csEditModal"));
                operate.form_datetime();
                operate.operatecssubmit();
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("csEditModal"));
            });
        });
    },

    saoperateUpdate: function () {
        $('#btn_sa_edit').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (!operate.operateCheck(arrselectedData)) { return; }
            $("#saEditModal").modal().on("shown.bs.modal", function () {
                var arrselectedData = tableInit.myViewModel.getSelections();
                if (!operate.operateCheck(arrselectedData)) { return; }
                //将选中该行数据有数据Model通过Mapping组件转换为viewmodel
                ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[0]));
                ko.applyBindings(operate.DepartmentModel, document.getElementById("saEditModal"));
                //console.log(operate.DepartmentModel.record_time())
                operate.form_datetime();
                operate.operatesasubmit();
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("saEditModal"));
            });
        });
    },

    GetDateDiff: function (startTime, endTime, diffType) {
        //将xxxx-xx-xx的时间格式，转换为 xxxx/xx/xx的格式
        startTime = startTime.replace(/\-/g, "/");
        endTime = endTime.replace(/\-/g, "/");
    
        //将计算间隔类性字符转换为小写
        diffType = diffType.toLowerCase();
        var sTime =new Date(startTime); //开始时间
        var eTime =new Date(endTime); //结束时间
        //作为除数的数字
        var divNum =1;
        switch (diffType) {
            case"second":
                divNum =1000;
            break;
            case"minute":
                divNum =1000*60;
            break;
            case"hour":
                divNum =1000*3600;
            break;
            case"day":
                divNum =1000*3600*24;
            break;
                default:
            break;
        }
        return parseInt((eTime.getTime() - sTime.getTime()) / parseInt(divNum));
    },

    //保存数据
    operatecsadd: function () {
        $('#btn_cs_add').on("click", function () {
            //取到当前的viewmodel
            var oViewModel = operate.DepartmentModel;
            //将Viewmodel转换为数据model
            var oDataModel = ko.toJS(oViewModel);
            //console.log(oDataModel)
            var funcName = oDataModel.id?"Update":"Add";
            $.ajax({
                url: "/malfunction/"+funcName,
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

    operatecssubmit: function () {
        $('#btn_cs_submit').on("click", function () {
            //取到当前的viewmodel
            var oViewModel = operate.DepartmentModel;
            //将Viewmodel转换为数据model
            var oDataModel = ko.toJS(oViewModel);
            //console.log(oDataModel)
            var funcName = oDataModel.id?"Update":"Add";
            $.ajax({
                url: "/malfunction/"+funcName,
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

    set_time_all: function(val1, val2) {
        //console.log('welcome!')
        time_all = operate.GetDateDiff(val1, val2, 'minute') + "分钟";
        //console.log(val1);
        //console.log(val2);
        //console.log(time_all);
        //$('#txt_time_all').val(time_all);
        operate.DepartmentModel.time_all=time_all;
        document.getElementById('txt_time_all').value=time_all;
    },

    form_datetime: function () {
        $(".form_datetime").datetimepicker({
            format: "yyyy-mm-dd hh:ii",
            autoclose: true,
            todayBtn: true,
            language:'zh-CN',
            minView: 0,
            maxView: 1,
            todayHighlight: 1,
            pickerPosition:"bottom-right"
        });
    },

    operatesasubmit: function () {
        $('#btn_sa_submit').on("click", function () {
            //取到当前的viewmodel
            tableInit.myViewModel.refresh();
            var oViewModel = operate.DepartmentModel;
            //将Viewmodel转换为数据model
            var oDataModel = ko.toJS(oViewModel);
            //alert(oDataModel.id)
            var funcName = oDataModel.id?"Update":"Add";
            $.ajax({
                url: "/malfunction/"+funcName,
                type: "post",
                data: oDataModel,
                success: function (data, status) {
                    //alert(data);
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