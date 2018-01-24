$(function () {
    tableInit.Init_undone();
    operate_mal.operateInit();
});

//初始化表格
var tableInit = {
    Init_undone: function () {
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/malfunction/QueryAll',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            //singleSelect:false,
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset };
            },//传递参数（*）
        });      
        ko.applyBindings(this.myViewModel, document.getElementById("all_table"));
    },
};

//操作
var operate_mal = {
    //初始化按钮事件
    operateInit: function () {
        this.operateMalSelect();
        //this.set_time_all();
    },

    selectpicker: function() {
        $('.selectpicker').selectpicker({
            style: 'btn-default',
            width: "auto",
            size: 10,
            showSubtext:true,
        });
    },

    operateMalSelect: function(){
        $('#mal_undone').on("click", function () {
            document.getElementById('mal_undone').disabled = true;
            document.getElementById('mal_done').disabled = false;
            document.getElementById('mal_all').disabled = false;
            if (document.getElementById('btn_add')){
            document.getElementById('btn_add').disabled = false;
            }
            if (document.getElementById('btn_confirm_delete')){
            document.getElementById('btn_confirm_delete').disabled = false;
            }
            //document.getElementById('mal_done').setAttribute("class", "btn btn-default");
            //document.getElementById('mal_all').setAttribute("class", "btn btn-default");
            var params = {
                url: '/malfunction/Query',
                method: 'get',
                singleSelect: false,
            }
            tableInit.myViewModel.refresh(params);
        });
        $('#mal_done').on("click", function () {
            //document.getElementById('mal_undone').setAttribute("class", "btn btn-default");
            document.getElementById('mal_undone').disabled = false;
            document.getElementById('mal_done').disabled = true;
            document.getElementById('mal_all').disabled = false;
            if (document.getElementById('btn_add')){
            document.getElementById('btn_add').disabled = true;
            }
            if (document.getElementById('btn_confirm_delete')){
            document.getElementById('btn_confirm_delete').disabled = true;
            }
            //document.getElementById('mal_all').setAttribute("class", "btn btn-default");
            var params = {
                url: '/malfunction/Query',
                method: 'post',
                singleSelect: false,
            }
            tableInit.myViewModel.refresh(params);
        });
        $('#mal_all').on("click", function () {
            //document.getElementById('mal_undone').setAttribute("class", "btn btn-default");
            //document.getElementById('mal_done').setAttribute("class", "btn btn-default");
            document.getElementById('mal_undone').disabled = false;
            document.getElementById('mal_done').disabled = false;
            document.getElementById('mal_all').disabled = true;
            if (document.getElementById('btn_add')){
            document.getElementById('btn_add').disabled = false;
            }
            if (document.getElementById('btn_confirm_delete')){
            document.getElementById('btn_confirm_delete').disabled = true;
            }
            var params = {
                url: '/malfunction/QueryAll',
                method: 'get',
                singleSelect: false,
            }
            tableInit.myViewModel.refresh(params);
        });
    },
}