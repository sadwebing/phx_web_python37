$(function () {
    tableInit.Init();
    //operate.operateInit();
});

//初始化表格
var tableInit = {
    Init: function () {
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/malfunction/QueryOpHistory',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            //singleSelect:true,
            clickToSelect: false,
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset };
            },//传递参数（*）
                        columns: [
                //{ 
                //    checkbox: true 
                //},
                {
                    field: 'id',
                    title: 'id',
                    sortable: true,
                    width:'1%',
                    //align: 'center'
                },{
                    field: 'op_time',
                    title: '操作时间',
                    sortable: true,
                    //align: 'center',
                    width:'10%',
                },{
                    field: 'op_user',
                    title: '操作用户',
                    sortable: true,
                    //width:'6%',
                    //align: 'center'
                },{
                    field: 'op_ip_addr',
                    title: '用户地址',
                    sortable: true,
                    //width:'5%',
                    //align: 'center'
                },{
                    field: 'op_type',
                    title: '操作类型',
                    sortable: true,
                    //width:'18%',
                    //align: 'center'
                },{
                    field: 'op_before',
                    title: '操作前',
                    sortable: true,
                    //width:'6%',
                    //align: 'center',
                },{
                    field: 'op_after',
                    title: '操作后',
                    sortable: true,
                    //align: 'center',
                },
            ]
        });
        ko.applyBindings(this.myViewModel, document.getElementById("op_history"));
    },
};
