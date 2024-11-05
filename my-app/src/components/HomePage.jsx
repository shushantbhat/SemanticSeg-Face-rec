import React, { useState } from 'react';
import axios from 'axios';
import '../App.css';

function HomePage() {
  const [image, setImage] = useState(null);
  const [mask, setMask] = useState(null);

  const handleImageUpload = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!image) return alert('Please upload an image');

    const formData = new FormData();
    formData.append('file', image);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setMask(response.data.mask);
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  return (
    <div className="home-container">
      <h2>Upload Image</h2>
      <input type="file" accept="image/*" onChange={handleImageUpload} />
      <button onClick={handleSubmit}>Get Mask</button>
      {mask && <img src={`data:image/png;base64,${mask}`} alt="Mask" />}
    </div>
  );
}

export default HomePage;
