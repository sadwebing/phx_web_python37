$(function () {
    public.operateInit();
});

//操作
var public = {
    //初始化按钮事件
    operateInit: function () {
        this.selectpicker();
        //this.showSelectedValue();
    },

    ViewModel: function() {
                var self = this;
                self.datas = ko.observableArray();
    },

    selectpicker: function docombjs() {
        $('.selectpicker').selectpicker({
            style: 'btn-default',
            //width: "auto",
            size: 15,
            showSubtext:true,
        });
    },

    isStrinList: function (stringToSearch, arrayToSearch) {
        for (s = 0; s < arrayToSearch.length; s++) {
            thisEntry = arrayToSearch[s].toString();
            if (thisEntry == stringToSearch) {
                return true;
            }
        }
        return false;
    },

    showSelectedValue: function (selectid, bool){
        var selectedValue = []; 
        var objSelect = document.getElementById(selectid); 
        for(var i = 0; i < objSelect.options.length; i++) { 
            if (objSelect.options[i].selected == true) {
                selectedValue.push(objSelect.options[i].value);
            }
        }
        if (bool){
            if (selectedValue.length == 0) {
                for(var i = 0; i < objSelect.options.length; i++) {
                    selectedValue.push(objSelect.options[i].value);
                }
            }
        }
        
        return selectedValue;
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

    isSubDomain: function (value, proxied) {
        var regexp = /^(@|[-_a-zA-Z0-9]+|.*[-_a-zA-Z0-9]+.*\.[-_a-zA-Z0-9]*[-_a-zA-Z]+[-_a-zA-Z0-9]*)$/;

        var valid = regexp.test(value);
        if(!valid){
            return false;
        }

        return true;
    },

    isDomain: function (value, proxied) {
        var regexp = /^.*[-a-zA-Z0-9]+.*\.[-a-zA-Z0-9]*[-a-zA-Z]+[-a-zA-Z0-9]*$/;
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

    disableButtons: function (buttonList, fun) {
        for (var i = 0; i < buttonList.length; i++){
            if (fun){
                document.getElementById(buttonList[i]).disabled = true;
            }else {
                document.getElementById(buttonList[i]).disabled = false;
            }
        }
    },

    socketConn: function (uri, buttons) {
        if (! buttons){
            buttons = []
        }
        var socket = new WebSocket("ws://" + window.location.host + uri);
        socket.onopen = function () {
            //console.log('WebSocket open');//成功连接上Websocket
        };
        //$('#runprogress').modal('show');
        socket.onerror = function (){
            toastr.error('后端服务响应出现错误', '错误');
            public.disableButtons(buttons, false);
        };
        socket.onclose = function () {
            //setTimeout(function(){$('#confirmEditModal').modal('hide');}, 1000);
            toastr.info('连接已关闭...');
            public.disableButtons(buttons, false);
        };
        window.s = socket;

    },


};