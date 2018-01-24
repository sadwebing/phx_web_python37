$(function () {
    tableInit.Init_done();
});

//初始化表格
var tableInit = {
    Init_done: function () {
        //绑定table的viewmodel
        this.myViewModel = new ko.bootstrapTableViewModel({
            url: '/malfunction/Query',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            dataType: "json",
            toolbar: '#toolbar',                //工具按钮用哪个容器
            singleSelect:true,
            queryParams: function (param) {
                return { limit: param.limit, offset: param.offset };
            },//传递参数（*）
        });
        ko.applyBindings(this.myViewModel, document.getElementById("done_table"));
    }
};
