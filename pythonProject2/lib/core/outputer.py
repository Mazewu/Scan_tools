import sys
from importlib import reload

reload(sys)


class outputer:
    data = {}

    def get(self, key):
        if key in self.data:
            return self.data[key]
        return None

    def add(self, key, data):
        self.data[key] = data

    def add_list(self, key, data):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(data)

    def show(self):
        for key in self.data:
            print
            "%s:%s" % (key, self.data[key])

    def _build_table(self):
        _str = ""
        for key in self.data:
            if isinstance(self.data[key], list):
                _td = ""
                for key2 in self.data[key]:
                    _td += key2 + '</br>'
                _str += "<tr><td>%s</td><td>%s</td></tr>" % (key, _td)
            else:
                _str += "<tr><td>%s</td><td>%s</td></tr>" % (key, self.data[key])
        return _str

    def build_html(self, filename):
        html_head = '''
        <!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="gbk">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>scan Report</title>
    <![endif]-->
  </head>
  <body>
<div class="container container-fluid">
	<div class="row-fluid">
		<div class="span12">
			<h3 class="text-center">
				scan Report
			</h3>
			</BR>
			<table class="table table-bordered">
				<thead>
					<tr>
						<th>
							title
						</th>
						<th>
							content
						</th>
					</tr>
				</thead>
				<tbody>
					build_html_Scan
				</tbody>
			</table>
		</div>
	</div>
</div>  </body>
</html>'''.replace("build_html_Scan", self._build_table())
        file_object = open(filename + '.html', 'w')
        file_object.write(html_head)
        file_object.close()