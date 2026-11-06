// CatNip interactive report — the browser half.
//
// The Python half renders the whole page to HTML on every change and sends it here; this script
// morphs the live DOM into the new HTML instead of replacing it, so the slider being dragged, the
// text box being typed in, the table's sort order and the chart's zoom all survive a re-render.
// Everything the user does on a control is sent back as one small JSON message, which CatNip
// writes to the Python process's stdin.
(function () {
    'use strict';

    var state = {
        id: null,
        interactive: true,
        ended: false,
        css: null,
        tables: {},     // per table element id: { sort, dir, filter, page, data, selected }
        charts: {},     // per chart element id: the spec text last drawn
        lastSent: {}    // per bound name: the value last sent, so input + change send it once
    };

    // ── To CatNip ──────────────────────────────────────────────────────────────

    function post(message) {
        if (!state.id || state.ended || !state.interactive) return;
        message.page = state.id;
        var body = JSON.stringify(message);
        if (typeof window.invokeCSharpAction === 'function') window.invokeCSharpAction(body);
        else if (window.chrome && window.chrome.webview) window.chrome.webview.postMessage(body);
        else if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.invokeCSharpAction)
            window.webkit.messageHandlers.invokeCSharpAction.postMessage(body);
    }

    // ── From CatNip ────────────────────────────────────────────────────────────

    function apply(message) {
        if (!message || !message.op) return;
        switch (message.op) {
            case 'render': render(message); break;
            case 'toast': toast(message.message, message.kind); break;
            case 'busy': busy(message.on, message.label); break;
            case 'waiting': waiting(message.action); break;
            case 'ended': ended(message.reason); break;
        }
    }

    function render(message) {
        state.id = message.id;
        state.interactive = message.interactive !== false;
        if (message.css !== state.css) {
            state.css = message.css;
            document.getElementById('cn-user-style').textContent = message.css || '';
        }
        var root = document.getElementById('cn-root');
        var next = document.createElement('main');
        next.innerHTML = message.html || '';
        morphChildren(root, next);
        hydrate(root);
        document.body.classList.toggle('cn-static', !state.interactive);
    }

    // ── Morphing ──────────────────────────────────────────────────────────────

    function sameNode(a, b) {
        if (a.nodeType !== b.nodeType) return false;
        if (a.nodeType !== 1) return true;
        if (a.tagName !== b.tagName) return false;
        if (a.id || b.id) return a.id === b.id;
        if (a.tagName === 'INPUT' && a.type !== b.getAttribute('type')) return false;
        return true;
    }

    function morphChildren(from, to) {
        var byId = {};
        for (var c = from.firstElementChild; c; c = c.nextElementSibling)
            if (c.id) byId[c.id] = c;

        var cursor = from.firstChild;
        var incoming = Array.prototype.slice.call(to.childNodes);
        for (var i = 0; i < incoming.length; i++) {
            var node = incoming[i];
            var match = null;
            if (node.nodeType === 1 && node.id && byId[node.id] && byId[node.id].parentNode === from) match = byId[node.id];
            else if (cursor && sameNode(cursor, node)) match = cursor;

            if (match) {
                if (match === cursor) cursor = cursor.nextSibling;
                else from.insertBefore(match, cursor);
                morphNode(match, node);
            } else {
                from.insertBefore(node, cursor);
            }
        }
        while (cursor) {
            var next = cursor.nextSibling;
            from.removeChild(cursor);
            cursor = next;
        }
    }

    function morphNode(a, b) {
        if (a.nodeType !== 1) {
            if (a.nodeValue !== b.nodeValue) a.nodeValue = b.nodeValue;
            return;
        }
        var i, attr;
        for (i = a.attributes.length - 1; i >= 0; i--) {
            attr = a.attributes[i].name;
            if (!b.hasAttribute(attr)) a.removeAttribute(attr);
        }
        for (i = 0; i < b.attributes.length; i++) {
            attr = b.attributes[i];
            if (a.getAttribute(attr.name) !== attr.value) a.setAttribute(attr.name, attr.value);
        }

        // A chart or a table owns what is inside it: only the data block is compared, and the
        // element is redrawn by hydrate() when that changed.
        if (a.hasAttribute('data-cn-opaque')) {
            var oldData = a.querySelector(':scope > script[type="application/json"]');
            var newData = b.querySelector(':scope > script[type="application/json"]');
            if (newData && (!oldData || oldData.textContent !== newData.textContent)) {
                if (oldData) oldData.textContent = newData.textContent;
                else a.insertBefore(newData, a.firstChild);
            }
            return;
        }

        if (a.tagName === 'TEXTAREA') {
            if (document.activeElement !== a) a.value = b.textContent;
            return;
        }
        morphChildren(a, b);

        if (a.tagName === 'INPUT') {
            var focused = document.activeElement === a;
            if (a.type === 'checkbox' || a.type === 'radio') a.checked = b.hasAttribute('checked');
            else if (!focused || a.type === 'range') {
                var v = b.getAttribute('value');
                if (v !== null && a.value !== v && !(a.type === 'range' && dragging === a)) a.value = v;
            }
        } else if (a.tagName === 'SELECT') {
            for (i = 0; i < a.options.length; i++) a.options[i].selected = a.options[i].hasAttribute('selected');
        }
    }

    // ── Charts and tables ─────────────────────────────────────────────────────

    function dataOf(element) {
        var block = element.querySelector(':scope > script[type="application/json"]');
        return block ? block.textContent : null;
    }

    function hydrate(root) {
        var seenCharts = {}, seenTables = {};
        root.querySelectorAll('[data-cn-chart]').forEach(function (element) {
            seenCharts[element.id] = true;
            var text = dataOf(element);
            if (!text || state.charts[element.id] === text) return;
            state.charts[element.id] = text;
            drawChart(element, text);
        });
        root.querySelectorAll('[data-cn-table]').forEach(function (element) {
            seenTables[element.id] = true;
            var text = dataOf(element);
            var t = state.tables[element.id] || (state.tables[element.id] = { sort: -1, dir: 1, filter: '', page: 0, text: null });
            if (t.text !== text || !element.querySelector('.cn-table-body')) {
                t.text = text;
                try { t.data = JSON.parse(text); } catch (e) { t.data = { columns: [], rows: [] }; }
                drawTable(element, t);
            }
        });
        Object.keys(state.charts).forEach(function (id) { if (!seenCharts[id]) delete state.charts[id]; });
        Object.keys(state.tables).forEach(function (id) { if (!seenTables[id]) delete state.tables[id]; });
    }

    function drawChart(element, text) {
        var target = element.querySelector(':scope > .cn-chart-plot');
        if (!target) {
            target = document.createElement('div');
            target.className = 'cn-chart-plot';
            element.appendChild(target);
        }
        if (typeof window.Plotly === 'undefined') {
            target.textContent = 'The chart library did not load.';
            return;
        }
        try {
            var spec = JSON.parse(text);
            window.Plotly.react(target, spec.data || [], spec.layout || {}, spec.config || {});
        } catch (e) {
            target.textContent = 'The chart could not be drawn: ' + e.message;
        }
    }

    function cellText(value, format) {
        if (value === null || value === undefined) return '';
        if (typeof value === 'number' && format) {
            var m = /^,?\.(\d+)([f%])$/.exec(format.replace(/^,/, ',').trim());
            if (m) {
                var digits = parseInt(m[1], 10);
                var shown = m[2] === '%' ? value * 100 : value;
                var s = shown.toLocaleString(undefined, { minimumFractionDigits: digits, maximumFractionDigits: digits, useGrouping: format.charAt(0) === ',' });
                return m[2] === '%' ? s + '%' : s;
            }
        }
        if (typeof value === 'boolean') return value ? 'Yes' : 'No';
        return String(value);
    }

    function compare(a, b) {
        if (a === b) return 0;
        if (a === null || a === undefined) return 1;
        if (b === null || b === undefined) return -1;
        if (typeof a === 'number' && typeof b === 'number') return a - b;
        return String(a).localeCompare(String(b), undefined, { numeric: true });
    }

    function drawTable(element, t) {
        var d = t.data, cols = d.columns || [], rows = d.rows || [], formats = d.formats || {};
        var pageSize = d.pageSize > 0 ? d.pageSize : rows.length || 1;

        var visible = rows.map(function (r, i) { return i; });
        if (t.filter) {
            var needle = t.filter.toLowerCase();
            visible = visible.filter(function (i) {
                return rows[i].some(function (v) { return v !== null && String(v).toLowerCase().indexOf(needle) >= 0; });
            });
        }
        if (t.sort >= 0) {
            visible.sort(function (x, y) { return t.dir * compare(rows[x][t.sort], rows[y][t.sort]); });
        }
        var pages = Math.max(1, Math.ceil(visible.length / pageSize));
        if (t.page >= pages) t.page = pages - 1;
        var shown = visible.slice(t.page * pageSize, (t.page + 1) * pageSize);

        var html = [];
        if (d.filter !== false) {
            html.push('<div class="cn-table-tools"><input type="search" class="cn-input cn-table-filter" placeholder="Filter…" value="' +
                      escapeAttr(t.filter) + '"></div>');
        }
        html.push('<div class="cn-table-scroll"><table class="cn-table-body"><thead><tr>');
        cols.forEach(function (c, i) {
            var mark = t.sort === i ? (t.dir > 0 ? ' ▲' : ' ▼') : '';
            html.push('<th data-cn-col="' + i + '"' + (d.sortable === false ? '' : ' class="cn-sortable"') + '>' + escapeHtml(c) + mark + '</th>');
        });
        html.push('</tr></thead><tbody>');
        shown.forEach(function (index) {
            var row = rows[index];
            html.push('<tr data-cn-row="' + index + '"' + (t.selected === index ? ' class="cn-selected"' : '') + '>');
            cols.forEach(function (c, i) {
                var v = row[i];
                html.push('<td' + (typeof v === 'number' ? ' class="cn-num"' : '') + '>' + escapeHtml(cellText(v, formats[c])) + '</td>');
            });
            html.push('</tr>');
        });
        html.push('</tbody></table></div>');
        var total = d.total > rows.length ? ' (first ' + rows.length + ' of ' + d.total + ')' : '';
        html.push('<div class="cn-table-pager"><span>' + visible.length + ' rows' + total + '</span>');
        if (pages > 1) {
            html.push('<button type="button" class="cn-button cn-secondary" data-cn-page="-1"' + (t.page === 0 ? ' disabled' : '') + '>‹</button>' +
                      '<span>' + (t.page + 1) + ' / ' + pages + '</span>' +
                      '<button type="button" class="cn-button cn-secondary" data-cn-page="1"' + (t.page >= pages - 1 ? ' disabled' : '') + '>›</button>');
        }
        html.push('</div>');

        // Replace everything but the data block.
        var keep = element.querySelector(':scope > script[type="application/json"]');
        var focusFilter = document.activeElement && document.activeElement.classList.contains('cn-table-filter') &&
                          element.contains(document.activeElement);
        var caret = focusFilter ? document.activeElement.selectionStart : 0;
        Array.prototype.slice.call(element.childNodes).forEach(function (n) { if (n !== keep) element.removeChild(n); });
        var holder = document.createElement('div');
        holder.innerHTML = html.join('');
        while (holder.firstChild) element.appendChild(holder.firstChild);
        if (focusFilter) {
            var f = element.querySelector('.cn-table-filter');
            f.focus();
            f.setSelectionRange(caret, caret);
        }
    }

    function tableEvents(event) {
        var element = event.target.closest('[data-cn-table]');
        if (!element) return false;
        var t = state.tables[element.id];
        if (!t) return false;

        if (event.type === 'input' && event.target.classList.contains('cn-table-filter')) {
            t.filter = event.target.value;
            t.page = 0;
            drawTable(element, t);
            return true;
        }
        if (event.type !== 'click') return false;

        var header = event.target.closest('th[data-cn-col]');
        if (header && t.data.sortable !== false) {
            var col = parseInt(header.getAttribute('data-cn-col'), 10);
            if (t.sort === col) t.dir = -t.dir; else { t.sort = col; t.dir = 1; }
            drawTable(element, t);
            return true;
        }
        var pager = event.target.closest('[data-cn-page]');
        if (pager) {
            t.page += parseInt(pager.getAttribute('data-cn-page'), 10);
            drawTable(element, t);
            return true;
        }
        var row = event.target.closest('tr[data-cn-row]');
        if (row && t.data.select) {
            var index = parseInt(row.getAttribute('data-cn-row'), 10);
            t.selected = index;
            var value = {};
            t.data.columns.forEach(function (c, i) { value[c] = t.data.rows[index][i]; });
            drawTable(element, t);
            post({ op: 'change', name: t.data.select, value: value });
            return true;
        }
        return false;
    }

    // ── Controls ──────────────────────────────────────────────────────────────

    function typed(text, type) {
        if (type === 'number') { var f = parseFloat(text); return isNaN(f) ? null : f; }
        if (type === 'int') { var n = parseInt(text, 10); return isNaN(n) ? null : n; }
        if (type === 'bool') return text === true || text === 'true' || text === 'True';
        return text;
    }

    function valueOf(element) {
        var type = element.getAttribute('data-cn-type') || 'text';
        if (element.classList.contains('cn-radio')) {
            var checked = element.querySelector('input:checked');
            return checked ? typed(checked.value, type) : null;
        }
        if (type.indexOf('multi:') === 0) {
            var inner = type.substring(6);
            return Array.prototype.filter.call(element.options, function (o) { return o.selected; })
                .map(function (o) { return typed(o.value, inner); });
        }
        if (element.type === 'checkbox') return element.checked;
        return typed(element.value, type);
    }

    function sendChange(element, force) {
        var name = element.getAttribute('data-cn-bind');
        var value = valueOf(element);
        var key = JSON.stringify(value);
        if (!force && state.lastSent[name] === key) return;
        state.lastSent[name] = key;
        post({ op: 'change', name: name, value: value });
    }

    function showSliderValue(slider) {
        var output = slider.parentNode.querySelector('.cn-slider-value');
        if (output) output.textContent = slider.value;
    }

    var dragging = null, liveTimer = null;

    document.addEventListener('pointerdown', function (e) { if (e.target.classList && e.target.classList.contains('cn-slider')) dragging = e.target; }, true);
    document.addEventListener('pointerup', function () { dragging = null; }, true);

    document.addEventListener('input', function (event) {
        if (tableEvents(event)) return;
        var element = event.target.closest('[data-cn-bind]');
        if (!element) return;
        if (event.target.type === 'range') showSliderValue(event.target);
        if (element.hasAttribute('data-cn-live')) {
            clearTimeout(liveTimer);
            liveTimer = setTimeout(function () { sendChange(element); }, 60);
        } else if (element.tagName === 'SELECT' || element.classList.contains('cn-radio') ||
                   event.target.type === 'checkbox' || event.target.type === 'color' || event.target.type === 'date') {
            sendChange(element);
        }
    });

    document.addEventListener('change', function (event) {
        var element = event.target.closest('[data-cn-bind]');
        if (element) sendChange(element);
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && event.target.matches && event.target.matches('input[data-cn-bind]')) sendChange(event.target);
    });

    document.addEventListener('click', function (event) {
        if (tableEvents(event)) return;
        var button = event.target.closest('[data-cn-action],[data-cn-call]');
        if (!button || button.disabled) return;
        var confirmText = button.getAttribute('data-cn-confirm');
        if (confirmText && !window.confirm(confirmText)) return;
        // A text box being edited still holds its value; send it before the click it belongs to.
        var active = document.activeElement;
        if (active && active.hasAttribute && active.hasAttribute('data-cn-bind')) sendChange(active);
        if (button.hasAttribute('data-cn-action')) post({ op: 'action', name: button.getAttribute('data-cn-action') });
        else post({ op: 'call', name: button.getAttribute('data-cn-call') });
    });

    // Links never navigate the report away; CatNip opens http(s) links in the browser.
    document.addEventListener('click', function (event) {
        var link = event.target.closest('a[href]');
        if (!link) return;
        var href = link.getAttribute('href');
        if (href && href.charAt(0) === '#') return;
        event.preventDefault();
        if (/^https?:/i.test(href)) post({ op: 'open-link', url: href });
    }, true);

    // ── Status ────────────────────────────────────────────────────────────────

    function status(text, kind) {
        var bar = document.getElementById('cn-status');
        if (!text) { bar.hidden = true; return; }
        bar.hidden = false;
        bar.className = 'cn-status cn-' + (kind || 'info');
        bar.textContent = text;
    }

    function busy(on, label) {
        document.body.classList.toggle('cn-busy', !!on);
        status(on ? 'Running “' + (label || 'action') + '”…' : null, 'info');
    }

    function waiting(action) {
        document.querySelectorAll('[data-cn-action]').forEach(function (b) {
            b.classList.toggle('cn-awaited', !!action && b.getAttribute('data-cn-action') === action);
        });
        status(action ? 'The flow is waiting for “' + action + '”.' : null, 'warning');
    }

    function ended(reason) {
        state.ended = true;
        document.body.classList.add('cn-ended');
        status(reason || 'The run has ended — the page no longer answers.', 'muted');
    }

    function toast(text, kind) {
        var box = document.getElementById('cn-toasts');
        var item = document.createElement('div');
        item.className = 'cn-toast cn-' + (kind || 'info');
        item.textContent = text;
        box.appendChild(item);
        setTimeout(function () { item.classList.add('cn-leaving'); }, kind === 'error' ? 7000 : 3500);
        setTimeout(function () { if (item.parentNode) item.parentNode.removeChild(item); }, kind === 'error' ? 7600 : 4100);
    }

    function escapeHtml(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function escapeAttr(s) {
        return escapeHtml(s || '').replace(/"/g, '&quot;');
    }

    window.catnip = { apply: apply };
})();
