$(function () {
    dns.operateInit();
});

window.product_list_html = {}

//操作
var dns = {
    //初始化按钮事件
    operateInit: function () {
        //this.GetProductRecords('dnspod');
    },

    isSubDomain: function (value, proxied) {
        var regexp = /^(@|[a-zA-Z0-9]+|.*[a-zA-Z0-9]+.*\.[a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*)$/;

        var valid = regexp.test(value);
        if(!valid){
            return false;
        }

        return true;
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

    disableButtons: function (buttonList, fun) {
        for (var i = 0; i < buttonList.length; i++){
            if (fun){
                document.getElementById(buttonList[i]).disabled = true;
            }else {
                document.getElementById(buttonList[i]).disabled = false;
            }
        }
    },
    
    setProductHtml: function(value){
        var productlist = []
        //var project = document.getElementById("project_active").value;
        objSelectproject = document.productform.product;
        
        for(var i = 0; i < objSelectproject.options.length; i++) { 
            if (objSelectproject.options[i].selected == true) 
            productlist.push(objSelectproject.options[i].value);
        }
        var html = "";

        for (var num in productlist){
            product = productlist[num];
            html = html + product_list_html[product];
        }
        document.getElementById(value).innerHTML=html;
        //$('.selectpicker').selectpicker({title:"请选择服务器地址"});
        $('.selectpicker').selectpicker('refresh');
        return false;
    },

    GetProductRecords: function(value){
        dns.disableButtons(['btn_repost', 'btn_op_search'], true);
        toastr.info("正在获取数据，请耐心等待返回...");

        $.ajax({
            url: "/dns/"+value+"/get_product_records",
            type: "post",
            contentType: 'application/json',
            //data: JSON.stringify(postData),
            success: function (datas, status) {
                dns.disableButtons(['btn_repost', 'btn_op_search'], false);
                toastr.success('数据获取成功！');
                //alert(datas);
                var data = eval('('+datas+')');
                var product_html = "";

                $.each(data, function (index, item) { 
                    var domain_html = "";
                    product_html = product_html + "<option value="+item.product+">"+item.product+"</option>";
                    //循环获取数据 
                    $.each(item.domain, function (index, domain) {
                        if (domain.status == 'enable'){
                            domain_html = domain_html + "<option value='"+domain.id+"_"+item.product+"' data-subtext='"+item.product+"'>"+domain.name+"</option>";
                        }
                    })

                    product_list_html[item.product] = domain_html;
                })
                document.getElementById('product').innerHTML=product_html;
                //$('.selectpicker').selectpicker({title:"请选择服务器地址"});
                $('.selectpicker').selectpicker('refresh');
            },
            error:function(msg){
                dns.disableButtons(['btn_repost', 'btn_op_search'], false);
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