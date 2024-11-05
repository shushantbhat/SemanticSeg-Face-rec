import React, { useState } from 'react';
import axios from 'axios';
import '../App.css';

function LoginPage({ onLogin }) {
  const [password, setPassword] = useState('');
  const predefinedPassword = '12345';
  const [faceRecognitionStatus, setFaceRecognitionStatus] = useState(null);

  const handlePasswordLogin = () => {
    if (password === predefinedPassword) {
      onLogin();
    } else {
      alert('Incorrect password');
    }
  };

  const handleFaceRecognitionLogin = async () => {
    try {
      setFaceRecognitionStatus("Checking face recognition...");
      const response = await axios.get('http://localhost:5001/face-recognition');
      if (response.data.status === "recognized") {
        setFaceRecognitionStatus("Face recognized. Logging in...");
        onLogin();
      } else {
        setFaceRecognitionStatus("Face not recognized. Try again.");
      }
    } catch (error) {
      console.error("Error during face recognition:", error);
      setFaceRecognitionStatus("Error during face recognition");
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <input 
        type="password" 
        value={password} 
        onChange={(e) => setPassword(e.target.value)} 
        placeholder="Enter Password"
      />
      <button onClick={handlePasswordLogin}>Login with Password</button>
      <button onClick={handleFaceRecognitionLogin}>Login with Face Recognition</button>
      {faceRecognitionStatus && <p className="status-message">{faceRecognitionStatus}</p>}
    </div>
  );
}

export default LoginPage;
