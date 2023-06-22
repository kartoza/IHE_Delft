# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from dynamic_rest import routers
from geonode.urls import urlpatterns, url, include

from delft.api import (
    HierarchicalKeywordAutocompleteByParent,
    HierarchicalKeywordViewSetByParent,
    ResourceBaseViewSetWithKeywords
)

router = routers.DynamicRouter()
router.register(
    r'resources', ResourceBaseViewSetWithKeywords, 'base-resources'
)
router.register(
    r'keywords', HierarchicalKeywordViewSetByParent, 'keywords'
)

# You can register your own urlpatterns here
urlpatterns = [
                  url('^api/v2/', include(router.urls)),
                  url(
                      r'^autocomplete_hierachical_keyword_child/$',
                      HierarchicalKeywordAutocompleteByParent.as_view(),
                      name='autocomplete_hierachical_keyword_child',
                  ),
              ] + urlpatterns
