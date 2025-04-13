import './App.css';
import Card from './Card.js';
import Map from './Map.js';
import { useEffect, useState } from 'react';

function App() {
  const [locations, setLocations] = useState([]);

  useEffect(() => {
    fetch(process.env.PUBLIC_URL + '/Housing_data2.csv')
      .then((response) => response.text())
      .then((data) => {
        const rows = data.split('\n').slice(1); // skip header
        const locationList = rows.map(row => {
          const [address, lat, lng] = row.split(',');
          if (!address || !lat || !lng) return null;
          return {
            name: address.trim(), // default to address
            address: address.trim(),
            lat: parseFloat(lat),
            lng: parseFloat(lng),
            propertyType: "Residential" // default
          };
        }).filter(loc => loc !== null);
        setLocations(locationList);
      })
      .catch(err => console.error("CSV load error:", err));
  }, []);

  return (
    <div className="app">
      <Map />
      <div className="cards">
        {locations.map((loc, index) => (
          <Card
            key={index}
            name={loc.name}
            address={loc.address}
            lat={loc.lat}
            lng={loc.lng}
            propertyType={loc.propertyType}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
