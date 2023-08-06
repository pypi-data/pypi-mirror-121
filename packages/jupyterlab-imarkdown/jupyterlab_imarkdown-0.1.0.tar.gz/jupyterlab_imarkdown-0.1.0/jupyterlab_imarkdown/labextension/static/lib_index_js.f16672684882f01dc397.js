"use strict";
(self["webpackChunkjupyterlab_imarkdown"] = self["webpackChunkjupyterlab_imarkdown"] || []).push([["lib_index_js"],{

/***/ "./lib/attachment.js":
/*!***************************!*\
  !*** ./lib/attachment.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "OUTPUT_MIMETYPE": () => (/* binding */ OUTPUT_MIMETYPE),
/* harmony export */   "ERROR_MIMETYPE": () => (/* binding */ ERROR_MIMETYPE),
/* harmony export */   "isOutput": () => (/* binding */ isOutput),
/* harmony export */   "isError": () => (/* binding */ isError)
/* harmony export */ });
const OUTPUT_MIMETYPE = 'application/vnd.jupyterlab-imarkdown.output';
const ERROR_MIMETYPE = 'application/vnd.jupyterlab-imarkdown.error';
function isOutput(output) {
    return output.status === 'ok';
}
function isError(output) {
    return output.status === 'error';
}


/***/ }),

/***/ "./lib/cell.js":
/*!*********************!*\
  !*** ./lib/cell.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ATTACHMENT_PREFIX": () => (/* binding */ ATTACHMENT_PREFIX),
/* harmony export */   "RENDERED_CLASS": () => (/* binding */ RENDERED_CLASS),
/* harmony export */   "RESULT_CLASS": () => (/* binding */ RESULT_CLASS),
/* harmony export */   "ERROR_CLASS": () => (/* binding */ ERROR_CLASS),
/* harmony export */   "XMarkdownCell": () => (/* binding */ XMarkdownCell)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _tokenize__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./tokenize */ "./lib/tokenize.js");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _attachment__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./attachment */ "./lib/attachment.js");




