from perfdump.models import TestTime, SetupTime


class HtmlReport(object):
    """Writes the performance report to an HTML file."""

    @classmethod
    def write(cls, html_file):
        """Writes the HTML report to the given file."""
        f = open(html_file, 'w')
        f.write('<html>')
        f.write('<head>')
        f.write('</head>')
        f.write('<body>')
        f.write('<h1>Test times</h1>')
        
        fmt_test = '<tr><td>{:.05f}</td><td>{}</td></tr><tr><td>&nbsp;</td><td>{}</td></tr>'

        f.write('<table>')
        f.write('<tr><th>Time</th><th>Test info</th></tr>')
        for row in TestTime.get_slowest_tests(10):
            f.write(fmt_test.format(row['elapsed'], row['file'], '{}.{}.{}'.format(row['module'], row['class'], row['func'])))
        f.write('</table>')


        fmt_file = '<tr><td>{:.05f}</td><td>{}</td></tr>'
        f.write('<table>')
        f.write('<tr><th>Time</th><th>Test info</th></tr>')
        for row in TestTime.get_slowest_files(10):
            f.write(fmt_file.format(row['sum_elapsed'], row['file']))
        f.write('</table>')

        
        f.write('<h1>Setup times</h1>')

        f.write('<table>')
        f.write('<tr><th>Time</th><th>Test info</th></tr>')
        for row in SetupTime.get_slowest_tests(10):
            f.write(fmt_test.format(row['elapsed'], row['file'], '{}.{}.{}'.format(row['module'], row['class'], row['func'])))
        f.write('</table>')


        f.write('<table>')
        f.write('<tr><th>Time</th><th>Test info</th></tr>')
        for row in SetupTime.get_slowest_files(10):
            f.write(fmt_file.format(row['sum_elapsed'], row['file']))
        f.write('</table>')

        
        f.write('</body>')
        f.write('</html>')

        f.close()
