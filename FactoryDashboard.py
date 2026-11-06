# CatNip Interactive Report — generated from the block's page (markup, Python, style).
# Edit it in the block's editor: this file is rewritten whenever the editor is saved.
import base64 as _ir_base64
import html as _ir_html
import io as _ir_io
import json as _ir_json_module
import math as _ir_math
import os as _ir_os
import sys as _ir_sys
import threading as _ir_threading
import traceback as _ir_traceback
import uuid as _ir_uuid
import pandas as pd


class FactoryDashboard:
    TITLE = 'Fabryka: harmonogram z ewolucji na GPU'
    HEIGHT = 1400
    KEEP_ALIVE = True
    ACTIONS = {}
    CATNIP_LIVE_ACTIONS = ()
    MARKUP = (
        '<h2>{title}</h2>\n'
        '<p class="cn-muted">Harmonogram {orders_count} zleceń ({genes_count} operacji) na {machines_count} maszynach.\n'
        'Ewolucja: {individuals_text} osobników, {generations_text} pokoleń na {device}. Czas: {seconds_text} s\n'
        '({speed_text} ocen harmonogramu na sekundę). Każde pokolenie liczą kernele CUDA: BreedGeneration,\n'
        'EvaluateSchedules i ReplaceSurvivors.</p>\n'
        '\n'
        '<div class="cn-grid-4">\n'
        '  {kpi("Ważona spóźnialność: ewolucja", best_weighted)}\n'
        '  {kpi("Najlepsza reguła: " + best_rule, rule_weighted)}\n'
        '  {kpi("Poprawa względem reguły", improvement)}\n'
        '  {kpi("Spóźnione zlecenia: ewolucja", late_text)}\n'
        '</div>\n'
        '\n'
        '<h3>Porównanie harmonogramów</h3>\n'
        '{table(comparison_text, page_size=10, sortable=False, filter=False, id="comparison")}\n'
        '\n'
        '<h3>Przebieg ewolucji</h3>\n'
        '{chart("line", history, x="Pokolenie", y=["Najlepszy koszt", "Średni koszt"], layout=history_layout, hovertemplate=cost_hover)}\n'
        '\n'
        '<div class="cn-card">\n'
        '  <div class="cn-grid-3">\n'
        '    <div><b>Harmonogram</b>{select("schedule_name", schedule_names)}</div>\n'
        '    <div><b>Typ maszyny na wykresie Gantta</b>{select("machine_type", machine_options)}</div>\n'
        '    <div><b>Tabela zleceń</b>{checkbox("late_only", "tylko spóźnione")}</div>\n'
        '  </div>\n'
        '</div>\n'
        '\n'
        '<h3>Wykres Gantta: {schedule_name}</h3>\n'
        '{plotly(gantt)}\n'
        '\n'
        '<div class="cn-grid-2">\n'
        '  <div>\n'
        '    <h3>Wykorzystanie maszyn</h3>\n'
        '    {chart("bar", utilization, x="Maszyna", y="Wykorzystanie [%]", layout=utilization_layout, hovertemplate=percent_hover)}\n'
        '  </div>\n'
        '  <div>\n'
        '    <h3>Napływ zleceń na godzinę</h3>\n'
        '    {chart("stacked_bar", arrivals, x="Godzina", y=products, layout=arrivals_layout)}\n'
        '  </div>\n'
        '</div>\n'
        '\n'
        '<h3>Wynik zleceń: {schedule_name}</h3>\n'
        '{table(outcomes_text, page_size=12, sortable=False, id="outcomes")}\n'
        '\n'
        '<h3>Dane wejściowe</h3>\n'
        '<div class="cn-grid-2">\n'
        '  <div><b>Maszyny</b>{table(machines_text, page_size=8, sortable=False, filter=False, id="machines")}</div>\n'
        '  <div><b>Przepisy</b>{table(recipes_text, page_size=8, sortable=False, filter=False, id="recipes")}</div>\n'
        '</div>\n'
        '<p><b>Losowy strumień zleceń</b></p>\n'
        '{table(orders_text, page_size=12, sortable=False, id="orders")}\n'
        '<p class="cn-muted">Pliki CSV: {paths_text}</p>\n'
        ''
    )
    STYLE = (
        '.cn-card { margin-bottom: 12px; }\n'
        'h3 { margin-top: 18px; }\n'
        'td { white-space: nowrap; }\n'
        ''
    )

    def __init__(self, input_tables=None, result=None, report=None, written_paths=None, formatter=None):
        self.input_tables = input_tables
        self.result = result
        self.report = report
        self.written_paths = written_paths
        self.formatter = formatter
        self.data = input_tables
        _ir_init(self, {'input_tables': input_tables, 'result': result, 'report': report, 'written_paths': written_paths, 'formatter': formatter})

    def show(self):
        """Shows the page in the Run Engine's Output tab, or updates it when it is already there."""
        return _ir_show(self)

    def set(self, name, value, refresh=False):
        """Sets a state value; the markup sees it by name. refresh=True renders the page again."""
        self.state[name] = value
        if refresh:
            self.refresh()

    def get(self, name, default=None):
        """A state value — what a control bound to that name holds."""
        return self.state.get(name, default)

    def values(self):
        """A copy of the page's state."""
        return dict(self.state)

    def refresh(self):
        """Renders the page again and sends it to the Run Engine."""
        if self._ir['shown'] and not self._ir['closed']:
            _ir_push(self)

    def toast(self, message, kind='info'):
        """A short message over the page; kind is info, success, warning or error."""
        if self._ir['shown'] and not self._ir['closed'] and _ir_engine():
            _ir_send({'op': 'toast', 'id': self._ir['id'], 'message': str(message), 'kind': kind})
        else:
            print('[%s] %s' % (kind, message), flush=True)

    def close(self):
        """Closes the page; once every page is closed the run may end."""
        _ir_close(self)

    def bind_action(self, name, handler):
        """Calls handler(values) on every click of the action's button — what the generated main does with a live action."""
        _ir_bind(self, name, handler)

    # ── The Python tab ─────────────────────────────────────────────────────

    ALL_MACHINES = "Wszystkie"

    def setup(self):
        self.set("schedule_name", self.report["evolution_name"])
        self.set("machine_type", self.ALL_MACHINES)
        self.set("late_only", False)
        print(self.formatter.frame(self.report["comparison"], decimals=0).to_string(index=False))
        print("Pliki CSV: " + ", ".join(self.written_paths))

    def _gantt(self, operations, machine_type):
        shown = operations if machine_type == self.ALL_MACHINES else operations[operations["Typ"] == machine_type]
        number = self.formatter.number
        traces = []
        for product, group in shown.groupby("Produkt"):
            traces.append({
                "type": "bar", "orientation": "h", "name": product,
                "y": group["Maszyna"].tolist(),
                "x": (group["Koniec [min]"] - group["Start [min]"]).tolist(),
                "base": group["Start [min]"].tolist(),
                "text": ["%s · %s, krok %d<br>%s–%s min" % (row["Zlecenie"], product, row["Krok"],
                                                            number(row["Start [min]"], 0), number(row["Koniec [min]"], 0))
                         for _, row in group.iterrows()],
                "textposition": "none",
                "hovertemplate": "%{text}<extra></extra>",
            })
        machines = sorted(shown["Maszyna"].unique(), reverse=True)
        layout = self.formatter.plotly_layout(x_title="minuta od początku zmiany")
        layout["xaxis"].update({"tickformat": ",.0f", "dtick": 60})
        layout["yaxis"] = {"type": "category", "categoryorder": "array", "categoryarray": machines, "automargin": True}
        layout.update({"barmode": "overlay", "height": max(240, 26 * len(machines) + 90), "bargap": 0.15})
        return {"data": traces, "layout": layout}

    def _arrivals(self, orders):
        hours = orders.assign(Godzina=orders["Napływ [min]"] // 60)
        table = hours.pivot_table(index="Godzina", columns="Produkt", values="Zlecenie", aggfunc="count", fill_value=0)
        table = table.reset_index()
        table["Godzina"] = ["%d–%d h" % (hour, hour + 1) for hour in table["Godzina"]]
        table.columns.name = None
        return table

    def prepare(self):
        report, form, tables, result = self.report, self.formatter, self.input_tables, self.result
        number = form.number
        name = self.get("schedule_name")
        machine_type = self.get("machine_type")
        comparison = report["comparison"]
        evolution = comparison[comparison["Harmonogram"] == report["evolution_name"]].iloc[0]
        rules = comparison[comparison["Harmonogram"] != report["evolution_name"]]
        best_rule = rules.loc[rules["Koszt"].idxmin()]
        rule_weighted = int(best_rule["Ważona spóźnialność [min]"])
        best_weighted = int(evolution["Ważona spóźnialność [min]"])
        outcomes = report["outcomes"][name]
        if self.get("late_only"):
            outcomes = outcomes[outcomes["Spóźnienie [min]"] > 0]
        arrivals = self._arrivals(tables["orders"])
        utilization_layout = form.plotly_layout(y_title="%", y_decimals=1)
        history_layout = form.plotly_layout(y_title="koszt (skala logarytmiczna)", x_title="pokolenie")
        history_layout["yaxis"]["type"] = "log"
        arrivals_layout = form.plotly_layout(y_title="zlecenia")
        arrivals_layout["xaxis"]["type"] = "category"
        return {
            "orders_count": number(len(tables["orders"]), 0),
            "genes_count": number(len(report["operations"][name]), 0),
            "machines_count": number(tables["machines"]["Sztuk"].sum(), 0),
            "individuals_text": number(result.individuals, 0),
            "generations_text": number(result.generations, 0),
            "device": result.device,
            "seconds_text": number(result.seconds, 1),
            "speed_text": number(result.individuals * (result.generations + 1) / result.seconds, 0),
            "best_weighted": number(best_weighted, 0) + " min",
            "best_rule": str(best_rule["Harmonogram"]),
            "rule_weighted": number(rule_weighted, 0) + " min",
            "improvement": form.percent(100.0 * (rule_weighted - best_weighted) / rule_weighted, 1) if rule_weighted else "nie dotyczy",
            "late_text": "%s z %s" % (number(evolution["Spóźnione zlecenia"], 0), number(len(tables["orders"]), 0)),
            "comparison_text": form.frame(comparison, decimals=0),
            "history": result.history,
            "history_layout": history_layout,
            "cost_hover": form.hover(),
            "schedule_names": report["names"],
            "machine_options": [self.ALL_MACHINES] + tables["machines"]["Maszyna"].tolist(),
            "gantt": self._gantt(report["operations"][name], machine_type),
            "utilization": report["utilization"][name],
            "utilization_layout": utilization_layout,
            "percent_hover": form.hover("%", 1),
            "arrivals": arrivals,
            "products": [column for column in arrivals.columns if column != "Godzina"],
            "arrivals_layout": arrivals_layout,
            "outcomes_text": form.frame(outcomes, decimals=0),
            "machines_text": form.frame(tables["machines"], decimals=0),
            "recipes_text": form.frame(tables["recipes"], decimals=0),
            "orders_text": form.frame(tables["orders"], decimals=0),
            "paths_text": ", ".join(self.written_paths),
        }


# ── CatNip interactive report runtime ─────────────────────────────────────────
# Generated with the class above; everything here is shared by every interactive report of a
# process through one hub, so two reports on one page of output never fight over stdin.
#
# The page lives in CatNip's Run Engine. It reaches this process as lines on stdin
# (__CATNIP_UI__ {json}) and this process answers through the ordinary visual stream
# (__VISUAL_START__ {"type": "interactive", ...} __VISUAL_END__) — the two channels every kind of
# run already has, locally, in Docker, in a compiled executable and on the CatNip Server.

_IR_PREFIX = '__CATNIP_UI__'
_IR_LOCAL = _ir_threading.local()


class Html(str):
    """Text that goes into the page as HTML instead of being escaped."""
    __slots__ = ()

    def __html__(self):
        return str(self)


def html(text):
    """Marks text as HTML, to be inserted as it is."""
    return Html('' if text is None else text)


def esc(value):
    """Escapes a value for the page."""
    return _ir_html.escape('' if value is None else str(value), quote=True)


def fmt(value, spec=None):
    """Formats a value with a format spec (',.2f', '.1%', ...); None reads as empty."""
    if value is None:
        return ''
    if not spec:
        return str(value)
    try:
        return format(value, spec)
    except (TypeError, ValueError):
        return str(value)


# ── The hub: one per process ──────────────────────────────────────────────────

def _ir_hub():
    hub = getattr(_ir_sys, '_catnip_interactive_hub', None)
    if hub is None:
        hub = {
            'pages': {},
            'lock': _ir_threading.RLock(),
            'out': _ir_threading.Lock(),
            'reader': None,
            'keeper': None,
            'closed': _ir_threading.Event(),
            'eof': False,
        }
        setattr(_ir_sys, '_catnip_interactive_hub', hub)
    return hub


def _ir_engine():
    """True when a CatNip engine is listening on the other end of stdout and stdin."""
    env = _ir_os.environ
    return bool(env.get('CATNIP_MAIN_PY') or env.get('CATNIP_SCRIPT')
                or env.get('CATNIP_ENGINE') or env.get('CATNIP_INTERACTIVE'))


def _ir_plain(value):
    """A value JSON can carry: numpy scalars, dates, decimals and the like are reduced to one."""
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        return value if _ir_math.isfinite(value) else None
    if isinstance(value, (list, tuple)):
        return [_ir_plain(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _ir_plain(v) for k, v in value.items()}
    if hasattr(value, 'item') and not hasattr(value, '__len__'):
        try:
            return _ir_plain(value.item())
        except Exception:
            pass
    if hasattr(value, 'tolist'):
        try:
            return _ir_plain(value.tolist())
        except Exception:
            pass
    if hasattr(value, 'isoformat'):
        try:
            return value.isoformat()
        except Exception:
            pass
    try:
        import decimal
        if isinstance(value, decimal.Decimal):
            return float(value)
    except Exception:
        pass
    return str(value)


def _ir_json(value):
    return _ir_json_module.dumps(_ir_plain(value), separators=(',', ':'), ensure_ascii=False)


def _ir_send(message):
    web = _ir_hub().get('web')
    if web is not None:
        _ir_web_publish(web, message)
        return
    body = _ir_json(message).encode('utf-8')
    payload = _ir_json_module.dumps({
        'type': 'interactive',
        'title': message.get('title', ''),
        'data': _ir_base64.b64encode(body).decode('ascii'),
    })
    with _ir_hub()['out']:
        _ir_sys.stdout.write('__VISUAL_START__' + payload + '__VISUAL_END__\n')
        _ir_sys.stdout.flush()


def _ir_register(page, keep_alive):
    hub = _ir_hub()
    with hub['lock']:
        hub['pages'][page._ir['id']] = page
        if hub['eof']:
            return
        # In a browser of its own the page talks over HTTP; stdin is the user's console.
        if hub['reader'] is None and hub.get('web') is None:
            hub['reader'] = _ir_threading.Thread(target=_ir_read_loop, name='catnip-interactive', daemon=True)
            hub['reader'].start()
        # The keeper is what keeps the process alive after the flow finished: the reader is a
        # daemon thread and would die with the main one.
        if keep_alive and hub['keeper'] is None:
            hub['keeper'] = _ir_threading.Thread(target=hub['closed'].wait, name='catnip-interactive-keeper')
            hub['keeper'].start()


def _ir_unregister(page_id):
    hub = _ir_hub()
    with hub['lock']:
        hub['pages'].pop(page_id, None)
        if not hub['pages']:
            hub['closed'].set()


def _ir_read_loop():
    hub = _ir_hub()
    stream = _ir_sys.stdin
    while True:
        try:
            line = stream.readline() if stream is not None else ''
        except Exception:
            line = ''
        if not line:
            # Nobody will ever answer again (the run was stopped, or nothing was attached):
            # whoever is waiting for a click must be let go, and the process may end.
            with hub['lock']:
                hub['eof'] = True
                pages = list(hub['pages'].values())
            for page in pages:
                _ir_release_waiters(page)
            hub['closed'].set()
            return
        line = line.strip()
        if not line.startswith(_IR_PREFIX):
            continue
        try:
            message = _ir_json_module.loads(line[len(_IR_PREFIX):])
        except ValueError:
            continue
        with hub['lock']:
            page = hub['pages'].get(message.get('page'))
        if page is None:
            continue
        try:
            _ir_dispatch(page, message)
        except Exception:
            _ir_traceback.print_exc()


# ── On its own: the page in a browser ─────────────────────────────────────────
# A compiled executable or `python main_1.py` has no Run Engine to draw the page. It serves the
# same host page CatNip uses (the catnip_web folder shipped beside the program) from a server on
# 127.0.0.1 behind a random token, and opens it in a browser window: renders reach the page as
# server-sent events, the page's messages come back as POSTs and are dispatched exactly as the
# stdin lines are. The process lives until the browser window has been closed.
# No class is declared here: the report must stay the only class with an __init__ in its file,
# so the request handler is built with type().

_IR_WEB_FILES = {
    'catnip-report.js': 'application/javascript; charset=utf-8',
    'catnip-report.css': 'text/css; charset=utf-8',
    'plotly.min.js': 'application/javascript; charset=utf-8',
}

_IR_BRIDGE = (
    '<script>(function(){var base=location.pathname.replace(/[^/]*$/,""),gone=false;'
    'window.invokeCSharpAction=function(body){fetch(base+"msg",{method:"POST",'
    'headers:{"Content-Type":"application/json"},body:body}).catch(function(){});};'
    'var es=new EventSource(base+"events");'
    'es.onopen=function(){gone=false;};'
    'es.onmessage=function(e){window.catnip.apply(JSON.parse(e.data));};'
    'es.onerror=function(){if(!gone){gone=true;'
    'window.catnip.apply({op:"ended",reason:"The program has ended."});}};'
    '})();</script>')


def _ir_web_dir():
    """The folder holding host.html and its scripts: beside this module (inside a onefile
    executable that is its unpack folder), beside the program, or CATNIP_WEB_DIR."""
    roots = []
    if _ir_os.environ.get('CATNIP_WEB_DIR'):
        roots.append(_ir_os.environ['CATNIP_WEB_DIR'])
    here = globals().get('__file__')
    if here:
        roots.append(_ir_os.path.join(_ir_os.path.dirname(_ir_os.path.abspath(here)), 'catnip_web'))
    for base in (_ir_sys.argv[0] if _ir_sys.argv else '', _ir_sys.executable):
        if base:
            roots.append(_ir_os.path.join(_ir_os.path.dirname(_ir_os.path.abspath(base)), 'catnip_web'))
    for root in roots:
        if _ir_os.path.isfile(_ir_os.path.join(root, 'host.html')) and \
                _ir_os.path.isfile(_ir_os.path.join(root, 'catnip-report.js')):
            return root
    return None


def _ir_web_start(title):
    """Starts the page server once per process and opens the browser; False when it cannot."""
    hub = _ir_hub()
    with hub['lock']:
        if hub.get('web') is not None:
            return True
        if hub.get('web_failed'):
            return False
        hub['web_failed'] = True
        folder = _ir_web_dir()
        if folder is None:
            print('[CatNip] The page files (a catnip_web folder) were not found beside the program.', flush=True)
            return False
        try:
            import http.server as _ir_http
            web = {'dir': folder, 'token': _ir_uuid.uuid4().hex, 'title': title,
                   'cond': _ir_threading.Condition(), 'version': 0, 'renders': {}, 'events': [],
                   'clients': 0, 'seen': False, 'quiet_since': None}
            handler = type('_IrWebHandler', (_ir_http.BaseHTTPRequestHandler,), {
                'do_GET': _ir_web_get,
                'do_POST': _ir_web_post,
                'log_message': lambda self, *args: None,
            })
            server = _ir_http.ThreadingHTTPServer(('127.0.0.1', 0), handler)
        except Exception as ex:
            print('[CatNip] The page server could not start: %s' % ex, flush=True)
            return False
        server.daemon_threads = True
        server.catnip_web = web
        web['port'] = server.server_address[1]
        hub['web'] = web
        hub['web_failed'] = False
    _ir_threading.Thread(target=server.serve_forever, name='catnip-page-server', daemon=True).start()
    _ir_threading.Thread(target=_ir_web_watch, args=(web,), name='catnip-page-watch', daemon=True).start()
    url = 'http://127.0.0.1:%d/%s/' % (web['port'], web['token'])
    print('[CatNip] %s is open in a browser window: %s\n'
          '[CatNip] The program ends when that window is closed (or press Ctrl+C).' % (title, url), flush=True)
    _ir_web_open(url)
    return True


def _ir_web_open(url):
    """A window of its own (Edge/Chrome app mode) when one of them is installed, else the
    default browser."""
    if _ir_os.environ.get('CATNIP_NO_BROWSER'):
        return  # a headless machine, or a test: the address printed above is all there is
    import shutil
    import subprocess
    candidates = []
    if _ir_sys.platform == 'win32':
        for root in (_ir_os.environ.get('ProgramFiles(x86)'), _ir_os.environ.get('ProgramFiles'),
                     _ir_os.environ.get('LOCALAPPDATA')):
            if root:
                candidates.append(_ir_os.path.join(root, 'Microsoft', 'Edge', 'Application', 'msedge.exe'))
                candidates.append(_ir_os.path.join(root, 'Google', 'Chrome', 'Application', 'chrome.exe'))
    elif _ir_sys.platform != 'darwin':
        for name in ('microsoft-edge', 'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'):
            found = shutil.which(name)
            if found:
                candidates.append(found)
    for exe in candidates:
        if _ir_os.path.isfile(exe):
            try:
                subprocess.Popen([exe, '--app=' + url, '--new-window'],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except Exception:
                pass
    try:
        import webbrowser
        webbrowser.open_new(url)
    except Exception:
        pass


def _ir_web_publish(web, message):
    with web['cond']:
        web['version'] += 1
        if message.get('op') == 'render':
            web['renders'][message.get('id')] = (web['version'], message)
        else:
            web['events'].append((web['version'], message))
            del web['events'][:-200]
        web['cond'].notify_all()


def _ir_web_allowed(handler, web):
    """The token is the capability; the Host check keeps a rebound DNS name out as well."""
    host = handler.headers.get('Host', '')
    return host in ('127.0.0.1:%d' % web['port'], 'localhost:%d' % web['port'])


def _ir_web_get(self):
    web = self.server.catnip_web
    prefix = '/' + web['token'] + '/'
    path = self.path.split('?', 1)[0]
    if not _ir_web_allowed(self, web) or not path.startswith(prefix):
        self.send_error(404)
        return
    name = path[len(prefix):]
    if name == 'events':
        _ir_web_events(self, web)
        return
    try:
        if name in ('', 'host.html'):
            with open(_ir_os.path.join(web['dir'], 'host.html'), encoding='utf-8') as f:
                text = f.read()
            text = text.replace('<title>CatNip interactive report</title>', '<title>%s</title>' % esc(web['title']), 1)
            text = text.replace('</body>', _IR_BRIDGE + '</body>', 1)
            body, ctype = text.encode('utf-8'), 'text/html; charset=utf-8'
        elif name in _IR_WEB_FILES:
            with open(_ir_os.path.join(web['dir'], name), 'rb') as f:
                body, ctype = f.read(), _IR_WEB_FILES[name]
        else:
            self.send_error(404)
            return
    except OSError:
        self.send_error(404)
        return
    self.send_response(200)
    self.send_header('Content-Type', ctype)
    self.send_header('Content-Length', str(len(body)))
    self.send_header('Cache-Control', 'no-store')
    self.end_headers()
    self.wfile.write(body)


def _ir_web_events(self, web):
    self.send_response(200)
    self.send_header('Content-Type', 'text/event-stream; charset=utf-8')
    self.send_header('Cache-Control', 'no-cache')
    self.end_headers()
    with web['cond']:
        web['clients'] += 1
        web['seen'] = True
        last = web['version']
        batch = sorted(web['renders'].values(), key=lambda item: item[0])
    try:
        while True:
            if batch:
                for _, message in batch:
                    if message.get('op') == 'close':
                        message = {'op': 'ended', 'id': message.get('id'), 'reason': 'The report was closed.'}
                    self.wfile.write(('data: ' + _ir_json(message) + '\n\n').encode('utf-8'))
            else:
                self.wfile.write(b': ping\n\n')
            self.wfile.flush()
            with web['cond']:
                # A closed window is only noticed when a write fails, so the ping is frequent.
                if web['version'] == last:
                    web['cond'].wait(5)
                batch = sorted([item for item in web['renders'].values() if item[0] > last]
                               + [item for item in web['events'] if item[0] > last], key=lambda item: item[0])
                last = web['version']
    except Exception:
        pass
    finally:
        with web['cond']:
            web['clients'] -= 1
            if web['clients'] == 0:
                import time
                web['quiet_since'] = time.monotonic()


def _ir_web_post(self):
    web = self.server.catnip_web
    if not _ir_web_allowed(self, web) or self.path.split('?', 1)[0] != '/' + web['token'] + '/msg':
        self.send_error(404)
        return
    try:
        length = min(int(self.headers.get('Content-Length') or 0), 16 * 1024 * 1024)
    except ValueError:
        length = 0
    raw = self.rfile.read(length) if length > 0 else b''
    self.send_response(204)
    self.send_header('Content-Length', '0')
    self.end_headers()
    try:
        message = _ir_json_module.loads(raw.decode('utf-8'))
    except ValueError:
        return
    if not isinstance(message, dict):
        return
    hub = _ir_hub()
    with hub['lock']:
        page = hub['pages'].get(message.get('page'))
    if page is None:
        return
    try:
        _ir_dispatch(page, message)
    except Exception:
        _ir_traceback.print_exc()


def _ir_web_watch(web):
    """Ends the wait once the browser window has been closed: no page connected for 10 s after
    one was (a reload reconnects well within that)."""
    import time
    hub = _ir_hub()
    while not hub['closed'].is_set():
        time.sleep(1)
        with web['cond']:
            quiet = web['seen'] and web['clients'] == 0 and web['quiet_since'] is not None \
                and time.monotonic() - web['quiet_since'] > 10
        if quiet:
            with hub['lock']:
                hub['eof'] = True
                pages = list(hub['pages'].values())
            for page in pages:
                _ir_release_waiters(page)
            hub['closed'].set()
            return


# ── A page ────────────────────────────────────────────────────────────────────

def _ir_init(page, inputs):
    page.state = {}
    page._ir = {
        'id': _ir_uuid.uuid4().hex,
        'shown': False,
        'closed': False,
        'bindings': {},
        'waiters': {},
        'pending': {},
        'controls': {},
        'counter': 0,
        'inputs': inputs,
        'lock': _ir_threading.RLock(),
    }
    setup = getattr(page, 'setup', None)
    if callable(setup):
        setup()


def _ir_show(page):
    ir = page._ir
    if ir['closed']:
        return None
    if not _ir_engine():
        # Run on its own (a compiled executable, `python main_1.py`): the page opens in the
        # browser and talks to this process over a local HTTP server.
        if _ir_sys.gettrace() is None and _ir_web_start(type(page).TITLE):
            ir['shown'] = True
            # Kept alive whatever KEEP_ALIVE says: the browser connects after show() returns, and
            # a process that had already ended would leave it an empty window.
            _ir_register(page, True)
            _ir_push(page)
            return None
        print('[CatNip] %s: an interactive report is shown by the CatNip Run Engine or in a browser; '
              'neither is available here.' % type(page).TITLE, flush=True)
        return None
    if _ir_sys.gettrace() is not None:
        # A debugger reads stdin too, and the page would steal its commands.
        print('[CatNip] %s: the page stays static while debugging.' % type(page).TITLE, flush=True)
        ir['shown'] = True
        _ir_push(page, interactive=False)
        return None
    ir['shown'] = True
    _ir_register(page, type(page).KEEP_ALIVE)
    _ir_push(page)
    return None


def _ir_push(page, interactive=True):
    """Renders the page and sends it; the Run Engine replaces the card with the same id."""
    cls = type(page)
    try:
        body = _ir_render(page)
    except Exception as ex:
        _ir_traceback.print_exc()
        body = '<div class="cn-error-page"><b>The page could not be rendered.</b><pre>%s</pre></div>' % esc(
            '%s: %s' % (type(ex).__name__, ex))
    _ir_send({
        'op': 'render',
        'id': page._ir['id'],
        'title': cls.TITLE,
        'height': cls.HEIGHT,
        'css': cls.STYLE,
        'html': body,
        'interactive': interactive,
        'actions': dict(cls.ACTIONS),
    })


def _ir_namespace(page):
    namespace = dict(globals())
    prepare = getattr(page, 'prepare', None)
    extra = prepare() if callable(prepare) else None
    namespace.update(page.state)
    for name, value in page._ir['inputs'].items():
        namespace[name] = getattr(page, name, value)
    namespace.update({'self': page, 'state': page.state, 'data': page.data, 'title': type(page).TITLE})
    if isinstance(extra, dict):
        namespace.update(extra)
    return namespace


def _ir_render(page):
    with page._ir['lock']:
        page._ir['counter'] = 0
        page._ir['controls'] = {}
        previous = (getattr(_IR_LOCAL, 'page', None), getattr(_IR_LOCAL, 'namespace', None))
        _IR_LOCAL.page = page
        _IR_LOCAL.namespace = None
        try:
            namespace = _ir_namespace(page)
            # A control placed further up gives its state value a default as it renders; the holes
            # below it must see that value, so the namespace is shared with _ir_default.
            _IR_LOCAL.namespace = namespace
            return _ir_template(type(page).MARKUP, namespace)
        finally:
            _IR_LOCAL.page, _IR_LOCAL.namespace = previous


def _ir_current():
    page = getattr(_IR_LOCAL, 'page', None)
    if page is None:
        raise RuntimeError('controls, charts and tables are placed from the markup, while the page renders')
    return page


def _ir_next_id(prefix):
    page = getattr(_IR_LOCAL, 'page', None)
    if page is None:
        return 'cn-%s-%s' % (prefix, _ir_uuid.uuid4().hex[:8])
    page._ir['counter'] += 1
    return 'cn-%s-%d' % (prefix, page._ir['counter'])


def _ir_dispatch(page, message):
    op = message.get('op')
    if op == 'ready':
        _ir_push(page)
        return
    if op == 'close':
        _ir_close(page, notify=False)
        return
    if op == 'change':
        name = str(message.get('name') or '')
        if not name:
            return
        value = message.get('value')
        page.state[name] = value
        hook = getattr(page, 'on_%s_change' % name, None)
        if callable(hook):
            _ir_guard(page, hook, value)
        else:
            hook = getattr(page, 'on_change', None)
            if callable(hook):
                _ir_guard(page, hook, name, value)
        _ir_push(page)
        return
    if op == 'call':
        name = str(message.get('name') or '')
        method = getattr(page, name, None) if name and not name.startswith('_') else None
        if callable(method):
            _ir_guard(page, method)
        else:
            page.toast('The page has no method called %s.' % name, 'error')
        _ir_push(page)
        return
    if op == 'action':
        _ir_fire(page, str(message.get('name') or ''))


def _ir_guard(page, func, *args):
    try:
        return func(*args)
    except Exception as ex:
        _ir_traceback.print_exc()
        page.toast('%s: %s' % (type(ex).__name__, ex), 'error')
        return None


def _ir_payload(page, name):
    values = dict(page.state)
    hook = getattr(page, 'on_' + name, None)
    if callable(hook):
        result = hook(values)
        if result is not None:
            return result
    return values


def _ir_fire(page, name):
    ir = page._ir
    if name not in type(page).ACTIONS:
        page.toast('The page has no action called %s.' % name, 'error')
        return
    with ir['lock']:
        waiter = ir['waiters'].pop(name, None)
        binding = ir['bindings'].get(name)
    try:
        payload = _ir_payload(page, name)
    except Exception as ex:
        _ir_traceback.print_exc()
        page.toast('%s: %s' % (type(ex).__name__, ex), 'error')
        return
    if waiter is not None:
        waiter['payload'] = payload
        waiter['event'].set()
        return
    if (binding is None and type(page).ACTIONS.get(name) == 'live'
            and _ir_threading.main_thread().is_alive()
            and _ir_os.environ.get('CATNIP_INTERACTIVE') != 'preview'):
        # The generated main binds live actions after the rest of the flow has been called, and
        # the flow may still be on its way there (waiting at a submit, say): the click is kept
        # and handled the moment the binding arrives.
        with ir['lock']:
            ir['pending'][name] = payload
        page.toast('"%s" runs as soon as the flow reaches it.' % name, 'info')
        return
    if binding is None:
        if _ir_os.environ.get('CATNIP_INTERACTIVE') == 'preview':
            page.toast('%s would hand over: %s' % (name, _ir_json(payload)[:400]), 'info')
        else:
            page.toast('Nothing is waiting for "%s" — connect a block to its output and run the generated main.' % name, 'warning')
        return
    _ir_run_binding(page, name, binding, payload)


def _ir_run_binding(page, name, binding, payload):
    ir = page._ir
    _ir_send({'op': 'busy', 'id': ir['id'], 'on': True, 'label': name})
    try:
        _ir_guard(page, binding, payload)
    finally:
        _ir_send({'op': 'busy', 'id': ir['id'], 'on': False})
        _ir_push(page)


def _ir_bind(page, name, handler):
    ir = page._ir
    with ir['lock']:
        ir['bindings'][name] = handler
        pending = ir['pending'].pop(name, None)
    if pending is not None:
        _ir_run_binding(page, name, handler, pending)


def _ir_wait(page, name):
    """The output of a submit action: shows the page if it is not shown, then waits for the click."""
    ir = page._ir
    if not ir['shown']:
        page.show()
    hub = _ir_hub()
    listening = _ir_engine() or hub.get('web') is not None
    if ir['closed'] or not listening or hub['eof'] or _ir_sys.gettrace() is not None:
        # Nobody can click: carry on with what the page holds.
        return _ir_payload(page, name)
    waiter = {'event': _ir_threading.Event(), 'payload': None}
    with ir['lock']:
        ir['waiters'][name] = waiter
    _ir_send({'op': 'waiting', 'id': ir['id'], 'action': name})
    waiter['event'].wait()
    _ir_send({'op': 'waiting', 'id': ir['id'], 'action': None})
    return waiter['payload']


def _ir_release_waiters(page):
    with page._ir['lock']:
        waiters = list(page._ir['waiters'].values())
        page._ir['waiters'].clear()
    for waiter in waiters:
        waiter['event'].set()


def _ir_close(page, notify=True):
    ir = page._ir
    if ir['closed']:
        return
    ir['closed'] = True
    _ir_release_waiters(page)
    if notify and ir['shown']:
        _ir_send({'op': 'close', 'id': ir['id']})
    _ir_unregister(ir['id'])


# ── The template: HTML with {python} holes ───────────────────────────────────

_IR_COMPILED = {}


def _ir_template(text, namespace):
    out = []
    i = 0
    n = len(text)
    lower = text.lower()
    while i < n:
        c = text[i]
        if c == '<' and (lower.startswith('<script', i) or lower.startswith('<style', i)):
            # Script and style blocks are copied as they are: their braces are not holes.
            tag = 'script' if lower.startswith('<script', i) else 'style'
            end = lower.find('</' + tag, i)
            end = n if end < 0 else lower.find('>', end) + 1 or n
            out.append(text[i:end])
            i = end
            continue
        if c == '{':
            if text.startswith('{{', i):
                out.append('{')
                i += 2
                continue
            close = _ir_matching(text, i)
            if close < 0:
                out.append(text[i:])
                break
            out.append(_ir_hole(text[i + 1:close], namespace))
            i = close + 1
            continue
        if c == '}':
            out.append('}')
            i += 2 if text.startswith('}}', i) else 1
            continue
        nxt = min([p for p in (text.find('{', i), text.find('}', i), lower.find('<s', i)) if p >= 0] or [n])
        if nxt == i:
            nxt = i + 1
        out.append(text[i:nxt])
        i = nxt
    return ''.join(out)


def _ir_matching(text, start):
    """The brace closing the one at start, skipping braces inside strings and nested brackets."""
    depth = 0
    quote = None
    i = start
    while i < len(text):
        c = text[i]
        if quote:
            if c == '\\':
                i += 2
                continue
            if text.startswith(quote, i):
                i += len(quote)
                quote = None
                continue
        elif c in '\'"':
            quote = c * 3 if text.startswith(c * 3, i) else c
            i += len(quote)
            continue
        elif c in '{[(':
            depth += 1
        elif c in '}])':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _ir_hole(expression, namespace):
    raw = expression.startswith('!')
    source = expression[1:] if raw else expression
    source = source.strip()
    if not source:
        return ''
    try:
        code = _IR_COMPILED.get(source)
        if code is None:
            code = compile(source, '<markup {%s}>' % source[:60], 'eval')
            _IR_COMPILED[source] = code
        value = eval(code, namespace)
    except Exception as ex:
        return '<span class="cn-error" title="%s">{%s} → %s: %s</span>' % (
            esc(source), esc(source[:80]), esc(type(ex).__name__), esc(ex))
    return _ir_value(value, raw)


def _ir_value(value, raw=False):
    if value is None:
        return ''
    if hasattr(value, '__html__'):
        return str(value.__html__())
    if raw:
        return str(value)
    if hasattr(value, 'to_plotly_json'):
        return plotly(value)
    if hasattr(value, 'savefig'):
        return figure(value)
    if hasattr(value, 'columns') and hasattr(value, 'itertuples'):
        return table(value)
    if isinstance(value, float):
        return esc(_ir_number(value))
    return esc(value)


def _ir_number(value):
    if value != value:
        return ''
    if float(value).is_integer() and abs(value) < 1e15:
        return str(int(value))
    return ('%.6g' % value) if abs(value) < 1e-4 or abs(value) >= 1e15 else str(round(value, 6))


# ── Data shapes ───────────────────────────────────────────────────────────────

def _ir_table(rows, columns=None, limit=0):
    """(headers, rows of values) out of a DataFrame, numpy array, dict of columns, list of dicts
    or list of rows — resolved when the page renders, so the data may change shape between runs."""
    if rows is None:
        return [], []
    limit = int(limit or 0)
    if hasattr(rows, 'columns') and hasattr(rows, 'itertuples'):
        frame = rows[list(columns)] if columns else rows
        if limit > 0:
            frame = frame.head(limit)
        return [str(c) for c in frame.columns], [list(r) for r in frame.itertuples(index=False, name=None)]
    if hasattr(rows, 'column_names') and hasattr(rows, 'to_pylist'):          # pyarrow Table
        return _ir_table(rows.to_pylist(), columns, limit)
    if hasattr(rows, 'tolist') and not isinstance(rows, (list, tuple, dict)):
        rows = rows.tolist()
    if isinstance(rows, dict):
        headers = [str(k) for k in (columns or rows.keys())]
        cols = [rows.get(h, []) for h in headers]
        cols = [c.tolist() if hasattr(c, 'tolist') else list(c) if hasattr(c, '__iter__') and not isinstance(c, str) else [c] for c in cols]
        length = max((len(c) for c in cols), default=0)
        if limit > 0:
            length = min(length, limit)
        return headers, [[c[i] if i < len(c) else None for c in cols] for i in range(length)]
    rows = list(rows)
    if not rows:
        return [str(c) for c in (columns or [])], []
    if limit > 0:
        rows = rows[:limit]
    if isinstance(rows[0], dict):
        headers = [str(k) for k in (columns or rows[0].keys())]
        return headers, [[row.get(h) for h in headers] for row in rows]
    if hasattr(rows[0], '_fields'):                                            # namedtuple
        headers = list(columns or rows[0]._fields)
        return headers, [[getattr(row, h, None) for h in headers] for row in rows]
    cells = [list(row) if hasattr(row, '__iter__') and not isinstance(row, str) else [row] for row in rows]
    width = max(len(r) for r in cells)
    headers = [str(c) for c in columns] if columns else ['Column %d' % (i + 1) for i in range(width)]
    return headers, cells


def rows_of(data, columns=None):
    """Any tabular shape as a list of dicts — the easiest form to compute with in a report."""
    if data is None:
        return []
    headers, cells = _ir_table(data, columns)
    return [dict(zip(headers, row)) for row in cells]


def column(data, key):
    """One column of any tabular shape as a list; a sequence passed as the key comes back as a list."""
    if key is None:
        return None
    if not isinstance(key, str):
        return key.tolist() if hasattr(key, 'tolist') else list(key)
    if data is None:
        raise KeyError('no data to take the column %r from' % key)
    if hasattr(data, 'columns') and hasattr(data, 'itertuples'):
        return data[key].tolist()
    if isinstance(data, dict):
        values = data[key]
        return values.tolist() if hasattr(values, 'tolist') else list(values)
    headers, cells = _ir_table(data)
    if key not in headers:
        raise KeyError('no column %r — the data has %s' % (key, ', '.join(headers) or 'no columns'))
    index = headers.index(key)
    return [row[index] if index < len(row) else None for row in cells]


def _ir_data(data):
    if data is None:
        page = getattr(_IR_LOCAL, 'page', None)
        return page.data if page is not None else None
    return data


def _ir_attrs(**attributes):
    parts = []
    for key, value in attributes.items():
        if value is None or value is False:
            continue
        key = key.rstrip('_').replace('_', '-')
        parts.append(key if value is True else '%s="%s"' % (key, esc(value)))
    return ' '.join(parts)


def _ir_json_block(value):
    return _ir_json(value).replace('</', '<\\/')


def _ir_label(label, for_id, body, css='cn-field'):
    caption = '<label class="cn-label" for="%s">%s</label>' % (for_id, esc(label)) if label else ''
    return Html('<div class="%s">%s%s</div>' % (css, caption, body))


def _ir_default(name, value):
    page = _ir_current()
    if name not in page.state:
        page.state[name] = value
        namespace = getattr(_IR_LOCAL, 'namespace', None)
        if namespace is not None:
            namespace.setdefault(name, value)
    page._ir['controls'][name] = True
    return page.state[name]


# ── Controls: each one is bound to the state value of its name ───────────────

def slider(name, min=0, max=100, step=1, value=None, label=None, live=False, format=None):
    """A slider; the state value changes when it is released, or while dragging with live=True."""
    current = _ir_default(name, min if value is None else value)
    control_id = 'cn-' + name
    shown = fmt(current, format)
    body = ('<div class="cn-slider-row"><input type="range" %s/><output class="cn-slider-value" data-cn-format="%s">%s</output></div>'
            % (_ir_attrs(id=control_id, class_='cn-slider', min=min, max=max, step=step, value=current,
                         data_cn_bind=name, data_cn_type='number', data_cn_live='1' if live else None),
               esc(format or ''), esc(shown)))
    return _ir_label(label, control_id, body)


def number(name, value=None, min=None, max=None, step=None, label=None, integer=False):
    """A number box."""
    current = _ir_default(name, 0 if value is None else value)
    control_id = 'cn-' + name
    body = '<input type="number" %s/>' % _ir_attrs(
        id=control_id, class_='cn-input', value=current, min=min, max=max, step=step if step is not None else (1 if integer else 'any'),
        data_cn_bind=name, data_cn_type='int' if integer else 'number')
    return _ir_label(label, control_id, body)


def text_input(name, value='', label=None, placeholder=None):
    """A one-line text box; the state value changes when it loses focus or Enter is pressed."""
    current = _ir_default(name, value)
    control_id = 'cn-' + name
    body = '<input type="text" %s/>' % _ir_attrs(
        id=control_id, class_='cn-input', value=current, placeholder=placeholder, data_cn_bind=name, data_cn_type='text')
    return _ir_label(label, control_id, body)


def textarea(name, value='', label=None, rows=4, placeholder=None):
    """A multi-line text box."""
    current = _ir_default(name, value)
    control_id = 'cn-' + name
    body = '<textarea %s>%s</textarea>' % (_ir_attrs(
        id=control_id, class_='cn-input', rows=rows, placeholder=placeholder, data_cn_bind=name, data_cn_type='text'), esc(current))
    return _ir_label(label, control_id, body)


def _ir_options(options):
    if options is None:
        return []
    if isinstance(options, dict):
        return [(k, v) for k, v in options.items()]
    if hasattr(options, 'tolist'):
        options = options.tolist()
    result = []
    for option in options:
        if isinstance(option, (list, tuple)) and len(option) == 2:
            result.append((option[0], option[1]))
        else:
            result.append((option, option))
    return result


def _ir_option_type(pairs):
    values = [v for v, _ in pairs]
    if values and all(isinstance(v, bool) for v in values):
        return 'bool'
    if values and all(isinstance(v, int) and not isinstance(v, bool) for v in values):
        return 'int'
    if values and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values):
        return 'number'
    return 'text'


def select(name, options, value=None, label=None):
    """A combo box. Options are values, (value, caption) pairs or a {value: caption} dictionary."""
    pairs = _ir_options(options)
    current = _ir_default(name, value if value is not None else (pairs[0][0] if pairs else None))
    control_id = 'cn-' + name
    items = ''.join('<option value="%s"%s>%s</option>' % (esc(v), ' selected' if v == current else '', esc(c)) for v, c in pairs)
    body = '<select %s>%s</select>' % (_ir_attrs(
        id=control_id, class_='cn-input', data_cn_bind=name, data_cn_type=_ir_option_type(pairs)), items)
    return _ir_label(label, control_id, body)


def multiselect(name, options, value=None, label=None, size=5):
    """A list in which several options may be chosen; the state value is a list."""
    pairs = _ir_options(options)
    current = _ir_default(name, list(value or []))
    control_id = 'cn-' + name
    items = ''.join('<option value="%s"%s>%s</option>' % (esc(v), ' selected' if v in (current or []) else '', esc(c)) for v, c in pairs)
    body = '<select multiple %s>%s</select>' % (_ir_attrs(
        id=control_id, class_='cn-input', size=size, data_cn_bind=name, data_cn_type='multi:' + _ir_option_type(pairs)), items)
    return _ir_label(label, control_id, body)


def radio(name, options, value=None, label=None, inline=True):
    """A group of radio buttons."""
    pairs = _ir_options(options)
    current = _ir_default(name, value if value is not None else (pairs[0][0] if pairs else None))
    control_id = 'cn-' + name
    kind = _ir_option_type(pairs)
    items = ''.join('<label class="cn-choice"><input type="radio" name="%s" value="%s"%s/> %s</label>'
                    % (control_id, esc(v), ' checked' if v == current else '', esc(c)) for v, c in pairs)
    body = '<div %s>%s</div>' % (_ir_attrs(id=control_id, class_='cn-radio' + (' cn-inline' if inline else ''),
                                           data_cn_bind=name, data_cn_type=kind), items)
    return _ir_label(label, control_id, body)


def checkbox(name, label='', value=False):
    """A check box; the state value is True or False."""
    current = bool(_ir_default(name, bool(value)))
    control_id = 'cn-' + name
    return Html('<label class="cn-choice cn-field"><input type="checkbox" %s/> %s</label>' % (_ir_attrs(
        id=control_id, checked=current, data_cn_bind=name, data_cn_type='bool'), esc(label)))


def toggle(name, label='', value=False):
    """An on/off switch; the state value is True or False."""
    current = bool(_ir_default(name, bool(value)))
    control_id = 'cn-' + name
    return Html('<label class="cn-toggle cn-field"><input type="checkbox" %s/><span class="cn-toggle-track"></span> %s</label>' % (_ir_attrs(
        id=control_id, checked=current, data_cn_bind=name, data_cn_type='bool'), esc(label)))


def date_input(name, value=None, label=None):
    """A date picker; the state value is an ISO date string ('2026-10-05')."""
    if value is not None and hasattr(value, 'isoformat'):
        value = value.isoformat()[:10]
    current = _ir_default(name, value or '')
    control_id = 'cn-' + name
    body = '<input type="date" %s/>' % _ir_attrs(id=control_id, class_='cn-input', value=current, data_cn_bind=name, data_cn_type='text')
    return _ir_label(label, control_id, body)


def color_input(name, value='#3366cc', label=None):
    """A colour picker; the state value is '#rrggbb'."""
    current = _ir_default(name, value)
    control_id = 'cn-' + name
    body = '<input type="color" %s/>' % _ir_attrs(id=control_id, class_='cn-color', value=current, data_cn_bind=name, data_cn_type='text')
    return _ir_label(label, control_id, body)


def button(label, action=None, call=None, kind='primary', confirm=None, disabled=False):
    """A button. action= fires one of the report's actions (an output of the block); call= runs a
    method of the report and renders the page again."""
    return Html('<button type="button" %s>%s</button>' % (_ir_attrs(
        class_='cn-button cn-' + kind, data_cn_action=action, data_cn_call=call, data_cn_confirm=confirm,
        disabled=bool(disabled)), esc(label)))


# ── Displays ──────────────────────────────────────────────────────────────────

def table(rows=None, columns=None, page_size=20, height=None, sortable=True, filter=True, select=None,
          formats=None, max_rows=20000, id=None):
    """A table with sorting, filtering and pages. select= names a state value that receives the
    clicked row as a dictionary."""
    headers, cells = _ir_table(_ir_data(rows), columns)
    total = len(cells)
    cells = cells[:max_rows] if max_rows else cells
    if select:
        _ir_default(select, None)
    spec = {
        'columns': headers, 'rows': cells, 'total': total, 'pageSize': page_size,
        'sortable': sortable, 'filter': filter, 'select': select, 'formats': formats or {},
    }
    style = 'max-height:%dpx' % height if height else None
    return Html('<div %s><script type="application/json">%s</script></div>' % (_ir_attrs(
        id=id or _ir_next_id('table'), class_='cn-table', data_cn_table='1', data_cn_opaque='1', style=style),
        _ir_json_block(spec)))


_IR_PALETTE = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099', '#0099c6', '#dd4477', '#66aa00', '#b82e2e', '#316395']


def _ir_series(data, keys):
    if keys is None:
        return []
    if isinstance(keys, str):
        return [(keys, column(data, keys))]
    keys = keys.tolist() if hasattr(keys, 'tolist') else list(keys)
    if keys and all(isinstance(k, str) for k in keys) and data is not None:
        return [(k, column(data, k)) for k in keys]
    if keys and all(isinstance(k, (list, tuple)) or hasattr(k, 'tolist') for k in keys):
        return [('Series %d' % (i + 1), column(None, k)) for i, k in enumerate(keys)]
    return [('', keys)]


def chart(kind='line', data=None, x=None, y=None, labels=None, values=None, z=None, title='', height=360,
          colors=None, x_title=None, y_title=None, legend=True, stacked=False, size=None, text=None,
          min=None, max=None, layout=None, id=None, **trace):
    """A chart drawn with Plotly. kind: line, bar, barh, area, scatter, bubble, pie, donut,
    histogram, box, violin, heatmap, funnel, waterfall, radar, treemap, sunburst, gauge,
    indicator, candlestick. x/y/labels/values/z take column names of data or sequences; y may be
    a list of column names to draw several series."""
    data = _ir_data(data)
    kind = (kind or 'line').lower()
    palette = list(colors) if colors else _IR_PALETTE
    traces = []

    if kind in ('pie', 'donut', 'funnel', 'treemap', 'sunburst', 'funnelarea'):
        names = column(data, labels if labels is not None else x)
        amounts = column(data, values if values is not None else y)
        if kind in ('pie', 'donut'):
            t = {'type': 'pie', 'labels': names, 'values': amounts, 'marker': {'colors': palette}, 'sort': False}
            if kind == 'donut':
                t['hole'] = 0.5
        elif kind == 'funnel':
            t = {'type': 'funnel', 'y': names, 'x': amounts, 'marker': {'color': palette[0]}}
        else:
            t = {'type': kind, 'labels': names, 'values': amounts}
            parents = trace.pop('parents', None)
            t['parents'] = column(data, parents) if parents is not None else [''] * len(names or [])
        traces.append(t)
    elif kind in ('histogram',):
        for i, (name, series) in enumerate(_ir_series(data, x if x is not None else y)):
            traces.append({'type': 'histogram', 'x': series, 'name': name, 'marker': {'color': palette[i % len(palette)]}})
    elif kind in ('box', 'violin'):
        for i, (name, series) in enumerate(_ir_series(data, y if y is not None else x)):
            traces.append({'type': kind, 'y': series, 'name': name, 'marker': {'color': palette[i % len(palette)]}})
    elif kind == 'heatmap':
        matrix = z
        if isinstance(matrix, str):
            matrix = column(data, matrix)
        if matrix is None and data is not None:
            matrix = data.values.tolist() if hasattr(data, 'values') and hasattr(data, 'columns') else data
        t = {'type': 'heatmap', 'z': _ir_plain(matrix), 'colorscale': trace.pop('colorscale', 'RdYlGn')}
        if x is not None:
            t['x'] = column(data, x) if isinstance(x, str) else list(x)
        elif hasattr(data, 'columns'):
            t['x'] = [str(c) for c in data.columns]
        if y is not None:
            t['y'] = column(data, y) if isinstance(y, str) else list(y)
        traces.append(t)
    elif kind == 'radar':
        theta = column(data, labels if labels is not None else x)
        for i, (name, series) in enumerate(_ir_series(data, values if values is not None else y)):
            traces.append({'type': 'scatterpolar', 'r': series + series[:1], 'theta': theta + theta[:1], 'fill': 'toself',
                           'name': name, 'line': {'color': palette[i % len(palette)]}})
    elif kind in ('gauge', 'indicator'):
        amount = values if values is not None else y
        amount = column(data, amount)[-1] if isinstance(amount, str) else amount
        t = {'type': 'indicator', 'value': amount, 'title': {'text': title}}
        if kind == 'gauge':
            low = 0 if min is None else min
            high = 100 if max is None else max
            t['mode'] = 'gauge+number'
            t['gauge'] = {'axis': {'range': [low, high]}, 'bar': {'color': palette[0]}}
        else:
            t['mode'] = 'number'
        traces.append(t)
        title = ''
    elif kind == 'candlestick':
        t = {'type': 'candlestick', 'x': column(data, x)}
        for part in ('open', 'high', 'low', 'close'):
            t[part] = column(data, trace.pop(part, part))
        traces.append(t)
    elif kind == 'waterfall':
        traces.append({'type': 'waterfall', 'x': column(data, x), 'y': column(data, y)})
    else:
        xs = column(data, x)
        for i, (name, series) in enumerate(_ir_series(data, y)):
            color = palette[i % len(palette)]
            if kind in ('bar', 'barh', 'stacked_bar'):
                t = {'type': 'bar', 'name': name, 'marker': {'color': color}}
                if kind == 'barh':
                    t.update({'orientation': 'h', 'x': series, 'y': xs})
                else:
                    t.update({'x': xs, 'y': series})
            elif kind in ('scatter', 'bubble'):
                t = {'type': 'scatter', 'mode': 'markers', 'x': xs, 'y': series, 'name': name, 'marker': {'color': color}}
                if size is not None:
                    sizes = column(data, size)
                    # min and max are parameters here, so the builtin is reached by another name.
                    top = float(_ir_builtin_max(sizes) if sizes else 1.0) or 1.0
                    t['marker']['size'] = [6 + 40 * float(s) / top for s in sizes]
            else:
                t = {'type': 'scatter', 'mode': 'lines+markers' if kind == 'line' else 'lines', 'x': xs, 'y': series,
                     'name': name, 'line': {'color': color}}
                if kind == 'area':
                    t['fill'] = 'tonexty' if stacked and i else 'tozeroy'
                    if stacked:
                        t['stackgroup'] = 'one'
            if text is not None:
                t['text'] = column(data, text)
            traces.append(t)

    for t in traces:
        t.update(trace)
    spec_layout = {
        'title': {'text': title} if title else None,
        'height': height,
        'margin': {'l': 50, 'r': 20, 't': 50 if title else 20, 'b': 40},
        'showlegend': bool(legend) and len(traces) > 1 or (legend and kind in ('pie', 'donut')),
        'barmode': 'stack' if stacked or kind == 'stacked_bar' else 'group',
        'xaxis': {'title': {'text': x_title}} if x_title else {},
        'yaxis': {'title': {'text': y_title}} if y_title else {},
        'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)',
    }
    if layout:
        spec_layout.update(layout)
    return plotly({'data': traces, 'layout': {k: v for k, v in spec_layout.items() if v is not None}}, height=height, id=id)


def _ir_builtin_max(values):
    import builtins
    return builtins.max(values)


def plotly(figure, height=None, id=None, config=None):
    """Any Plotly figure: a plotly.graph_objects Figure or a {'data': [...], 'layout': {...}} dictionary."""
    spec = figure.to_plotly_json() if hasattr(figure, 'to_plotly_json') else dict(figure)
    spec.setdefault('layout', {})
    if height:
        spec['layout'].setdefault('height', height)
    spec['config'] = dict({'displaylogo': False, 'responsive': True}, **(config or {}))
    box_height = spec['layout'].get('height') or 360
    return Html('<div %s><script type="application/json">%s</script></div>' % (_ir_attrs(
        id=id or _ir_next_id('chart'), class_='cn-chart', data_cn_chart='1', data_cn_opaque='1',
        style='min-height:%dpx' % box_height), _ir_json_block(spec)))


def figure(fig, width=None, dpi=110):
    """A matplotlib figure, as a picture."""
    buffer = _ir_io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=dpi)
    try:
        import matplotlib.pyplot as plt
        plt.close(fig)
    except Exception:
        pass
    return image(buffer.getvalue(), width=width)


def image(source, width=None, alt=''):
    """A picture: bytes, a file path, or a URL."""
    if isinstance(source, (bytes, bytearray)):
        kind = 'jpeg' if bytes(source[:3]) == b'\xff\xd8\xff' else 'png'
        src = 'data:image/%s;base64,%s' % (kind, _ir_base64.b64encode(bytes(source)).decode('ascii'))
    elif isinstance(source, str) and _ir_os.path.isfile(source):
        extension = _ir_os.path.splitext(source)[1].lower().lstrip('.') or 'png'
        mime = {'jpg': 'jpeg', 'svg': 'svg+xml'}.get(extension, extension)
        with open(source, 'rb') as handle:
            src = 'data:image/%s;base64,%s' % (mime, _ir_base64.b64encode(handle.read()).decode('ascii'))
    else:
        src = str(source)
    style = 'width:%s' % (width if isinstance(width, str) else '%dpx' % width) if width else None
    return Html('<img %s/>' % _ir_attrs(class_='cn-image', src=src, alt=alt, style=style))


_IR_DEFAULT_SCALE = ['#d73027', '#fc8d59', '#fee08b', '#91cf60', '#1a9850']


def color_bar(value, min=0, max=100, colors=None, label=None, show_value=True, format=None, height=14, ticks=True):
    """A colour scale with a marker at the value — red to green by default."""
    scale = list(colors) if colors else _IR_DEFAULT_SCALE
    try:
        position = (float(value) - float(min)) / (float(max) - float(min)) * 100.0
    except (TypeError, ValueError, ZeroDivisionError):
        position = 0.0
    position = 0.0 if position != position else position
    position = 0.0 if position < 0 else 100.0 if position > 100 else position
    gradient = 'linear-gradient(to right, %s)' % ', '.join(scale)
    caption = '<div class="cn-label">%s%s</div>' % (
        esc(label or ''), (' <b>%s</b>' % esc(fmt(value, format) if format else _ir_number(float(value)) if isinstance(value, (int, float)) else value)) if show_value else '')
    marks = ('<div class="cn-colorbar-ticks"><span>%s</span><span>%s</span></div>' % (esc(min), esc(max))) if ticks else ''
    return Html('<div class="cn-colorbar cn-field">%s<div class="cn-colorbar-track" style="height:%dpx;background:%s">'
                '<div class="cn-colorbar-marker" style="left:%.2f%%"></div></div>%s</div>'
                % (caption, height, gradient, position, marks))


def progress(value, max=100, label=None, color=None, format=None):
    """A progress bar."""
    try:
        share = float(value) / float(max) * 100.0
    except (TypeError, ValueError, ZeroDivisionError):
        share = 0.0
    share = 0.0 if share < 0 else 100.0 if share > 100 else share
    style = 'width:%.2f%%%s' % (share, ';background:%s' % color if color else '')
    caption = '<div class="cn-label">%s <b>%s</b></div>' % (esc(label or ''), esc(fmt(value, format) if format else '%.0f%%' % share))
    return Html('<div class="cn-progress cn-field">%s<div class="cn-progress-track"><div class="cn-progress-fill" style="%s"></div></div></div>'
                % (caption, style))


def kpi(label, value, delta=None, format=None, delta_format=None, good='up', color=None):
    """A headline figure with an optional change beside it."""
    shown = fmt(value, format) if format else (_ir_number(value) if isinstance(value, float) else value)
    change = ''
    if delta is not None:
        try:
            positive = float(delta) >= 0
        except (TypeError, ValueError):
            positive = True
        tone = 'cn-good' if positive == (good == 'up') else 'cn-bad'
        arrow = '▲' if positive else '▼'
        change = '<div class="cn-kpi-delta %s">%s %s</div>' % (tone, arrow, esc(fmt(delta, delta_format) if delta_format else delta))
    style = ' style="border-top-color:%s"' % esc(color) if color else ''
    return Html('<div class="cn-kpi"%s><div class="cn-kpi-label">%s</div><div class="cn-kpi-value">%s</div>%s</div>'
                % (style, esc(label), esc(shown), change))


def badge(text, color='#3366cc'):
    """A small coloured label."""
    return Html('<span class="cn-badge" style="background:%s">%s</span>' % (esc(color), esc(text)))
