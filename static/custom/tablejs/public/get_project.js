$(function () {
    gp.operateInit();
});

//操作
var gp = {
    //初始化按钮事件
    operateInit: function () {
        this.GetProject();
    },

    GetProject: function(){
        $.ajax({
            url: "/saltstack/restart/get_project",
            type: "post",
            contentType: 'application/json',
            //data: JSON.stringify(postData),
            success: function (datas, status) {
                //alert(datas);
                var data = eval(datas);
                //var html = "<option value=''></option>";
                var html_B79 = "";
                var html_P02 = "";
                var html_E02 = "";
                var html_E03 = "";
                var html_E04 = "";
                var html_NWF = "";
                var html_PUBLIC = "";
                $.each(data, function (index, item) { 
                    //循环获取数据 
                    var name = data[index];
                    //console.log(data)
                    //html_name = "<option>"+name+"</option>";
                    if (name.product === 'B79') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_B79 = html_B79 + html_name
                    }else if (name.product === 'P02') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_P02 = html_P02 + html_name
                    }else if (name.product === 'E02') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_E02 = html_E02 + html_name
                    }else if (name.product === 'E03') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_E03 = html_E03 + html_name
                    }else if (name.product === 'E04') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_E04 = html_E04 + html_name
                    }else if (name.product === 'NWF') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_NWF = html_NWF + html_name
                    }else if (name.product === 'PUBLIC') {
                        html_name = "<option value='"+name.project+"'>"+name.project+"</option>";
                        html_PUBLIC = html_PUBLIC + html_name
                    }
                }); 
                //$("#project").html(html);
                //$("#project_active").html(html);
                var html = ['<optgroup label="B79">',
                                html_B79,
                            '</optgroup>',
                            '<optgroup label="P02">',
                                html_P02,
                            '</optgroup>',
                            '<optgroup label="E02">',
                                html_E02,
                            '</optgroup>',
                            '<optgroup label="E03">',
                                html_E03,
                            '</optgroup>',
                            '<optgroup label="E04">',
                                html_E04,
                            '</optgroup>',
                            '<optgroup label="NWF">',
                                html_NWF,
                            '</optgroup>',
                            '<optgroup label="PUBLIC">',
                                html_PUBLIC,
                            '</optgroup>',].join("")
                document.getElementById('project_active').innerHTML=html;
                if (document.getElementById('restart_project_active')){
                    document.getElementById('restart_project_active').innerHTML=html;
                }
                $('.selectpicker').selectpicker('refresh');
                return false;
            },
            error:function(msg){
                alert("获取项目失败！");
                return false;
            }
        });
    },
};