$(function () {
    tableInit.Init();
    operate.operateInit();
});

dns.GetProductRecords('cloudflare');

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
            height:730,
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
                    }
                    //width:'8%',
                    //align: 'center'
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
                    events: operateStatusEvents,
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
        '<a class="add_record" href="javascript:void(0)" title="新增记录">',
        '新增',
        '</a>',
        ' | ',
        '<a class="delete_record" href="javascript:void(0)" title="删除记录">',
        '删除',
        '</a>'
        ].join('');
        return content;
    },
};

window.operateStatusEvents = {
    'click .delete_record': function (e, value, row, index) {
        var postData = [row];
        var row_d    = {'index': row.id-1};
        //console.log(row);

        //删除前先隐藏删除列
        tableInit.myViewModel.hideRow(row_d);
        //setTimeout(function(){tableInit.myViewModel.showRow(row_d)}, 2000);
        //tableInit.myViewModel.showRow(row_d);

        $.ajax({
            url: "/dns/cloudflare/delete_records",
            type: "post",
            data: JSON.stringify(postData),
            success: function (data, enabled) {
                toastr.success(row.product+": "+row.name, '域名删除成功');
                //删除列表行
                tableInit.myViewModel.remove({
                    'field': 'id',
                    'values': [row.id]
                });
                
                //alert(data);
                //tableInit.myViewModel.refresh();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                //删除失败，重新展示行
                tableInit.myViewModel.showRow(row_d);
                
                if (XMLHttpRequest.enabled == '0'){
                    toastr.error('后端服务不响应', '错误')
                }else {
                    toastr.error(XMLHttpRequest.responseText, XMLHttpRequest.enabled)
                }
                //console.info(XMLHttpRequest)
                //alert(XMLHttpRequest.enabled+': '+XMLHttpRequest.responseText);
                //tableInit.myViewModel.refresh();
            }
        });
        return false;
    },

    'click .add_record': function (e, value, row, index) {

        //model页面数据初始化
        $("#progress_bar_add_record").css("width", "0%");
        document.getElementById('add_record_finished_count').innerHTML="finished: 0  &emsp;  success: 0  &emsp;  failed: 0";

        //document.getElementById('add_record_content').value = "";
        document.getElementById('add_domain_zone').value = row.zone;
        dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);

        var options = document.getElementById('add_record_type').children;
        options[0].selected=true;

        var options = document.getElementById('add_record_proxied').children;
        options[0].selected=true;

        $("#confirmAddModal").modal().on("shown.bs.modal", function () {
            operate.operateCommitAdd(row);
            //vm.datas.valueHasMutated();
        }).on('hidden.bs.modal', function () {
            //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
            ko.cleanNode(document.getElementById("confirmAddModal"));
        });

        return false;
    },

};

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        tableInit.myViewModel.hidecolumn('zone_id');
        tableInit.myViewModel.hidecolumn('record_id');
        //this.operateCheckStatus();
        //this.isIp();
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

    //查询zone记录
    operateSearch: function () {
        $('#btn_op_search').on("click", function () {
            var zone_list = []
            
            //var project = document.getElementById("project_active").value;
            var objSelectzone = document.domainsform.zone_name; 
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
            dns.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
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
            dns.disableButtons(['btn_close_edit', 'btn_commit_edit'], true);
            var arrselectedData = tableInit.myViewModel.getSelections();
            var postdata = {};
            postdata['type'] = $("#record_type option:selected").val()
            if (! postdata['type']){
                alert('pls select the type!');
                dns.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
                return false;
            }
            postdata['proxied'] = $("#record_proxied option:selected").val()
            if (! postdata['proxied']){
                alert('pls select the proxied!');
                dns.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
                return false;
            }
            postdata['content'] = document.getElementById('record_content').value.replace(/(^\s*)|(\s*$)/g, "");
            if (! postdata['content']){
                alert('content can\'t be empty!');
                dns.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
                return false;
            }

            if (postdata['type'] == 'A') {
                if (! dns.isIp(postdata['content'])){
                    alert('Content for A record is invalid.');
                    dns.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
                    return false;
                }
            }else if (postdata['type'] == 'CNAME'){
                if (! dns.isDomain(postdata['content'], postdata['proxied'])){
                    alert('Content for CNAME record is invalid.');
                    dns.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
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
                dns.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
            };
            socket.onmessage = function (e) {

                //console.log(e.data);

                if (e.data == 'userNone'){
                    toastr.error('未获取用户名，请重新登陆！', '错误');
                    dns.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
                    socket.close();
                    return false;
                }

                data = eval('('+ e.data +')');

                if (! data.permission){
                    toastr.error('抱歉，您没有修改['+data.record.name+']权限！', '错误');
                }

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
                    //tableInit.myViewModel.refresh();
                    dns.disableButtons(['btn_close_edit', 'btn_commit_edit'], false);
                }
            };
            return false;
        });
    },

    operateCommitAdd: function (row) {
        $('#btn_commit_add').on("click", function () {
            $("#progress_bar_add_record").css("width", "0%");
            dns.disableButtons(['btn_close_add', 'btn_commit_add'], true);

            var postdata = {
                'zone':    row.zone,
                'zone_id': row.zone_id,
                'product': row.product,
                'type':    document.getElementById('add_record_type').value,
                'proxied': document.getElementById('add_record_proxied').value,
                'content': document.getElementById('add_record_content').value.replace(/(^\s*)|(\s*$)/g, ""),
            };

            postdata['sub_domain'] = document.getElementById('textarea_add_sub_domain').value.split('\n');

            for(var i = 0; i < postdata['sub_domain'].length; i++) { 
                if(postdata['sub_domain'][i].replace(/ /g, '') === ''){
                    postdata['sub_domain'].splice(i, 1);
                }else if (! public.isSubDomain(postdata['sub_domain'][i])) {
                    alert(postdata['sub_domain'][i] + "格式不正确！");
                    dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);
                    return false;
                }
            }

            if (postdata['sub_domain'].length == 0){
                alert('sub_domain can\'t be empty!');
                dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);
                return false;
            }

            if (! postdata['type']){
                alert('pls select the type!');
                dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);
                return false;
            }

            if (! postdata['proxied']){
                alert('pls select the proxied!');
                dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);
                return false;
            }

            if (! postdata['content']){
                alert('content can\'t be empty!');
                dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);
                return false;
            }

            if (postdata['type'] == 'A') {
                if (! dns.isIp(postdata['content'])){
                    alert('Content for A record is invalid.');
                    dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);
                    return false;
                }
            }else if (postdata['type'] == 'CNAME'){
                if (! dns.isDomain(postdata['content'], postdata['proxied'])){
                    alert('Content for CNAME record is invalid.');
                    dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);
                    return false;
                }
            }

            count = postdata['sub_domain'].length;
            success = 0;
            failed = 0;

            var socket = new WebSocket("ws://" + window.location.host + "/dns/cloudflare/create_records");
            socket.onopen = function () {
                //console.log('WebSocket open');//成功连接上Websocket
                socket.send(JSON.stringify(postdata));
            };
            //$('#runprogress').modal('show');
            socket.onerror = function (){
                toastr.error('后端服务不响应', '错误');
                dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);
            };
            socket.onclose = function () {
                //setTimeout(function(){$('#confirmaddModal').modal('hide');}, 1000);
                toastr.info('连接已关闭...');
                dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);
            };
            socket.onmessage = function (e) {

                if (e.data == 'userNone'){
                    toastr.error('未获取用户名，请重新登陆！', '错误');
                    dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);
                    socket.close();
                    return false;
                }

                if (e.data == 'noPermission'){
                    toastr.error('抱歉，您没有权限！', '错误');
                    dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);
                    socket.close();
                    return false;
                }

                data = eval('('+ e.data +')');
                var width = 100*(data.step)/count + "%";
                if (data.result){
                    success = success + 1;
                    $('#textarea_add_result').append("<p>"+data.domain+": 域名解析新增成功</p>");
                }else {
                    failed = failed + 1;
                    $('#textarea_add_result').append("<p>"+data.domain+": <strong>域名解析新增失败</strong></p>");
                }
                document.getElementById('add_record_finished_count').innerHTML="finished: "+data.step+"  &emsp;  success: "+success+"  &emsp;  failed: "+failed+"";
                $("#progress_bar_add_record").css("width", width);
                if (data.step == count){
                    tableInit.myViewModel.refresh();
                    socket.close();
                    dns.disableButtons(['btn_close_add', 'btn_commit_add'], false);
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