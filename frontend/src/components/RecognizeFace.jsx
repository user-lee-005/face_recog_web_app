import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';

const RecognizeFace = () => {
  const webcamRef = useRef(null);
  const [message, setMessage] = useState('');

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user"
  };

  const capture = useCallback(async (e) => {
    e.preventDefault();
    if (!webcamRef.current) {
      setMessage("No webcam available");
      return;
    }
    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) {
      setMessage("Failed to capture image");
      return;
    }

    try {
      const blob = await fetch(imageSrc).then(res => res.blob());
      const formData = new FormData();
      formData.append("file", blob, "capture.png");

      const res = await axios.post(
        "http://127.0.0.1:5000/recognize",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setMessage(res.data.message);
    } catch (err) {
      console.error(err);
      setMessage("Error recognizing face");
    }
  }, [webcamRef]);

  return (
    <div>
      <h1>Recognize Face</h1>
      <Webcam
        audio={false}
        height={720}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={1280}
        videoConstraints={videoConstraints}
      />
      <button onClick={capture}>Recognize Face</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default RecognizeFace;
