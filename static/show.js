$(function () {
    $.getJSON('/statistics_data/'+ statistics_clientid, function(dataStatus){
         $('#container').vectorMap({ map: 'china_zh',
            color: "#B4B4B4", //地图颜色
            onLabelShow: function (event, label, code) {//动态显示内容
                $.each(dataStatus, function (i, items) {
                    if (code == items.cha) {
                        label.html(items.name 
                            + " 累计访问次数：" + items.hits
                            + " 平均响应时间：" + items.response_time 
                            + " 平均域名解析时间：" + items.domain_lookup_time
                            );
                    }
                });
            }
        })
        $.each(dataStatus, function (i, items) {
            if (items.response_time > 2000) {
                var josnStr = "{" + items.cha + ":'red'}";
                $('#container').vectorMap('set', 'colors', eval('(' + josnStr + ')'));
            }else{
                var josnStr = "{" + items.cha + ":'green'}";
                $('#container').vectorMap('set', 'colors', eval('(' + josnStr + ')'));
            }
        });
        $('.jvectormap-zoomin').click(); 
    });
});
