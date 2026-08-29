/* @ds-bundle: {"format":4,"namespace":"KarukaDesignSystem_69ceb9","components":[{"name":"Badge","sourcePath":"components/display/Badge.jsx"},{"name":"Callout","sourcePath":"components/display/Callout.jsx"},{"name":"Card","sourcePath":"components/display/Card.jsx"},{"name":"CodeBlock","sourcePath":"components/display/CodeBlock.jsx"},{"name":"InlineCode","sourcePath":"components/display/CodeBlock.jsx"},{"name":"DataTable","sourcePath":"components/display/DataTable.jsx"},{"name":"MetricStat","sourcePath":"components/display/MetricStat.jsx"},{"name":"Button","sourcePath":"components/forms/Button.jsx"},{"name":"Checkbox","sourcePath":"components/forms/Checkbox.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Radio","sourcePath":"components/forms/Radio.jsx"},{"name":"Select","sourcePath":"components/forms/Select.jsx"},{"name":"Switch","sourcePath":"components/forms/Switch.jsx"},{"name":"Tabs","sourcePath":"components/navigation/Tabs.jsx"}],"sourceHashes":{"components/display/Badge.jsx":"4feba5b798a1","components/display/Callout.jsx":"b24be26d1e54","components/display/Card.jsx":"78afd191f216","components/display/CodeBlock.jsx":"cf55a769653a","components/display/DataTable.jsx":"d9d27c7b327a","components/display/MetricStat.jsx":"c623430a5020","components/forms/Button.jsx":"8c58d175c156","components/forms/Checkbox.jsx":"fa876e6b70e5","components/forms/Input.jsx":"0869315a3d6a","components/forms/Radio.jsx":"67b046b86850","components/forms/Select.jsx":"dfff0f6aecb5","components/forms/Switch.jsx":"27bb1dfcab98","components/navigation/Tabs.jsx":"e14c368c3598","ui_kits/eval-console/app.jsx":"675f4ec2e087","ui_kits/eval-console/live.jsx":"4a51e312adb1","ui_kits/eval-console/report.jsx":"b1ace2088a51","ui_kits/eval-console/runs.jsx":"61583e24a1e2","ui_kits/eval-console/shell.jsx":"c6674a7e3686"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.KarukaDesignSystem_69ceb9 = window.KarukaDesignSystem_69ceb9 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/display/Badge.jsx
try { (() => {
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-badge')) {
    const s = document.createElement('style');
    s.id = 'krk-badge';
    s.textContent = `.krk-badge{display:inline-flex;align-items:center;gap:5px;height:20px;padding:0 9px;border-radius:999px;font-family:var(--font-sans);font-size:12px;font-weight:600;letter-spacing:.01em}
.krk-badge-dot{width:6px;height:6px;border-radius:50%;background:currentColor}
.krk-badge-neutral{background:var(--surface-inline-code);color:var(--gray-600)}
.krk-badge-info{background:var(--surface-info);color:var(--blue)}
.krk-badge-success{background:var(--success-bg);color:var(--success-text)}
.krk-badge-warning{background:var(--warning-bg);color:var(--warning-text)}
.krk-badge-danger{background:var(--danger-bg);color:var(--danger-text)}
.krk-badge-mono{font-family:var(--font-mono);font-weight:400}`;
    document.head.appendChild(s);
  }
})();
function Badge({
  tone = 'neutral',
  dot,
  mono,
  children
}) {
  return /*#__PURE__*/React.createElement("span", {
    className: 'krk-badge krk-badge-' + tone + (mono ? ' krk-badge-mono' : '')
  }, dot && /*#__PURE__*/React.createElement("span", {
    className: "krk-badge-dot"
  }), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Badge.jsx", error: String((e && e.message) || e) }); }

// components/display/Callout.jsx
try { (() => {
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-callout')) {
    const s = document.createElement('style');
    s.id = 'krk-callout';
    s.textContent = `.krk-callout{font-family:var(--font-sans);border-left:4px solid;border-radius:0 6px 6px 0;padding:16px 20px;font-size:14px;line-height:1.5;color:var(--ink)}
.krk-callout-title{font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.5em}
.krk-callout-info{border-color:var(--blue);background:var(--surface-info)}.krk-callout-info .krk-callout-title{color:var(--blue)}
.krk-callout-warning{border-color:var(--warning);background:var(--warning-bg)}.krk-callout-warning .krk-callout-title{color:var(--warning-text)}
.krk-callout-tip{border-color:var(--success);background:var(--success-bg)}.krk-callout-tip .krk-callout-title{color:var(--success-text)}
.krk-callout-danger{border-color:var(--danger);background:var(--danger-bg)}.krk-callout-danger .krk-callout-title{color:var(--danger-text)}`;
    document.head.appendChild(s);
  }
})();
function Callout({
  kind = 'info',
  title,
  children,
  style
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: 'krk-callout krk-callout-' + kind,
    style: style
  }, title && /*#__PURE__*/React.createElement("div", {
    className: "krk-callout-title"
  }, title), children);
}
Object.assign(__ds_scope, { Callout });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Callout.jsx", error: String((e && e.message) || e) }); }

