
(function () {
  var KB_HTML = [
        "<div class=\"td-root\" role=\"region\" aria-label=\"任务详情\">",
        "  <section class=\"td-left\" aria-label=\"任务详细信息\">",
        "    <header class=\"td-bar\">",
        "      <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn td-back\" type=\"button\" aria-label=\"返回任务看板\" data-td-back=\"1\">",
        "        <svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M9.8 3.4L5.2 8l4.6 4.6\"/></svg>",
        "      </button>",
        "      <span class=\"td-bar-title\">任务详情</span>",
        "      <div class=\"td-bar-actions\">",
        "        <button class=\"giencoder-btn giencoder-btn-primary giencoder-btn-size-small td-btn\" type=\"button\">开始任务</button>",
        "        <span class=\"giencoder-popover-reference\"><button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small td-btn\" type=\"button\" data-td-dispatch aria-haspopup=\"dialog\" aria-expanded=\"false\">转派</button></span>",
        "        <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small td-btn\" type=\"button\">协作</button>",
        "        <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small td-btn\" type=\"button\">编辑</button>",
        "        <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn\" type=\"button\" aria-label=\"更多操作\">",
        "          <svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"currentColor\"><circle cx=\"3.4\" cy=\"8\" r=\"1.3\"/><circle cx=\"8\" cy=\"8\" r=\"1.3\"/><circle cx=\"12.6\" cy=\"8\" r=\"1.3\"/></svg>",
        "        </button>",
        "        <span class=\"td-bar-sep\" aria-hidden=\"true\"></span>",
        "        <div class=\"td-bar-nav\">",
        "          <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn\" type=\"button\" aria-label=\"上一个任务\" data-td-prev=\"1\">",
        "            <svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3.6 9.8L8 5.4l4.4 4.4\"/></svg>",
        "          </button>",
        "          <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-small giencoder-btn-icon td-iconbtn\" type=\"button\" aria-label=\"下一个任务\" data-td-next=\"1\">",
        "            <svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M3.6 6.2L8 10.6l4.4-4.4\"/></svg>",
        "          </button>",
        "        </div>",
        "      </div>",
        "    </header>",
        "    <div class=\"td-left-body\">",
        "      <div class=\"td-main\">",
        "        <h1 class=\"td-title\">端到端流程初始化：用户输入业务流程并触发全链路交付</h1>",
        "        <div class=\"td-desc\">",
        "          <div class=\"td-desc-body\" id=\"td-desc-body\" data-td-desc=\"1\">",
        "            <p>第一步：梳理端到端交付链路</p>",
        "            <div class=\"giencoder-image\" data-td-desc-img=\"1\">",
        "              <div class=\"giencoder-image-mask-wrapper\" role=\"button\" tabindex=\"0\" aria-label=\"预览大图：端到端交付链路示意图\">",
        "                <img class=\"giencoder-image-img\" src=\"data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjQwIDYyMCIgd2lkdGg9IjEyNDAiIGhlaWdodD0iNjIwIiByb2xlPSJpbWciIGFyaWEtbGFiZWw9Iuerr+WIsOerr+S6pOS7mOmTvui3ryA4IOS4qumYtuauteekuuaEj+WbviI+CjxkZWZzPjxtYXJrZXIgaWQ9ImFoIiB2aWV3Qm94PSIwIDAgMTAgMTAiIHJlZlg9IjkiIHJlZlk9IjUiIG1hcmtlcldpZHRoPSI2IiBtYXJrZXJIZWlnaHQ9IjYiIG9yaWVudD0iYXV0by1zdGFydC1yZXZlcnNlIj48cGF0aCBkPSJNMCAwIEwxMCA1IEwwIDEwIHoiIGZpbGw9IiNBOUE5QTkiLz48L21hcmtlcj48L2RlZnM+CjxyZWN0IHdpZHRoPSIxMjQwIiBoZWlnaHQ9IjYyMCIgcng9IjE2IiBmaWxsPSIjRjdGN0Y3Ii8+CjxwYXRoIGQ9Ik0xMDcwIDI0MCBWMzEwIEgxNzAgVjM4MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjRENEQ0RDIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgbWFya2VyLWVuZD0idXJsKCNhaCkiLz4KPHBhdGggZD0iTTI5OCAxOTAgSDM0MiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjRENEQ0RDIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgbWFya2VyLWVuZD0idXJsKCNhaCkiLz4KPHBhdGggZD0iTTU5OCAxOTAgSDY0MiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjRENEQ0RDIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgbWFya2VyLWVuZD0idXJsKCNhaCkiLz4KPHBhdGggZD0iTTg5OCAxOTAgSDk0MiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjRENEQ0RDIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgbWFya2VyLWVuZD0idXJsKCNhaCkiLz4KPHBhdGggZD0iTTI5OCA0MzAgSDM0MiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjRENEQ0RDIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgbWFya2VyLWVuZD0idXJsKCNhaCkiLz4KPHBhdGggZD0iTTU5OCA0MzAgSDY0MiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjRENEQ0RDIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgbWFya2VyLWVuZD0idXJsKCNhaCkiLz4KPHBhdGggZD0iTTg5OCA0MzAgSDk0MiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjRENEQ0RDIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgbWFya2VyLWVuZD0idXJsKCNhaCkiLz4KPHJlY3QgeD0iNTAiIHk9IjE0MCIgd2lkdGg9IjI0MCIgaGVpZ2h0PSIxMDAiIHJ4PSIxMiIgZmlsbD0iI0ZGRkZGRiIgc3Ryb2tlPSIjRTVFNUU1Ii8+CjxjaXJjbGUgY3g9IjgwIiBjeT0iMTc0IiByPSIxMyIgZmlsbD0iI0U4RjBGRSIvPgo8dGV4dCB4PSI4MCIgeT0iMTc4IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iUGluZ0ZhbmcgU0MsIE1pY3Jvc29mdCBZYUhlaSwgSGVsdmV0aWNhLCBBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMyIgZm9udC13ZWlnaHQ9IjYwMCIgZmlsbD0iIzM3NzBGNyI+MTwvdGV4dD4KPHRleHQgeD0iMTA0IiB5PSIxNzkiIGZvbnQtZmFtaWx5PSJQaW5nRmFuZyBTQywgTWljcm9zb2Z0IFlhSGVpLCBIZWx2ZXRpY2EsIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE1IiBmb250LXdlaWdodD0iNTAwIiBmaWxsPSIjMUYxRjFGIj7pnIDmsYLmvoTmuIU8L3RleHQ+Cjx0ZXh0IHg9IjgwIiB5PSIyMTQiIGZvbnQtZmFtaWx5PSJQaW5nRmFuZyBTQywgTWljcm9zb2Z0IFlhSGVpLCBIZWx2ZXRpY2EsIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEyIiBmaWxsPSIjODY4Njg2Ij7mmI7noa7ovpPlhaXjgIHovpPlh7rkuI7otKPku7vkuro8L3RleHQ+CjxyZWN0IHg9IjM1MCIgeT0iMTQwIiB3aWR0aD0iMjQwIiBoZWlnaHQ9IjEwMCIgcng9IjEyIiBmaWxsPSIjRkZGRkZGIiBzdHJva2U9IiNFNUU1RTUiLz4KPGNpcmNsZSBjeD0iMzgwIiBjeT0iMTc0IiByPSIxMyIgZmlsbD0iI0U4RjBGRSIvPgo8dGV4dCB4PSIzODAiIHk9IjE3OCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IlBpbmdGYW5nIFNDLCBNaWNyb3NvZnQgWWFIZWksIEhlbHZldGljYSwgQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTMiIGZvbnQtd2VpZ2h0PSI2MDAiIGZpbGw9IiMzNzcwRjciPjI8L3RleHQ+Cjx0ZXh0IHg9IjQwNCIgeT0iMTc5IiBmb250LWZhbWlseT0iUGluZ0ZhbmcgU0MsIE1pY3Jvc29mdCBZYUhlaSwgSGVsdmV0aWNhLCBBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNSIgZm9udC13ZWlnaHQ9IjUwMCIgZmlsbD0iIzFGMUYxRiI+5pa55qGI6K6+6K6hPC90ZXh0Pgo8dGV4dCB4PSIzODAiIHk9IjIxNCIgZm9udC1mYW1pbHk9IlBpbmdGYW5nIFNDLCBNaWNyb3NvZnQgWWFIZWksIEhlbHZldGljYSwgQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTIiIGZpbGw9IiM4Njg2ODYiPuamguimgeiuvuiuoeS4juaOpeWPo+WumuS5iTwvdGV4dD4KPHJlY3QgeD0iNjUwIiB5PSIxNDAiIHdpZHRoPSIyNDAiIGhlaWdodD0iMTAwIiByeD0iMTIiIGZpbGw9IiNGRkZGRkYiIHN0cm9rZT0iI0U1RTVFNSIvPgo8Y2lyY2xlIGN4PSI2ODAiIGN5PSIxNzQiIHI9IjEzIiBmaWxsPSIjRThGMEZFIi8+Cjx0ZXh0IHg9IjY4MCIgeT0iMTc4IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iUGluZ0ZhbmcgU0MsIE1pY3Jvc29mdCBZYUhlaSwgSGVsdmV0aWNhLCBBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMyIgZm9udC13ZWlnaHQ9IjYwMCIgZmlsbD0iIzM3NzBGNyI+MzwvdGV4dD4KPHRleHQgeD0iNzA0IiB5PSIxNzkiIGZvbnQtZmFtaWx5PSJQaW5nRmFuZyBTQywgTWljcm9zb2Z0IFlhSGVpLCBIZWx2ZXRpY2EsIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE1IiBmb250LXdlaWdodD0iNTAwIiBmaWxsPSIjMUYxRjFGIj7ku7vliqHmi4bliIY8L3RleHQ+Cjx0ZXh0IHg9IjY4MCIgeT0iMjE0IiBmb250LWZhbWlseT0iUGluZ0ZhbmcgU0MsIE1pY3Jvc29mdCBZYUhlaSwgSGVsdmV0aWNhLCBBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMiIgZmlsbD0iIzg2ODY4NiI+5ouG5Yiw5Y+v54us56uL5Lqk5LuY55qE57KS5bqmPC90ZXh0Pgo8cmVjdCB4PSI5NTAiIHk9IjE0MCIgd2lkdGg9IjI0MCIgaGVpZ2h0PSIxMDAiIHJ4PSIxMiIgZmlsbD0iI0ZGRkZGRiIgc3Ryb2tlPSIjRTVFNUU1Ii8+CjxjaXJjbGUgY3g9Ijk4MCIgY3k9IjE3NCIgcj0iMTMiIGZpbGw9IiNFOEYwRkUiLz4KPHRleHQgeD0iOTgwIiB5PSIxNzgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJQaW5nRmFuZyBTQywgTWljcm9zb2Z0IFlhSGVpLCBIZWx2ZXRpY2EsIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEzIiBmb250LXdlaWdodD0iNjAwIiBmaWxsPSIjMzc3MEY3Ij40PC90ZXh0Pgo8dGV4dCB4PSIxMDA0IiB5PSIxNzkiIGZvbnQtZmFtaWx5PSJQaW5nRmFuZyBTQywgTWljcm9zb2Z0IFlhSGVpLCBIZWx2ZXRpY2EsIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE1IiBmb250LXdlaWdodD0iNTAwIiBmaWxsPSIjMUYxRjFGIj7lvIDlj5Hlrp7njrA8L3RleHQ+Cjx0ZXh0IHg9Ijk4MCIgeT0iMjE0IiBmb250LWZhbWlseT0iUGluZ0ZhbmcgU0MsIE1pY3Jvc29mdCBZYUhlaSwgSGVsdmV0aWNhLCBBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMiIgZmlsbD0iIzg2ODY4NiI+57yW56CB5LiO5Y2V5YWD5rWL6K+VPC90ZXh0Pgo8cmVjdCB4PSI1MCIgeT0iMzgwIiB3aWR0aD0iMjQwIiBoZWlnaHQ9IjEwMCIgcng9IjEyIiBmaWxsPSIjRkZGRkZGIiBzdHJva2U9IiNFNUU1RTUiLz4KPGNpcmNsZSBjeD0iODAiIGN5PSI0MTQiIHI9IjEzIiBmaWxsPSIjRThGMEZFIi8+Cjx0ZXh0IHg9IjgwIiB5PSI0MTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJQaW5nRmFuZyBTQywgTWljcm9zb2Z0IFlhSGVpLCBIZWx2ZXRpY2EsIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEzIiBmb250LXdlaWdodD0iNjAwIiBmaWxsPSIjMzc3MEY3Ij41PC90ZXh0Pgo8dGV4dCB4PSIxMDQiIHk9IjQxOSIgZm9udC1mYW1pbHk9IlBpbmdGYW5nIFNDLCBNaWNyb3NvZnQgWWFIZWksIEhlbHZldGljYSwgQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTUiIGZvbnQtd2VpZ2h0PSI1MDAiIGZpbGw9IiMxRjFGMUYiPuiHqua1i+mqjOivgTwvdGV4dD4KPHRleHQgeD0iODAiIHk9IjQ1NCIgZm9udC1mYW1pbHk9IlBpbmdGYW5nIFNDLCBNaWNyb3NvZnQgWWFIZWksIEhlbHZldGljYSwgQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTIiIGZpbGw9IiM4Njg2ODYiPueUqOS+i+mAmui/h+eOh+S4jue8uumZt+aUtuaVmzwvdGV4dD4KPHJlY3QgeD0iMzUwIiB5PSIzODAiIHdpZHRoPSIyNDAiIGhlaWdodD0iMTAwIiByeD0iMTIiIGZpbGw9IiNGRkZGRkYiIHN0cm9rZT0iI0U1RTVFNSIvPgo8Y2lyY2xlIGN4PSIzODAiIGN5PSI0MTQiIHI9IjEzIiBmaWxsPSIjRThGMEZFIi8+Cjx0ZXh0IHg9IjM4MCIgeT0iNDE4IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iUGluZ0ZhbmcgU0MsIE1pY3Jvc29mdCBZYUhlaSwgSGVsdmV0aWNhLCBBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMyIgZm9udC13ZWlnaHQ9IjYwMCIgZmlsbD0iIzM3NzBGNyI+NjwvdGV4dD4KPHRleHQgeD0iNDA0IiB5PSI0MTkiIGZvbnQtZmFtaWx5PSJQaW5nRmFuZyBTQywgTWljcm9zb2Z0IFlhSGVpLCBIZWx2ZXRpY2EsIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE1IiBmb250LXdlaWdodD0iNTAwIiBmaWxsPSIjMUYxRjFGIj7ogZTosIPpqozmlLY8L3RleHQ+Cjx0ZXh0IHg9IjM4MCIgeT0iNDU0IiBmb250LWZhbWlseT0iUGluZ0ZhbmcgU0MsIE1pY3Jvc29mdCBZYUhlaSwgSGVsdmV0aWNhLCBBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMiIgZmlsbD0iIzg2ODY4NiI+6Leo57O757uf6IGU6LCD5LiO6aqM5pS256Gu6K6kPC90ZXh0Pgo8cmVjdCB4PSI2NTAiIHk9IjM4MCIgd2lkdGg9IjI0MCIgaGVpZ2h0PSIxMDAiIHJ4PSIxMiIgZmlsbD0iI0ZGRkZGRiIgc3Ryb2tlPSIjRTVFNUU1Ii8+CjxjaXJjbGUgY3g9IjY4MCIgY3k9IjQxNCIgcj0iMTMiIGZpbGw9IiNFOEYwRkUiLz4KPHRleHQgeD0iNjgwIiB5PSI0MTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJQaW5nRmFuZyBTQywgTWljcm9zb2Z0IFlhSGVpLCBIZWx2ZXRpY2EsIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEzIiBmb250LXdlaWdodD0iNjAwIiBmaWxsPSIjMzc3MEY3Ij43PC90ZXh0Pgo8dGV4dCB4PSI3MDQiIHk9IjQxOSIgZm9udC1mYW1pbHk9IlBpbmdGYW5nIFNDLCBNaWNyb3NvZnQgWWFIZWksIEhlbHZldGljYSwgQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTUiIGZvbnQtd2VpZ2h0PSI1MDAiIGZpbGw9IiMxRjFGMUYiPueBsOW6puWPkeW4gzwvdGV4dD4KPHRleHQgeD0iNjgwIiB5PSI0NTQiIGZvbnQtZmFtaWx5PSJQaW5nRmFuZyBTQywgTWljcm9zb2Z0IFlhSGVpLCBIZWx2ZXRpY2EsIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEyIiBmaWxsPSIjODY4Njg2Ij7liIbmibnmlL7ph4/lubbop4Llr5/moLjlv4PmjIfmoIc8L3RleHQ+CjxyZWN0IHg9Ijk1MCIgeT0iMzgwIiB3aWR0aD0iMjQwIiBoZWlnaHQ9IjEwMCIgcng9IjEyIiBmaWxsPSIjRkZGRkZGIiBzdHJva2U9IiNFNUU1RTUiLz4KPGNpcmNsZSBjeD0iOTgwIiBjeT0iNDE0IiByPSIxMyIgZmlsbD0iI0U4RjBGRSIvPgo8dGV4dCB4PSI5ODAiIHk9IjQxOCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IlBpbmdGYW5nIFNDLCBNaWNyb3NvZnQgWWFIZWksIEhlbHZldGljYSwgQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTMiIGZvbnQtd2VpZ2h0PSI2MDAiIGZpbGw9IiMzNzcwRjciPjg8L3RleHQ+Cjx0ZXh0IHg9IjEwMDQiIHk9IjQxOSIgZm9udC1mYW1pbHk9IlBpbmdGYW5nIFNDLCBNaWNyb3NvZnQgWWFIZWksIEhlbHZldGljYSwgQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTUiIGZvbnQtd2VpZ2h0PSI1MDAiIGZpbGw9IiMxRjFGMUYiPuS6pOS7mOW9kuahozwvdGV4dD4KPHRleHQgeD0iOTgwIiB5PSI0NTQiIGZvbnQtZmFtaWx5PSJQaW5nRmFuZyBTQywgTWljcm9zb2Z0IFlhSGVpLCBIZWx2ZXRpY2EsIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEyIiBmaWxsPSIjODY4Njg2Ij7kuqTku5jniannmbvorrDkuI7niYjmnKznlZnlrZg8L3RleHQ+Cjwvc3ZnPg==\" width=\"1240\" height=\"620\" alt=\"端到端交付链路示意图：需求澄清、方案设计、任务拆分、开发实现、自测验证、联调验收、灰度发布、交付归档 共 8 个阶段\">",
        "                <div class=\"giencoder-image-mask\" aria-hidden=\"true\"><svg viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z\"/><circle cx=\"12\" cy=\"12\" r=\"3\"/></svg><span>预览</span></div>",
        "              </div>",
        "            </div>",
        "            <p>从业务方原始需求进入系统开始，到最终交付物归档为止，完整链路包含需求澄清、方案设计、任务拆分、开发实现、自测验证、联调验收、灰度发布与交付归档共 8 个阶段。每个阶段都需要明确输入、输出、责任人与准入准出条件，避免出现“任务已发起但无人认领”或“交付物缺失但流程已关闭”的情况。</p>",
        "            <p>第二步：定义状态流转规则（启动整个流程）</p>",
        "            <p>状态标识采用“交通灯”模式，方便直观管理：</p>",
        "            <ul>",
        "              <li>未开始：任务尚未启动。</li>",
        "              <li>进行中：任务已启动，正在执行。</li>",
        "              <li>已完成：任务成功完成并通过质量门禁。</li>",
        "              <li>阻塞/异常：任务执行受阻，需要人工介入处理。</li>",
        "            </ul>",
        "            <p>第三步：设定交付物标准</p>",
        "            <p>每类任务需产出对应交付物并登记到任务详情：需求类任务产出需求说明与验收标准；设计类任务产出概要设计与接口定义；开发类任务产出代码与单元测试报告；验证类任务产出测试用例与缺陷清单。所有交付物需带版本号与责任人，便于回溯。</p>",
        "            <p>第四步：明确质量门禁</p>",
        "            <p>进入“已完成”前必须通过三项门禁检查：交付物齐全且可访问、关键路径有自动化验证覆盖、遗留缺陷已评估且不影响验收。任一门禁未通过，任务自动回退到“进行中”并通知责任人。</p>",
        "          </div>",
        "        </div>",
        "        <div class=\"td-expand\"><span class=\"td-expand-line\"></span><button class=\"giencoder-btn giencoder-btn-text giencoder-btn-size-small td-expand-btn\" type=\"button\" aria-expanded=\"false\" aria-controls=\"td-desc-body\" data-td-desc-toggle=\"1\">展开全文</button><span class=\"td-expand-line\"></span></div>",
        "        <section class=\"td-sec\">",
        "          <div class=\"td-sec-head\"><svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M2.9 5.5v4a3.5 3.5 0 0 0 7 0v-4a3.5 3.5 0 0 0-7 0z\"/><path d=\"M6.4 6.2v3.6a1.75 1.75 0 0 0 3.5 0V6.2\"/><path d=\"M12.7 3.2v7.6\"/></svg>2个附件</div>",
        "          <div class=\"td-files\">",
        "            <a class=\"td-file\" href=\"#\" title=\"端到端流程初始化：用户输入业务流程并触发全链路交付.docx\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M8 1.5H2.6A1.1 1.1 0 0 0 1.5 2.6V12.9A1.1 1.1 0 0 0 2.6 14H10.4A1.1 1.1 0 0 0 11.5 12.9V5.75Z\"/><path d=\"M7 1.5v4.25H11.5\"/><path d=\"M3.7 7.6h4.5\"/><path d=\"M3.7 10.2h3.1\"/></svg></span><span class=\"td-file-tx\">端到端流程初始化：用户输入业务流程并触发全链路交付.docx</span></a>",
        "            <a class=\"td-file\" href=\"#\" title=\"TaskBoard.png\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 16 16\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M8 1.5H2.6A1.1 1.1 0 0 0 1.5 2.6V12.9A1.1 1.1 0 0 0 2.6 14H10.4A1.1 1.1 0 0 0 11.5 12.9V5.75Z\"/><path d=\"M7 1.5v4.25H11.5\"/><path d=\"M3.7 7.6h4.5\"/><path d=\"M3.7 10.2h3.1\"/></svg></span><span class=\"td-file-tx\">TaskBoard.png</span></a>",
        "          </div>",
        "        </section>",
        "        <section class=\"td-sec\">",
        "          <div class=\"td-sec-head\"><svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M2.6 12.6V5.3a1.5 1.5 0 0 1 1.5-1.5h2.4c.5 0 .97.25 1.25.67l.5.76c.28.42.75.67 1.25.67h3.9a1.5 1.5 0 0 1 1.5 1.5v5.2\"/><path d=\"M4.7 8.4h7.2a1.1 1.1 0 0 1 1.1 1.1v2a1.1 1.1 0 0 1-1.1 1.1H4.7a1.1 1.1 0 0 1-1.1-1.1v-2a1.1 1.1 0 0 1 1.1-1.1z\"/></svg>3个 AI 产物</div>",
        "          <div class=\"td-files\">",
        "            <a class=\"td-file td-file--lg\" href=\"#\" title=\"prd-template.html\"><span class=\"td-file-ico is-web\"><svg viewBox=\"0 0 24 24\" width=\"24\" height=\"24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.8\" aria-hidden=\"true\"><circle cx=\"12\" cy=\"12\" r=\"9.6\"/><ellipse cx=\"12\" cy=\"12\" rx=\"3.4\" ry=\"9.6\"/><path d=\"M2.4 12h19.2\" stroke-linecap=\"round\"/></svg></span><span class=\"td-file-sep\" aria-hidden=\"true\"></span><span class=\"td-file-body\"><span class=\"td-file-tx\">prd-template.html</span><span class=\"td-file-size\">128KB</span></span></a>",
        "            <a class=\"td-file td-file--lg\" href=\"#\" title=\"端到端初始化 - 任务分析报告.md\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 24 24\" width=\"24\" height=\"24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.45\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M4.5 1.5H18.8A1.5 1.5 0 0 1 20.3 3V15.6L16.6 21H4.5A1.5 1.5 0 0 0 3 19.5V3A1.5 1.5 0 0 1 4.5 1.5Z\"/><path d=\"M15 21v-5.25H20.3\"/><path d=\"M7.5 7.2h7.5\"/><path d=\"M7.5 11h7.5\"/><path d=\"M7.5 14.7h3.5\"/></svg></span><span class=\"td-file-sep\" aria-hidden=\"true\"></span><span class=\"td-file-body\"><span class=\"td-file-tx\">端到端初始化 - 任务分析报告.md</span><span class=\"td-file-size\">128KB</span></span></a>",
        "            <a class=\"td-file td-file--lg\" href=\"#\" title=\"spec-template.md\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 24 24\" width=\"24\" height=\"24\" aria-hidden=\"true\"><path class=\"td-ico-md-body\" d=\"M3 1h12v5.5h6V23H3z\"/><path class=\"td-ico-md-fold\" d=\"M15 1l6 5.5h-6z\"/><path class=\"td-ico-md-mark\" d=\"M5 16.5v-5l3.35 3.5L11.7 11.5v5\"/><path class=\"td-ico-md-mark\" d=\"M15.9 11.5v5\"/><path class=\"td-ico-md-mark is-solid\" d=\"M13.9 14.15h4l-2 2.5z\"/></svg></span><span class=\"td-file-sep\" aria-hidden=\"true\"></span><span class=\"td-file-body\"><span class=\"td-file-tx\">spec-template.md</span><span class=\"td-file-size\">128KB</span></span></a>",
        "          </div>",
        "        </section>",
        "        <section class=\"td-sec\">",
        "          <div class=\"td-sec-head\"><svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M2.6 12.6V5.3a1.5 1.5 0 0 1 1.5-1.5h2.4c.5 0 .97.25 1.25.67l.5.76c.28.42.75.67 1.25.67h3.9a1.5 1.5 0 0 1 1.5 1.5v5.2\"/><path d=\"M4.7 8.4h7.2a1.1 1.1 0 0 1 1.1 1.1v2a1.1 1.1 0 0 1-1.1 1.1H4.7a1.1 1.1 0 0 1-1.1-1.1v-2a1.1 1.1 0 0 1 1.1-1.1z\"/></svg>文件</div>",
        "          <div class=\"td-files\">",
        "            <a class=\"td-file td-file--lg\" href=\"#\" title=\"概要设计-Steps.md\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 24 24\" width=\"24\" height=\"24\" aria-hidden=\"true\"><path class=\"td-ico-md-body\" d=\"M3 1h12v5.5h6V23H3z\"/><path class=\"td-ico-md-fold\" d=\"M15 1l6 5.5h-6z\"/><path class=\"td-ico-md-mark\" d=\"M5 16.5v-5l3.35 3.5L11.7 11.5v5\"/><path class=\"td-ico-md-mark\" d=\"M15.9 11.5v5\"/><path class=\"td-ico-md-mark is-solid\" d=\"M13.9 14.15h4l-2 2.5z\"/></svg></span><span class=\"td-file-sep\" aria-hidden=\"true\"></span><span class=\"td-file-body\"><span class=\"td-file-tx\">概要设计-Steps.md</span><span class=\"td-file-size\">17KB</span></span></a>",
        "          </div>",
        "        </section>",
        "      </div>",
        "      <aside class=\"td-side\" aria-label=\"任务属性与动态\">",
        "        <section class=\"td-side-attr\">",
        "          <h2>任务属性</h2>",
        "          <div class=\"td-attr\">",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">状态</span><span class=\"td-attr-v\"><span class=\"giencoder-badge giencoder-badge-status\"><span class=\"giencoder-badge-status-dot giencoder-badge-status-processing\"></span><span class=\"giencoder-badge-status-text\">进行中</span></span></span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">执行人</span><span class=\"td-attr-v\">邵禹铭</span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">优先级</span><span class=\"td-attr-v\"><span class=\"giencoder-tag giencoder-tag-danger td-tag-prio\"><span class=\"giencoder-tag-content\">高优先级</span></span></span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">项目</span><span class=\"td-attr-v\">演练指挥系统</span></div>",
        "            <div class=\"td-attr-row is-wrap\"><span class=\"td-attr-k\">来源需求</span><span class=\"td-attr-v\"><a class=\"td-attr-link\" href=\"#\"><svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6.4 9.6a2.6 2.6 0 0 0 3.7 0l2-2a2.6 2.6 0 0 0-3.7-3.7l-1 1\"/><path d=\"M9.6 6.4a2.6 2.6 0 0 0-3.7 0l-2 2a2.6 2.6 0 0 0 3.7 3.7l1-1\"/></svg>GienX端到端初始化：用户输入业务流程描述，自动生成需求条目并触发全链路交付</a></span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">实际开始</span><span class=\"td-attr-v\">2026/08/01 10:12</span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">实际完成</span><span class=\"td-attr-v\">2026/08/12 15:27</span></div>",
        "          </div>",
        "        </section>",
        "        <section class=\"td-side-dyn\">",
        "          <h2>任务动态</h2>",
        "          <ul class=\"td-tl\">",
        "            <li><div class=\"td-tl-line1\"><span class=\"td-tl-who\">Agent</span><span class=\"td-tl-what\">完成了任务开发</span></div><span class=\"td-tl-time\">刚刚</span></li>",
        "            <li><div class=\"td-tl-line1\"><span class=\"td-tl-who\">Agent</span><span class=\"td-tl-what\">已确认任务目标和优先级</span></div><span class=\"td-tl-time\">半小时前</span></li>",
        "            <li><div class=\"td-tl-line1\"><span class=\"td-tl-who\">邵禹铭</span><span class=\"td-tl-what\">状态更新为进行中</span></div><span class=\"td-tl-time\">昨天 10:02</span></li>",
        "            <li><div class=\"td-tl-line1\"><span class=\"td-tl-who\">邵禹铭</span><span class=\"td-tl-what\">补充了需求说明材料</span></div><span class=\"td-tl-time\">08/12 09:27</span></li>",
        "            <li><div class=\"td-tl-line1\"><span class=\"td-tl-who\">系统</span><span class=\"td-tl-what\">已同步最新处理进展</span></div><span class=\"td-tl-time\">08/11 16:51</span></li>",
        "          </ul>",
        "        </section>",
        "        <section class=\"td-side-foot\" aria-label=\"任务记录信息\">",
        "          <div class=\"td-attr\">",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">创建者</span><span class=\"td-attr-v\">秦怡</span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">创建时间</span><span class=\"td-attr-v\">2026/08/12 15:27</span></div>",
        "            <div class=\"td-attr-row\"><span class=\"td-attr-k\">最后更新</span><span class=\"td-attr-v\">半小时前</span></div>",
        "          </div>",
        "        </section>",
        "      </aside>",
        "    </div>",
        "  </section>",
        "  <div class=\"td-gutter\" role=\"separator\" tabindex=\"0\" aria-orientation=\"vertical\" aria-label=\"调整 AI 会话栏宽度\" aria-valuenow=\"480\" aria-valuemin=\"48\" aria-valuemax=\"1200\" data-td-gutter=\"1\"><span class=\"td-gutter-bar\"></span></div>",
        "  <aside class=\"td-right\" aria-label=\"AI 会话\">",
        "    <div class=\"td-right-inner\">",
        "      <header class=\"td-right-bar\">",
        "        <div class=\"td-right-head\">",
        "          <div class=\"td-right-title\">端到端流程初始化：用户输入业务流程并触发全链路交付</div>",
        "          <div class=\"td-right-time\">2026/08/01 11:26</div>",
        "        </div>",
        "        <div class=\"td-right-acts\">",
        "          <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round-btn\" type=\"button\" aria-label=\"新会话\"><svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"lucide lucide-plus\" aria-hidden=\"true\"><path d=\"M5 12h14\"/><path d=\"M12 5v14\"/></svg></button>",
        "          <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round-btn\" type=\"button\" aria-label=\"会话历史\"><svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"lucide lucide-history\" aria-hidden=\"true\"><path d=\"M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8\"/><path d=\"M3 3v5h5\"/><path d=\"M12 7v5l4 2\"/></svg></button>",
        "          <button class=\"giencoder-btn giencoder-btn-secondary giencoder-btn-size-default giencoder-btn-icon td-round-btn\" type=\"button\" aria-label=\"全屏\" aria-pressed=\"false\" title=\"全屏\" data-td-fullscreen=\"1\"><svg class=\"td-ico-max\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M8 3H5a2 2 0 0 0-2 2v3\"/><path d=\"M21 8V5a2 2 0 0 0-2-2h-3\"/><path d=\"M3 16v3a2 2 0 0 0 2 2h3\"/><path d=\"M16 21h3a2 2 0 0 0 2-2v-3\"/></svg><svg class=\"td-ico-min\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M8 3v3a2 2 0 0 1-2 2H3\"/><path d=\"M21 8h-3a2 2 0 0 1-2-2V3\"/><path d=\"M3 16h3a2 2 0 0 1 2 2v3\"/><path d=\"M16 21v-3a2 2 0 0 1 2-2h3\"/></svg></button>",
        "        </div>",
        "      </header>",
        "      <div class=\"td-chat\">",
        "        <div class=\"td-chat-inner\">",
        "          <div class=\"td-msg-user\">请帮我先分析一下这个任务</div>",
        "          <div class=\"td-msg-ai\">",
        "            <div class=\"td-ai-head\">",
        "              <span class=\"td-ai-avatar\"><svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M8 2.2l1.8 4 4 1.8-4 1.8L8 13.8l-1.8-4-4-1.8 4-1.8z\"/></svg></span>",
        "              <span class=\"td-ai-name\">艾迪</span>",
        "            </div>",
        "            <div class=\"td-ai-meta\">",
        "              <a href=\"#\"><svg viewBox=\"0 0 16 16\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M6.4 9.6a2.6 2.6 0 0 0 3.7 0l2-2a2.6 2.6 0 0 0-3.7-3.7l-1 1\"/><path d=\"M9.6 6.4a2.6 2.6 0 0 0-3.7 0l-2 2a2.6 2.6 0 0 0 3.7 3.7l1-1\"/></svg>思考过程</a>",
        "              <span class=\"td-sep\"></span>",
        "              <a href=\"#\">任务完成，耗时 28m12s</a>",
        "            </div>",
        "            <p>好的，收到您的需求。这是一个典型的“从需求到交付”的端到端流程初始化场景。我将为您设计一个完整的交付状态跟踪表，并定义启动整个流程所需的初始状态和关键节点。</p>",
        "            <p>我先把几个核心不确定性列出来，请你选择倾向，不确定的地方我会标注我的判断。</p>",
        "            <div class=\"td-ai-file\"><span class=\"td-file-ico\"><svg viewBox=\"0 0 24 24\" width=\"24\" height=\"24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.45\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M4.5 1.5H18.8A1.5 1.5 0 0 1 20.3 3V15.6L16.6 21H4.5A1.5 1.5 0 0 0 3 19.5V3A1.5 1.5 0 0 1 4.5 1.5Z\"/><path d=\"M15 21v-5.25H20.3\"/><path d=\"M7.5 7.2h7.5\"/><path d=\"M7.5 11h7.5\"/><path d=\"M7.5 14.7h3.5\"/></svg></span><span class=\"td-file-sep\" aria-hidden=\"true\"></span><span class=\"td-file-body\"><span class=\"td-file-tx\">端到端初始化 - 任务分析报告.md</span><span class=\"td-file-size\">128KB</span></span></div>",
        "            <div class=\"td-ai-foot\"><span class=\"td-ai-foot-item\"><span class=\"td-ai-foot-ico\"><svg viewBox=\"0 0 12 12\" width=\"12\" height=\"12\" fill=\"none\" aria-hidden=\"true\"><circle cx=\"6\" cy=\"6\" r=\"6\" fill=\"currentColor\"/><path class=\"td-ico-check\" d=\"M3.3 6.1l1.9 1.85 3.5-3.75\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg></span><span>输出完成</span></span><span class=\"td-sep\"></span><span class=\"td-ai-foot-item\"><span class=\"td-ai-foot-ico\"><svg viewBox=\"0 0 12 12\" width=\"12\" height=\"12\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.1\" stroke-linecap=\"round\" aria-hidden=\"true\"><circle cx=\"6\" cy=\"6\" r=\"5\"/><path d=\"M6 6l2.4-2.4\"/><circle cx=\"6\" cy=\"6\" r=\".75\" fill=\"currentColor\" stroke=\"none\"/><path d=\"M3.5 3.9l.75.75\"/><path d=\"M2.9 6.5h1.05\"/><path d=\"M9.1 6.5H8.05\"/></svg></span><span>Token 速率：256/s</span></span></div>",
        "          </div>",
        "        </div>",
        "      </div>",
        "        <!-- 复用基础工作台的对话框模块（pages/base.html，结构与类名一致） -->",
        "        <div class=\"td-composer\">",
        "          <div class=\"relative flex w-full flex-col rounded-[16px] border bg-white p-3 transition-colors\" style=\"border-color: var(--color-border-2); box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);\">",
        "            <textarea rows=\"1\" placeholder=\"描述你的任务，/ 调用技能，@引用文件\" aria-label=\"输入消息\" class=\"min-w-0 resize-none bg-transparent text-sm leading-[22px] [color:var(--color-text-1)] outline-none placeholder:[color:var(--color-text-3)] min-h-[96px]\"></textarea>",
        "            <div class=\"mt-auto flex items-center justify-between\">",
        "              <div class=\"flex items-center gap-[8px]\">",
        "                <div class=\"giencoder-select\" style=\"flex-direction: row; align-items: flex-start; position: relative;\">",
        "                  <button type=\"button\" aria-label=\"添加\" aria-haspopup=\"menu\" aria-expanded=\"false\" data-td-add-btn=\"1\" class=\"flex size-8 items-center justify-center rounded-full border border-[var(--color-border-1)] text-[var(--color-text-2)] transition-colors hover:bg-[var(--color-fill-1)] hover:[color:var(--color-text-1)]\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"lucide lucide-plus size-[14px]\" aria-hidden=\"true\"><path d=\"M5 12h14\"></path><path d=\"M12 5v14\"></path></svg></button>",
        "                  <div role=\"menu\" aria-label=\"添加内容\" class=\"td-add-pop\" data-td-add-pop=\"1\" hidden>",
        "                    <div role=\"menuitem\" tabindex=\"-1\" class=\"td-add-item\" data-td-add=\"file\"><svg viewBox=\"0 0 14 14\" width=\"14\" height=\"14\" fill=\"currentColor\" fill-rule=\"evenodd\" aria-hidden=\"true\"><path d=\"M1.5,1.9C1.5,1.2,2.1,0.6,2.8,0.6C2.8,0.6,9.8,0.6,9.8,0.6C9.8,0.6,12.4,3.2,12.4,3.2C12.4,3.2,12.4,12.2,12.4,12.2C12.4,12.9,11.9,13.5,11.2,13.5C11.2,13.5,2.8,13.5,2.8,13.5C2.1,13.5,1.5,12.9,1.5,12.2C1.5,12.2,1.5,1.9,1.5,1.9C1.5,1.9,1.5,1.9,1.5,1.9ZM9.3,1.9C9.3,1.9,2.8,1.9,2.8,1.9C2.8,1.9,2.8,12.2,2.8,12.2C2.8,12.2,11.2,12.2,11.2,12.2C11.2,12.2,11.2,3.8,11.2,3.8C11.2,3.8,9.3,1.9,9.3,1.9C9.3,1.9,9.3,1.9,9.3,1.9ZM9.5,6.7C9.5,6.7,4.4,6.7,4.4,6.7C4.4,6.7,4.4,5.4,4.4,5.4C4.4,5.4,9.5,5.4,9.5,5.4C9.5,6.7,9.5,6.7,9.5,6.7C9.5,6.7,9.5,6.7,9.5,6.7ZM7.6,9.3C7.6,9.3,4.4,9.3,4.4,9.3C4.4,9.3,4.4,8,4.4,8C4.4,8,7.6,8,7.6,8C7.6,9.3,7.6,9.3,7.6,9.3C7.6,9.3,7.6,9.3,7.6,9.3Z\"/></svg><span>添加本地文件</span></div>",
        "                    <span class=\"td-add-sep\" aria-hidden=\"true\"></span>",
        "                    <div role=\"menuitem\" tabindex=\"-1\" class=\"td-add-item\" data-td-add=\"kb\"><svg viewBox=\"0 0 14 14\" width=\"14\" height=\"14\" fill=\"currentColor\" fill-rule=\"evenodd\" aria-hidden=\"true\"><path d=\"M12.2,10.8L2.9,10.8C2.5,10.8,2.2,11.1,2.2,11.4C2.2,11.8,2.5,12.1,2.9,12.1L12.2,12.1L12.2,13.4L2.9,13.4C1.8,13.4,1,12.5,1,11.4L1,1.8C1,1.4,1.1,1.1,1.4,0.9C1.6,0.6,1.9,0.5,2.2,0.5L12.2,0.5L12.2,10.8ZM2.2,9.5C2.3,9.5,2.4,9.5,2.6,9.5L10.9,9.5L10.9,1.8L2.2,1.8L2.2,9.5ZM4.1,5L9.1,5L9.1,3.7L4.1,3.7L4.1,5Z\"/></svg><span>知识库</span></div>",
        "                  </div>",
        "                </div>",
        "                <button type=\"button\" aria-label=\"技能\" aria-haspopup=\"listbox\" aria-expanded=\"false\" data-td-skill-btn=\"1\" class=\"flex size-8 items-center justify-center rounded-full border border-[var(--color-border-1)] text-[var(--color-text-2)] transition-colors hover:bg-[var(--color-fill-1)] hover:[color:var(--color-text-1)]\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"lucide lucide-wrench size-[14px]\" aria-hidden=\"true\"><path d=\"M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.106-3.105c.32-.322.863-.22.983.218a6 6 0 0 1-8.259 7.057l-7.91 7.91a1 1 0 0 1-2.999-3l7.91-7.91a6 6 0 0 1 7.057-8.259c.438.12.54.662.219.984z\"></path></svg></button>",
        "                <div class=\"avatar-wrap relative flex items-center\">",
        "                  <button type=\"button\" aria-label=\"数字分身\" aria-pressed=\"true\" class=\"flex h-8 items-center gap-[2px] rounded-full px-3 py-[5px] text-[14px] leading-[19px] transition-colors\" style=\"background: rgb(236, 242, 255); color: rgb(55, 112, 247); border: 1px solid rgb(211, 226, 255);\"><svg viewBox=\"0 0 14 14\" width=\"14\" height=\"14\" class=\"size-[14px]\"><path d=\"M6.988754947683716,13.43000001192093C5.103876847683716,13.43000001192093,3.4284298476837156,12.17341601192093,2.9048526476837155,10.497968511920929L2.590706447683716,10.812115011920929C2.381275537683716,11.02154501192093,1.9624137876837158,11.02154501192093,1.6482674076837158,10.812115011920929C1.334121017683716,10.602683011920929,1.4388364836837158,10.183822411920929,1.6482674076837158,9.869675411920928L2.6954218476837157,8.822521011920928L2.6954218476837157,7.984796811920929C2.2765598876837156,7.670650811920929,2.067129017683716,7.147073111920929,2.067129017683716,6.623495911920929L2.067129017683716,3.586747711920929C2.067129017683716,2.539593411920929,2.9048526476837155,1.701869811920929,3.952006847683716,1.701869811920929L6.360462447683716,1.701869811920929L6.360462447683716,1.1782926319209288C6.360462447683716,0.8641463219209289,6.674608947683716,0.550000011920929,6.988754947683716,0.550000011920929C7.302901547683716,0.550000011920929,7.617047547683716,0.8641463219209289,7.617047547683716,1.1782926319209288L7.617047547683716,1.701869811920929L10.025503347683715,1.701869811920929C11.072657847683717,1.701869811920929,11.910381047683716,2.539593411920929,11.910381047683716,3.586747711920929L11.910381047683716,6.623495911920929C11.910381047683716,7.147073111920929,11.700949047683716,7.670649811920929,11.282088547683715,7.984796811920929L11.282088547683715,8.822521011920928L12.329243047683716,9.869675411920928C12.538674047683715,10.079107111920928,12.538674047683715,10.497968511920929,12.329243047683716,10.812115011920929C12.119811047683715,11.126262011920929,11.700951047683716,11.02154501192093,11.386802947683716,10.812115011920929L11.072657847683717,10.497968511920929C10.549079147683717,12.17341601192093,8.873632647683717,13.43000001192093,6.988754947683716,13.43000001192093ZM3.9520075476837158,9.13666611192093C3.9520075476837158,10.81211401192093,5.313308247683716,12.173413011920928,6.988754947683716,12.173413011920928C8.664201947683715,12.173413011920928,10.025503347683715,10.81211401192093,10.025503347683715,9.13666611192093L10.025503347683715,8.50837351192093L3.9520075476837158,8.50837351192093L3.9520075476837158,9.13666611192093ZM3.9520075476837158,3.063170711920929C3.6378612476837158,3.063170711920929,3.3237144476837157,3.2726017119209287,3.3237144476837157,3.586747911920929L3.3237144476837157,6.623495911920929C3.3237144476837157,6.937641911920929,3.6378610476837157,7.251788411920929,3.952006847683716,7.251788411920929L10.025502447683715,7.251788411920929C10.339648447683716,7.251788411920929,10.549078247683715,7.042357311920929,10.549078247683715,6.728210711920929L10.549078247683715,3.586747511920929C10.549078247683715,3.272601211920929,10.339647547683716,3.0631702119209288,10.025502447683715,3.0631702119209288L3.9520075476837158,3.063170711920929ZM8.873633647683715,6.099919111920929C8.559487547683716,6.099919111920929,8.245341047683716,5.785772111920929,8.245341047683716,5.471626611920929L8.245341047683716,4.843334011920929C8.140625747683716,4.424471911920929,8.454771747683715,4.1103256119209295,8.873633647683715,4.1103256119209295C9.292495947683715,4.1103256119209295,9.501925747683716,4.424471911920929,9.501925747683716,4.738618211920929L9.501925747683716,5.366911211920929C9.501925747683716,5.785772111920929,9.187779647683715,6.099919111920929,8.873633647683715,6.099919111920929ZM5.103877547683716,6.099919111920929C4.789731547683716,6.099919111920929,4.475585247683716,5.785772111920929,4.475585247683716,5.471626611920929L4.475585247683716,4.843334011920929C4.475585247683716,4.424471911920929,4.789731547683716,4.1103256119209295,5.103877547683716,4.1103256119209295C5.418023847683716,4.1103256119209295,5.732170347683716,4.424471911920929,5.732170347683716,4.738618211920929L5.732170347683716,5.366911211920929C5.836885647683716,5.785772111920929,5.5227391476837155,6.099919111920929,5.103877547683716,6.099919111920929Z\" fill=\"currentColor\" fill-rule=\"evenodd\"></path></svg>艾迪</button>",
        "                  <div role=\"tooltip\" class=\"avatar-tooltip\">停用数字分身</div>",
        "                </div>",
        "                <div class=\"giencoder-select\" style=\"width: 96px; flex-shrink: 0;\">",
        "                  <div class=\"giencoder-select-view select-view-ghost\" tabindex=\"0\" role=\"combobox\" aria-haspopup=\"listbox\" aria-expanded=\"false\" style=\"height: 32px; min-height: 32px; border: 1px solid var(--color-border-1); border-radius: 32px; background-color: transparent; box-shadow: none; padding: 5px 12px; gap: 4px;\">",
        "                    <div class=\"giencoder-select-selection\" style=\"gap: 4px;\"><span class=\"giencoder-select-view-text\">标准模式</span></div>",
        "                    <span class=\"giencoder-select-suffix\"><svg viewBox=\"0 0 12 12\" width=\"12\" height=\"12\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.4\" stroke-linecap=\"round\"><path d=\"M2.6 4.6L6 8l3.4-3.4\"/></svg></span>",
        "                  </div>",
        "                  <div class=\"giencoder-select-popup\">",
        "                    <ul class=\"giencoder-select-option-list\" role=\"listbox\">",
        "                      <li class=\"giencoder-select-option giencoder-select-option-selected\" role=\"option\" aria-selected=\"true\">标准模式</li>",
        "                      <li class=\"giencoder-select-option\" role=\"option\" aria-selected=\"false\">专家模式</li>",
        "                    </ul>",
        "                  </div>",
        "                </div>",
        "              </div>",
        "              <div class=\"flex items-center gap-2\">",
        "                <div class=\"giencoder-select\" style=\"width: fit-content; max-width: 200px; flex-shrink: 0; margin-left: auto;\">",
        "                  <div class=\"giencoder-select-view select-view-ghost\" tabindex=\"0\" role=\"combobox\" aria-haspopup=\"listbox\" aria-expanded=\"false\" style=\"height: 32px; min-height: 32px; border: none; border-radius: 32px; gap: 2px; padding: 0 12px;\">",
        "                    <div class=\"giencoder-select-selection\" style=\"gap: 2px;\"><span class=\"giencoder-select-view-text\">DeepSeek-V4-Pro</span></div>",
        "                    <span class=\"giencoder-select-suffix\"><svg viewBox=\"0 0 12 12\" width=\"12\" height=\"12\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.4\" stroke-linecap=\"round\"><path d=\"M2.6 4.6L6 8l3.4-3.4\"/></svg></span>",
        "                  </div>",
        "                  <div class=\"giencoder-select-popup\">",
        "                    <ul class=\"giencoder-select-option-list\" role=\"listbox\" aria-label=\"大模型选择\">",
        "                      <li class=\"giencoder-select-option giencoder-select-option-selected\" role=\"option\" aria-selected=\"true\">DeepSeek-V4-Pro</li>",
        "                      <li class=\"giencoder-select-option\" role=\"option\" aria-selected=\"false\">GLM-5.2-公司共用</li>",
        "                      <li class=\"giencoder-select-option giencoder-select-option-disabled\" role=\"option\" aria-selected=\"false\" aria-disabled=\"true\">Qwen 3.8-max</li>",
        "                      <li class=\"giencoder-select-option\" role=\"option\" aria-selected=\"false\">Kimi-2.6</li>",
        "                    </ul>",
        "                  </div>",
        "                </div>",
        "                <button type=\"button\" aria-label=\"优化提示词\" class=\"flex size-8 items-center justify-center rounded-full transition-colors hover:bg-[var(--color-fill-1)]\" style=\"background: rgb(255, 255, 255);\"><svg viewBox=\"0 0 14.08 14.06\" width=\"14\" height=\"14\" fill=\"none\"><path d=\"M9.1414957,4.6432233C8.8303785,4.9347887,8.3439808,4.9266973,8.0427332,4.6249452C7.7414865,4.3231936,7.7342105,3.8367827,8.0262985,3.5261555L9.7009659,1.8514888C10.009434,1.5430192,10.509562,1.5430192,10.818031,1.8514888C11.126502,2.1599586,11.126502,2.6600869,10.818032,2.9685569L9.1405592,4.6432233L9.1414957,4.6432233Z\" fill=\"#BEBEBE\"></path><path d=\"M11.878967,7.1103153L9.5091734,7.1103153C9.0621662,7.1256995,8.6914234,6.7674994,8.6914234,6.3202286C8.6914234,5.8729568,9.0621662,5.5147567,9.5091734,5.5301414L11.879902,5.5301414C12.326908,5.5147567,12.697651,5.8729568,12.697651,6.3202286C12.697649,6.7674994,12.326908,7.1256995,11.879902,7.1103153L11.878967,7.1103153Z\" fill=\"#BEBEBE\"></path><path d=\"M4.1137528,4.8761797C3.9033761,4.8776922,3.7011769,4.7947903,3.5524123,4.6460304L1.8777457,2.971364C1.569276,2.6628945,1.569276,2.162766,1.8777457,1.8542962C2.1862154,1.5458264,2.6863437,1.5458263,2.9948137,1.854296L4.6694798,3.5289626C4.8958349,3.7551589,4.9632897,4.0956059,4.8402843,4.3910227C4.717279,4.68644,4.4281397,4.8784089,4.1081395,4.8771148L4.1137528,4.8761797Z\" fill=\"#BEBEBE\"></path><path d=\"M6.3497601,0C6.7863712,0,7.1403146,0.35394344,7.1403146,0.79055488L7.1403146,3.1612837C7.1256599,3.5870585,6.7762556,3.9246454,6.3502278,3.9246454C5.9242005,3.9246454,5.5747943,3.5870588,5.5601397,3.1612837L5.5601397,0.79055488C5.5601397,0.35430831,5.9135146,0.00051608856,6.3497601,0Z\" fill=\"#BEBEBE\"></path><path d=\"M0.819619,5.5301414L3.1884768,5.5301414C3.6354835,5.5147562,4.0062251,5.8729568,4.0062251,6.3202286C4.0062251,6.7674994,3.6354835,7.1256995,3.1884768,7.1103153L0.81774795,7.1103153C0.37074119,7.1256995,0,6.7674994,0,6.3202286C2.5033659e-8,5.8729568,0.37074125,5.5147562,0.81774795,5.5301414L0.819619,5.5301414Z\" fill=\"#BEBEBE\"></path><path d=\"M3.5570905,7.9972339C3.8655162,7.6885071,4.3658547,7.6883845,4.6744308,7.9969606C4.9830074,8.3055372,4.9828858,8.8058758,4.6741581,9.1143007L2.9994922,10.788968C2.688375,11.08053,2.2019811,11.072435,1.9007362,10.770686C1.5994915,10.468936,1.5922134,9.9825287,1.8842953,9.6718998L3.5570905,7.9972339Z\" fill=\"#BEBEBE\"></path><path d=\"M6.3497601,8.6886187C6.7863712,8.6886187,7.1403146,9.0425615,7.1403146,9.4791737L7.1403146,11.849901C7.1256599,12.275676,6.7762556,12.613264,6.3502278,12.613264C5.9242005,12.613264,5.5747943,12.275676,5.5601397,11.849901L5.5601397,9.4791737C5.5601397,9.0429258,5.9135141,8.6891346,6.3497601,8.6886187Z\" fill=\"#BEBEBE\"></path><path d=\"M5.9540148,5.9240155C6.2626376,5.6159139,6.7624602,5.6159139,7.0710826,5.9240155L9.1424294,7.9953628L10.817097,9.6700287L13.785653,12.650749C14.077717,12.96138,14.070429,13.447771,13.769192,13.749513C13.467955,14.051255,12.981577,14.059359,12.670459,13.767816L5.9577575,7.0410843C5.6478443,6.7339692,5.6457491,6.2337155,5.9530797,5.9240155L5.9540148,5.9240155Z\" fill=\"#BEBEBE\"></path></svg></button>",
        "                <button type=\"button\" aria-label=\"发送\" disabled class=\"flex shrink-0 !size-8 !rounded-full !p-0 items-center justify-center transition-colors\" style=\"background: var(--color-fill-3); cursor: not-allowed; opacity: 0.5;\"><svg viewBox=\"8.82 10.73 14.08 11.38\" width=\"14\" height=\"14\" fill=\"none\"><path d=\"M9.028238606,34.839137L11.6378174,29.1173639C11.6825285,28.9479885,11.6825285,28.7663059,11.6378174,28.6000094L9.028238606,22.87514764C8.88469238,22.32391092,9.31768426,21.81578781,9.7224375,22.065230064L19.998936,28.4367857C20.267201,28.6030817,20.267201,29.1050444,19.998936,29.2713394L9.7224375,35.649054C9.31768426,35.898499,8.88469242,35.390374,9.028238606,34.839137Z\" fill=\"#FFFFFF\" transform=\"matrix(0,-1,1,0,-13,31)\"></path></svg></button>",
        "              </div>",
        "            </div>",
        "            <!-- 技能面板（★ 第 28 轮第 4 项）：结构与内容对齐 pages/base.html 实测面板。",
        "                 放在对话框根容器内、absolute 定位于其上方（bottom: calc(100% + 8px)）。 -->",
        "            <div class=\"giencoder-select td-skill-pop\" role=\"listbox\" aria-label=\"技能选择\" data-td-skill-pop=\"1\" hidden>",
        "              <div class=\"td-skill-list\">",
        "                <div class=\"td-skill-row is-goal is-active\" role=\"option\" tabindex=\"-1\"><span class=\"td-skill-ico is-goal\"><svg viewBox=\"0 0 14.076962 14.882011\" width=\"14\" height=\"14\" fill=\"currentColor\" aria-hidden=\"true\"><path d=\"M7.3,0.6C6.9,0.5,6.4,0.7,6.4,1.2L6.4,7.6C6.4,7.9,6.7,8.2,7,8.2C7.3,8.2,7.6,7.9,7.6,7.6L7.6,6.2L11.9,4C12.1,3.9,12.3,3.7,12.3,3.5C12.3,3.3,12.1,3.1,11.9,3L7.3,0.6ZM7.6,2.1L10.4,3.5L7.6,4.9L7.6,2.1ZM4.9,2.3C4.7,2.3,4.6,2.3,4.4,2.4C0,4.5,0.2,11,4.7,13C9.3,14.9,14.1,10.5,12.5,5.8C12.4,5.5,12.1,5.3,11.8,5.4C11.5,5.5,11.3,5.8,11.4,6.1C12.7,10,8.9,13.5,5.2,11.9C1.5,10.3,1.3,5.2,4.9,3.4C5.2,3.3,5.3,2.9,5.2,2.6C5.1,2.5,5,2.4,4.9,2.3ZM4.2,5.5C4.3,5.4,4.4,5.3,4.6,5.3C4.7,5.2,4.9,5.3,5,5.4C5.3,5.6,5.3,5.9,5.1,6.2C4.1,7.5,4.8,9.5,6.5,9.9C8.1,10.3,9.6,8.8,9.3,7.1C9.2,6.8,9.4,6.5,9.7,6.4C10.1,6.4,10.4,6.6,10.4,6.9C10.9,9.4,8.7,11.6,6.2,11C3.8,10.4,2.7,7.5,4.2,5.5Z\"/></svg></span><span class=\"td-skill-txt\"><span class=\"td-skill-name\">Goal</span><span class=\"td-skill-desc\">构建一个以实现目标为结果的任务，持续运行直到全部完成。</span></span></div>",
        "                <div class=\"td-skill-group\">技能 Skills</div>",
        "                <div class=\"td-skill-row\" role=\"option\" tabindex=\"-1\"><span class=\"td-skill-ico\"><svg viewBox=\"0 0 14 14\" width=\"12\" height=\"12\" aria-hidden=\"true\"><path d=\"M24.2,2.6C25.4,4.2,25.3,6.5,23.8,7.9C22.7,9.1,21.1,9.4,19.7,8.9L15.7,12.9C15.5,13,15.3,13,15.1,12.9L13.1,10.9C13,10.7,13,10.5,13.1,10.3L17.1,6.3C16.6,4.9,16.9,3.3,18.1,2.2C19.5,0.7,21.8,0.6,23.4,1.8L21,4.2L21.8,5L24.2,2.6ZM23.9,4.5L23.9,4.5L22.1,6.3C21.9,6.4,21.6,6.4,21.4,6.3L19.7,4.6C19.6,4.4,19.6,4.1,19.7,3.9L21.5,2.1L21.5,2.1C20.6,2,19.6,2.2,18.9,2.9L18.8,3C18,3.8,17.8,4.9,18.1,6L18.1,6L18.3,6.6L14.3,10.6L15.4,11.7L19.4,7.7L20,7.9C21.1,8.2,22.2,8,23,7.2C23.8,6.4,24,5.5,23.9,4.5Z\" fill=\"currentColor\" transform=\"matrix(-1,0,0,1,26,0)\"/></svg></span><span class=\"td-skill-txt\"><span class=\"td-skill-name\">systematic-debugging</span><span class=\"td-skill-desc\">一个用于调试软件问题的结构化方法，强制要求在提出修复方案前进行根本原因分析。</span></span><span class=\"td-skill-tag\">预置</span></div>",
        "                <div class=\"td-skill-row\" role=\"option\" tabindex=\"-1\"><span class=\"td-skill-ico\"><svg viewBox=\"0 0 14 14\" width=\"12\" height=\"12\" aria-hidden=\"true\"><path d=\"M24.2,2.6C25.4,4.2,25.3,6.5,23.8,7.9C22.7,9.1,21.1,9.4,19.7,8.9L15.7,12.9C15.5,13,15.3,13,15.1,12.9L13.1,10.9C13,10.7,13,10.5,13.1,10.3L17.1,6.3C16.6,4.9,16.9,3.3,18.1,2.2C19.5,0.7,21.8,0.6,23.4,1.8L21,4.2L21.8,5L24.2,2.6ZM23.9,4.5L23.9,4.5L22.1,6.3C21.9,6.4,21.6,6.4,21.4,6.3L19.7,4.6C19.6,4.4,19.6,4.1,19.7,3.9L21.5,2.1L21.5,2.1C20.6,2,19.6,2.2,18.9,2.9L18.8,3C18,3.8,17.8,4.9,18.1,6L18.1,6L18.3,6.6L14.3,10.6L15.4,11.7L19.4,7.7L20,7.9C21.1,8.2,22.2,8,23,7.2C23.8,6.4,24,5.5,23.9,4.5Z\" fill=\"currentColor\" transform=\"matrix(-1,0,0,1,26,0)\"/></svg></span><span class=\"td-skill-txt\"><span class=\"td-skill-name\">writing-skills</span><span class=\"td-skill-desc\">将测试驱动开发方法应用于Claude技能文档创建。</span></span><span class=\"td-skill-tag\">预置</span></div>",
        "                <div class=\"td-skill-row\" role=\"option\" tabindex=\"-1\"><span class=\"td-skill-ico\"><svg viewBox=\"0 0 14 14\" width=\"12\" height=\"12\" aria-hidden=\"true\"><path d=\"M24.2,2.6C25.4,4.2,25.3,6.5,23.8,7.9C22.7,9.1,21.1,9.4,19.7,8.9L15.7,12.9C15.5,13,15.3,13,15.1,12.9L13.1,10.9C13,10.7,13,10.5,13.1,10.3L17.1,6.3C16.6,4.9,16.9,3.3,18.1,2.2C19.5,0.7,21.8,0.6,23.4,1.8L21,4.2L21.8,5L24.2,2.6ZM23.9,4.5L23.9,4.5L22.1,6.3C21.9,6.4,21.6,6.4,21.4,6.3L19.7,4.6C19.6,4.4,19.6,4.1,19.7,3.9L21.5,2.1L21.5,2.1C20.6,2,19.6,2.2,18.9,2.9L18.8,3C18,3.8,17.8,4.9,18.1,6L18.1,6L18.3,6.6L14.3,10.6L15.4,11.7L19.4,7.7L20,7.9C21.1,8.2,22.2,8,23,7.2C23.8,6.4,24,5.5,23.9,4.5Z\" fill=\"currentColor\" transform=\"matrix(-1,0,0,1,26,0)\"/></svg></span><span class=\"td-skill-txt\"><span class=\"td-skill-name\">create-ex</span><span class=\"td-skill-desc\">Distill an ex-partner into an AI Skill. Import WeChat history, photos, social media posts, generate...</span></span><span class=\"td-skill-tag\">预置</span></div>",
        "                <div class=\"td-skill-row\" role=\"option\" tabindex=\"-1\"><span class=\"td-skill-ico\"><svg viewBox=\"0 0 14 14\" width=\"12\" height=\"12\" aria-hidden=\"true\"><path d=\"M24.2,2.6C25.4,4.2,25.3,6.5,23.8,7.9C22.7,9.1,21.1,9.4,19.7,8.9L15.7,12.9C15.5,13,15.3,13,15.1,12.9L13.1,10.9C13,10.7,13,10.5,13.1,10.3L17.1,6.3C16.6,4.9,16.9,3.3,18.1,2.2C19.5,0.7,21.8,0.6,23.4,1.8L21,4.2L21.8,5L24.2,2.6ZM23.9,4.5L23.9,4.5L22.1,6.3C21.9,6.4,21.6,6.4,21.4,6.3L19.7,4.6C19.6,4.4,19.6,4.1,19.7,3.9L21.5,2.1L21.5,2.1C20.6,2,19.6,2.2,18.9,2.9L18.8,3C18,3.8,17.8,4.9,18.1,6L18.1,6L18.3,6.6L14.3,10.6L15.4,11.7L19.4,7.7L20,7.9C21.1,8.2,22.2,8,23,7.2C23.8,6.4,24,5.5,23.9,4.5Z\" fill=\"currentColor\" transform=\"matrix(-1,0,0,1,26,0)\"/></svg></span><span class=\"td-skill-txt\"><span class=\"td-skill-name\">nuwa-skill</span><span class=\"td-skill-desc\">女娲（Nuwa）：输入任何人的名字，自动调研 → 提取思维框架 → 生成可运行的视角技能。</span></span><span class=\"td-skill-tag\">自有</span></div>",
        "                <div class=\"td-skill-row\" role=\"option\" tabindex=\"-1\"><span class=\"td-skill-ico\"><svg viewBox=\"0 0 14 14\" width=\"12\" height=\"12\" aria-hidden=\"true\"><path d=\"M24.2,2.6C25.4,4.2,25.3,6.5,23.8,7.9C22.7,9.1,21.1,9.4,19.7,8.9L15.7,12.9C15.5,13,15.3,13,15.1,12.9L13.1,10.9C13,10.7,13,10.5,13.1,10.3L17.1,6.3C16.6,4.9,16.9,3.3,18.1,2.2C19.5,0.7,21.8,0.6,23.4,1.8L21,4.2L21.8,5L24.2,2.6ZM23.9,4.5L23.9,4.5L22.1,6.3C21.9,6.4,21.6,6.4,21.4,6.3L19.7,4.6C19.6,4.4,19.6,4.1,19.7,3.9L21.5,2.1L21.5,2.1C20.6,2,19.6,2.2,18.9,2.9L18.8,3C18,3.8,17.8,4.9,18.1,6L18.1,6L18.3,6.6L14.3,10.6L15.4,11.7L19.4,7.7L20,7.9C21.1,8.2,22.2,8,23,7.2C23.8,6.4,24,5.5,23.9,4.5Z\" fill=\"currentColor\" transform=\"matrix(-1,0,0,1,26,0)\"/></svg></span><span class=\"td-skill-txt\"><span class=\"td-skill-name\">subagent-driven-development</span><span class=\"td-skill-desc\">将实施计划分解为独立任务的工作流，每个任务由新的AI子代理处理，并经过规...</span></span><span class=\"td-skill-tag\">自有</span></div>",
        "              </div>",
        "              <button type=\"button\" class=\"td-skill-x\" aria-label=\"关闭技能面板\" data-td-skill-close=\"1\"><svg viewBox=\"0 0 10.4989 10.487117\" width=\"12\" height=\"12\" aria-hidden=\"true\"><path d=\"M7.5,10.5L3,10.5L1.8,10.5C1.8,10.5,1.7,10.5,1.7,10.4C1.6,10.5,1.4,10.4,1.4,10.3L0.8,9.8C0.7,9.7,0.7,9.5,0.8,9.3L3.3,6.1C3.4,6,3.7,6,3.8,6.1L4.3,6.6C4.5,6.8,4.5,7,4.3,7.1L2.9,9L6.9,9C8,8.9,8.9,8,9,6.9L9,4.1C9,3.9,9.2,3.7,9.4,3.7L10.1,3.7C10.3,3.7,10.5,3.9,10.5,4.1L10.5,4.5L10.5,7.1L10.5,7.5C10.5,9.1,9.2,10.5,7.5,10.5Z\" fill=\"currentColor\"/></svg></button>",
        "              <div class=\"td-skill-foot\">",
        "                <div>",
        "                  <button type=\"button\" class=\"giencoder-btn giencoder-btn-size-default giencoder-btn-secondary\">安装技能</button>",
        "                  <button type=\"button\" class=\"giencoder-btn giencoder-btn-size-default giencoder-btn-secondary\">管理技能</button>",
        "                </div>",
        "              </div>",
        "            </div>",
        "          </div>",
        "        </div>",
        "    </div>",
        "    <button class=\"td-collapsed\" type=\"button\" aria-label=\"展开 AI 会话\" data-td-expand=\"1\">",
        "      <span>展</span><span>开</span><span>AI</span><span>会</span><span>话</span>",
        "    </button>",
        "  </aside>",
        "</div>"
].join('\n');

  function bindDetail(wrap) {
    var root = wrap.querySelector('.td-root');
    if (!root) return;
    /* 返回任务看板 */
    var back = wrap.querySelector('[data-td-back]');
    if (back) back.addEventListener('click', function () { location.href = 'kanban.html'; });

    /* 描述区：展开全文 / 收起（第 25 轮第 4 项：加 max-height 微动效）
       max-height 从 px → none 不可动画，所以全程只用像素值过渡，
       过渡结束后才把内联值清掉（回到 CSS 的 374px / none）。 */
    var descBody = wrap.querySelector('[data-td-desc]');
    var descBtn = wrap.querySelector('[data-td-desc-toggle]');
    if (descBody && descBtn) {
      var COLLAPSED_H = parseFloat(getComputedStyle(descBody).maxHeight) || 374;
      var descBusy = false;
      function onDescEnd(fn) {
        var done = false;
        function once() { if (done) return; done = true; descBody.removeEventListener('transitionend', once); fn(); }
        descBody.addEventListener('transitionend', once);
        setTimeout(once, 420);   /* 兜底：transitionend 可能因高度无变化而不触发 */
      }
      descBtn.addEventListener('click', function () {
        if (descBusy) return;
        var open = !descBody.classList.contains('is-open');
        var curH = descBody.getBoundingClientRect().height;
        descBusy = true;
        descBody.classList.add('is-animating');
        if (open) {
          /* 先离屏量出展开后的真实高度（临时 max-height:none），再回到当前高度起跑 */
          descBody.style.maxHeight = 'none';
          var fullH = descBody.getBoundingClientRect().height;
          descBody.style.maxHeight = curH + 'px';
          descBody.classList.add('is-open');
          requestAnimationFrame(function () { descBody.style.maxHeight = fullH + 'px'; });
          onDescEnd(function () {
            descBusy = false;
            descBody.classList.remove('is-animating');
            if (descBody.classList.contains('is-open')) descBody.style.maxHeight = 'none';
          });
        } else {
          descBody.style.maxHeight = curH + 'px';   /* 从 none 落到确定像素值，才能起跑 */
          descBody.classList.remove('is-open');
          requestAnimationFrame(function () { descBody.style.maxHeight = COLLAPSED_H + 'px'; });
          onDescEnd(function () {
            descBusy = false;
            descBody.classList.remove('is-animating');
            descBody.style.maxHeight = '';
          });
        }
        descBtn.textContent = open ? '收起' : '展开全文';
        descBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }

    /* AI 会话全屏 / 取消全屏（第 26 轮第 5 项）：形态完全由 CSS 的 .td-root.is-fullscreen 决定，
       这里只切类并同步按钮语义（aria-label / title / aria-pressed），图标显隐由 .td-ico-max/.td-ico-min 控制。 */
    var fsBtn = wrap.querySelector('[data-td-fullscreen]');
    if (fsBtn) {
      fsBtn.addEventListener('click', function () {
        var on = root.classList.toggle('is-fullscreen');
        fsBtn.setAttribute('aria-label', on ? '取消全屏' : '全屏');
        fsBtn.setAttribute('title', on ? '取消全屏' : '全屏');
        fsBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }

    /* ================= 对话框三个弹层（★ 第 28 轮第 4 项） =================
       行为对齐 pages/base.html 实测：
         · 点「添加」按钮 → 在按钮上方弹出 180×92 菜单（两项 + 分隔线）；再点按钮关闭；
         · 点「技能」按钮 → 在对话框上方弹出 760×320 面板（Goal + 技能列表 + 底部两个按钮）；
         · 点「大模型 / 标准模式」视图 → 展开 DS Select 弹层；
         · 点菜单项 / 技能行 / 模型项 → **只关闭弹层**（base 实测：不写 textarea、也没有隐藏的
           input[type=file]，所以「添加本地文件」这里同样只关闭，保持一致）；
         · 点弹层外部 → 全部关闭；
         · Esc → 全部关闭。⚠️ base 里 Esc 不关技能面板，但本页 Esc 是「返回任务看板」的全局快捷键，
           必须先吃掉这次 Esc，否则会误跳转 → 用自定义事件 td:close-popovers 与页尾脚本约定（见 TAIL）。 */
    var opAdd = null, opSkill = null, opSel = null;
    function popFlag() { document.documentElement.toggleAttribute('data-td-pop-open', !!(opAdd || opSkill || opSel)); }
    function closeAdd() { if (!opAdd) return; opAdd.pop.hidden = true; opAdd.btn.setAttribute('aria-expanded', 'false'); opAdd = null; popFlag(); }
    function closeSkill() { if (!opSkill) return; opSkill.pop.hidden = true; opSkill.btn.setAttribute('aria-expanded', 'false'); opSkill = null; popFlag(); }
    /* ⚠️ DS Select 弹层的开合唯一开关是 `.giencoder-popup-open`（ui-controls.css），
       不要用内联 display（display:block 但 opacity:0/visibility:hidden ⇒ 看不见）。 */
    function closeSel() { if (!opSel) return; opSel.pop.classList.remove('giencoder-popup-open'); opSel.view.setAttribute('aria-expanded', 'false'); opSel = null; popFlag(); }
    function closePops() { closeAdd(); closeSkill(); closeSel(); }

    var addBtn = wrap.querySelector('[data-td-add-btn]');
    var addPop = wrap.querySelector('[data-td-add-pop]');
    if (addBtn && addPop) {
      addBtn.addEventListener('click', function () {
        closeSkill(); closeSel();
        if (opAdd) { closeAdd(); return; }
        addPop.hidden = false;
        addBtn.setAttribute('aria-expanded', 'true');
        opAdd = { btn: addBtn, pop: addPop }; popFlag();
        var f = addPop.querySelector('[role="menuitem"]');
        if (f) f.focus();
      });
      Array.prototype.forEach.call(addPop.querySelectorAll('[role="menuitem"]'), function (it) {
        it.addEventListener('click', function () { closeAdd(); });
      });
    }

    var skillBtn = wrap.querySelector('[data-td-skill-btn]');
    var skillPop = wrap.querySelector('[data-td-skill-pop]');
    if (skillBtn && skillPop) {
      skillBtn.addEventListener('click', function () {
        closeAdd(); closeSel();
        if (opSkill) { closeSkill(); return; }
        skillPop.hidden = false;
        skillBtn.setAttribute('aria-expanded', 'true');
        opSkill = { btn: skillBtn, pop: skillPop }; popFlag();
      });
      Array.prototype.forEach.call(skillPop.querySelectorAll('.td-skill-row'), function (row) {
        row.addEventListener('click', function () { closeSkill(); });
      });
      var skillX = skillPop.querySelector('[data-td-skill-close]');
      if (skillX) skillX.addEventListener('click', function () { closeSkill(); skillBtn.focus(); });
    }

    /* 大模型 / 标准模式：DS Select 契约结构 —— 视图点击开合、选项点击选中并回写文案 */
    Array.prototype.forEach.call(wrap.querySelectorAll('.td-composer .giencoder-select'), function (sel) {
      var view = sel.querySelector('.giencoder-select-view');
      var pop = sel.querySelector('.giencoder-select-popup');
      if (!view || !pop) return;
      view.addEventListener('click', function () {
        closeAdd(); closeSkill();
        if (opSel && opSel.pop === pop) { closeSel(); return; }
        closeSel();
        pop.classList.add('giencoder-popup-open');
        view.setAttribute('aria-expanded', 'true');
        opSel = { view: view, pop: pop }; popFlag();
      });
      view.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); view.click(); }
      });
      Array.prototype.forEach.call(pop.querySelectorAll('.giencoder-select-option'), function (opt) {
        opt.addEventListener('click', function () {
          if (opt.classList.contains('giencoder-select-option-disabled')) return;
          Array.prototype.forEach.call(pop.querySelectorAll('.giencoder-select-option'), function (o) {
            o.classList.remove('giencoder-select-option-selected');
            o.setAttribute('aria-selected', 'false');
          });
          opt.classList.add('giencoder-select-option-selected');
          opt.setAttribute('aria-selected', 'true');
          var txt = view.querySelector('.giencoder-select-view-text');
          if (txt) txt.textContent = opt.textContent.trim();
          closeSel();
        });
      });
    });

    /* 点弹层与触发器以外的任何地方 → 全部关闭
       ⚠️ 「技能」按钮本身不在 .giencoder-select 里，必须单独列出，否则它的 click 会先打开面板、
          紧接着冒泡到 document 又被立刻关掉。 */
    document.addEventListener('click', function (e) {
      if (!opAdd && !opSkill && !opSel) return;
      if (e.target.closest && e.target.closest('.td-add-pop, .td-skill-pop, .giencoder-select, [data-td-skill-btn]')) return;
      closePops();
    });
    document.addEventListener('td:close-popovers', closePops);

    var gutter = wrap.querySelector('[data-td-gutter]');
    var right = wrap.querySelector('.td-right');
    var left = wrap.querySelector('.td-left');
    if (!gutter || !right) return;

    var DEFAULT_W = 480;   /* 右栏默认宽（设计稿实测） */
    var MIN_W = 100;       /* 拖到此值以下即自动折叠（第24轮：原 320） */
    var COLLAPSED_W = 48;  /* 折叠条宽（设计稿实测 1343:18532 = 48×844） */
    var LEFT_MIN = 320;    /* 左栏保底 */
    var dragging = false, curW = DEFAULT_W;

    function setWidth(w) {
      curW = w;
      root.style.setProperty('--td-right-w', w + 'px');
      gutter.setAttribute('aria-valuenow', String(Math.round(w)));
    }
    /* 由指针 x 反推右栏应有的宽度。
       第 28 轮第 1 项：两栏可互换位置（.is-swapped → row-reverse）后 .td-right 会跑到左侧、
       拖动条落在它**右侧**，此时宽度与 clientX 是正相关（原来恒为负相关）→ 必须按状态取反。 */
    function widthFrom(clientX) {
      var box = root.getBoundingClientRect();
      var w = root.classList.contains('is-swapped') ? (clientX - box.left) : (box.right - clientX);
      var maxW = box.width - LEFT_MIN;
      if (w > maxW) w = maxW;
      if (w < 0) w = 0;
      return w;
    }
    function collapse() {
      root.classList.add('is-collapsed');
      setWidth(COLLAPSED_W);
    }
    function expand(w) {
      root.classList.remove('is-collapsed');
      setWidth(w || DEFAULT_W);
    }
    /* 拖动分栏 */
    gutter.addEventListener('pointerdown', function (e) {
      if (root.classList.contains('is-collapsed')) return;
      dragging = true;
      root.classList.add('is-dragging');
      gutter.classList.add('is-dragging');
      if (gutter.setPointerCapture) { try { gutter.setPointerCapture(e.pointerId); } catch (err) {} }
      e.preventDefault();
    });
    gutter.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var w = widthFrom(e.clientX);
      /* 第 24 轮第 4 项：拖到 100px 以下立刻折叠成窄条（实时反馈）；
         继续向左拖回 100px 以上则恢复跟随鼠标。松手时以 curW 判定最终状态。 */
      if (w < MIN_W) {
        curW = w;                                  /* 记录真实拖拽宽度，便于反向恢复 */
        root.classList.add('is-collapsed');
        setWidth(COLLAPSED_W);
      } else {
        root.classList.remove('is-collapsed');
        setWidth(Math.round(w));
      }
    });
    function endDrag() {
      if (!dragging) return;
      dragging = false;
      root.classList.remove('is-dragging');
      gutter.classList.remove('is-dragging');
      if (curW < MIN_W) collapse();          /* 过窄 -> 自动折叠 */
      else root.classList.remove('is-collapsed');
    }
    gutter.addEventListener('pointerup', endDrag);
    gutter.addEventListener('pointercancel', endDrag);
    /* 键盘可达：默认 ← 变宽 / → 变窄（到阈值即折叠）；两栏互换后方向随之取反 */
    gutter.addEventListener('keydown', function (e) {
      var step = 24;
      var maxW = root.getBoundingClientRect().width - LEFT_MIN;
      var swapped = root.classList.contains('is-swapped');
      var widerKey = swapped ? 'ArrowRight' : 'ArrowLeft';
      var narrowKey = swapped ? 'ArrowLeft' : 'ArrowRight';
      if (e.key === widerKey) { expand(Math.min(curW + step, maxW)); e.preventDefault(); }
      else if (e.key === narrowKey) {
        var nw = curW - step;
        if (nw < MIN_W) collapse(); else expand(nw);
        e.preventDefault();
      }
    });
    /* 折叠态：点击整列恢复默认宽度比例 */
    right.addEventListener('click', function (e) {
      if (!root.classList.contains('is-collapsed')) return;
      e.preventDefault();
      expand(DEFAULT_W);
    });

    /* ---------- 按住标题栏左右拖动互换两栏位置 ----------
       ★ 第 28 轮第 1 项建立；★ 第 30 轮第 2 项重写（原实现「瞬间切类 + 260ms 透明度闪一下」太生硬）。

       保留的判定规则：
         · pointerdown 必须落在 .td-bar / .td-right-bar 上，且不在按钮/链接/输入控件上
           （否则会和顶栏那些按钮的点击抢事件）；
         · 位移 < 6px 视为点击（不进入拖动态、不 preventDefault、不影响原有点击）；
         · 方向在 pointerdown 时按两栏实测中心算出 ⇒ 换位后再拖同一个标题栏会自动反向，
           不会出现「单向死锁」；
         · 静止态仍只切 .is-swapped（CSS row-reverse），DOM 顺序不动。

       第 30 轮的五个手感优化：
         ① 跟手位移（橡皮筋，不是硬限幅）：|dx| ≤ cap(两栏中心距 ×14%，实测约 100px) 时 1:1 跟手；
            超出后每多拖 1px 只走 RB=0.18px → 大拖不会「顶住不动」，但越拖越沉；
            另一栏反向 12% 微移「让位」→ 拖起来立刻有物理反馈，两栏又不会在途中就交叉重叠；
         ② FLIP 滑动：松手判定换位时，先记 first rect → 切类 → 记 last rect →
            用 Web Animations 从 translateX(dx) 滑回 0，两栏真的横着挪过去（不是瞬移）；
            飞行期被拖的那一栏加 is-fly-left/right → z=3 + 加深投影（「拎起来」）；
         ③ 回弹：未达阈值时把跟手位移用同一条曲线弹回 0，而不是瞬间归位；
         ④ 甩动判定：|v| ≥ 0.6 px/ms 且方向正确 ⇒ 即使位移不够也换位（短促快拖也能换）。
       曲线统一 cubic-bezier(0.22, 1, 0.36, 1)：起步快、收尾稳、**无过冲**（不会越界出容器）。
       prefers-reduced-motion 下跳过所有位移动画，只切类。 */
    var SWAP_T = 72;              /* 距离阈值 px（原 80：略微降低，配合甩动判定更好触发） */
    var SWAP_FLICK = 0.6;         /* 甩动速度阈值 px/ms */
    var SWAP_DUR = 400;           /* FLIP 滑动时长 ms */
    var RB = 0.18;                /* 橡皮筋系数：超出限幅后每多拖 1px 只走 0.18px */
    var SWAP_EASE = 'cubic-bezier(0.22, 1, 0.36, 1)';
    var reduceMotion = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var xdrag = null;

    /* 把元素从 from px 位移滑回 0，结束即清掉内联 transform（回到自然布局位） */
    function slideBack(el, from, dur) {
      if (!el) return;
      if (reduceMotion || !from) { el.style.transform = ''; return; }
      var anim = el.animate(
        [{ transform: 'translate3d(' + from + 'px,0,0)' },
         { transform: 'translate3d(' + Math.round(from * 0.55) + 'px,0,0)', offset: 0.45 },
         { transform: 'translate3d(0,0,0)' }],
        { duration: dur, easing: SWAP_EASE, fill: 'both' });
      anim.onfinish = function () {
        el.style.transform = '';
        if (anim.cancel) anim.cancel();
      };
    }

    function bindSwapBar(bar, panel) {
      if (!bar) return;
      var other = (panel === left) ? right : left;

      bar.addEventListener('pointerdown', function (e) {
        if (e.button !== 0) return;
        if (e.target.closest('button, a, input, textarea, select, [role="combobox"]')) return;
        if (root.classList.contains('is-fullscreen') || root.classList.contains('is-collapsed')) return;
        var a = panel.getBoundingClientRect(), b = other.getBoundingClientRect();
        var gap = Math.abs((b.left + b.width / 2) - (a.left + a.width / 2));
        xdrag = {
          bar: bar, panel: panel, other: other,
          x0: e.clientX, dx: 0, applied: 0, v: 0, moved: false, tPrev: e.timeStamp,
          cap: Math.max(24, Math.round(gap * 0.14)),   /* 跟手限幅：一次性算好，避免 pointermove 里反复取 rect */
          dir: (b.left + b.width / 2) >= (a.left + a.width / 2) ? 1 : -1
        };
        if (bar.setPointerCapture) { try { bar.setPointerCapture(e.pointerId); } catch (err) {} }
      });

      bar.addEventListener('pointermove', function (e) {
        var d = xdrag;
        if (!d || d.bar !== bar) return;
        var dt = Math.max(1, e.timeStamp - d.tPrev);
        var next = e.clientX - d.x0;
        d.v = (next - d.dx) / dt;        /* 瞬时速度 px/ms */
        d.tPrev = e.timeStamp;
        d.dx = next;
        if (!d.moved) {
          if (Math.abs(d.dx) < 6) return;
          d.moved = true;
          root.classList.add('is-xdrag');
          d.panel.classList.add('is-xdrag-panel');
          d.other.classList.add('is-xdrag-peer');
        }
        root.classList.toggle('is-xarmed', (d.dx * d.dir >= SWAP_T) || (d.v * d.dir >= SWAP_FLICK));
        if (!reduceMotion) {
          /* ③ 橡皮筋阻尼（不是硬限幅）：|dx| ≤ cap 时 1:1 跟手；
             超出后按 RB 系数继续走（cap + 超出量*0.18）→ 大拖也不会「顶住不动」，
             但越拖越沉，视觉上明确「这里拖不过去」。*/
          var abs = Math.abs(d.dx);
          var raw = abs <= d.cap ? abs : d.cap + (abs - d.cap) * RB;
          var applied = (d.dx < 0 ? -1 : 1) * Math.round(raw);
          var k = Math.min(1, Math.abs(applied) / d.cap);   /* 0~1：越接近目标位置，主动栏越「浮起来」 */
          d.applied = applied;
          d.panel.style.transform = 'translate3d(' + applied + 'px,0,0) scale(' + (1 + 0.006 * k).toFixed(4) + ')';
          d.other.style.transform = 'translate3d(' + Math.round(applied * -0.12) + 'px,0,0)';
        }
        e.preventDefault();
      });

      function endSwap() {
        var d = xdrag;
        if (!d || d.bar !== bar) return;
        xdrag = null;
        d.panel.classList.remove('is-xdrag-panel');
        d.other.classList.remove('is-xdrag-peer');
        root.classList.remove('is-xarmed', 'is-xdrag');
        if (!d.moved) return;

        var pass = (d.dx * d.dir >= SWAP_T) || (d.v * d.dir >= SWAP_FLICK);
        if (pass) {
          /* ② FLIP：先清掉跟手位移 → 记 first → 切类 → 记 last → 从差值滑入 */
          d.panel.style.transform = '';
          d.other.style.transform = '';
          var fL = left.getBoundingClientRect(), fR = right.getBoundingClientRect();
          var fG = gutter.getBoundingClientRect();
          root.classList.toggle('is-swapped');
          var lL = left.getBoundingClientRect(), lR = right.getBoundingClientRect();
          var lG = gutter.getBoundingClientRect();
          var dxL = Math.round(fL.left - lL.left);
          var dxR = Math.round(fR.left - lR.left);
          var dxG = Math.round(fG.left - lG.left);
          if (!reduceMotion && (dxL || dxR)) {
            /* 飞行期把**被拎起的那一栏**抬到上层并加深投影：两栏重叠时读起来像
               「把卡片拎起来挪过去」，而不是两张不透明卡片硬生生对穿。
               （is-fly-left / is-fly-right 由 d.panel 决定，谁被拖谁在上层。） */
            root.classList.add('is-swap-fly', d.panel === left ? 'is-fly-left' : 'is-fly-right');
            if (dxL) left.style.transform = 'translate3d(' + dxL + 'px,0,0)';
            if (dxR) right.style.transform = 'translate3d(' + dxR + 'px,0,0)';
            if (dxG) gutter.style.transform = 'translate3d(' + dxG + 'px,0,0)';
            slideBack(left, dxL, SWAP_DUR);
            slideBack(right, dxR, SWAP_DUR);
            slideBack(gutter, dxG, SWAP_DUR);
            setTimeout(function () {
              root.classList.remove('is-swap-fly', 'is-fly-left', 'is-fly-right');
            }, SWAP_DUR + 40);
          }
        } else {
          /* ③ 回弹 */
          slideBack(d.panel, d.applied, 260);
          slideBack(d.other, Math.round(d.applied * -0.12), 260);
        }
      }
      bar.addEventListener('pointerup', endSwap);
      bar.addEventListener('pointercancel', endSwap);
    }
    bindSwapBar(wrap.querySelector('.td-bar'), left);
    bindSwapBar(wrap.querySelector('.td-right-bar'), right);
  }

  /* 外壳页签：本页归属研发工作台。React 外壳按「文件名 → 路由」判页签
     （task-detail.html 不在映射表内 → 被判成「基础工作台」）。外观（轨道底/游标/文字色）
     已由 CSS 覆盖；这里把页签的**文案与图标**也还原成 shell 自己的 dev 态：
     未选中 = 无图标 + 前 2 字；选中 = 图标 + 完整文案（与 shell 内 `r?label:label.slice(0,2)` 一致）。 */
  var DEV_ICON = '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" class="mr-1.5 size-4 shrink-0" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M23.08 4.315a3 3 0 012.328.01l17.769 7.576A3 3 0 0145 14.661v19.645a3 3 0 01-1.951 2.81L25.28 43.745a3 3 0 01-2.074.008L4.974 37.12A3 3 0 013 34.299V14.668a3 3 0 011.848-2.77l18.231-7.582zm1.146 3.855L7 15.334V33.6l17.227 6.27L41 33.61V15.32L24.226 8.17zm3.498 17.623L21.608 18l-6.377 4.723h-6.19L9 26.37h7.367l4.376-3.051l6.34 7.68 6.307-4.63H39l-.02-3.647h-7.117l-4.139 3.07z" fill="currentColor"></path></svg>';
  function setTabLabel(btn, text) {
    for (var i = btn.childNodes.length - 1; i >= 0; i--) {
      if (btn.childNodes[i].nodeType === 3) btn.removeChild(btn.childNodes[i]);
    }
    btn.appendChild(document.createTextNode(text));
  }
  function syncShellTab() {
    var tl = document.querySelector('[role="tablist"][aria-label="工作台切换"]');
    if (!tl) return false;
    var base = tl.querySelector('[data-tab="base"]');
    var dev = tl.querySelector('[data-tab="dev"]');
    if (base) {
      base.setAttribute('aria-selected', 'false');
      var bi = base.querySelector('svg');
      if (bi) base.removeChild(bi);
      setTabLabel(base, '基础');
    }
    if (dev) {
      dev.setAttribute('aria-selected', 'true');
      if (!dev.querySelector('svg')) dev.insertAdjacentHTML('afterbegin', DEV_ICON);
      setTabLabel(dev, '研发工作台');
    }
    return true;
  }

  /* ---------- 描述区配图的蒙层预览（★ 第 30 轮第 1 项） ----------
     完全按 DS Image 契约（components/image.json）实现，不自造同义结构：
       · 缩略图 = div.giencoder-image > div.giencoder-image-mask-wrapper > img.giencoder-image-img
         + div.giencoder-image-mask（悬停提示「预览」）；
       · 点缩略图 → 动态创建 div.giencoder-image-preview（契约 anatomy 的「预览层」= 全屏遮罩，
         内含 -preview-mask / -preview-img / -preview-close / -preview-zoom），挂在 <body> 上
         ——与 preview/component-image.html 参考实现同一套类名，只是把 demo 的 pv-* 换成契约 is-* 状态类；
       · 关闭方式：右上关闭按钮 / 点遮罩空白处 / Esc；
       · 动效：遮罩淡入 0.3s + 大图 scale(.95→1)（spring）；关闭 0.2s —— 与参考实现同参数。
     Esc 优先级约定（页尾 TAIL）：图片预览 > 对话框弹层 > 退出全屏 > 返回看板；
       打开时给 <html> 打 data-td-img-preview，页尾先判它再派发 td:close-image-preview。 */
  function bindDescImagePreview(wrap) {
    var thumb = wrap.querySelector('.td-desc .giencoder-image-mask-wrapper');
    if (!thumb) return;
    var thumbImg = thumb.querySelector('img.giencoder-image-img');
    if (!thumbImg) return;

    var overlay = null, scale = 1, closing = false;

    function build() {
      if (overlay) return overlay;
      overlay = document.createElement('div');
      overlay.className = 'giencoder-image-preview';
      overlay.setAttribute('role', 'dialog');
      overlay.setAttribute('aria-modal', 'true');
      overlay.setAttribute('aria-label', '图片预览');
      overlay.innerHTML =
        '<div class="giencoder-image-preview-mask">' +
          '<button type="button" class="giencoder-image-preview-btn giencoder-image-preview-close" aria-label="关闭预览">' +
            '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 5l14 14M19 5L5 19"/></svg>' +
          '</button>' +
          '<img class="giencoder-image-preview-img" alt="">' +
          '<div class="giencoder-image-preview-zoom">' +
            '<button type="button" class="giencoder-image-preview-btn" aria-label="缩小" data-td-zoom="out">' +
              '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 12h14"/></svg>' +
            '</button>' +
            '<button type="button" class="giencoder-image-preview-btn" aria-label="放大" data-td-zoom="in">' +
              '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>' +
            '</button>' +
          '</div>' +
        '</div>';
      document.body.appendChild(overlay);

      overlay.querySelector('.giencoder-image-preview-close').addEventListener('click', close);
      /* 点遮罩空白处关闭（mask 铺满全屏，target 落在遮罩/mask 上即视为点背景） */
      overlay.addEventListener('click', function (e) {
        var isBg = (e.target === overlay) ||
                   (e.target.classList && e.target.classList.contains('giencoder-image-preview-mask'));
        if (isBg) close();
      });
      Array.prototype.forEach.call(overlay.querySelectorAll('[data-td-zoom]'), function (btn) {
        btn.addEventListener('click', function () {
          var im = overlay.querySelector('.giencoder-image-preview-img');
          scale = btn.getAttribute('data-td-zoom') === 'in'
            ? Math.min(3, +(scale * 1.25).toFixed(2))
            : Math.max(0.5, +(scale * 0.8).toFixed(2));
          im.style.transform = 'scale(' + scale + ')';
          im.style.setProperty('--giencoder-image-scale', scale);
        });
      });
      return overlay;
    }

    function flag(on) { document.documentElement.toggleAttribute('data-td-img-preview', on); }

    function close() {
      if (!overlay || closing || overlay.style.display === 'none') return;
      closing = true;
      var im = overlay.querySelector('.giencoder-image-preview-img');
      im.style.setProperty('--giencoder-image-scale', scale);
      im.classList.remove('is-opening');
      im.classList.add('is-closing');
      overlay.classList.add('is-closing');
      overlay.classList.remove('is-open');
      flag(false);
      setTimeout(function () {
        overlay.style.display = 'none';
        overlay.classList.remove('is-open', 'is-closing');
        im.classList.remove('is-opening', 'is-closing');
        closing = false;
      }, 240);
    }

    function open() {
      build();
      if (closing || overlay.style.display === 'flex') return;
      var im = overlay.querySelector('.giencoder-image-preview-img');
      im.setAttribute('src', thumbImg.getAttribute('src'));
      im.setAttribute('alt', thumbImg.getAttribute('alt') || '');
      scale = 1;
      im.style.transform = '';
      im.style.setProperty('--giencoder-image-scale', 1);
      overlay.classList.remove('is-closing');
      overlay.style.display = 'flex';
      void overlay.offsetHeight;             /* 强制回流，让遮罩淡入过渡生效 */
      overlay.classList.add('is-open');
      im.classList.add('is-opening');
      flag(true);
      setTimeout(function () { im.classList.remove('is-opening'); }, 340);
    }

    thumb.addEventListener('click', open);
    thumb.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });
    /* 页尾 Esc 链通过自定义事件通知关闭（与 td:close-popovers 同一约定） */
    document.addEventListener('td:close-image-preview', close);
  }

  /* ---------- 顶栏「转派」→ 成员浮窗（★ 第 31 轮，设计稿节点 1345:18366） ----------
     完全按 DS 契约组装，不自造同义结构：
       div.giencoder-popover（契约 popover.json 的 popup；按契约渲染到 popupContainer=body）
         ├ div.giencoder-popover-title     标题 + 副标题
         ├ div.giencoder-popover-content
         │   ├ div.giencoder-input-wrapper > span.giencoder-input-prefix + input.giencoder-input
         │   └ div.giencoder-list.giencoder-scroll-thin > div.giencoder-list-item（role=option）
         └ div.giencoder-popover-footer > button.giencoder-btn-primary
     显隐唯一开关 = DS 弹层的 .giencoder-popup-open（ui-controls.css），与 Select 弹层同参数。
     关闭途径：再点触发按钮 / 点浮窗外 / Esc（页尾 Esc 链派发 td:close-dispatch，
     优先级排在图片预览之后、对话框弹层之前）。
     渲染到 body 而不是 .td-bar 内：① 契约默认 popupContainer=body；② 顶栏本身是
     「按住拖动互换两栏」的把手，浮窗落在顶栏内会被拖拽判定命中。
     设计稿实测的尺寸/间距见 CSS 段注释；两处设计稿未定义处取 DS 既有约定（4px 间距 + 左对齐）。 */
  var DISPATCH_MEMBERS = [
    { name: '邵禹铭', sid: 'P0098602', ch: '铭' },
    { name: '秦怡',   sid: 'P0098603', ch: '怡' },
    { name: '韩佳毅', sid: 'P0098604', ch: '毅' },
    { name: '顾帆',   sid: 'P0098605', ch: '帆' },
    { name: '姜嘉怡', sid: 'P0098606', ch: '怡' },
    { name: '朱甜',   sid: 'P0098607', ch: '甜' },
    { name: '齐瑞辰', sid: 'P0098608', ch: '辰' }
  ];
  var DP_CHECK_SVG = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.6 7.5l3 3L11.4 4.2"/></svg>';
  var DP_SEARCH_SVG = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><circle cx="6.1" cy="6.1" r="4.35"/><path d="M9.3 9.3l3.1 3.1"/></svg>';
  var DP_MSG_SVG = '<svg viewBox="0 0 14 14" width="14" height="14" fill="none" aria-hidden="true"><circle cx="7" cy="7" r="6.2" fill="currentColor"/><path d="M4.3 7.2l1.9 1.9 3.5-3.7" stroke="var(--color-white)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  function bindDispatchPicker() {
    var btn = document.querySelector('[data-td-dispatch]');
    if (!btn || btn.hasAttribute('data-td-dp-bound')) return;
    btn.setAttribute('data-td-dp-bound', '1');

    var pop = null, listEl = null, inputEl = null, noneEl = null, okEl = null;
    var items = [], cur = 0;

    function build() {
      if (pop) return pop;
      pop = document.createElement('div');
      pop.className = 'giencoder-popover td-dp';
      pop.setAttribute('role', 'dialog');
      pop.setAttribute('aria-label', '选择转派人员');
      pop.setAttribute('tabindex', '-1');   /* 打开时焦点落在浮层本身：Esc 可关且不会给搜索框套上 focus 环 */
      pop.innerHTML =
        '<div class="giencoder-popover-title">将任务转派给：' +
          '<div class="td-dp-t2">转派仅变更任务负责人，不改变任务状态。</div>' +
        '</div>' +
        '<div class="giencoder-popover-content">' +
          '<div class="giencoder-input-wrapper" data-size="medium">' +
            '<span class="giencoder-input-prefix">' + DP_SEARCH_SVG + '</span>' +
            '<input class="giencoder-input" type="text" placeholder="搜索成员" aria-label="搜索成员" autocomplete="off">' +
          '</div>' +
          '<div class="giencoder-list giencoder-scroll-thin" role="listbox" aria-label="成员列表">' +
            DISPATCH_MEMBERS.map(function (m, i) {
              return '<div class="giencoder-list-item giencoder-list-item-hoverable td-dp-item" role="option"' +
                     ' data-size="small" data-td-idx="' + i + '"' +
                     ' aria-selected="' + (i === cur ? 'true' : 'false') + '"' +
                     ' style="--avatar-bg: var(--avatar-bg-' + ((i % 7) + 1) + ')">' +
                     '<span class="giencoder-avatar giencoder-avatar-circle giencoder-avatar-text td-dp-av" aria-hidden="true">' + m.ch + '</span>' +
                     '<span class="giencoder-list-item-meta"><span class="giencoder-list-item-title td-dp-name">' + m.name +
                       '<span class="td-dp-id"> (' + m.sid + ')</span></span></span>' +
                     '<span class="giencoder-list-item-action"><span class="td-dp-check" aria-hidden="true">' + DP_CHECK_SVG + '</span></span>' +
                     '</div>';
            }).join('') +
            '<div class="giencoder-empty td-dp-none" hidden><div class="giencoder-empty-description">未找到匹配成员</div></div>' +
          '</div>' +
        '</div>' +
        '<div class="giencoder-popover-footer">' +
          '<button class="giencoder-btn giencoder-btn-primary giencoder-btn-size-default td-dp-ok" type="button">确定转派</button>' +
        '</div>';
      /* ★ 挂载前先写内联坐标：绝对定位元素若 left/top 还是 auto，会先按「静态位置」落在文档末尾，
         把文档撑高 → 出现页面竖向滚动条 → 顶栏右对齐按钮整体左移一个滚动条宽度（实测 10px），
         于是 place() 读到的按钮 x 比最终值小 10px。预置 0/0 后挂载，布局不抖，place() 才拿到真值。 */
      pop.style.left = '0px';
      pop.style.top = '0px';
      document.body.appendChild(pop);

      listEl = pop.querySelector('.giencoder-list');
      inputEl = pop.querySelector('.giencoder-input');
      noneEl = pop.querySelector('.td-dp-none');
      okEl = pop.querySelector('.td-dp-ok');
      items = Array.prototype.slice.call(pop.querySelectorAll('[data-td-idx]'));

      listEl.addEventListener('click', function (e) {
        var it = e.target.closest('[data-td-idx]');
        if (it) select(+it.getAttribute('data-td-idx'));
      });
      inputEl.addEventListener('input', filter);
      /* 焦点在搜索框里时 Esc 不该被页尾「INPUT 直接 return」吞掉 → 浮层内自行处理 */
      pop.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { e.stopPropagation(); close(); }
      });
      okEl.addEventListener('click', confirm);
      return pop;
    }

    function place() {
      var r = btn.getBoundingClientRect();
      var left = Math.min(r.left, window.innerWidth - pop.offsetWidth - 8);
      pop.style.left = Math.round(Math.max(8, left) + window.scrollX) + 'px';
      pop.style.top = Math.round(r.bottom + 4 + window.scrollY) + 'px';
      pop.style.right = 'auto';
      pop.style.bottom = 'auto';
    }

    function select(i) {
      cur = i;
      items.forEach(function (it, k) { it.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
    }

    function filter() {
      var q = inputEl.value.trim().toLowerCase();
      var shown = 0;
      items.forEach(function (it, i) {
        var m = DISPATCH_MEMBERS[i];
        var hit = !q || (m.name + m.sid).toLowerCase().indexOf(q) >= 0;
        it.hidden = !hit;
        if (hit) shown++;
      });
      noneEl.hidden = shown > 0;
    }

    function flag(on) { document.documentElement.toggleAttribute('data-td-dp-open', on); }

    function open() {
      build();
      place();
      if (pop.classList.contains('giencoder-popup-open')) return;
      pop.classList.add('giencoder-popup-open');
      btn.setAttribute('aria-expanded', 'true');
      flag(true);
      pop.focus();
    }

    function close() {
      if (!pop || !pop.classList.contains('giencoder-popup-open')) return;
      pop.classList.remove('giencoder-popup-open');
      btn.setAttribute('aria-expanded', 'false');
      flag(false);
    }

    /* 转派结果：写回 aside「执行人」+ 一条 DS Message 提示 */
    function toast(text) {
      var box = document.querySelector('.td-dp-msg');
      if (!box) {
        box = document.createElement('div');
        box.className = 'td-dp-msg';
        box.innerHTML = '<div class="giencoder-message" role="status">' +
          '<span class="giencoder-message-icon" aria-hidden="true">' + DP_MSG_SVG + '</span>' +
          '<span class="giencoder-message-content"></span></div>';
        box.hidden = true;
        document.body.appendChild(box);
      }
      box.querySelector('.giencoder-message-content').textContent = text;
      box.hidden = false;
      clearTimeout(box._t);
      box._t = setTimeout(function () { box.hidden = true; }, 2400);
    }

    function confirm() {
      var m = DISPATCH_MEMBERS[cur];
      close();
      var rows = document.querySelectorAll('.td-attr-row');
      for (var i = 0; i < rows.length; i++) {
        var k = rows[i].querySelector('.td-attr-k');
        if (!k || k.textContent.indexOf('执行人') < 0) continue;
        var v = rows[i].querySelector('.td-attr-v');
        if (v) v.textContent = m.name;
        break;
      }
      toast('已转派给 ' + m.name);
    }

    btn.addEventListener('click', function () {
      if (pop && pop.classList.contains('giencoder-popup-open')) close(); else open();
    });
    document.addEventListener('pointerdown', function (e) {
      if (!pop || !pop.classList.contains('giencoder-popup-open')) return;
      if (pop.contains(e.target) || btn.contains(e.target)) return;
      close();
    });
    window.addEventListener('resize', function () {
      if (pop && pop.classList.contains('giencoder-popup-open')) place();
    });
    document.addEventListener('td:close-dispatch', close);
  }

  function inject() {
    var main = document.querySelector('main');
    if (!main || main.querySelector('.td-root')) return false;
    var wrap = document.createElement('div');
    wrap.className = 'td-wrap';
    wrap.innerHTML = KB_HTML;
    main.appendChild(wrap);
    bindDetail(wrap);
    bindDescImagePreview(wrap);
    bindDispatchPicker();
    return true;
  }
  /* 注意：两个动作都要执行，不能短路（页签在 React 挂载后才出现，可能晚于注入）。
     inject() 只在首次真正插入时返回 true，所以这里补一个「已注入」判断，
     否则 ready() 永远返回 false、MutationObserver 永不卸载、每次 DOM 变更都白跑一遍。
     页签点击（第 25 轮第 3 项）改由公共片段 SHELL_TABS 承担，见文件尾部。 */
  function ready() {
    var injected = inject() || !!document.querySelector('.td-root');
    var tabbed = syncShellTab();
    return injected && tabbed;
  }
  if (!ready()) {
    var mo = new MutationObserver(function () { if (ready()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
  }
})();
