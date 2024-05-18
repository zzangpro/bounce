import React, { useState } from 'react';

const ParaphraseText = ({ onParaphrase }) => {
  const [inputText, setInputText] = useState('');
  const [paraphrasedText, setParaphrasedText] = useState('');

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleParaphrase = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/paraphrase', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) {
        throw new Error('Failed to paraphrase text');
      }

      const data = await response.json();
      setParaphrasedText(data.paraphrased_text);
      onParaphrase(data.paraphrased_text);  // 부모 컴포넌트에 결과 전달
    } catch (error) {
      console.error('Error paraphrasing text:', error);
    }
  };

  return (
    <div>
      <h3>Paraphrase Text</h3>
      <textarea
        rows="4"
        cols="50"
        placeholder="Enter text to paraphrase"
        value={inputText}
        onChange={handleInputChange}
      />
      <button onClick={handleParaphrase}>Paraphrase</button>
      {paraphrasedText && (
        <div>
          <h4>Paraphrased Text</h4>
          <p>{paraphrasedText}</p>
        </div>
      )}
    </div>
  );
};

export default ParaphraseText;
