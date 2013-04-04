class StringExpr(object):
    implements(ITALESExpression)

    def __init__(self, name, expr, engine):
        self._s = expr
        if '%' in expr:
            expr = expr.replace('%', '%%')
        self._vars = vars = []
        if '$' in expr:
            # Use whatever expr type is registered as "path".                                                                                                                       
            path_type = engine.getTypes()['path']
            parts = []
            for exp in expr.split('$$'):
                if parts: parts.append('$')
                m = _interp.search(exp)
                while m is not None:
                    parts.append(exp[:m.start()])
                    parts.append('%s')
                    vars.append(path_type(
                        'path', m.group(1) or m.group(2), engine))
                    exp = exp[m.end():]
                    m = _interp.search(exp)
                if '$' in exp:
                    raise engine.getCompilerError()(
                        '$ must be doubled or followed by a simple path')
                parts.append(exp)
            expr = ''.join(parts)
        self._expr = expr
     
