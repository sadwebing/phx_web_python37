$(function () {
    dns.operateInit();
});

//操作
var dns = {
    //初始化按钮事件
    operateInit: function () {
        this.GetProductRecords();
    },

    GetProductRecords: function(){
        var productlist = []
        //var project = document.getElementById("project_active").value;
        var objSelectproduct = document.productform.cf_product; 
        for(var i = 0; i < objSelectproduct.options.length; i++) { 
            if (objSelectproduct.options[i].selected == true) 
            productlist.push(objSelectproduct.options[i].value);
        }
        //console.log(productlist);
        var postData = {};
        postData['product'] = productlist;
        $.ajax({
            url: "/dns/cloudflare/get_product_records",
            type: "post",
            contentType: 'application/json',
            data: JSON.stringify(postData),
            success: function (datas, status) {
                //alert(datas);
                var data = eval(datas);
                var html = "";

                $.each(data, function (index, zone) { 
                    //循环获取数据 
                    html = html + "<option value='"+zone.id+"_"+zone.product+"' data-subtext='"+zone.product+"'>"+zone.name+"</option>";
                })
                document.getElementById('zone_name').innerHTML=html;
                //$('.selectpicker').selectpicker({title:"请选择服务器地址"});
                $('.selectpicker').selectpicker('refresh');
            },
            error:function(msg){
                alert("获取项目失败！");
                return false;
            }
        });
    },

    selectpicker: function docombjs() {
        $('.selectpicker').selectpicker({
            style: 'btn-default',
            //width: "auto",
            size: 15,
            showSubtext:true,
        });
    },
};