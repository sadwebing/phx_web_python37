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
            //url: '/servers/get_servers_records',         //请求后台的URL（*）
            //method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            clickToSelect: true,
            height:830,
            toolbarAlign: "right",
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset, 'act':'query_all' };
            },//传递参数（*）
            columns: [
                {
                    checkbox: true,
                    width:'2%',
                },{
                    field: 'id',
                    title: 'id',
                    sortable: true,
                    formatter: function (value, row, index) {
                        row.id = index+1;
                        return index+1;
                    },
                    visible: false,
                    //width:'8%',
                    //align: 'center'
                },{
                    field: 'envir',
                    title: 'envir',
                    sortable: true,
                    formatter: function (value, row, index) {
                        return value[1];
                    },
                    //width:'8%',
                    //align: 'center'
                },{
                    field: 'product',
                    title: 'product',
                    sortable: true,
                    formatter: function (value, row, index) {
                        return value[1];
                    },
                    //width:'15%',
                    //align: 'center'
                },{
                    field: 'project',
                    title: 'project',
                    sortable: true,
                    formatter: function (value, row, index) {
                        return value[1];
                    },
                    //width:'15%',
                    //align: 'center'
                },{
                    field: 'customer',
                    title: 'customer',
                    sortable: true,
                    formatter: function (value, row, index) {
                        return value[1];
                    },
                    //width:'15%',
                    //align: 'center'
                },{
                    field: 'server_type',
                    title: 'server_type',
                    sortable: true,
                    formatter: function (value, row, index) {
                        return value[1];
                    },
                    //width:'5%',
                    //align: 'center'
                },{
                    field: 'minion_id',
                    title: 'minion_id',
                    sortable: true,
                    //width:'15%',
                    //align: 'center'
                },{
                    field: 'system',
                    title: 'system',
                    sortable: true,
                    visible: false,
                    //width:'15%',
                    //align: 'center'
                },{
                    field: 'ip',
                    title: 'ip',
                    sortable: true,
                    formatter: function (value, row, index) {
                        return row.ip.join('<br>');
                    },
                    //events: operateStatusEvents,
                    //formatter: this.operateStatusFormatter,
                    //width:'auto',
                    //align: 'center'
                },{
                    field: 'service_type',
                    title: 'service_type',
                    sortable: true,
                    //width:'auto',
                    //align: 'center'
                },{
                    field: 'user',
                    title: 'user',
                    sortable: true,
                    //width:'auto',
                    //align: 'center'
                },{
                    field: 'port',
                    title: 'port',
                    sortable: true,
                    //width:'auto',
                    //align: 'center'
                },{
                    field: 'password',
                    title: 'password',
                    sortable: true,
                    //events: operateStatusEvents,
                    //formatter: this.operateStatusFormatter,
                    //width:'auto',
                    //align: 'center'
                },{
                    field: 'price',
                    title: 'price',
                    sortable: true,
                    //width:'5%',
                    //align: 'center'
                },{
                    field: 'provider',
                    title: 'provider',
                    sortable: true,
                    //width:'5%',
                    //align: 'center'
                },{
                    field: 'info',
                    title: 'info',
                    sortable: true,
                    //events: operateStatusEvents,
                    //formatter: this.operateStatusFormatter,
                    //width:'auto',
                    //align: 'center'
                },{
                    field: 'operations',
                    title: '操作项',
                    //align: 'center',
                    width:'6%',
                    checkbox: false,
                    //events: operateEvents,
                    formatter: this.operateFormatter,
                    //width:300,
                },
            ]

        });
        //console.log(this.myViewModel)
        //this.myViewModel.hidecolumn('zone_id');
        ko.applyBindings(this.myViewModel, document.getElementById("records_table"));
        //部分列进行隐藏
        $('#records_table').bootstrapTable('hideColumn', 'operations');
    },

    dbclick: function (){
        $('#records_table').on('all.bs.table', function (e, name, args) {
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
        '<a class="check_server" href="javascript:void(0)" title="删除记录">',
        '<i class="text-primary"> 删除</i>',
        '</a>'
        ].join('');   
        return content;
    },
};


