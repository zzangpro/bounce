import React, { useState } from 'react';

const HwpDataProcessor = ({ onProcessed }) => {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setError(null); // 초기화
  };

  const processFile = async () => {
    if (!file) {
      setError("Please upload a HWP file first.");
      return;
    }

    const formData = new FormData();
    formData.append("hwpFile", file);

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/process-hwp', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error('Failed to process file');
      }
      const data = await response.json();
      onProcessed(data); // 추출된 데이터를 상위 컴포넌트로 전달
      setIsLoading(false);
    } catch (error) {
      setError(error.message);
      setIsLoading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} accept=".hwp"/>
      <button onClick={processFile} disabled={isLoading}>
        {isLoading ? 'Processing...' : 'Process HWP File'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default HwpDataProcessor;
