/* The live map on a trail page (see topo/trail.html).

   The page already shows the trail on a static relief. This swaps in a map you can pan, zoom, and tilt
   into 3D: MapLibre (vendored in _static/vendor), with OpenFreeMap's vector tiles of OpenStreetMap and
   USGS terrain from the AWS Terrain Tiles, styled in the site's colors. The route, nights, passes, and
   photos come from the page's own data. Hovering the elevation profile moves a marker along the map,
   and hovering the route moves one along the profile.

   It only replaces the static map once the map's tiles have loaded. Without WebGL, or if the tiles
   fail or are slow, the static map stays, so the page never shows a blank box. */
(function () {
  'use strict';
  var figure = document.querySelector('.topo-trail-map');
  var dataEl = figure && figure.querySelector('.topo-trail-data');
  if (!figure || !dataEl || !window.WebGLRenderingContext) return;
  var data = JSON.parse(dataEl.textContent);
  var base = figure.getAttribute('data-static');
  var VERSION = 'maplibre-gl-4.7.1';
  var TIMEOUT = 10000;
  var PADDING = { top: 40, bottom: 40, left: 40, right: 60 };

  // The site's tokens (topo.css); the map's style needs them as values.
  var css = getComputedStyle(document.documentElement);
  function token(name, fallback) { return (css.getPropertyValue(name) || '').trim() || fallback; }
  var C = {
    paper: token('--paper', '#F2EBDC'), hero: token('--hero', '#EBE2CD'), ink: token('--ink', '#332A20'),
    muted: token('--muted', '#6B6354'), rule: token('--rule', '#D9CFB8'), ruleStrong: token('--rule-strong', '#B5A784'),
    forest: token('--forest', '#255A42'), blaze: token('--blaze', '#C96B32'), sign: token('--sign', '#4F3520'), gold: token('--sign-gold', '#DBA63E'),
    water: '#BFC7B5', wood: '#DDE0C8' // forest mixed into paper, 25% and 12%
  };

  function load(tag, attrs) {
    return new Promise(function (resolve, reject) {
      var el = document.createElement(tag);
      for (var k in attrs) el.setAttribute(k, attrs[k]);
      el.onload = resolve; el.onerror = reject;
      document.head.appendChild(el);
    });
  }

  function lineFeature(coords, props) {
    return { type: 'Feature', properties: props || {}, geometry: { type: 'LineString', coordinates: coords } };
  }
  function pointFeature(lon, lat, props) {
    return { type: 'Feature', properties: props || {}, geometry: { type: 'Point', coordinates: [lon, lat] } };
  }
  function collection(features) { return { type: 'FeatureCollection', features: features }; }

  var track = data.track; // [lon, lat, mile, feet]
  var route = lineFeature(track.map(function (p) { return [p[0], p[1]]; }));
  function atMile(mile) {
    var best = track[0];
    for (var i = 1; i < track.length; i++) if (Math.abs(track[i][2] - mile) < Math.abs(best[2] - mile)) best = track[i];
    return best;
  }
  function nearest(lngLat) {
    var k = Math.cos(lngLat.lat * Math.PI / 180), best = null, bestD = Infinity;
    for (var i = 0; i < track.length; i++) {
      var dx = (track[i][0] - lngLat.lng) * k, dy = track[i][1] - lngLat.lat, d = dx * dx + dy * dy;
      if (d < bestD) { bestD = d; best = track[i]; }
    }
    return best;
  }
  function feet(n) { return Math.round(n).toLocaleString('en-US'); }

  var FONT = ['Noto Sans Regular'];
  var halo = { 'text-halo-color': C.paper, 'text-halo-width': 1.6, 'text-halo-blur': 0.4 };
  var style = {
    version: 8,
    glyphs: 'https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf',
    sources: {
      osm: { type: 'vector', url: 'https://tiles.openfreemap.org/planet' },
      dem: {
        type: 'raster-dem', tiles: ['https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'],
        encoding: 'terrarium', tileSize: 256, maxzoom: 14
      },
      // The same terrain again for 3D, which MapLibre draws better from a source of its own.
      terrain: {
        type: 'raster-dem', tiles: ['https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'],
        encoding: 'terrarium', tileSize: 256, maxzoom: 14
      },
      route: { type: 'geojson', data: route },
      day: { type: 'geojson', data: collection([]) },
      spurs: { type: 'geojson', data: collection(data.spurs.map(function (s) { return lineFeature(s.line, { name: s.name }); })) },
      nights: { type: 'geojson', data: collection(data.nights.map(function (n) { return pointFeature(n.lon, n.lat, n); })) },
      passes: {
        type: 'geojson', data: collection(data.passes.map(function (p) {
          var t = atMile(p.mile); return pointFeature(t[0], t[1], { name: p.name, label: p.name + '\n' + feet(p.feet) + ' ft', mile: p.mile });
        }))
      },
      ends: {
        type: 'geojson', data: collection([data.start, data.end].map(function (e) { return pointFeature(e.lon, e.lat, { name: e.name }); }))
      }
    },
    layers: [
      { id: 'paper', type: 'background', paint: { 'background-color': C.paper } },
      { id: 'wood', type: 'fill', source: 'osm', 'source-layer': 'landcover', filter: ['==', ['get', 'class'], 'wood'],
        paint: { 'fill-color': C.wood, 'fill-opacity': 0.7 } },
      { id: 'park', type: 'line', source: 'osm', 'source-layer': 'park', minzoom: 7,
        paint: { 'line-color': C.forest, 'line-opacity': 0.25, 'line-width': 1, 'line-dasharray': [3, 2] } },
      { id: 'shade', type: 'hillshade', source: 'dem',
        paint: { 'hillshade-shadow-color': '#7A6A4C', 'hillshade-highlight-color': '#FBF7EE', 'hillshade-accent-color': C.ruleStrong,
                 'hillshade-exaggeration': 0.55, 'hillshade-illumination-direction': 315 } },
      { id: 'glacier', type: 'fill', source: 'osm', 'source-layer': 'landcover', filter: ['==', ['get', 'class'], 'ice'],
        paint: { 'fill-color': '#FBF7EE', 'fill-opacity': 0.6 } },
      { id: 'water', type: 'fill', source: 'osm', 'source-layer': 'water', paint: { 'fill-color': C.water } },
      { id: 'river', type: 'line', source: 'osm', 'source-layer': 'waterway', minzoom: 9,
        paint: { 'line-color': C.water, 'line-width': ['interpolate', ['linear'], ['zoom'], 9, 0.6, 14, 2] } },
      { id: 'roads', type: 'line', source: 'osm', 'source-layer': 'transportation',
        filter: ['match', ['get', 'class'], ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'minor'], true, false],
        paint: { 'line-color': '#FBF7EE', 'line-width': ['interpolate', ['linear'], ['zoom'], 7, 0.6, 14, 3] } },
      { id: 'roads-edge', type: 'line', source: 'osm', 'source-layer': 'transportation', minzoom: 9,
        filter: ['match', ['get', 'class'], ['motorway', 'trunk', 'primary', 'secondary'], true, false],
        paint: { 'line-color': C.ruleStrong, 'line-width': 0.5, 'line-gap-width': ['interpolate', ['linear'], ['zoom'], 9, 1, 14, 3] } },
      { id: 'paths', type: 'line', source: 'osm', 'source-layer': 'transportation', minzoom: 11,
        filter: ['match', ['get', 'class'], ['path', 'track'], true, false],
        paint: { 'line-color': C.sign, 'line-opacity': 0.45, 'line-width': 1, 'line-dasharray': [2, 2] } },
      { id: 'spurs', type: 'line', source: 'spurs', paint: { 'line-color': C.sign, 'line-width': 2, 'line-dasharray': [2, 2] } },
      { id: 'route-halo', type: 'line', source: 'route', layout: { 'line-join': 'round', 'line-cap': 'round' },
        paint: { 'line-color': C.paper, 'line-width': ['interpolate', ['linear'], ['zoom'], 7, 5, 14, 9], 'line-opacity': 0.85 } },
      { id: 'route', type: 'line', source: 'route', layout: { 'line-join': 'round', 'line-cap': 'round' },
        paint: { 'line-color': C.forest, 'line-width': ['interpolate', ['linear'], ['zoom'], 7, 2.5, 14, 5] } },
      { id: 'day', type: 'line', source: 'day', layout: { 'line-join': 'round', 'line-cap': 'round' },
        paint: { 'line-color': C.blaze, 'line-width': ['interpolate', ['linear'], ['zoom'], 7, 4, 14, 7] } },
      { id: 'lake-names', type: 'symbol', source: 'osm', 'source-layer': 'water_name', minzoom: 11,
        layout: { 'text-field': ['get', 'name'], 'text-font': ['Noto Sans Italic'], 'text-size': 11 },
        paint: Object.assign({ 'text-color': '#4E5E50' }, halo) },
      { id: 'peaks', type: 'symbol', source: 'osm', 'source-layer': 'mountain_peak', minzoom: 10,
        filter: ['has', 'name'],
        layout: { 'text-field': ['concat', ['get', 'name'], '\n', ['to-string', ['get', 'ele_ft']], ' ft'], 'text-font': FONT,
                  'text-size': 10, 'text-anchor': 'top', 'text-offset': [0, 0.4] },
        paint: Object.assign({ 'text-color': C.muted }, halo) },
      { id: 'towns', type: 'symbol', source: 'osm', 'source-layer': 'place', minzoom: 7,
        filter: ['match', ['get', 'class'], ['city', 'town', 'village'], true, false],
        layout: { 'text-field': ['get', 'name'], 'text-font': FONT, 'text-size': 11 },
        paint: Object.assign({ 'text-color': C.ink }, halo) },
      { id: 'passes', type: 'symbol', source: 'passes', minzoom: 8.5,
        layout: { 'text-field': ['get', 'label'], 'text-font': FONT, 'text-size': 11, 'text-anchor': 'left', 'text-offset': [0.9, 0],
                  'text-optional': true, 'icon-image': 'pass', 'icon-allow-overlap': true },
        paint: Object.assign({ 'text-color': C.sign }, halo) },
      { id: 'nights', type: 'circle', source: 'nights',
        paint: { 'circle-radius': ['interpolate', ['linear'], ['zoom'], 7, 3.5, 13, 6], 'circle-color': C.gold,
                 'circle-stroke-color': C.sign, 'circle-stroke-width': 1.5 } },
      { id: 'ends', type: 'circle', source: 'ends',
        paint: { 'circle-radius': 6, 'circle-color': C.forest, 'circle-stroke-color': C.paper, 'circle-stroke-width': 2 } },
      { id: 'end-names', type: 'symbol', source: 'ends',
        layout: { 'text-field': ['get', 'name'], 'text-font': FONT, 'text-size': 13, 'text-anchor': 'left', 'text-offset': [0.9, 0] },
        paint: Object.assign({ 'text-color': C.ink }, halo) }
    ]
  };

  function passIcon(map) {
    var s = 14, canvas = document.createElement('canvas');
    canvas.width = canvas.height = s * 2;
    var g = canvas.getContext('2d');
    g.scale(2, 2);
    g.beginPath(); g.moveTo(s / 2, 1.5); g.lineTo(s - 2, s - 2.5); g.lineTo(2, s - 2.5); g.closePath();
    g.fillStyle = C.sign; g.strokeStyle = C.paper; g.lineWidth = 1.5; g.stroke(); g.fill();
    map.addImage('pass', g.getImageData(0, 0, s * 2, s * 2), { pixelRatio: 2 });
  }

  function start() {
    var maplibregl = window.maplibregl;
    var canvas = figure.querySelector('.topo-trail-canvas');
    var holder = document.createElement('div');
    holder.className = 'topo-trail-live';
    canvas.appendChild(holder);

    var lons = track.map(function (p) { return p[0]; }), lats = track.map(function (p) { return p[1]; });
    var bounds = [[Math.min.apply(null, lons), Math.min.apply(null, lats)], [Math.max.apply(null, lons), Math.max.apply(null, lats)]];
    var map;
    try {
      map = new maplibregl.Map({
        container: holder, style: style, bounds: bounds, fitBoundsOptions: { padding: PADDING },
        cooperativeGestures: true, attributionControl: false, maxPitch: 70
      });
    } catch (e) { holder.remove(); return; }

    // Swap in once the map has drawn with real map data; otherwise drop it and keep the static map.
    var settled = false;
    function giveUp() { if (!settled) { settled = true; map.remove(); holder.remove(); } }
    var timer = setTimeout(giveUp, TIMEOUT);
    map.on('idle', function () {
      if (settled) return;
      var drawn = ['water', 'transportation', 'landcover', 'place'].some(function (l) {
        return map.querySourceFeatures('osm', { sourceLayer: l }).length;
      });
      if (!drawn) return; // tiles not here yet
      settled = true; clearTimeout(timer);
      figure.classList.add('is-live');
      map.resize();
      map.fitBounds(bounds, { padding: PADDING, duration: 0 });
      // Credits start folded into the (i) button, so they don't cover the route's end.
      var attrib = holder.querySelector('.maplibregl-compact-show');
      if (attrib) attrib.classList.remove('maplibregl-compact-show');
    });
    map.on('styleimagemissing', function (e) { if (e.id === 'pass') passIcon(map); });

    map.addControl(new maplibregl.AttributionControl({
      compact: true,
      customAttribution: 'Terrain: USGS 3DEP' // OpenFreeMap's own credits come with its tiles
    }));
    map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'top-right');
    map.addControl(new maplibregl.FullscreenControl({ container: figure.querySelector('.topo-trail-canvas') }), 'top-right');
    map.addControl(new maplibregl.ScaleControl({ unit: 'imperial' }), 'bottom-left');

    // 3D: the terrain, tilted, and back to flat.
    var tilt = document.createElement('button');
    tilt.type = 'button'; tilt.className = 'topo-trail-3d'; tilt.textContent = '3D'; tilt.setAttribute('aria-pressed', 'false');
    tilt.title = 'Show the terrain in 3D';
    holder.appendChild(tilt);
    tilt.addEventListener('click', function () {
      var on = tilt.getAttribute('aria-pressed') !== 'true';
      tilt.setAttribute('aria-pressed', String(on));
      if (on) { map.setTerrain({ source: 'terrain', exaggeration: 1.3 }); map.easeTo({ pitch: 60, duration: 900 }); }
      else { map.easeTo({ pitch: 0, bearing: 0, duration: 700 }); map.once('moveend', function () { map.setTerrain(null); }); }
    });

    map.on('load', function () {
      var popup = new maplibregl.Popup({ closeButton: false, offset: 10, className: 'topo-trail-popup' });
      function hoverText(layer, text) {
        map.on('mouseenter', layer, function (e) {
          map.getCanvas().style.cursor = 'default';
          popup.setLngLat(e.features[0].geometry.coordinates).setHTML(text(e.features[0].properties)).addTo(map);
        });
        map.on('mouseleave', layer, function () { popup.remove(); });
      }
      hoverText('nights', function (p) { return '<strong>Night ' + p.night + '</strong> · ' + p.day + ' · mile ' + p.mile; });
      hoverText('passes', function (p) { return '<strong>' + p.name + '</strong> · mile ' + Math.round(p.mile); });

      // Photos: numbered pins on the route; a click opens the photo.
      data.photos.forEach(function (ph) {
        if (ph.lon == null) return;
        var pin = document.createElement('button');
        pin.type = 'button'; pin.className = 'topo-trail-map-photo'; pin.textContent = ph.n;
        pin.setAttribute('aria-label', 'Photo ' + ph.n + ', ' + ph.day);
        var card = new maplibregl.Popup({ offset: 14, maxWidth: '280px', className: 'topo-trail-popup is-photo' }).setHTML(
          '<a href="#photo-' + ph.n + '"><img src="' + base + ph.file + '" alt="Photo ' + ph.n + '" loading="lazy"></a>' +
          '<span>' + ph.day + (ph.mile != null ? ' · mile ' + ph.mile : '') + '</span>');
        new maplibregl.Marker({ element: pin }).setLngLat([ph.lon, ph.lat]).setPopup(card).addTo(map);
      });
    });

    // The route and the profile follow each other.
    var cursor = document.createElement('div');
    cursor.className = 'topo-trail-cursor';
    var here = new maplibregl.Marker({ element: cursor });
    var plot = document.querySelector('.topo-trail-plot');
    var line = document.createElement('div');
    line.className = 'topo-trail-plot-cursor';
    line.hidden = true;
    if (plot) plot.appendChild(line);
    var miles = track[track.length - 1][2];
    function show(p, fromMap) {
      here.setLngLat([p[0], p[1]]).addTo(map);
      cursor.setAttribute('data-label', 'Mile ' + Math.round(p[2]) + ' · ' + feet(p[3]) + ' ft');
      if (plot) { line.hidden = false; line.style.left = (100 * p[2] / miles) + '%'; line.setAttribute('data-label', fromMap ? 'Mile ' + Math.round(p[2]) : ''); }
    }
    function hide() { here.remove(); line.hidden = true; }
    if (plot) {
      plot.addEventListener('pointermove', function (e) {
        if (!figure.classList.contains('is-live')) return;
        var r = plot.getBoundingClientRect();
        show(atMile(Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * miles), false);
      });
      plot.addEventListener('pointerleave', hide);
    }
    map.on('mousemove', 'route-halo', function (e) { show(nearest(e.lngLat), true); });
    map.on('mouseleave', 'route-halo', hide);

    // Day by day: hovering a day lights up its stretch on the map and the profile; a click zooms to it.
    var band = document.createElement('div');
    band.className = 'topo-trail-plot-band';
    band.hidden = true;
    if (plot) plot.appendChild(band);
    function stretch(from, to) {
      return track.filter(function (p) { return p[2] >= from - 0.01 && p[2] <= to + 0.01; });
    }
    function light(day) {
      if (!figure.classList.contains('is-live')) return;
      var from = +day.getAttribute('data-from'), to = +day.getAttribute('data-to');
      var pts = stretch(from, to);
      if (pts.length > 1) map.getSource('day').setData(lineFeature(pts.map(function (p) { return [p[0], p[1]]; })));
      if (plot) { band.hidden = false; band.style.left = (100 * from / miles) + '%'; band.style.width = (100 * (to - from) / miles) + '%'; }
    }
    function unlight() {
      if (map.getSource('day')) map.getSource('day').setData(collection([]));
      band.hidden = true;
    }
    [].forEach.call(document.querySelectorAll('.topo-trail-day'), function (day) {
      day.addEventListener('mouseenter', function () { light(day); });
      day.addEventListener('mouseleave', unlight);
      day.addEventListener('click', function (e) {
        if (e.target.closest('a') || !figure.classList.contains('is-live')) return;
        var pts = stretch(+day.getAttribute('data-from'), +day.getAttribute('data-to'));
        if (pts.length < 2) pts = stretch(+day.getAttribute('data-from') - 2, +day.getAttribute('data-to') + 2);
        var lons = pts.map(function (p) { return p[0]; }), lats = pts.map(function (p) { return p[1]; });
        map.fitBounds([[Math.min.apply(null, lons), Math.min.apply(null, lats)], [Math.max.apply(null, lons), Math.max.apply(null, lats)]],
          { padding: PADDING, maxZoom: 13, duration: 800 });
        figure.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  // Wait until the map is near the screen, then load MapLibre.
  function go() {
    load('link', { rel: 'stylesheet', href: base + 'vendor/' + VERSION + '/maplibre-gl.css' })
      .then(function () { return load('script', { src: base + 'vendor/' + VERSION + '/maplibre-gl.js' }); })
      .then(start)
      .catch(function () {});
  }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      if (entries.some(function (e) { return e.isIntersecting; })) { io.disconnect(); go(); }
    }, { rootMargin: '400px' });
    io.observe(figure);
  } else {
    go();
  }
})();
