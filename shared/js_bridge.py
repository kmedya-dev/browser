
CONSOLE_OVERRIDE_JS = """(function() {
    if (window.console.isOverridden) return;

    var originalLog = console.log;
    var originalWarn = console.warn;
    var originalError = console.error;

    function getBridge() {
        if (window.pywebview && window.pywebview.api) {
            return window.pywebview.api; // Desktop (pywebview)
        } else if (window.LogcatBridge) {
            return window.LogcatBridge; // Android (pyjnius)
        }
        return null;
    }

    function sendMessage(type, args) {
        var bridge = getBridge();
        if (!bridge || typeof bridge.log !== 'function') return;

        try {
            var message = Array.from(args).map(function(arg) {
                if (typeof arg === 'object' && arg !== null) {
                    return JSON.stringify(arg);
                }
                return String(arg);
            }).join(' ');
            
            bridge.log(type + ': ' + message);
        } catch (e) {
            // Fallback if something fails
            originalError.call(console, 'Error in console bridge:', e);
        }
    }

    console.log = function(...args) {
        originalLog.apply(console, args);
        sendMessage('LOG', args);
    };

    console.warn = function(...args) {
        originalWarn.apply(console, args);
        sendMessage('WARN', args);
    };

    console.error = function(...args) {
        originalError.apply(console, args);
        sendMessage('ERROR', args);
    };
    
    window.console.isOverridden = true;
})();
"""
