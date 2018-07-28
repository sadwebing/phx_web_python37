$(function () {
    public.operateInit();
});

//操作
var public = {
    //初始化按钮事件
    operateInit: function () {
        //this.isStrinList();
        //this.showSelectedValue();
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

};