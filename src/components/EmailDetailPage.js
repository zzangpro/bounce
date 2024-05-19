import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import '../styles/EmailDetailPage.scss';

const EmailDetailPage = () => {
  const { id } = useParams();
  const [email, setEmail] = useState(null);

  useEffect(() => {
    const fetchEmail = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/emails/${id}`);
        if (!response.ok) {
          throw new Error('Failed to fetch');
        }
        const data = await response.json();
        setEmail(data);
      } catch (error) {
        console.error('Error fetching email:', error);
      }
    };

    fetchEmail();
  }, [id]);

  if (!email) {
    return <div>Loading...</div>;
  }

  return (
    <div className="email-detail-container">
      <h2>{email.subject}</h2>
      <p><strong>From:</strong> {email.from}</p>
      <p><strong>Date:</strong> {email.date}</p>
      <h3>Attachments:</h3>
      <ul>
        {email.attachments && email.attachments.length > 0 ? (
          email.attachments.map((attachment, idx) => (
            <li key={idx}>
              <a href={`http://localhost:5000/api/download/${encodeURIComponent(attachment.filename)}`} download>{attachment.filename}</a>
            </li>
          ))
        ) : (
          <li>No attachments</li>
        )}
      </ul>
      <Link to="/emails">Back to Emails</Link>
    </div>
  );
};

export default EmailDetailPage;
