$(function () {
    operate.operateInit();
});

//全局变量
window.detect_results = document.getElementById("detect_results");
window.detect_table = document.getElementById("detect_table");

//操作
var operate = {
    //初始化按钮事件
    operateInit: function () {
        this.selectpicker();
        this.formValidator();
        this.submitDetect();
        $('#btn_clear').bind('click', function(){
            detect_table.innerHTML = "";
            var rowNums = detect_table.rows.length;
            var newRow = detect_table.insertRow(rowNums);
            var col = newRow.insertCell(0);
            newRow.insertCell(0).innerHTML = '<strong>Ip</strong>';
            newRow.insertCell(1).innerHTML = '<strong>http_code</strong>';
            newRow.insertCell(2).innerHTML = '<strong>title</strong>';
        });
    },

    formValidator: function () {
        $('#ip_addr_form').bootstrapValidator({
            message: 'This value is not valid',
            fields: {
                ip_network: {
                    validators: {
                        //notEmpty: {
                        //    message: '&emsp;&emsp;&emsp;&emsp;&emsp;Ip网络位不能为空'
                        //},
                        regexp: {
                            regexp: /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){2}(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))$/,
                            message: '&emsp;&emsp;&emsp;&emsp;请填写正确的网络位地址'
                        }
                    }
                },
                ip_host_start: {
                    validators: {
                        //notEmpty: {
                        //    message: '&emsp;&emsp;&emsp;&emsp;&emsp;起始主机位不能为空'
                        //},
                        regexp: {
                            regexp: /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))$/,
                            message: '&emsp;&emsp;&emsp;&emsp;请填写正确的起始主机位地址'
                        }
                    }
                },
                ip_host_end: {
                    validators: {
                        //notEmpty: {
                        //    message: '&emsp;&emsp;&emsp;&emsp;&emsp;结束主机位不能为空'
                        //},
                        between: {
                            //message: '&emsp;&emsp;&emsp;&emsp;&emsp;起始位不能大于结束位',
                            min: 1,
                            max: 255,
                            message: '&emsp;&emsp;&emsp;&emsp;请填写正确的结束主机位地址'
                        },
                        //regexp: {
                        //    regexp: /^(?:(?:2[0-5][0-5])|(?:25[0-5])|(?:1[0-9][0-9])|(?:[1-9][0-9])|(?:[0-9]))$/,
                        //    message: '&emsp;&emsp;&emsp;&emsp;请填写正确的结束主机位地址'
                        //}
                    }
                },
                port: {
                    validators: {
                        //regexp: {
                        //    regexp: /^[0-9]+$/,
                        //    message: '&emsp;&emsp;&emsp;请填写正确的端口'
                        //},
                        between: {
                            //message: '&emsp;&emsp;&emsp;&emsp;&emsp;起始位不能大于结束位',
                            min: 1,
                            max: 65535,
                            message: '&emsp;&emsp;&emsp;&emsp;&emsp;1 - 65535'
                        },
                    }
                },
            },
            
            submitHandler: function (validator, form, submitButton) {
                alert("submit");
            }
        });
        $('#port_form').bootstrapValidator({
            message: 'This value is not valid',
            fields: {
                port: {
                    validators: {
                        //regexp: {
                        //    regexp: /^[0-9]+$/,
                        //    message: '&emsp;&emsp;&emsp;请填写正确的端口'
                        //},
                        between: {
                            //message: '&emsp;&emsp;&emsp;&emsp;&emsp;起始位不能大于结束位',
                            min: 1,
                            max: 65535,
                            message: '&emsp;&emsp;&emsp;&emsp;&emsp;1 - 65535'
                        },
                    }
                }
            },
        });
    },

    getdetectEles: function() {
        var detectEles = {
            'ip_network':'',
            'ip_host_start':'',
            'ip_host_end':'',
            'port':'',
            'uri':'',
            'step':0
        };
        detectEles['ip_network'] = document.getElementById('ip_network').value;
        detectEles['ip_host_start'] = parseInt(document.getElementById('ip_host_start').value, 10);
        detectEles['ip_host_end'] = parseInt(document.getElementById('ip_host_end').value, 10);
        detectEles['port'] = document.getElementById('port').value;
        detectEles['uri'] = document.getElementById('uri').value;
        return detectEles;
    },

    submitDetect: function () {
        $('#btn_submit_detect').on("click", function () {
            var postData = operate.getdetectEles();
            if (!postData.ip_network){
                toastr.warning('', '网络位不能为空');
                return false;
            }
            if (!postData.ip_host_start){
                postData.ip_host_start = 1;
            }
            if (!postData.ip_host_end){
                postData.ip_host_end = 254;
            }
            if (!postData.port){
                postData.port = '80';
            }
            if (postData.ip_host_start > postData.ip_host_end){
                toastr.warning(postData.ip_host_start+" : "+postData.ip_host_end, '起始主机位大于结束主机位');
                return false;
            }

            document.getElementById('btn_clear').disabled = true;
            document.getElementById('btn_submit_detect').disabled = true;
            
            var socket = new WebSocket("ws://" + window.location.host + "/detect/execute");
            socket.onopen = function () {
                //console.log('WebSocket open');//成功连接上Websocket
                socket.send(JSON.stringify(postData));
            };
            socket.onerror = function (){
                detect_results.append('与服务器连接失败...' );
                document.getElementById('btn_clear').disabled = false;
                document.getElementById('btn_submit_detect').disabled = false;
            };
            socket.onmessage = function (e) {
                data = eval('('+ e.data +')')
                //console.log('message: ' + data);//打印服务端返回的数据
                var rowNums = detect_table.rows.length;
                var newRow = detect_table.insertRow(rowNums);
                var col = newRow.insertCell(0);
                newRow.insertCell(0).innerHTML = postData.ip_network + '.' + (postData.ip_host_start+data.step);
                newRow.insertCell(1).innerHTML = data.http_code;
                newRow.insertCell(2).innerHTML = data.title;
                
                postData.step += 1;
                if (data.step < postData.ip_host_end-postData.ip_host_start){
                    socket.send(JSON.stringify(postData));
                }else {
                    document.getElementById('btn_clear').disabled = false;
                    document.getElementById('btn_submit_detect').disabled = false;
                    return false;
                }
            }; 
            return false;
        });

    },

    selectpicker: function() {
        $('.selectpicker').selectpicker({
            style: 'btn-default',
            width: "auto",
            size: 15,
            showSubtext:true,
        });
    },
};