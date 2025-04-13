
// PASTED BELOW
import './Card.css';

const Card = ({ name, address, propertyType, lat, lng }) => {
  const googleMapsAPI_KEY = 'AIzaSyCDm-kHtEIsMQMo_VkGQ3pWDz_eu7S9O-0';

  const getStreetViewImageURL = (lat, lng) => {
    const baseURL = "https://maps.googleapis.com/maps/api/streetview";
    const size = "150x150";
    const location = `${lat},${lng}`;
    return `${baseURL}?size=${size}&location=${location}&key=${googleMapsAPI_KEY}`;
  };

  const displayName = name || address;
  const displayType = propertyType || "Residential";

  return (
    <div className="card">
      <div className="card-left">
        <h4>{displayName}</h4>
        <img
          src={getStreetViewImageURL(lat, lng)}
          alt="Street View"
          className="picture"
        />
      </div>
      <div className="card-right">
        <p><strong>Address:</strong> {address}</p>
        <p className="type"><strong>Property Type:</strong> {displayType}</p>
      </div>
    </div>
  );
};

export default Card;
