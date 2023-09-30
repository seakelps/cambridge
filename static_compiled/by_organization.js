var by_organization =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./static_src/by_organization.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./static_src/by_organization.js":
/*!***************************************!*\
  !*** ./static_src/by_organization.js ***!
  \***************************************/
/*! exports provided: createTable */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"createTable\", function() { return createTable; });\nfunction createTable() {\n  $.fn.dataTable.Buttons.defaults.dom.button.className = 'btn btn-light';\n  $.fn.dataTable.Buttons.defaults.dom.split.action.className = 'btn btn-light';\n  $.fn.dataTable.Buttons.defaults.dom.split.dropdown.className = 'btn btn-light';\n  $.fn.dataTable.Buttons.defaults.dom.container.className = 'btn-group-toggle';\n  var dt = new DataTable(\"#myTable\", {\n    ordering: false,\n    paging: false,\n    searching: false,\n    dom: \"<'#filterBar.py-4'B>t\",\n    buttons: [{\n      extend: \"columnsToggle\",\n      columns: \".col-organization\"\n    }],\n    columnDefs: [{\n      targets: 0,\n      visible: false,\n      // not yet done\n      render: function render(data, type, row) {\n        return \"\\n            <a class=\\\"btn btn-dark btn-sm\\\" href=\\\"\".concat(data, \"\\\">\\n              <i class=\\\"fa fa-plus\\\"></i>\\n            </a>\");\n      }\n    }, {\n      targets: 1,\n      visible: true,\n      render: function render(data, type, row) {\n        return \"<a href=\".concat(row[2], \">\").concat(data, \"</a>\");\n      }\n    }, {\n      // detail url\n      targets: [2],\n      visible: false\n    }, {\n      targets: \"col-organization\",\n      render: function render(data, type, row) {\n        switch (data) {\n          case \"True\":\n            return '<i class=\"fa fa-check text-success\"></i>';\n\n          case \"False\":\n            return '<i class=\"fa fa-ban text-danger\"></i>';\n\n          default:\n            return value;\n        }\n      }\n    }, {\n      // first few organizations\n      targets: [3, 4, 5],\n      visible: true\n    }, {\n      // rest of organizations\n      targets: \"_all\",\n      visible: false\n    }]\n  });\n  $(\"#filterBar\").prepend(\"<label>Click an organization below to show or hide their endorsements in the table.</label>\");\n  document.querySelectorAll('#org-toggle > label').forEach(function (el) {\n    el.addEventListener('click', function (e) {\n      e.preventDefault();\n      var columnName = e.target.getAttribute('data-column');\n      var column = dt.column(\":contains(\\\"\".concat(columnName, \"\\\")\")); // Toggle the visibility\n\n      column.visible(!column.visible());\n    });\n  });\n  window.dt = dt;\n  /* table-responsive must wrap the table, but data-tables adds a div\n       before and after the table, so we have to do this after DataTables is\n       applied so the table controls don't also scroll */\n\n  $(\"#myTable\").wrap(\"<div class='table-responsive'></div>\");\n  $(\"[data-toggle=tooltip]\").tooltip();\n}\n\n\n\n//# sourceURL=webpack://%5Bname%5D/./static_src/by_organization.js?");

/***/ })

/******/ });