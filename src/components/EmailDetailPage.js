import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/EmailDetailPage.scss';

function EmailDetailPage() {
  const { id } = useParams();  // URL에서 id 파라미터를 추출
  console.log('Email ID:', id);  // 로그로 id 확인

  const [emailDetails, setEmailDetails] = useState(null);  // 이메일 세부 정보를 저장할 상태

  useEffect(() => {
    async function fetchEmailDetails() {
      console.log(`Fetching details for ID: ${id}`); // Fetching log
      try {
        const response = await fetch(`http://localhost:5000/api/emails/${id}`);
        if (!response.ok) {
          throw new Error('Something went wrong!');
        }
        const data = await response.json();
        setEmailDetails(data);
        console.log('Fetched data:', data); // Fetched data log
      } catch (error) {
        console.error('Error fetching email details:', error);
      }
    }

    if (id && id !== '[object Object]') { // 추가적인 확인 로직
      fetchEmailDetails();
    } else {
      console.log('Invalid ID:', id);
    }
  }, [id]);

  return (
    <div className="email-details">
      {emailDetails ? (
        <div>
          <h1>{emailDetails.subject}</h1>
          <p>From: {emailDetails.from}</p>
          <p>Date Received: {emailDetails.date}</p>
          {emailDetails && emailDetails.attachments && emailDetails.attachments.length > 0 ? (
              <div>
                <h2>Attachments:</h2>
                <ul>
                  {emailDetails.attachments.map((attachment, idx) => (
                    <li key={idx}>{attachment.filename} <a href={attachment.path} download>Download</a>
                    </li>
                  ))}
                </ul>
              </div>
            ) : (
              <p>No attachments</p>
            )}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default EmailDetailPage;
