import Map from 'ol/Map.js';
import {unByKey} from 'ol/Observable.js';
import Overlay from 'ol/Overlay.js';
import {getArea, getLength} from 'ol/sphere.js';
import View from 'ol/View.js';
import {LineString, Polygon} from 'ol/geom.js';
import Draw from 'ol/interaction/Draw.js';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer.js';
import {OSM, Vector as VectorSource} from 'ol/source.js';
import {Circle as CircleStyle, Fill, Stroke, Style} from 'ol/style.js';


window.app = {};

var app = window.app;
var mapLoadInput = document.getElementById('map-load-control');
var loadButton = document.getElementById('map-load-button');
var cleanButton = document.getElementById('map-clean-button');
var testLabel = document.getElementById('query-test');
var histTable = document.getElementById('load-history');
var typeSelect = document.getElementById('measure-type');

var legendOnOff = false;

// Create a new dictionary to hold objects that have been loaded
var loadedDict = {};
var layersDic = {};

var baseTile = new TileLayer({
    source: new OSM()
});

// Measurement related variables
var source = new VectorSource();

var vector = new VectorLayer({
source: source,
style: new Style({
    fill: new Fill({
        color: 'rgba(255, 255, 255, 0.2)'
    }),
    stroke: new Stroke({
        color: '#ffcc33',
        width: 2
    }),
    image: new CircleStyle({
        radius: 7,
        fill: new Fill({color: '#ffcc33' })
    })
  })
});

var sketch;
var helpTooltipElement;
var helpTooltip;
var measureTooltipElement;
var measureTooltip;
var draw;

var continuePolygonMsg = 'Click para continuar dibujando el polígono';
var continueLineMsg = 'Click para continuar dibujando la línea';

app.CenterViewControl = function(opt_options) {
    var options = opt_options || {};
    var button = document.createElement('button');
    button.innerHTML = '&#x2605;';
    var this_ = this;

    var handleCenterView = function() {
        this_.getMap().getView().setZoom(7.2);
        this_.getMap().getView().setCenter(ol.proj.fromLonLat([-84.0, 9.40]));
    };

    button.addEventListener('click', handleCenterView, false);
    button.addEventListener('touchstart', handleCenterView, false);

    var element = document.createElement('div');
    element.className = 'center-view ol-unselectable ol-control';
    element.appendChild(button);

    ol.control.Control.call(this, {
        element: element,
        target: options.target
    });
};

// Measurement tools
var pointerMoveHandler = function(evt) {
    if (evt.dragging) {
      return;
    }

    var helpMsg = 'Click para iniciar el trazo';

    if (sketch) {
      var geom = (sketch.getGeometry());
      if (geom instanceof Polygon) {
        helpMsg = continuePolygonMsg;
      } else if (geom instanceof LineString) {
        helpMsg = continueLineMsg;
      }
    }

    helpTooltipElement.innerHTML = helpMsg;
    helpTooltip.setPosition(evt.coordinate);

    helpTooltipElement.classList.remove('hidden');
};

var map = new Map({
    projection: "EPSG:5367",
    units: "m",
    loadTilesWhileAnimating: true,
    loadTilesWhileInteracting: true,
    target: 'map',
    layers: [ baseTile ],
    controls: ol.control.defaults({ attribution: false }).extend([
        new ol.control.FullScreen(),
        new ol.control.ScaleLine(),
        new ol.control.ZoomSlider()
        ]),
    view: new ol.View({
      center: ol.proj.fromLonLat([-84.30, 9.80]),
      zoom: 9,
      enableRotation: true
    })
});

map.on('pointermove', pointerMoveHandler);

/*
map.getViewport().addEventListener('mouseout', function() {
helpTooltipElement.classList.add('hidden');
});

var formatLength = function(line) {
    var length = getLength(line);
    var output;
    if (length > 100) {
      output = (Math.round(length / 1000 * 100) / 100) +
          ' ' + 'km';
    } else {
      output = (Math.round(length * 100) / 100) +
          ' ' + 'm';
    }
    return output;
};

var formatArea = function(polygon) {
    var area = getArea(polygon);
    var output;
    if (area > 10000) {
      output = (Math.round(area / 1000000 * 100) / 100) +
          ' ' + 'km<sup>2</sup>';
    } else {
      output = (Math.round(area * 100) / 100) +
          ' ' + 'm<sup>2</sup>';
    }
    return output;
};

function addInteraction() {
    if (typeSelect.value != 'none') {
        var type = (typeSelect.value == 'area' ? 'Polygon' : 'LineString');
        draw = new Draw({
            source: source,
            type: type,
            style: new Style({
                    fill: new Fill({
                    color: 'rgba(255, 255, 255, 0.2)'
                }),
                stroke: new Stroke({
                    color: 'rgba(0, 0, 0, 0.5)',
                    lineDash: [10, 10],
                    width: 2
                }),
                image: new CircleStyle({
                    radius: 5,
                    stroke: new Stroke({
                        color: 'rgba(0, 0, 0, 0.7)'
                    }),
                    fill: new Fill({
                        color: 'rgba(255, 255, 255, 0.2)'
                    })
                })
            })
        });
        map.addInteraction(draw);

        createMeasureTooltip();
        createHelpTooltip();

        var listener;
        draw.on('drawstart',
          function(evt) {
            // set sketch
            sketch = evt.feature;

            var tooltipCoord = evt.coordinate;

            listener = sketch.getGeometry().on('change', function(evt) {
              var geom = evt.target;
              var output;
              if (geom instanceof Polygon) {
                output = formatArea(geom);
                tooltipCoord = geom.getInteriorPoint().getCoordinates();
              } else if (geom instanceof LineString) {
                output = formatLength(geom);
                tooltipCoord = geom.getLastCoordinate();
              }
              measureTooltipElement.innerHTML = output;
              measureTooltip.setPosition(tooltipCoord);
            });
          }, this);

        draw.on('drawend',
          function() {
            measureTooltipElement.className = 'tooltip tooltip-static';
            measureTooltip.setOffset([0, -7]);
            // unset sketch
            sketch = null;
            // unset tooltip so that a new one can be created
            measureTooltipElement = null;
            createMeasureTooltip();
            unByKey(listener);}, this);
    } else {
        map.removeInteraction(draw);
    }
}

function createHelpTooltip() {
    if (helpTooltipElement) {
      helpTooltipElement.parentNode.removeChild(helpTooltipElement);
    }
    helpTooltipElement = document.createElement('div');
    helpTooltipElement.className = 'tooltip hidden';
    helpTooltip = new Overlay({
      element: helpTooltipElement,
      offset: [15, 0],
      positioning: 'center-left'
    });
    map.addOverlay(helpTooltip);
}

function createMeasureTooltip() {
    if (measureTooltipElement) {
      measureTooltipElement.parentNode.removeChild(measureTooltipElement);
    }
    measureTooltipElement = document.createElement('div');
    measureTooltipElement.className = 'tooltip tooltip-measure';
    measureTooltip = new Overlay({
      element: measureTooltipElement,
      offset: [0, -15],
      positioning: 'bottom-center'
    });
    map.addOverlay(measureTooltip);
}

typeSelect.onchange = function() {
    map.removeInteraction(draw);
    addInteraction();
};


*/