// components/display/Card.jsx
try { (() => {
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-card')) {
    const s = document.createElement('style');
    s.id = 'krk-card';
    s.textContent = `.krk-card{font-family:var(--font-sans);background:#fff;border:1px solid var(--border-default);border-radius:var(--radius-md);color:var(--ink)}
.krk-card-head{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 16px;border-bottom:1px solid var(--border-default)}
.krk-card-title{font-size:15px;font-weight:600;letter-spacing:-.01em}
.krk-card-body{padding:16px}`;
    document.head.appendChild(s);
  }
})();
function Card({
  title,
  actions,
  children,
  style
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "krk-card",
    style: style
  }, (title || actions) && /*#__PURE__*/React.createElement("div", {
    className: "krk-card-head"
  }, /*#__PURE__*/React.createElement("span", {
    className: "krk-card-title"
  }, title), actions), /*#__PURE__*/React.createElement("div", {
    className: "krk-card-body"
  }, children));
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/Card.jsx", error: String((e && e.message) || e) }); }

// components/display/CodeBlock.jsx
try { (() => {
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-code')) {
    const s = document.createElement('style');
    s.id = 'krk-code';
    s.textContent = `.krk-code{background:var(--surface-code);border:1px solid var(--border-strong);border-radius:var(--radius-md);padding:16px;margin:0;overflow-x:auto}
.krk-code-lang{display:block;text-align:right;font-family:var(--font-sans);font-size:11px;color:#656D76;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid var(--border-strong)}
.krk-code code{font-family:var(--font-mono);font-size:13px;line-height:1.4;color:var(--ink);white-space:pre-wrap;word-wrap:break-word}
.krk-code-inline{font-family:var(--font-mono);background:var(--surface-inline-code);padding:.15em .35em;border-radius:4px;font-size:.9em}`;
    document.head.appendChild(s);
  }
})();
function CodeBlock({
  language,
  children,
  style
}) {
  return /*#__PURE__*/React.createElement("pre", {
    className: "krk-code",
    style: style
  }, language && /*#__PURE__*/React.createElement("span", {
    className: "krk-code-lang"
  }, language), /*#__PURE__*/React.createElement("code", null, children));
}
function InlineCode({
  children
}) {
  return /*#__PURE__*/React.createElement("code", {
    className: "krk-code-inline"
  }, children);
}
Object.assign(__ds_scope, { CodeBlock, InlineCode });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/CodeBlock.jsx", error: String((e && e.message) || e) }); }

// components/display/DataTable.jsx
try { (() => {
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-table')) {
    const s = document.createElement('style');
    s.id = 'krk-table';
    s.textContent = `.krk-table{width:100%;border-collapse:collapse;font-family:var(--font-sans);font-size:13px;color:var(--ink)}
.krk-table thead{background:var(--surface-thead)}
.krk-table th{font-weight:600;text-align:left;padding:10px 12px;border-bottom:2px solid #334155;font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--gray-600)}
.krk-table td{padding:8px 12px;border-bottom:1px solid var(--border-default);vertical-align:top}
.krk-table tbody tr:nth-child(even){background:var(--surface-zebra)}
.krk-table td.krk-td-mono{font-family:var(--font-mono);font-size:12.5px}
.krk-table td.krk-td-num{font-family:var(--font-mono);font-size:12.5px;text-align:right}
.krk-table th.krk-td-num{text-align:right}`;
    document.head.appendChild(s);
  }
})();
function DataTable({
  columns = [],
  rows = [],
  style
}) {
  return /*#__PURE__*/React.createElement("table", {
    className: "krk-table",
    style: style
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, columns.map((c, i) => /*#__PURE__*/React.createElement("th", {
    key: i,
    className: c.align === 'right' ? 'krk-td-num' : ''
  }, c.label)))), /*#__PURE__*/React.createElement("tbody", null, rows.map((r, ri) => /*#__PURE__*/React.createElement("tr", {
    key: ri
  }, columns.map((c, ci) => /*#__PURE__*/React.createElement("td", {
    key: ci,
    className: c.mono ? 'krk-td-mono' : c.align === 'right' ? 'krk-td-num' : ''
  }, r[c.key]))))));
}
Object.assign(__ds_scope, { DataTable });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/DataTable.jsx", error: String((e && e.message) || e) }); }

// components/display/MetricStat.jsx
try { (() => {
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-stat')) {
    const s = document.createElement('style');
    s.id = 'krk-stat';
    s.textContent = `.krk-stat{font-family:var(--font-sans);display:flex;flex-direction:column;gap:4px;min-width:110px}
.krk-stat-label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:var(--gray-500)}
.krk-stat-value{font-family:var(--font-mono);font-size:24px;line-height:1.1;color:var(--ink)}
.krk-stat-unit{font-size:13px;color:var(--gray-500);margin-left:2px}
.krk-stat-delta{font-family:var(--font-mono);font-size:12px;font-weight:400}
.krk-stat-delta-up{color:var(--success-text)}.krk-stat-delta-down{color:var(--danger-text)}.krk-stat-delta-flat{color:var(--gray-500)}`;
    document.head.appendChild(s);
  }
})();
function MetricStat({
  label,
  value,
  unit,
  delta,
  deltaTone = 'flat',
  style
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "krk-stat",
    style: style
  }, /*#__PURE__*/React.createElement("span", {
    className: "krk-stat-label"
  }, label), /*#__PURE__*/React.createElement("span", {
    className: "krk-stat-value"
  }, value, unit && /*#__PURE__*/React.createElement("span", {
    className: "krk-stat-unit"
  }, unit)), delta != null && /*#__PURE__*/React.createElement("span", {
    className: 'krk-stat-delta krk-stat-delta-' + deltaTone
  }, delta));
}
Object.assign(__ds_scope, { MetricStat });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/display/MetricStat.jsx", error: String((e && e.message) || e) }); }