//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        //console.log(tableInit.myViewModel);
        //console.log(tableInit.myViewModel.getData());
        //tableInit.myViewModel.hidecolumn('zone_id');
        //tableInit.myViewModel.hidecolumn('record_id');
        //this.operateCheckStatus();
        this.operateEdit();
        //this.operateCommitEdit();
    },

    //修改zone记录
    operateEdit: function () {
        $('#btn_edit').on("click", function () {
            $("#progress_bar_update_record").css("width", "0%");
            document.getElementById('update_record_finished_count').innerHTML="finished: 0  &emsp;  success: 0  &emsp;  failed: 0";
            document.getElementById('password').value = "";
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (arrselectedData.length <= 0){
                alert("请至少选择一行数据");
                return false;
            }

            var vm = new public.ViewModel();
            for (var i=0;i<arrselectedData.length;i++){
                vm.datas.push(ko.mapping.fromJS(arrselectedData[i]));
            }
            $("#confirmEditModal").modal().on("shown.bs.modal", function () {
                //ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData));
                //ko.applyBindings(operate.DepartmentModel, document.getElementById("confirmEditModal"));
                window.buttons = ['btn_close_edit', 'btn_commit_edit'];
                public.socketConn('/servers/update', window.buttons)
                public.disableButtons(window.buttons, false);

                ko.applyBindings(vm, document.getElementById("confirmEditModal"));
                //datas = ko.mapping.fromJS(arrselectedData)
                var html = "";
                $.each(vm.datas(), function (index, item) { 
                    //循环获取数据
                    var record = vm.datas()[index];
                    //alert(record)
                    html_record = "<tr id="+record.minion_id()+"><td>"+record.product()[1]+"</td><td>"+record.project()[1]+"</td><td>"+record.customer()[1]+"</td><td>"+record.server_type()[1]+"</td><td>"+record.minion_id()+"</td></tr>";
                    html = html + html_record
                }); 
                $("#EditDatas").html(html);
                operate.operateCommitEdit();
                //vm.datas.valueHasMutated();
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("confirmEditModal"));
                if (window.s) {
                    window.s.close();
                }
            });
        });
    },

    operateCommitEdit: function () {
        $('#btn_commit_edit').on("click", function () {
            $("#progress_bar_update_record").css("width", "0%");
            document.getElementById('update_record_finished_count').innerHTML="finished: 0  &emsp;  success: 0  &emsp;  failed: 0";
            public.disableButtons(window.buttons, true);
            var arrselectedData = tableInit.myViewModel.getSelections();
            var postdata = {};

            postdata['password'] = document.getElementById('password').value.replace(/(^\s*)|(\s*$)/g, "");
            if (postdata['password'].length < 6){
                alert('password is too short.');
                public.disableButtons(window.buttons, false);
                return false;
            }

            postdata['records'] = arrselectedData;
            count = postdata['records'].length;
            success = 0;
            failed = 0;

            if (window.s.readyState == 1) {
                window.s.send(JSON.stringify(postdata));
            }else {
                toastr.error('socket 未连接成功，请重新打开！', '错误');
                public.disableButtons(window.buttons, false);
                return false;
            }

            window.s.onmessage = function (e) {

                data = eval('('+ e.data +')');

                if (! data.permission){
                    toastr.error('抱歉，您没有修改['+data.record.minion_id+']权限！', '错误');
                }

                var width = 100*(data.step)/count + "%";
                if (data.result){
                    success = success + 1;
                    document.getElementById(data.record.minion_id).style.backgroundColor = "white";
                    $('#textarea_edit_result').append("<p>"+data.record.minion_id+": 密码修改成功</p>");
                }else {
                    failed = failed + 1;
                    document.getElementById(data.record.minion_id).style.backgroundColor = "red";
                    $('#textarea_edit_result').append("<p>"+data.record.minion_id+": <strong>密码修改失败</strong></p>");
                    $('#textarea_edit_result').append("<p>"+data.info+"</p>");
                }
                document.getElementById('update_record_finished_count').innerHTML="finished: "+data.step+"  &emsp;  success: "+success+"  &emsp;  failed: "+failed+"";
                $("#progress_bar_update_record").css("width", width);
                if (data.step == count){
                    window.s.close();
                    public.disableButtons(window.buttons, false);
                }
            };
            return false;
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