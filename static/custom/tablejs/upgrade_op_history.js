$(function () {
    tableInit.Init();
    operate.operateInit();
});

//全局变量
window.run = true;
//window.rollback_results = document.getElementById("rollback_results")
window.modal_head_content = document.getElementById("rollback_modal_head_content");
window.modal_results = document.getElementById("rollback_results");
window.modal_head_close = document.getElementById("rollback_modal_head_close");
window.rollback_progress_head = document.getElementById("rollback_progress_head");
window.rollback_progress_body = document.getElementById("rollback_progress_body");

//初始化表格
var tableInit = {
    Init: function () {
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/upgrade/op_history/Query',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            //singleSelect:true,
            clickToSelect: true,
            queryParams: function (param) {
                return { limit: 1000, offset: param.offset, 'act':'query_all', };
            },//传递参数（*）
            rowStyle: function (row, index) {
                //这里有5个取值代表5中颜色['active', 'success', 'info', 'warning', 'danger'];
                var strclass = "";
                if (row.op_status == 0) {
                    strclass = 'danger';
                }else if (row.op_status == 1) {
                    strclass = 'success';
                }else {
                    return {};
                }
                return { classes: strclass }
            },
        });
        ko.applyBindings(this.myViewModel, document.getElementById("upgrade_op_history"));
    },

    checkboxFormatter: function (value,row,index){
        if (row.act == 'diff' || row.act == 'rollback' ){
            return {
                disabled : true
            };
        }        
    },

    infoFormatter: function (value,row,index){
        var content = [
            '<a class="info text-info" href="javascript:void(0)" title="详情">',
                '详情',
            '</a>',
        ].join('');
        return content;
    },

    opStatusFormatter: function (value,row,index){
        if (row.op_status == 1){
            var content = '成功';
        }else if (row.op_status == 0){
            var content = '失败';
        }else if (row.op_status == -1){
            var content = '参数错误';
        }else {
            var content = '未知';
        }
        return content;
    },
};

