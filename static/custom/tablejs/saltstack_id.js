$(function () {
    tableInit.Init();
    operate.operateInit();
});

//初始化表格
var tableInit = {
    Init: function () {
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/saltstack/saltstack_id/Query',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            singleSelect:true,
            //clickToSelect:true,
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset };
            },//传递参数（*）
        });
        //this.myViewModel.query('查看');
        //var viewModel = {
        //    query : ko.observable("查看"),
        //};
        ko.applyBindings(this.myViewModel, document.getElementById("saltstack_id"));
    }
};
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.QueryMinion();
        this.CancelSelect();
        this.QueryModel = {
            minion_id: ko.observable(),
            minion_status: ko.observable(),
        };
    },
    QueryMinion: function(){
        $('#btn_query_minion').on("click", function () {
            var arrselectedData = tableInit.myViewModel.getSelections();
            var index = arrselectedData.length - 1;
            //console.log(index, arrselectedData[index])
            ko.utils.extend(operate.QueryModel, ko.mapping.fromJS(arrselectedData[0]))
            if (!operate.operateCheck(arrselectedData)) { return; }
            html = "<p align='left'>正在加载，请稍后！</p>";
            $("#queryresults").html(html);
            $.ajax({
                url: "/saltstack/saltstack_id/QueryMinion",
                type: "post",
                contentType: 'application/json',
                data: JSON.stringify(arrselectedData),
                //dataType: "json",
                success: function (data, status) {
                    var minion_id = operate.QueryModel.minion_id();
                    var datas = JSON.parse(data);
                    var html = "";
                    if (JSON.stringify(datas) !== "{}"){
                        //alert(datas[minion_id]);
                        html = html + "<p align='left'>主机ID: "+minion_id+"</p>";
                        html = html + "<p align='left'>CPU: "+datas[minion_id]['num_cpus']+"核</p>";
                        html = html + "<p align='left'>系统版本: "+datas[minion_id]['osfullname']+ " "+datas[minion_id]['osrelease']+"</p>";
                        var ip_list = datas[minion_id]['ip4_interfaces'];
                        var ip = " ";       
                        for (var key in ip_list){
                            if (key !== 'lo' ){
                                //alert(ip)
                                ip = ip + ip_list[key] + " ";
                            }
                        }
                        html = html + "<p align='left'>IP地址: "+ip+"</p>";
                    }else{
                        html = html + "<p align='left'>主机ID: "+minion_id+"</p>";
                        html = html + "<p align='left'>主机已DOWN，请检查！</p>";
                    }
                    $("#queryresults").html(html);
                    //tableInit.myViewModel.refresh();
                },
                error:function(msg){
                    alert("失败，请检查日志！");
                    //tableInit.myViewModel.refresh();
                }
            });
            $("#modal_query_minion").modal({keyboard: true});
        });
    },
    //数据校验
    operateCheck:function(arr){
        if (arr.length <= 0) {
            alert("请至少选择一行数据");
            return false;
        }
        if (arr.length > 1) {
            alert("只能选择一行数据");
            return false;
        }
        return true;
    },

    CancelSelect:function (){
        $('#btn_cancel_select').on("click", function () {
            $("input[type='checkbox']").each( function() {
                $(this).parents('.checkbox').find('tr').removeClass('selected');
            });
            console.log("cancel select.");
        });
    }
};