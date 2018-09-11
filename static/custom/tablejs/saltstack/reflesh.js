$(function () {
    operate.operateInit();
});

//全局变量
window.modal_results = document.getElementById("OperateRestartresults");
window.modal_footer = document.getElementById("progressFooter");
window.modal_head = document.getElementById("progress_head");
window.project_list_html = {}
window.cdn_list_html = {}

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.GetProjects();
        this.DisplayPanel();
        //this.Submit();
        this.Results();
        this.selectpicker();
        //this.showSelectedValue();
        //this.Exe();
    },

    ChangeArgumentsStyle: function (fun, arg){
        if (document.getElementById(fun).value == 'test.ping'){
            document.getElementById(arg).disabled = true;
        }else {
            document.getElementById(arg).disabled = false;
        }
    },

    GetProjects: function(value){
        operate.disableButtons(['btn_repost', 'btn_submit_cdn_proj', 'btn_submit_cdn'], true);

        var projectlist = []
        //var project = document.getElementById("project_active").value;
        //console.log(productlist);
        var postData = {};
        toastr.info("正在获取数据，请耐心等待返回...");
        $.ajax({
            url: "/saltstack/reflesh/get_project",
            type: "post",
            contentType: 'application/json',
            //data: JSON.stringify(postData),
            success: function (datas, status) {
                operate.disableButtons(['btn_repost', 'btn_submit_cdn_proj', 'btn_submit_cdn'], false);
                toastr.success('数据获取成功！');
                //alert(datas);
                var data = eval('('+datas+')');
                //console.log(data);
                var project_html = "";
                var cdn_html     = "";
                $.each(data.cdn_proj, function (index, item) {
                    var domain_html = "";
                    //循环获取数据 
                    //$.each(item.cdn, function (index, cdn) {
                    //    cdn_html = cdn_html + "<option value='"+cdn.name+"_"+cdn.account+"' data-subtext='"+cdn.name+"'>"+cdn.account+"</option>";
                    //})
                    $.each(item.domain, function (index, domain) {
                        domain_html = domain_html + "<option value="+domain.id+" data-subtext='"+domain.product+" "+domain.customer+"'>"+domain.name+"</option>";
                    })

                    project_html = project_html + "<option value='"+item.project+"'>"+item.project+"</option>";
                    project_list_html[item.project] = {'domain_html': domain_html};
                })
                
                $.each(data.cdn, function (index, item) {
                    var domain_html = "";
                    cdn_html = cdn_html + "<option value="+item.id+" data-subtext='"+item.name+"'>"+item.account+"</option>";
                    
                    $.each(item.domain, function (index, domain) {
                        if (domain.ssl === 1){
                            domain_html = domain_html + "<option value=https://"+domain.name+">https://"+domain.name+"</option>";
                        }else {
                            domain_html = domain_html + "<option value=http://"+domain.name+">http://"+domain.name+"</option>";
                        }
                        
                    })
                    
                    cdn_list_html[item.id] = {'domain_html': domain_html};
                })

                document.getElementById('cdn_projects').innerHTML=project_html;
                document.getElementById('cdns').innerHTML=cdn_html;
                //console.log(cdn_list_html)

                $('.selectpicker').selectpicker('refresh');
            },
            error:function(msg){
                operate.disableButtons(['btn_repost', 'btn_submit_cdn_proj', 'btn_submit_cdn'], false);
                alert("获取项目失败！");
                return false;
            }
        });
    },

    DisplayPanel: function (){
        $("#cdn_panel").bind('click',function () {
            that = document.getElementById("cdn_form")
            if (that.style.display == "none"){
                that.style.display = "inline";
                document.getElementById('cdn_panel').innerHTML = "-";
                document.getElementById('cdn_panel').title = "隐藏";
            }else {
                that.style.display = "none";
                document.getElementById('cdn_panel').innerHTML = "+";
                document.getElementById('cdn_panel').title = "展开";
            }
        });

        $("#cdn_proj_panel").bind('click',function () {
            that = document.getElementById("cdn_proj_form")
            if (that.style.display == "none"){
                that.style.display = "inline";
                document.getElementById('cdn_proj_panel').innerHTML = "-";
                document.getElementById('cdn_proj_panel').title = "隐藏";
            }else {
                that.style.display = "none";
                document.getElementById('cdn_proj_panel').innerHTML = "+";
                document.getElementById('cdn_proj_panel').title = "展开";
            }
        });
    },
    
    setPorjectHtml: function(form, value){
        project = document.getElementById("cdn_projects").value;
        //console.log(project_list_html)
        //document.getElementById('cdns').innerHTML=project_list_html[project]['cdn_html'];
        document.getElementById('cdn_project_domains').innerHTML=project_list_html[project]['domain_html'];
        //$('.selectpicker').selectpicker({title:"请选择服务器地址"});
        $('.selectpicker').selectpicker('refresh');
        return false;
    },

    setCdnHtml: function(form, value){
        cdn = document.getElementById("cdns").value;
        document.getElementById('cdn_domains').innerHTML=cdn_list_html[cdn]['domain_html'];
        //$('.selectpicker').selectpicker({title:"请选择服务器地址"});
        $('.selectpicker').selectpicker('refresh');
        return false;
    },
    
    Results: function(){
        $("#show_results").modal({
            keyboard: true
        })
    },

    selectpicker: function() {
        $('.selectpicker').selectpicker({
            style: 'btn-default',
            //width: "auto",
            size: 13,
            showSubtext:true,
        });
    },

    showSelectedValue: function (selects){
        var selectedValue = []; 
        var objSelect = selects; 
        //var objSelect = document.projectreform.minions_id; 
        for(var i = 0; i < objSelect.options.length; i++) { 
            if (objSelect.options[i].selected == true) 
            selectedValue.push(objSelect.options[i].value);
        }
        return selectedValue;
    },

    
    isUri: function (value) {
        var regexp = /^(\/[0-9a-zA-Z_!~*\'().;?:@&=+$,%#-]+)+\/?$/;
        //var regexp = /^\/[a-zA-Z0-9]+.*[a-zA-Z0-9\/]+$/;
        //var regexp_tw = /^(tw|.*\.tw)\..*$/;

        if (value === '/'){
            return true;
        }
        var valid = regexp.test(value);
        if(!valid){
            return false;
        }
        return true;
    },
    
    getcdnSubmitpostData: function(){
        var postData = {
            'id': document.getElementById("cdns").value,
            'uri': document.getElementById("textarea_cdn_domain_uri").value,
            'domain': operate.showSelectedValue(document.cdnreform.cdn_domains),
        };
        
        if (! postData['id']){
            alert("请选择 CDN！");
            return false;
        }
        //if (postData['cdn'].length === 0){
        //    alert("请选择CDN！");
        //    return false;
        //}
        if (postData['domain'].length === 0){
            alert("请选择域名！");
            return false;
        }
        
        var uri_l = postData['uri'].split('\n');
        postData['uri'] = [];
        for(var i = 0; i < uri_l.length; i++) { 
            if(uri_l[i].replace(/ /g, '') === ''){
                continue;
            }
            if (! operate.isUri(uri_l[i].replace(/(^\s*)|(\s*$)/g, ""))) {
                alert(uri_l[i].replace(/(^\s*)|(\s*$)/g, "") + "格式不正确！");
                return false;
            }
            postData['uri'].push(uri_l[i].replace(/(^\s*)|(\s*$)/g, ""));
        }
        if (postData['uri'].length === 0){
            postData['uri'] = ['/'];
        }
        return postData;
    },
    
    getcdnprojSubmitpostData: function(){
        var postData = {
            'project': document.getElementById("cdn_projects").value,
            'uri': document.getElementById("textarea_domain_uri").value,
            //'cdn': operate.showSelectedValue(document.projectreform.cdns),
            'domain': operate.showSelectedValue(document.projectreform.cdn_project_domains),
        };
        
        if (! postData['project']){
            alert("请选择项目！");
            return false;
        }
        //if (postData['cdn'].length === 0){
        //    alert("请选择CDN！");
        //    return false;
        //}
        if (postData['domain'].length === 0){
            alert("请选择域名！");
            return false;
        }
        
        var uri_l = postData['uri'].split('\n');
        postData['uri'] = [];
        for(var i = 0; i < uri_l.length; i++) { 
            if(uri_l[i].replace(/ /g, '') === ''){
                continue;
            }
            if (! operate.isUri(uri_l[i].replace(/(^\s*)|(\s*$)/g, ""))) {
                alert(uri_l[i].replace(/(^\s*)|(\s*$)/g, "") + "格式不正确！");
                return false;
            }
            postData['uri'].push(uri_l[i].replace(/(^\s*)|(\s*$)/g, ""));
        }
        if (postData['uri'].length === 0){
            postData['uri'] = ['/'];
        }
        return postData;
    
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
    
    Submit: function(submit){

        if (submit == 'cdn') {
            var postData = operate.getcdnSubmitpostData();
            var posturi  = "/saltstack/reflesh/execute/cdn";
        }else if (submit == 'cdn_proj') {
            var postData = operate.getcdnprojSubmitpostData();
            var posturi  = "/saltstack/reflesh/execute";
        }else {
            alert('数据提交错误！');
            return false;
        }
        if (! postData) {
            return false;
        }
        
        $('#runprogress').modal('show');

        //alert("获取到的表单数据为:"+JSON.stringify(postData));
        modal_results.innerHTML = "";
        modal_footer.innerHTML = "";
        $("#progress_bar").css("width", "30%");
        modal_head.innerHTML = "操作进行中，请勿刷新页面......";
        $('#OperateRestartresults').append('<p>连接中......</p>' );

        public.socketConn(posturi, [])

        window.s.onopen = function (e) {
            window.s.send(JSON.stringify(postData));
        };
        
        window.s.onerror = function (){
            modal_head.innerHTML = "与服务器连接失败...";
            $('#OperateRestartresults').append('<p>连接失败......</p>' );
            $("#commandresults").append('<p>执行失败！</p>');
            setTimeout(function(){$('#runprogress').modal('hide');}, 1000);
        };

        window.s.onclose = function () {
            setTimeout(function(){$('#runprogress').modal('hide');}, 1000);
        };

        window.s.onmessage = function (e) {
            if (e.data == 'userNone'){
                toastr.error('未获取用户名，请重新登陆！', '错误');
                window.s.close();
                return false;
            }

            //return false;
            data = eval('('+ e.data +')')
            //console.log('message: ' + data['target']);//打印服务端返回的数据
            if (data.step == 'one'){
                $("#progress_bar").css("width", "50%");
                $('#OperateRestartresults').append('<p>连接成功......</p>' );
                modal_head.innerHTML = "命令执行中...";
            }else if (data.step == 'two'){
                modal_head.innerHTML = "命令执行完成...";
                //$("#progress_bar").css("width", "100%");
                //$('#OperateRestartresults').append('<pre>' + data['result'] + '</pre>');
                //$('#OperateRestartresults').append('<p>执行完成......</p>' );
                //console.log('websocket已关闭');
                //setTimeout(function(){$('#runprogress').modal('hide');}, 1000);
                var html = "";

                for(var i = 0; i < data.result.length; i++) { 
                    html = html + data.result[i]+"<br/>";
                }
                
                $("#commandresults").append(html);
                $('#OperateRestartresults').append(html);
                //socket.close();
                //return false;
            }else if (data.step == 'final'){
                $("#progress_bar").css("width", "100%");
                $('#OperateRestartresults').append('<p>执行完成......</p>' );
                window.s.close();
                setTimeout(function(){$('#runprogress').modal('hide');}, 1000);
            }
        }; 
        return false;
    },

    Exe: function(){
        $("#btn_exe").bind('click',function () {
            //var postData=operate.Getform();
            var postData = {
                expr_form,
                target,
                function:document.getElementById("function2").value,
                arguments:document.getElementById("arguments2").value,
            };
            //console.log(postData)
            postData['target'] = operate.showSelectedValue();
            if (document.getElementById("project_active").value.length == 0){
                alert("请至少选择一个服务！")
                return false;
            }
            if (postData['target'].length == 0){
                alert("请至少选择一个服务器！")
                return false;
            }
            postData['expr_form'] = 'list';
            console.log(postData)
            //alert("获取到的表单数据为:"+JSON.stringify(postData));
            $.ajax({
                url: "/saltstack/command/execute",
                type: "post",
                contentType: 'application/json',
                dataType: "json",
                data: JSON.stringify(postData),
                success: function (data, status) {
                    var html = "";
                    var button = "";
                    for (var tgt in data){
                        button = button + [
                            '<div class="btn-group">',
                                '<button data-toggle="modal" data-target="#'+tgt+'" id="#'+tgt+'" type="button" class="btn btn-primary">'+tgt+'',
                                '</button>',
                            '</div>',
                            '<div class="modal fade" id="'+tgt+'" tabindex="-1" role="dialog" dialaria-labelledby="'+tgt+'" aria-hidden="true">',
                                '<div class="modal-dialog" style="width:1000px;">',
                                    '<div class="modal-content" >',
                                        '<div class="modal-body">',
                                            '<xmp>'+data[tgt]+'</xmp>',
                                        '</div>',
                                    '</div>',
                                '</div>',
                            '</div>',].join("");
                        html = html + "<p><strong>"+tgt+"</strong></p><pre class='pre-scrollable'><xmp>"+data[tgt]+"</xmp></pre>";
                    }
                    button = "<div class='btn-toolbar' role='toolbar'>" + button +"</div>" + "<hr>"
                    $("#commandresults").html(button+html);
                    for (var tgt in data){
                        $("#"+tgt).click(function(){
                            $(this).modal({keyboard: true});
                        });
                    }
                    return false;
                },
                error:function(msg){
                    alert("参数输入错误！");
                    return false;
                }
            });
            return false;
        });
    },

};