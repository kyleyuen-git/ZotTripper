import React, { useRef, useState, useEffect } from 'react';
import {
  GoogleMap,
  LoadScript,
  Autocomplete,
  Marker,
  DirectionsRenderer,
  Polyline,
} from '@react-google-maps/api';
import Card from './Card';

const containerStyle = {
  width: '100%',
  height: '500px',
};

const center = {
  lat: 33.6846,
  lng: -117.8265,
};

const libraries = ['places'];

function haversineDistance(lat1, lng1, lat2, lng2) {
  const toRad = (x) => (x * Math.PI) / 180;
  const R = 6371;
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function Map() {
  const [locations, setLocations] = useState([]);
  const [directions, setDirections] = useState(null);
  const [totalDistance, setTotalDistance] = useState(0);
  const [useWalkingRoute, setUseWalkingRoute] = useState(true);
  const [routeText, setRouteText] = useState('');
  const [selectedMarkerIndex, setSelectedMarkerIndex] = useState(null);
  const autocompleteRef = useRef(null);

  const addLocation = () => {
    const place = autocompleteRef.current.getPlace();
    if (!place || !place.geometry) return;

    const loc = {
      lat: place.geometry.location.lat(),
      lng: place.geometry.location.lng(),
      address: place.formatted_address || place.name,
      name: place.name,
      propertyType: 'Residential',
    };

    setLocations((prev) => [...prev, loc]);
  };

  const clearAll = () => {
    setLocations([]);
    setDirections(null);
    setTotalDistance(0);
    setSelectedMarkerIndex(null);
  };

  const toggleRouteType = () => {
    setUseWalkingRoute((prev) => !prev);
    setDirections(null);
  };

  const geocodeAddress = (address) => {
    return new Promise((resolve) => {
      const geocoder = new window.google.maps.Geocoder();
      geocoder.geocode({ address }, (results, status) => {
        if (status === 'OK') {
          const loc = results[0].geometry.location;
          resolve({
            lat: loc.lat(),
            lng: loc.lng(),
            address: results[0].formatted_address,
            name: results[0].formatted_address,
            propertyType: 'Residential',
          });
        } else {
          console.error('Geocode failed for:', address, status);
          resolve(null);
        }
      });
    });
  };

  const handleUploadRouteText = async () => {
    const addresses = routeText
      .split('->')
      .map((addr) => addr.trim() + ', Irvine, CA, USA')
      .filter(Boolean);

    const newLocations = [];
    for (let address of addresses) {
      const coords = await geocodeAddress(address);
      if (coords) newLocations.push(coords);
    }

    if (newLocations.length > 0) {
      setLocations((prev) => [...prev, ...newLocations]);
    }
  };

  useEffect(() => {
    if (locations.length < 2) return;

    if (useWalkingRoute) {
      const origin = locations[0];
      const destination = locations[locations.length - 1];
      const waypoints = locations.slice(1, -1).map((loc) => ({
        location: { lat: loc.lat, lng: loc.lng },
        stopover: true,
      }));

      const directionsService = new window.google.maps.DirectionsService();
      directionsService.route(
        {
          origin,
          destination,
          waypoints,
          travelMode: window.google.maps.TravelMode.WALKING,
        },
        (result, status) => {
          if (status === 'OK') {
            setDirections(result);
            let distance = 0;
            result.routes[0].legs.forEach((leg) => {
              distance += leg.distance.value;
            });
            setTotalDistance((distance / 1000).toFixed(2));
          } else {
            console.error('Directions request failed:', status);
            setDirections(null);
          }
        }
      );
    } else {
      let distance = 0;
      for (let i = 1; i < locations.length; i++) {
        const prev = locations[i - 1];
        const curr = locations[i];
        distance += haversineDistance(prev.lat, prev.lng, curr.lat, curr.lng);
      }
      setDirections(null);
      setTotalDistance(distance.toFixed(2));
    }
  }, [locations, useWalkingRoute]);

  return (
    <LoadScript googleMapsApiKey="AIzaSyCDm-kHtEIsMQMo_VkGQ3pWDz_eu7S9O-0" libraries={libraries}>
      <div style={{ marginBottom: 10 }}>
        <Autocomplete onLoad={(ref) => (autocompleteRef.current = ref)}>
          <input
            type="text"
            placeholder="Add Location"
            style={{ width: 300, marginRight: 10 }}
          />
        </Autocomplete>
        <button onClick={addLocation}>Add</button>
        <button onClick={toggleRouteType} style={{ marginLeft: 10 }}>
          Use {useWalkingRoute ? 'Straight Line' : 'Walking Route'}
        </button>
        <button onClick={clearAll} style={{ marginLeft: 10 }}>
          Clear All
        </button>
      </div>

      <div style={{ marginBottom: 10 }}>
        <textarea
          rows={4}
          cols={100}
          value={routeText}
          placeholder="Paste route text here (e.g., A -> B -> C)"
          onChange={(e) => setRouteText(e.target.value)}
        />
        <br />
        <button onClick={handleUploadRouteText}>Upload Route</button>
      </div>

      <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={13}>
        {locations.map((loc, idx) => (
          <Marker
            key={idx}
            position={loc}
            icon={{
              url: 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png',
            }}
            label={{
              text: `${idx + 1}`,
              color: 'white',
              fontSize: '14px',
              fontWeight: 'bold',
            }}
            onClick={() => setSelectedMarkerIndex(idx)}
          />


        ))}
        {useWalkingRoute && directions && <DirectionsRenderer directions={directions} />}
        {!useWalkingRoute && locations.length > 1 && (
          <Polyline
            path={locations}
            options={{ strokeColor: '#FF0000', strokeOpacity: 1.0, strokeWeight: 2 }}
          />
        )}
      </GoogleMap>

      {locations.length > 1 && (
        <div style={{ marginTop: 10 }}>
          Total {useWalkingRoute ? 'walking' : 'straight-line'} distance:{' '}
          <strong>{totalDistance} km</strong>
        </div>
      )}

      {selectedMarkerIndex !== null && locations[selectedMarkerIndex] && (
        <div style={{ marginTop: 20 }}>
          <Card {...locations[selectedMarkerIndex]} />
        </div>
      )}
    </LoadScript>
  );
}

export default Map;
