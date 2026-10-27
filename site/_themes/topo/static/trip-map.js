/* The trip maps on the home page and the Adventures page (see topo/recent-trips.html and timeline.html).

   Each trip is one map, in the site's colors: terrain from the AWS Terrain Tiles, water and borders
   from OpenFreeMap's tiles of OpenStreetMap, and the trip's places drawn as what they were on the
   ground, from trip_shapes.json: a park as its boundary, a trail as its route, anything else as a
   pin, each with its name. scripts/trip_topo.py draws these with topoTripStyle into the images the
   pages show, so the home page loads no map library and a map never shows a blank box.

   On the Adventures page, opening a trip swaps in the same map, live, so you can pan and zoom:
   MapLibre (vendored in _static/vendor), loaded only then. Like the trail map, it replaces the image
   only once its tiles have drawn; without WebGL, or if the tiles fail or are slow, the image stays. */
(function () {
  'use strict';
  var C = {
    paper: '#F2EBDC', land: '#E6DCC4', ink: '#332A20', ruleStrong: '#B5A784', muted: '#6B6354',
    forest: '#255A42', blaze: '#C96B32', sign: '#4F3520', water: '#BFC7B5', wood: '#DDE0C8'
  };
  var FONT = ['Noto Sans Regular'];
  // Countries too small to name at a trip's scale, whose names would crowd the ones that matter.
  var SMALL = ['Andorra', 'Monaco', 'San Marino', 'Vatican City', 'Liechtenstein', 'Luxembourg', 'Gibraltar', 'Malta', 'Brunei', 'Singapore', 'Kosovo'];

  function feature(geometry, props) { return { type: 'Feature', properties: props || {}, geometry: geometry }; }
  function point(p) { return feature({ type: 'Point', coordinates: [p.lon, p.lat] }, { name: p.name, kind: p.kind, anchor: p.anchor || 'left' }); }
  function collection(features) { return { type: 'FeatureCollection', features: features }; }

  // geo is a trip's "geo" (topo_trips.trip_geo). size is the name's size in pixels.
  // Room around the places for their names, as a share of the map's size.
  window.topoTripPadding = function (w, h) {
    return { top: Math.round(h * 0.16), bottom: Math.round(h * 0.16), left: Math.round(w * 0.12), right: Math.round(w * 0.12) };
  };

  window.topoTripStyle = function (geo, size) {
    size = size || 12;
    var shaped = geo.places.filter(function (p) { return p.shape; });
    var isLine = function (p) { return /LineString/.test(p.shape.type); };
    return {
      version: 8,
      glyphs: 'https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf',
      sources: {
        osm: { type: 'vector', url: 'https://tiles.openfreemap.org/planet' },
        dem: { type: 'raster-dem', tiles: ['https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'],
               encoding: 'terrarium', tileSize: 256, maxzoom: 12 },
        areas: { type: 'geojson', data: collection(shaped.filter(function (p) { return !isLine(p); }).map(function (p) { return feature(p.shape); })) },
        routes: { type: 'geojson', data: collection(shaped.filter(isLine).map(function (p) { return feature(p.shape); })) },
        // A park gets a pin too, since at the scale of a long trip its shape can be a speck.
        pins: { type: 'geojson', data: collection(geo.places.filter(function (p) { return !p.shape || !isLine(p); }).map(point)) },
        names: { type: 'geojson', data: collection(geo.places.map(point)) }
      },
      layers: [
        { id: 'land', type: 'background', paint: { 'background-color': C.land } },
        { id: 'wood', type: 'fill', source: 'osm', 'source-layer': 'landcover', filter: ['==', ['get', 'class'], 'wood'],
          paint: { 'fill-color': C.wood, 'fill-opacity': 0.5 } },
        { id: 'shade', type: 'hillshade', source: 'dem',
          paint: { 'hillshade-shadow-color': '#7A6A4C', 'hillshade-highlight-color': '#FBF7EE', 'hillshade-accent-color': C.ruleStrong,
                   'hillshade-exaggeration': 0.55, 'hillshade-illumination-direction': 315 } },
        { id: 'glacier', type: 'fill', source: 'osm', 'source-layer': 'landcover', filter: ['==', ['get', 'class'], 'ice'],
          paint: { 'fill-color': '#FBF7EE', 'fill-opacity': 0.6 } },
        { id: 'water', type: 'fill', source: 'osm', 'source-layer': 'water', paint: { 'fill-color': C.water } },
        { id: 'coast', type: 'line', source: 'osm', 'source-layer': 'water', paint: { 'line-color': '#A9B3A0', 'line-width': 0.6 } },
        { id: 'borders', type: 'line', source: 'osm', 'source-layer': 'boundary',
          filter: ['all', ['==', ['get', 'admin_level'], 2], ['!=', ['get', 'maritime'], 1]],
          paint: { 'line-color': C.muted, 'line-opacity': 0.55, 'line-width': 0.9, 'line-dasharray': [3, 2] } },
        { id: 'area-fill', type: 'fill', source: 'areas', paint: { 'fill-color': C.forest, 'fill-opacity': 0.28 } },
        { id: 'area-line', type: 'line', source: 'areas', paint: { 'line-color': C.forest, 'line-width': 1.3 } },
        { id: 'route-halo', type: 'line', source: 'routes', layout: { 'line-join': 'round', 'line-cap': 'round' },
          paint: { 'line-color': C.paper, 'line-width': 5, 'line-opacity': 0.85 } },
        { id: 'route', type: 'line', source: 'routes', layout: { 'line-join': 'round', 'line-cap': 'round' },
          paint: { 'line-color': C.forest, 'line-width': 2.6 } },
        { id: 'pins', type: 'circle', source: 'pins',
          paint: { 'circle-radius': size * 0.36, 'circle-stroke-color': C.paper, 'circle-stroke-width': 1.5,
                   'circle-color': ['match', ['get', 'kind'], 'lived', C.sign, 'hiked', C.forest, C.blaze] } },
        { id: 'states', type: 'line', source: 'osm', 'source-layer': 'boundary',
          filter: ['all', ['==', ['get', 'admin_level'], 4], ['!=', ['get', 'maritime'], 1]],
          layout: { visibility: geo.states ? 'visible' : 'none' },
          paint: { 'line-color': C.muted, 'line-opacity': 0.4, 'line-width': 0.7, 'line-dasharray': [3, 2] } },
        // Countries (or US states) for a sense of where, below the places' names, which win any overlap.
        { id: 'countries', type: 'symbol', source: 'osm', 'source-layer': 'place',
          filter: geo.states ? ['==', ['get', 'class'], 'state'] : ['all', ['==', ['get', 'class'], 'country'], ['!', ['in', ['get', 'name:en'], ['literal', SMALL]]]],
          layout: { 'text-field': ['upcase', ['coalesce', ['get', 'name:en'], ['get', 'name']]], 'text-font': FONT,
                    'text-size': size * 0.72, 'text-letter-spacing': 0.14, 'text-padding': 6 },
          paint: { 'text-color': C.muted, 'text-opacity': 0.8, 'text-halo-color': C.land, 'text-halo-width': 1 } },
        { id: 'names', type: 'symbol', source: 'names',
          layout: { 'text-field': ['get', 'name'], 'text-font': FONT, 'text-size': size, 'text-max-width': 9,
                    'text-anchor': ['get', 'anchor'], 'text-radial-offset': 0.8, 'text-justify': 'auto', 'text-padding': 1 },
          paint: { 'text-color': C.ink, 'text-halo-color': C.paper, 'text-halo-width': 1.6 } }
      ]
    };
  };

  var figures = document.querySelectorAll('.topo-trip-map[data-geo]');
  if (!figures.length || !window.WebGLRenderingContext) return;
  var base = figures[0].getAttribute('data-static');
  var VERSION = 'maplibre-gl-4.7.1';
  var TIMEOUT = 10000;
  var loading = null;

  function load(tag, attrs) {
    return new Promise(function (resolve, reject) {
      var el = document.createElement(tag);
      for (var k in attrs) el.setAttribute(k, attrs[k]);
      el.onload = resolve; el.onerror = reject;
      document.head.appendChild(el);
    });
  }
  function maplibre() {
    loading = loading || load('link', { rel: 'stylesheet', href: base + 'vendor/' + VERSION + '/maplibre-gl.css' })
      .then(function () { return load('script', { src: base + 'vendor/' + VERSION + '/maplibre-gl.js' }); });
    return loading;
  }

  function start(figure) {
    var geo = JSON.parse(figure.getAttribute('data-geo'));
    var style = window.topoTripStyle(geo, 13);
    var holder = document.createElement('div');
    holder.className = 'topo-trip-live';
    figure.appendChild(holder);
    var b = geo.bounds;
    var map = new maplibregl.Map({
      container: holder, style: style, bounds: [[b[0], b[1]], [b[2], b[3]]],
      fitBoundsOptions: { padding: window.topoTripPadding(holder.clientWidth, holder.clientHeight) },
      attributionControl: false, cooperativeGestures: true, renderWorldCopies: false, dragRotate: false,
      pitchWithRotate: false, touchPitch: false
    });
    map.touchZoomRotate.disableRotation();
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right');
    map.addControl(new maplibregl.AttributionControl({ compact: true, customAttribution: 'Terrain: Terrain Tiles on AWS' }), 'bottom-right');
    var timer = setTimeout(function () { map.remove(); holder.remove(); }, TIMEOUT);
    map.once('idle', function () {
      if (!holder.isConnected) return;
      clearTimeout(timer);
      figure.classList.add('is-live');
      var attrib = holder.querySelector('.maplibregl-ctrl-attrib');
      if (attrib) attrib.classList.remove('maplibregl-compact-show');
    });
  }

  [].forEach.call(figures, function (figure) {
    var details = figure.closest('details');
    function open() {
      if (figure.dataset.started || details && !details.open) return;
      figure.dataset.started = '1';
      maplibre().then(function () { start(figure); }).catch(function () {});
    }
    if (details) details.addEventListener('toggle', open);
    open();
  });
})();
