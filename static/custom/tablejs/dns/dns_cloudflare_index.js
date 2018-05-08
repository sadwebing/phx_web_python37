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
            //url: '/monitor/project/Query',         //请求后台的URL（*）
            //method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            clickToSelect: true,
            toolbarAlign: "right",
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset, 'act':'query_all' };
            },//传递参数（*）
            columns: [
                {
                    checkbox: true,
                    width:'2%',
                },{
                    field: 'product',
                    title: 'product',
                    sortable: true,
                    //width:'8%',
                    //align: 'center'
                },{
                    field: 'zone',
                    title: 'zone',
                    sortable: true,
                    //width:'15%',
                    //align: 'center'
                },{
                    field: 'name',
                    title: 'name',
                    sortable: true,
                    //width:'15%',
                    //align: 'center'
                },{
                    field: 'type',
                    title: 'type',
                    sortable: true,
                    //width:'5%',
                    //align: 'center'
                },{
                    field: 'content',
                    title: 'content',
                    sortable: true,
                    //width:'15%',
                    //align: 'center'
                },{
                    field: 'proxied',
                    title: 'proxied',
                    sortable: true,
                    //width:'auto',
                    //align: 'center'
                },{
                    field: 'record_id',
                    title: 'record_id',
                    sortable: true,
                    //width:'auto',
                    //align: 'center'
                },{
                    field: 'zone_id',
                    title: 'zone_id',
                    sortable: true,
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
        //this.myViewModel.hidecolumn('zone_id');
        ko.applyBindings(this.myViewModel, document.getElementById("records_table"));
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
        //tableInit.myViewModel.hidecolumn('zone_id');
        //this.operateCheckStatus();
        this.isIp();
        this.selectpicker();
        this.operateSearch();
        this.operateEdit();
        this.detectDns();
        //this.operateCommitEdit();
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

    detectDns: function () {
        $('#detect_dns').on("click", function () {
            
        });
    },


    isIp: function (value) {
        var regexp = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;
                 
        var valid = regexp.test(value);
        if(!valid){//首先必须是 xxx.xxx.xxx.xxx 类型的数字，如果不是，返回false
            return false;
        }
             
        return value.split('.').every(function(num){
            //切割开来，每个都做对比，可以为0，可以小于等于255，但是不可以0开头的俩位数
            //只要有一个不符合就返回false
            if(num.length > 1 && num.charAt(0) === '0'){
                //大于1位的，开头都不可以是‘0’
                return false;
            }else if(parseInt(num , 10) > 255){
                //大于255的不能通过
                return false;
            }
            return true;
        });
    },

    isDomain: function (value, proxied) {
        var regexp = /^.*[a-zA-Z0-9]+.*\.[a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$/;
        var regexp_tw = /^(tw|.*\.tw)\..*$/;

        var valid = regexp.test(value);
        if(!valid){
            return false;
        }

        if (proxied == 'false'){
            var valid_tw = regexp_tw.test(value);

            if(valid_tw){
                return false;
            }
        }


        return true;
    },

    //查询zone记录
    operateSearch: function () {
        $('#btn_op_search').on("click", function () {
            var zone_list = []
            
            //var project = document.getElementById("project_active").value;
            var objSelectzone = document.productform.zone_name; 
            for(var i = 0; i < objSelectzone.options.length; i++) { 
                if (objSelectzone.options[i].selected == true){
                    var tmp = {}
                    tmp['zone_id'] = objSelectzone.options[i].value.split('_')[0];
                    tmp['name'] = objSelectzone.options[i].text;
                    tmp['product'] = objSelectzone.options[i].value.split('_')[1];
                    zone_list.push(tmp);
                }
            }
            //console.log(zone_list);
            var params = {
                url: '/dns/cloudflare/get_zone_records',
                method: 'post',
                singleSelect: false,
                queryParams: function (param) {
                    return { limit: param.limit, offset: param.offset, 'postdata':zone_list };
                },
            }
            tableInit.myViewModel.refresh(params);

        });
    },

    ViewModel: function() {
                var self = this;
                self.datas = ko.observableArray();
    },

    //修改zone记录
    operateEdit: function () {
        $('#btn_edit').on("click", function () {
            $("#progress_bar_update_record").css("width", "0%");
            document.getElementById('update_record_finished_count').innerHTML="finished: 0  &emsp;  success: 0  &emsp;  failed: 0";
            document.getElementById('record_content').value = "";
            operate.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
            var arrselectedData = tableInit.myViewModel.getSelections();
            if (arrselectedData.length <= 0){
                alert("请至少选择一行数据");
                return false;
            }

            var options = document.getElementById('record_type').children;
            options[0].selected=true;

            var options = document.getElementById('record_proxied').children;
            options[0].selected=true;

            var vm = new operate.ViewModel();
            for (var i=0;i<arrselectedData.length;i++){
                //ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData[i]));
                //vm.datas.push(operate.DepartmentModel);
                vm.datas.push(ko.mapping.fromJS(arrselectedData[i]));
            }
            $("#confirmEditModal").modal().on("shown.bs.modal", function () {
                //ko.utils.extend(operate.DepartmentModel, ko.mapping.fromJS(arrselectedData));
                //ko.applyBindings(operate.DepartmentModel, document.getElementById("confirmEditModal"));
                ko.applyBindings(vm, document.getElementById("confirmEditModal"));
                //datas = ko.mapping.fromJS(arrselectedData)
                var html = "";
                $.each(vm.datas(), function (index, item) { 
                    //循环获取数据
                    var record = vm.datas()[index];
                    //alert(record)
                    html_record = "<tr id="+record.name()+"><td>"+record.product()+"</td><td>"+record.zone()+"</td><td>"+record.name()+"</td><td>"+record.type()+"</td><td>"+record.content()+"</td><td>"+record.proxied()+"</td></tr>";
                    html = html + html_record
                }); 
                $("#EditDatas").html(html);
                operate.operateCommitEdit();
                //vm.datas.valueHasMutated();
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("confirmEditModal"));
            });
        });
    },

    operateCommitEdit: function () {
        $('#btn_commit_edit').on("click", function () {
            $("#progress_bar_update_record").css("width", "0%");
            document.getElementById('update_record_finished_count').innerHTML="finished: 0  &emsp;  success: 0  &emsp;  failed: 0";
            operate.disableButtons(['btn_close_edit', 'btn_commit_edit'], true);
            var arrselectedData = tableInit.myViewModel.getSelections();
            var postdata = {};
            postdata['type'] = $("#record_type option:selected").val()
            if (! postdata['type']){
                alert('pls select the type!');
                operate.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
                return false;
            }
            postdata['proxied'] = $("#record_proxied option:selected").val()
            if (! postdata['proxied']){
                alert('pls select the proxied!');
                operate.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
                return false;
            }
            postdata['content'] = document.getElementById('record_content').value.replace(/(^\s*)|(\s*$)/g, "");
            if (! postdata['content']){
                alert('content can\'t be empty!');
                operate.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
                return false;
            }

            if (postdata['type'] == 'A') {
                if (! operate.isIp(postdata['content'])){
                    alert('Content for A record is invalid.');
                    operate.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
                    return false;
                }
            }else if (postdata['type'] == 'CNAME'){
                if (! operate.isDomain(postdata['content'], postdata['proxied'])){
                    alert('Content for CNAME record is invalid.');
                    operate.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
                    return false;
                }




            }

            postdata['records'] = arrselectedData;
            count = postdata['records'].length;
            success = 0;
            failed = 0;

            var socket = new WebSocket("ws://" + window.location.host + "/dns/cloudflare/update_records");
            socket.onopen = function () {
                //console.log('WebSocket open');//成功连接上Websocket
                socket.send(JSON.stringify(postdata));
            };
            //$('#runprogress').modal('show');
            socket.onerror = function (){
                toastr.error('后端服务不响应', '错误');
                operate.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
            };
            socket.onmessage = function (e) {
                data = eval('('+ e.data +')');
                var width = 100*(data.step)/count + "%";
                if (data.result){
                    success = success + 1;
                    document.getElementById(data.record.name).style.backgroundColor = "white";
                }else {
                    failed = failed + 1;
                    document.getElementById(data.record.name).style.backgroundColor = "red";
                }
                document.getElementById('update_record_finished_count').innerHTML="finished: "+data.step+"  &emsp;  success: "+success+"  &emsp;  failed: "+failed+"";
                $("#progress_bar_update_record").css("width", width);
                if (data.step == count){
                    socket.close();
                    operate.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
                }
            };
            return false;
        });
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