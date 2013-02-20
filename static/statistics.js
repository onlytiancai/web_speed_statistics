(function(){
    window.onload = function() {
        var timing = window.performance.timing;
        if (timing === undefined) return;

        var domain_lookup_time = timing.domainLookupEnd - timing.domainLookupStart;
        var server_time = timing.responseStart - timing.requestStart;
        var read_content_time = timing.responseEnd - timing.responseStart;

        new Image().src = "/statistics/" 
            + statistics_clientid + "/" 
            + domain_lookup_time + "/" 
            + server_time + "/" 
            + read_content_time + ".png"; 
    }
}());