window.infoEvents = {
    'click .info': function (e, value, row, index) {
        var html = row.info;
        var info_xmp = document.getElementById('info_xmp')
        info_xmp.innerHTML = html;
        $('#info_modal').modal('show');

        return false;
    },

    'click .recover': function (e, value, row, index) {
        var postData = {};
        postData['deleted'] = 0
        postData['id'] = row.id
        postData['svn_id'] = row.svn_id

        $.ajax({
            url: "/upgrade/update_svn",
            type: "post",
            data: JSON.stringify(postData),
            success: function (datas, status) {
                if (datas == 'failure'){
                    alert("failure");
                }else {
                    toastr.warning('恢复成功！', row.project+": "+row.svn_id)
                    $('#upgrade_op_table').bootstrapTable('refresh');
                }
            },
            error:function(msg){
                alert("恢复失败，请检查日志！");
            }
        });
        
        return false;
    }
};  

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.operateRollback();
        this.opHisModel = {
            id: ko.observable(),
            envir: ko.observable(),
            svn_id: ko.observable(),
            project: ko.observable(),
            ip_addr: ko.observable(),
            act: ko.observable(),
            op_time: ko.observable(),
            com_time: ko.observable(),
            op_user: ko.observable(),
            op_ip_addr: ko.observable(),
            op_status: ko.observable(),
            backup_file: ko.observable(),
            info: ko.observable(),
        };
    },

    ViewModel: function() {
                var self = this;
                self.datas = ko.observableArray();
    },

    operateRollback: function () {

        $('#rollback_interrupt').on("click", function () {
            //alert('终止')
            //cur_status.innerHTML = '中断';
            rollback_modal_head_content.innerHTML = "中断";
            run = false;
            operate.disableButtons(['confirm_rollback'], false);
            operate.disableButtons(['rollback_interrupt'], true);
        });

        $('#upgrade_rollback').on("click", function () {
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

            //初始化按钮
            operate.disableButtons(['confirm_rollback'], false);
            operate.disableButtons(['rollback_interrupt'], true);

            //初始化页面参数
            //rollback_progress_body.hidden = true;
            rollback_progress_head.innerHTML= "";
            modal_head_content.innerHTML = "请选择回退参数";
            modal_head_close.innerHTML = "&times;";
            modal_results.innerHTML = "";
            $("#rollback_progress_bar").css("width", "0%");
            rollback_progress_head.innerHTML="执行中 总共：<strong>0</strong>台    "+"成功：<strong>0</strong>台";
            var obj_restart = document.getElementsByName('rollback_restart');
            for(i=0;i<obj_restart.length;i++) { 
                if(obj_restart[i].checked) { 
                    obj_restart[i].checked = false; 
                } 
            }

            $("#confirmRollbackModal").modal().on("shown.bs.modal", function () {
                ko.applyBindings(vm, document.getElementById("confirmRollbackModal"));
                //datas = ko.mapping.fromJS(arrselectedData)
                var html = "";
                $.each(vm.datas(), function (index, item) { 
                    //循环获取数据
                    var name = vm.datas()[index];
                    //alert(name)
                    html_name = "<tr style='text-align: center;'><td>"+name.id()+"</td><td>"+name.envir()+"</td><td>"+name.svn_id()+"</td><td>"+name.project()+"</td><td>"+name.ip_addr()+"</td><td>"+name.backup_file()+"</td></tr>";
                    html = html + html_name;
                }); 
                $("#RollbackDatas").html(html);
                operate.operateconfirmRollback();
                //vm.datas.valueHasMutated();
            }).on('hidden.bs.modal', function () {
                //关闭弹出框的时候清除绑定(这个清空包括清空绑定和清空注册事件)
                ko.cleanNode(document.getElementById("confirmRollbackModal"));
            });
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

    getNowFormatDate: function (type) {
        var seperator1 = "-";
        var seperator2 = ":";
        var dtCur = new Date();
        var yearCur = dtCur.getFullYear();
        var monCur = dtCur.getMonth() + 1;
        var dayCur = dtCur.getDate();
        var hCur = dtCur.getHours();
        var mCur = dtCur.getMinutes();
        var sCur = dtCur.getSeconds();
        var currentdate = yearCur + seperator1 + (monCur < 10 ? "0" + monCur : monCur) + seperator1 + (dayCur < 10 ? "0" + dayCur : dayCur) + " " + (hCur < 10 ? "0" + hCur : hCur) + seperator2 + (mCur < 10 ? "0" + mCur : mCur) + seperator2 + (sCur < 10 ? "0" + sCur : sCur);
        var timestamp = yearCur + (monCur < 10 ? "0" + monCur : monCur) + (dayCur < 10 ? "0" + dayCur : dayCur) + (hCur < 10 ? "0" + hCur : hCur) + (mCur < 10 ? "0" + mCur : mCur) + (sCur < 10 ? "0" + sCur : sCur);
        if (type == 'normal'){
            return currentdate;
        }else if (type = 'timestamp'){
            return timestamp;
        }   
    },

    operateconfirmRollback: function () {
        $('#confirm_rollback').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            var postData = {};
            postData['step'] = 0;
            postData['act']  = 'rollback';
            postData['dict'] = arrselectedData[postData['step']];
            postData['restart'] = '';
            
            var obj_restart = document.getElementsByName('rollback_restart');
            for(i=0;i<obj_restart.length;i++) { 
                if(obj_restart[i].checked) { 
                    postData['restart'] = obj_restart[i].value; 
                } 
            }
            if (postData['restart'] == ''){
                alert('请选择是否重启服务！');
                return false;
            }


            //更改页面展示的状态
            modal_head_content.innerHTML = "回退操作中，请勿刷新页面......";
            modal_head_close.innerHTML = "";
            rollback_progress_body.hidden = false;
            rollback_progress_head.innerHTML="执行中 总共：<strong>"+arrselectedData.length+"</strong>台    "+"成功：<strong>0</strong>台";
            //$("#rollback_progress_bar").css("width", "0%");

            //按钮
            operate.disableButtons(['confirm_rollback'], true);
            operate.disableButtons(['rollback_interrupt'], false);

            //建立socket连接
            var socket = new WebSocket("ws://" + window.location.host + "/upgrade/op_upgrade/deploy");
            socket.onopen = function () {
                //第一次发送数据
                socket.send(JSON.stringify(postData));
                $('#rollback_results').append('<p>返回结果:</p>');
            };
            socket.onerror = function (){
                modal_head_content.innerHTML = '与服务器连接失败...';
                rollback_progress_head.innerHTML = '与服务器连接失败...';
                modal_head_close.innerHTML = "&times;";
                operate.disableButtons(['confirm_rollback'], false);
                operate.disableButtons(['rollback_interrupt'], true);
            };
            socket.onmessage = function (e) {
                //return false;
                data = eval('('+ e.data +')')
    
                if (data.op_status == -1){
                    modal_head_close.innerHTML = "&times;"
                    operate.disableButtons(['confirm_rollback'], false);
                    operate.disableButtons(['rollback_interrupt'], true);
                    $('#rollback_results').append('<p>传入参数错误，请检查服务！</p>');
                    return false;
                }else if (data.op_status == 0){
                    modal_head_close.innerHTML = "&times;"
                    operate.disableButtons(['confirm_rollback'], false);
                    operate.disableButtons(['rollback_interrupt'], true);
                    $('#rollback_results').append('<p>错误：'+ data.result +'</p>');
                    return false;
                }
    
                var button = ""
                var button_html = "";
                //console.log('ip_addr: ' + data.ip_addr);//打印服务端返回的数据
                var timestamp = operate.getNowFormatDate('timestamp')
                var width = 100*(data.step+1)/arrselectedData.length + "%"
                postData.step = postData.step + 1;
                postData['dict'] = arrselectedData[postData.step];
                if (postData.step == arrselectedData.length - 1){
                    operate.disableButtons(['rollback_interrupt'], true);
                }
                $("#rollback_progress_bar").css("width", width);
                $('#rollback_results').append('<p><strong>'+data.ip_addr+'</strong></p>');
                //console.log(typeof(data.result))
                $('#rollback_results').append('<pre class="pre-scrollable"><xmp>'+data.info+'</xmp></pre>',)
                rollback_progress_head.innerHTML="执行中 总共：<strong>"+arrselectedData.length+"</strong>台    "+"成功：<strong>"+(postData.step)+"</strong>台";
                //console.log(data.step+" : "+postData.ip_addr.length)
                if (run){
                    if (data.step < arrselectedData.length - 1){
                        //console.log(postData);
                        socket.send(JSON.stringify(postData));
                    }else {
                        //cur_status.innerHTML = args.content2;
                        modal_head_close.innerHTML = "&times;"
                        modal_head_content.innerHTML = '回退完成';
                        operate.disableButtons(['confirm_rollback'], false);
                        operate.disableButtons(['rollback_interrupt'], true);
                        //socket.close();
                    }
                }else {
                    modal_head_close.innerHTML = "&times;"
                    operate.disableButtons(['confirm_rollback'], false);
                    operate.disableButtons(['rollback_interrupt'], true);
                    //socket.close();
                }
                
            }; 
            return false;
        });
    },

}