loadButton.onclick = function(event) {
    event.preventDefault();

    var dropselection = mapLoadInput.options[mapLoadInput.selectedIndex].value;

    if (dropselection !== 'none' && dropselection !== '') {

        if (!loadedDict[dropselection]){
            paramarray = dropselection.split('|');

            serviceurl = paramarray[0];
            layername = paramarray[1];

            opacval = 1.0;

            newlayer = new ol.layer.Tile({
                opacity: opacval,
                source: new ol.source.TileWMS({
                    url: serviceurl,
                    params: {'LAYERS': layername, 'TILED': true}
                })
            });

            map.addLayer(newlayer);
            loadedDict[dropselection] = true;
            layersDic[dropselection] = newlayer;

            // Also, create a most recent entry in the table
            droptext = mapLoadInput.options[mapLoadInput.selectedIndex].innerHTML;

            row = histTable.insertRow(0);

            btnremove = document.createElement('input');
            btnremove.id = dropselection.concat('-btn');
            btnremove.type = "button";
            btnremove.class = "btn";
            btnremove.value = "X";
            btnremove.onclick =
                function () {
                    // Unpack the ID
                    reflayer = this.id.substring(0, this.id.length - 4);
                    // Remove the map
                    map.removeLayer(layersDic[reflayer]);
                    delete layersDic[reflayer];
                    loadedDict[reflayer] = false;
                    // Remove the whole row I belong to
                    rIndex = this.parentNode.parentNode.rowIndex;
                    histTable.deleteRow(rIndex);
                };

            btnlegend = document.createElement('input');
            btnlegend.id = dropselection.concat('-lgn');
            btnlegend.type = "button";
            btnlegend.class = "btn";
            btnlegend.value = "Leyenda";
            btnlegend.onclick =
                function () {
                    if (! legendOnOff){
                        // Unpack the ID
                        reflayer = this.id.substring(0, this.id.length - 4);

                        // Parse service and data
                        prarray = reflayer.split('|');

                        serurl = prarray[0];
                        layname = prarray[1];

                        if(serurl.includes('?'))
                            specchar = '&';
                        else
                            specchar = '?';

                        // Construct the query
                        qtext = serurl + specchar + 'request=GetLegendGraphic&format=image%2Fpng&layer=' + layname;

                        //testLabel.innerHTML = qtext;

                        // Put the new legend
                        document.getElementById("img-legend").src = qtext;
                        legendOnOff = true;
                    }
                    else {
                        document.getElementById("img-legend").src = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=";
                        legendOnOff = false;
                    }
                };

            sldopacity = document.createElement('input');
            sldopacity.id = dropselection.concat('-sld');
            sldopacity.type = "range";
            sldopacity.class = "slider";
            sldopacity.value = opacval;
            sldopacity.min = 0.0;
            sldopacity.max = 1.0;
            sldopacity.step = 0.05;
            sldopacity.onclick  = function () {
                reflayer = this.id.substring(0, this.id.length - 4);
                layersDic[reflayer].setOpacity(this.value);
            };

            btre = row.insertCell(0);
            btre.appendChild(btnremove);

            lgre = row.insertCell(1);
            lgre.appendChild(btnlegend)

            slre = row.insertCell(2);
            btre.appendChild(sldopacity);

            ftre = row.insertCell(3);
            ftre.innerHTML = droptext
        }
        else {
            testLabel.innerHTML = 'Capa ya cargada';
        }
    }
};

cleanButton.onclick = function(event) {
    event.preventDefault();

    Object.keys(layersDic).forEach(function(key) {
            map.removeLayer(map.removeLayer(layersDic[key]));
            loadedDict = {};
            layersDic = {};
        }
    );

    document.getElementById("img-legend").src = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=";

};
