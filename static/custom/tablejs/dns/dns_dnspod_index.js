$(function () {
    tableInit.Init();
    operate.operateInit();
});

dns.GetProductRecords('dnspod');

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
                    field: 'value',
                    title: 'content',
                    sortable: true,
                    //width:'15%',
                    //align: 'center'
                },{
                    field: 'record_line',
                    title: '线路',
                    sortable: true,
                    //width:'15%',
                    //align: 'center'
                },{
                    field: 'record_id',
                    title: 'record_id',
                    sortable: true,
                    //width:'auto',
                    //align: 'center'
                },{
                    field: 'enabled',
                    title: '状态',
                    sortable: true,
                    //width:'5%',
                    events: operateStatusEvents,
                    formatter: this.operateStatusFormatter,
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
                    events: operateStatusEvents,
                    formatter: this.operateFormatter,
                    //width:300,
                },
            ]

        });
        //this.myViewModel.hidecolumn('zone_id');
        //this.myViewModel.hidecolumn('record_id');
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
        if (row.enabled == '1'){
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id='+ row.record_id +' class="update_status" checked><span></span>',
                '</label>',
            '</div>'
            ].join('');
        }else if (row.enabled == '0'){
            content = [
            '<div class="checkbox checkbox-slider--a" style="margin:0px;">',
                '<label>',
                    '<input type="checkbox" id='+ row.record_id +' class="update_status"><span></span>',
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
    'click .update_status': function (e, value, row, index) {
        var postData = [row];
        if (document.getElementById(row.record_id).checked){
            postData[0].enabled = '1';
            //console.log(postData);
        }else {
            postData[0].enabled = '0';
            //console.log(postData);
        }
        $.ajax({
            url: "/dns/dnspod/update_records",
            type: "post",
            data: JSON.stringify(postData),
            success: function (data, enabled) {
                if (postData[0].enabled == '1'){
                    toastr.success(row.product+": "+row.name, '域名解析已启用');
                }else {
                    toastr.warning(row.product+": "+row.name, '域名解析已禁用');
                }
                
                //ko.cleanNode(document.getElementById("tomcat_table"));
                row.enabled = postData[0].enabled;
                //alert(data);
                //tableInit.myViewModel.refresh();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                if (postData[0].enabled == '1'){
                    document.getElementById(row.record_id).checked = false;
                }else {
                    document.getElementById(row.record_id).checked = true;
                }
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

    'click .delete_record': function (e, value, row, index) {
        var postData = [row];
        var row_d    = {'index': row.id-1};
        //console.log(row);

        //删除前先隐藏删除列
        tableInit.myViewModel.hideRow(row_d);
        //setTimeout(function(){tableInit.myViewModel.showRow(row_d)}, 2000);
        //tableInit.myViewModel.showRow(row_d);

        $.ajax({
            url: "/dns/dnspod/delete_records",
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
        window.buttons = ['btn_close_add', 'btn_commit_add'];
        public.disableButtons(window.buttons, false);

        var options = document.getElementById('add_record_type').children;
        options[0].selected=true;

        var options = document.getElementById('add_record_line').children;
        options[0].selected=true;

        $("#confirmAddModal").modal().on("shown.bs.modal", function () {
            public.socketConn('/dns/dnspod/create_records', window.buttons)
            operate.operateCommitAdd(row);
            //vm.datas.valueHasMutated();
        }).on('hidden.bs.modal', function () {
            //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
            ko.cleanNode(document.getElementById("confirmAddModal"));
            if (window.s) {
                window.s.close();
            }
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

            var objSelectzone = document.domainsform.zone_name; 
            for(var i = 0; i < objSelectzone.options.length; i++) { 
                if (objSelectzone.options[i].selected == true){
                    var tmp = {}
                    tmp['id'] = objSelectzone.options[i].value.split('_')[0];
                    tmp['name'] = objSelectzone.options[i].text;
                    tmp['product'] = objSelectzone.options[i].value.split('_')[1];
                    zone_list.push(tmp);
                }
            }
            //console.log(zone_list);
            var params = {
                url: '/dns/dnspod/get_zone_records',
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

            var options = document.getElementById('record_status').children;
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
                    //console.log(record);
                    //alert(record)
                    html_record = "<tr id="+record.name()+"><td>"+record.product()+"</td><td>"+record.zone()+"</td><td>"+record.name()+"</td><td>"+record.type()+"</td><td>"+record.value()+"</td><td>"+record.enabled()+"</td></tr>";
                    html = html + html_record
                }); 
                $("#EditDatas").html(html);
                window.buttons = ['btn_close_edit', 'btn_commit_edit'];
                public.socketConn('/dns/dnspod/update_records', window.buttons)
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
            postdata['type'] = $("#record_type option:selected").val()
            if (! postdata['type']){
                alert('pls select the type!');
                public.disableButtons(window.buttons, false);
                return false;
            }
            postdata['enabled'] = $("#record_status option:selected").val()
            if (! postdata['enabled']){
                alert('pls select the status!');
                public.disableButtons(window.buttons, false);
                return false;
            }
            postdata['value'] = document.getElementById('record_content').value.replace(/(^\s*)|(\s*$)/g, "");
            if (! postdata['value']){
                alert('content can\'t be empty!');
                public.disableButtons(window.buttons, false);
                return false;
            }

            if (postdata['type'] == 'A') {
                if (! operate.isIp(postdata['value'])){
                    alert('Content for A record is invalid.');
                    public.disableButtons(window.buttons, false);
                    return false;
                }
            }else if (postdata['type'] == 'CNAME'){
                if (! operate.isDomain(postdata['value'], postdata['enabled'])){
                    alert('Content for CNAME record is invalid.');
                    public.disableButtons(window.buttons, false);
                    return false;
                }
            }

            postdata['records'] = arrselectedData;
            count = postdata['records'].length;
            success = 0;
            failed = 0;

            if (! window.s){
                toastr.error('socket 未连接，请重新修改！', '错误');
                public.disableButtons(window.buttons, false);
                return false;
            }else {
                window.s.send(JSON.stringify(postdata));
            }

            window.s.onmessage = function (e) {

                if (e.data == 'userNone'){
                    toastr.error('未获取用户名，请重新登陆！', '错误');
                    public.disableButtons(window.buttons, false);
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
                    //socket.close();
                    //tableInit.myViewModel.refresh();
                    public.disableButtons(window.buttons, false);
                }
            };
            return false;
        });
    },

    operateCommitAdd: function (row) {
        $('#btn_commit_add').on("click", function () {
            $("#progress_bar_add_record").css("width", "0%");
            public.disableButtons(window.buttons, true);

            var postdata = {
                'zone':    row.zone,
                'product': row.product,
                'type':        document.getElementById('add_record_type').value,
                'record_line': document.getElementById('add_record_line').value,
                'value':       document.getElementById('add_record_content').value.replace(/(^\s*)|(\s*$)/g, ""),
            };

            postdata['sub_domain'] = document.getElementById('textarea_add_sub_domain').value.split('\n');

            for(var i = 0; i < postdata['sub_domain'].length; i++) { 
                if(postdata['sub_domain'][i].replace(/ /g, '') === ''){
                    postdata['sub_domain'].splice(i, 1);
                }else if (! public.isSubDomain(postdata['sub_domain'][i])) {
                    alert(postdata['sub_domain'][i] + "格式不正确！");
                    public.disableButtons(window.buttons, false);
                    return false;
                }
            }

            if (postdata['sub_domain'].length == 0){
                alert('sub_domain can\'t be empty!');
                public.disableButtons(window.buttons, false);
                return false;
            }

            if (! postdata['type']){
                alert('pls select the type!');
                public.disableButtons(window.buttons, false);
                return false;
            }

            if (! postdata['record_line']){
                alert('pls select the record_line!');
                public.disableButtons(window.buttons, false);
                return false;
            }

            if (! postdata['value']){
                alert('content can\'t be empty!');
                public.disableButtons(window.buttons, false);
                return false;
            }

            if (postdata['type'] == 'A') {
                if (! operate.isIp(postdata['value'])){
                    alert('Content for A record is invalid.');
                    public.disableButtons(window.buttons, false);
                    return false;
                }
            }else if (postdata['type'] == 'CNAME'){
                if (! operate.isDomain(postdata['value'], 'true')){
                    alert('Content for CNAME record is invalid.');
                    public.disableButtons(window.buttons, false);
                    return false;
                }
            }

            count = postdata['sub_domain'].length;
            success = 0;
            failed = 0;

            if (! window.s){
                toastr.error('socket 未连接，请重新修改！', '错误');
                public.disableButtons(window.buttons, false);
                return false;
            }else {
                window.s.send(JSON.stringify(postdata));
            }

            window.s.onmessage = function (e) {

                if (e.data == 'userNone'){
                    toastr.error('未获取用户名，请重新登陆！', '错误');
                    public.disableButtons(window.buttons, false);
                    socket.close();
                    return false;
                }

                if (e.data == 'noPermission'){
                    toastr.error('抱歉，您没有权限！', '错误');
                    public.disableButtons(window.buttons, false);
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
                    public.disableButtons(window.buttons, false);
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