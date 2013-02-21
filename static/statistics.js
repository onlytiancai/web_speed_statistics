(function(){
    if (!window.addEventListener) return;
    window.addEventListener('load', function(){
        var timing = window.performance.timing;
        if (timing === undefined) return;
       
        if (document.cookie.indexOf('statistics_clientid=') != -1) return; //一天一台机器提交一次数据就行了

        var domain_lookup_time = timing.domainLookupEnd - timing.domainLookupStart;
        var server_time = timing.responseStart - timing.requestStart;
        var read_content_time = timing.responseEnd - timing.responseStart;

        new Image().src = "/statistics/" 
            + statistics_clientid + "/" 
            + domain_lookup_time + "/" 
            + server_time + "/" 
            + read_content_time + ".png"; 
 
        var exdate=new Date();
        exdate.setDate(exdate.getDate() + 1);
        document.cookie="statistics_clientid=" + escape(statistics_clientid) + ";expires="+exdate.toGMTString();
    
    }, false);
}());
