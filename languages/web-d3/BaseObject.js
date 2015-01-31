(function () {
    'use strict';
    module.exports = { // Based on http://www.uxebu.com/blog/2011/02/object-based-inheritance-for-ecmascript-5/
        create: function () { // Creates a class instance, calls _init
            var instance = Object.create(this);
            instance._init.apply(instance, arguments);
            return instance;
        },
        extend: function (properties) { // Class inheritance
            return Object.create(_.extend({}, Object.getPrototypeOf(this), this, properties, {_parent: this}));
        },
        _init: function () {},
        _parent_init: function () {
            if (!this._parent) {
                return;
            }
            var saved_parent = this._parent,
                init_function = this._parent._init;
            this._parent = this._parent._parent;
            init_function.apply(this, arguments);
            this._parent = saved_parent;
        },
    };
})();
