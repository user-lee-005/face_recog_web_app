import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file to upload");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setMessage(res.data.message);
    } catch (err) {
      setMessage("Error uploading file");
    }
  };

  const handleRecognize = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file to recognize");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    try {
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
      setMessage("Error recognizing file");
    }
  };

  return (
    <div>
      <h1>Face Recognition</h1>
      <form onSubmit={handleUpload}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      <form onSubmit={handleRecognize}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Recognize</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default FileUpload;
