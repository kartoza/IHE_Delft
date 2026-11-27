(function () {
    'use strict';

    var injector = angular.element(document).injector();
    if (!injector) {
        return;
    }

    injector.invoke(['$rootScope', '$location', function ($rootScope, $location) {
        var unwatch = $rootScope.$watch('groupCategories', function (categories) {
            if (!categories) {
                return;
            }
            unwatch();

            var slugs = $location.search()['categories__slug__in'];
            if (slugs) {
                angular.module('geonode_main_search')
                    .set_initial_filters_from_query(categories, slugs, 'slug');
            }
        });
    }]);
})();