// Name prefix for cell attachments
const ATTACHMENT_PREFIX = 'jupyterlab-imarkdown';
// Base CSS class for jupyterlab-imarkdown outputs
const RENDERED_CLASS = 'im-rendered';
// CSS class for execution-result outputs
const RESULT_CLASS = 'im-result';
// CSS class for missing outputs
const ERROR_CLASS = 'im-error';
class XMarkdownCell extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.MarkdownCell {
    constructor(options) {
        super(options);
        this.__expressions = {};
        this.__placeholders = {};
        this.__lastContent = '';
        this.__doneRendering = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.PromiseDelegate();
        this.__rendermime = options.rendermime;
    }
    /**
     * Get a mapping of names to kernel expressions.
     */
    get expressions() {
        return this.__expressions;
    }
    /**
     * Whether the Markdown renderer has finished rendering.
     */
    get doneRendering() {
        return this.__doneRendering.promise;
    }
    /**
     * Create an IRenderMime.IMimeModel for a given IExpressionResult
     */
    _createExpressionResultModel(payload) {
        let options;
        if ((0,_attachment__WEBPACK_IMPORTED_MODULE_2__.isOutput)(payload)) {
            // Output results are simple to re-intepret
            options = {
                trusted: this.model.trusted,
                data: payload.data,
                metadata: payload.metadata
            };
        }
        else {
            // Errors need to be formatted as stderr objects
            options = {
                data: {
                    'application/vnd.jupyter.stderr': payload.traceback.join('\n') ||
                        `${payload.ename}: ${payload.evalue}`
                }
            };
        }
        return this.__rendermime.createModel(options);
    }
    /**
     * Render the IExpressionResult produced by the kernel
     */
    _renderExpressionResult(payload) {
        const model = this._createExpressionResultModel(payload);
        // Select preferred mimetype for bundle
        // FIXME: choose appropriate value for `safe`
        const mimeType = this.__rendermime.preferredMimeType(model.data, 'any');
        if (mimeType === undefined) {
            console.error("Couldn't find mimetype");
            return this._renderError();
        }
        // Create renderer
        const renderer = this.__rendermime.createRenderer(mimeType);
        renderer.addClass(RENDERED_CLASS);
        renderer.addClass(RESULT_CLASS);
        // Render model
        renderer.renderModel(model);
        return renderer.node;
    }
    /**
     * Render a generic error in-line
     */
    _renderError() {
        const node = document.createElement('span');
        node.classList.add(RENDERED_CLASS);
        node.classList.add(ERROR_CLASS);
        return node;
    }
    /**
     * Render the given expression from an existing cell attachment MIME bundle.
     * Render an in-line error if no data are available.
     */
    _renderExpression(name) {
        var _a;
        const attachment = this.model.attachments.get(name);
        // We need an attachment!
        if (attachment === undefined) {
            console.error(`Couldn't find attachment ${name}`);
            return this._renderError();
        }
        // Try and render the output from cell attachments
        const payload = ((_a = attachment.data[_attachment__WEBPACK_IMPORTED_MODULE_2__.OUTPUT_MIMETYPE]) !== null && _a !== void 0 ? _a : attachment.data[_attachment__WEBPACK_IMPORTED_MODULE_2__.ERROR_MIMETYPE]);
        if (payload !== undefined) {
            return this._renderExpressionResult(payload);
        }
        // Couldn't find valid MIME bundle, so we need to handle that!
        console.error(`Couldn't find valid MIME bundle for attachment ${name}`);
        return this._renderError();
    }
    /**
     * Update rendered expressions from current attachment MIME-bundles
     */
    renderExpressions() {
        console.log('Rendering expressions');
        // Loop over expressions and render them from the cell attachments
        for (const name in this.__expressions) {
            const node = this._renderExpression(name);
            this._replaceRenderedExpression(name, node);
        }
    }
    /**
     * Update an expression DOM node (result or placeholder) with a new result
     */
    _replaceRenderedExpression(name, node) {
        var _a;
        const placeholder = this.__placeholders[name];
        (_a = placeholder.parentNode) === null || _a === void 0 ? void 0 : _a.replaceChild(node, placeholder);
        this.__placeholders[name] = node;
    }
    /**
     * Wait for Markdown rendering to complete.
     * Assume that rendered container will have at least one child.
     */
    _waitForRender(widget, timeout) {
        // FIXME: this is a HACK
        return new Promise(resolve => {
            function waitReady() {
                const firstChild = widget.node.querySelector('.jp-RenderedMarkdown *');
                if (firstChild !== null) {
                    return resolve();
                }
                setTimeout(waitReady, timeout);
            }
            waitReady();
        });
    }
    renderInput(widget) {
        // FIXME: `renderInput` is called without waiting for render future to finish
        // Therefore, this is sometimes executed before the DOM is updated.
        super.renderInput(widget);
        const currentContent = this.model.value.text;
        // If the content has changed
        if (this.__lastContent !== undefined &&
            this.__lastContent !== currentContent) {
            this.__doneRendering = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.PromiseDelegate();
            // Store parsed expressions
            this._waitForRender(widget, 10).then(() => {
                this._identifyExpressions(widget);
                this.renderExpressions();
                this.__doneRendering.resolve();
            });
            this.__lastContent = currentContent;
        }
    }
    /**
     * Parse the rendered markdown, and store placeholder and expression mappings
     */
    _identifyExpressions(widget) {
        const exprInputNodes = widget.node.querySelectorAll(`input.${_tokenize__WEBPACK_IMPORTED_MODULE_3__.EXPR_CLASS}`);
        // Store expressions & placeholders
        this.__expressions = {};
        this.__placeholders = {};
        exprInputNodes.forEach((node, index) => {
            const name = `${ATTACHMENT_PREFIX}-${index}`;
            this.__expressions[name] = node.value;
            this.__placeholders[name] = node;
        });
        console.log('Found expressions', this.__expressions, this.__placeholders);
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _plugin__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./plugin */ "./lib/plugin.js");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _cell__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./cell */ "./lib/cell.js");
/* harmony import */ var _kernel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./kernel */ "./lib/kernel.js");





class XMarkdownContentFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel.ContentFactory {
    /**
     * Create a new markdown cell widget.
     *
     * #### Notes
     * If no cell content factory is passed in with the options, the one on the
     * notebook content factory is used.
     */
    createMarkdownCell(options, parent) {
        if (!options.contentFactory) {
            options.contentFactory = this;
        }
        return new _cell__WEBPACK_IMPORTED_MODULE_2__.XMarkdownCell(options).initializeState();
    }
}
/**
 * The notebook cell factory provider.
 */
const factory = {
    id: '@agoose77/jupyterlab-imarkdown:factory',
    provides: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel.IContentFactory,
    requires: [_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.IEditorServices],
    autoStart: true,
    activate: (app, editorServices) => {
        console.log('Using jupyterlab-imarkdown:editor');
        const editorFactory = editorServices.factoryService.newInlineEditor;
        return new XMarkdownContentFactory({ editorFactory });
    }
};
function isMarkdownCell(cell) {
    return cell.model.type === 'markdown';
}
function removeKernelAttachments(cell) {
    const attachments = cell.model.attachments;
    attachments.keys
        .filter(key => {
        key.startsWith(_cell__WEBPACK_IMPORTED_MODULE_2__.ATTACHMENT_PREFIX);
    })
        .map(attachments.remove);
}
/**
 * The notebook cell executor.
 */
const executor = {
    id: '@agoose77/jupyterlab-imarkdown:executor',
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    autoStart: true,
    activate: (app, tracker) => {
        console.log('Using jupyterlab-imarkdown:executor');
        const executed = _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executed;
        executed.connect((sender, value) => {
            const { notebook, cell } = value;
            // Find the Notebook panel
            const panel = tracker.find((w) => {
                return w.content === notebook;
            });
            // Retrieve the kernel context
            const ctx = panel === null || panel === void 0 ? void 0 : panel.sessionContext;
            if (ctx === undefined) {
                return;
            }
            // Load the user expressions for the given cell.
            if (!isMarkdownCell(cell)) {
                return;
            }
            console.log('Markdown cell was executed, waiting for render to complete ...');
            cell.doneRendering.then(() => {
                console.log('Clearing results from cell attachments');
                removeKernelAttachments(cell);
                console.log('Loading results from kernel');
                (0,_kernel__WEBPACK_IMPORTED_MODULE_3__.loadUserExpressions)(cell, ctx).then(() => {
                    console.log('Re-rendering cell!');
                    cell.renderExpressions();
                });
            });
        });
        return;
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [factory, executor, _plugin__WEBPACK_IMPORTED_MODULE_4__.plugin];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./lib/kernel.js":
/*!***********************!*\
  !*** ./lib/kernel.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "loadUserExpressions": () => (/* binding */ loadUserExpressions)
/* harmony export */ });
/* harmony import */ var _attachment__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./attachment */ "./lib/attachment.js");

/**
 * Load user expressions for given XMarkdown cell from kernel.
 * Store results in cell attachments.
 */
