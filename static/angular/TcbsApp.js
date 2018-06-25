var TcbsApp = angular.module("TcbsApp",  ['ngAnimate', 'ui.router']);
TcbsApp.config(function ($stateProvider, $urlRouterProvider) {

    //$urlRouterProvider.when("", "mainnav");

    $urlRouterProvider.otherwise("/home");
    $stateProvider
        .state("home", {
            url:"/home",
            templateUrl: "/home"
        })
        .state("malfunction_all", {
            url:"/malfunction_all",
            templateUrl: "/malfunction/all"
        })
        .state("malfunction_op_history", {
            url:"/op_history",
            templateUrl: "/malfunction/op_history"
        })
        .state("monitor_services", {
            url:"/services",
            templateUrl: "/monitor/services"
        })
        .state("monitor_domains", {
            url:"/domains",
            templateUrl: "/monitor/domains"
        })
        .state("dns_cloudflare", {
            url:"/dns/cloudflare",
            templateUrl: "/dns/cloudflare/index"
        })
        .state("dns_nginx", {
            url:"/dns/nginx",
            templateUrl: "/dns/nginx"
        })
        .state("saltstack_command", {
            url:"/saltstack_command",
            templateUrl: "/saltstack/command"
        })
        .state("saltstack_reflesh", {
            url:"/saltstack_reflesh",
            templateUrl: "/saltstack/reflesh"
        })
        .state("saltstack_deploy", {
            url:"/saltstack_deploy",
            templateUrl: "/saltstack/deploy"
        })
        .state("saltstack_restart", {
            url:"/saltstack_restart",
            templateUrl: "/saltstack/restart"
        })
        .state("saltstack_saltstack_id", {
            url:"/saltstack_id",
            templateUrl: "/saltstack/saltstack_id"
        })
        .state("upgrade_operate", {
            url:"/upgrade_operate",
            templateUrl: "/upgrade/operate"
        })
        .state("upgrade_op_history", {
            url:"/upgrade_op_history",
            templateUrl: "/upgrade/op_history"
        })
        .state("detect_index", {
            url:"/detect_index",
            templateUrl: "/detect/index"
        })
});