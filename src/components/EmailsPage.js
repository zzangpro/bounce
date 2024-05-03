import React, { useState, useEffect } from 'react';
import { Table } from 'react-bootstrap';
import Paginate from 'react-paginate';
import { Link } from 'react-router-dom';
import '../styles/EmailsPage.scss';

const EmailsPage = () => {
  const [emails, setEmails] = useState([]);
  const [filteredEmails, setFilteredEmails] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [emailsPerPage] = useState(15); // 페이지당 이메일 수

  useEffect(() => {
    const fetchEmails = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/emails');
        if (!response.ok) {
          throw new Error('Failed to fetch');
        }
        const data = await response.json();
        console.log(data);  // 데이터 구조 확인
        setEmails(data);
        setFilteredEmails(data); // 검색 없이 초기 데이터 설정
      } catch (error) {
        console.error('Error fetching emails:', error);
      }
    };

    fetchEmails();
  }, []);

  // 검색 기능
  const handleSearch = (event) => {
    const value = event.target.value.toLowerCase();
    const filtered = emails.filter(email => email.subject.toLowerCase().includes(value));
    setFilteredEmails(filtered);
    setCurrentPage(0); // 검색시 페이지 초기화
  };

  // 페이지네이션 처리
  const currentEmails = filteredEmails.slice(currentPage * emailsPerPage, (currentPage + 1) * emailsPerPage);

  const pageCount = Math.ceil(filteredEmails.length / emailsPerPage);

  const handlePageClick = (event) => {
    setCurrentPage(event.selected);
  };

  return (
    <div className="emails-container">
      <h2>Imported Emails</h2>
      <input type="text" placeholder="Search emails..." onChange={handleSearch} />
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Subject</th>
            <th>Sender</th>
            <th>Date Received</th>
            <th>Has Attachments</th>
          </tr>
        </thead>
        <tbody>
            {currentEmails.map((email, index) => (
                <tr key={index}>
                    <td><Link to={`/emails/${email._id.$oid || email._id}`}>{email.subject}</Link></td>
                    <td>{email.from}</td>
                    <td>{email.date}</td>
                    <td>{email.attachments && email.attachments.length > 0 ? (
                          email.attachments.map((attachment, idx) => <div key={idx}>{attachment.filename}</div>)
                      ) : (
                          'No attachments'
                      )}</td>
                </tr>
            ))}
        </tbody>
      </Table>
      <Paginate
        previousLabel={'previous'}
        nextLabel={'next'}
        breakLabel={'...'}
        pageCount={pageCount}
        marginPagesDisplayed={2}
        pageRangeDisplayed={5}
        onPageChange={handlePageClick}
        containerClassName={'pagination'}
        subContainerClassName={'pages pagination'}
        activeClassName={'active'}
      />
    </div>
  );
};

export default EmailsPage;
