$(function () {
    var show_china_map = function(region_data){
        if (!region_data) return;
        $('#china_map').vectorMap({ map: 'china_zh',
            color: "#B4B4B4", //地图颜色
            onLabelShow: function (event, label, code) {//动态显示内容
                $.each(region_data, function (i, items) {
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
        $.each(region_data, function (i, items) {
            if (items.response_time > 2000) {
                var josnStr = "{" + items.cha + ":'red'}";
                $('#china_map').vectorMap('set', 'colors', eval('(' + josnStr + ')'));
            }else{
                var josnStr = "{" + items.cha + ":'green'}";
                $('#china_map').vectorMap('set', 'colors', eval('(' + josnStr + ')'));
            }
        });
        $('.jvectormap-zoomin').click(); 
    };

    var show_region_bar = function(region_data){
        if (!region_data) return;
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'region_bar',
                type: 'bar'
            },
            title: {
                text: '全国访问速度排名'
            },
            xAxis: {
                categories: _.pluck(region_data, 'name')
            },
            yAxis: {
                min: 0,
                title: {
                    text: '总响应时间'
                }
            },
            legend: {
                backgroundColor: '#FFFFFF',
                reversed: true
            },
            tooltip: {
                formatter: function() {
                    return ''+
                        this.series.name +': '+ this.y +'';
                }
            },
            plotOptions: {
                series: {
                    stacking: 'normal'
                }
            },
            series: [{
                name: '域名解析时间',
                data: _.pluck(region_data, 'domain_lookup_time')
            }, {
                name: '连接服务器时间',
                data: _.pluck(region_data, 'connect_time')
            }, {
                name: '读取网页时间',
                data: _.pluck(region_data, 'read_content_time')
            }]
        });
    };
    var show_isp_bar = function(isp_data){
        if (!isp_data) return;
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'isp_bar',
                type: 'column'
            },
            title: {
                enabled: false,
                text: '各运营商平均响应时间'
            },
            xAxis: {
                categories: _.pluck(isp_data, 'name')
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Rainfall (mm)'
                }
            },
            legend: {
                layout: 'vertical',
                backgroundColor: '#FFFFFF',
                align: 'left',
                verticalAlign: 'top',
                x: 100,
                y: 70,
                floating: true,
                shadow: true
            },
            tooltip: {
                formatter: function() {
                    return ''+
                        this.x +': '+ this.y +' ms';
                }
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: [{
                name: '域名解析时间',
                data: _.pluck(isp_data, 'domain_lookup_time')
            }, {
                name: '连接服务器时间',
                data: _.pluck(isp_data, 'connect_time')
            }, {
                name: '读取网页时间',
                data: _.pluck(isp_data, 'read_content_time')
            }]
       }); 
    };
    $.getJSON('/statistics_data/'+ statistics_clientid, function(result){
        show_china_map(result.region_data);
        show_region_bar(result.region_data);
        show_isp_bar(result.isp_data);
    });
});