// components/forms/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-btn')) {
    const s = document.createElement('style');
    s.id = 'krk-btn';
    s.textContent = `.krk-btn{font-family:var(--font-sans);font-weight:600;letter-spacing:.01em;border-radius:var(--radius-md);border:1px solid transparent;cursor:pointer;display:inline-flex;align-items:center;gap:8px;transition:background .14s ease-out,color .14s ease-out,border-color .14s ease-out;white-space:nowrap}
.krk-btn:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.krk-btn:disabled{opacity:.45;cursor:not-allowed}
.krk-btn-sm{height:28px;padding:0 10px;font-size:13px}.krk-btn-md{height:36px;padding:0 14px;font-size:14px}.krk-btn-lg{height:44px;padding:0 18px;font-size:15px}
.krk-btn-primary{background:var(--blue);color:#fff}.krk-btn-primary:hover:not(:disabled){background:var(--blue-hover)}
.krk-btn-secondary{background:#fff;color:var(--ink);border-color:var(--border-strong)}.krk-btn-secondary:hover:not(:disabled){background:var(--surface-code)}
.krk-btn-ghost{background:transparent;color:var(--blue)}.krk-btn-ghost:hover:not(:disabled){background:var(--surface-info)}
.krk-btn-danger{background:var(--danger-text);color:#fff}.krk-btn-danger:hover:not(:disabled){background:#B91C1C}`;
    document.head.appendChild(s);
  }
})();
function Button({
  variant = 'primary',
  size = 'md',
  icon,
  children,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("button", _extends({
    className: 'krk-btn krk-btn-' + size + ' krk-btn-' + variant
  }, rest), icon, children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Button.jsx", error: String((e && e.message) || e) }); }

// components/forms/Checkbox.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-check')) {
    const s = document.createElement('style');
    s.id = 'krk-check';
    s.textContent = `.krk-check{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-sans);font-size:14px;color:var(--ink);cursor:pointer}
.krk-check input{appearance:none;width:14px;height:14px;margin:0;border:2px solid var(--border-strong);border-radius:3px;position:relative;cursor:pointer;transition:background .12s ease-out,border-color .12s ease-out}
.krk-check input:checked{background:var(--blue);border-color:var(--blue)}
.krk-check input:checked::after{content:'\\2713';color:#fff;font-size:10px;position:absolute;top:-2px;left:1px}
.krk-check input:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.krk-check input:disabled{opacity:.45}`;
    document.head.appendChild(s);
  }
})();
function Checkbox({
  label,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("label", {
    className: "krk-check"
  }, /*#__PURE__*/React.createElement("input", _extends({
    type: "checkbox"
  }, rest)), label);
}
Object.assign(__ds_scope, { Checkbox });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Checkbox.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-input')) {
    const s = document.createElement('style');
    s.id = 'krk-input';
    s.textContent = `.krk-field{font-family:var(--font-sans);display:flex;flex-direction:column;gap:6px}
.krk-field-label{font-size:13px;font-weight:600;color:var(--ink)}
.krk-input{height:36px;padding:0 12px;font-size:14px;font-family:var(--font-sans);color:var(--ink);background:#fff;border:1px solid var(--border-strong);border-radius:var(--radius-md);transition:border-color .14s ease-out}
.krk-input::placeholder{color:var(--gray-400)}
.krk-input:hover{border-color:var(--gray-400)}
.krk-input:focus{outline:2px solid var(--blue);outline-offset:1px;border-color:var(--blue)}
.krk-input:disabled{opacity:.45;background:var(--surface-code)}
.krk-input-mono{font-family:var(--font-mono);font-size:13px}
.krk-input-error{border-color:var(--danger)}
.krk-field-hint{font-size:12px;color:var(--gray-500)}
.krk-field-hint-error{color:var(--danger-text)}`;
    document.head.appendChild(s);
  }
})();
function Input({
  label,
  hint,
  error,
  mono,
  style,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("label", {
    className: "krk-field",
    style: style
  }, label && /*#__PURE__*/React.createElement("span", {
    className: "krk-field-label"
  }, label), /*#__PURE__*/React.createElement("input", _extends({
    className: 'krk-input' + (mono ? ' krk-input-mono' : '') + (error ? ' krk-input-error' : '')
  }, rest)), (error || hint) && /*#__PURE__*/React.createElement("span", {
    className: 'krk-field-hint' + (error ? ' krk-field-hint-error' : '')
  }, error || hint));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/forms/Radio.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-radio')) {
    const s = document.createElement('style');
    s.id = 'krk-radio';
    s.textContent = `.krk-radio{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-sans);font-size:14px;color:var(--ink);cursor:pointer}
.krk-radio input{appearance:none;width:14px;height:14px;margin:0;border:2px solid var(--border-strong);border-radius:50%;position:relative;cursor:pointer;transition:border-color .12s ease-out}
.krk-radio input:checked{border-color:var(--blue)}
.krk-radio input:checked::after{content:'';position:absolute;inset:1px;border-radius:50%;background:var(--blue)}
.krk-radio input:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.krk-radio input:disabled{opacity:.45}`;
    document.head.appendChild(s);
  }
})();
function Radio({
  label,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("label", {
    className: "krk-radio"
  }, /*#__PURE__*/React.createElement("input", _extends({
    type: "radio"
  }, rest)), label);
}
Object.assign(__ds_scope, { Radio });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Radio.jsx", error: String((e && e.message) || e) }); }

// components/forms/Select.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-select')) {
    const s = document.createElement('style');
    s.id = 'krk-select';
    s.textContent = `.krk-select{height:36px;padding:0 32px 0 12px;font-size:14px;font-family:var(--font-sans);color:var(--ink);background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23616B73' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E") no-repeat right 10px center;border:1px solid var(--border-strong);border-radius:var(--radius-md);appearance:none;cursor:pointer}
.krk-select:hover{border-color:var(--gray-400)}
.krk-select:focus{outline:2px solid var(--blue);outline-offset:1px}
.krk-select:disabled{opacity:.45}`;
    document.head.appendChild(s);
  }
})();
function Select({
  label,
  hint,
  options = [],
  style,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("label", {
    className: "krk-field",
    style: style
  }, label && /*#__PURE__*/React.createElement("span", {
    className: "krk-field-label"
  }, label), /*#__PURE__*/React.createElement("select", _extends({
    className: "krk-select"
  }, rest), options.map(o => {
    const v = typeof o === 'string' ? {
      value: o,
      label: o
    } : o;
    return /*#__PURE__*/React.createElement("option", {
      key: v.value,
      value: v.value
    }, v.label);
  })), hint && /*#__PURE__*/React.createElement("span", {
    className: "krk-field-hint"
  }, hint));
}
Object.assign(__ds_scope, { Select });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Select.jsx", error: String((e && e.message) || e) }); }

// components/forms/Switch.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-switch')) {
    const s = document.createElement('style');
    s.id = 'krk-switch';
    s.textContent = `.krk-switch{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-sans);font-size:14px;color:var(--ink);cursor:pointer}
.krk-switch input{appearance:none;width:32px;height:18px;margin:0;border-radius:999px;background:var(--border-strong);position:relative;cursor:pointer;transition:background .14s ease-out}
.krk-switch input::after{content:'';position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;background:#fff;transition:left .14s ease-out}
.krk-switch input:checked{background:var(--blue)}
.krk-switch input:checked::after{left:16px}
.krk-switch input:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.krk-switch input:disabled{opacity:.45}`;
    document.head.appendChild(s);
  }
})();
function Switch({
  label,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("label", {
    className: "krk-switch"
  }, /*#__PURE__*/React.createElement("input", _extends({
    type: "checkbox",
    role: "switch"
  }, rest)), label);
}
Object.assign(__ds_scope, { Switch });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Switch.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Tabs.jsx
try { (() => {
(function () {
  if (typeof document !== 'undefined' && !document.getElementById('krk-tabs')) {
    const s = document.createElement('style');
    s.id = 'krk-tabs';
    s.textContent = `.krk-tabs{display:flex;gap:4px;border-bottom:1px solid var(--border-default);font-family:var(--font-sans)}
.krk-tab{appearance:none;background:none;border:none;border-bottom:2px solid transparent;margin-bottom:-1px;padding:9px 14px;font-size:14px;font-weight:600;font-family:var(--font-sans);color:var(--gray-500);cursor:pointer;transition:color .14s ease-out}
.krk-tab:hover{color:var(--ink)}
.krk-tab[aria-selected="true"]{color:var(--blue);border-bottom-color:var(--blue)}
.krk-tab:focus-visible{outline:2px solid var(--blue);outline-offset:-2px}
.krk-tab-count{font-family:var(--font-mono);font-weight:400;font-size:12px;color:var(--gray-400);margin-left:6px}`;
    document.head.appendChild(s);
  }
})();
function Tabs({
  tabs = [],
  active,
  onChange
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "krk-tabs",
    role: "tablist"
  }, tabs.map(t => {
    const v = typeof t === 'string' ? {
      id: t,
      label: t
    } : t;
    return /*#__PURE__*/React.createElement("button", {
      key: v.id,
      role: "tab",
      "aria-selected": active === v.id,
      className: "krk-tab",
      onClick: () => onChange && onChange(v.id)
    }, v.label, v.count != null && /*#__PURE__*/React.createElement("span", {
      className: "krk-tab-count"
    }, v.count));
  }));
}
Object.assign(__ds_scope, { Tabs });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Tabs.jsx", error: String((e && e.message) || e) }); }

// ui_kits/eval-console/app.jsx
try { (() => {
function App() {
  const [screen, setScreen] = React.useState('runs');
  const [command, setCommand] = React.useState('rm');
  const [runs, setRuns] = React.useState([{
    run: '1942-07',
    cmd: 'rm',
    cond: 'naive-LLM (plain)',
    status: /*#__PURE__*/React.createElement(window.KarukaDesignSystem_69ceb9.Badge, {
      tone: "success",
      dot: true
    }, "Completed"),
    q2: '94.1%',
    cost: '$0.038',
    wall: '12.4s'
  }, {
    run: '1942-06',
    cmd: 'rm',
    cond: 'v1 baseline',
    status: /*#__PURE__*/React.createElement(window.KarukaDesignSystem_69ceb9.Badge, {
      tone: "success",
      dot: true
    }, "Completed"),
    q2: '91.2%',
    cost: '$0.013',
    wall: '14.9s'
  }, {
    run: '1938-02',
    cmd: 'chmod',
    cond: 'naive-LLM (augmented)',
    status: /*#__PURE__*/React.createElement(window.KarukaDesignSystem_69ceb9.Badge, {
      tone: "success",
      dot: true
    }, "Completed"),
    q2: '92.3%',
    cost: '$0.067',
    wall: '21.0s'
  }, {
    run: '1938-01',
    cmd: 'chmod',
    cond: 'naive-LLM (plain)',
    status: /*#__PURE__*/React.createElement(window.KarukaDesignSystem_69ceb9.Badge, {
      tone: "warning",
      dot: true
    }, "Queued"),
    q2: '—',
    cost: '—',
    wall: '—'
  }, {
    run: '1921-04',
    cmd: 'ln',
    cond: 'naive-LLM (plain)',
    status: /*#__PURE__*/React.createElement(window.KarukaDesignSystem_69ceb9.Badge, {
      tone: "danger",
      dot: true
    }, "Failed"),
    q2: '—',
    cost: '$0.004',
    wall: '2.1s'
  }]);
  const onNewRun = cmd => {
    setCommand(cmd);
    setRuns(r => [{
      run: 'now',
      cmd,
      cond: 'naive-LLM (plain)',
      status: /*#__PURE__*/React.createElement(window.KarukaDesignSystem_69ceb9.Badge, {
        tone: "info",
        dot: true
      }, "Streaming"),
      q2: '—',
      cost: '—',
      wall: '—'
    }, ...r]);
    setScreen('live');
  };
  return /*#__PURE__*/React.createElement(ConsoleShell, {
    active: screen,
    onNav: setScreen
  }, screen === 'runs' && /*#__PURE__*/React.createElement(RunsScreen, {
    runs: runs,
    onNewRun: onNewRun
  }), screen === 'live' && /*#__PURE__*/React.createElement(LiveScreen, {
    command: command
  }), screen === 'report' && /*#__PURE__*/React.createElement(ReportScreen, null));
}
ReactDOM.createRoot(document.getElementById('root')).render(/*#__PURE__*/React.createElement(App, null));
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/eval-console/app.jsx", error: String((e && e.message) || e) }); }

// ui_kits/eval-console/live.jsx
try { (() => {
const {
  Button,
  Badge,
  MetricStat,
  Card
} = window.KarukaDesignSystem_69ceb9;
const V1_LINES = [{
  t: '$ caruca syntax-spec rm',
  c: '#7FB2F0'
}, {
  t: '[dspy] loading few-shot module … ok'
}, {
  t: '[dspy] model=claude-sonnet-4-5 seed=7'
}, {
  t: '[spec] parsing man/rm.1 (4.1 KB)'
}, {
  t: '[spec] inferring flag grammar … 17 flags'
}, {
  t: '[spec] emitting Python DSL → specs/rm_v1.py',
  c: '#8BE0A4'
}, {
  t: ''
}, {
  t: 'tokens: 8,412 in / 1,206 out'
}, {
  t: 'wall-clock: 14.9s  cost: $0.0130',
  c: '#9CA3AF'
}];
const V2_LINES = [{
  t: '$ caruca-v2 naive-llm rm --docs man/rm.1 --seed 7',
  c: '#7FB2F0'
}, {
  t: '[naive] single-prompt, few-shot primed'
}, {
  t: '[naive] no tool use, no retry loop (by design)'
}, {
  t: '[naive] model=claude-sonnet-4-5 seed=7'
}, {
  t: '[spec] emitting Python DSL → specs/rm_naive.py',
  c: '#8BE0A4'
}, {
  t: '[sandbox] profile=v2-extended backend=firecracker'
}, {
  t: '[sandbox] 312 permutations · strace visible · teardown ok',
  c: '#8BE0A4'
}, {
  t: ''
}, {
  t: 'tokens: 6,077 in / 988 out'
}, {
  t: 'wall-clock: 12.4s  cost: $0.0410',
  c: '#9CA3AF'
}];
function LiveScreen({
  command
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("h2", {
    style: {
      margin: 0,
      fontSize: 20,
      fontWeight: 600,
      letterSpacing: '-.01em'
    }
  }, "Live comparison \u2014 ", /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontWeight: 400
    }
  }, command)), /*#__PURE__*/React.createElement(Badge, {
    tone: "success",
    dot: true
  }, "Streaming"), /*#__PURE__*/React.createElement(Badge, {
    tone: "info",
    mono: true
  }, "seed 7"), /*#__PURE__*/React.createElement("div", {
    style: {
      marginLeft: 'auto',
      display: 'flex',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "sm",
    icon: /*#__PURE__*/React.createElement(Icon, {
      name: "Square",
      size: 13
    })
  }, "Stop"), /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    size: "sm",
    icon: /*#__PURE__*/React.createElement(Icon, {
      name: "RotateCcw",
      size: 13
    })
  }, "Re-run"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(Term, {
    title: "v1 \xB7 caruca",
    host: "pty:0 \xB7 cloudlab-04",
    lines: V1_LINES,
    tone: "live"
  }), /*#__PURE__*/React.createElement(Term, {
    title: "v2 \xB7 caruca-v2",
    host: "pty:1 \xB7 cloudlab-04",
    lines: V2_LINES,
    tone: "live"
  })), /*#__PURE__*/React.createElement(Card, {
    title: "Telemetry \u2014 this run"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 40,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement(MetricStat, {
    label: "v1 tokens",
    value: "9,618"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "v2 tokens",
    value: "7,065",
    delta: "\u221226.5%",
    deltaTone: "up"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "v1 cost",
    value: "$0.013"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "v2 cost",
    value: "$0.041",
    delta: "3.1x v1",
    deltaTone: "down"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "v1 wall-clock",
    value: "14.9",
    unit: "s"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "v2 wall-clock",
    value: "12.4",
    unit: "s",
    delta: "\u221218%",
    deltaTone: "up"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "Model",
    value: "sonnet-4-5"
  }))));
}
Object.assign(window, {
  LiveScreen
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/eval-console/live.jsx", error: String((e && e.message) || e) }); }

// ui_kits/eval-console/report.jsx
try { (() => {
const {
  Badge,
  DataTable,
  MetricStat,
  Callout,
  Card,
  Button
} = window.KarukaDesignSystem_69ceb9;
function ReportScreen() {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-end',
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h2", {
    style: {
      margin: 0,
      fontSize: 27,
      fontWeight: 700,
      letterSpacing: '-.01em',
      color: 'var(--blue)'
    }
  }, "Three-way comparison"), /*#__PURE__*/React.createElement("div", {
    style: {
      width: 80,
      height: 4,
      background: 'linear-gradient(to right,var(--teal),var(--ink))',
      borderRadius: 2,
      marginTop: 8
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      marginLeft: 'auto',
      display: 'flex',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "sm",
    icon: /*#__PURE__*/React.createElement(Icon, {
      name: "FileText",
      size: 13
    })
  }, "Export LaTeX tables"), /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    size: "sm",
    icon: /*#__PURE__*/React.createElement(Icon, {
      name: "Download",
      size: 13
    })
  }, "Figures (PDF)"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 36
    }
  }, /*#__PURE__*/React.createElement(MetricStat, {
    label: "Q2 exact-match \u0394",
    value: "+4.2",
    unit: "%",
    delta: "v2 vs v1, N=12 cmds",
    deltaTone: "up"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "Cost \u0394",
    value: "3.1x",
    delta: "v2 vs v1",
    deltaTone: "down"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "Coverage \u0394",
    value: "+38",
    unit: "%",
    delta: "v2-extended fixtures",
    deltaTone: "up"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "Consistency",
    value: "\xB12.3",
    unit: "pp",
    delta: "variance across N=5",
    deltaTone: "flat"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "Hand-encoded LOC",
    value: "\u22125,890",
    delta: "of v1's 6,520",
    deltaTone: "up"
  })), /*#__PURE__*/React.createElement(Card, {
    title: "Per-command results \u2014 Q2 (cmp_specs.py methodology)",
    actions: /*#__PURE__*/React.createElement(Badge, {
      tone: "neutral",
      mono: true
    }, "eval/runs/2026-08-29T1942/")
  }, /*#__PURE__*/React.createElement(DataTable, {
    columns: [{
      key: 'cmd',
      label: 'Command',
      mono: true
    }, {
      key: 'gt',
      label: 'Ground truth',
      align: 'right'
    }, {
      key: 'v1',
      label: 'v1',
      align: 'right'
    }, {
      key: 'naive',
      label: 'naive-LLM (plain)',
      align: 'right'
    }, {
      key: 'aug',
      label: 'naive-LLM (augmented)',
      align: 'right'
    }, {
      key: 'delta',
      label: 'Δ v2 vs v1',
      align: 'right'
    }],
    rows: [{
      cmd: 'rm',
      gt: '—',
      v1: '91.2%',
      naive: '94.1%',
      aug: '95.6%',
      delta: /*#__PURE__*/React.createElement("span", {
        style: {
          color: 'var(--success-text)'
        }
      }, "+2.9pp")
    }, {
      cmd: 'mkdir',
      gt: '—',
      v1: '100%',
      naive: '100%',
      aug: '100%',
      delta: '0.0pp'
    }, {
      cmd: 'chmod',
      gt: '—',
      v1: '89.4%',
      naive: '88.7%',
      aug: '92.3%',
      delta: /*#__PURE__*/React.createElement("span", {
        style: {
          color: 'var(--danger-text)'
        }
      }, "\u22120.7pp")
    }, {
      cmd: 'ln',
      gt: '—',
      v1: '84.0%',
      naive: '90.5%',
      aug: '91.1%',
      delta: /*#__PURE__*/React.createElement("span", {
        style: {
          color: 'var(--success-text)'
        }
      }, "+6.5pp")
    }, {
      cmd: 'head',
      gt: '—',
      v1: '96.8%',
      naive: '97.2%',
      aug: '97.2%',
      delta: /*#__PURE__*/React.createElement("span", {
        style: {
          color: 'var(--success-text)'
        }
      }, "+0.4pp")
    }]
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      color: 'var(--gray-500)',
      marginTop: 10
    }
  }, "Coverage subtotals are disaggregated (strong-normalization-only alongside blended %) by default. Conditions are reported separately, never blended.")), /*#__PURE__*/React.createElement(Callout, {
    kind: "warning",
    title: "Open dependency"
  }, "v1's annotator was not built to interpret v2-extended trace shapes (symlinks, permission-denied, SIGPIPE). Where it mishandles one, that is itself a reportable coverage-gap finding \u2014 dimension 3 \u2014 not a defect to hide."));
}
Object.assign(window, {
  ReportScreen
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/eval-console/report.jsx", error: String((e && e.message) || e) }); }

// ui_kits/eval-console/runs.jsx
try { (() => {
const {
  Button,
  Input,
  Select,
  Checkbox,
  Card,
  Badge,
  DataTable,
  MetricStat,
  Callout
} = window.KarukaDesignSystem_69ceb9;
function RunsScreen({
  runs,
  onNewRun
}) {
  const [cmd, setCmd] = React.useState('rm');
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 36,
      padding: '4px 2px'
    }
  }, /*#__PURE__*/React.createElement(MetricStat, {
    label: "Commands evaluated",
    value: "12"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "Q2 exact-match",
    value: "87.5",
    unit: "%",
    delta: "+4.2% vs v1",
    deltaTone: "up"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "Cost / command",
    value: "$0.041",
    delta: "3.1x v1",
    deltaTone: "down"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "Wall-clock / cmd",
    value: "12.4",
    unit: "s",
    delta: "\u221218% vs v1",
    deltaTone: "up"
  }), /*#__PURE__*/React.createElement(MetricStat, {
    label: "Variance (N=5)",
    value: "\xB12.3",
    unit: "pp"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 330px',
      gap: 20,
      alignItems: 'start'
    }
  }, /*#__PURE__*/React.createElement(Card, {
    title: "Telemetry runs",
    actions: /*#__PURE__*/React.createElement(Button, {
      variant: "ghost",
      size: "sm",
      icon: /*#__PURE__*/React.createElement(Icon, {
        name: "Download",
        size: 14
      })
    }, "Export JSON")
  }, /*#__PURE__*/React.createElement(DataTable, {
    columns: [{
      key: 'run',
      label: 'Run',
      mono: true
    }, {
      key: 'cmd',
      label: 'Command',
      mono: true
    }, {
      key: 'cond',
      label: 'Condition',
      mono: true
    }, {
      key: 'status',
      label: 'Status'
    }, {
      key: 'q2',
      label: 'Q2 match',
      align: 'right'
    }, {
      key: 'cost',
      label: 'Cost',
      align: 'right'
    }, {
      key: 'wall',
      label: 'Wall-clock',
      align: 'right'
    }],
    rows: runs
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      color: 'var(--gray-500)',
      marginTop: 10
    }
  }, "Runs write to ", /*#__PURE__*/React.createElement("code", {
    style: {
      fontFamily: 'var(--font-mono)',
      background: 'var(--surface-inline-code)',
      padding: '1px 4px',
      borderRadius: 4
    }
  }, "eval/runs/<timestamp>/"), " \u2014 conditions are never blended.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(Card, {
    title: "New run"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 12
    }
  }, /*#__PURE__*/React.createElement(Input, {
    label: "Command",
    mono: true,
    value: cmd,
    onChange: e => setCmd(e.target.value),
    hint: "Binary name as invoked"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement(Select, {
    label: "Profile",
    options: ['v1-faithful', 'v2-extended', 'both'],
    style: {
      flex: 1
    }
  }), /*#__PURE__*/React.createElement(Input, {
    label: "Seed",
    mono: true,
    defaultValue: "7",
    style: {
      width: 80
    }
  })), /*#__PURE__*/React.createElement(Select, {
    label: "Isolation backend",
    options: [{
      value: '',
      label: 'No default — undecided'
    }, {
      value: 'docker',
      label: 'docker'
    }, {
      value: 'firecracker',
      label: 'firecracker'
    }, {
      value: 'gvisor',
      label: 'gvisor'
    }],
    hint: "Open question: backend choice is unresolved"
  }), /*#__PURE__*/React.createElement(Checkbox, {
    label: "Variance sampling (N=5)",
    defaultChecked: true
  }), /*#__PURE__*/React.createElement(Checkbox, {
    label: "Augmented docs \u2014 separate condition"
  }), /*#__PURE__*/React.createElement(Button, {
    icon: /*#__PURE__*/React.createElement(Icon, {
      name: "Play",
      size: 15
    }),
    onClick: () => onNewRun(cmd)
  }, "Run comparison"))), /*#__PURE__*/React.createElement(Callout, {
    kind: "info",
    title: "Telemetry"
  }, "Every run records tokens, cost, wall-clock, model-ID and seed automatically \u2014 no measurement is reconstructed after the fact."))));
}
Object.assign(window, {
  RunsScreen
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/eval-console/runs.jsx", error: String((e && e.message) || e) }); }

// ui_kits/eval-console/shell.jsx
try { (() => {
const {
  Tabs,
  Badge,
  Button
} = window.KarukaDesignSystem_69ceb9;
function Icon({
  name,
  size = 16,
  color = 'currentColor',
  style
}) {
  const ref = React.useRef();
  React.useEffect(() => {
    if (ref.current && window.lucide && lucide.icons[name]) {
      ref.current.innerHTML = '';
      const el = lucide.createElement(lucide.icons[name]);
      el.setAttribute('width', size);
      el.setAttribute('height', size);
      el.setAttribute('stroke', color === 'currentColor' ? 'currentColor' : color);
      ref.current.appendChild(el);
    }
  }, [name, size, color]);
  return /*#__PURE__*/React.createElement("span", {
    ref: ref,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      ...style
    }
  });
}
function ConsoleShell({
  active,
  onNav,
  children,
  right
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      minHeight: '100vh',
      background: '#fff',
      fontFamily: 'var(--font-sans)',
      color: 'var(--ink)'
    }
  }, /*#__PURE__*/React.createElement("header", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 14,
      padding: '14px 28px 0',
      borderBottom: '1px solid var(--border-default)'
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/logo.png",
    alt: "Caruca",
    style: {
      height: 34
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      marginRight: 'auto'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 17,
      fontWeight: 700,
      lineHeight: 1
    }
  }, "Caruca v2 ", /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: 400,
      color: 'var(--gray-500)'
    }
  }, "\xB7 eval console")), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      fontStyle: 'italic',
      color: 'var(--gray-500)',
      marginTop: 2
    }
  }, "LLM-based specification mining for opaque shell commands.")), right, /*#__PURE__*/React.createElement("div", {
    style: {
      alignSelf: 'flex-end'
    }
  }, /*#__PURE__*/React.createElement(Tabs, {
    tabs: [{
      id: 'runs',
      label: 'Runs',
      count: 12
    }, {
      id: 'live',
      label: 'Live comparison'
    }, {
      id: 'report',
      label: 'Report'
    }],
    active: active,
    onChange: onNav
  }))), /*#__PURE__*/React.createElement("main", {
    style: {
      padding: '22px 28px',
      maxWidth: 1224,
      margin: '0 auto'
    }
  }, children));
}
function Term({
  title,
  host,
  lines,
  tone
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 0,
      border: '1px solid var(--border-default)',
      borderRadius: 6,
      overflow: 'hidden',
      display: 'flex',
      flexDirection: 'column'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      padding: '8px 12px',
      background: 'var(--surface-thead)',
      borderBottom: '1px solid var(--border-default)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 11,
      fontWeight: 600,
      textTransform: 'uppercase',
      letterSpacing: '.05em',
      color: 'var(--gray-600)'
    }
  }, title), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 11,
      color: 'var(--gray-400)',
      marginLeft: 'auto'
    }
  }, host), /*#__PURE__*/React.createElement("span", {
    style: {
      width: 7,
      height: 7,
      borderRadius: '50%',
      background: tone === 'live' ? 'var(--success)' : 'var(--gray-400)'
    }
  })), /*#__PURE__*/React.createElement("pre", {
    style: {
      margin: 0,
      flex: 1,
      background: '#0B1F33',
      color: '#D7E3F0',
      padding: '14px 16px',
      fontFamily: 'var(--font-mono)',
      fontSize: 12.5,
      lineHeight: 1.55,
      whiteSpace: 'pre-wrap',
      minHeight: 290
    }
  }, lines.map((l, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      color: l.c || '#D7E3F0'
    }
  }, l.t))));
}
Object.assign(window, {
  Icon,
  ConsoleShell,
  Term
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/eval-console/shell.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Callout = __ds_scope.Callout;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.CodeBlock = __ds_scope.CodeBlock;

__ds_ns.InlineCode = __ds_scope.InlineCode;

__ds_ns.DataTable = __ds_scope.DataTable;

__ds_ns.MetricStat = __ds_scope.MetricStat;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Checkbox = __ds_scope.Checkbox;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Radio = __ds_scope.Radio;

__ds_ns.Select = __ds_scope.Select;

__ds_ns.Switch = __ds_scope.Switch;

__ds_ns.Tabs = __ds_scope.Tabs;

})();