async function loadUserExpressions(cell, sessionContext) {
    var _a;
    const model = cell.model;
    const cellId = { cellId: model.id };
    // Populate request data
    const content = {
        code: '',
        user_expressions: cell.expressions
    };
    // Perform request
    console.log('Performing kernel request', cell.expressions);
    const kernel = (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
    if (!kernel) {
        throw new Error('Session has no kernel.');
    }
    const future = kernel.requestExecute(content, false, Object.assign(Object.assign({}, model.metadata.toJSON()), cellId));
    // Set response handler
    future.onReply = (msg) => {
        const content = msg.content;
        if (content.status !== 'ok') {
            return;
        }
        console.log('Handling kernel response', msg);
        // Store results as attachments
        for (const key in content.user_expressions) {
            const result = content.user_expressions[key];
            // Determine MIME type to store
            const mimeType = (0,_attachment__WEBPACK_IMPORTED_MODULE_0__.isError)(result) ? _attachment__WEBPACK_IMPORTED_MODULE_0__.ERROR_MIMETYPE : _attachment__WEBPACK_IMPORTED_MODULE_0__.OUTPUT_MIMETYPE;
            // Construct payload from kernel response
            // We don't do any type validation here
            const payload = {};
            payload[mimeType] = result;
            cell.model.attachments.set(key, payload);
            console.log(`Saving ${key} to cell attachments`);
        }
    };
    await future.done;
}


/***/ }),

/***/ "./lib/plugin.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "plugin": () => (/* binding */ plugin)
/* harmony export */ });
/* harmony import */ var _tokenize__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokenize */ "./lib/tokenize.js");
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @agoose77/jupyterlab-markup */ "webpack/sharing/consume/default/@agoose77/jupyterlab-markup");
/* harmony import */ var _agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__);


const PACKAGE_NS = '@agoose77/jupyterlab-imarkdown';
/**
 * Captures expressions as data-attributes
 */
const plugin = (0,_agoose77_jupyterlab_markup__WEBPACK_IMPORTED_MODULE_0__.simpleMarkdownItPlugin)(PACKAGE_NS, {
    id: 'markdown-it-expression',
    title: 'Create spans with stored expressions from Markdown',
    description: 'Embed Markdown text in a data attribute in rendered spans',
    documentationUrls: {
        Plugin: '...'
    },
    plugin: async () => {
        const defaultOptions = {
            openDelim: '{{',
            closeDelim: '}}'
        };
        return [_tokenize__WEBPACK_IMPORTED_MODULE_1__.expressionPlugin, defaultOptions];
    }
});


/***/ }),

/***/ "./lib/tokenize.js":
/*!*************************!*\
  !*** ./lib/tokenize.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EXPR_CLASS": () => (/* binding */ EXPR_CLASS),
/* harmony export */   "expressionPlugin": () => (/* binding */ expressionPlugin)
/* harmony export */ });
const EXPR_CLASS = 'im-expr';
function expressionPlugin(md, options) {
    var _a, _b;
    const openDelim = (_a = options === null || options === void 0 ? void 0 : options.openDelim) !== null && _a !== void 0 ? _a : '{{';
    const closeDelim = (_b = options === null || options === void 0 ? void 0 : options.closeDelim) !== null && _b !== void 0 ? _b : '}}';
    console.log(options);
    function tokenize(state, silent) {
        // Check we start with the correct markers
        let pos = state.pos;
        // For performance, just check first character
        if (state.src[pos] !== openDelim[0]) {
            return false;
        }
        // Does the full substring match?
        if (state.src.slice(pos, pos + openDelim.length) !== openDelim) {
            return false;
        }
        pos += openDelim.length;
        // First index _after_ {{
        const startPos = pos;
        // Find end marker }}
        let stopPos = -1;
        while (stopPos === -1) {
            // Find first character of end marker
            pos = state.src.indexOf(closeDelim[0], pos);
            // Didn't find character
            if (pos === -1) {
                return false;
            }
            // If subsequent tokens don't match, just advance by one token!
            if (state.src.slice(pos, pos + closeDelim.length) === closeDelim) {
                pos++;
                continue;
            }
            stopPos = pos;
            pos += closeDelim.length;
        }
        // Read tokens inside of the bracket
        const expression = state.src.slice(startPos, stopPos);
        state.pos = pos;
        const exprToken = state.push('expr', 'input', 0);
        exprToken.attrSet('type', 'hidden');
        exprToken.attrSet('class', EXPR_CLASS);
        exprToken.attrSet('value', expression);
        return true;
    }
    md.inline.ruler.after('emphasis', 'expr', tokenize);
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.f16672684882f01dc397.js.map